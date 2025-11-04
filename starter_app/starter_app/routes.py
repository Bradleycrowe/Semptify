from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return jsonify({"status": "ok", "message": "Hello from starter_app"})
