"""
Profile FastAPI Router - Client/case profile management
Converted from Flask blueprint: profile_routes.py
"""
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from profile_manager import (
    get_all_profiles, get_active_profile, set_active_profile,
    create_profile, update_profile, delete_profile, init_profiles
)
from r2_profile_storage import sync_profiles_to_r2

router = APIRouter(prefix="/profiles", tags=["profiles"])
templates = Jinja2Templates(directory="templates")


# ============================================================================
# Pydantic Models
# ============================================================================

class CreateProfileRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    color: Optional[str] = "#4A90E2"


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class ProfileResponse(BaseModel):
    success: bool
    profile_id: Optional[str] = None
    error: Optional[str] = None


class ProfileListResponse(BaseModel):
    profiles: List[Dict[str, Any]]


# ============================================================================
# Routes
# ============================================================================

@router.get("", response_class=HTMLResponse)
async def list_profiles(request: Request):
    """Show all profiles with active indicator"""
    profiles = get_all_profiles()
    active = get_active_profile()
    return templates.TemplateResponse(
        "profiles.html",
        {"request": request, "profiles": profiles, "active_profile": active}
    )


@router.post("/switch/{profile_id}", response_model=ProfileResponse)
async def switch_profile(profile_id: str):
    """Switch to different profile"""
    if set_active_profile(profile_id):
        sync_profiles_to_r2()
        return ProfileResponse(success=True, profile_id=profile_id)
    raise HTTPException(status_code=404, detail="Profile not found")


@router.post("/create", response_model=ProfileResponse)
async def create_new_profile(
    name: str = Form(...),
    description: str = Form(""),
    color: str = Form("#4A90E2")
):
    """Create new client/case profile"""
    name = name.strip()
    
    if not name:
        raise HTTPException(status_code=400, detail="Name required")
    
    profile_id = create_profile(
        name=name,
        description=description,
        color=color
    )
    sync_profiles_to_r2()
    
    return ProfileResponse(success=True, profile_id=profile_id)


@router.post("/create/json", response_model=ProfileResponse)
async def create_new_profile_json(data: CreateProfileRequest):
    """Create new client/case profile (JSON endpoint)"""
    name = data.name.strip()
    
    if not name:
        raise HTTPException(status_code=400, detail="Name required")
    
    profile_id = create_profile(
        name=name,
        description=data.description,
        color=data.color
    )
    sync_profiles_to_r2()
    
    return ProfileResponse(success=True, profile_id=profile_id)


@router.post("/update/{profile_id}", response_model=ProfileResponse)
async def update_profile_route(profile_id: str, data: UpdateProfileRequest):
    """Update profile metadata"""
    kwargs = {}
    if data.name is not None:
        kwargs['name'] = data.name
    if data.description is not None:
        kwargs['description'] = data.description
    if data.color is not None:
        kwargs['color'] = data.color
    
    if update_profile(profile_id, **kwargs):
        sync_profiles_to_r2()
        return ProfileResponse(success=True)
    
    raise HTTPException(status_code=404, detail="Profile not found")


@router.post("/delete/{profile_id}", response_model=ProfileResponse)
async def delete_profile_route(profile_id: str):
    """Delete a profile"""
    if delete_profile(profile_id):
        sync_profiles_to_r2()
        return ProfileResponse(success=True)
    
    raise HTTPException(status_code=400, detail="Cannot delete default profile")


@router.get("/api/active")
async def get_active():
    """API endpoint for current profile"""
    return get_active_profile()


@router.get("/api/all", response_model=ProfileListResponse)
async def get_all():
    """API endpoint for all profiles"""
    return ProfileListResponse(profiles=get_all_profiles())


# Initialize profiles on import
init_profiles()
