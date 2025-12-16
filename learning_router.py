"""
Learning Engine FastAPI Router - Adaptive learning and suggestions
Converted from Flask blueprint: learning_routes.py
"""
from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import json

from engines.learning_engine import get_learning
from security import validate_user_token, validate_admin_token
from curiosity_hooks import on_learning_module_completed

router = APIRouter(prefix="/api/learning", tags=["learning"])


# ============================================================================
# Pydantic Models
# ============================================================================

class ObserveActionRequest(BaseModel):
    user_token: Optional[str] = None
    action: str
    context: Dict[str, Any] = {}


class ObserveSequenceRequest(BaseModel):
    user_token: Optional[str] = None
    action1: str
    action2: str


class FeedbackRequest(BaseModel):
    user_token: Optional[str] = None
    suggestion: str
    helpful: bool = False


class ResetRequest(BaseModel):
    admin_token: Optional[str] = None
    confirm: str


class ActionResponse(BaseModel):
    status: str
    action: Optional[str] = None
    sequence: Optional[str] = None
    thanks: Optional[str] = None


class SuggestionsResponse(BaseModel):
    personalized: List[str]
    time_based: Optional[str] = None
    next_action: Optional[str] = None


class StatsResponse(BaseModel):
    total_users: int
    total_sequences: int
    peak_hours: List[int]
    common_actions: List[tuple]


class DocumentSuggestionsResponse(BaseModel):
    modules: List[str] = []
    resources: List[str] = []
    next_steps: List[str] = []


# ============================================================================
# Routes
# ============================================================================

@router.post("/observe", response_model=ActionResponse)
async def observe_action(
    data: ObserveActionRequest,
    x_user_token: Optional[str] = Header(None)
):
    """
    Record a user action for learning
    
    Tracks user actions to build personalized patterns and suggestions.
    Triggers curiosity engine to identify learning opportunities.
    """
    user_token = data.user_token or x_user_token
    user_id = validate_user_token(user_token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    learning = get_learning()
    learning.observe_action(user_id, data.action, data.context)
    
    # Trigger curiosity hook
    try:
        question = on_learning_module_completed(user_id, data.action, data.context)
        if question:
            print(f'[CURIOSITY] {question}')
    except Exception as e:
        print(f'[WARN] Curiosity hook failed: {e}')
    
    return ActionResponse(status="recorded", action=data.action)


@router.post("/observe/sequence", response_model=ActionResponse)
async def observe_sequence(
    data: ObserveSequenceRequest,
    x_user_token: Optional[str] = Header(None)
):
    """
    Record an action sequence for learning
    
    Tracks sequential actions to identify user workflows and patterns.
    """
    user_token = data.user_token or x_user_token
    user_id = validate_user_token(user_token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    learning = get_learning()
    learning.observe_sequence(user_id, data.action1, data.action2)
    
    return ActionResponse(status="recorded", sequence=f"{data.action1}->{data.action2}")


@router.get("/suggest", response_model=SuggestionsResponse)
async def get_suggestion(
    user_token: Optional[str] = Query(None),
    last_action: Optional[str] = Query(None),
    x_user_token: Optional[str] = Header(None)
):
    """
    Get personalized suggestions for user
    
    Returns:
    - Personalized suggestions based on user history
    - Time-based suggestions (contextual to time of day)
    - Next action suggestions (if last_action provided)
    """
    token = user_token or x_user_token
    user_id = validate_user_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    learning = get_learning()
    
    suggestions = SuggestionsResponse(
        personalized=learning.get_personalized_suggestions(user_id),
        time_based=learning.get_time_based_suggestion()
    )
    
    if last_action:
        suggestions.next_action = learning.suggest_next_action(user_id, last_action)
    
    return suggestions


@router.post("/feedback", response_model=ActionResponse)
async def record_feedback(
    data: FeedbackRequest,
    x_user_token: Optional[str] = Header(None)
):
    """
    Record user feedback on suggestions
    
    Allows users to rate suggestion helpfulness, improving future recommendations.
    """
    user_token = data.user_token or x_user_token
    user_id = validate_user_token(user_token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    learning = get_learning()
    learning.record_feedback(data.suggestion, data.helpful)
    
    return ActionResponse(status="recorded", thanks="feedback recorded")


@router.get("/insights")
async def get_insights(
    user_token: Optional[str] = Query(None),
    admin_token: Optional[str] = Query(None),
    x_user_token: Optional[str] = Header(None),
    x_admin_token: Optional[str] = Header(None)
):
    """
    Get learning insights
    
    - User token: Shows personalized insights
    - Admin token: Shows global system insights
    """
    u_token = user_token or x_user_token
    a_token = admin_token or x_admin_token
    
    user_id = validate_user_token(u_token) if u_token else None
    admin_id = validate_admin_token(a_token) if a_token else None
    
    if not user_id and not admin_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    learning = get_learning()
    insights = learning.get_insights(user_id=user_id if not admin_id else None)
    
    return insights


@router.post("/admin/reset")
async def reset_learning(
    data: ResetRequest,
    x_admin_token: Optional[str] = Header(None)
):
    """
    Reset learning patterns (admin only)
    
    Clears all learning data. Requires confirmation string "RESET".
    """
    admin_token = data.admin_token or x_admin_token
    admin_id = validate_admin_token(admin_token)
    
    if not admin_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    if data.confirm != "RESET":
        raise HTTPException(status_code=400, detail="confirmation required")
    
    learning = get_learning()
    
    # Reset patterns
    learning.patterns = {
        "user_habits": {},
        "sequences": {},
        "time_patterns": {},
        "success_rates": {},
        "suggestions": {}
    }
    learning._save_patterns()
    
    return {"status": "reset", "message": "All learning patterns cleared"}


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get learning statistics (public endpoint)
    
    Returns:
    - Total users tracked
    - Total action sequences
    - Peak usage hours
    - Most common action patterns
    """
    learning = get_learning()
    
    stats = StatsResponse(
        total_users=len(learning.patterns["user_habits"]),
        total_sequences=len(learning.patterns["sequences"]),
        peak_hours=learning._get_peak_hours(),
        common_actions=sorted(
            learning.patterns["sequences"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
    )
    
    return stats


@router.get("/suggestions/{doc_id}", response_model=DocumentSuggestionsResponse)
async def get_document_learning_suggestions(
    doc_id: str,
    user_token: Optional[str] = Query(None),
    x_user_token: Optional[str] = Header(None)
):
    """
    Get learning suggestions for a specific uploaded document
    
    Returns personalized learning modules, resources, and next steps
    based on document analysis.
    """
    token = user_token or x_user_token
    user_id = validate_user_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    cert_path = os.path.join("uploads", "vault", doc_id, f"{doc_id}.cert.json")
    
    if not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="document not found")
    
    try:
        with open(cert_path, 'r') as f:
            cert = json.load(f)
        
        # Verify user owns this document
        if cert.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="unauthorized")
        
        suggestions = cert.get("learning_suggestions", {
            "modules": [],
            "resources": [],
            "next_steps": []
        })
        
        return DocumentSuggestionsResponse(**suggestions)
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="invalid certificate format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
