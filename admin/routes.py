# filepath: d:\Semptify\Semptify\admin\routes.py
from flask import Blueprint, render_template, request, jsonify
import json, time, uuid, os
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
    with open("logs/release-log.json","a",encoding="utf-8") as f: f.write(json.dumps(ev)+"\n")
    return jsonify(result="release triggered", request_id=ev["id"])

