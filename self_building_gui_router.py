"""
mc² Dashboard - Self-Learning Dashboard - AI-driven adaptive interface
Uses: learning_engine, context analysis, curiosity_hooks, journey_automation
Principle: GUI evolves with user, no two dashboards look the same over time
"""
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import json
from pathlib import Path

# Semptify modules
from role_guards import get_user_role, ROLE_HIERARCHY
from security import validate_user_token

router = APIRouter(tags=["mc2"])
templates = Jinja2Templates(directory="templates")

# Seed templates - starting points for new users
SEED_TEMPLATES = {
    "newcomer": {
        "stage": "Getting Started",
        "widgets": [
            {"id": "vault", "title": "My Vault", "icon": "🔐", "priority": 1, "hint": "Start by uploading documents"},
            {"id": "help", "title": "Help & Resources", "icon": "❓", "priority": 2, "hint": "Learn how to use Semptify"},
            {"id": "calendar", "title": "Calendar", "icon": "📅", "priority": 3, "hint": "Track important dates"}
        ],
        "layout": "simple",
        "show_tutorial": True
    },
    "documenting": {
        "stage": "Building Your Case",
        "widgets": [
            {"id": "vault", "title": "Document Vault", "icon": "🔐", "priority": 1, "badge": "Active"},
            {"id": "timeline", "title": "Timeline", "icon": "📅", "priority": 2, "hint": "Record events"},
            {"id": "ledger", "title": "Rent Ledger", "icon": "🧾", "priority": 3, "hint": "Track payments"},
            {"id": "case_strength", "title": "Case Strength", "icon": "📊", "priority": 4, "auto_added": True}
        ],
        "layout": "evidence-focused"
    },
    "learning": {
        "stage": "Understanding Your Rights",
        "widgets": [
            {"id": "vault", "title": "My Vault", "icon": "🔐", "priority": 3},
            {"id": "library", "title": "Legal Library", "icon": "📚", "priority": 1, "badge": "Recommended"},
            {"id": "research", "title": "Research Tools", "icon": "🔍", "priority": 2},
            {"id": "timeline", "title": "Timeline", "icon": "📅", "priority": 4}
        ],
        "layout": "learning-mode"
    },
    "organizing": {
        "stage": "Preparing to File",
        "widgets": [
            {"id": "vault", "title": "Document Vault", "icon": "🔐", "priority": 2, "status": "Complete"},
            {"id": "complaint_preview", "title": "Complaint Preview", "icon": "👁️", "priority": 1, "auto_added": True},
            {"id": "court_forms", "title": "Court Forms", "icon": "📄", "priority": 3},
            {"id": "timeline", "title": "Timeline", "icon": "📅", "priority": 4},
            {"id": "case_strength", "title": "Case Strength: 78%", "icon": "📊", "priority": 5}
        ],
        "layout": "action-ready"
    },
    "ready": {
        "stage": "Ready to File",
        "widgets": [
            {"id": "complaint_filing", "title": "FILE COMPLAINT", "icon": "🎯", "priority": 1, "highlighted": True},
            {"id": "case_review", "title": "Review Your Case", "icon": "✅", "priority": 2},
            {"id": "court_forms", "title": "Court Forms", "icon": "📄", "priority": 3},
            {"id": "vault", "title": "Evidence Vault", "icon": "🔐", "priority": 4, "status": "92% Complete"}
        ],
        "layout": "action-primary"
    }
}

# Widget catalog - all available components
WIDGET_CATALOG = {
    "vault": {"route": "/vault", "desc": "Secure document storage", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "ledger": {"route": "/ledger", "desc": "Rent payment tracking", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "timeline": {"route": "/timeline", "desc": "Event timeline", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "calendar": {"route": "/calendar", "desc": "Calendar & deadlines", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "complaint_filing": {"route": "/complaint", "desc": "File complaint wizard", "roles": ["user", "attorney", "advocate"]},
    "journey": {"route": "/journey", "desc": "Progress tracker", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "help": {"route": "/help", "desc": "Help & crisis resources", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "library": {"route": "/library", "desc": "Legal forms library", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "research": {"route": "/research", "desc": "Landlord research", "roles": ["user", "attorney", "advocate", "manager", "admin"]},
    "court_forms": {"route": "/library/court-forms", "desc": "Court forms", "roles": ["attorney", "advocate", "manager", "admin"]},
    "case_strength": {"route": "/api/case-strength", "desc": "Case analysis", "roles": ["user", "attorney", "advocate"], "ai": True},
    "complaint_preview": {"route": "/api/complaint-preview", "desc": "Preview filing", "roles": ["user", "attorney", "advocate"], "ai": True},
    "case_review": {"route": "/api/case-review", "desc": "AI case review", "roles": ["user", "attorney", "advocate"], "ai": True}
}


def get_user_stage(user_token: str) -> str:
    """Determine user journey stage - integrates with journey_automation"""
    # Try to load from journey data
    try:
        from journey_automation import get_user_stage as journey_get_stage
        return journey_get_stage(user_token)
    except:
        pass
    
    # Fallback: check user activity patterns
    user_file = Path(f"data/users/{user_token[:8]}_activity.json")
    if user_file.exists():
        with open(user_file) as f:
            activity = json.load(f)
            # Simple heuristic
            if activity.get("total_actions", 0) < 5:
                return "newcomer"
            elif activity.get("vault_uploads", 0) > 5:
                return "documenting"
            elif activity.get("complaint_started"):
                return "ready"
    
    return "newcomer"


def learn_from_usage(user_token: str) -> Dict[str, Any]:
    """Get usage patterns from learning engine"""
    try:
        # Load learning data
        learning_file = Path(f"data/learning/user_{user_token[:8]}.json")
        if learning_file.exists():
            with open(learning_file) as f:
                return json.load(f)
    except:
        pass
    
    return {
        "most_used": [],
        "last_action": None,
        "action_count": 0,
        "patterns": []
    }


def build_adaptive_widgets(user_token: str, stage: str, learning_data: Dict) -> List[Dict]:
    """Build widget list dynamically based on user behavior"""
    
    # Start with seed template
    seed = SEED_TEMPLATES.get(stage, SEED_TEMPLATES["newcomer"])
    widgets = seed["widgets"].copy()
    
    # Adjust priorities based on usage
    if learning_data.get("most_used"):
        for widget in widgets:
            if widget["id"] in learning_data["most_used"]:
                widget["priority"] -= 1  # Move up
                widget["badge"] = "Frequently Used"
    
    # Add AI-suggested widgets
    suggestions = get_ai_suggestions(user_token, learning_data)
    for suggestion in suggestions:
        if suggestion["id"] not in [w["id"] for w in widgets]:
            widgets.append({
                **suggestion,
                "auto_added": True,
                "badge": "✨ Suggested"
            })
    
    # Sort by priority
    widgets.sort(key=lambda w: w.get("priority", 99))
    
    return widgets


def get_ai_suggestions(user_token: str, learning_data: Dict) -> List[Dict]:
    """AI-powered suggestions based on context"""
    suggestions = []
    
    # If user uploads docs but no timeline entries → suggest timeline
    if learning_data.get("vault_uploads", 0) > 3 and learning_data.get("timeline_entries", 0) == 0:
        suggestions.append({
            "id": "timeline",
            "title": "Timeline Assistant",
            "icon": "📅",
            "priority": 2,
            "hint": "Track when events happened - helps build your case"
        })
    
    # If strong document collection → suggest case strength
    if learning_data.get("vault_uploads", 0) > 8:
        suggestions.append({
            "id": "case_strength",
            "title": "Case Strength Meter",
            "icon": "📊",
            "priority": 3,
            "hint": "AI analysis of your evidence strength"
        })
    
    # If timeline complete → suggest complaint filing
    if learning_data.get("timeline_entries", 0) > 5 and learning_data.get("vault_uploads", 0) > 5:
        suggestions.append({
            "id": "complaint_filing",
            "title": "Ready to File?",
            "icon": "��",
            "priority": 1,
            "hint": "Your case looks strong - consider filing"
        })
    
    return suggestions


@router.get("/mc2", response_class=HTMLResponse)
async def live_dashboard(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Self-building dashboard - adapts in real-time
    Each user sees different widgets based on their journey
    """
    if not user_token:
        return templates.TemplateResponse("token_entry.html", {"request": request})
    
    if not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Get user role for overlays
    role = get_user_role(user_token)
    
    # Determine current stage
    stage = get_user_stage(user_token)
    
    # Learn from usage patterns
    learning_data = learn_from_usage(user_token)
    
    # Build adaptive widget list
    widgets = build_adaptive_widgets(user_token, stage, learning_data)
    
    # Get seed template info
    seed_info = SEED_TEMPLATES.get(stage, SEED_TEMPLATES["newcomer"])
    
    context = {
        "request": request,
        "user_token": user_token,
        "role": role,
        "stage": stage,
        "stage_title": seed_info["stage"],
        "widgets": widgets,
        "layout": seed_info["layout"],
        "show_tutorial": seed_info.get("show_tutorial", False),
        "action_count": learning_data.get("action_count", 0)
    }
    
    return templates.TemplateResponse("self_building_dashboard.html", context)


@router.post("/api/mc2/observe")
async def observe_action(
    user_token: str = Query(...),
    action: str = Query(...),
    widget_id: Optional[str] = Query(None)
):
    """
    Track user actions to learn and adapt GUI
    Called every time user interacts with dashboard
    """
    # Log action
    user_file = Path(f"data/users/{user_token[:8]}_activity.json")
    user_file.parent.mkdir(parents=True, exist_ok=True)
    
    activity = {}
    if user_file.exists():
        with open(user_file) as f:
            activity = json.load(f)
    
    # Update counters
    activity["total_actions"] = activity.get("total_actions", 0) + 1
    activity["last_action"] = action
    activity["last_widget"] = widget_id
    
    # Track widget usage
    if widget_id:
        usage = activity.get("widget_usage", {})
        usage[widget_id] = usage.get(widget_id, 0) + 1
        activity["widget_usage"] = usage
    
    # Save
    with open(user_file, 'w') as f:
        json.dump(activity, f, indent=2)
    
    # Trigger learning engine
    try:
        from engines.learning_engine import get_learning
        engine = get_learning()
        engine.observe_action(user_token, action, {"widget": widget_id})
    except:
        pass
    
    return {"status": "observed", "total_actions": activity["total_actions"]}


@router.get("/api/mc2/rebuild")
async def trigger_rebuild(user_token: str = Query(...)):
    """
    Force GUI rebuild - useful for testing
    Returns new widget configuration
    """
    stage = get_user_stage(user_token)
    learning_data = learn_from_usage(user_token)
    widgets = build_adaptive_widgets(user_token, stage, learning_data)
    
    return {
        "stage": stage,
        "widgets": widgets,
        "timestamp": "now"
    }


