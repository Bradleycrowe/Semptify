"""
Admin Control Panel FastAPI Router - System configuration management
Converted from Flask blueprint: admin_control_panel.py
"""
from fastapi import APIRouter, Request, HTTPException, Form, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime

from security import validate_admin_token, _get_or_create_csrf_token
from user_database import _get_db

router = APIRouter(prefix="/admin/panel", tags=["admin-panel"])
templates = Jinja2Templates(directory="templates")

CONFIG_FILE = 'data/admin_config.json'


# ============================================================================
# Pydantic Models
# ============================================================================

class ConfigUpdateRequest(BaseModel):
    email_enabled: Optional[bool] = None
    phone_enabled: Optional[bool] = None
    require_verification: Optional[bool] = None
    allow_registration: Optional[bool] = None
    require_email: Optional[bool] = None
    manual_approval_required: Optional[bool] = None
    allow_system_storage: Optional[bool] = None
    allow_user_storage: Optional[bool] = None
    default_backend: Optional[str] = None
    security_mode: Optional[str] = None
    rate_limiting_enabled: Optional[bool] = None
    csrf_enabled: Optional[bool] = None
    force_https: Optional[bool] = None
    vault_enabled: Optional[bool] = None
    complaint_filing_enabled: Optional[bool] = None
    timeline_enabled: Optional[bool] = None
    ai_assistance_enabled: Optional[bool] = None
    learning_engine_enabled: Optional[bool] = None


class UserCreateRequest(BaseModel):
    email: str
    password: str
    verified: Optional[bool] = False
    storage_qualified: Optional[bool] = False


class SuccessResponse(BaseModel):
    success: bool
    message: Optional[str] = None


# ============================================================================
# Helper Functions
# ============================================================================

def _load_config():
    """Load admin configuration"""
    os.makedirs('data', exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    return {
        'user_verification': {
            'email_enabled': True,
            'phone_enabled': False,
            'sms_enabled': False,
            'require_verification': True
        },
        'registration': {
            'allow_registration': True,
            'require_email': False,
            'require_phone': False,
            'manual_approval_required': False
        },
        'storage': {
            'allow_system_storage': True,
            'allow_user_storage': True,
            'require_storage_qualification': False,
            'default_backend': 'local'
        },
        'security': {
            'security_mode': 'open',
            'rate_limiting_enabled': True,
            'csrf_enabled': True,
            'force_https': False
        },
        'features': {
            'vault_enabled': True,
            'complaint_filing_enabled': True,
            'timeline_enabled': True,
            'ai_assistance_enabled': True,
            'learning_engine_enabled': True
        }
    }


def _save_config(config):
    """Save admin configuration"""
    os.makedirs('data', exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


# ============================================================================
# Routes
# ============================================================================

@router.get("", response_class=HTMLResponse)
async def index(
    request: Request,
    admin_token: Optional[str] = None,
    x_admin_token: Optional[str] = Header(None)
):
    """Main admin control panel"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Admin token required")
    
    config = _load_config()
    csrf_token = _get_or_create_csrf_token()
    
    return templates.TemplateResponse(
        "admin_control_panel.html",
        {
            "request": request,
            "config": config,
            "csrf_token": csrf_token,
            "admin_token": token
        }
    )


@router.post("/update", response_model=SuccessResponse)
async def update_config(
    data: ConfigUpdateRequest,
    admin_token: Optional[str] = Form(None),
    x_admin_token: Optional[str] = Header(None)
):
    """Update configuration"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    config = _load_config()
    
    # Update user verification
    if data.email_enabled is not None:
        config['user_verification']['email_enabled'] = data.email_enabled
    if data.phone_enabled is not None:
        config['user_verification']['phone_enabled'] = data.phone_enabled
    if data.require_verification is not None:
        config['user_verification']['require_verification'] = data.require_verification
    
    # Update registration
    if data.allow_registration is not None:
        config['registration']['allow_registration'] = data.allow_registration
    if data.require_email is not None:
        config['registration']['require_email'] = data.require_email
    if data.manual_approval_required is not None:
        config['registration']['manual_approval_required'] = data.manual_approval_required
    
    # Update storage
    if data.allow_system_storage is not None:
        config['storage']['allow_system_storage'] = data.allow_system_storage
    if data.allow_user_storage is not None:
        config['storage']['allow_user_storage'] = data.allow_user_storage
    if data.default_backend is not None:
        config['storage']['default_backend'] = data.default_backend
    
    # Update security
    if data.security_mode is not None:
        config['security']['security_mode'] = data.security_mode
    if data.rate_limiting_enabled is not None:
        config['security']['rate_limiting_enabled'] = data.rate_limiting_enabled
    if data.csrf_enabled is not None:
        config['security']['csrf_enabled'] = data.csrf_enabled
    if data.force_https is not None:
        config['security']['force_https'] = data.force_https
    
    # Update features
    if data.vault_enabled is not None:
        config['features']['vault_enabled'] = data.vault_enabled
    if data.complaint_filing_enabled is not None:
        config['features']['complaint_filing_enabled'] = data.complaint_filing_enabled
    if data.timeline_enabled is not None:
        config['features']['timeline_enabled'] = data.timeline_enabled
    if data.ai_assistance_enabled is not None:
        config['features']['ai_assistance_enabled'] = data.ai_assistance_enabled
    if data.learning_engine_enabled is not None:
        config['features']['learning_engine_enabled'] = data.learning_engine_enabled
    
    _save_config(config)
    
    return SuccessResponse(success=True, message="Configuration updated")


@router.get("/users")
async def list_users(
    admin_token: Optional[str] = None,
    x_admin_token: Optional[str] = Header(None)
):
    """List all users"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, created_at FROM users")
    users = [
        {"id": row[0], "email": row[1], "created_at": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    
    return {"users": users}


@router.post("/users/{user_id}/verify", response_model=SuccessResponse)
async def verify_user(
    user_id: int,
    admin_token: Optional[str] = Form(None),
    x_admin_token: Optional[str] = Header(None)
):
    """Mark user as verified"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET verified = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return SuccessResponse(success=True, message="User verified")


@router.post("/users/{user_id}/storage", response_model=SuccessResponse)
async def qualify_user_storage(
    user_id: int,
    admin_token: Optional[str] = Form(None),
    x_admin_token: Optional[str] = Header(None)
):
    """Qualify user for storage"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET storage_qualified = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return SuccessResponse(success=True, message="User storage qualified")


@router.post("/users/create", response_model=SuccessResponse)
async def create_user(
    data: UserCreateRequest,
    admin_token: Optional[str] = Form(None),
    x_admin_token: Optional[str] = Header(None)
):
    """Create new user (admin only)"""
    token = admin_token or x_admin_token
    if not validate_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    import hashlib
    password_hash = hashlib.sha256(data.password.encode()).hexdigest()
    
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, password_hash, verified, storage_qualified, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.email, password_hash, data.verified, data.storage_qualified, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    
    return SuccessResponse(success=True, message="User created")
