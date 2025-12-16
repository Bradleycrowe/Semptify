"""
EMERGENCY BYPASS - storage_autologin.py
Allows access to EVERYTHING with no authentication
FOR PERSONAL USE ONLY
"""
from flask import Blueprint, request, session, g
import os

storage_autologin_bp = Blueprint('storage_autologin', __name__)

@storage_autologin_bp.before_app_request
def check_storage_auth():
    """EMERGENCY BYPASS: Allow everything"""
    # Skip OAuth routes and static files
    if request.path.startswith(('/oauth/', '/static/')):
        return
    
    # Set fake session for compatibility
    if not session.get('bypass_mode'):
        session['bypass_mode'] = True
        session['authenticated'] = True
        session['user_token'] = '999999999999'  # Fake token
        session['storage_connected'] = True
        session['storage_type'] = 'local'
    
    # Allow ALL requests
    return None

@storage_autologin_bp.route('/clear-session')
def clear_session():
    """Clear session"""
    session.clear()
    return 'Session cleared'
