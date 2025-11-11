"""
Flask Routes for Preliminary Learning Module
Provides API endpoints for accessing procedures, forms, timelines, and fact-checking.
"""

from flask import Blueprint, jsonify, request, session, abort
from preliminary_learning import get_preliminary_learning_module

# Import from the top-level security module if it exists, otherwise provide decorator
try:
    from security import _require_user_or_401, incr_metric
except ImportError:
    # Fallback: use security package
    from security import incr_metric
    # Simple fallback decorator
    def _require_user_or_401():
        def decorator(f):
            def wrapper(*args, **kwargs):
                if not session.get('user_id'):
                    return jsonify({"error": "Not authenticated"}), 401
                return f(*args, **kwargs)
            wrapper.__name__ = f.__name__
            return wrapper
        return decorator

# Create blueprint
learning_module_bp = Blueprint('learning_module', __name__, url_prefix='/api/learning')

# Initialize module
module = get_preliminary_learning_module()


# ============================================================================
# INFORMATION ACQUISITION ENDPOINTS
# ============================================================================

@learning_module_bp.route('/procedures', methods=['GET'])
def get_procedures():
    """
    Get procedures by category.

    Query params:
        - category: 'rental_procedures', 'legal_procedures', 'court_procedures',
                   'complaint_filing', 'funding_sources', 'governing_agencies'
        - subcategory: Optional specific procedure (e.g., 'lease_signing')

    Returns:
        JSON of procedures with steps, forms, timelines
    """
    if not _require_user_or_401():
        abort(401)
        abort(401)

    incr_metric("learning_requests_total")

    category = request.args.get('category')
    subcategory = request.args.get('subcategory')

    if not category:
        return jsonify({
            "error": "Missing 'category' parameter",
            "valid_categories": [
                "rental_procedures",
                "legal_procedures",
                "court_procedures",
                "complaint_filing",
                "funding_sources",
                "governing_agencies"
            ]
        }), 400

    procedures = module.get_procedures(category, subcategory)

    return jsonify({
        "success": True,
        "category": category,
        "subcategory": subcategory,
        "data": procedures
    }), 200


@learning_module_bp.route('/forms', methods=['GET'])
def get_forms():
    """
    Get required forms for a procedure.

    Query params:
        - category: Procedure category
        - subcategory: Specific procedure

    Returns:
        JSON list of required forms
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    category = request.args.get('category')
    subcategory = request.args.get('subcategory')

    if not category:
        return jsonify({"error": "Missing 'category' parameter"}), 400

    forms = module.get_forms(category, subcategory)

    return jsonify({
        "success": True,
        "category": category,
        "subcategory": subcategory,
        "forms": forms,
        "count": len(forms)
    }), 200


@learning_module_bp.route('/timeline', methods=['GET'])
def get_timeline():
    """
    Get timeline for a procedure.

    Query params:
        - category: Procedure category
        - subcategory: Specific procedure

    Returns:
        JSON with timeline in days and description
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    category = request.args.get('category')
    subcategory = request.args.get('subcategory')

    if not category:
        return jsonify({"error": "Missing 'category' parameter"}), 400

    days, unit = module.get_timeline(category, subcategory)

    return jsonify({
        "success": True,
        "category": category,
        "subcategory": subcategory,
        "timeline_days": days,
        "unit": unit
    }), 200


@learning_module_bp.route('/jurisdiction-info', methods=['GET'])
def get_jurisdiction_info():
    """
    Check if procedure varies by jurisdiction.

    Query params:
        - category: Procedure category
        - subcategory: Specific procedure

    Returns:
        JSON with jurisdiction specificity flag
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    category = request.args.get('category')
    subcategory = request.args.get('subcategory')

    if not category or not subcategory:
        return jsonify({"error": "Missing 'category' or 'subcategory' parameter"}), 400

    is_jurisdiction_specific = module.get_jurisdiction_info(category, subcategory)

    return jsonify({
        "success": True,
        "category": category,
        "subcategory": subcategory,
        "jurisdiction_specific": is_jurisdiction_specific,
        "note": "Check local regulations for specific requirements"
    }), 200


@learning_module_bp.route('/agencies', methods=['GET'])
def get_agencies_for_issue():
    """
    Get relevant agencies for an issue type.

    Query params:
        - issue_type: 'maintenance', 'eviction', 'discrimination', 'fraud', etc.

    Returns:
        JSON list of relevant agencies with contact info
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    issue_type = request.args.get('issue_type')

    if not issue_type:
        return jsonify({"error": "Missing 'issue_type' parameter"}), 400

    agencies = module.get_agencies_for_issue(issue_type)

    return jsonify({
        "success": True,
        "issue_type": issue_type,
        "agencies": agencies,
        "count": len(agencies)
    }), 200


@learning_module_bp.route('/quick-reference', methods=['GET'])
def get_quick_reference():
    """
    Get quick reference card for a topic.

    Query params:
        - topic: Topic to get reference for (e.g., 'lease', 'repair', 'eviction')

    Returns:
        JSON quick reference with key points, timeline, forms, next steps
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    topic = request.args.get('topic')

    if not topic:
        return jsonify({"error": "Missing 'topic' parameter"}), 400

    reference = module.get_quick_reference(topic)

    return jsonify({
        "success": True,
        "topic": topic,
        "reference": reference
    }), 200


@learning_module_bp.route('/resources', methods=['GET'])
def get_all_resources():
    """
    Get list of all available learning resources.

    Returns:
        JSON with available categories and total topics
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    resources = module.get_all_resources()

    return jsonify({
        "success": True,
        "resources": resources
    }), 200


# ============================================================================
# FACT-CHECKING ENDPOINTS
# ============================================================================

@learning_module_bp.route('/fact-check', methods=['POST'])
def fact_check_claim():
    """
    Fact-check a claim against the knowledge base.

    POST body:
        {
            "claim": "Claim to verify",
            "category": "Category to check against",
            "subcategory": "Optional specific subcategory"
        }

    Returns:
        JSON with fact-check result: status, details, sources
    """
    if not _require_user_or_401():
        abort(401)
    incr_metric("learning_requests_total")

    data = request.get_json() or {}

    claim = data.get('claim')
    category = data.get('category')
    subcategory = data.get('subcategory')

    if not claim or not category:
        return jsonify({
            "error": "Missing 'claim' or 'category' parameter"
        }), 400

    result = module.fact_check(claim, category, subcategory)

    return jsonify({
        "success": True,
        "result": result
    }), 200


@learning_module_bp.route('/fact-check-batch', methods=['POST'])
def fact_check_batch():
    """
    Fact-check multiple claims at once.

    POST body:
        {
            "claims": [
                {"claim": "...", "category": "...", "subcategory": "..."},
                ...
            ]
        }

    Returns:
        JSON with array of fact-check results
    """
    if not _require_user_or_401():
        abort(401)

    incr_metric("learning_requests_total")

    data = request.get_json() or {}
    claims = data.get('claims', [])

    if not claims:
        return jsonify({"error": "Missing 'claims' parameter"}), 400

    results = []
    for claim_data in claims:
        result = module.fact_check(
            claim_data.get('claim'),
            claim_data.get('category'),
            claim_data.get('subcategory')
        )
        results.append(result)

    return jsonify({
        "success": True,
        "results": results,
        "count": len(results)
    }), 200


# ============================================================================
# KNOWLEDGE UPDATE ENDPOINTS (Admin only)
# ============================================================================

@learning_module_bp.route('/update-knowledge', methods=['POST'])
def update_knowledge():
    """
    Update knowledge base with new information.

    POST body:
        {
            "category": "...",
            "subcategory": "...",
            "updates": {...}
        }

    Returns:
        JSON success confirmation
    """
    if not _require_user_or_401():
        abort(401)

    # Check if admin (can add check here)
    incr_metric("learning_updates_total")

    data = request.get_json() or {}

    category = data.get('category')
    subcategory = data.get('subcategory')
    updates = data.get('updates', {})

    if not category or not subcategory:
        return jsonify({
            "error": "Missing 'category' or 'subcategory' parameter"
        }), 400

    success = module.update_knowledge(category, subcategory, updates)

    if success:
        return jsonify({
            "success": True,
            "message": f"Knowledge base updated: {category}/{subcategory}"
        }), 200
    else:
        return jsonify({
            "error": f"Category '{category}' not found"
        }), 400


# ============================================================================
# HEALTH CHECK
# ============================================================================

@learning_module_bp.route('/health', methods=['GET'])
def module_health():
    """Health check endpoint (no auth required)."""
    return jsonify({
        "status": "healthy",
        "module": "preliminary_learning",
        "version": "1.0"
    }), 200
