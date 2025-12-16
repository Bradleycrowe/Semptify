"""
Settings FastAPI Router - User preferences and configuration
Converted from Flask blueprint: settings_routes.py
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from security import validate_user_token

router = APIRouter(tags=["settings"])
templates = Jinja2Templates(directory="templates")


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    user_token: Optional[str] = None
):
    """
    User settings page
    
    Provides access to:
    - Storage backend selection
    - Theme preferences
    - Notification settings
    - Privacy controls
    """
    if user_token and not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")
    
    # Get current storage backend from session or default
    current_backend = request.session.get("storage_backend", "local") if hasattr(request, 'session') else "local"
    
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "user_token": user_token,
            "current_backend": current_backend
        }
    )


@router.post("/settings/change-storage")
async def change_storage_backend(
    request: Request,
    backend: str = Form(...),
    user_token: Optional[str] = Form(None)
):
    """
    Change storage backend
    
    Supported backends:
    - local: Local filesystem storage
    - r2: Cloudflare R2 cloud storage
    - oauth: OAuth-based cloud storage
    """
    if user_token and not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")
    
    # Validate backend choice
    valid_backends = ["local", "r2", "oauth"]
    if backend not in valid_backends:
        raise HTTPException(status_code=400, detail=f"Invalid backend. Must be one of: {', '.join(valid_backends)}")
    
    # Store in session
    if hasattr(request, 'session'):
        request.session["storage_backend"] = backend
    
    return RedirectResponse(url="/settings", status_code=303)
