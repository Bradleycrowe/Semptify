"""
GUI Hub FastAPI Router - Graphical interface hub and launcher
Converted from Flask blueprint: gui_hub_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["gui-hub"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/hub", response_class=HTMLResponse)
async def hub_main(request: Request):
    """GUI Hub - Launcher page"""
    return templates.TemplateResponse("gui_hub.html", {"request": request})


@router.get("/gui-hub", response_class=HTMLResponse)
async def hub_gui(request: Request):
    """GUI Hub - Launcher page (alternate URL)"""
    return templates.TemplateResponse("gui_hub.html", {"request": request})


@router.get("/choose-gui", response_class=HTMLResponse)
async def hub_choose(request: Request):
    """GUI Hub - Launcher page (alternate URL)"""
    return templates.TemplateResponse("gui_hub.html", {"request": request})


@router.get("/quick-launch/{gui_name}")
async def quick_launch(gui_name: str):
    """
    Quick launch specific GUI
    
    Supported GUIs:
    - learning: Dashboard
    - brad: Brad GUI
    - modern: Modern interface
    - main: Main dashboard
    - calendar: Calendar vault
    - complaint: Complaint filing
    - perspective: Perspective dashboard
    - vault: Document vault
    """
    routes = {
        "learning": "/dashboard",
        "brad": "/brad",
        "modern": "/modern",
        "main": "/main",
        "calendar": "/calendar-vault",
        "complaint": "/file-complaint",
        "perspective": "/dashboard/perspective",
        "vault": "/vault"
    }
    return RedirectResponse(url=routes.get(gui_name.lower(), "/hub"))
