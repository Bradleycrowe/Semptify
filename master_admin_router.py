"""
Master Admin FastAPI Router - System administration interface
Converted from Flask blueprint: master_admin_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["master-admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/master-admin", response_class=HTMLResponse)
async def admin_panel_master_admin(request: Request):
    """Master Admin Control Panel"""
    return templates.TemplateResponse("master_admin.html", {"request": request})


@router.get("/admin/master", response_class=HTMLResponse)
async def admin_panel_admin_master(request: Request):
    """Master Admin Control Panel (alternate URL)"""
    return templates.TemplateResponse("master_admin.html", {"request": request})


@router.get("/admin/session-cache", response_class=HTMLResponse)
async def admin_session_cache(request: Request):
    """Session cache toggle and configuration page"""
    return templates.TemplateResponse("admin_session_cache.html", {"request": request})
