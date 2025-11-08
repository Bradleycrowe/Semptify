"""
Flask Routes: Tenant Journey Integration
Exposes journey tracking and intelligent guidance to users.
"""

from flask import Blueprint, request, jsonify
from tenant_journey import get_tenant_journey
from security import validate_user_token

journey_bp = Blueprint("journey", __name__, url_prefix="/api/journey")


@journey_bp.route("/start", methods=["POST"])
def start_journey():
    """
    Start tracking tenant's journey.

    Body:
    {
        "user_token": "...",
        "location": {
            "city": "sacramento_city",
            "county": "sacramento_county",
            "state": "california",
            "zip": "95814"
        },
        "context": {
            "looking_for": "1br apartment",
            "budget": 1500
        }
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    location = data.get("location", {})
    context = data.get("context", {})

    journey_tracker = get_tenant_journey()
    result = journey_tracker.start_journey(user_id, location, context)

    return jsonify(result)


@journey_bp.route("/<journey_id>/advance", methods=["POST"])
def advance_stage(journey_id):
    """
    Move to next stage in journey.

    Body:
    {
        "user_token": "...",
        "new_stage": "applying",
        "data": {
            "agency": "ABC Property Management",
            "address": "123 Main St",
            "application_fee": 75
        }
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    new_stage = data.get("new_stage")
    stage_data = data.get("data", {})

    if not new_stage:
        return jsonify({"error": "new_stage required"}), 400

    journey_tracker = get_tenant_journey()
    result = journey_tracker.advance_stage(journey_id, new_stage, stage_data)

    return jsonify(result)


@journey_bp.route("/<journey_id>/guidance", methods=["GET"])
def get_guidance(journey_id):
    """
    Get intelligent guidance for current stage.
    Uses all learning systems to provide smart advice.

    Query params:
    - user_token: Authentication
    - stage: (optional) Get guidance for specific stage
    """
    user_token = request.args.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    stage = request.args.get("stage")

    journey_tracker = get_tenant_journey()
    journey = journey_tracker.journeys.get(journey_id)

    if not journey:
        return jsonify({"error": "journey not found"}), 404

    if journey["user_id"] != user_id:
        return jsonify({"error": "unauthorized"}), 403

    current_stage = stage or journey["stage"]
    guidance = journey_tracker.get_stage_guidance(journey_id, current_stage)

    return jsonify({
        "journey_id": journey_id,
        "stage": current_stage,
        "guidance": guidance
    })


@journey_bp.route("/<journey_id>/outcome", methods=["POST"])
def record_outcome(journey_id):
    """
    Record journey outcome - triggers learning.

    Body:
    {
        "user_token": "...",
        "outcome_type": "resolved" | "dispute" | "moved_out" | "lost_case" | "won_case",
        "outcome_data": {
            "resolution": "Repair completed",
            "time_taken_days": 45,
            "cost": 1800,
            "satisfaction": "high"
        }
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    outcome_type = data.get("outcome_type")
    outcome_data = data.get("outcome_data", {})

    if not outcome_type:
        return jsonify({"error": "outcome_type required"}), 400

    journey_tracker = get_tenant_journey()
    journey_tracker.record_outcome(journey_id, outcome_type, outcome_data)

    return jsonify({
        "status": "recorded",
        "message": "Thank you! Your outcome helps other tenants."
    })


@journey_bp.route("/<journey_id>", methods=["GET"])
def get_journey(journey_id):
    """Get full journey details."""
    user_token = request.args.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    journey_tracker = get_tenant_journey()
    journey = journey_tracker.journeys.get(journey_id)

    if not journey:
        return jsonify({"error": "journey not found"}), 404

    if journey["user_id"] != user_id:
        return jsonify({"error": "unauthorized"}), 403

    return jsonify(journey)
