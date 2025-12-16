"""
OAuth Router - FastAPI
OAuth2 authentication flows
"""
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os
import secrets
import httpx

from routers.session import get_session_manager

router = APIRouter()

# OAuth config from env
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
OAUTH_REDIRECT_URI = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:8000/api/oauth/callback")

# State storage (in production use Redis)
_oauth_states: dict = {}


class TokenExchangeRequest(BaseModel):
    code: str
    provider: str
    redirect_uri: Optional[str] = None


@router.get("/providers")
async def list_providers():
    """List available OAuth providers."""
    return {
        "providers": [
            {"name": "google", "enabled": bool(GOOGLE_CLIENT_ID)},
            {"name": "github", "enabled": bool(GITHUB_CLIENT_ID)},
        ]
    }


@router.get("/login/{provider}")
async def oauth_login(provider: str, request: Request):
    """Start OAuth flow - redirect to provider."""
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = {"provider": provider}
    
    if provider == "google":
        if not GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=400, detail="Google OAuth not configured")
        
        url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={OAUTH_REDIRECT_URI}"
            "&response_type=code"
            "&scope=openid%20email%20profile"
            f"&state={state}"
        )
        return RedirectResponse(url)
    
    elif provider == "github":
        if not GITHUB_CLIENT_ID:
            raise HTTPException(status_code=400, detail="GitHub OAuth not configured")
        
        url = (
            "https://github.com/login/oauth/authorize?"
            f"client_id={GITHUB_CLIENT_ID}"
            f"&redirect_uri={OAUTH_REDIRECT_URI}"
            "&scope=user:email"
            f"&state={state}"
        )
        return RedirectResponse(url)
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")


@router.get("/callback")
async def oauth_callback(code: str, state: str, response: Response):
    """OAuth callback - exchange code for tokens."""
    if state not in _oauth_states:
        raise HTTPException(status_code=400, detail="Invalid state")
    
    state_data = _oauth_states.pop(state)
    provider = state_data["provider"]
    
    try:
        if provider == "google":
            user_info = await _exchange_google_code(code)
        elif provider == "github":
            user_info = await _exchange_github_code(code)
        else:
            raise HTTPException(status_code=400, detail="Unknown provider")
        
        # Create or get user
        user_id = f"{provider}_{user_info.get('id', user_info.get('email', 'unknown'))}"
        
        # Generate permanent token for this user
        permanent_token = secrets.token_urlsafe(32)
        mgr = get_session_manager()
        mgr.register_permanent_token(user_id, permanent_token)
        
        # Create session
        session_token, expires_at = mgr.create_session(permanent_token)
        
        # Set cookie
        response.set_cookie(
            key="semptify_session",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=86400
        )
        
        return {
            "status": "authenticated",
            "provider": provider,
            "user_id": user_id,
            "session_token": session_token,
            "expires_at": expires_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _exchange_google_code(code: str) -> dict:
    """Exchange Google auth code for user info."""
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": OAUTH_REDIRECT_URI,
            }
        )
        tokens = token_resp.json()
        access_token = tokens.get("access_token")
        
        if not access_token:
            raise Exception("Failed to get access token")
        
        # Get user info
        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return user_resp.json()


async def _exchange_github_code(code: str) -> dict:
    """Exchange GitHub auth code for user info."""
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"}
        )
        tokens = token_resp.json()
        access_token = tokens.get("access_token")
        
        if not access_token:
            raise Exception("Failed to get access token")
        
        # Get user info
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return user_resp.json()
