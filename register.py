"""
User Registration Blueprint for Semptify

Provides registration flow for new users with anonymous token-based identity.
"""
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import os
import json
import secrets
import hashlib
from datetime import datetime

register_bp = Blueprint('register_bp', __name__)

SECURITY_DIR = os.path.join(os.getcwd(), 'security')

def _hash_token(token):
    """Hash a token using SHA-256"""
    return hashlib.sha256(token.encode()).hexdigest()

def _load_users():
    """Load users from security/users.json"""
    users_path = os.path.join(SECURITY_DIR, 'users.json')
    if os.path.exists(users_path):
        try:
            with open(users_path, 'r') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return list(data.values()) if data else []
                return []
        except:
            return []
    return []

def _save_users(users):
    """Save users to security/users.json"""
    os.makedirs(SECURITY_DIR, exist_ok=True)
    users_path = os.path.join(SECURITY_DIR, 'users.json')
    with open(users_path, 'w') as f:
        json.dump(users, f, indent=2)

def _generate_user_token():
    """Generate a 12-digit anonymous token"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(12)])

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and form handler"""
    if request.method == 'GET':
        return render_template('register.html')
    
    # POST: Process registration
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    address = request.form.get('address', '')
    city = request.form.get('city', '')
    county = request.form.get('county', '')
    state = request.form.get('state', '')
    zip_code = request.form.get('zip', '')
    verify_method = request.form.get('verify_method', 'email')
    
    # Generate anonymous token
    user_token = _generate_user_token()
    user_id = f"u_{secrets.token_hex(4)}"
    
    # Create user entry
    users = _load_users()
    new_user = {
        'id': user_id,
        'hash': _hash_token(user_token),
        'enabled': True,
        'created_at': datetime.utcnow().isoformat(),
        'profile': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'county': county,
            'state': state,
            'zip': zip_code
        },
        'verify_method': verify_method,
        'verified': False
    }
    users.append(new_user)
    _save_users(users)
    
    # Store token in session for verification page
    from flask import session
    session['pending_user_token'] = user_token
    session['pending_user_id'] = user_id
    session['verify_method'] = verify_method
    
    # Redirect to verification
    return redirect('/verify')

@register_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """Verification page"""
    from flask import session
    if request.method == 'GET':
        user_token = session.get('pending_user_token')
        verify_method = session.get('verify_method', 'email')
        return render_template('verify.html', 
                             user_token=user_token,
                             verify_method=verify_method)
    
    # POST: Process verification code
    code = request.form.get('code', '')
    # For now, accept any code (in production, validate against sent code)
    user_id = session.get('pending_user_id')
    if user_id:
        users = _load_users()
        for user in users:
            if user.get('id') == user_id:
                user['verified'] = True
                break
        _save_users(users)
    
    user_token = session.get('pending_user_token')
    return render_template('register_success.html', 
                         user_token=user_token,
                         message='Registration complete! Here is your one-time token.')

