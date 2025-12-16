"""
Onboarding FastAPI Router - User onboarding flow with reasoning engine
Converted from Flask blueprint: onboarding_routes.py
"""
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import json

from user_database import get_user, log_user_interaction
from engines.reasoning_engine import get_reasoning_engine

router = APIRouter(tags=["onboarding"])
templates = Jinja2Templates(directory="templates")


class LocationData(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None


class OnboardingSubmitRequest(BaseModel):
    location: Optional[LocationData] = None
    issue_type: Optional[str] = None
    urgency: Optional[str] = None
    has_court_date: bool = False
    court_date: Optional[str] = None
    notes: Optional[str] = ""


@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding_start(request: Request):
    """
    Start onboarding flow - gather essential info
    
    Collects:
    - Location (city, state, zip)
    - Issue type (eviction, repair, harassment)
    - Urgency level (immediate, days, weeks)
    - Court date information
    """
    return templates.TemplateResponse("onboarding.html", {"request": request})


@router.post("/api/onboarding/submit")
async def onboarding_submit(
    data: OnboardingSubmitRequest,
    x_user_token: Optional[str] = Header(None)
):
    """
    Process onboarding data and initialize user profile
    
    Runs reasoning engine to analyze situation and generate
    personalized dashboard content.
    """
    user_token = x_user_token
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get user
    user = get_user(user_token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user['id']
    
    # Build context for reasoning engine
    location_str = f"{data.location.city}, {data.location.state}" if data.location else "general"
    context = {
        "location": location_str,
        "zip": data.location.zip if data.location else None,
        "issue_type": data.issue_type,
        "urgency": data.urgency,
        "has_court_date": data.has_court_date,
        "court_date": data.court_date,
        "user_stress_level": "high" if data.urgency == "immediate" else "medium",
        "severity": "high" if data.has_court_date else "medium"
    }
    
    # Log the onboarding interaction
    log_user_interaction(
        user_id=user_id,
        action="onboarding_complete",
        details=json.dumps(context)
    )
    
    # Run reasoning engine to generate initial content
    reasoning = get_reasoning_engine()
    analysis = reasoning.analyze_situation(user_id, context)
    
    # Store context in session (if session middleware enabled)
    if hasattr(request, 'session'):
        request.session['user_context'] = context
        request.session['onboarding_complete'] = True
    
    return {
        "success": True,
        "message": "Onboarding complete",
        "analysis": analysis,
        "redirect": "/dashboard"
    }


@router.post("/api/onboarding/skip")
async def onboarding_skip(
    request: Request,
    x_user_token: Optional[str] = Header(None)
):
    """
    Skip onboarding - use default context
    
    Sets generic context for users who want to skip initial setup.
    """
    user_token = x_user_token
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = get_user(user_token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Set default context
    default_context = {
        "location": "general",
        "issue_type": "general",
        "urgency": "medium",
        "severity": "medium"
    }
    
    if hasattr(request, 'session'):
        request.session['user_context'] = default_context
        request.session['onboarding_complete'] = True
    
    return {
        "success": True,
        "redirect": "/dashboard"
    }
