"""
Calendar Vault UI FastAPI Router - Timeline assistant dashboard
Converted from Flask blueprint: calendar_vault_ui_routes.py
"""
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

from calendar_vault_bridge import CalendarVaultBridge

router = APIRouter(tags=["calendar-vault-ui"])
templates = Jinja2Templates(directory="templates")


# ============================================================================
# Pydantic Models
# ============================================================================

class SuggestionsResponse(BaseModel):
    suggestions: List[str]
    count: int


# ============================================================================
# Routes
# ============================================================================

@router.get("/timeline/assistant", response_class=HTMLResponse)
async def timeline_assistant(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Dashboard showing smart recommendations for completing timeline
    
    Displays:
    - High priority events needing documents
    - Normal priority recommendations
    - Document suggestions based on event type
    
    Uses /system/context for intelligent recommendations.
    """
    if not user_token:
        raise HTTPException(status_code=401, detail="User token required")
    
    bridge = CalendarVaultBridge()
    
    # Get events needing documents
    needs_docs = bridge.get_events_needing_documents(user_token)
    
    # Separate by urgency
    high_priority = [e for e in needs_docs if e['urgency'] == 'high']
    normal_priority = [e for e in needs_docs if e['urgency'] != 'high']
    
    return templates.TemplateResponse(
        "calendar_vault/assistant_dashboard.html",
        {
            "request": request,
            "high_priority": high_priority,
            "normal_priority": normal_priority,
            "user_token": user_token
        }
    )


@router.get("/api/timeline/suggestions", response_model=SuggestionsResponse)
async def api_suggestions(
    user_token: Optional[str] = Query(None),
    event_type: str = Query("general"),
    event_id: str = Query("temp")
):
    """
    API endpoint for getting document suggestions
    
    Returns intelligent document recommendations based on:
    - Event type (eviction, repair, lease_violation, etc.)
    - Existing documents in vault
    - Legal requirements
    
    Uses /system/context for context-aware suggestions.
    """
    if not user_token:
        raise HTTPException(status_code=401, detail="user_token required")
    
    bridge = CalendarVaultBridge()
    event_data = {'event_id': event_id}
    suggestions = bridge.suggest_documents_for_event(event_type, event_data)
    
    return SuggestionsResponse(
        suggestions=suggestions,
        count=len(suggestions)
    )
