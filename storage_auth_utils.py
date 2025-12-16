"""
Session Token System for Semptify

Architecture:
1. Permanent token stored securely in R2/storage (never exposed to client)
2. User authenticates once with permanent token
3. System generates temporary session token (default 24 hours)
4. All subsequent requests use session token
5. Session token can be refreshed before expiry
6. Permanent token only needed to create new sessions
"""

import secrets
import string
import hashlib
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from functools import wraps

# Configuration
SESSION_DURATION_HOURS = int(os.getenv('SESSION_DURATION_HOURS', '24'))
SESSION_TOKEN_LENGTH = 32
PERMANENT_TOKEN_LENGTH = 48
 CAN YOU MAKE A WELL THOUGHT# Role and storage codes for user ID generation
ROLE_CODES: Dict[str, str] = {
    'user': 'U',
    'admin': 'A', 
    'manager': 'M',
    'attorney': 'L',
    'advocate': 'V',
}

STORAGE_CODES: Dict[str, str] = {
    'google_drive': 'G',
    'dropbox': 'D',
    'r2': 'R',
    'local': 'X',
}

_CHARS = string.ascii_uppercase + string.digits


def _hash(token: str) -> str:
    """SHA-256 hash a token."""
    return hashlib.sha256(token.encode()).hexdigest()


def generate_user_id(role: str = 'user', storage: str = 'r2') -> str:
    """Generate 7-char user ID encoding role + storage + 5 random chars."""
    role_code = ROLE_CODES.get(role, 'U')
    storage_code = STORAGE_CODES.get(storage, 'R')
    random_part = ''.join(secrets.choice(_CHARS) for _ in range(5))
    return f"{role_code}{storage_code}{random_part}"


def parse_user_id(user_id: str) -> Dict[str, str]:
    """Parse user ID back to components."""
    if len(user_id) != 7:
        raise ValueError("Invalid user_id length")
    role_code = user_id[0]
    storage_code = user_id[1]
    role = {v: k for k, v in ROLE_CODES.items()}.get(role_code, 'user')
    storage = {v: k for k, v in STORAGE_CODES.items()}.get(storage_code, 'local')
    return {
        'role': role,
        'storage': storage,
        'random': user_id[2:],
        'full_id': user_id,
    }


def generate_permanent_token() -> str:
    """Generate a permanent token (stored securely, never sent to client directly)."""
    return secrets.token_urlsafe(PERMANENT_TOKEN_LENGTH)


def generate_session_token() -> str:
    """Generate a temporary session token for client use."""
    return secrets.token_urlsafe(SESSION_TOKEN_LENGTH)


class SessionManager:
    """
    Manages session tokens backed by permanent tokens in storage.
    
    Flow:
    1. create_session(permanent_token) -> session_token, expires_at
    2. validate_session(session_token) -> user_id or None
    3. refresh_session(session_token) -> new_session_token, expires_at
    4. revoke_session(session_token) -> bool
    """
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.path.join(
            os.getcwd(), 'security', 'sessions.json'
        )
        self._sessions: Dict[str, dict] = {}  # session_hash -> {user_id, expires_at, permanent_hash}
        self._permanent_tokens: Dict[str, str] = {}  # permanent_hash -> user_id
        self._load()
    
    def _load(self):
        """Load sessions from storage."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self._sessions = data.get('sessions', {})
                    self._permanent_tokens = data.get('permanent_tokens', {})
                    self._cleanup_expired()
        except Exception:
            self._sessions = {}
            self._permanent_tokens = {}
    
    def _save(self):
        """Save sessions to storage."""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'sessions': self._sessions,
                    'permanent_tokens': self._permanent_tokens,
                }, f, indent=2)
        except Exception as e:
            print(f"[SESSION] Failed to save: {e}")
    
    def _cleanup_expired(self):
        """Remove expired sessions."""
        now = time.time()
        expired = [h for h, s in self._sessions.items() if s.get('expires_at', 0) < now]
        for h in expired:
            del self._sessions[h]
        if expired:
            self._save()
    
    def register_permanent_token(self, user_id: str, permanent_token: str) -> bool:
        """Register a permanent token for a user (done once during setup)."""
        token_hash = _hash(permanent_token)
        self._permanent_tokens[token_hash] = user_id
        self._save()
        return True
    
    def create_session(self, permanent_token: str, duration_hours: int = None) -> Tuple[Optional[str], Optional[float]]:
        """
        Create a new session using permanent token.
        Returns (session_token, expires_at) or (None, None) if invalid.
        """
        duration = duration_hours or SESSION_DURATION_HOURS
        perm_hash = _hash(permanent_token)
        
        user_id = self._permanent_tokens.get(perm_hash)
        if not user_id:
            return None, None
        
        # Generate session token
        session_token = generate_session_token()
        session_hash = _hash(session_token)
        expires_at = time.time() + (duration * 3600)
        
        self._sessions[session_hash] = {
            'user_id': user_id,
            'expires_at': expires_at,
            'permanent_hash': perm_hash,
            'created_at': time.time(),
        }
        self._save()
        
        return session_token, expires_at
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """
        Validate a session token.
        Returns user_id if valid and not expired, None otherwise.
        """
        if not session_token:
            return None
        
        session_hash = _hash(session_token)
        session = self._sessions.get(session_hash)
        
        if not session:
            return None
        
        if session.get('expires_at', 0) < time.time():
            # Expired - remove it
            del self._sessions[session_hash]
            self._save()
            return None
        
        return session.get('user_id')
    
    def refresh_session(self, session_token: str, duration_hours: int = None) -> Tuple[Optional[str], Optional[float]]:
        """
        Refresh a session - generates new token, invalidates old one.
        Returns (new_session_token, expires_at) or (None, None) if invalid.
        """
        duration = duration_hours or SESSION_DURATION_HOURS
        session_hash = _hash(session_token)
        session = self._sessions.get(session_hash)
        
        if not session or session.get('expires_at', 0) < time.time():
            return None, None
        
        # Create new session
        new_token = generate_session_token()
        new_hash = _hash(new_token)
        expires_at = time.time() + (duration * 3600)
        
        self._sessions[new_hash] = {
            'user_id': session['user_id'],
            'expires_at': expires_at,
            'permanent_hash': session['permanent_hash'],
            'created_at': time.time(),
        }
        
        # Remove old session
        del self._sessions[session_hash]
        self._save()
        
        return new_token, expires_at
    
    def revoke_session(self, session_token: str) -> bool:
        """Revoke/logout a session."""
        session_hash = _hash(session_token)
        if session_hash in self._sessions:
            del self._sessions[session_hash]
            self._save()
            return True
        return False
    
    def revoke_all_user_sessions(self, user_id: str) -> int:
        """Revoke all sessions for a user."""
        to_remove = [h for h, s in self._sessions.items() if s.get('user_id') == user_id]
        for h in to_remove:
            del self._sessions[h]
        if to_remove:
            self._save()
        return len(to_remove)
    
    def get_session_info(self, session_token: str) -> Optional[dict]:
        """Get session info without validating."""
        session_hash = _hash(session_token)
        session = self._sessions.get(session_hash)
        if not session:
            return None
        
        expires_at = session.get('expires_at', 0)
        return {
            'user_id': session.get('user_id'),
            'expires_at': expires_at,
            'expires_in_seconds': max(0, expires_at - time.time()),
            'created_at': session.get('created_at'),
            'is_expired': expires_at < time.time(),
        }


# Global session manager instance
_session_manager: Optional[SessionManager] = None

def get_session_manager() -> SessionManager:
    """Get or create the global session manager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


# Flask integration helpers
def get_session_token_from_request(request) -> Optional[str]:
    """Extract session token from Flask request."""
    # Check Authorization header first
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    # Check X-Session-Token header
    session_token = request.headers.get('X-Session-Token')
    if session_token:
        return session_token
    
    # Check query param
    session_token = request.args.get('session_token')
    if session_token:
        return session_token
    
    # Check cookie
    session_token = request.cookies.get('semptify_session')
    if session_token:
        return session_token
    
    return None


def require_session(f):
    """Decorator to require valid session for a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify, g
        
        session_token = get_session_token_from_request(request)
        if not session_token:
            return jsonify({'error': 'No session token provided'}), 401
        
        user_id = get_session_manager().validate_session(session_token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Store user_id in Flask's g for route access
        g.user_id = user_id
        g.session_token = session_token
        
        return f(*args, **kwargs)
    return decorated
