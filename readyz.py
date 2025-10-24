from flask import Blueprint, jsonify
import os
readyz_bp = Blueprint("readyz", __name__)
@readyz_bp.route("/readyz")
def readyz():
    details = {}
    status = "ready"
    for d in ["uploads","logs","copilot_sync","final_notices","security"]:
        ok = os.access(d, os.W_OK)
        details[d] = "ok" if ok else "not writable"
        if not ok: status = "degraded"
    return jsonify(status=status, details=details)
