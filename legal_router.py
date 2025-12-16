"""
Legal FastAPI Router - Privacy and terms pages
Converted from Flask blueprint: legal_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["legal"])
templates = Jinja2Templates(directory="templates")


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    """Privacy policy page"""
    return templates.TemplateResponse("legal/privacy.html", {"request": request})


@router.get("/terms", response_class=HTMLResponse)
async def terms_of_service(request: Request):
    """Terms of service page (placeholder)"""
    return templates.TemplateResponse("legal/privacy.html", {"request": request})
