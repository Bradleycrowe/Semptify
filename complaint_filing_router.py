"""
FastAPI router for comprehensive complaint filing system.
Converted from Flask blueprint: complaint_filing_routes.py
"""
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
import os
from pathlib import Path

from engines.complaint_filing_engine import get_filing_engine, VenueType
from engines.accuracy_engine import get_accuracy_engine

router = APIRouter(prefix="/complaint", tags=["complaint-filing"])
templates = Jinja2Templates(directory="templates")


# ============================================================================
# Pydantic Models
# ============================================================================

class LocationModel(BaseModel):
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None


class IdentifyVenuesRequest(BaseModel):
    issue_type: str
    location: LocationModel
    user_situation: Optional[Dict[str, Any]] = {}
    urgency: Optional[str] = "normal"


class GetProceduresRequest(BaseModel):
    location: LocationModel


class OutcomeModel(BaseModel):
    success: bool
    timeline: Optional[str] = None
    resolution: Optional[str] = None
    notes: Optional[str] = None


class TrackOutcomeRequest(BaseModel):
    venue_key: str
    location: LocationModel
    issue_type: str
    outcome: OutcomeModel


class UpdateProcedureRequest(BaseModel):
    venue_key: str
    location: LocationModel
    procedure: Dict[str, Any]


class AutofillRequest(BaseModel):
    user_token: Optional[str] = None


# ============================================================================
# Context Integration - Auto-fill from uploaded documents
# ============================================================================

def get_user_context_data(user_token: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Fetch user's context data from unified Context System.
    Returns: {
        'user': user_info,
        'documents': [uploaded docs with intelligence],
        'timeline': timeline events,
        'case_data': extracted case information
    }
    """
    try:
        from security import validate_user_token
        user_id = validate_user_token(user_token)
        if not user_id:
            return None

        # Get comprehensive context
        context = {
            'user_id': user_id,
            'documents': [],
            'timeline': [],
            'case_data': {}
        }

        # Load vault documents with intelligence
        vault_dir = f"uploads/vault/{user_id}"
        if os.path.exists(vault_dir):
            for filename in os.listdir(vault_dir):
                if filename.endswith('.cert.json'):
                    cert_path = os.path.join(vault_dir, filename)
                    with open(cert_path, 'r') as f:
                        cert = json.load(f)
                        context['documents'].append(cert)

        # Load intelligence data
        intel_path = f"{vault_dir}/intelligence.json"
        if os.path.exists(intel_path):
            with open(intel_path, 'r') as f:
                intel = json.load(f)
                context['case_data']['intelligence'] = intel

        # Load timeline events
        from user_database import get_user_db
        conn = get_user_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT event_type, title, description, event_date, created_at
            FROM timeline_events
            WHERE user_id = ?
            ORDER BY event_date DESC
        ''', (user_id,))

        for row in cursor.fetchall():
            context['timeline'].append({
                'event_type': row[0],
                'title': row[1],
                'description': row[2],
                'event_date': row[3],
                'created_at': row[4]
            })

        conn.close()

        # Extract key case data from documents
        context['case_data']['landlord_name'] = None
        context['case_data']['property_address'] = None
        context['case_data']['lease_start_date'] = None
        context['case_data']['monthly_rent'] = None
        context['case_data']['issue_description'] = None

        # Parse from intelligence if available
        if 'intelligence' in context['case_data']:
            intel = context['case_data']['intelligence']
            if 'parties' in intel:
                parties = intel.get('parties', [])
                for party in parties:
                    if party.get('role') == 'landlord':
                        context['case_data']['landlord_name'] = party.get('name')

            if 'monetary_amounts' in intel:
                amounts = intel.get('monetary_amounts', [])
                if amounts:
                    context['case_data']['monthly_rent'] = amounts[0].get('amount')

            if 'key_dates' in intel:
                dates = intel.get('key_dates', [])
                for date_obj in dates:
                    if 'lease_start' in date_obj.get('label', '').lower():
                        context['case_data']['lease_start_date'] = date_obj.get('date')

        return context

    except Exception as e:
        print(f"[ERROR] Context data fetch failed: {e}")
        return None


# ============================================================================
# Routes
# ============================================================================

@router.get("/file-complaint", response_class=HTMLResponse)
async def file_complaint_page(request: Request):
    """
    Main complaint filing page.
    User describes issue, system identifies ALL venues.
    """
    return templates.TemplateResponse("file_complaint.html", {"request": request})


@router.post("/api/identify-venues")
async def identify_venues(data: IdentifyVenuesRequest):
    """
    Identify all applicable filing venues for issue.
    Returns multi-venue strategy.
    """
    filing_engine = get_filing_engine()

    # Get comprehensive filing strategy
    strategy = filing_engine.generate_filing_strategy(
        issue_type=data.issue_type,
        location=data.location.dict(),
        user_situation=data.user_situation,
        urgency=data.urgency
    )

    return {
        "success": True,
        "strategy": strategy,
        "total_venues": len(strategy.get("immediate_actions", [])) + len(strategy.get("simultaneous_filings", [])),
        "confidence": strategy.get("success_probability")
    }


@router.post("/api/get-procedures/{venue_key}")
async def get_filing_procedures(venue_key: str, data: GetProceduresRequest):
    """
    Get detailed step-by-step procedures for specific venue.
    Returns most up-to-date, verified procedures.
    """
    filing_engine = get_filing_engine()
    accuracy_engine = get_accuracy_engine()

    # Get current procedures
    procedures = filing_engine._get_current_procedures(venue_key, data.location.dict())

    # Verify accuracy
    verification = accuracy_engine.verify_guidance(
        guidance_type="filing_procedure",
        location_key=f"{data.location.city}_{data.location.state}",
        guidance_content=json.dumps(procedures),
        sources=[{"type": "official_website"}, {"type": "user_outcome"}]
    )

    return {
        "success": True,
        "procedures": procedures,
        "verification": {
            "confidence": verification.get("confidence"),
            "quality_level": verification.get("quality_level"),
            "last_verified": procedures.get("last_updated")
        }
    }


@router.post("/api/track-outcome")
async def track_outcome(data: TrackOutcomeRequest):
    """
    User reports outcome of filing.
    System learns what works.
    """
    filing_engine = get_filing_engine()

    # Track outcome for effectiveness scoring
    filing_engine.track_filing_outcome(
        venue_key=data.venue_key,
        location=data.location.dict(),
        issue_type=data.issue_type,
        outcome=data.outcome.dict()
    )

    # Also track in accuracy engine
    accuracy_engine = get_accuracy_engine()
    accuracy_engine.track_outcome(
        guidance_type="filing_venue",
        location_key=f"{data.location.city}_{data.location.state}",
        guidance_content=data.venue_key,
        outcome="success" if data.outcome.success else "failure"
    )

    return {
        "success": True,
        "message": "Outcome recorded. Thank you for helping improve the system!"
    }


@router.post("/api/update-procedure")
async def update_procedure(data: UpdateProcedureRequest):
    """
    User provides updated procedure info.
    Keeps procedures current.
    """
    filing_engine = get_filing_engine()

    filing_engine.update_procedures_from_outcome(
        venue_key=data.venue_key,
        location=data.location.dict(),
        updated_procedure=data.procedure
    )

    return {
        "success": True,
        "message": "Procedure updated. Thank you!"
    }


@router.get("/library", response_class=HTMLResponse)
async def complaint_library(request: Request):
    """
    Browse all known venues and procedures.
    Searchable by issue type, location, agency.
    """
    filing_engine = get_filing_engine()

    # Get all venues
    all_venues = filing_engine.venues

    # Group by type
    federal_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') == 'federal'}
    state_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') == 'state'}
    local_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') in ['city', 'county']}

    return templates.TemplateResponse(
        "complaint_library.html",
        {
            "request": request,
            "federal_venues": federal_venues,
            "state_venues": state_venues,
            "local_venues": local_venues,
            "total_venues": len(all_venues)
        }
    )


@router.get("/success-stories", response_class=HTMLResponse)
async def success_stories(request: Request):
    """
    Show success stories by venue.
    Users see what works.
    """
    filing_engine = get_filing_engine()
    accuracy_engine = get_accuracy_engine()

    # Get outcomes data
    all_outcomes = filing_engine.outcomes

    # Find high-success venues
    success_stories = []
    for outcome_key, outcome_data in all_outcomes.items():
        if outcome_data.get("total_count", 0) >= 3:
            effectiveness = outcome_data.get("effectiveness", 0)
            if effectiveness >= 0.75:
                venue_key, location_key, issue_type = outcome_key.split(":")

                success_stories.append({
                    "venue_key": venue_key,
                    "location": location_key,
                    "issue_type": issue_type,
                    "success_rate": f"{int(effectiveness * 100)}%",
                    "case_count": outcome_data["total_count"],
                    "recent_outcomes": outcome_data.get("outcomes", [])[-3:]  # Last 3
                })

    # Sort by success rate
    success_stories.sort(key=lambda x: float(x["success_rate"].rstrip('%')), reverse=True)

    return templates.TemplateResponse(
        "filing_success_stories.html",
        {
            "request": request,
            "success_stories": success_stories
        }
    )


@router.post("/api/autofill")
async def autofill_complaint(data: AutofillRequest, x_user_token: Optional[str] = Header(None)):
    """
    Auto-fill complaint form from user's context data.
    Returns pre-populated form fields from uploaded documents.
    """
    user_token = data.user_token or x_user_token

    # Get context data
    context = get_user_context_data(user_token)
    if not context:
        raise HTTPException(status_code=500, detail="Could not load context data")

    # Build pre-filled form data
    form_data = {
        'tenant_name': None,  # Would come from user profile
        'landlord_name': context['case_data'].get('landlord_name'),
        'property_address': context['case_data'].get('property_address'),
        'lease_start_date': context['case_data'].get('lease_start_date'),
        'monthly_rent': context['case_data'].get('monthly_rent'),
        'issue_description': context['case_data'].get('issue_description'),
        'evidence_count': len(context['documents']),
        'evidence_files': [
            {
                'filename': doc.get('filename'),
                'doc_type': doc.get('intelligence', {}).get('doc_type'),
                'upload_date': doc.get('created')
            }
            for doc in context['documents']
            if doc.get('filename')
        ],
        'timeline_events': [
            {
                'date': event.get('event_date'),
                'description': event.get('title')
            }
            for event in context['timeline'][:10]  # Most recent 10
        ],
        'intelligence_available': 'intelligence' in context['case_data']
    }

    return {
        "success": True,
        "form_data": form_data,
        "context_loaded": True,
        "documents_found": len(context['documents']),
        "timeline_events_found": len(context['timeline'])
    }
