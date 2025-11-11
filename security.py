"""Security and token helpers used by Semptify and tests."""

import os
import json
import hashlib
import secrets
import uuid
import time
from datetime import datetime, timezone
from typing import Any, Optional
from flask import session, request

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def _resolve_paths():
    """Resolve paths to security files, preferring cwd."""
    cwd = os.getcwd()
    sec_dir = os.path.join(cwd, "security") if os.path.isdir(os.path.join(cwd, "security")) else os.path.join(ROOT_DIR, "security")
    users_path = os.path.join(sec_dir, "users.json")
    admin_tokens_path = os.path.join(sec_dir, "admin_tokens.json")
    logs_dir = os.path.join(cwd, "logs") if os.path.isdir(os.path.join(cwd, "logs")) else os.path.join(ROOT_DIR, "logs")
    events_log = os.path.join(logs_dir, "events.log")
    return sec_dir, users_path, admin_tokens_path, logs_dir, events_log

# Public paths
def get_security_dir():
    return _resolve_paths()[0]

def get_users_file():
    return _resolve_paths()[1]

def get_admin_tokens_file():
    return _resolve_paths()[2]

ADMIN_FILE = get_admin_tokens_file()

# ============================================================================
# Metrics & Logging
# ============================================================================

_metrics = {
    'requests_total': 0,
    'admin_requests_total': 0,
    'admin_actions_total': 0,
    'errors_total': 0,
    'releases_total': 0,
    'rate_limited_total': 0,
    'breakglass_used_total': 0,
    'token_rotations_total': 0,
}

def incr_metric(name: str, delta: int = 1):
    """Increment a counter metric."""
    if name in _metrics:
        _metrics[name] += delta

def get_metrics() -> dict:
    """Get all metrics."""
    return dict(_metrics)

def log_event(event_type: str, details: dict = None):
    """Log an event to events.log (JSON format)."""
    try:
        _, _, _, logs_dir, events_log = _resolve_paths()
        os.makedirs(logs_dir, exist_ok=True)
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': event_type,
            'details': details or {}
        }
        with open(events_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')
    except Exception:
        pass

def record_request_latency(latency: float):
    """Record request latency (for metrics)."""
    pass

# ============================================================================
# CSRF Token Handling
# ============================================================================

def _get_or_create_csrf_token():
    """Get or create CSRF token for the session."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

# ============================================================================
# Token Management
# ============================================================================

def _hash_token(token: str) -> str:
    """Hash a token using SHA256."""
    return hashlib.sha256(token.encode()).hexdigest()

def _load_json(path: str, default=None):
    """Load JSON from file, with fallback."""
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default if default is not None else {}

def _atomic_write_json(path: str, data: Any):
    """Atomically write JSON data to a file."""
    import tempfile
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    
    # Write to temp file first
    fd, temp_path = tempfile.mkstemp(dir=dir_path, suffix='.json.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        # Atomic rename
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on error
        try:
            os.remove(temp_path)
        except Exception:
            pass
        raise

def get_token_from_request(request) -> Optional[str]:
    """Extract user token from request (header, args, or form)."""
    return (
        request.headers.get('X-User-Token') or
        request.args.get('user_token') or
        request.form.get('user_token')
    )

def validate_user_token(token: Optional[str]) -> Optional[str]:
    """Validate a user token and return the user ID if valid."""
    if not token:
        return None

    users_file = get_users_file()
    try:
        users_data = _load_json(users_file, {})
        h = _hash_token(token)

        # Users can be stored as dict or list
        if isinstance(users_data, dict):
            for user_id, user_info in users_data.items():
                if isinstance(user_info, dict):
                    stored_hash = user_info.get('hash')
                else:
                    stored_hash = user_info
                if stored_hash == h:
                    return user_id
        elif isinstance(users_data, list):
            for user in users_data:
                if isinstance(user, dict) and user.get('hash') == h:
                    return user.get('id')
    except Exception:
        pass

    return None

def save_user_token() -> str:
    """
    Generate a new user token, save its hash to users.json, and return the plain token.
    This token should be shown to the user ONCE for vault access.
    """
    import secrets
    import json
    from datetime import datetime

    # Generate a simple numeric token (easier to remember/type)
    token = ''.join([str(secrets.randbelow(10)) for _ in range(16)])
    user_id = f"user_{secrets.token_hex(8)}"

    users_file = get_users_file()
    users_data = _load_json(users_file, {})

    # Store hash with metadata
    users_data[user_id] = {
        'hash': _hash_token(token),
        'created': datetime.now().isoformat(),
        'type': 'vault_user'
    }

    # Save to file
    os.makedirs(os.path.dirname(users_file), exist_ok=True)
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2)

    log_event('user_registered', {'user_id': user_id})
    return token

def validate_admin_token(token: Optional[str]) -> Optional[str]:
    """Validate an admin token and return the token ID if valid.

    Checks in order:
    1. MASTER_KEY environment variable (superadmin access to admin functions)
    2. ADMIN_TOKEN environment variable (legacy single admin)
    3. admin_tokens.json (multi-admin support)

    IMPORTANT: Admin tokens grant access to admin functions (settings, logs, etc.)
    but DO NOT bypass vault privacy. Only document owners can access their vault.
    """
    if not token:
        return None

    # Check MASTER_KEY first (superadmin access to admin functions)
    # NOTE: Does NOT grant access to user vaults - only document owner can access
    master_key = os.getenv("MASTER_KEY")
    if master_key and token == master_key:
        log_event('master_key_used', {'ip': request.remote_addr if request else 'unknown'})
        return "master_admin"

    # Check breakglass (emergency one-time access)
    if is_breakglass_active():
        # Check if token has breakglass permission
        admin_file = get_admin_tokens_file()
        try:
            adata = _load_json(admin_file, {})
            h = _hash_token(token)
            if isinstance(adata, dict):
                for token_id, token_info in adata.items():
                    if isinstance(token_info, dict):
                        stored_hash = token_info.get('hash')
                        has_breakglass = token_info.get('breakglass', False)
                        if stored_hash == h and has_breakglass:
                            consume_breakglass()  # One-time use
                            log_event('breakglass_used', {'token_id': token_id, 'ip': request.remote_addr if request else 'unknown'})
                            return f"breakglass_{token_id}"
        except Exception:
            pass

    # Check environment variable (legacy support)
    env_token = os.getenv("ADMIN_TOKEN")
    if env_token and token == env_token:
        return "env_admin"

    # Check admin_tokens.json
    admin_file = get_admin_tokens_file()
    try:
        adata = _load_json(admin_file, {})
        h = _hash_token(token)

        if isinstance(adata, dict):
            for token_id, token_info in adata.items():
                if isinstance(token_info, dict):
                    stored_hash = token_info.get('hash')
                else:
                    stored_hash = token_info
                if stored_hash == h:
                    return token_id
        elif isinstance(adata, list):
            for item in adata:
                if isinstance(item, dict) and item.get('hash') == h:
                    return item.get('id')
    except Exception:
        pass

    return None

# ============================================================================
# Rate Limiting
# ============================================================================

_rate_limit_buckets = {}

def check_rate_limit(key: str) -> bool:
    """Check if a rate limit key is within acceptable limits.
    Returns True if request is allowed, False if rate limited.
    Uses sliding window with env vars: ADMIN_RATE_WINDOW (seconds), ADMIN_RATE_MAX (count).
    """
    window = int(os.getenv("ADMIN_RATE_WINDOW", "60"))
    max_requests = int(os.getenv("ADMIN_RATE_MAX", "60"))

    now = time.time()
    bucket = _rate_limit_buckets.get(key, [])

    # Remove old entries outside the window
    bucket = [ts for ts in bucket if now - ts < window]

    if len(bucket) >= max_requests:
        incr_metric("rate_limited_total", 1)
        log_event("rate_limited", {"key": key})
        return False

    bucket.append(now)
    _rate_limit_buckets[key] = bucket
    return True

# ============================================================================
# Breakglass Access
# ============================================================================

_breakglass_used = False

def is_breakglass_active() -> bool:
    """Check if breakglass.flag file exists."""
    sec_dir = get_security_dir()
    return os.path.exists(os.path.join(sec_dir, "breakglass.flag"))

def consume_breakglass():
    """Remove the breakglass.flag file (one-time use)."""
    global _breakglass_used
    if not _breakglass_used:
        sec_dir = get_security_dir()
        flag_path = os.path.join(sec_dir, "breakglass.flag")
        try:
            if os.path.exists(flag_path):
                os.remove(flag_path)
            _breakglass_used = True
            incr_metric("breakglass_used_total", 1)
            log_event("breakglass_consumed")
        except Exception:
            pass

# ============================================================================
# Admin Authorization
# ============================================================================

def _require_admin_or_401() -> bool:
    """Check if current request is authorized as admin."""
    t = request.headers.get("X-Admin-Token") or request.args.get("token") or request.args.get("admin_token")

    # If running in open mode and no token supplied, allow
    if not t and os.getenv("SECURITY_MODE", "open") == "open":
        return True

    if not t:
        return False

    aid = validate_admin_token(t)
    if aid:
        incr_metric("admin_requests_total", 1)
        return True

    return False

def _require_user_or_401() -> bool:
    """Check if current request has valid user token."""
    t = (request.headers.get("X-User-Token") or
         request.args.get("user_token") or
         request.form.get("user_token"))

    if not t:
        return False

    uid = validate_user_token(t)
    return uid is not None
