"""
Calendar Storage FastAPI Router - Calendar events with vault storage
Converted from Flask blueprint: calendar_storage_routes.py
"""
from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import json

from calendar_vault_bridge import CalendarVaultBridge
from security import validate_user_token

router = APIRouter(tags=["calendar-storage"])
templates = Jinja2Templates(directory="templates")
bridge = CalendarVaultBridge()


# ============================================================================
# Pydantic Models
# ============================================================================

class AddEventResponse(BaseModel):
    ok: bool
    message: str
    event_id: str
    documents: List[str]


# ============================================================================
# Helper Functions
# ============================================================================

def _sha256_of_file(file_path: str) -> str:
    """Calculate SHA256 hash of file"""
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# ============================================================================
# Routes
# ============================================================================

@router.get("/calendar", response_class=HTMLResponse)
async def calendar_view(request: Request):
    """
    Calendar interface for adding events + documents
    
    Provides UI for creating calendar events that are automatically
    stored in the vault with associated documents.
    """
    return templates.TemplateResponse("calendar_vault/calendar_input.html", {"request": request})


@router.post("/api/calendar/add-event", response_model=AddEventResponse)
async def add_event_with_storage(
    user_token: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    event_date: str = Form(...),
    event_type: str = Form("general"),
    files: List[UploadFile] = File(default=[])
):
    """
    Add event to calendar AND store in vault
    
    Accepts event data with optional file attachments. Files are stored
    in the vault with certificate generation, and the event is cataloged
    with document references.
    
    Triggers:
    - Curiosity engine hooks
    - Journey automation
    """
    if not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")
    
    event_data = {
        'title': title,
        'description': description or '',
        'event_date': event_date,
        'event_type': event_type
    }
    
    # Handle file uploads (store in vault)
    document_ids = []
    if files:
        user_dir = os.path.join('uploads', 'vault', user_token)
        os.makedirs(user_dir, exist_ok=True)
        
        for file in files:
            if file.filename:
                # Generate document ID
                timestamp = datetime.utcnow().isoformat().replace(':', '').replace('-', '').replace('.', '')
                doc_id = f"doc_{timestamp}_{file.filename}"
                
                # Save file
                file_path = os.path.join(user_dir, doc_id)
                contents = await file.read()
                with open(file_path, 'wb') as f:
                    f.write(contents)
                
                # Create certificate
                cert = {
                    'doc_id': doc_id,
                    'filename': file.filename,
                    'sha256': _sha256_of_file(file_path),
                    'timestamp': datetime.utcnow().isoformat(),
                    'uploaded_via': 'calendar',
                    'event_title': event_data['title']
                }
                
                cert_file = os.path.join(user_dir, f'{doc_id}.cert.json')
                with open(cert_file, 'w', encoding='utf-8') as f:
                    json.dump(cert, f, indent=2)
                
                document_ids.append(doc_id)
    
    # Catalog event with documents
    try:
        catalog_entry = bridge.catalog_event_with_documents(
            user_id=user_token,
            event_data=event_data,
            document_ids=document_ids
        )
        
        # Trigger curiosity hook
        try:
            from curiosity_hooks import on_calendar_event_added, auto_advance_journey
            question = on_calendar_event_added(user_token, event_data)
            if question:
                print(f'[CURIOSITY] {question}')
        except Exception as e:
            print(f'[WARN] Curiosity hook failed: {e}')
        
        # Journey automation
        try:
            from curiosity_hooks import auto_advance_journey
            journey_result = auto_advance_journey(user_token, 'calendar', {
                'action_type': 'calendar_event',
                'event_type': event_data.get('event_type', 'general')
            })
            if journey_result and journey_result.get('advanced'):
                print(f'[JOURNEY] Advanced to: {journey_result.get("new_stage")}')
        except Exception as e:
            print(f'[WARN] Journey automation failed: {e}')
        
        return AddEventResponse(
            ok=True,
            message=f'Event stored with {len(document_ids)} document(s)',
            event_id=catalog_entry['event_id'],
            documents=document_ids
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline", response_class=HTMLResponse)
async def timeline_viewer(
    request: Request,
    user_token: Optional[str] = None,
    view: str = "month"
):
    """
    Lightweight viewer for vault contents
    
    Displays timeline of events and documents with filtering by view type.
    """
    return templates.TemplateResponse(
        "calendar_vault/timeline_viewer.html",
        {
            "request": request,
            "user_token": user_token,
            "view": view
        }
    )
