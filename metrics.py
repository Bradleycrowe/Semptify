from flask import Blueprint, jsonify
from security import get_metrics
metrics_bp = Blueprint("metrics", __name__)
@metrics_bp.route("/metrics")
def metrics():
    return jsonify(get_metrics())
