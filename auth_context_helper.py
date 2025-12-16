"""
Context Data Loop Process Helper
Tracks authorization state to prevent redirect loops
"""
import time
from flask import session

def init_auth_context():
    """Initialize or get auth context tracker"""
    if 'auth_context' not in session:
        session['auth_context'] = {
            'setup_visits': [],
            'oauth_completed': False,
            'storage_connected': False,
            'token_validated': False,
            'last_path': None,
            'bypass_auth': False
        }
    return session['auth_context']

def track_setup_visit():
    """Track visit to /setup route"""
    ctx = init_auth_context()
    now = time.time()
    # Keep only visits from last 60 seconds
    ctx['setup_visits'] = [v for v in ctx['setup_visits'] if now - v < 60]
    ctx['setup_visits'].append(now)
    session.modified = True
    return len(ctx['setup_visits'])

def should_bypass_auth():
    """Check if we should bypass auth due to loop"""
    ctx = init_auth_context()
    visit_count = len([v for v in ctx['setup_visits'] if time.time() - v < 30])
    return visit_count >= 3 or ctx.get('bypass_auth', False)

def mark_oauth_complete():
    """Mark OAuth flow as completed"""
    ctx = init_auth_context()
    ctx['oauth_completed'] = True
    ctx['oauth_ts'] = time.time()
    session.modified = True

def mark_storage_connected(storage_type):
    """Mark storage as connected"""
    ctx = init_auth_context()
    ctx['storage_connected'] = True
    ctx['storage_type'] = storage_type
    session.modified = True

def mark_token_validated(token):
    """Mark token as validated"""
    ctx = init_auth_context()
    ctx['token_validated'] = True
    ctx['token'] = token[:8] + '...'  # Store partial for debug
    session.modified = True

def is_auth_complete():
    """Check if authorization is complete"""
    ctx = init_auth_context()
    return (ctx.get('oauth_completed') and 
            ctx.get('storage_connected') and 
            ctx.get('token_validated'))

def reset_auth_context():
    """Clear auth context"""
    session.pop('auth_context', None)
    session.modified = True
