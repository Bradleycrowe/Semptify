# filepath: d:\Semptify\Semptify\admin\routes.py
from flask import Blueprint, render_template, request, jsonify, Response
import json
import time
import uuid
import os
from security import _require_admin_or_401, _get_or_create_csrf_token, incr_metric

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates/admin", static_folder="../static/admin")

@admin_bp.route("/")
def dashboard():
    _require_admin_or_401()
    csrf = _get_or_create_csrf_token()
    return render_template("admin/dashboard.html", csrf_token=csrf)

@admin_bp.route("/release_now", methods=["POST"])
def release_now():
    _require_admin_or_401()
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
    if not _require_admin_or_401():
        return Response("Unauthorized", status=401)
    csrf_token = _get_or_create_csrf_token()
    return render_template('admin.html', csrf_token=csrf_token)

@admin_bp.route('/admin/logs', methods=['GET'])
def view_logs():
    """Fetch and return application logs."""
    if not _require_admin_or_401():
        return Response("Unauthorized", status=401)
    with open('logs/init.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()
    return jsonify({"logs": logs})

@admin_bp.route('/admin/metrics', methods=['GET'])
def view_metrics():
    """Fetch and return system metrics."""
    if not _require_admin_or_401():
        return Response("Unauthorized", status=401)
    metrics = {
        "uptime": "24 hours",
        "requests_total": 1024,
        "errors_total": 12
    }
    return jsonify(metrics)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    """Manage users (view, add, remove)."""
    if not _require_admin_or_401():
        return Response("Unauthorized", status=401)
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

