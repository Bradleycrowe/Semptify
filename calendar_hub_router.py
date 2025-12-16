"""
Calendar Hub FastAPI Router - Unified calendar and timeline page
Converted from Flask blueprint: calendar_hub_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["calendar"])
templates = Jinja2Templates(directory="templates")


@router.get("/calendar", response_class=HTMLResponse)
async def calendar_hub(request: Request):
    """
    Main calendar hub with timeline and vault features
    
    Unified interface for:
    - Evidence timeline visualization
    - Deadline tracking
    - Document vault integration
    - Calendar event management
    """
    return templates.TemplateResponse("calendar_hub.html", {"request": request})
