"""
Timeline API FastAPI Router - Deadline intelligence and management
Converted from Flask blueprint: timeline_api_routes.py
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from timeline_intelligence import TimelineIntelligence

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


# ============================================================================
# Pydantic Models
# ============================================================================

class DeadlineResponse(BaseModel):
    success: bool
    deadlines: Optional[List[Dict[str, Any]]] = None
    next_deadline: Optional[Dict[str, Any]] = None
    critical_count: Optional[int] = None
    requires_immediate_action: Optional[bool] = None
    error: Optional[str] = None


class NextActionResponse(BaseModel):
    success: bool
    next_deadline: Optional[Dict[str, Any]] = None
    critical_count: Optional[int] = None
    requires_immediate_action: Optional[bool] = None
    message: Optional[str] = None
    error: Optional[str] = None


# ============================================================================
# Routes
# ============================================================================

@router.get("/deadlines/{user_id}")
async def get_deadlines(user_id: str):
    """
    Get all deadlines for a user with urgency analysis.
    Returns comprehensive deadline data.
    """
    try:
        intel = TimelineIntelligence()
        result = intel.get_user_deadlines(user_id)

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/next-action/{user_id}")
async def get_next_action(user_id: str):
    """
    Get the most urgent next action for a user.
    Returns single most critical deadline with action steps.
    """
    try:
        intel = TimelineIntelligence()
        result = intel.get_user_deadlines(user_id)

        if result.get('next_deadline'):
            return {
                "success": True,
                "next_deadline": result['next_deadline'],
                "critical_count": result['critical_count'],
                "requires_immediate_action": result['requires_immediate_action']
            }
        else:
            return {
                "success": True,
                "next_deadline": None,
                "message": "No upcoming deadlines found"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
