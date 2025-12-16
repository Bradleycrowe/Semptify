"""
Calendar Timeline FastAPI Router - Timeline events and rent ledger API
Converted from Flask blueprint: calendar_timeline_routes.py
"""
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import io

from engines.calendar_timeline_engine import get_timeline_engine

router = APIRouter(prefix="/api/calendar", tags=["calendar-timeline"])


# ============================================================================
# Pydantic Models
# ============================================================================

class CreateEventRequest(BaseModel):
    type: str
    date: str
    title: str
    description: Optional[str] = ""
    amount: Optional[float] = None
    status: str = "upcoming"
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateEventRequest(BaseModel):
    type: Optional[str] = None
    date: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EventsResponse(BaseModel):
    success: bool
    count: int
    events: List[Dict[str, Any]]


class EventResponse(BaseModel):
    success: bool
    event: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None


class ExportICalRequest(BaseModel):
    event_ids: Optional[str] = None


# ============================================================================
# Routes
# ============================================================================

@router.get("/events", response_model=EventsResponse)
async def get_events(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    types: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None)
):
    """
    Get filtered timeline events
    
    Query params:
    - start_date: ISO date (YYYY-MM-DD)
    - end_date: ISO date
    - types: comma-separated event types
    - status: upcoming|completed|missed|cancelled
    - user_id: filter by user
    """
    engine = get_timeline_engine()
    
    event_types = types.split(',') if types else None
    
    events = engine.get_events(
        start_date=start_date,
        end_date=end_date,
        event_types=event_types,
        status=status,
        user_id=user_id
    )
    
    return EventsResponse(success=True, count=len(events), events=events)


@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(data: CreateEventRequest):
    """
    Create new timeline event
    
    Supports event types:
    - rent_payment
    - court_date
    - deadline
    - lease_violation
    - repair_request
    - inspection
    """
    engine = get_timeline_engine()
    
    try:
        event = engine.add_event(
            event_type=data.type,
            date=data.date,
            title=data.title,
            description=data.description,
            amount=data.amount,
            status=data.status,
            user_id=data.user_id,
            metadata=data.metadata
        )
        
        return EventResponse(success=True, event=event)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: str, data: UpdateEventRequest):
    """
    Update existing event
    
    Partial updates supported - only provided fields are updated.
    """
    engine = get_timeline_engine()
    
    # Convert to dict and remove None values
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    # Don't allow changing ID or created_at (not in model anyway)
    update_data.pop('id', None)
    update_data.pop('created_at', None)
    
    success = engine.update_event(event_id, update_data)
    
    if success:
        return EventResponse(success=True, message="Event updated")
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}", response_model=EventResponse)
async def delete_event(event_id: str):
    """Delete timeline event"""
    engine = get_timeline_engine()
    
    success = engine.delete_event(event_id)
    
    if success:
        return EventResponse(success=True, message="Event deleted")
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.get("/rent-ledger")
async def get_rent_ledger(user_id: Optional[str] = Query(None)):
    """
    Get rent payment ledger
    
    Returns chronological list of rent payments with balance tracking.
    """
    engine = get_timeline_engine()
    ledger = engine.get_rent_ledger(user_id)
    
    return {"success": True, "ledger": ledger}


@router.get("/deadlines")
async def get_deadlines(
    days_ahead: int = Query(30),
    user_id: Optional[str] = Query(None)
):
    """
    Get upcoming deadlines
    
    Returns deadlines within specified number of days with urgency scoring.
    """
    engine = get_timeline_engine()
    deadlines = engine.get_upcoming_deadlines(days_ahead, user_id)
    
    return {"success": True, "count": len(deadlines), "deadlines": deadlines}


@router.get("/statistics")
async def get_statistics(user_id: Optional[str] = Query(None)):
    """
    Get timeline statistics
    
    Returns:
    - Event counts by type
    - Completion rates
    - Missed deadline counts
    - Payment statistics
    """
    engine = get_timeline_engine()
    stats = engine.get_statistics(user_id)
    
    return {"success": True, "statistics": stats}


@router.get("/export/ical")
async def export_ical_get(event_ids: Optional[str] = Query(None)):
    """
    Export events to iCal format (GET)
    
    Query param:
    - event_ids: comma-separated list of event IDs (optional, exports all if omitted)
    
    Returns .ics file for calendar import
    """
    engine = get_timeline_engine()
    
    ids = event_ids.split(',') if event_ids else None
    ical_content = engine.export_to_ical(ids)
    
    ical_file = io.BytesIO(ical_content.encode('utf-8'))
    ical_file.seek(0)
    
    filename = f"semptify_timeline_{datetime.now().strftime('%Y%m%d')}.ics"
    
    return StreamingResponse(
        ical_file,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/export/ical")
async def export_ical_post(data: ExportICalRequest):
    """
    Export events to iCal format (POST)
    
    Body:
    - event_ids: comma-separated list of event IDs (optional)
    
    Returns .ics file for calendar import
    """
    engine = get_timeline_engine()
    
    ids = data.event_ids.split(',') if data.event_ids else None
    ical_content = engine.export_to_ical(ids)
    
    ical_file = io.BytesIO(ical_content.encode('utf-8'))
    ical_file.seek(0)
    
    filename = f"semptify_timeline_{datetime.now().strftime('%Y%m%d')}.ics"
    
    return StreamingResponse(
        ical_file,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/types")
async def get_event_types():
    """
    Get available event types with metadata
    
    Returns list of supported event types with:
    - Display names
    - Icons
    - Default durations
    - Color codes
    """
    engine = get_timeline_engine()
    
    return {"success": True, "event_types": engine.event_types}
