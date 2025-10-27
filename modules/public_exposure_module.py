from flask import Blueprint, jsonify

public_exposure_bp = Blueprint('public_exposure', __name__)

@public_exposure_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Public Exposure Module"})