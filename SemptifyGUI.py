from flask import Flask, render_template, request, redirect, send_file, jsonify, abort, session
import os
from datetime import datetime, timezone
import json
import requests
import time
import threading
import hashlib
from collections import deque, defaultdict
from typing import Optional, Callable

# -----------------------------
# Rate limiting (simple sliding window) & config
# -----------------------------
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get('ADMIN_RATE_WINDOW', '60'))
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get('ADMIN_RATE_MAX', '60'))  # per window per IP
RATE_LIMIT_STATUS = int(os.environ.get('ADMIN_RATE_STATUS', '429'))  # HTTP status for rate limiting
RATE_LIMIT_RETRY_AFTER = int(os.environ.get('ADMIN_RATE_RETRY_AFTER', os.environ.get('ADMIN_RATE_WINDOW', '60')))  # seconds clients should wait before retry
_RATE_HISTORY = defaultdict(lambda: deque())  # key -> deque[timestamps]
_rate_lock = threading.Lock()

def _rate_limit(key: str) -> bool:
    """Return True if allowed, False if over limit."""
    if RATE_LIMIT_MAX_REQUESTS <= 0:
        return True
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    with _rate_lock:
        dq = _RATE_HISTORY[key]
        # Purge old
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= RATE_LIMIT_MAX_REQUESTS:
            return False
        dq.append(now)
    return True

# In-memory metrics (simple counters; reset on restart)
METRICS = {
    'requests_total': 0,
    'admin_requests_total': 0,
    'admin_actions_total': 0,
    'errors_total': 0,
    'releases_total': 0,
    'rate_limited_total': 0,
    'breakglass_used_total': 0,
    'token_rotations_total': 0,
}
_metrics_lock = threading.Lock()
_START_TIME = time.time()

def _inc(metric: str, amt: int = 1):
    with _metrics_lock:
        METRICS[metric] = METRICS.get(metric, 0) + amt

def _metrics_text() -> str:
    # Expose simple Prometheus style with HELP/TYPE
    help_map = {
        'requests_total': 'Total HTTP requests (all endpoints)',
        'admin_requests_total': 'Total authenticated admin requests',
        'admin_actions_total': 'Total mutating admin actions performed',
        'errors_total': 'Total error responses (admin + general)',
        'releases_total': 'Total release tags created via UI',
        'rate_limited_total': 'Total admin requests blocked by rate limiting',
        'breakglass_used_total': 'Total successful break-glass authentications',
        'token_rotations_total': 'Total admin token rotations executed'
    }
    lines = []
    for k, v in METRICS.items():
        if k in help_map:
            lines.append(f"# HELP {k} {help_map[k]}")
            lines.append(f"# TYPE {k} counter")
        lines.append(f"{k} {v}")
    # Dynamic uptime gauge (not stored in METRICS since it changes continuously)
    uptime = int(time.time() - _START_TIME)
    lines.append("# HELP uptime_seconds Application uptime in seconds")
    lines.append("# TYPE uptime_seconds gauge")
    lines.append(f"uptime_seconds {uptime}")
    return "\n".join(lines) + "\n"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Make template/static paths explicit so deployment environments with different CWDs still resolve correctly
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
# Secret key for session/CSRF (set FLASK_SECRET in production)
app.secret_key = os.environ.get('FLASK_SECRET', os.urandom(32))

# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def _utc_now():
    """Return an aware UTC datetime."""
    return datetime.now(timezone.utc)

def _utc_now_iso():
    """Return RFC3339-ish UTC timestamp with trailing Z."""
    return _utc_now().isoformat().replace('+00:00', 'Z')

def _rotate_if_needed(path: str):
    max_bytes = int(os.environ.get('LOG_MAX_BYTES', '1048576'))  # 1 MB default
    if not os.path.exists(path):
        return
    try:
        size = os.path.getsize(path)
        if size < max_bytes:
            return
        ts = _utc_now().strftime('%Y%m%d%H%M%S')
        rotated = f"{path}.{ts}"
        os.rename(path, rotated)
    except Exception:
        # Silent failure; rotation is best-effort
        pass

def _append_log(line: str):
    log_path_local = os.path.join("logs", "init.log")
    _rotate_if_needed(log_path_local)
    timestamp_local = _utc_now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path_local, "a") as f:
        f.write(f"[{timestamp_local}] {line}\n")

def _event_log(event: str, **fields):
    """Structured JSON event log (append-only)."""
    log_path = os.path.join('logs', 'events.log')
    _rotate_if_needed(log_path)
    payload = {
        'ts': _utc_now_iso(),
        'event': event,
        **fields
    }
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        _append_log(f"event_log_error {e}")

# -----------------------------
# Simple .env loader (no external dependency) executed *before* using env vars in prod runner
# -----------------------------
def load_dotenv(path: str = '.env') -> None:
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r') as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)  # do not override existing explicit env
    except Exception as e:  # pragma: no cover
        _append_log(f"dotenv_load_error {e}")

# Attempt to load .env from project root (idempotent)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

def _current_security_mode():
    mode = os.environ.get("SECURITY_MODE", "open").lower()
    if mode not in ("open", "enforced"):
        mode = "open"
    return mode

# Security mode snapshot used only for initial startup log; all runtime checks call _current_security_mode()
SECURITY_MODE = _current_security_mode()

# Log initialization (and security mode)
_append_log(f"SemptifyGUI initialized with folders: {', '.join(folders)} | security_mode={SECURITY_MODE}")
try:
    # Log a quick inventory of key template & static assets to aid remote diagnostics
    index_tpl = os.path.join(app.template_folder, 'index.html')
    admin_tpl = os.path.join(app.template_folder, 'admin.html')
    manifest_path = os.path.join(app.static_folder, 'manifest.webmanifest')
    _append_log(
        "asset_check "
        f"index_exists={os.path.exists(index_tpl)} "
        f"admin_exists={os.path.exists(admin_tpl)} "
        f"manifest_exists={os.path.exists(manifest_path)}"
    )
except Exception as e:  # pragma: no cover (best effort)
    _append_log(f"asset_check_error {e}")

# -----------------------------
# Security headers middleware
# -----------------------------
@app.after_request
def _set_security_headers(resp):  # pragma: no cover (headers logic simple)
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resp.headers.setdefault('X-Frame-Options', 'DENY')
    resp.headers.setdefault('Referrer-Policy', 'no-referrer')
    resp.headers.setdefault('X-XSS-Protection', '0')  # modern browsers ignore / CSP recommended
    # Mild default CSP allowing same-origin scripts/styles/images & data: images
    csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    resp.headers.setdefault('Content-Security-Policy', csp)
    return resp

@app.route("/")
def index():
    # Use a Jinja2 template so UI can be extended without changing the route.
    message = "SemptifyGUI is live. Buttons coming next."
    _inc('requests_total')
    return render_template("index.html", message=message, folders=folders)


@app.route("/health")
def health():
    _inc('requests_total')
    return "OK", 200

@app.route("/healthz")
def healthz():
    _inc('requests_total')
    return jsonify({
        "status": "ok",
        "time": _utc_now_iso(),
        "folders": folders,
    }), 200

@app.route('/readyz')
def readyz():
    """Readiness probe verifying writable runtime dirs & token file load."""
    _inc('requests_total')
    writable = {}
    for d in folders:
        test_file = os.path.join(d, '.readyz.tmp')
        try:
            with open(test_file, 'w') as f:
                f.write('ok')
            os.remove(test_file)
            writable[d] = True
        except Exception:
            writable[d] = False
    tokens_ok = True
    try:
        _load_tokens(force=True)
    except Exception:
        tokens_ok = False
    status_ok = all(writable.values()) and tokens_ok
    return jsonify({
        'status': 'ready' if status_ok else 'degraded',
        'writable': writable,
        'tokens_load': tokens_ok,
        'time': _utc_now_iso()
    }), 200 if status_ok else 503

def _rate_or_unauth_response():
    """Return a standardized JSON response for rate limited or unauthorized admin access."""
    if getattr(request, '_rate_limited', False):
        return (jsonify({'error': 'rate_limited', 'retry_after': RATE_LIMIT_RETRY_AFTER}),
                RATE_LIMIT_STATUS,
                {'Retry-After': str(RATE_LIMIT_RETRY_AFTER)})
    return jsonify({'error': 'unauthorized'}), 401

@app.errorhandler(500)
def internal_error(e):  # pragma: no cover (framework error path)
    # Provide a lightweight JSON response for API clients while logging root cause
    _append_log(f"ERROR_500 path={request.path} error={e}")
    _event_log('error_500', path=request.path, msg=str(e))
    # If it's a template resolution problem, hint at likely cause
    hint = ''
    if 'TemplateNotFound' in str(e):
        hint = ' (template not found – ensure templates/ directory is deployed)'
    return ("An internal server error occurred" + hint, 500)

@app.route("/version")
def version():
    _inc('requests_total')
    git_sha = os.environ.get("GIT_SHA", "unknown")
    build_time = os.environ.get("BUILD_TIME", "unknown")
    return jsonify({
        "git_sha": git_sha,
        "build_time": build_time,
        "app": "SemptifyGUI"
    }), 200

@app.route('/metrics')
def metrics():
    _inc('requests_total')
    txt = _metrics_text()
    return txt, 200, { 'Content-Type': 'text/plain; version=0.0.4' }


TOKENS_CACHE = { 'loaded_at': 0, 'tokens': [], 'path': os.path.join('security','admin_tokens.json'), 'mtime': None }

def _hash_token(raw: str) -> str:
    return 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest()

def _load_tokens(force: bool=False):
    path = TOKENS_CACHE['path']
    try:
        if not os.path.exists(path):
            if force:
                TOKENS_CACHE['tokens'] = []
            return
        mtime = os.path.getmtime(path)
        if force or TOKENS_CACHE['mtime'] != mtime:
            with open(path,'r') as f:
                data = json.load(f)
            # Normalize
            norm = []
            for entry in data:
                if not entry.get('enabled', True):
                    continue
                h = entry.get('hash')
                if not h:
                    continue
                norm.append({
                    'id': entry.get('id','unknown'),
                    'hash': h,
                    'breakglass': entry.get('breakglass', False)
                })
            TOKENS_CACHE['tokens'] = norm
            TOKENS_CACHE['mtime'] = mtime
    except Exception as e:
        _append_log(f"token_load_error {e}")

def _match_token(raw: str):
    if raw is None:
        return None
    _load_tokens()
    h = _hash_token(raw)
    for t in TOKENS_CACHE['tokens']:
        if t['hash'] == h:
            return t
    return None

def _get_admin_token_legacy():
    # Legacy single-token fallback
    return app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')

def _is_authorized(req) -> bool:
    """Authorization logic with multi-token & optional break-glass.

    open mode: always True.
    enforced: verify against tokens file (hash matches). If no file, fallback to legacy single token.
    break-glass: requires security/breakglass.flag present AND token marked breakglass.
    After successful break-glass use, flag file is removed (one-shot) and event logged.
    """
    if _current_security_mode() == "open":
        return True
    supplied = req.args.get('token') or req.headers.get('X-Admin-Token') or req.form.get('token')
    # Primary multi-token path
    token_entry = _match_token(supplied)
    if token_entry:
        _event_log('admin_auth', method='multi-token', token_id=token_entry['id'], path=req.path, ip=req.remote_addr)
        return True
    # Break-glass path
    flag_path = os.path.join('security','breakglass.flag')
    if os.path.exists(flag_path):
        token_entry = _match_token(supplied)
        if token_entry and token_entry.get('breakglass'):
            try:
                os.remove(flag_path)
            except OSError:
                pass
            _event_log('breakglass_used', token_id=token_entry['id'], path=req.path, ip=req.remote_addr)
            _inc('breakglass_used_total')
            return True
    # Legacy single token fallback (for transitional period)
    legacy = _get_admin_token_legacy()
    if supplied == legacy:
        _event_log('admin_auth', method='legacy-token', token_id='legacy', path=req.path, ip=req.remote_addr)
        return True
    return False

# -----------------------------
# GitHub API helper with retry/backoff (minimal)
# -----------------------------
def _github_request(method: str, url: str, headers: dict, json_payload: Optional[dict] = None, attempts: int = 3, backoff: float = 0.6):
    for i in range(1, attempts + 1):
        try:
            if method == 'GET':
                r = requests.get(url, headers=headers, timeout=10)
            else:
                r = requests.post(url, headers=headers, json=json_payload, timeout=15)
            if r.status_code >= 500 and i < attempts:
                time.sleep(backoff * i)
                continue
            return r
        except requests.RequestException as e:  # pragma: no cover (network failure path)
            if i == attempts:
                raise
            time.sleep(backoff * i)
    # Should not reach here
    raise RuntimeError('github_request_exhausted')

def _simulate_release_for_test(owner: str, repo: str) -> str:
    tag_name = f"vTEST-{_utc_now().strftime('%Y%m%d%H%M%S')}"
    log_path = os.path.join('logs', 'release-log.json')
    entry = { 'tag': tag_name, 'sha': 'testing-sha', 'timestamp': _utc_now_iso(), 'simulated': True }
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                data = json.load(f)
        else:
            data = []
        data.insert(0, entry)
        with open(log_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:  # pragma: no cover
        _append_log(f'sim_release_write_fail {e}')
    _append_log(f'Simulated release tag {tag_name} (TESTING mode)')
    _event_log('release_simulated', tag=tag_name)
    return tag_name

def _require_admin_or_401():
    if not _is_authorized(request):
        _append_log(f"UNAUTHORIZED admin attempt path={request.path} ip={request.remote_addr}")
        _event_log('admin_unauthorized', path=request.path, ip=request.remote_addr)
        _inc('errors_total')
        return False
    # Apply rate limiting AFTER auth so attackers do not cause noise with unauth attempts
    rl_key = f"admin:{request.remote_addr}:{request.path}"
    if not _rate_limit(rl_key):
        _append_log(f"RATE_LIMIT path={request.path} ip={request.remote_addr}")
        _event_log('rate_limited', path=request.path, ip=request.remote_addr)
        _inc('errors_total')
        _inc('rate_limited_total')
        # Store marker so caller can translate to proper HTTP status
        request._rate_limited = True  # pylint: disable=protected-access
        return False
    if _current_security_mode() == "open":
        # Still log accesses to admin endpoints while open
        _append_log(f"OPEN_MODE admin access path={request.path} ip={request.remote_addr}")
    _inc('admin_requests_total')
    return True

def _get_or_create_csrf_token():
    token = session.get('_csrf_token')
    if not token:
        token = hashlib.sha256(os.urandom(32)).hexdigest()
        session['_csrf_token'] = token
    return token

def _validate_csrf(req):
    # Only enforce CSRF for state-changing POST requests when enforced mode is active
    if _current_security_mode() != 'enforced':
        return True
    sent = req.form.get('csrf_token') or req.headers.get('X-CSRF-Token')
    token = session.get('_csrf_token')
    if not token or not sent or sent != token:
        _append_log(f"CSRF_FAIL path={req.path} ip={req.remote_addr}")
        _event_log('csrf_fail', path=req.path, ip=req.remote_addr)
        _inc('errors_total')
        return False
    return True


@app.route('/admin', methods=['GET'])
def admin():
    # Simple token check
    if not _require_admin_or_401():
        return _rate_or_unauth_response()

    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    ci_url = f"https://github.com/{owner}/{repo}/actions"
    pages_url = f"https://{owner}.github.io/{repo}/"
    # Expose token ids (not hashes) for visibility if enforced
    _load_tokens()
    token_ids = [t['id'] + (' (breakglass)' if t.get('breakglass') else '') for t in TOKENS_CACHE['tokens']]
    csrf_token = _get_or_create_csrf_token()
    return render_template('admin.html',
                           ci_url=ci_url,
                           pages_url=pages_url,
                           folders=folders,
                           security_mode=_current_security_mode(),
                           token_ids=token_ids,
                           admin_token=_get_admin_token_legacy(),
                           csrf_token=csrf_token)

@app.route('/admin/status')
def admin_status():
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    _inc('admin_requests_total')
    _load_tokens()
    token_summaries = [{'id': t['id'], 'breakglass': t.get('breakglass', False)} for t in TOKENS_CACHE['tokens']]
    return jsonify({
        'security_mode': _current_security_mode(),
        'metrics': METRICS,
        'tokens': token_summaries,
        'time': _utc_now_iso()
    })


@app.route('/release_now', methods=['POST'])
def release_now():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    if not _require_admin_or_401():
        return _rate_or_unauth_response()

    # Soft confirmation: require hidden field confirm_release=yes
    if request.form.get('confirm_release') != 'yes':
        return abort(400, description="Missing confirmation field")

    github_token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    if not github_token:
        # In test mode simulate a successful release so tests can pass without secret
        if app.config.get('TESTING'):
            tag_name = _simulate_release_for_test(owner, repo)
            _inc('releases_total')
            _inc('admin_actions_total')
            return redirect(f'https://github.com/{owner}/{repo}/releases/tag/{tag_name}')
        _append_log('release_now failed: missing GITHUB_TOKEN')
        return "GITHUB_TOKEN not configured on server", 500

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get latest commit SHA from default branch (main)
    ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main'
    r = _github_request('GET', ref_url, headers=headers)
    if r.status_code != 200:
        _append_log(f'release_now failed: cannot read ref: {r.status_code}')
        return f'Failed to read ref: {r.status_code}', 500
    sha = r.json().get('object', {}).get('sha')

    # Create a timestamped tag
    tag_name = f'v{_utc_now().strftime("%Y%m%d%H%M%S")}'
    create_ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs'
    payload = { 'ref': f'refs/tags/{tag_name}', 'sha': sha }
    r = _github_request('POST', create_ref_url, headers=headers, json_payload=payload)
    if r.status_code in (201, 200):
        _append_log(f'Created tag {tag_name} via API')
        _event_log('release_created', tag=tag_name, sha=sha, ip=request.remote_addr)
        _inc('releases_total')
        _inc('admin_actions_total')
        # record release in release-log.json
        log_path = os.path.join('logs', 'release-log.json')
        entry = { 'tag': tag_name, 'sha': sha, 'timestamp': _utc_now_iso() }
        try:
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            data.insert(0, entry)
            with open(log_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            _append_log(f'Failed to write release-log.json: {e}')

        return redirect(f'https://github.com/{owner}/{repo}/releases/tag/{tag_name}')
    else:
        _append_log(f'Failed to create tag: {r.status_code} {r.text}')
        return f'Failed to create tag: {r.status_code}', 500


@app.route('/trigger_workflow', methods=['POST'])
def trigger_workflow():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    if not _require_admin_or_401():
        return _rate_or_unauth_response()

    if request.form.get('confirm_trigger') != 'yes':
        return abort(400, description="Missing confirmation field")

    workflow = request.form.get('workflow', 'ci.yml')
    ref = request.form.get('ref', 'main')
    github_token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    if not github_token:
        return "GITHUB_TOKEN not configured", 500

    headers = { 'Authorization': f'token {github_token}', 'Accept': 'application/vnd.github.v3+json' }
    dispatch_url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches'
    payload = { 'ref': ref }
    r = requests.post(dispatch_url, headers=headers, json=payload)
    if r.status_code in (204, 201):
        _append_log(f'Triggered workflow {workflow} on {ref}')
        _event_log('workflow_dispatch', workflow=workflow, ref=ref, ip=request.remote_addr)
        _inc('admin_actions_total')
        return redirect(f'https://github.com/{owner}/{repo}/actions')
    else:
        _append_log(f'Failed to trigger workflow {workflow}: {r.status_code} {r.text}')
        return f'Failed to trigger workflow: {r.status_code}', 500


@app.route('/release_history')
def release_history():
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    _inc('admin_requests_total')
    log_path = os.path.join('logs', 'release-log.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
    else:
        data = []
    return render_template('release_history.html', data=data)


@app.route('/sbom')
def sbom_list():
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    _inc('admin_requests_total')
    sbom_dir = os.path.join('.', 'sbom')
    files = []
    if os.path.exists(sbom_dir):
        files = sorted(os.listdir(sbom_dir), reverse=True)
    supplied = request.args.get('token') or request.form.get('token') or request.headers.get('X-Admin-Token')
    return render_template('sbom_list.html', files=files, token=supplied)

@app.route('/sbom/<path:filename>')
def sbom_get(filename):
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    _inc('admin_requests_total')
    sbom_dir = os.path.join('.', 'sbom')
    path = os.path.join(sbom_dir, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Not found", 404

@app.route('/offline')
def offline():
    # Simple offline fallback route (also cached by SW if added there)
    _inc('requests_total')
    return "You are offline. Limited functionality.", 200, { 'Content-Type': 'text/plain' }

# -----------------------------
# Token rotation endpoint
# -----------------------------
def _write_tokens(tokens: list):
    path = TOKENS_CACHE['path']
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(tokens, f, indent=2)
        # force reload
        _load_tokens(force=True)
    except Exception as e:
        _append_log(f"token_write_error {e}")

@app.route('/rotate_token', methods=['POST'])
def rotate_token():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    # current auth token already validated; now require target id & new token value
    target_id = request.form.get('target_id')
    new_value = request.form.get('new_value')
    if not target_id or not new_value:
        return "Missing target_id or new_value", 400
    path = TOKENS_CACHE['path']
    if not os.path.exists(path):
        return "Token file missing", 400
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return f"Failed to read tokens: {e}", 500
    found = False
    for entry in data:
        if entry.get('id') == target_id:
            entry['hash'] = _hash_token(new_value)
            found = True
            break
    if not found:
        return "Target token id not found", 404
    _write_tokens(data)
    _event_log('token_rotated', token_id=target_id, ip=request.remote_addr)
    _inc('token_rotations_total')
    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)
