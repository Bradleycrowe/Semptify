# filepath: d:\Semptify\Semptify\admin\routes.py
from flask import Blueprint, render_template, request, jsonify, Response, send_file, redirect, url_for
import json
import time
import uuid
import os
from security import _require_admin_or_401, _get_or_create_csrf_token, incr_metric, validate_admin_token, check_rate_limit, is_breakglass_active, consume_breakglass, log_event
import sqlite3
from typing import Any, Dict

# Optional human perspective formatter
try:
    from human_perspective import humanize_object
except Exception:
    def humanize_object(obj: Any, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"title": "Humanized View", "summary": str(obj)}

try:
    from r2_database_adapter import sync_database_to_r2, get_r2_adapter
except Exception:
    def sync_database_to_r2():
        pass
    def get_r2_adapter():
        class _Dummy:
            enabled = False
            bucket = None
        return _Dummy()

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates/admin", static_folder="../static/admin")

def _admin_check():
    """Extract token from request and validate admin access."""
    token = request.args.get('token') or request.args.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(token):
        return None, ("unauthorized", 401), None

    # Check rate limit AFTER auth
    ip = request.remote_addr or 'unknown'
    rate_key = f"admin:{ip}:{request.path}"
    if not check_rate_limit(rate_key):
        log_event("admin_rate_limited", {"path": request.path, "ip": ip})
        incr_metric("rate_limited_total")
        return None, (jsonify({'error': 'rate_limited'}), int(os.environ.get('ADMIN_RATE_STATUS', '429'))), None

    # Handle breakglass token (one-shot use)
    if token and is_breakglass_active(token):
        consume_breakglass(token)
        log_event("breakglass_used", {"ip": ip})

    incr_metric("admin_requests_total")
    log_event("admin_access", {"path": request.path, "ip": ip})
    return token, None, None

@admin_bp.route("/")
def dashboard():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    panels = [
        {"name": "Storage / DB", "path": "/admin/storage-db", "desc": "SQLite + R2 status & tools"},
        {"name": "Users", "path": "/admin/users-panel", "desc": "Browse and export users"},
        {"name": "Email", "path": "/admin/email", "desc": "Delivery provider & test"},
        {"name": "Security", "path": "/admin/security", "desc": "Mode, tokens, breakglass"},
        {"name": "Human Perspective", "path": "/admin/human", "desc": "Explain, simplify, and format for people"},
    ]
    return render_template("admin/dashboard.html", csrf_token=csrf, panels=panels)

@admin_bp.route("/release_now", methods=["POST"])
def release_now():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    if request.form.get("csrf_token") != csrf or request.form.get("confirm_release") != "yes":
        return "CSRF or confirmation failed", 403
    incr_metric("releases_total")
    ev = {"event":"release_triggered","ts":int(time.time()),"id":str(uuid.uuid4())}
    os.makedirs("logs", exist_ok=True)
    with open("logs/release-log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")
    return jsonify(result="release triggered", request_id=ev["id"])

@admin_bp.route('/admin', methods=['GET'])
def admin_dashboard():
    """Render the admin dashboard."""
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf_token = _get_or_create_csrf_token()
    return render_template('admin.html', csrf_token=csrf_token)

@admin_bp.route('/admin/logs', methods=['GET'])
def view_logs():
    """Fetch and return application logs."""
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    with open('logs/init.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()
    return jsonify({"logs": logs})

@admin_bp.route('/admin/metrics', methods=['GET'])
def view_metrics():
    """Fetch and return system metrics."""
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    metrics = {
        "uptime": "24 hours",
        "requests_total": 1024,
        "errors_total": 12
    }
    return jsonify(metrics)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    """Manage users (view, add, remove)."""
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    if request.method == 'GET':
        # Example user data
        users = [
            {"id": 1, "name": "Admin", "role": "admin"},
            {"id": 2, "name": "User1", "role": "user"}
        ]
        return jsonify(users)
    elif request.method == 'POST':
        # Add a new user (example logic)
        new_user = request.json
        return jsonify({"message": "User added", "user": new_user})
    return Response("Invalid method", status=405)

# =============================
# STORAGE / DATABASE PANEL
# =============================
@admin_bp.route('/storage-db')
def storage_db_panel():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    db_path = 'security/users.db'
    size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    r2 = get_r2_adapter()
    r2_enabled = getattr(r2, 'enabled', False)
    bucket = getattr(r2, 'bucket', None)
    return render_template('admin/storage_db.html', csrf_token=csrf, db_size=size, r2_enabled=r2_enabled, r2_bucket=bucket)

@admin_bp.route('/storage-db/sync', methods=['POST'])
def storage_db_sync():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    if request.form.get('csrf_token') != csrf:
        return "CSRF failed", 403
    sync_database_to_r2()
    return redirect(url_for('admin.storage_db_panel'))

@admin_bp.route('/storage-db/download')
def storage_db_download():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    path = 'security/users.db'
    if not os.path.exists(path):
        return "DB not found", 404
    return send_file(path, as_attachment=True, download_name='users.db')

# =============================
# USERS PANEL
# =============================
@admin_bp.route('/users-panel')
def users_panel():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    users = []
    try:
        conn = sqlite3.connect('security/users.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT user_id, email, first_name, last_name, verified_at, login_count FROM users ORDER BY verified_at DESC LIMIT 25')
        users = [dict(r) for r in cur.fetchall()]
        cur.execute('SELECT COUNT(*) FROM users')
        total = cur.fetchone()[0]
        conn.close()
    except Exception:
        total = 0
    return render_template('admin/users_panel.html', csrf_token=csrf, users=users, total=total)

@admin_bp.route('/users-panel/export')
def users_panel_export():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    try:
        conn = sqlite3.connect('security/users.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        all_rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify({"users": all_rows, "count": len(all_rows)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================
# EMAIL PANEL
# =============================
@admin_bp.route('/email', methods=['GET', 'POST'])
def email_panel():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    resend = os.environ.get('RESEND_API_KEY')
    gmail = os.environ.get('GMAIL_ADDRESS') and os.environ.get('GMAIL_APP_PASSWORD')
    if resend:
        provider = 'Resend'
    elif gmail:
        provider = 'Gmail SMTP'
    else:
        provider = 'Dev Mode (console only)'
    sent = None
    if request.method == 'POST':
        if request.form.get('csrf_token') != csrf:
            return "CSRF failed", 403
        test_email = request.form.get('email')
        if test_email:
            from email_service import send_verification_email
            ok = send_verification_email(test_email, '123456', 'Test')
            sent = ok
    return render_template('admin/email_panel.html', csrf_token=csrf, provider=provider, sent=sent)

# =============================
# SECURITY PANEL
# =============================
@admin_bp.route('/security')
def security_panel():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()
    mode = os.environ.get('SECURITY_MODE', 'open')
    breakglass_flag = os.path.exists('security/breakglass.flag')
    return render_template('admin/security_panel.html', csrf_token=csrf, mode=mode, breakglass=breakglass_flag)


# =============================
# HUMAN PERSPECTIVE PANEL
# =============================
@admin_bp.route('/human', methods=['GET', 'POST'])
def human_perspective_panel():
    token, error_resp, error_code = _admin_check()
    if error_resp:
        return error_resp, error_code
    csrf = _get_or_create_csrf_token()

    result = None
    input_text = ''
    format_pref = 'concise'
    if request.method == 'POST':
        if request.form.get('csrf_token') != csrf:
            return "CSRF failed", 403
        input_text = request.form.get('input_text', '')
        format_pref = request.form.get('format_pref', 'concise')
        context = {
            'format_pref': format_pref,
            'audience': request.form.get('audience', 'tenant'),
            'reading_level': request.form.get('reading_level', 'plain'),
        }
        try:
            import json as _json
            obj = _json.loads(input_text)
        except Exception:
            obj = input_text
        result = humanize_object(obj, context)

    return render_template('admin/human_perspective.html', csrf_token=csrf, result=result, input_text=input_text, format_pref=format_pref)

