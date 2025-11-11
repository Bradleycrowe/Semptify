"""
DEPRECATED: JSON-based user registration and verification (pending_users.json, users.json).

This module has been superseded by SQLite-backed `user_database.py` that manages both
pending users and verified users atomically. It remains in the repo for historical
reference and to ease migrations/tests that import it, but new code must use
`user_database` exclusively.

Note: Functions here are still callable and used by some older scripts, but the active
Flask auth blueprint has been fully migrated to `user_database`.
"""
import json
import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

USERS_FILE = "security/users.json"
PENDING_FILE = "security/pending_users.json"

def _ensure_security_dir():
    """Ensure security directory exists"""
    os.makedirs("security", exist_ok=True)

def _load_json(filepath: str) -> Dict:
    """Load JSON file or return empty dict"""
    _ensure_security_dir()
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def _save_json(filepath: str, data: Dict):
    """Save data to JSON file"""
    _ensure_security_dir()
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def hash_code(code: str) -> str:
    """Hash a verification code for storage"""
    return hashlib.sha256(code.encode()).hexdigest()

def create_pending_user(form_data: dict, verification_method: str) -> tuple[str, str]:
    """
    Create a pending user registration
    Returns: (user_id, verification_code)
    """
    pending = _load_json(PENDING_FILE)
    
    # Generate unique user ID
    user_id = secrets.token_urlsafe(16)
    
    # Generate verification code
    code = generate_verification_code()
    
    # Store pending user with hashed code
    pending[user_id] = {
        'first_name': form_data.get('first_name'),
        'last_name': form_data.get('last_name'),
        'email': form_data.get('email'),
        'phone': form_data.get('phone'),
        'address': form_data.get('address'),
        'city': form_data.get('city'),
        'county': form_data.get('county'),
        'state': form_data.get('state'),
        'zip': form_data.get('zip'),
        'verification_method': verification_method,
        'code_hash': hash_code(code),
        'created_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(minutes=10)).isoformat(),
        'attempts': 0
    }
    
    _save_json(PENDING_FILE, pending)
    return user_id, code

def verify_code(user_id: str, code: str) -> tuple[bool, Optional[str]]:
    """
    Verify a code for a pending user
    Returns: (success, error_message)
    """
    pending = _load_json(PENDING_FILE)
    
    if user_id not in pending:
        return False, "Invalid verification session"
    
    user_data = pending[user_id]
    
    # Check expiration
    expires_at = datetime.fromisoformat(user_data['expires_at'])
    if datetime.now() > expires_at:
        return False, "Verification code expired. Please register again."
    
    # Check attempts
    if user_data['attempts'] >= 5:
        return False, "Too many attempts. Please register again."
    
    # Verify code
    if hash_code(code) != user_data['code_hash']:
        user_data['attempts'] += 1
        _save_json(PENDING_FILE, pending)
        return False, f"Invalid code. {5 - user_data['attempts']} attempts remaining."
    
    # Code is valid - activate user
    users = _load_json(USERS_FILE)
    
    # Create verified user record
    users[user_id] = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'phone': user_data['phone'],
        'address': user_data['address'],
        'city': user_data['city'],
        'county': user_data['county'],
        'state': user_data['state'],
        'zip': user_data['zip'],
        'verified_at': datetime.now().isoformat(),
        'status': 'active'
    }
    
    _save_json(USERS_FILE, users)
    
    # Remove from pending
    del pending[user_id]
    _save_json(PENDING_FILE, pending)
    
    return True, None

def get_pending_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get pending user data"""
    pending = _load_json(PENDING_FILE)
    return pending.get(user_id)

def resend_verification_code(user_id: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Resend verification code to a pending user
    Returns: (success, new_code, error_message)
    """
    pending = _load_json(PENDING_FILE)
    
    if user_id not in pending:
        return False, None, "Invalid verification session"
    
    user_data = pending[user_id]
    
    # Generate new code
    code = generate_verification_code()
    
    # Update pending user with new code and extended expiration
    user_data['code_hash'] = hash_code(code)
    user_data['expires_at'] = (datetime.now() + timedelta(minutes=10)).isoformat()
    user_data['attempts'] = 0  # Reset attempts
    
    _save_json(PENDING_FILE, pending)
    
    return True, code, None

def mask_contact(contact: str, method: str) -> str:
    """Mask email or phone for display"""
    if method == 'email' or '@' in contact:
        parts = contact.split('@')
        if len(parts) == 2:
            username = parts[0]
            domain = parts[1]
            masked = username[0] + '***' if len(username) > 1 else '***'
            return f"{masked}@{domain}"
    else:  # phone
        # Keep last 4 digits
        if len(contact) >= 4:
            return '***-***-' + contact[-4:]
    return '***'
