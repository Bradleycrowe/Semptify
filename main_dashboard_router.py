"""
Main Dashboard FastAPI Router - Primary dashboard routes
Converted from Flask blueprint: main_dashboard_routes.py
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(tags=["main-dashboard"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index_redirect(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Root index - renders main dashboard
    
    Primary entry point showing:
    - Quick actions
    - Recent activity
    - Case summary
    - Notifications
    """
    return templates.TemplateResponse(
        "main_dashboard.html",
        {"request": request, "user_token": user_token}
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """Main dashboard page"""
    return templates.TemplateResponse(
        "main_dashboard.html",
        {"request": request, "user_token": user_token}
    )


@router.get("/ledger", response_class=HTMLResponse)
async def ledger_page(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Rent ledger page
    
    Displays:
    - Payment history
    - Balance tracking
    - Receipt uploads
    - Late fee calculations
    """
    return templates.TemplateResponse(
        "ledger.html",
        {"request": request, "user_token": user_token}
    )


@router.get("/housing_journey", response_class=HTMLResponse)
async def housing_journey(request: Request):
    """
    Housing journey visualization
    
    Shows user progress through 5-stage journey.
    """
    return templates.TemplateResponse("housing_journey.html", {"request": request})


@router.get("/pages/research", response_class=HTMLResponse)
async def research_page(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Research tools page
    
    Access to:
    - Landlord lookup
    - Building records
    - Property history
    """
    return templates.TemplateResponse(
        "research.html",
        {"request": request, "user_token": user_token}
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """User settings and preferences"""
    return templates.TemplateResponse(
        "settings.html",
        {"request": request, "user_token": user_token}
    )
