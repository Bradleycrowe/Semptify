from flask import Flask, render_template, request, redirect, send_file, jsonify, abort
import os
from datetime import datetime
import json
import requests
import time
import threading

# In-memory metrics (simple counters; reset on restart)
METRICS = {
    'requests_total': 0,
    'admin_requests_total': 0,
    'admin_actions_total': 0,
    'errors_total': 0,
    'releases_total': 0,
}
_metrics_lock = threading.Lock()

def _inc(metric: str, amt: int = 1):
    with _metrics_lock:
        METRICS[metric] = METRICS.get(metric, 0) + amt

def _metrics_text() -> str:
    lines = []
    for k, v in METRICS.items():
        lines.append(f"{k} {v}")
    return "\n".join(lines) + "\n"

app = Flask(__name__)

# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def _append_log(line: str):
    log_path_local = os.path.join("logs", "init.log")
    timestamp_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path_local, "a") as f:
        f.write(f"[{timestamp_local}] {line}\n")

def _event_log(event: str, **fields):
    """Structured JSON event log (append-only)."""
    log_path = os.path.join('logs', 'events.log')
    payload = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event': event,
        **fields
    }
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        _append_log(f"event_log_error {e}")

# Security mode: "open" (no admin token enforced) or "enforced"
SECURITY_MODE = os.environ.get("SECURITY_MODE", "open").lower()
if SECURITY_MODE not in ("open", "enforced"):
    SECURITY_MODE = "open"

# Log initialization (and security mode)
_append_log(f"SemptifyGUI initialized with folders: {', '.join(folders)} | security_mode={SECURITY_MODE}")

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
        "time": datetime.utcnow().isoformat(),
        "folders": folders,
    }), 200

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


def _get_admin_token():
    return app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')

def _is_authorized(req) -> bool:
    """Return True if request is authorized for admin access under current security mode.

    open mode: always True (logged for audit)
    enforced mode: token (query/header/form) must match ADMIN_TOKEN
    """
    if SECURITY_MODE == "open":
        return True
    supplied = req.args.get('token') or req.headers.get('X-Admin-Token') or req.form.get('token')
    return supplied == _get_admin_token()

def _require_admin_or_401():
    if not _is_authorized(request):
        _append_log(f"UNAUTHORIZED admin attempt path={request.path} ip={request.remote_addr}")
        _event_log('admin_unauthorized', path=request.path, ip=request.remote_addr)
        _inc('errors_total')
        return False
    if SECURITY_MODE == "open":
        # Still log accesses to admin endpoints while open
        _append_log(f"OPEN_MODE admin access path={request.path} ip={request.remote_addr}")
    _inc('admin_requests_total')
    return True


@app.route('/admin', methods=['GET'])
def admin():
    # Simple token check
    if not _require_admin_or_401():
        return "Unauthorized", 401

    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    ci_url = f"https://github.com/{owner}/{repo}/actions"
    pages_url = f"https://{owner}.github.io/{repo}/"
    return render_template('admin.html',
                           ci_url=ci_url,
                           pages_url=pages_url,
                           folders=folders,
                           security_mode=SECURITY_MODE,
                           admin_token=_get_admin_token())


@app.route('/release_now', methods=['POST'])
def release_now():
    if not _require_admin_or_401():
        return "Unauthorized", 401

    # Soft confirmation: require hidden field confirm_release=yes
    if request.form.get('confirm_release') != 'yes':
        return abort(400, description="Missing confirmation field")

    github_token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    if not github_token:
        _append_log('release_now failed: missing GITHUB_TOKEN')
        return "GITHUB_TOKEN not configured on server", 500

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get latest commit SHA from default branch (main)
    ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main'
    r = requests.get(ref_url, headers=headers)
    if r.status_code != 200:
        _append_log(f'release_now failed: cannot read ref: {r.status_code}')
        return f'Failed to read ref: {r.status_code}', 500
    sha = r.json().get('object', {}).get('sha')

    # Create a timestamped tag
    tag_name = f'v{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    create_ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs'
    payload = { 'ref': f'refs/tags/{tag_name}', 'sha': sha }
    r = requests.post(create_ref_url, headers=headers, json=payload)
    if r.status_code in (201, 200):
        _append_log(f'Created tag {tag_name} via API')
        _event_log('release_created', tag=tag_name, sha=sha, ip=request.remote_addr)
        _inc('releases_total')
        _inc('admin_actions_total')
        # record release in release-log.json
        log_path = os.path.join('logs', 'release-log.json')
        entry = { 'tag': tag_name, 'sha': sha, 'timestamp': datetime.utcnow().isoformat() }
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
    if not _require_admin_or_401():
        return "Unauthorized", 401

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
        return "Unauthorized", 401
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
        return "Unauthorized", 401
    _inc('admin_requests_total')
    sbom_dir = os.path.join('.', 'sbom')
    files = []
    if os.path.exists(sbom_dir):
        files = sorted(os.listdir(sbom_dir), reverse=True)
    return render_template('sbom_list.html', files=files)


@app.route('/sbom/<path:filename>')
def sbom_get(filename):
    if not _require_admin_or_401():
        return "Unauthorized", 401
    _inc('admin_requests_total')
    sbom_dir = os.path.join('.', 'sbom')
@app.route('/offline')
def offline():
    # Simple offline fallback route (also cached by SW if added there)
    _inc('requests_total')
    return "You are offline. Limited functionality.", 200, { 'Content-Type': 'text/plain' }
    path = os.path.join(sbom_dir, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Not found", 404

if __name__ == "__main__":
    app.run(debug=True)
