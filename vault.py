# filepath: d:\Semptify\Semptify\vault.py
import os, time, json, hashlib
from flask import Blueprint, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
vault_bp = Blueprint("vault_blueprint", __name__)

@vault_bp.route("/vault", methods=["GET","POST"])
def vault():
    if request.method == "GET":
        return "Vault - POST a file with form field file and user_token param"
    t = request.args.get("user_token") or request.headers.get("X-User-Token") or request.form.get("user_token")
    if not t:
        abort(401)
    f = request.files.get("file")
    if not f or not f.filename:
        return "no file", 400
    userdir = os.path.join("uploads","vault", t)
    os.makedirs(userdir, exist_ok=True)
    name = secure_filename(f.filename)
    path = os.path.join(userdir, name)
    f.save(path)
    sha = hashlib.sha256(open(path,"rb").read()).hexdigest()
    cert = {"sha256":sha, "ts":int(time.time()), "request_id": request.headers.get("X-Request-Id"), "evidence":{"user":t}}
    open(path + ".json","w",encoding="utf-8").write(json.dumps(cert))
    return jsonify(saved=name, cert=cert)

