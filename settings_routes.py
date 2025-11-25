"""
Settings Page Routes
User account information and storage management
"""

from flask import Blueprint, render_template, request, session, redirect, url_for
from core.storage import UnifiedStorageBackend
import json
import os
from datetime import datetime

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/settings')
def settings_page():
    """Display user settings and account information"""
    
    # Get token from query param or session
    token = request.args.get('user_token') or session.get('user_token')
    
    if not token:
        return redirect(url_for('register'))
    
    # Validate token
    if not UnifiedStorageBackend.validate_token(token):
        return 'Invalid token', 401
    
    # Get user info from security/users.json
    user_info = None
    try:
        with open('security/users.json', 'r') as f:
            users = json.load(f)
            token_hash = UnifiedStorageBackend.hash_token(token)
            user_info = users.get(token_hash, {})
    except:
        user_info = {}
    
    # Prepare settings data
    settings_data = {
        'token': token,
        'token_masked': f"{token[:4]}...{token[-4:]}",
        'created_at': user_info.get('created_at', 'Unknown'),
        'storage_provider': user_info.get('provider', session.get('storage_provider', 'Unknown')),
        'vault_url': url_for('vault_bp.vault_home', user_token=token, _external=True),
        'timeline_url': url_for('timeline', user_token=token, _external=True) if 'timeline' else None
    }
    
    return render_template('settings.html', **settings_data)


@settings_bp.route('/settings/change-storage', methods=['POST'])
def change_storage():
    """Redirect to storage setup to change provider"""
    
    token = request.form.get('user_token') or session.get('user_token')
    
    if not token or not UnifiedStorageBackend.validate_token(token):
        return 'Invalid token', 401
    
    # Redirect to storage setup
    return redirect(url_for('storage_setup.choose_storage'))
