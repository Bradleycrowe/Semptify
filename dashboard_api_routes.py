"""
Dashboard API Routes - Serve dynamic content to cells A-F
"""

from flask import Blueprint, jsonify, request
from dashboard_engine import get_dashboard_engine, AVAILABLE_WIDGETS

dashboard_api_bp = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')

@dashboard_api_bp.route('/layout/<user_id>', methods=['GET'])
def get_layout(user_id):
    """Get complete dashboard layout for user."""
    engine = get_dashboard_engine()
    layout = engine.get_user_layout(user_id)
    
    # Include widget details
    result = {}
    for cell, widget_id in layout.items():
        if widget_id in AVAILABLE_WIDGETS:
            result[cell] = {
                "widget_id": widget_id,
                **AVAILABLE_WIDGETS[widget_id]
            }
    
    return jsonify(result)

@dashboard_api_bp.route('/cell/<user_id>/<cell>', methods=['GET'])
def get_cell(user_id, cell):
    """Get content for a specific cell."""
    if cell not in ['a', 'b', 'c', 'd', 'e', 'f']:
        return jsonify({"error": "Invalid cell"}), 400
    
    engine = get_dashboard_engine()
    content = engine.get_cell_content(user_id, cell)
    return jsonify(content)

@dashboard_api_bp.route('/progress/<user_id>', methods=['POST'])
def update_progress(user_id):
    """Update user progress (triggers layout recalculation)."""
    data = request.get_json()
    engine = get_dashboard_engine()
    engine.update_user_progress(user_id, data)
    return jsonify({"success": True})

@dashboard_api_bp.route('/widgets', methods=['GET'])
def list_widgets():
    """List all available widgets."""
    return jsonify(AVAILABLE_WIDGETS)
