"""
Calendar Master View - Central hub for vault documents, events, and packet assembly
"""
from flask import Blueprint, render_template, request, jsonify
from functools import wraps

calendar_master_bp = Blueprint('calendar_master', __name__)

def _get_user_token():
    """Extract user token from request"""
    return request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')

@calendar_master_bp.route('/calendar')
def calendar_master():
    """Master calendar view - visual reference to documented journey"""
    user_token = _get_user_token()
    return render_template('calendar_master.html', user_token=user_token)

@calendar_master_bp.route('/api/calendar/vault-items')
def vault_items():
    """Get all vault items organized by date"""
    # TODO: Integrate with vault to fetch user documents
    # For now, return structure
    return jsonify({
        "items": [],
        "categories": ["evidence", "receipts", "correspondence", "photos", "recordings"],
        "timeline": []
    })

@calendar_master_bp.route('/api/calendar/packet-builder')
def packet_builder():
    """Get available items for court packet assembly"""
    return jsonify({
        "available_items": [],
        "packet_types": ["eviction_defense", "repair_claim", "discrimination", "security_deposit"],
        "templates": []
    })
