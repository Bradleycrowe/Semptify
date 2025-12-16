"""
Journey FastAPI Router - User journey tracking and automation
Converted from Flask blueprint: journey_routes.py
"""
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

from curiosity_hooks import on_journey_step_completed
from journey_automation import get_user_stage, get_next_milestone, get_stage_progress, check_and_advance

router = APIRouter(prefix="/journey", tags=["journey"])
templates = Jinja2Templates(directory="templates")


class CheckProgressRequest(BaseModel):
    user_token: str
    action_type: str


@router.get("/", response_class=HTMLResponse)
async def journey_home(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Display user's journey progress
    
    5-stage progression:
    - Newcomer: Getting started
    - Documenting: Uploading evidence
    - Learning: Understanding rights
    - Organizing: Building case
    - Ready: Prepared for action
    """
    if not user_token:
        return templates.TemplateResponse("housing_journey.html", {"request": request})
    
    # Get user's journey data
    stage = get_user_stage(user_token) or 'newcomer'
    progress = get_stage_progress(user_token)
    milestone = get_next_milestone(user_token)
    
    stages = [
        {'name': 'Newcomer', 'value': 'newcomer', 'icon': 'fa-user-plus', 'color': 'secondary'},
        {'name': 'Documenting', 'value': 'documenting', 'icon': 'fa-upload', 'color': 'primary'},
        {'name': 'Learning', 'value': 'learning', 'icon': 'fa-graduation-cap', 'color': 'info'},
        {'name': 'Organizing', 'value': 'organizing', 'icon': 'fa-sitemap', 'color': 'warning'},
        {'name': 'Ready', 'value': 'ready', 'icon': 'fa-check-circle', 'color': 'success'}
    ]
    
    return templates.TemplateResponse(
        "journey_progress.html",
        {
            "request": request,
            "current_stage": stage,
            "stages": stages,
            "progress": progress,
            "next_milestone": milestone,
            "user_token": user_token
        }
    )


@router.post("/api/check-progress")
async def api_check_progress(data: CheckProgressRequest):
    """
    API endpoint to check and advance journey progress
    
    Action types:
    - upload: Document upload
    - event: Calendar event
    - module_complete: Learning module completion
    """
    if not data.user_token or not data.action_type:
        raise HTTPException(status_code=400, detail="Missing user_token or action_type")
    
    # Check if user advanced
    result = check_and_advance(data.user_token, data.action_type)
    
    # Trigger curiosity hook
    try:
        if result.get('advanced'):
            question = on_journey_step_completed(
                data.user_token,
                result.get('new_stage', data.action_type),
                result
            )
            if question:
                print(f'[CURIOSITY] {question}')
    except Exception as e:
        print(f'[WARN] Curiosity hook failed: {e}')
    
    return result
