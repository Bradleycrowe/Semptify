from flask import Blueprint, jsonify

enforcement_bp = Blueprint('enforcement', __name__)

@enforcement_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Enforcement Module"})