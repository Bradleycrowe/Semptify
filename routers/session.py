"""
Session Management Router - FastAPI
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import time
import secrets
import hashlib
import json
import os

router = APIRouter()
security = HTTPBearer(auto_error=False)

# ============================================================================
# MODELS
# ============================================================================

class CreateSessionRequest(BaseModel):
    permanent_token: str
    duration_hours: Optional[int] = 24

class RegisterRequest(BaseModel):
    role: Optional[str] = "user"
    storage: Optional[str] = "r2"

class RefreshRequest(BaseModel):
    duration_hours: Optional[int] = 24

# ============================================================================
# SESSION MANAGER
# ============================================================================

class SessionManager:
    """Manages permanent tokens and temporary sessions."""
    
    def __init__(self):
        self.sessions: dict = {}  # session_token_hash -> {user_id, expires_at, permanent_token_hash}
        self.permanent_tokens: dict = {}  # permanent_token_hash -> user_id
        self._load_permanent_tokens()
    
    def _hash(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
    
    def _load_permanent_tokens(self):
        """Load permanent tokens from security/session_tokens.json"""
        path = "security/session_tokens.json"
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self.permanent_tokens = json.load(f)
            except:
                pass
    
    def _save_permanent_tokens(self):
        """Save permanent tokens to file."""
        path = "security/session_tokens.json"
        os.makedirs("security", exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.permanent_tokens, f, indent=2)
    
    def register_permanent_token(self, user_id: str, permanent_token: str) -> bool:
        """Register a new permanent token for a user."""
        token_hash = self._hash(permanent_token)
        self.permanent_tokens[token_hash] = user_id
        self._save_permanent_tokens()
        return True
    
    def validate_permanent_token(self, token: str) -> Optional[str]:
        """Validate permanent token, return user_id or None."""
        token_hash = self._hash(token)
        return self.permanent_tokens.get(token_hash)
    
    def create_session(self, permanent_token: str, duration_hours: int = 24) -> tuple:
        """Create session from permanent token. Returns (session_token, expires_at) or (None, None)."""
        user_id = self.validate_permanent_token(permanent_token)
        if not user_id:
            return None, None
        
        session_token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + (duration_hours * 3600)
        
        session_hash = self._hash(session_token)
        perm_hash = self._hash(permanent_token)
        
        self.sessions[session_hash] = {
            "user_id": user_id,
            "expires_at": expires_at,
            "permanent_token_hash": perm_hash,
            "created_at": int(time.time())
        }
        
        return session_token, expires_at
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate session token, return user_id or None."""
        session_hash = self._hash(session_token)
        session = self.sessions.get(session_hash)
        
        if not session:
            return None
        
        if session["expires_at"] < time.time():
            del self.sessions[session_hash]
            return None
        
        return session["user_id"]
    
    def refresh_session(self, old_token: str, duration_hours: int = 24) -> tuple:
        """Refresh session - invalidate old, create new. Returns (new_token, expires_at)."""
        session_hash = self._hash(old_token)
        session = self.sessions.get(session_hash)
        
        if not session or session["expires_at"] < time.time():
            return None, None
        
        # Create new session
        new_token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + (duration_hours * 3600)
        
        new_hash = self._hash(new_token)
        self.sessions[new_hash] = {
            "user_id": session["user_id"],
            "expires_at": expires_at,
            "permanent_token_hash": session["permanent_token_hash"],
            "created_at": int(time.time())
        }
        
        # Invalidate old
        del self.sessions[session_hash]
        
        return new_token, expires_at
    
    def revoke_session(self, session_token: str) -> bool:
        """Revoke a session."""
        session_hash = self._hash(session_token)
        if session_hash in self.sessions:
            del self.sessions[session_hash]
            return True
        return False
    
    def get_session_info(self, session_token: str) -> Optional[dict]:
        """Get session info."""
        session_hash = self._hash(session_token)
        session = self.sessions.get(session_hash)
        if not session:
            return None
        return {
            "user_id": session["user_id"],
            "expires_at": session["expires_at"],
            "created_at": session["created_at"],
            "ttl_seconds": max(0, session["expires_at"] - int(time.time()))
        }


# Global session manager
_session_manager = None

def get_session_manager() -> SessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


# ============================================================================
# DEPENDENCIES
# ============================================================================

def get_session_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[str]:
    """Extract session token from request."""
    # Bearer token
    if credentials:
        return credentials.credentials
    
    # Header
    if token := request.headers.get("X-Session-Token"):
        return token
    
    # Cookie
    if token := request.cookies.get("semptify_session"):
        return token
    
    # Query param
    if token := request.query_params.get("session_token"):
        return token
    
    return None


async def require_session(
    session_token: str = Depends(get_session_token)
) -> str:
    """Dependency that requires valid session. Returns user_id."""
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")
    
    user_id = get_session_manager().validate_session(session_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return user_id


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/register")
async def register_user(req: RegisterRequest):
    """Register new user - returns permanent token (save securely!)."""
    import uuid
    
    user_id = f"{req.role}_{req.storage}_{uuid.uuid4().hex[:8]}"
    permanent_token = secrets.token_urlsafe(32)
    
    get_session_manager().register_permanent_token(user_id, permanent_token)
    
    return {
        "user_id": user_id,
        "permanent_token": permanent_token,
        "message": "SAVE THIS TOKEN SECURELY - it will not be shown again!"
    }


@router.post("/create")
async def create_session(req: CreateSessionRequest, response: Response):
    """Create session from permanent token."""
    mgr = get_session_manager()
    session_token, expires_at = mgr.create_session(req.permanent_token, req.duration_hours)
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Invalid permanent token")
    
    user_id = mgr.validate_session(session_token)
    
    # Set cookie
    response.set_cookie(
        key="semptify_session",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(expires_at - time.time())
    )
    
    return {
        "session_token": session_token,
        "expires_at": expires_at,
        "user_id": user_id,
        "message": "Session created"
    }


@router.get("/validate")
async def validate_session(session_token: str = Depends(get_session_token)):
    """Validate current session."""
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")
    
    user_id = get_session_manager().validate_session(session_token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return {"valid": True, "user_id": user_id}


@router.post("/refresh")
async def refresh_session(
    req: RefreshRequest,
    response: Response,
    session_token: str = Depends(get_session_token)
):
    """Refresh session - get new token."""
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")
    
    mgr = get_session_manager()
    new_token, expires_at = mgr.refresh_session(session_token, req.duration_hours)
    
    if not new_token:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    user_id = mgr.validate_session(new_token)
    
    response.set_cookie(
        key="semptify_session",
        value=new_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(expires_at - time.time())
    )
    
    return {
        "session_token": new_token,
        "expires_at": expires_at,
        "user_id": user_id,
        "message": "Session refreshed"
    }


@router.post("/logout")
async def logout(response: Response, session_token: str = Depends(get_session_token)):
    """Logout - revoke session."""
    if session_token:
        get_session_manager().revoke_session(session_token)
    
    response.delete_cookie("semptify_session")
    return {"message": "Logged out"}


@router.get("/info")
async def session_info(session_token: str = Depends(get_session_token)):
    """Get session info."""
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")
    
    info = get_session_manager().get_session_info(session_token)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return info


@router.get("/me")
async def get_me(user_id: str = Depends(require_session)):
    """Get current user (requires session)."""
    return {"user_id": user_id, "authenticated": True}
