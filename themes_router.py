"""
Themes FastAPI Router - Dashboard theme variants
Converted from Flask blueprint: themes_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from cards_model import get_all_cards

router = APIRouter(tags=["themes"])
templates = Jinja2Templates(directory="templates")


@router.get("/theme/legal", response_class=HTMLResponse)
async def theme_legal(request: Request):
    """
    Legal Document Portal theme
    
    Professional legal interface styling for document management.
    """
    cards = get_all_cards()
    user_name = request.session.get("user_name", "Dev User") if hasattr(request, 'session') else "Dev User"
    
    return templates.TemplateResponse(
        "dashboard_theme_legal.html",
        {"request": request, "cards": cards, "user_name": user_name}
    )


@router.get("/theme/helpdesk", response_class=HTMLResponse)
async def theme_helpdesk(request: Request):
    """
    Tenant Helpdesk theme
    
    Support-focused interface with iconography and accessible design.
    """
    cards = get_all_cards()
    
    # Add icons for helpdesk theme
    icon_map = {
        "Vault": "🔐",
        "Timeline": "📅",
        "Court": "⚖️",
        "Complaint": "📝",
        "Research": "📚",
        "Calendar": "🗓️"
    }
    for card in cards:
        for key, icon in icon_map.items():
            if key.lower() in card.get("title", "").lower():
                card["icon"] = icon
                break
    
    user_name = request.session.get("user_name", "Dev User") if hasattr(request, 'session') else "Dev User"
    
    return templates.TemplateResponse(
        "dashboard_theme_helpdesk.html",
        {"request": request, "cards": cards, "user_name": user_name}
    )


@router.get("/theme/action", response_class=HTMLResponse)
async def theme_action(request: Request):
    """
    Rights Action Dashboard theme
    
    Action-oriented interface emphasizing quick access to key features.
    """
    cards = get_all_cards()
    user_name = request.session.get("user_name", "Dev User") if hasattr(request, 'session') else "Dev User"
    
    return templates.TemplateResponse(
        "dashboard_theme_action.html",
        {"request": request, "cards": cards, "user_name": user_name}
    )
