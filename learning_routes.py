"""
Flask Blueprint: Learning Engine API
Provides endpoints for self-learning capabilities.
"""

from flask import Blueprint, request, jsonify
from engines.learning_engine import get_learning
from security import
from curiosity_hooks import on_learning_module_completed validate_user_token, validate_admin_token

learning_bp = Blueprint("learning", __name__, url_prefix="/api/learning")


@learning_bp.route("/observe", methods=["POST"])
def observe_action():
    """
    Record a user action for learning.

    Body:
    {
        "user_token": "...",
        "action": "upload_lease",
        "context": {"success": true, "time_taken": 5.2}
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    action = data.get("action")
    context = data.get("context", {})

    if not action:
        return jsonify({"error": "action required"}), 400

    learning = get_learning()
    learning.observe_action(user_id, action, context)

    # Trigger curiosity: What did user learn?
    try:
        question = on_learning_module_completed(user_id, action, context)
        if question:
            print(f'[CURIOSITY] {question}')
    except Exception as e:
        print(f'[WARN] Curiosity hook failed: {e}')

    return jsonify({"status": "recorded", "action": action})


@learning_bp.route("/observe/sequence", methods=["POST"])
def observe_sequence():
    """
    Record an action sequence for learning.

    Body:
    {
        "user_token": "...",
        "action1": "upload_lease",
        "action2": "file_complaint"
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    action1 = data.get("action1")
    action2 = data.get("action2")

    if not action1 or not action2:
        return jsonify({"error": "action1 and action2 required"}), 400

    learning = get_learning()
    learning.observe_sequence(user_id, action1, action2)

    return jsonify({"status": "recorded", "sequence": f"{action1}->{action2}"})


@learning_bp.route("/suggest", methods=["GET"])
def get_suggestion():
    """
    Get personalized suggestions for user.

    Query params:
    - user_token: User's token
    - last_action: (optional) Last action performed
    """
    user_token = request.args.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    learning = get_learning()
    last_action = request.args.get("last_action")

    suggestions = {
        "personalized": learning.get_personalized_suggestions(user_id),
        "time_based": learning.get_time_based_suggestion()
    }

    if last_action:
        suggestions["next_action"] = learning.suggest_next_action(user_id, last_action)

    return jsonify(suggestions)


@learning_bp.route("/feedback", methods=["POST"])
def record_feedback():
    """
    Record user feedback on suggestions.

    Body:
    {
        "user_token": "...",
        "suggestion": "file_complaint",
        "helpful": true
    }
    """
    data = request.get_json() or {}

    user_token = data.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)

    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    suggestion = data.get("suggestion")
    helpful = data.get("helpful", False)

    if not suggestion:
        return jsonify({"error": "suggestion required"}), 400

    learning = get_learning()
    learning.record_feedback(suggestion, helpful)

    return jsonify({"status": "recorded", "thanks": "feedback recorded"})


@learning_bp.route("/insights", methods=["GET"])
def get_insights():
    """
    Get learning insights (requires user or admin token).

    Query params:
    - user_token: User's token (shows personalized insights)
    - admin_token: Admin token (shows global insights)
    """
    user_token = request.args.get("user_token") or request.headers.get("X-User-Token")
    admin_token = request.args.get("admin_token") or request.headers.get("X-Admin-Token")

    user_id = validate_user_token(user_token) if user_token else None
    admin_id = validate_admin_token(admin_token) if admin_token else None

    if not user_id and not admin_id:
        return jsonify({"error": "unauthorized"}), 401

    learning = get_learning()

    # Admin sees global insights, user sees personalized
    insights = learning.get_insights(user_id=user_id if not admin_id else None)

    return jsonify(insights)


@learning_bp.route("/admin/reset", methods=["POST"])
def reset_learning():
    """
    Reset learning patterns (admin only).

    Body:
    {
        "admin_token": "...",
        "confirm": "RESET"
    }
    """
    data = request.get_json() or {}

    admin_token = data.get("admin_token") or request.headers.get("X-Admin-Token")
    admin_id = validate_admin_token(admin_token)

    if not admin_id:
        return jsonify({"error": "unauthorized"}), 401

    if data.get("confirm") != "RESET":
        return jsonify({"error": "confirmation required"}), 400

    learning = get_learning()

    # Reset patterns
    learning.patterns = {
        "user_habits": {},
        "sequences": {},
        "time_patterns": {},
        "success_rates": {},
        "suggestions": {}
    }
    learning._save_patterns()

    return jsonify({"status": "reset", "message": "All learning patterns cleared"})


@learning_bp.route("/stats", methods=["GET"])
def get_stats():
    """
    Get learning statistics (public endpoint).

    Returns:
    - Total actions tracked
    - Most common patterns
    - Success rates
    """
    learning = get_learning()

    stats = {
        "total_users": len(learning.patterns["user_habits"]),
        "total_sequences": len(learning.patterns["sequences"]),
        "peak_hours": learning._get_peak_hours(),
        "common_actions": sorted(
            learning.patterns["sequences"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
    }

    return jsonify(stats)


@learning_bp.route("/suggestions/<doc_id>", methods=["GET"])
def get_document_learning_suggestions(doc_id):
    """
    Get learning suggestions for a specific uploaded document
    
    GET /api/learning/suggestions/<doc_id>?user_token=...
    
    Returns: {
        "modules": ["eviction_defenses", ...],
        "resources": ["Legal aid contacts", ...],
        "next_steps": ["Review your eviction notice", ...]
    }
    """
    user_token = request.args.get("user_token") or request.headers.get("X-User-Token")
    user_id = validate_user_token(user_token)
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    # Read certificate file to get learning suggestions
    import os
    import json
    
    cert_path = os.path.join("uploads", "vault", doc_id, f"{doc_id}.cert.json")
    
    if not os.path.exists(cert_path):
        return jsonify({"error": "document not found"}), 404
    
    try:
        with open(cert_path, 'r') as f:
            cert = json.load(f)
        
        # Verify user owns this document
        if cert.get("user_id") != user_id:
            return jsonify({"error": "unauthorized"}), 403
        
        suggestions = cert.get("learning_suggestions", {
            "modules": [],
            "resources": [],
            "next_steps": []
        })
        
        return jsonify(suggestions)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500