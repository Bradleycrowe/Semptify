"""
Onboarding Flow - Collects essential user info to activate reasoning engine
and populate cells with relevant content.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from user_database import get_user, log_user_interaction
from reasoning_engine import get_reasoning_engine
import json

onboarding_bp = Blueprint('onboarding', __name__)


@onboarding_bp.route('/onboarding')
def onboarding_start():
    """Start onboarding flow - gather essential info."""
    return render_template('onboarding.html')


@onboarding_bp.route('/api/onboarding/submit', methods=['POST'])
def onboarding_submit():
    """
    Process onboarding data and initialize user profile.
    
    Required data:
    - location (city, state, zip)
    - issue_type (eviction, repair, harassment, etc.)
    - urgency (immediate, days, weeks)
    - has_court_date (yes/no)
    - court_date (if yes)
    """
    try:
        data = request.get_json()
        user_token = request.headers.get('X-User-Token') or session.get('user_token')
        
        if not user_token:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Get user
        user = get_user(user_token)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user_id = user['id']
        
        # Extract onboarding data
        location = data.get('location', {})
        issue_type = data.get('issue_type')
        urgency = data.get('urgency')
        has_court_date = data.get('has_court_date', False)
        court_date = data.get('court_date')
        additional_notes = data.get('notes', '')
        
        # Build context for reasoning engine
        context = {
            "location": f"{location.get('city')}, {location.get('state')}",
            "zip": location.get('zip'),
            "issue_type": issue_type,
            "urgency": urgency,
            "has_court_date": has_court_date,
            "court_date": court_date,
            "user_stress_level": "high" if urgency == "immediate" else "medium",
            "severity": "high" if has_court_date else "medium"
        }
        
        # Log the onboarding interaction
        log_user_interaction(
            user_id=user_id,
            action="onboarding_complete",
            details=json.dumps(context)
        )
        
        # Run reasoning engine to generate initial content
        reasoning = get_reasoning_engine()
        analysis = reasoning.analyze_situation(user_id, context)
        
        # Store context in session for dashboard
        session['user_context'] = context
        session['onboarding_complete'] = True
        
        return jsonify({
            "success": True,
            "message": "Onboarding complete",
            "analysis": analysis,
            "redirect": "/dashboard"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@onboarding_bp.route('/api/onboarding/skip', methods=['POST'])
def onboarding_skip():
    """Skip onboarding - use default context."""
    try:
        user_token = request.headers.get('X-User-Token') or session.get('user_token')
        
        if not user_token:
            return jsonify({"error": "Not authenticated"}), 401
        
        user = get_user(user_token)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Set default context
        session['user_context'] = {
            "location": "general",
            "issue_type": "general",
            "urgency": "medium",
            "severity": "medium"
        }
        session['onboarding_complete'] = True
        
        return jsonify({
            "success": True,
            "redirect": "/dashboard"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
