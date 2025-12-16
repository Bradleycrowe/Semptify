"""
Help Hub FastAPI Router - Crisis resources and support services
Converted from Flask blueprint: help_hub_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["help"])
templates = Jinja2Templates(directory="templates")


@router.get("/help", response_class=HTMLResponse)
async def help_hub(request: Request):
    """
    Help hub page with emergency contacts and resources
    
    Provides access to:
    - Crisis hotlines
    - Legal aid contacts
    - Emergency shelter information
    - Support services directory
    """
    return templates.TemplateResponse("help_hub.html", {"request": request})
