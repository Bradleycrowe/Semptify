"""
Adaptive GUI Router - Self-building interface with role overlays
Base: Everyone is a User
Overlays: Legal, Advocate, Manager, Admin (hover bubbles)
Self-Building: Uses learning engine + context to generate UI
"""
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict
from pydantic import BaseModel

router = APIRouter(tags=["adaptive-gui"])
templates = Jinja2Templates(directory="templates")

# Role overlay definitions
ROLE_OVERLAYS = {
    "admin": {
        "icon": "⚙️",
        "color": "#e74c3c",
        "position": "top-right",
        "trigger": "hover",
        "features": [
            {"name": "System Config", "route": "/admin/config", "icon": "🔧"},
            {"name": "User Management", "route": "/admin/users", "icon": "👥"},
            {"name": "Metrics", "route": "/metrics", "icon": "📊"},
            {"name": "Coding Assistant", "route": "/admin/ai-assistant", "icon": "🤖", "ai": "claude-sonnet-4.5"},
            {"name": "Reference Manuals", "route": "/admin/docs", "icon": "📚"},
            {"name": "Token Management", "route": "/admin/tokens", "icon": "🔑"}
        ]
    },
    "manager": {
        "icon": "📊",
        "color": "#3498db",
        "position": "top-left",
        "trigger": "click",
        "features": [
            {"name": "All Users", "route": "/manager/users", "icon": "👥"},
            {"name": "Case Overview", "route": "/manager/cases", "icon": "📋"},
            {"name": "Analytics", "route": "/manager/analytics", "icon": "📈"},
            {"name": "Team Activity", "route": "/manager/activity", "icon": "🔔"}
        ]
    },
    "legal": {
        "icon": "⚖️",
        "color": "#9b59b6",
        "position": "bottom-right",
        "trigger": "click",
        "features": [
            {"name": "Court Forms", "route": "/library/court-forms", "icon": "📄"},
            {"name": "Case Law", "route": "/legal/caselaw", "icon": "📚"},
            {"name": "Legal Review", "route": "/legal/review", "icon": "⚖️"},
            {"name": "Attestation", "route": "/attestation", "icon": "✍️"}
        ]
    },
    "advocate": {
        "icon": "🤝",
        "color": "#27ae60",
        "position": "bottom-left",
        "trigger": "click",
        "features": [
            {"name": "My Clients", "route": "/clients", "icon": "👥"},
            {"name": "Help Upload", "route": "/assist/upload", "icon": "📤"},
            {"name": "Journey Guide", "route": "/guide", "icon": "🧭"},
            {"name": "Resources", "route": "/resources", "icon": "📦"}
        ]
    }
}

@router.get("/adaptive-dashboard", response_class=HTMLResponse)
async def adaptive_dashboard(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Adaptive dashboard - Everyone sees base user features
    Additional roles add overlay bubbles
    """
    if not user_token:
        return templates.TemplateResponse("token_entry.html", {"request": request})
    
    # Determine user roles (can have multiple)
    roles = get_user_roles(user_token)  # Returns list: ['user', 'admin', 'legal']
    
    # Get active overlays
    overlays = {role: ROLE_OVERLAYS[role] for role in roles if role in ROLE_OVERLAYS}
    
    return templates.TemplateResponse("adaptive_dashboard.html", {
        "request": request,
        "user_token": user_token,
        "roles": roles,
        "overlays": overlays
    })


@router.post("/api/gui/generate")
async def generate_ui_component(data: Dict):
    """
    Self-building GUI endpoint
    Generates UI components based on context + learning patterns
    """
    context = data.get("context", {})
    user_action = data.get("action", "")
    history = data.get("history", [])
    
    # Use learning engine to determine what UI to show
    suggested_component = await analyze_and_suggest_ui(context, user_action, history)
    
    return {
        "component_type": suggested_component["type"],
        "html": suggested_component["html"],
        "position": suggested_component["position"],
        "priority": suggested_component["priority"]
    }


def get_user_roles(user_token: str) -> List[str]:
    """
    Get all roles for a user (can have multiple)
    Base role is always 'user'
    """
    # TODO: Query from database
    # For now, detect from token
    roles = ["user"]  # Everyone starts as user
    
    # Check for additional roles
    if validate_admin_token(user_token):
        roles.append("admin")
    
    # Check user metadata for legal/advocate/manager flags
    user_meta = get_user_metadata(user_token)
    if user_meta.get("is_legal_professional"):
        roles.append("legal")
    if user_meta.get("is_advocate"):
        roles.append("advocate")
    if user_meta.get("is_manager"):
        roles.append("manager")
    
    return roles


async def analyze_and_suggest_ui(context: Dict, action: str, history: List) -> Dict:
    """
    AI-powered UI generation
    Uses learning patterns + context to build interface elements
    """
    # Analyze user behavior patterns
    patterns = await get_learning_patterns(context.get("user_id"))
    
    # Determine contextual needs
    if "filing_complaint" in action:
        return {
            "type": "wizard",
            "html": generate_complaint_wizard(context),
            "position": "center",
            "priority": "high"
        }
    elif "need_help" in action:
        return {
            "type": "assistant_popup",
            "html": generate_ai_assistant_bubble(context),
            "position": "bottom-right",
            "priority": "medium"
        }
    elif "viewing_documents" in action and patterns.get("frequently_uploads"):
        return {
            "type": "quick_upload",
            "html": generate_quick_upload_button(),
            "position": "top-right",
            "priority": "low"
        }
    
    return {"type": "none", "html": "", "position": "", "priority": ""}


def generate_complaint_wizard(context: Dict) -> str:
    """Generate HTML for complaint filing wizard"""
    return """
    <div class="wizard-popup">
        <h3>File a Complaint</h3>
        <div class="steps">
            <button>1. Identify Issue</button>
            <button>2. Gather Evidence</button>
            <button>3. Submit</button>
        </div>
    </div>
    """


def generate_ai_assistant_bubble(context: Dict) -> str:
    """Generate Claude Sonnet 4.5 assistant bubble"""
    return """
    <div class="ai-bubble">
        <div class="ai-icon">🤖</div>
        <div class="ai-message">
            <p>Need help? I'm Claude, your AI assistant.</p>
            <input placeholder="Ask me anything..." />
        </div>
    </div>
    """


def generate_quick_upload_button() -> str:
    """Generate contextual quick upload button"""
    return """
    <button class="quick-upload" onclick="openUploadModal()">
        📤 Quick Upload
    </button>
    """


async def get_learning_patterns(user_id: str) -> Dict:
    """Get learned patterns from learning engine"""
    # TODO: Query learning_engine
    return {
        "frequently_uploads": True,
        "prefers_step_by_step": True,
        "needs_legal_help": False
    }


def get_user_metadata(user_token: str) -> Dict:
    """Get user metadata including role flags"""
    # TODO: Query from users.json or database
    return {
        "is_legal_professional": False,
        "is_advocate": False,
        "is_manager": False
    }


def validate_admin_token(token: str) -> bool:
    """Check if token is admin"""
    from security import validate_admin_token as vat
    return vat(token)
