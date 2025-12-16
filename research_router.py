"""
Research Tools FastAPI Router - Landlord, building, and property lookup
Converted from Flask blueprint: research_routes.py
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(prefix="/research", tags=["research"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def research_home(
    request: Request,
    user_token: Optional[str] = Query("")
):
    """
    Research tools landing page
    
    Provides tools for:
    - Landlord background checks
    - Building inspection records
    - Property ownership lookup
    - Violation history
    """
    return templates.TemplateResponse(
        "research.html",
        {"request": request, "user_token": user_token}
    )
