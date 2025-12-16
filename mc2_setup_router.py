"""
mc² Setup Flow Router - OAuth-based authentication for everyone
Flow: Welcome → Role → Username → OAuth Login → Token Generated → Dashboard
"""
from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import hashlib
import json
from pathlib import Path
from datetime import datetime
import secrets

router = APIRouter(tags=["mc2-setup"])
templates = Jinja2Templates(directory="templates")

@router.get("/setup", response_class=HTMLResponse)
async def setup_start(request: Request):
    """Step 1: Welcome to mc²"""
    return templates.TemplateResponse("mc2_setup_welcome.html", {
        "request": request,
        "step": 1
    })

@router.get("/setup/role", response_class=HTMLResponse)
async def setup_role(request: Request):
    """Step 2: Select role"""
    return templates.TemplateResponse("mc2_setup_role.html", {
        "request": request,
        "step": 2,
        "roles": [
            {
                "id": "user",
                "title": "User (Tenant)",
                "desc": "I need help with my housing situation",
                "icon": "🏠",
                "features": ["Personal vault", "Rent ledger", "Timeline", "Complaint filing"]
            },
            {
                "id": "attorney",
                "title": "Attorney/Lawyer",
                "desc": "Legal professional helping clients",
                "icon": "⚖️",
                "features": ["Court forms", "Legal review", "Case strategy", "All user tools"]
            },
            {
                "id": "advocate",
                "title": "Advocate",
                "desc": "Supporting tenants and communities",
                "icon": "🤝",
                "features": ["Client management", "Resource referrals", "Journey guide", "All user tools"]
            },
            {
                "id": "manager",
                "title": "Manager",
                "desc": "Managing cases and team members",
                "icon": "👥",
                "features": ["Multi-user dashboard", "Analytics", "Case assignment", "Team oversight"]
            },
            {
                "id": "admin",
                "title": "Administrator",
                "desc": "System configuration and management",
                "icon": "⚙️",
                "features": ["System config", "User management", "Metrics", "AI assistant", "All tools"]
            }
        ]
    })

@router.post("/setup/role")
async def save_role(role: str = Form(...)):
    """Save role selection and move to username"""
    return RedirectResponse(url=f"/setup/username?role={role}", status_code=303)

@router.get("/setup/username", response_class=HTMLResponse)
async def setup_username(request: Request, role: str):
    """Step 3: Enter username before OAuth"""
    return templates.TemplateResponse("mc2_setup_username.html", {
        "request": request,
        "step": 3,
        "role": role
    })

@router.post("/setup/oauth")
async def initiate_oauth(
    username: str = Form(...),
    role: str = Form(...)
):
    """
    Step 4: Store pending user data and redirect to OAuth provider
    Token will be generated AFTER successful OAuth
    """
    # Store pending user data in session/temp storage
    pending_id = secrets.token_urlsafe(8)
    pending_file = Path(f"data/pending_users/{pending_id}.json")
    pending_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(pending_file, 'w') as f:
        json.dump({
            "username": username,
            "role": role,
            "storage_backend": "oauth",  # Everyone uses OAuth
            "created_at": datetime.now().isoformat(),
            "pending_id": pending_id
        }, f, indent=2)
    
    # Redirect to OAuth provider (Google, Microsoft, GitHub, etc.)
    oauth_provider = "google"  # or make it selectable
    return RedirectResponse(
        url=f"/oauth/login/{oauth_provider}?state={pending_id}",
        status_code=303
    )

@router.get("/oauth/callback")
async def oauth_callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...)  # pending_id
):
    """
    Step 5: OAuth callback - exchange code for access token
    Then generate Semptify token and complete setup
    """
    # Load pending user data
    pending_file = Path(f"data/pending_users/{state}.json")
    if not pending_file.exists():
        raise HTTPException(status_code=400, detail="Invalid or expired setup session")
    
    with open(pending_file) as f:
        pending_data = json.load(f)
    
    # TODO: Exchange OAuth code for access token
    # This would call the OAuth provider's token endpoint
    # For now, we'll simulate success
    oauth_access_token = f"oauth_token_{secrets.token_urlsafe(32)}"
    
    # Generate Semptify user token
    user_token = secrets.token_urlsafe(16)
    token_hash = hashlib.sha256(user_token.encode()).hexdigest()
    
    # Save user to security/users.json
    users_file = Path("security/users.json")
    users_file.parent.mkdir(parents=True, exist_ok=True)
    
    users = {}
    if users_file.exists():
        with open(users_file) as f:
            users = json.load(f)
    
    # Add new user
    user_id = f"user_{len(users) + 1}"
    users[user_id] = {
        "hash": token_hash,
        "username": pending_data["username"],
        "role": pending_data["role"],
        "storage_backend": "oauth",
        "oauth_provider": "google",  # or from request
        "oauth_token_hash": hashlib.sha256(oauth_access_token.encode()).hexdigest(),
        "created_at": datetime.now().isoformat(),
        "setup_complete": True
    }
    
    # Save
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    # Create user activity tracking
    user_data_dir = Path(f"data/users/{user_token[:8]}_activity.json")
    user_data_dir.parent.mkdir(parents=True, exist_ok=True)
    
    with open(user_data_dir, 'w') as f:
        json.dump({
            "user_id": user_id,
            "username": pending_data["username"],
            "role": pending_data["role"],
            "storage": "oauth",
            "total_actions": 0,
            "vault_uploads": 0,
            "timeline_entries": 0,
            "created_at": datetime.now().isoformat()
        }, f, indent=2)
    
    # Clean up pending data
    pending_file.unlink()
    
    # Show completion page with token
    return templates.TemplateResponse("mc2_setup_complete.html", {
        "request": request,
        "step": 4,
        "username": pending_data["username"],
        "role": pending_data["role"],
        "token": user_token,
        "dashboard_url": f"/mc2?user_token={user_token}"
    })
