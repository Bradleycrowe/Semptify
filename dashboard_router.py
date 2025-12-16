"""
Dashboard API FastAPI Router - Dynamic content for cells A-F
Converted from Flask blueprint: dashboard_api_routes.py
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Literal

from engines.dashboard_engine import get_dashboard_engine, AVAILABLE_WIDGETS

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


# ============================================================================
# Pydantic Models
# ============================================================================

class ProgressUpdate(BaseModel):
    """User progress data for dashboard recalculation"""
    pass  # Flexible dict accepted


class CellResponse(BaseModel):
    widget_id: str
    content: Dict[str, Any]


class SuccessResponse(BaseModel):
    success: bool


# ============================================================================
# Routes
# ============================================================================

@router.get("/layout/{user_id}")
async def get_layout(user_id: str):
    """Get complete dashboard layout for user with widget details"""
    engine = get_dashboard_engine()
    layout = engine.get_user_layout(user_id)

    # Include widget details
    result = {}
    for cell, widget_id in layout.items():
        if widget_id in AVAILABLE_WIDGETS:
            result[cell] = {
                "widget_id": widget_id,
                **AVAILABLE_WIDGETS[widget_id]
            }

    return result


@router.get("/cell/{user_id}/{cell}")
async def get_cell(user_id: str, cell: Literal['a', 'b', 'c', 'd', 'e', 'f']):
    """Get content for a specific dashboard cell"""
    engine = get_dashboard_engine()
    content = engine.get_cell_content(user_id, cell)
    return content


@router.post("/progress/{user_id}", response_model=SuccessResponse)
async def update_progress(user_id: str, data: Dict[str, Any]):
    """Update user progress (triggers layout recalculation)"""
    engine = get_dashboard_engine()
    engine.update_user_progress(user_id, data)
    return SuccessResponse(success=True)


@router.get("/widgets")
async def list_widgets():
    """List all available dashboard widgets"""
    return AVAILABLE_WIDGETS
