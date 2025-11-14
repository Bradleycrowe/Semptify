"""
Enhanced authentication with persistent login and remember-me tokens
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from user_database import _get_db

def create_remember_token(user_id: str, days: int = 30) -> str:
    """Create a persistent remember-me token for user"""
    conn = _get_db()
    cursor = conn.cursor()
    
    # Generate secure token
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires = (datetime.now() + timedelta(days=days)).isoformat()
    
    # Store hashed token
    cursor.execute('''
        INSERT INTO remember_tokens (user_id, token_hash, expires_at, created_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, token_hash, expires, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return token

def verify_remember_token(token: str) -> str:
    """Verify remember token and return user_id if valid"""
    if not token:
        return None
        
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT rt.user_id, rt.expires_at, u.first_name, u.last_name
        FROM remember_tokens rt
        JOIN users u ON rt.user_id = u.user_id
        WHERE rt.token_hash = ? AND rt.expires_at > ?
    ''', (token_hash, datetime.now().isoformat()))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'user_id': result[0],
            'expires_at': result[1],
            'first_name': result[2],
            'last_name': result[3]
        }
    return None

def delete_remember_token(token: str):
    """Delete a remember token (for logout)"""
    if not token:
        return
        
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM remember_tokens WHERE token_hash = ?', (token_hash,))
    conn.commit()
    conn.close()

def cleanup_expired_tokens():
    """Remove expired remember tokens"""
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM remember_tokens WHERE expires_at < ?', (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
