from flask import Flask, render_template, request, redirect, send_file, jsonify, abort, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone
import json
import requests
import time
import base64
import secrets
import threading
import hashlib
import uuid
from collections import deque, defaultdict
from typing import Optional, Callable
from ron_providers import get_provider
import subprocess
import shlex
from modules.law_notes.mn_jurisdiction_checklist import mn_check
from modules.law_notes.law_notes_actions import law_notes_actions
from modules.law_notes.evidence_packet_builder import evidence_packet_builder
from modules.law_notes.evidence_metadata import evidence_meta
from modules.law_notes.complaint_templates import complaint_templates
from modules.law_notes.attorney_trail import attorney_trail

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

# Register law_notes Blueprints
try:
    from modules.law_notes.mn_jurisdiction_checklist import mn_jurisdiction_checklist_bp
    app.register_blueprint(mn_jurisdiction_checklist_bp)
except ImportError:
    pass
try:
    from modules.law_notes.law_notes_actions import law_notes_actions_bp
    app.register_blueprint(law_notes_actions_bp)
except ImportError:
    pass
try:
    from modules.law_notes.evidence_packet_builder import evidence_packet_builder_bp
    app.register_blueprint(evidence_packet_builder_bp)
except ImportError:
    pass
try:
    from modules.law_notes.evidence_metadata import evidence_metadata_bp
    app.register_blueprint(evidence_metadata_bp)
except ImportError:
    pass
try:
    from modules.law_notes.complaint_templates import complaint_templates_bp
    app.register_blueprint(complaint_templates_bp)
except ImportError:
    pass
try:
    from modules.law_notes.attorney_trail import attorney_trail_bp
    app.register_blueprint(attorney_trail_bp)
except ImportError:
    pass

# Optional data root for shared storage (e.g., NFS/volume mount) to enable horizontal scaling
_DATA_ROOT = os.environ.get('SEMPTIFY_DATA_ROOT')
if _DATA_ROOT:
    try:
        os.makedirs(_DATA_ROOT, exist_ok=True)
        os.chdir(_DATA_ROOT)
    except OSError:
        # Best-effort; fall back to current working directory
        pass

# Route to render all law_notes modules together
@app.route('/law_notes/all_modules')
def law_notes_all_modules():
    # Use the same context data as the modules, not their view functions
    checklist = {
        'title': "Minnesota Jurisdiction Checklist",
        'state_statutes': [
            "Minn. Stat. Ch. 504B - Residential landlord and tenant",
            "Minn. Stat. Ch. 327A - Eviction procedure references",
            "Minn. Stat. Ch. 325F - Consumer protections where relevant"
        ],
        'local_actions': [
            "Check city rental licensing (Minneapolis, St. Paul)",
            "Lookup local code enforcement complaint process",
            "Confirm filing venue and service rules for housing court"
        ],
        'filing_steps': [
            "Record issue with dates and evidence",
            "Send demand letter per statute and local form",
            "File administrative complaint or small claims/civil filing as needed"
        ]
    }
    address = ''

    module = {
        'title': 'Evidence Packet Builder',
        'sections': [
            {'heading':'Upload Evidence','text':'Attach photos, documents, audio, or video files that support your complaint.'},
            {'heading':'Organize by Violation','text':'Group evidence by issue: late fees, unsafe conditions, retaliation, or harassment.'},
            {'heading':'Export Packet','text':'Generate a printable, multilingual packet for regulators, attorneys, or court.'}
        ],
        'buttons': [
            {'label':'Upload Files','action':'/upload_evidence'},
            {'label':'Group by Violation','action':'/group_evidence'},
            {'label':'Export Packet','action':'/export_evidence_packet'},
            {'label':'Multilingual Export','action':'/export_multilingual'}
        ]
    }

    template = {
        'title': 'Late Fee Challenge - Minnesota',
        'citation': 'Minn. Stat. Ch. 504B; local ordinance',
        'body': 'Facts: [dates]; Legal basis: landlord failed to follow statutory notice and fee limits; Request: refund, correction, and penalty where applicable.'
    }
    lang = 'en'

    metadata = [
        {'filename': 'file1.pdf', 'violation_tag': 'Late Notice', 'timestamp_utc': '2025-10-16T12:00:00Z'},
        {'filename': 'file2.pdf', 'violation_tag': 'Unlawful Entry', 'timestamp_utc': '2025-10-16T13:00:00Z'}
    ]

    attorney_content = {
        'title': 'Attorney Trail',
        'steps': [
            'Identify claims and jurisdiction',
            'Collect evidence packet',
            'Prepare retainer outline and jurisdiction-specific deadlines',
            'Draft cover memo for attorney review'
        ]
    }

    return render_template(
        'law_notes/semptify_all_modules.html',
        checklist=checklist,
        address=address,
        module=module,
        template=template,
        lang=lang,
        title='Evidence Packet Cover',
        generated_at='2025-10-16',
        translation_method='Manual',
        reviewer='Attorney Smith',
        metadata=metadata,
        attorney_content=attorney_content
    )
# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def _bootstrap_tokens_if_needed():
    """If in enforced mode and tokens file missing but ADMIN_TOKEN env provided, create a single-entry tokens file.
    This eases first-time hardened deployments without manually crafting JSON. Idempotent: does nothing if file exists.
    """
    if _current_security_mode() != 'enforced':
        return
    path = os.path.join('security','admin_tokens.json')
    if os.path.exists(path):
        return
    legacy = os.environ.get('ADMIN_TOKEN')
    if not legacy:
        return
    entry = [{ 'id': 'legacy-bootstrap', 'hash': _hash_token(legacy), 'enabled': True }]
    try:
        with open(path,'w', encoding='utf-8') as f:
            json.dump(entry, f, indent=2)
        _append_log('Bootstrapped admin_tokens.json from ADMIN_TOKEN env (legacy-bootstrap)')
        _event_log('tokens_bootstrap_created')
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f'tokens_bootstrap_failed {e}')

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
    except OSError:
        # Silent failure; rotation is best-effort
        pass

# -----------------------------
# Help panel settings storage
# -----------------------------
HELP_PANEL_CACHE = {
    'path': os.path.join('security', 'help_panel.json'),
    'mtime': None,
    'data': None
}

def _help_panel_load(force: bool=False) -> dict:
    path = HELP_PANEL_CACHE['path']
    if not os.path.exists(path):
        return {}
    try:
        mtime = os.path.getmtime(path)
        if force or HELP_PANEL_CACHE['mtime'] != mtime or HELP_PANEL_CACHE['data'] is None:
            with open(path, 'r', encoding='utf-8') as f:
                HELP_PANEL_CACHE['data'] = json.load(f)
            HELP_PANEL_CACHE['mtime'] = mtime
        return HELP_PANEL_CACHE['data'] or {}
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"help_panel_load_error {e}")
        return {}

def _help_panel_save(data: dict) -> bool:
    path = HELP_PANEL_CACHE['path']
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        HELP_PANEL_CACHE['data'] = data
        HELP_PANEL_CACHE['mtime'] = os.path.getmtime(path)
        return True
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"help_panel_save_error {e}")
        return False

@app.route('/api/help_panel_settings', methods=['GET'])
def api_help_panel_settings():
    _inc('requests_total')
    cfg = _help_panel_load()
    # Return minimal defaults if no config exists
    defaults = {
        'enabled': True,
        'label': 'R',
        'position': 'br',  # br=bottom-right, bl=bottom-left
        'read_default': 'Quick overview: This page helps you manage tenant documentation and records.',
        'instructions_default': 'Use the forms on this page to create or record documents. Save to your Vault.'
    }
    defaults.update(cfg or {})
    return jsonify(defaults)

@app.route('/admin/help_panel_save', methods=['POST'])
def admin_help_panel_save():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    try:
        enabled = request.form.get('enabled') in ('on','yes','true','1')
        label = (request.form.get('label') or 'R').strip()[:2] or 'R'
        position = (request.form.get('position') or 'br').strip()
        if position not in ('br','bl'):
            position = 'br'
        read_default = (request.form.get('read_default') or '').strip()
        instructions_default = (request.form.get('instructions_default') or '').strip()
        data = {
            'enabled': enabled,
            'label': label,
            'position': position,
            'read_default': read_default,
            'instructions_default': instructions_default
        }
        ok = _help_panel_save(data)
        if not ok:
            return "Failed to save settings", 500
        _event_log('help_panel_settings_saved', position=position, enabled=enabled)
        return redirect('/admin')
    except Exception as e:  # pragma: no cover
        _append_log(f"help_panel_save_exception {e}")
        return "Failed to save settings", 500

def _append_log(line: str):
    log_path_local = os.path.join("logs", "init.log")
    _rotate_if_needed(log_path_local)
    timestamp_local = _utc_now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path_local, "a", encoding="utf-8") as f:
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
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(payload) + "\n")
    except (OSError, json.JSONDecodeError) as e:
        _append_log(f"event_log_error {e}")

def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# -----------------------------
# Users registry for Document Vault
# -----------------------------
USERS_CACHE = {
    'path': os.path.join('security', 'users.json'),
    'mtime': None,
    'users': []  # list of { id, name, hash, enabled }
}

def _load_users(force: bool = False):
    path = USERS_CACHE['path']
    try:
        if not os.path.exists(path):
            if force:
                USERS_CACHE['users'] = []
            return
        mtime = os.path.getmtime(path)
        if force or USERS_CACHE['mtime'] != mtime:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            norm = []
            for u in data:
                if not u.get('enabled', True):
                    continue
                if 'hash' not in u or 'id' not in u:
                    continue
                norm.append({
                    'id': u.get('id'),
                    'name': u.get('name', u.get('id')),
                    'hash': u.get('hash'),
                    'enabled': True
                })
            USERS_CACHE['users'] = norm
            USERS_CACHE['mtime'] = mtime
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"users_load_error {e}")

def _write_users(users: list) -> None:
    path = USERS_CACHE['path']
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
        USERS_CACHE['mtime'] = os.path.getmtime(path)
        USERS_CACHE['users'] = [
            { 'id': u.get('id'), 'name': u.get('name', u.get('id')), 'hash': u.get('hash'), 'enabled': u.get('enabled', True) }
            for u in users if u.get('hash') and u.get('id') and u.get('enabled', True)
        ]
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"users_write_error {e}")

# -----------------------------
# Grants registry for read-only vault sharing
# -----------------------------
GRANTS_CACHE = {
    'path': os.path.join('security', 'grants.json'),
    'mtime': None,
    'grants': []  # list of { id, user_id, hash, enabled, scope, label, expires_ts }
}

def _load_grants(force: bool = False):
    path = GRANTS_CACHE['path']
    try:
        if not os.path.exists(path):
            if force:
                GRANTS_CACHE['grants'] = []
            return
        mtime = os.path.getmtime(path)
        if force or GRANTS_CACHE['mtime'] != mtime:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            norm = []
            now = int(time.time())
            for g in data:
                if not g.get('enabled', True):
                    continue
                if 'hash' not in g or 'user_id' not in g or 'id' not in g:
                    continue
                exp = g.get('expires_ts')
                if isinstance(exp, int) and exp > 0 and exp < now:
                    # Skip expired grants
                    continue
                norm.append({
                    'id': g.get('id'),
                    'user_id': g.get('user_id'),
                    'hash': g.get('hash'),
                    'scope': g.get('scope', 'vault_read'),
                    'label': g.get('label', ''),
                    'expires_ts': g.get('expires_ts', 0),
                    'enabled': True
                })
            GRANTS_CACHE['grants'] = norm
            GRANTS_CACHE['mtime'] = mtime
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"grants_load_error {e}")

def _write_grants(grants: list) -> None:
    path = GRANTS_CACHE['path']
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(grants, f, indent=2)
        GRANTS_CACHE['mtime'] = os.path.getmtime(path)
        # refresh cache
        _load_grants(force=True)
    except (OSError, json.JSONDecodeError) as e:  # pragma: no cover
        _append_log(f"grants_write_error {e}")

def _match_grant_token(grant_id: str, raw: Optional[str]):
    if not grant_id or not raw:
        return None
    _load_grants()
    h = _hash_token(raw)
    now = int(time.time())
    for g in GRANTS_CACHE['grants']:
        if g['id'] == grant_id and g['hash'] == h and (not g.get('expires_ts') or g['expires_ts'] > now):
            return g
    return None

def _match_user_token(raw: Optional[str]):
    if not raw:
        return None
    _load_users()
    h = _hash_token(raw)
    for u in USERS_CACHE['users']:
        if u['hash'] == h:
            return u
    return None

def _require_user_or_401():
    """Authenticate a regular user for the Document Vault.
    Accept token via query, header, or form. Returns user dict or (json,401).
    """
    supplied = request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')
    user = _match_user_token(supplied)
    if not user:
        _event_log('user_unauthorized', path=request.path, ip=request.remote_addr)
        return None
    return user

def _new_user_id() -> str:
    # Timestamp-based id to keep simple and unique enough for MVP
    return f"u{_utc_now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"

def _random_token_urlsafe(nbytes: int = 32) -> str:
    raw = os.urandom(nbytes)
    b64 = base64.urlsafe_b64encode(raw).decode('ascii').rstrip('=')
    return b64

def _random_digit_key(length: int = 24) -> str:
    # High-entropy digits-only key (length>=24 ~80 bits)
    return ''.join(secrets.choice('0123456789') for _ in range(max(1, length)))

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

# Optional HTTPS enforcement & HSTS
def _truthy(s: str) -> bool:
    return str(s).lower() in ("1", "true", "yes", "on")

# -----------------------------
# Public marketing/static pages
# -----------------------------
@app.route('/about', methods=['GET'])
def about_page():
    _inc('requests_total')
    return render_template('about.html')

@app.route('/features', methods=['GET'])
def features_page():
    _inc('requests_total')
    return render_template('features.html')

@app.route('/how_it_works', methods=['GET'])
def how_it_works_page():
    _inc('requests_total')
    return render_template('how_it_works.html')

@app.route('/faq', methods=['GET'])
def faq_page():
    _inc('requests_total')
    return render_template('faq.html')

@app.route('/get_started', methods=['GET'])
def get_started_page():
    _inc('requests_total')
    return render_template('get_started.html')

@app.route('/site_map', methods=['GET'])
def site_map_page():
    _inc('requests_total')
    return render_template('site_map.html')

FORCE_HTTPS = _truthy(os.environ.get('FORCE_HTTPS', '0'))
HSTS_MAX_AGE = int(os.environ.get('HSTS_MAX_AGE', '31536000'))  # 1 year
HSTS_PRELOAD = _truthy(os.environ.get('HSTS_PRELOAD', '0'))

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
    # HSTS only when secure or when forced (useful with local self-signed certs)
    try:
        is_secure = request.is_secure or request.headers.get('X-Forwarded-Proto', '').lower() == 'https'
    except Exception:
        is_secure = False
    if is_secure or FORCE_HTTPS:
        hsts_val = f"max-age={HSTS_MAX_AGE}; includeSubDomains"
        if HSTS_PRELOAD:
            hsts_val += "; preload"
        resp.headers.setdefault('Strict-Transport-Security', hsts_val)
    # Propagate request id
    rid = getattr(request, 'request_id', None)
    if rid:
        resp.headers.setdefault('X-Request-Id', rid)
    # Optional structured access log (enabled by ACCESS_LOG_JSON=1)
    if os.environ.get('ACCESS_LOG_JSON') == '1':
        try:
            started = getattr(request, '_start_time', None)
            dur_ms = None
            if started is not None:
                dur_ms = int((time.time() - started) * 1000)
            _event_log('access',
                       method=request.method,
                       path=request.full_path.rstrip('?'),
                       status=resp.status_code,
                       ip=request.remote_addr,
                       dur_ms=dur_ms,
                       request_id=rid)
        except Exception as e:  # pragma: no cover
            _append_log(f'access_log_error {e}')
    return resp

# -----------------------------
# Events & Logbook (per-user)
# -----------------------------

def _logbook_user_dir(user_id: str) -> str:
    base = os.path.join('uploads', 'logbook', user_id)
    os.makedirs(base, exist_ok=True)
    return base

def _logbook_path(user_id: str) -> str:
    return os.path.join(_logbook_user_dir(user_id), 'events.json')

def _logbook_load(user_id: str) -> list:
    path = _logbook_path(user_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):  # pragma: no cover
        return []

def _logbook_save(user_id: str, events: list):
    path = _logbook_path(user_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2)

def _parse_date_time(date_str: str | None, time_str: str | None):
    try:
        d = datetime.strptime((date_str or _utc_now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    except Exception:
        d = _utc_now().date()
    t = None
    if time_str:
        try:
            t = datetime.strptime(time_str, '%H:%M').time()
        except Exception:
            t = None
    return d, t

@app.route('/resources/logbook', methods=['GET'])
def logbook_view():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    events = _logbook_load(user['id'])
    # sort by date then time
    def _key(e):
        return (e.get('date',''), e.get('time',''))
    try:
        events.sort(key=_key)
    except (TypeError, AttributeError):
        pass
    csrf_token = _get_or_create_csrf_token()
    today = _utc_now().date().strftime('%Y-%m-%d')
    return render_template('logbook.html', events=events, csrf_token=csrf_token, user=user, today=today)

@app.route('/resources/logbook_add', methods=['POST'])
def logbook_add():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
    time_str = (request.form.get('time') or '').strip()
    title = (request.form.get('title') or '').strip() or 'Untitled'
    typ = (request.form.get('type') or 'meeting').strip()
    location = (request.form.get('location') or '').strip()
    people = (request.form.get('people') or '').strip()
    notes = (request.form.get('notes') or '').strip()
    # minimally validate date/time
    d, t = _parse_date_time(date, time_str)
    date = d.strftime('%Y-%m-%d')
    time_str = t.strftime('%H:%M') if t else ''
    events = _logbook_load(user['id'])
    ev = {
        'id': f"e{uuid.uuid4().hex[:10]}",
        'date': date,
        'time': time_str,
        'title': title,
        'type': typ,
        'location': location,
        'people': people,
        'notes': notes,
        'created_ts': _utc_now_iso(),
    }
    events.append(ev)
    try:
        events.sort(key=lambda e: (e.get('date',''), e.get('time','')))
    except Exception:
        pass
    _logbook_save(user['id'], events)
    _event_log('logbook_event_added', user_id=user['id'], date=date, time=time_str, type=typ)
    token = request.form.get('user_token') or ''
    return redirect(f"/resources/logbook?user_token={token}")

@app.route('/resources/logbook_edit', methods=['POST'])
def logbook_edit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    ev_id = (request.form.get('id') or '').strip()
    if not ev_id:
        return "Missing id", 400
    events = _logbook_load(user['id'])
    found = None
    for e in events:
        if e.get('id') == ev_id:
            found = e
            break
    if not found:
        return "Event not found", 404
    # Track changes
    before = found.copy()
    for field in ['date','time','title','type','location','people','notes']:
        if field in request.form:
            found[field] = (request.form.get(field) or '').strip()
    found['updated_ts'] = _utc_now_iso()
    # Save
    _logbook_save(user['id'], events)
    # Audit
    changes = {}
    for k in ['date','time','title','type','location','people','notes']:
        if before.get(k) != found.get(k):
            changes[k] = {'from': before.get(k), 'to': found.get(k)}
    _audit_log(user['id'], 'edit', 'logbook', ev_id, changes)
    token = request.form.get('user_token') or ''
    return redirect(f"/resources/logbook?user_token={token}")

@app.route('/resources/logbook.ics', methods=['GET'])
def logbook_ics():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    events = _logbook_load(user['id'])
    now = _utc_now()
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Semptify//Logbook//EN',
    ]
    for e in events:
        # build DTSTART; default to date only
        dtstart = e.get('date','').replace('-','')
        if e.get('time'):
            dtstart = f"{dtstart}T{e['time'].replace(':','')}00"
        uid = f"{e.get('id','evt')}-{user['id']}@semptify"
        summary = e.get('title','Event').replace('\n',' ').replace('\r',' ')
        description = e.get('notes','').replace('\n',' ').replace('\r',' ')
        location = e.get('location','').replace('\n',' ').replace('\r',' ')
        lines.extend([
            'BEGIN:VEVENT',
            f"UID:{uid}",
            f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{dtstart}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            'END:VEVENT',
        ])
    lines.append('END:VCALENDAR')
    ics = "\r\n".join(lines)
    from flask import Response
    resp = Response(ics, mimetype='text/calendar')
    resp.headers['Content-Disposition'] = 'attachment; filename="logbook.ics"'
    return resp

def _logbook_add_event(user_id: str, title: str, *, typ: str = 'other', date: str | None = None, time_str: str = '', location: str = '', people: str = '', notes: str = '') -> str:
    """Programmatically add a logbook event for a user and return event id."""
    events = _logbook_load(user_id)
    if not date:
        date = _utc_now().strftime('%Y-%m-%d')
    ev_id = f"e{uuid.uuid4().hex[:10]}"
    ev = {
        'id': ev_id,
        'date': date,
        'time': time_str,
        'title': title,
        'type': typ,
        'location': location,
        'people': people,
        'notes': notes,
        'created_ts': _utc_now_iso(),
        'auto_linked': True,
    }
    events.append(ev)
    try:
        events.sort(key=lambda e: (e.get('date',''), e.get('time','')))
    except Exception:
        pass
    _logbook_save(user_id, events)
    return ev_id

# -----------------------------
# Audit trail utilities (per-user JSONL)
# -----------------------------

def _audit_user_dir(user_id: str) -> str:
    base = os.path.join('uploads', 'audit', user_id)
    os.makedirs(base, exist_ok=True)
    return base

def _audit_path(user_id: str) -> str:
    return os.path.join(_audit_user_dir(user_id), 'audit.log')

def _audit_log(user_id: str, action: str, entity: str, entity_id: str, details: dict | None = None):
    try:
        rec = {
            'ts': _utc_now_iso(),
            'user_id': user_id,
            'action': action,
            'entity': entity,
            'entity_id': entity_id,
            'details': details or {},
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(request, 'request_id', None),
        }
        with open(_audit_path(user_id), 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:  # pragma: no cover
        _append_log(f"audit_log_error {e}")

# -----------------------------
# Contacts manager (per-user)
# -----------------------------

def _contacts_user_dir(user_id: str) -> str:
    base = os.path.join('uploads', 'contacts', user_id)
    os.makedirs(base, exist_ok=True)
    return base

def _contacts_path(user_id: str) -> str:
    return os.path.join(_contacts_user_dir(user_id), 'contacts.json')

def _contacts_load(user_id: str) -> list:
    p = _contacts_path(user_id)
    if not os.path.exists(p):
        return []
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:  # pragma: no cover
        return []

def _contacts_save(user_id: str, contacts: list):
    with open(_contacts_path(user_id), 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2)

@app.route('/resources/contacts', methods=['GET'])
def contacts_view():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    contacts = _contacts_load(user['id'])
    csrf_token = _get_or_create_csrf_token()
    return render_template('contacts.html', contacts=contacts, csrf_token=csrf_token, user=user)

@app.route('/resources/contacts_add', methods=['POST'])
def contacts_add():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    name = (request.form.get('name') or '').strip()
    if not name:
        return "Name is required", 400
    role = (request.form.get('role') or '').strip()
    org = (request.form.get('organization') or '').strip()
    phone = (request.form.get('phone') or '').strip()
    email = (request.form.get('email') or '').strip()
    address = (request.form.get('address') or '').strip()
    notes = (request.form.get('notes') or '').strip()
    contacts = _contacts_load(user['id'])
    cid = f"c{uuid.uuid4().hex[:10]}"
    contact = {
        'id': cid,
        'name': name,
        'role': role,
        'organization': org,
        'phone': phone,
        'email': email,
        'address': address,
        'notes': notes,
        'created_ts': _utc_now_iso(),
    }
    contacts.append(contact)
    # sort by name
    try:
        contacts.sort(key=lambda c: (c.get('name','').lower(), c.get('organization','').lower()))
    except Exception:
        pass
    _contacts_save(user['id'], contacts)
    _audit_log(user['id'], 'create', 'contact', cid, {'name': name})
    token = request.form.get('user_token') or ''
    return redirect(f"/resources/contacts?user_token={token}")

@app.route('/resources/contacts_edit', methods=['POST'])
def contacts_edit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    cid = (request.form.get('id') or '').strip()
    if not cid:
        return "Missing id", 400
    contacts = _contacts_load(user['id'])
    found = None
    for c in contacts:
        if c.get('id') == cid:
            found = c
            break
    if not found:
        return "Contact not found", 404
    before = found.copy()
    # Update fields
    for field in ['name','role','organization','phone','email','address','notes']:
        if field in request.form:
            found[field] = (request.form.get(field) or '').strip()
    found['updated_ts'] = _utc_now_iso()
    _contacts_save(user['id'], contacts)
    # Audit with changed fields
    changes = {}
    for k in ['name','role','organization','phone','email','address','notes']:
        if before.get(k) != found.get(k):
            changes[k] = {'from': before.get(k), 'to': found.get(k)}
    _audit_log(user['id'], 'edit', 'contact', cid, changes)
    token = request.form.get('user_token') or ''
    return redirect(f"/resources/contacts?user_token={token}")

@app.before_request
def _access_start():  # pragma: no cover (timing capture)
    # Store start timestamp for latency computation if access logging is enabled
    if os.environ.get('ACCESS_LOG_JSON') == '1':
        request._start_time = time.time()  # pylint: disable=protected-access
    # Generate a request id (idempotent if reverse proxy already set one via header)
    incoming = request.headers.get('X-Request-Id')
    request.request_id = incoming or uuid.uuid4().hex  # type: ignore[attr-defined]

@app.before_request
def _enforce_https_redirect():
    """If FORCE_HTTPS is enabled and request is not HTTPS, redirect to HTTPS.
    Honors X-Forwarded-Proto for reverse proxies. Health/metrics still redirect for consistency.
    """
    if not FORCE_HTTPS:
        return None
    # If behind a proxy sending X-Forwarded-Proto, respect it
    xf_proto = request.headers.get('X-Forwarded-Proto', '').lower()
    is_secure = request.is_secure or xf_proto == 'https'
    if is_secure:
        return None
    # If we cannot determine original scheme (missing X-Forwarded-Proto), avoid redirect loops
    if not xf_proto:
        return None
    # Only redirect if Host header exists and scheme is http
    host = request.host
    if not host:
        return None
    # Preserve full path and query string; swap scheme
    new_url = request.url.replace('http://', 'https://', 1)
    return redirect(new_url, code=301)

@app.route("/")
def index():
    # Use a Jinja2 template so UI can be extended without changing the route.
    message = "Welcome to Semptify — tools for renters to act confidently."
    _inc('requests_total')
    return render_template("index.html", message=message, folders=folders)

@app.route("/broker_trail", methods=["GET"])
def broker_trail():
    _inc('requests_total')
    return render_template("broker_trail.html")

@app.route("/owner_trail", methods=["GET"])
def owner_trail():
    _inc('requests_total')
    return render_template("owner_trail.html")

@app.route("/complaint_generator", methods=["GET"])
def complaint_generator():
    _inc('requests_total')
    return render_template("complaint_generator.html")

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
    snapshot, status_ok = _readiness_snapshot()
    return jsonify(snapshot), 200 if status_ok else 503

def _readiness_snapshot():
    """Return (snapshot_dict, healthy_bool)."""
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
    # Users file optional: do not fail readiness if missing, but record status
    users_ok = True
    try:
        _load_users(force=True)
    except Exception:
        users_ok = False
    status_ok = all(writable.values()) and tokens_ok
    snapshot = {
        'status': 'ready' if status_ok else 'degraded',
        'writable': writable,
        'tokens_load': tokens_ok,
        'users_load': users_ok,
        'time': _utc_now_iso()
    }
    return snapshot, status_ok

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

@app.route('/info')
def info():
    """Aggregated lightweight info: version + readiness + security mode."""
    _inc('requests_total')
    snapshot, _status = _readiness_snapshot()
    git_sha = os.environ.get("GIT_SHA", "unknown")
    build_time = os.environ.get("BUILD_TIME", "unknown")
    return jsonify({
        'app': 'SemptifyGUI',
        'git_sha': git_sha,
        'build_time': build_time,
        'security_mode': _current_security_mode(),
        'readiness': snapshot
    })


@app.context_processor
def inject_now():  # pragma: no cover (simple template helper)
    try:
        return {'now': str(_utc_now().year)}
    except Exception:
        return {'now': ''}

@app.route('/legal/terms')
def legal_terms():
    _inc('requests_total')
    return render_template('terms.html', updated=_utc_now().strftime('%Y-%m-%d'))

@app.route('/legal/privacy')
def legal_privacy():
    _inc('requests_total')
    return render_template('privacy.html', updated=_utc_now().strftime('%Y-%m-%d'))

@app.route('/legal/dmca')
def legal_dmca():
    _inc('requests_total')
    return render_template('dmca.html')


TOKENS_CACHE = { 'loaded_at': 0, 'tokens': [], 'path': os.path.join('security','admin_tokens.json'), 'mtime': None }

def _hash_token(raw: str) -> str:
    return 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest()

# Perform legacy token bootstrap only after required helpers are defined
_bootstrap_tokens_if_needed()

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
            data.append(entry)
            with open(log_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            _append_log(f'release_log_write_error {e}')
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


@app.route('/admin/run_tests', methods=['POST'])
def admin_run_tests():
    """Run pytest from the admin UI and show a brief summary. Secured by admin auth and CSRF in enforced mode.
    Limits runtime to prevent runaway executions in production.
    """
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    if not _require_admin_or_401():
        return _rate_or_unauth_response()
    _inc('admin_actions_total')
    try:
        # Run pytest quietly with max duration. Use a short timeout to avoid long runs on small dynos.
        # We prefer json summary if available; fall back to -q text.
        cmd = ['python', '-m', 'pytest', '-q']
        # Run within repo root; capture output
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, text=True)
        output = proc.stdout[-5000:]  # cap output to last 5k chars
        code = proc.returncode
        status = 'PASS' if code == 0 else 'FAIL'
        # Inline minimal HTML with pre block; avoid creating a new template for now
        html = (
            '<!doctype html><html><head><meta charset="utf-8"><title>Test Results</title>'
            '<link rel="stylesheet" href="/static/css/admin.css" />'
            '</head><body>'
            f'<h1>Test Results: {status}</h1>'
            '<p><a href="/admin">Back to Admin</a></p>'
            '<pre style="white-space:pre-wrap">' + (output.replace('<','&lt;').replace('>','&gt;')) + '</pre>'
            '</body></html>'
        )
        return html, 200 if code == 0 else 500
    except subprocess.TimeoutExpired:
        return ("<!doctype html><html><body><h1>Test Results: TIMEOUT</h1>"
                "<p>Tests exceeded the 180s limit. Try running locally or reduce scope.</p>"
                "<p><a href='/admin'>Back to Admin</a></p></body></html>", 500)
    except Exception as e:
        _append_log(f"admin_run_tests_error {e}")
        return ("<!doctype html><html><body><h1>Test Results: ERROR</h1>"
                f"<p>{str(e)}</p><p><a href='/admin'>Back to Admin</a></p></body></html>", 500)


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
# Resources: witness statements and filing packet checklist
# -----------------------------

@app.route('/resources')
def resources():
    _inc('requests_total')
    return render_template('resources.html')

# --- Placeholders for integrations still in progress ---
@app.route('/setup/ron')
def setup_ron():
    _inc('requests_total')
    tips = [
        'Set RON_PROVIDER=bluenotary and define a strong RON_WEBHOOK_SECRET in your environment.',
        'In the provider console, configure the webhook to https://<your-host>/webhooks/ron with the shared secret.',
        'Optional: Set BLUENOTARY_API_KEY when moving from mock to live; verify session creation and webhook HMAC if provided.']
    return render_template('setup_page.html', title='RON Provider Setup', banner='Remote Notarization requires a provider account and webhook configuration.', tips=tips)

@app.route('/setup/certified_mail')
def setup_certified_mail():
    _inc('requests_total')
    tips = [
        'Select a provider (e.g., Lob or Click2Mail) and create API credentials.',
        'Set provider env vars in Render and implement the submission call in a future update.',
        'Use the existing Certified Post form to track manual mailings until live integration.'
    ]
    return render_template('setup_page.html', title='Certified Mail Integration', banner='Automated mail is optional—manual tracking already works.', tips=tips)

@app.route('/setup/email')
def setup_email():
    _inc('requests_total')
    tips = [
        'Choose a transactional email provider (e.g., Postmark, SendGrid) and create an API key.',
        'Add env vars to Render: EMAIL_PROVIDER, EMAIL_API_KEY, and a verified sender domain.',
        'For now, Electronic Service is simulated and records certificates without sending.'
    ]
    return render_template('setup_page.html', title='Email Provider Setup', banner='Live email sending requires a provider; simulation remains available.', tips=tips)

@app.route('/resources/advocacy')
def resources_advocacy():
    _inc('requests_total')
    # Simple static list for now; can evolve to region-aware later
    orgs = [
        { 'name': 'Legal Aid (US directory)', 'url': 'https://www.lsc.gov/about-lsc/what-legal-aid/find-legal-aid', 'desc': 'Find a local legal aid provider by ZIP/State.' },
        { 'name': 'Housing Justice / Tenant Unions (local)', 'url': 'https://tenantresourcehub.org/', 'desc': 'Tenant support and local advocacy org discovery.' },
        { 'name': '211.org', 'url': 'https://www.211.org/', 'desc': 'Community services directory (housing, utilities, legal help).' },
        { 'name': 'National Low Income Housing Coalition', 'url': 'https://nlihc.org/', 'desc': 'Policy, research, and renter resources.' }
    ]
    learning = [
        { 'title': 'Documenting Housing Issues', 'desc': 'How to build a clean evidence trail (photos, dates, notices).'},
        { 'title': 'Understanding Notices & Timelines', 'desc': 'What common notices mean and typical response windows.'},
        { 'title': 'Preparing for Court', 'desc': 'Organizing documents, service proofs, and what to expect.'}
    ]
    return render_template('advocacy.html', orgs=orgs, learning=learning)

@app.route('/resources/roadmap')
def resources_roadmap():
    _inc('requests_total')
    items = [
        { 'title': 'Remote Online Notarization (live integration)', 'desc': 'Connect to BlueNotary for MN-compliant RON sessions with webhooks and audit trail storage.' },
        { 'title': 'Hybrid Mail (Certified/Registered)', 'desc': 'Automate certified mail via a provider (Lob/Click2Mail) and store tracking in certificates.' },
        { 'title': 'Court e-Filing Helpers', 'desc': 'State-specific e-filing checklists and document packaging.' },
        { 'title': 'Evidence OCR and Auto-Index', 'desc': 'Extract text and dates from uploads to improve search and timelines.' },
        { 'title': 'Share Scopes & Expirations', 'desc': 'Grant sharing that exposes only selected files/certificates with auto-expire.' }
    ]
    guidance = [
        'Use the Help panel (R) for quick page-specific tips and to jot Notes/To-Do.',
        'Leverage the Vault and Certificates export bundle to assemble records quickly.',
        'Advocacy & Learning has links for legal help and documentation best practices.'
    ]
    return render_template('roadmap.html', items=items, guidance=guidance)

@app.route('/resources/download/<name>.txt')
def resources_download(name: str):
    _inc('requests_total')
    # Whitelist known templates
    allowed = {
        'witness_statement': os.path.join(BASE_DIR, 'docs', 'templates', 'witness_statement_template.txt'),
        'filing_packet_checklist': os.path.join(BASE_DIR, 'docs', 'templates', 'filing_packet_checklist.txt'),
        'filing_packet_timeline': os.path.join(BASE_DIR, 'docs', 'templates', 'filing_packet_timeline.txt')
    }
    path = allowed.get(name)
    if not path or not os.path.exists(path):
        return "Not found", 404
    return send_file(path, as_attachment=True, download_name=f"{name}.txt")

# -----------------------------
# Fillable forms: Witness Statement and Filing Packet Builder
# -----------------------------

def _render_csrf():
    return _get_or_create_csrf_token()
@app.route('/register', methods=['GET'])
def register_page():
    _inc('requests_total')
    return render_template('register.html', csrf_token=_get_or_create_csrf_token())

@app.route('/register', methods=['POST'])
def register_submit():
    # Simple rate limit per IP
    rl_key = f"register:{request.remote_addr}"
    if not _rate_limit(rl_key):
        _inc('rate_limited_total')
        return jsonify({'error': 'rate_limited'}), RATE_LIMIT_STATUS, {'Retry-After': str(RATE_LIMIT_RETRY_AFTER)}
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    name = (request.form.get('name') or '').strip()
    _load_users()
    # Create user
    uid = _new_user_id()
    # Anonymous, digit-key accounts by default
    token = _random_digit_key(24)
    hashed = _hash_token(token)
    full = USERS_CACHE.get('users', [])
    # Store full list including disabled or others if file exists
    existing = []
    try:
        if os.path.exists(USERS_CACHE['path']):
            with open(USERS_CACHE['path'],'r', encoding='utf-8') as f:
                existing = json.load(f)
    except Exception:
        existing = []
    payload = { 'id': uid, 'hash': hashed, 'enabled': True }
    if name:
        payload['name'] = name
    existing.append(payload)
    _write_users(existing)
    _event_log('user_registered', user_id=uid, ip=request.remote_addr)
    # Show token once
    return render_template('register_success.html', user_id=uid, token=token)

# -----------------------------
# AI Copilot MVP
# -----------------------------

def _ai_provider() -> str:
    return (os.environ.get('AI_PROVIDER') or 'none').strip().lower()

def _copilot_call_openai(prompt: str) -> str:
    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL') or 'gpt-4o-mini'
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY not configured')
    url = os.environ.get('OPENAI_BASE_URL') or 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'You are Semptify Copilot, a helpful assistant for tenant-justice automation.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.2
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f'OpenAI error {r.status_code}: {r.text[:200]}')
    data = r.json()
    return data['choices'][0]['message']['content']

def _copilot_call_azure(prompt: str) -> str:
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
    api_version = os.environ.get('AZURE_OPENAI_API_VERSION') or '2024-02-15-preview'
    if not endpoint or not api_key or not deployment:
        raise RuntimeError('Azure OpenAI env not configured')
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    headers = {'api-key': api_key, 'Content-Type': 'application/json'}
    payload = {
        'messages': [
            {'role': 'system', 'content': 'You are Semptify Copilot, a helpful assistant for tenant-justice automation.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.2
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f'Azure OpenAI error {r.status_code}: {r.text[:200]}')
    data = r.json()
    return data['choices'][0]['message']['content']

def _copilot_call_ollama(prompt: str) -> str:
    host = os.environ.get('OLLAMA_HOST') or 'http://localhost:11434'
    model = os.environ.get('OLLAMA_MODEL') or 'llama3.1'
    url = f"{host.rstrip('/')}/api/generate"
    payload = {'model': model, 'prompt': prompt, 'stream': False, 'options': {'temperature': 0.2}}
    r = requests.post(url, json=payload, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f'Ollama error {r.status_code}: {r.text[:200]}')
    data = r.json()
    return data.get('response') or ''

def _copilot_generate(prompt: str) -> tuple[str, int]:
    provider = _ai_provider()
    if provider in ('', 'none'):
        return ('AI Copilot is not configured. Set AI_PROVIDER and provider-specific environment variables.', 501)
    try:
        if provider == 'openai':
            out = _copilot_call_openai(prompt)
        elif provider in ('azure', 'azure-openai'):
            out = _copilot_call_azure(prompt)
        elif provider == 'ollama':
            out = _copilot_call_ollama(prompt)
        else:
            return (f'Unknown AI_PROVIDER: {provider}', 400)
        return (out, 200)
    except Exception as e:
        _append_log(f"copilot_error {e}")
        return (f'Error from provider: {e}', 502)

@app.route('/copilot', methods=['GET'])
def copilot_page():
    _inc('requests_total')
    csrf = _render_csrf()
    provider = _ai_provider()
    return render_template('copilot.html', csrf_token=csrf, provider=provider)

@app.route('/api/copilot', methods=['POST'])
def copilot_api():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) or 'unknown'
    # Skip rate limiting during tests to avoid flakiness across test cases
    if not app.config.get('TESTING') and not _rate_limit(f"copilot:{ip}"):
        _inc('rate_limited_total')
        return jsonify({'error': 'rate_limited'}), RATE_LIMIT_STATUS, {'Retry-After': str(RATE_LIMIT_RETRY_AFTER)}
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    data = request.get_json(silent=True) or {}
    prompt = (data.get('prompt') or '').strip()
    citations = bool(data.get('citations'))
    if not prompt:
        return jsonify({'error': 'missing_prompt'}), 400

    # Check if this is an evidence-enhanced request
    location = (data.get('location') or '').strip()
    timestamp = (data.get('timestamp') or '').strip()
    form_type = (data.get('form_type') or '').strip()
    form_data = data.get('form_data', {})

    # Enhance prompt with evidence context if provided
    if location or timestamp or form_type:
        enhanced_prompt = _build_evidence_prompt(prompt, location, timestamp, form_type, form_data)
        _event_log('evidence_copilot_request', ip=ip, location=location[:50] if location else None, form_type=form_type)
    else:
        enhanced_prompt = prompt
    if citations:
        enhanced_prompt += "\n\nAlso include citations to relevant statutes, regulations, or trusted sources, with links when possible."

    text, code = _copilot_generate(enhanced_prompt)
    return jsonify({'provider': _ai_provider(), 'output': text}), code

# Compatibility alias for legacy tests that call /api/evidence-copilot
@app.route('/api/evidence-copilot', methods=['POST'])
def evidence_copilot_api():
    # Reuse the same logic as /api/copilot for rate limiting and CSRF
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) or 'unknown'
    # Skip rate limiting during tests to avoid flakiness across test cases
    if not app.config.get('TESTING') and not _rate_limit(f"copilot:{ip}"):
        _inc('rate_limited_total')
        return jsonify({'error': 'rate_limited'}), RATE_LIMIT_STATUS, {'Retry-After': str(RATE_LIMIT_RETRY_AFTER)}
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    data = request.get_json(silent=True) or {}
    prompt = (data.get('prompt') or '').strip()
    if not prompt:
        return jsonify({'error': 'missing_prompt'}), 400
    # Support the same evidence-enhanced parameters
    location = (data.get('location') or '').strip()
    timestamp = (data.get('timestamp') or '').strip()
    form_type = (data.get('form_type') or '').strip()
    form_data = data.get('form_data', {})
    if location or timestamp or form_type:
        enhanced_prompt = _build_evidence_prompt(prompt, location, timestamp, form_type, form_data)
        _event_log('evidence_copilot_request', ip=ip, location=location[:50] if location else None, form_type=form_type)
    else:
        enhanced_prompt = prompt
    text, code = _copilot_generate(enhanced_prompt)
    return jsonify({'provider': _ai_provider(), 'output': text}), code

def _build_evidence_prompt(base_prompt: str, location: str, timestamp: str, form_type: str, form_data: dict) -> str:
    """Build enhanced prompt with evidence collection context"""
    enhanced = "You are an AI assistant specializing in tenant rights and evidence collection. "

    if timestamp:
        enhanced += f"Current time: {timestamp}. "

    if location and location != 'Location unavailable':
        enhanced += f"User location: {location}. "

    if form_type and form_type != 'general_form':
        enhanced += f"User is working on: {form_type.replace('_', ' ')}. "

    if form_data and isinstance(form_data, dict) and form_data:
        # Add relevant form data context
        relevant_fields = []
        for key, value in form_data.items():
            if value and len(str(value).strip()) > 0 and key not in ['csrf_token', 'user_token']:
                relevant_fields.append(f"{key}: {str(value)[:100]}")
        if relevant_fields:
            enhanced += f"Form context: {'; '.join(relevant_fields[:3])}. "

    enhanced += "\n\nUser request: " + base_prompt
    enhanced += "\n\nPlease provide specific, actionable guidance for tenant rights documentation and evidence collection. Focus on:"
    enhanced += "\n1. What evidence to collect for this situation"
    enhanced += "\n2. Legal considerations and tenant rights"
    enhanced += "\n3. Best practices for documentation"
    enhanced += "\n4. Recommended next steps"

    return enhanced

@app.route('/resources/witness_statement', methods=['GET'])
def witness_form():
    _inc('requests_total')
    return render_template('witness_form.html', csrf_token=_render_csrf())

@app.route('/resources/witness_statement_preview', methods=['POST'])
def witness_preview():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    _inc('requests_total')
    data = {
        'full_name': (request.form.get('full_name') or '').strip(),
        'contact': (request.form.get('contact') or '').strip(),
        'statement': (request.form.get('statement') or '').strip(),
        'date': (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip(),
        'sig_name': (request.form.get('sig_name') or '').strip(),
        'sig_consented': 'yes' if (request.form.get('sig_consented') in ('on','yes','true','1')) else 'no'
    }
    user_token = request.form.get('user_token') or ''
    return render_template('witness_preview.html', data=data, user_token=user_token, csrf_token=_render_csrf())

@app.route('/resources/witness_statement_save', methods=['POST'])
def witness_save():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    # Compose text content
    full_name = (request.form.get('full_name') or '').strip()
    contact = (request.form.get('contact') or '').strip()
    statement = (request.form.get('statement') or '').strip()
    date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
    sig_name = (request.form.get('sig_name') or '').strip()
    sig_consented = request.form.get('sig_consented') in ('on','yes','true','1')
    if not sig_name or not sig_consented:
        return "Electronic signature consent and typed name are required to save", 400
    content = (
        "Witness Statement\n"
        "==================\n\n"
        f"Full name: {full_name}\n"
        f"Contact: {contact}\n\n"
        f"Statement (dated {date}):\n{statement}\n\n"
        "Unsworn Declaration (28 U.S.C. § 1746):\n"
        "I declare under penalty of perjury that the foregoing is true and correct.\n"
        f"Executed on {date}.\n\n"
        f"Signature (typed): {sig_name}\n"
        f"Printed Name: {full_name}\n"
    )
    # Save to user's vault
    ts = _utc_now().strftime('%Y%m%d_%H%M%S')
    filename = f"witness_{ts}.txt"
    dest = os.path.join(_vault_user_dir(user['id']), filename)
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        # Extract evidence collection data
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        location_accuracy = (request.form.get('location_accuracy') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()

        # Write certificate JSON with hash and context
        cert = {
            'type': 'witness_statement',
            'file': filename,
            'sha256': _sha256_hex(content),
            'user_id': user['id'],
            'executed_date': date,
            'sig_name': sig_name,
            'sig_consented': True,
            'ts': _utc_now_iso(),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(request, 'request_id', None),
            'evidence_collection': {
                'timestamp': evidence_timestamp or _utc_now_iso(),
                'location': evidence_location or 'Not provided',
                'location_accuracy': location_accuracy or 'Unknown',
                'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
                'has_location_data': bool(evidence_location),
                'collection_method': 'semptify_evidence_system'
            }
        }
        cert_path = os.path.join(_vault_user_dir(user['id']), f"witness_{ts}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, indent=2)
        _event_log('witness_saved', user_id=user['id'], filename=filename, size=os.path.getsize(dest), sha256=cert['sha256'])
    except Exception as e:  # pragma: no cover
        _append_log(f"witness_save_error {e}")
        return "Failed to save file", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

@app.route('/resources/filing_packet', methods=['GET'])
def packet_form():
    _inc('requests_total')
    return render_template('packet_form.html', csrf_token=_render_csrf())

@app.route('/resources/filing_packet_preview', methods=['POST'])
def packet_preview():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    _inc('requests_total')
    data = {
        'title': (request.form.get('title') or '').strip(),
        'summary': (request.form.get('summary') or '').strip(),
        'issues': (request.form.get('issues') or '').strip(),
        'parties': (request.form.get('parties') or '').strip(),
        'date': (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip(),
        'sig_name': (request.form.get('sig_name') or '').strip(),
        'sig_consented': 'yes' if (request.form.get('sig_consented') in ('on','yes','true','1')) else 'no'
    }
    user_token = request.form.get('user_token') or ''
    return render_template('packet_preview.html', data=data, user_token=user_token, csrf_token=_render_csrf())

@app.route('/resources/filing_packet_save', methods=['POST'])
def packet_save():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    title = (request.form.get('title') or '').strip()
    summary = (request.form.get('summary') or '').strip()
    issues = (request.form.get('issues') or '').strip()
    parties = (request.form.get('parties') or '').strip()
    date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
    sig_name = (request.form.get('sig_name') or '').strip()
    sig_consented = request.form.get('sig_consented') in ('on','yes','true','1')
    if not sig_name or not sig_consented:
        return "Electronic signature consent and typed name are required to save", 400
    content = (
        "Filing Packet Summary\n"
        "=====================\n\n"
        f"Title: {title}\n"
        f"Date: {date}\n"
        f"Parties: {parties}\n\n"
        "Summary:\n"
        f"{summary}\n\n"
        "Key Issues:\n"
        f"{issues}\n\n"
        "Checklist:\n"
        "- Cover Page\n- Summary Sheet\n- Evidence Index\n- Exhibits\n- Timeline\n- Witness Statements\n- Final Page (signature/date)\n\n"
        "Attestation:\n"
        "I declare under penalty of perjury that this summary accurately reflects the attached materials to the best of my knowledge.\n\n"
        f"Signature (typed): {sig_name}\n"
    )
    ts = _utc_now().strftime('%Y%m%d_%H%M%S')
    filename = f"packet_{ts}.txt"
    dest = os.path.join(_vault_user_dir(user['id']), filename)
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        # Extract evidence collection data
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        location_accuracy = (request.form.get('location_accuracy') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
        cert = {
            'type': 'filing_packet_summary',
            'file': filename,
            'sha256': _sha256_hex(content),
            'user_id': user['id'],
            'executed_date': date,
            'sig_name': sig_name,
            'sig_consented': True,
            'ts': _utc_now_iso(),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(request, 'request_id', None),
            'evidence_collection': {
                'timestamp': evidence_timestamp or _utc_now_iso(),
                'location': evidence_location or 'Not provided',
                'location_accuracy': location_accuracy or 'Unknown',
                'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
                'has_location_data': bool(evidence_location),
                'collection_method': 'semptify_evidence_system'
            }
        }
        cert_path = os.path.join(_vault_user_dir(user['id']), f"packet_{ts}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, indent=2)
        _event_log('packet_saved', user_id=user['id'], filename=filename, size=os.path.getsize(dest), sha256=cert['sha256'])
    except Exception as e:  # pragma: no cover
        _append_log(f"packet_save_error {e}")
        return "Failed to save file", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Service Animal (Reasonable Accommodation) Request Letter
# -----------------------------

@app.route('/resources/service_animal', methods=['GET'])
def sa_form():
    _inc('requests_total')
    return render_template('service_animal_form.html', csrf_token=_render_csrf())

@app.route('/resources/service_animal_preview', methods=['POST'])
def sa_preview():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    _inc('requests_total')
    data = {
        'tenant_name': (request.form.get('tenant_name') or '').strip(),
        'landlord_name': (request.form.get('landlord_name') or '').strip(),
        'property_address': (request.form.get('property_address') or '').strip(),
        'date': (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip(),
        'animal_description': (request.form.get('animal_description') or '').strip(),
        'need_summary': (request.form.get('need_summary') or '').strip(),
        'sig_name': (request.form.get('sig_name') or '').strip(),
        'sig_consented': 'yes' if (request.form.get('sig_consented') in ('on','yes','true','1')) else 'no'
    }
    user_token = request.form.get('user_token') or ''
    return render_template('service_animal_preview.html', data=data, user_token=user_token, csrf_token=_render_csrf())

@app.route('/resources/service_animal_save', methods=['POST'])
def sa_save():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    tenant_name = (request.form.get('tenant_name') or '').strip()
    landlord_name = (request.form.get('landlord_name') or '').strip()
    property_address = (request.form.get('property_address') or '').strip()
    date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
    animal_description = (request.form.get('animal_description') or '').strip()
    need_summary = (request.form.get('need_summary') or '').strip()
    sig_name = (request.form.get('sig_name') or '').strip()
    sig_consented = request.form.get('sig_consented') in ('on','yes','true','1')
    if not sig_name or not sig_consented:
        return "Electronic signature consent and typed name are required to save", 400
    content = (
        "Reasonable Accommodation Request (Service/Support Animal)\n"
        "=========================================================\n\n"
        f"Date: {date}\n"
        f"To: {landlord_name}\n"
        f"Property: {property_address}\n\n"
        f"I, {tenant_name}, request a reasonable accommodation to keep my service or support animal described as: {animal_description}.\n"
        f"This accommodation is necessary because: {need_summary}.\n\n"
        "This request is made pursuant to applicable fair housing laws.\n\n"
        "Attestation:\n"
        "I declare under penalty of perjury that the above is true and correct to the best of my knowledge.\n\n"
        f"Signature (typed): {sig_name}\n"
        f"Printed Name: {tenant_name}\n"
    )
    ts = _utc_now().strftime('%Y%m%d_%H%M%S')
    filename = f"service_animal_{ts}.txt"
    dest = os.path.join(_vault_user_dir(user['id']), filename)
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        # Extract evidence collection data
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        location_accuracy = (request.form.get('location_accuracy') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
        cert = {
            'type': 'service_animal_request',
            'file': filename,
            'sha256': _sha256_hex(content),
            'user_id': user['id'],
            'executed_date': date,
            'sig_name': sig_name,
            'sig_consented': True,
            'ts': _utc_now_iso(),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(request, 'request_id', None),
            'evidence_collection': {
                'timestamp': evidence_timestamp or _utc_now_iso(),
                'location': evidence_location or 'Not provided',
                'location_accuracy': location_accuracy or 'Unknown',
                'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
                'has_location_data': bool(evidence_location),
                'collection_method': 'semptify_evidence_system'
            }
        }
        cert_path = os.path.join(_vault_user_dir(user['id']), f"service_animal_{ts}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, indent=2)
        _event_log('service_animal_saved', user_id=user['id'], filename=filename, sha256=cert['sha256'])
    except Exception as e:  # pragma: no cover
        _append_log(f"sa_save_error {e}")
        return "Failed to save file", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Move-in / Move-out Checklist
# -----------------------------

@app.route('/resources/move_checklist', methods=['GET'])
def move_form():
    _inc('requests_total')
    return render_template('move_checklist_form.html', csrf_token=_render_csrf())

@app.route('/resources/move_checklist_preview', methods=['POST'])
def move_preview():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    _inc('requests_total')
    items = request.form.getlist('items')
    data = {
        'address': (request.form.get('address') or '').strip(),
        'date': (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip(),
        'notes': (request.form.get('notes') or '').strip(),
        'items': items,
        'sig_name': (request.form.get('sig_name') or '').strip(),
        'sig_consented': 'yes' if (request.form.get('sig_consented') in ('on','yes','true','1')) else 'no'
    }
    user_token = request.form.get('user_token') or ''
    return render_template('move_checklist_preview.html', data=data, user_token=user_token, csrf_token=_render_csrf())

@app.route('/resources/move_checklist_save', methods=['POST'])
def move_save():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    address = (request.form.get('address') or '').strip()
    date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
    notes = (request.form.get('notes') or '').strip()
    items = request.form.getlist('items')
    sig_name = (request.form.get('sig_name') or '').strip()
    sig_consented = request.form.get('sig_consented') in ('on','yes','true','1')
    if not sig_name or not sig_consented:
        return "Electronic signature consent and typed name are required to save", 400
    lines = [
        "Move-in/Move-out Checklist",
        "===========================",
        f"Address: {address}",
        f"Date: {date}",
        "",
        "Checked Items:"
    ] + [f"- {it}" for it in items] + [
        "",
        "Notes:",
        notes,
        "",
        "Attestation:",
        "I declare under penalty of perjury that this checklist accurately reflects the observed condition.",
        "",
        f"Signature (typed): {sig_name}"
    ]
    content = "\n".join(lines) + "\n"
    ts = _utc_now().strftime('%Y%m%d_%H%M%S')
    filename = f"move_checklist_{ts}.txt"
    dest = os.path.join(_vault_user_dir(user['id']), filename)
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        # Extract evidence collection data
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        location_accuracy = (request.form.get('location_accuracy') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
        cert = {
            'type': 'move_checklist',
            'file': filename,
            'sha256': _sha256_hex(content),
            'user_id': user['id'],
            'executed_date': date,
            'sig_name': sig_name,
            'sig_consented': True,
            'ts': _utc_now_iso(),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(request, 'request_id', None),
            'evidence_collection': {
                'timestamp': evidence_timestamp or _utc_now_iso(),
                'location': evidence_location or 'Not provided',
                'location_accuracy': location_accuracy or 'Unknown',
                'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
                'has_location_data': bool(evidence_location),
                'collection_method': 'semptify_evidence_system'
            }
        }
        cert_path = os.path.join(_vault_user_dir(user['id']), f"move_checklist_{ts}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, indent=2)
        _event_log('move_checklist_saved', user_id=user['id'], filename=filename, sha256=cert['sha256'])
    except Exception as e:  # pragma: no cover
        _append_log(f"move_save_error {e}")
        return "Failed to save file", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Rent Ledger (minimal)
# -----------------------------

def _ledger_user_dir(user_id: str) -> str:
    base = os.path.join('uploads', 'ledger', user_id)
    os.makedirs(base, exist_ok=True)
    return base

def _ledger_path(user_id: str) -> str:
    return os.path.join(_ledger_user_dir(user_id), 'ledger.json')

def _ledger_load(user_id: str) -> list:
    path = _ledger_path(user_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:  # pragma: no cover
        return []

def _ledger_save(user_id: str, entries: list):
    path = _ledger_path(user_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2)

@app.route('/resources/rent_ledger', methods=['GET'])
def ledger_view():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    entries = _ledger_load(user['id'])
    # calculate totals
    total_rent = sum(e.get('amount', 0) for e in entries if e.get('type') == 'rent')
    total_fees = sum(e.get('amount', 0) for e in entries if e.get('type') == 'fee')
    total_payments = sum(e.get('amount', 0) for e in entries if e.get('type') == 'payment')
    balance = (total_rent + total_fees) - total_payments
    csrf_token = _get_or_create_csrf_token()
    return render_template('ledger.html', entries=entries, total_rent=total_rent, total_fees=total_fees, total_payments=total_payments, balance=balance, csrf_token=csrf_token, user=user)

@app.route('/resources/rent_ledger_add', methods=['POST'])
def ledger_add():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    try:
        date = (request.form.get('date') or _utc_now().strftime('%Y-%m-%d')).strip()
        typ = (request.form.get('type') or 'rent').strip()
        amount = float(request.form.get('amount'))
        note = (request.form.get('note') or '').strip()
    except Exception:
        return "Invalid input", 400
    entries = _ledger_load(user['id'])
    entries.append({'date': date, 'type': typ, 'amount': amount, 'note': note})
    # sort by date then by type
    try:
        entries.sort(key=lambda e: (e.get('date',''), e.get('type','')))
    except Exception:
        pass
    _ledger_save(user['id'], entries)
    _event_log('ledger_entry_added', user_id=user['id'], date=date, type=typ, amount=amount)
    token = request.form.get('user_token') or ''
    return redirect(f"/resources/rent_ledger?user_token={token}")

# -----------------------------
# Document Vault (per-user storage)
# -----------------------------

def _vault_user_dir(user_id: str) -> str:
    base = os.path.join('uploads', 'vault', user_id)
    os.makedirs(base, exist_ok=True)
    return base

@app.route('/vault', methods=['GET'])
def vault_home():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    # List user's files
    user_dir = _vault_user_dir(user['id'])
    files = []
    try:
        for name in sorted(os.listdir(user_dir)):
            full = os.path.join(user_dir, name)
            if os.path.isfile(full):
                files.append({
                    'name': name,
                    'size': os.path.getsize(full)
                })
    except Exception as e:  # pragma: no cover
        _append_log(f"vault_list_error {e}")
    csrf_token = _get_or_create_csrf_token()
    # Load active grants for this user
    try:
        _load_grants()
        active_grants = [g for g in GRANTS_CACHE.get('grants', []) if g.get('user_id') == user['id']]
    except Exception:
        active_grants = []
    return render_template('vault.html', user=user, files=files, grants=active_grants, csrf_token=csrf_token)

@app.route('/vault/upload', methods=['POST'])
def vault_upload():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    f = request.files.get('file')
    if not f or f.filename is None or f.filename.strip() == '':
        return "No file provided", 400
    filename = secure_filename(f.filename)
    if not filename:
        return "Invalid filename", 400
    user_dir = _vault_user_dir(user['id'])
    dest = os.path.join(user_dir, filename)
    try:
        f.save(dest)
        _event_log('vault_upload', user_id=user['id'], filename=filename, size=os.path.getsize(dest))
    except Exception as e:  # pragma: no cover
        _append_log(f"vault_upload_error {e}")
        return "Failed to save file", 500
    return redirect(f"/vault?user_token=" + (request.form.get('user_token') or ''))

@app.route('/vault/download/<path:filename>', methods=['GET'])
def vault_download(filename):
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    safe = secure_filename(filename)
    if not safe or safe != filename:
        return "Invalid filename", 400
    path = os.path.join(_vault_user_dir(user['id']), safe)
    if not os.path.exists(path):
        return "Not found", 404
    return send_file(path, as_attachment=True)

@app.route('/vault/revoke_share', methods=['POST'])
def vault_revoke_share():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    grant_id = (request.form.get('grant_id') or '').strip()
    if not grant_id:
        return "Missing grant_id", 400
    # Read grants and disable the matching one owned by this user
    path = GRANTS_CACHE['path']
    try:
        data = []
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        updated = False
        for entry in data:
            if entry.get('id') == grant_id and entry.get('user_id') == user['id'] and entry.get('enabled', True):
                entry['enabled'] = False
                updated = True
                break
        if updated:
            _write_grants(data)
            _event_log('vault_share_revoked', user_id=user['id'], grant_id=grant_id)
    except Exception as e:  # pragma: no cover
        _append_log(f"vault_revoke_error {e}")
        return "Failed to revoke share", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

@app.route('/vault/create_share', methods=['POST'])
def vault_create_share():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    # inputs
    label = (request.form.get('label') or '').strip() or 'Trusted person'
    try:
        days = int(request.form.get('expires_days') or '30')
        days = max(1, min(days, 90))
    except Exception:
        days = 30
    scope = (request.form.get('scope') or 'vault_read').strip()
    # create grant
    grant_id = f"g{_utc_now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
    grant_token = _random_digit_key(16)
    hashed = _hash_token(grant_token)
    # load existing file to append
    existing = []
    try:
        if os.path.exists(GRANTS_CACHE['path']):
            with open(GRANTS_CACHE['path'], 'r', encoding='utf-8') as f:
                existing = json.load(f)
    except Exception:
        existing = []
    expires_ts = int(time.time()) + days * 86400
    payload = {
        'id': grant_id,
        'user_id': user['id'],
        'hash': hashed,
        'scope': scope,
        'label': label,
        'created_ts': _utc_now_iso(),
        'expires_ts': expires_ts,
        'enabled': True
    }
    existing.append(payload)
    _write_grants(existing)
    _event_log('vault_share_created', user_id=user['id'], grant_id=grant_id, scope=scope, expires_ts=expires_ts)
    # Render a one-time display with the share URL and token embedded
    share_path = f"/vault/share/{grant_id}?grant_token={grant_token}"
    return render_template('share_success.html', share_path=share_path, label=label, expires_days=days)

@app.route('/vault/share/<grant_id>', methods=['GET'])
def vault_share_view(grant_id):
    raw = request.args.get('grant_token') or request.headers.get('X-Grant-Token') or request.form.get('grant_token')
    grant = _match_grant_token(grant_id, raw)
    if not grant:
        return jsonify({'error': 'unauthorized'}), 401
    # List files for the owner of this grant
    user_dir = _vault_user_dir(grant['user_id'])
    files = []
    try:
        for name in sorted(os.listdir(user_dir)):
            full = os.path.join(user_dir, name)
            if os.path.isfile(full):
                files.append({'name': name, 'size': os.path.getsize(full)})
    except Exception as e:  # pragma: no cover
        _append_log(f"vault_share_list_error {e}")
    return render_template('vault_share.html', grant=grant, files=files)

@app.route('/vault/share/<grant_id>/download/<path:filename>', methods=['GET'])
def vault_share_download(grant_id, filename):
    raw = request.args.get('grant_token') or request.headers.get('X-Grant-Token') or request.form.get('grant_token')
    grant = _match_grant_token(grant_id, raw)
    if not grant:
        return jsonify({'error': 'unauthorized'}), 401
    safe = secure_filename(filename)
    if not safe or safe != filename:
        return "Invalid filename", 400
    path = os.path.join(_vault_user_dir(grant['user_id']), safe)
    if not os.path.exists(path):
        return "Not found", 404
    return send_file(path, as_attachment=True)

# -----------------------------
# Home Search (stubbed)
# -----------------------------
@app.route('/resources/home_search', methods=['GET'])
def home_search_form():
    _inc('requests_total')
    return render_template('home_search_form.html', csrf_token=_get_or_create_csrf_token())

@app.route('/resources/home_search', methods=['POST'])
def home_search_submit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    _inc('requests_total')
    city = (request.form.get('city') or '').strip()
    max_rent = (request.form.get('max_rent') or '').strip()
    beds = (request.form.get('beds') or '').strip()
    pets = (request.form.get('pets') or 'any').strip()
    # Stubbed results for now; integrate external API later via env config
    samples = [
        { 'title': 'Cozy 1BR near transit', 'city': city or 'Your area', 'rent': 1200, 'beds': 1, 'pets': 'cats' },
        { 'title': 'Spacious 2BR with parking', 'city': city or 'Your area', 'rent': 1800, 'beds': 2, 'pets': 'dogs' },
        { 'title': 'Studio, utilities included', 'city': city or 'Your area', 'rent': 950, 'beds': 0, 'pets': 'none' }
    ]
    # Simple client-side filtering
    try:
        if max_rent:
            mr = float(max_rent)
            samples = [s for s in samples if s['rent'] <= mr]
    except Exception:
        pass
    try:
        if beds:
            b = int(beds)
            samples = [s for s in samples if s['beds'] >= b]
    except Exception:
        pass
    if pets and pets.lower() in ('cats','dogs','none'):
        samples = [s for s in samples if s['pets'] == pets.lower()]
    return render_template('home_search_results.html', results=samples, city=city, max_rent=max_rent, beds=beds, pets=pets)

# -----------------------------
# Virtual Notary (evidence-of-existence; not a legal notarization)
# -----------------------------
@app.route('/notary', methods=['GET'])
def notary_home():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    files = []
    try:
        if os.path.isdir(user_dir):
            for name in sorted(os.listdir(user_dir)):
                fp = os.path.join(user_dir, name)
                if os.path.isfile(fp) and not name.lower().endswith('.json'):
                    files.append({'name': name, 'size': os.path.getsize(fp)})
    except Exception as e:  # pragma: no cover
        _append_log(f"notary_list_error {e}")
    return render_template('notary.html', user=user, files=files, csrf_token=_render_csrf())

@app.route('/notary/upload', methods=['POST'])
def notary_upload():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    f = request.files.get('file')
    if not f or f.filename == '':
        return "No file provided", 400
    safe = secure_filename(f.filename)
    user_dir = _vault_user_dir(user['id'])
    os.makedirs(user_dir, exist_ok=True)
    dest = os.path.join(user_dir, safe)
    try:
        f.save(dest)
        sha = _sha256_file(dest)
        ts = _utc_now_iso()
        cert = {
            'type': 'notary_attestation',
            'method': 'upload',
            'filename': safe,
            'user_id': user['id'],
            'ts': ts,
            'sha256': sha,
            'request_id': getattr(request, 'request_id', None),
            'disclaimer': 'This is a digital attestation of file existence and integrity. It is not a legal notarization.'
        }
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
        cert['evidence_collection'] = {
            'timestamp': evidence_timestamp or ts,
            'location': evidence_location or 'Not provided',
            'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
            'has_location_data': bool(evidence_location),
            'collection_method': 'semptify_notary'
        }
        cert_path = os.path.join(user_dir, f"notary_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('notary_upload_attested', user_id=user['id'], filename=safe, sha256=sha)
    except Exception as e:
        _append_log(f"notary_upload_error {e}")
        return "Failed to save notary attestation", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

@app.route('/notary/attest_existing', methods=['POST'])
def notary_attest_existing():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    safe = secure_filename((request.form.get('filename') or '').strip())
    if not safe:
        return "Filename required", 400
    user_dir = _vault_user_dir(user['id'])
    path = os.path.join(user_dir, safe)
    if not os.path.isfile(path):
        return "File not found", 404
    try:
        sha = _sha256_file(path)
        ts = _utc_now_iso()
        cert = {
            'type': 'notary_attestation',
            'method': 'existing',
            'filename': safe,
            'user_id': user['id'],
            'ts': ts,
            'sha256': sha,
            'request_id': getattr(request, 'request_id', None),
            'disclaimer': 'This is a digital attestation of file existence and integrity. It is not a legal notarization.'
        }
        evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
        evidence_location = (request.form.get('evidence_location') or '').strip()
        evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
        cert['evidence_collection'] = {
            'timestamp': evidence_timestamp or ts,
            'location': evidence_location or 'Not provided',
            'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
            'has_location_data': bool(evidence_location),
            'collection_method': 'semptify_notary'
        }
        cert_path = os.path.join(user_dir, f"notary_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('notary_existing_attested', user_id=user['id'], filename=safe, sha256=sha)
    except Exception as e:
        _append_log(f"notary_existing_error {e}")
        return "Failed to save notary attestation", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Certified Post / Electronic Service tracker
# -----------------------------
@app.route('/certified_post', methods=['GET'])
def certified_post_form():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    # list existing files to pick from
    user_dir = _vault_user_dir(user['id'])
    files = []
    try:
        if os.path.isdir(user_dir):
            for name in sorted(os.listdir(user_dir)):
                fp = os.path.join(user_dir, name)
                if os.path.isfile(fp) and not name.lower().endswith('.json'):
                    files.append({'name': name, 'size': os.path.getsize(fp)})
    except Exception as e:  # pragma: no cover
        _append_log(f"certpost_list_error {e}")
    return render_template('certified_post.html', user=user, files=files, csrf_token=_render_csrf())

@app.route('/certified_post', methods=['POST'])
def certified_post_submit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    service_type = (request.form.get('service_type') or '').strip()
    tracking_number = (request.form.get('tracking_number') or '').strip()
    destination = (request.form.get('destination') or '').strip()
    related_file = secure_filename((request.form.get('filename') or '').strip())
    if not service_type or not destination:
        return "Service type and destination are required", 400
    # Optional: attach a receipt image/pdf
    receipt = request.files.get('receipt_file')
    receipt_name = None
    user_dir = _vault_user_dir(user['id'])
    try:
        if receipt and receipt.filename:
            receipt_name = secure_filename(receipt.filename)
            if receipt_name:
                receipt_dest = os.path.join(user_dir, f"receipt_{int(time.time())}_{receipt_name}")
                receipt.save(receipt_dest)
    except Exception as e:
        _append_log(f"certpost_receipt_save_error {e}")
    # Compute sha256 for related file if provided
    file_sha = None
    if related_file:
        fpath = os.path.join(user_dir, related_file)
        if os.path.isfile(fpath):
            try:
                file_sha = _sha256_file(fpath)
            except Exception as e:
                _append_log(f"certpost_hash_error {e}")
    ts = _utc_now_iso()
    cert = {
        'type': 'certified_post',
        'user_id': user['id'],
        'ts': ts,
        'service_type': service_type,
        'destination': destination,
        'tracking_number': tracking_number or None,
        'related_file': related_file or None,
        'related_file_sha256': file_sha,
        'receipt_file': receipt_name,
        'request_id': getattr(request, 'request_id', None)
    }
    # Evidence context optional
    evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
    evidence_location = (request.form.get('evidence_location') or '').strip()
    evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
    cert['evidence_collection'] = {
        'timestamp': evidence_timestamp or ts,
        'location': evidence_location or 'Not provided',
        'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
        'has_location_data': bool(evidence_location),
        'collection_method': 'semptify_certified_post'
    }
    try:
        cert_path = os.path.join(user_dir, f"certpost_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('certified_post_created', user_id=user['id'], service_type=service_type, tracking_number=tracking_number)
        # Auto-link a logbook event
        title = f"Sent via {service_type.replace('_',' ').title()}"
        notes = f"Destination: {destination}. Tracking: {tracking_number or 'n/a'}. Related: {related_file or 'n/a'}."
        _logbook_save(user['id'], _logbook_load(user['id']))  # ensure dir exists
        _logbook_add_event(user['id'], title, typ='communication' if service_type=='electronic' else 'deadline', notes=notes)
    except Exception as e:
        _append_log(f"certpost_write_error {e}")
        return "Failed to save certified post record", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Court Clerk filing tracker
# -----------------------------
@app.route('/court_clerk', methods=['GET'])
def court_clerk_form():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    files = []
    try:
        if os.path.isdir(user_dir):
            for name in sorted(os.listdir(user_dir)):
                fp = os.path.join(user_dir, name)
                if os.path.isfile(fp) and not name.lower().endswith('.json'):
                    files.append({'name': name, 'size': os.path.getsize(fp)})
    except Exception as e:  # pragma: no cover
        _append_log(f"courtclerk_list_error {e}")
    return render_template('court_clerk.html', user=user, files=files, csrf_token=_render_csrf())

@app.route('/court_clerk', methods=['POST'])
def court_clerk_submit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    court_name = (request.form.get('court_name') or '').strip()
    case_number = (request.form.get('case_number') or '').strip()
    filing_type = (request.form.get('filing_type') or '').strip()
    submission_method = (request.form.get('submission_method') or '').strip()
    status = (request.form.get('status') or 'submitted').strip()
    related_file = secure_filename((request.form.get('filename') or '').strip())
    if not court_name or not related_file:
        return "Court name and related file are required", 400
    user_dir = _vault_user_dir(user['id'])
    fpath = os.path.join(user_dir, related_file)
    if not os.path.isfile(fpath):
        return "Related file not found", 404
    # Optional: clerk stamp/receipt upload
    stamp = request.files.get('stamp_file')
    stamp_name = None
    try:
        if stamp and stamp.filename:
            stamp_name = secure_filename(stamp.filename)
            if stamp_name:
                stamp_dest = os.path.join(user_dir, f"clerkstamp_{int(time.time())}_{stamp_name}")
                stamp.save(stamp_dest)
    except Exception as e:
        _append_log(f"courtclerk_stamp_save_error {e}")
    file_sha = None
    try:
        file_sha = _sha256_file(fpath)
    except Exception as e:
        _append_log(f"courtclerk_hash_error {e}")
    ts = _utc_now_iso()
    cert = {
        'type': 'court_clerk_filing',
        'user_id': user['id'],
        'ts': ts,
        'court_name': court_name,
        'case_number': case_number or None,
        'filing_type': filing_type or None,
        'submission_method': submission_method or None,
        'status': status,
        'related_file': related_file,
        'related_file_sha256': file_sha,
        'stamp_file': stamp_name,
        'request_id': getattr(request, 'request_id', None)
    }
    evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
    evidence_location = (request.form.get('evidence_location') or '').strip()
    evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
    cert['evidence_collection'] = {
        'timestamp': evidence_timestamp or ts,
        'location': evidence_location or 'Not provided',
        'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
        'has_location_data': bool(evidence_location),
        'collection_method': 'semptify_court_clerk'
    }
    try:
        cert_path = os.path.join(user_dir, f"courtclerk_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('court_clerk_filing_recorded', user_id=user['id'], court=court_name, case=case_number)
        # Auto-link a logbook event
        title = f"Court filing: {filing_type or 'Document'} at {court_name}"
        notes = f"Case: {case_number or 'n/a'}. Status: {status}. Related: {related_file}. Method: {submission_method or 'n/a'}."
        _logbook_save(user['id'], _logbook_load(user['id']))
        _logbook_add_event(user['id'], title, typ='deadline', notes=notes)
    except Exception as e:
        _append_log(f"courtclerk_write_error {e}")
        return "Failed to save court clerk record", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Certificates: list, view, and export bundle
# -----------------------------
@app.route('/vault/certificates', methods=['GET'])
def vault_certificates_list():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    certs = []
    try:
        for name in sorted(os.listdir(user_dir)):
            if name.lower().endswith('.json') and (name.startswith('notary_') or name.startswith('certpost_') or name.startswith('courtclerk_') or name.startswith('electronic_service_') or name.startswith('legalnotary_') or name.startswith('ron_')):
                full = os.path.join(user_dir, name)
                certs.append({'name': name, 'size': os.path.getsize(full)})
    except Exception as e:  # pragma: no cover
        _append_log(f"cert_list_error {e}")
    return render_template('certificates.html', user=user, certs=certs, csrf_token=_render_csrf())

@app.route('/vault/certificates/<path:filename>', methods=['GET'])
def vault_certificate_view(filename):
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    safe = secure_filename(filename)
    if not safe or safe != filename or not safe.lower().endswith('.json'):
        return "Invalid filename", 400
    path = os.path.join(_vault_user_dir(user['id']), safe)
    if not os.path.isfile(path):
        return "Not found", 404
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = None
    return render_template('certificate_view.html', filename=safe, data=data)

@app.route('/vault/export_bundle', methods=['POST'])
def vault_export_bundle():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    # Build a zip in-memory containing all certificates and referenced files where present
    import io, zipfile
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        # Add certificates
        refs = []
        for name in sorted(os.listdir(user_dir)):
            if name.lower().endswith('.json') and (name.startswith('notary_') or name.startswith('certpost_') or name.startswith('courtclerk_') or name.startswith('electronic_service_') or name.startswith('legalnotary_') or name.startswith('ron_')):
                full = os.path.join(user_dir, name)
                try:
                    zf.write(full, arcname=f"certificates/{name}")
                    # collect referenced files
                    with open(full, 'r', encoding='utf-8') as cf:
                        c = json.load(cf)
                        # common keys that may reference filenames
                        for key in ('filename','related_file','receipt_file','stamp_file','attachments'):
                            v = c.get(key)
                            if isinstance(v, str) and v:
                                refs.append(v)
                            elif isinstance(v, list):
                                for item in v:
                                    if isinstance(item, str):
                                        refs.append(item)
                except Exception as e:  # pragma: no cover
                    _append_log(f"export_zip_add_cert_error {e}")
        # Deduplicate and add referenced files
        for rf in sorted(set(filter(None, refs))):
            safe = secure_filename(rf)
            fpath = os.path.join(user_dir, safe)
            if os.path.isfile(fpath):
                try:
                    zf.write(fpath, arcname=f"files/{safe}")
                except Exception as e:  # pragma: no cover
                    _append_log(f"export_zip_add_file_error {e}")
    mem.seek(0)
    fname = f"semptify_export_{user['id']}_{int(time.time())}.zip"
    return send_file(mem, as_attachment=True, download_name=fname, mimetype='application/zip')

# -----------------------------
# Electronic Service (email) - simulate send and record certificate
# -----------------------------
@app.route('/electronic_service', methods=['GET'])
def electronic_service_form():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    files = []
    try:
        if os.path.isdir(user_dir):
            for name in sorted(os.listdir(user_dir)):
                fp = os.path.join(user_dir, name)
                if os.path.isfile(fp) and not name.lower().endswith('.json'):
                    files.append({'name': name, 'size': os.path.getsize(fp)})
    except Exception as e:  # pragma: no cover
        _append_log(f"esvc_list_error {e}")
    return render_template('electronic_service.html', user=user, files=files, csrf_token=_render_csrf())

@app.route('/electronic_service', methods=['POST'])
def electronic_service_submit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    to_addr = (request.form.get('to') or '').strip()
    subject = (request.form.get('subject') or '').strip()
    body = (request.form.get('body') or '').strip()
    related_file = secure_filename((request.form.get('filename') or '').strip())
    if not to_addr:
        return "Recipient is required", 400
    user_dir = _vault_user_dir(user['id'])
    file_sha = None
    if related_file:
        fpath = os.path.join(user_dir, related_file)
        if os.path.isfile(fpath):
            try:
                file_sha = _sha256_file(fpath)
            except Exception as e:
                _append_log(f"esvc_hash_error {e}")
    ts = _utc_now_iso()
    # Simulate sending; in future integrate email provider
    cert = {
        'type': 'electronic_service',
        'user_id': user['id'],
        'ts': ts,
        'to': to_addr,
        'subject': subject or None,
        'body': body or None,
        'related_file': related_file or None,
        'related_file_sha256': file_sha,
        'outcome': 'simulated_sent',
        'request_id': getattr(request, 'request_id', None)
    }
    evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
    evidence_location = (request.form.get('evidence_location') or '').strip()
    evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
    cert['evidence_collection'] = {
        'timestamp': evidence_timestamp or ts,
        'location': evidence_location or 'Not provided',
        'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
        'has_location_data': bool(evidence_location),
        'collection_method': 'semptify_electronic_service'
    }
    try:
        cert_path = os.path.join(user_dir, f"electronic_service_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('electronic_service_recorded', user_id=user['id'], to=to_addr)
    except Exception as e:
        _append_log(f"esvc_write_error {e}")
        return "Failed to save electronic service record", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# Legal Notary: guidance + record of completed notarization (user-provided scan)
# -----------------------------
@app.route('/legal_notary', methods=['GET'])
def legal_notary_form():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    # List existing files so user can indicate which document was notarized
    files = []
    try:
        if os.path.isdir(user_dir):
            for name in sorted(os.listdir(user_dir)):
                fp = os.path.join(user_dir, name)
                if os.path.isfile(fp) and not name.lower().endswith('.json'):
                    files.append({'name': name, 'size': os.path.getsize(fp)})
    except Exception as e:  # pragma: no cover
        _append_log(f"legalnotary_list_error {e}")
    # Provider from env
    ron_provider = (os.environ.get('RON_PROVIDER') or '').strip().lower()
    return render_template('legal_notary.html', user=user, files=files, csrf_token=_render_csrf(), ron_provider=ron_provider)

@app.route('/legal_notary', methods=['POST'])
def legal_notary_submit():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_dir = _vault_user_dir(user['id'])
    # Metadata about the notarial act
    notary_name = (request.form.get('notary_name') or '').strip()
    commission_number = (request.form.get('commission_number') or '').strip()
    state = (request.form.get('state') or '').strip()
    notarization_date = (request.form.get('notarization_date') or '').strip() or _utc_now().strftime('%Y-%m-%d')
    method = (request.form.get('method') or '').strip()  # in_person | ron | enotarization
    provider = (request.form.get('provider') or '').strip()
    jurisdiction = (request.form.get('jurisdiction') or '').strip()
    source_file = secure_filename((request.form.get('source_file') or '').strip())
    notes = (request.form.get('notes') or '').strip()
    if not notary_name or not state:
        return "Notary name and state are required", 400
    # Upload scanned notarized document (optional but recommended)
    up = request.files.get('notarized_file')
    attach_name = None
    try:
        if up and up.filename:
            base = secure_filename(up.filename)
            if base:
                attach_name = f"notarized_{int(time.time())}_{base}"
                up.save(os.path.join(user_dir, attach_name))
    except Exception as e:
        _append_log(f"legalnotary_upload_error {e}")
    # Compute sha for source/attachment if present
    source_sha = None
    if source_file:
        spath = os.path.join(user_dir, source_file)
        if os.path.isfile(spath):
            try:
                source_sha = _sha256_file(spath)
            except Exception as e:
                _append_log(f"legalnotary_source_hash_error {e}")
    attach_sha = None
    if attach_name:
        apath = os.path.join(user_dir, attach_name)
        if os.path.isfile(apath):
            try:
                attach_sha = _sha256_file(apath)
            except Exception as e:
                _append_log(f"legalnotary_attach_hash_error {e}")
    # Certificate JSON (record of notarization)
    ts = _utc_now_iso()
    cert = {
        'type': 'legal_notary_record',
        'user_id': user['id'],
        'ts': ts,
        'notary_name': notary_name,
        'commission_number': commission_number or None,
        'state': state,
        'jurisdiction': jurisdiction or None,
        'method': method or None,
        'provider': provider or None,
        'notarization_date': notarization_date,
        'source_file': source_file or None,
        'source_file_sha256': source_sha,
        'attachments': [attach_name] if attach_name else [],
        'attachments_sha256': [attach_sha] if attach_sha else [],
        'notes': notes or None,
        'request_id': getattr(request, 'request_id', None),
        'disclaimer': 'This records a legal notarization performed outside Semptify. It does not perform or replace a notarization.'
    }
    # Evidence collection context (optional)
    evidence_timestamp = (request.form.get('evidence_timestamp') or '').strip()
    evidence_location = (request.form.get('evidence_location') or '').strip()
    evidence_user_agent = (request.form.get('evidence_user_agent') or '').strip()
    cert['evidence_collection'] = {
        'timestamp': evidence_timestamp or ts,
        'location': evidence_location or 'Not provided',
        'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
        'has_location_data': bool(evidence_location),
        'collection_method': 'semptify_legal_notary_record'
    }
    try:
        cert_path = os.path.join(user_dir, f"legalnotary_{int(time.time())}_{uuid.uuid4().hex[:8]}.json")
        with open(cert_path, 'w', encoding='utf-8') as cf:
            json.dump(cert, cf, ensure_ascii=False, indent=2)
        _event_log('legal_notary_recorded', user_id=user['id'], state=state, method=method)
    except Exception as e:
        _append_log(f"legalnotary_write_error {e}")
        return "Failed to save legal notary record", 500
    token = request.form.get('user_token') or ''
    return redirect(f"/vault?user_token={token}")

# -----------------------------
# RON adapter (BlueNotary-ready) minimal flow: start, return, webhook
# -----------------------------
def _ron_provider() -> str:
    return (os.environ.get('RON_PROVIDER') or '').strip().lower()

@app.route('/legal_notary/start', methods=['POST'])
def legal_notary_start():
    if not _validate_csrf(request):
        return "CSRF validation failed", 400
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    provider_name = _ron_provider()
    if provider_name not in ('bluenotary', 'onenotary', 'notarize', 'docusign', ''):
        return "RON provider not configured", 400
    # Minimal: collect metadata and simulate creation. Real impl would call provider API.
    source_file = secure_filename((request.form.get('source_file') or '').strip())
    user_dir = _vault_user_dir(user['id'])
    file_sha = None
    if source_file:
        spath = os.path.join(user_dir, source_file)
        if os.path.isfile(spath):
            try:
                file_sha = _sha256_file(spath)
            except Exception:
                pass
    # Create provider session (mocked in tests/no API key)
    ret_url = f"/legal_notary/return?user_token={request.form.get('user_token','')}"
    prov = get_provider(provider_name or 'bluenotary')
    created = prov.create_session(user['id'], source_file or None, ret_url)
    session_id = created.get('session_id') or f"sim-{uuid.uuid4().hex[:12]}"
    redirect_url = created.get('redirect_url') or f"/legal_notary/return?session_id={session_id}&user_token={request.form.get('user_token','')}"
    # Pre-write a pending certificate stub so webhook/return can update
    ts = _utc_now_iso()
    stub = {
        'type': 'ron_session',
        'status': 'started',
        'provider': (provider_name or 'bluenotary'),
        'user_id': user['id'],
        'ts': ts,
        'session_id': session_id,
        'source_file': source_file or None,
        'source_file_sha256': file_sha,
        'request_id': getattr(request, 'request_id', None)
    }
    try:
        with open(os.path.join(user_dir, f"ron_{session_id}.json"), 'w', encoding='utf-8') as cf:
            json.dump(stub, cf, indent=2)
    except Exception:
        pass
    return redirect(redirect_url)

@app.route('/legal_notary/return', methods=['GET'])
def legal_notary_return():
    user = _require_user_or_401()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    session_id = (request.args.get('session_id') or '').strip()
    if not session_id:
        return "Missing session_id", 400
    user_dir = _vault_user_dir(user['id'])
    path = os.path.join(user_dir, f"ron_{session_id}.json")
    # Simulate provider success and finalize certificate
    data = {
        'type': 'ron_session',
        'status': 'completed',
        'provider': _ron_provider(),
        'user_id': user['id'],
        'session_id': session_id,
        'completed_ts': _utc_now_iso(),
        'evidence_links': []
    }
    try:
        # Merge with existing
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                prev = json.load(f)
            prev.update(data)
            data = prev
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        _event_log('ron_completed', user_id=user['id'], session_id=session_id)
    except Exception:
        return "Failed to finalize RON record", 500
    return redirect(f"/vault?user_token={request.args.get('user_token','')}")

@app.route('/webhooks/ron', methods=['POST'])
def ron_webhook():
    # No CSRF; provider verification
    prov = get_provider(_ron_provider())
    if not prov.verify_webhook(request):
        return "unauthorized", 401
    payload = request.get_json(silent=True) or {}
    user_id = (payload.get('user_id') or '').strip()
    session_id = (payload.get('session_id') or '').strip()
    status = (payload.get('status') or 'completed').strip()
    evidence_links = payload.get('evidence_links') or []
    if not user_id or not session_id:
        return "bad payload", 400
    user_dir = _vault_user_dir(user_id)
    path = os.path.join(user_dir, f"ron_{session_id}.json")
    try:
        base = {}
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                base = json.load(f)
        base.update({
            'status': status,
            'provider': _ron_provider() or base.get('provider'),
            'updated_ts': _utc_now_iso(),
            'evidence_links': evidence_links
        })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(base, f, indent=2)
        _event_log('ron_webhook', user_id=user_id, session_id=session_id, status=status)
    except Exception:
        return "fail", 500
    return "ok", 200

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
