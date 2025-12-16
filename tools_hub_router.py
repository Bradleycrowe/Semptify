"""
Tools Hub FastAPI Router - AI, utilities, and power features
Converted from Flask blueprint: tools_hub_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["tools"])
templates = Jinja2Templates(directory="templates")


@router.get("/tools", response_class=HTMLResponse)
async def tools_hub(request: Request):
    """
    Tools hub page with AI and utilities
    
    Provides access to:
    - AI assistance tools
    - Document processing utilities
    - Automation features
    - System utilities
    """
    return templates.TemplateResponse("tools_hub.html", {"request": request})
