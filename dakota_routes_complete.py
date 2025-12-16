"""
Dakota County Eviction Defense Module - FastAPI Routes
Complete integration with all motions, tactics, statutes, and forms
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

# Create router
dakota_router = APIRouter(prefix="/dakota", tags=["Dakota County"])

# Templates
templates = Jinja2Templates(directory="templates")

# Load UI strings
try:
    with open("DakotaCounty_EvictionDefense_Module/ui_strings.json", "r") as f:
        UI_STRINGS = json.load(f)
except:
    UI_STRINGS = {
        "module_title": "Dakota County Eviction Defense",
        "emergency_warning": "Emergency eviction notice? You typically have 7-14 days to respond!"
    }

@dakota_router.get("/", response_class=HTMLResponse)
async def dakota_home(request: Request):
    """Dakota County main page"""
    return templates.TemplateResponse("dakota_home.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/eviction", response_class=HTMLResponse)
@dakota_router.get("/eviction/defense", response_class=HTMLResponse)
async def eviction_defense_full(request: Request):
    """Complete eviction defense library"""
    return templates.TemplateResponse("dakota_eviction_complete.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/motions", response_class=HTMLResponse)
async def motions_and_actions(request: Request):
    """All motions and legal actions"""
    return templates.TemplateResponse("dakota_motions.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/tactics", response_class=HTMLResponse)
async def proactive_tactics(request: Request):
    """Proactive defense tactics"""
    return templates.TemplateResponse("dakota_tactics.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/statutes", response_class=HTMLResponse)
async def statutes_and_forms(request: Request):
    """MN statutes and court forms"""
    return templates.TemplateResponse("dakota_statutes.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/process", response_class=HTMLResponse)
async def process_flow(request: Request):
    """Eviction process flowchart"""
    return templates.TemplateResponse("dakota_process.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/countersuits", response_class=HTMLResponse)
async def countersuit_guide(request: Request):
    """Countersuit strategies and forms"""
    return templates.TemplateResponse("dakota_countersuits.html", {
        "request": request,
        "ui": UI_STRINGS
    })

@dakota_router.get("/api/search")
async def search_library(query: str):
    """Search Dakota library content"""
    # Simple search implementation
    results = []
    
    if "eviction" in query.lower():
        results.append({
            "title": "Eviction Defense Guide",
            "url": "/dakota/eviction",
            "description": "Complete eviction defense with timelines and defenses"
        })
    
    if "motion" in query.lower():
        results.append({
            "title": "Motions & Actions",
            "url": "/dakota/motions",
            "description": "All available motions and legal actions"
        })
    
    if "statute" in query.lower():
        results.append({
            "title": "MN Statutes & Forms",
            "url": "/dakota/statutes",
            "description": "Minnesota housing law statutes and court forms"
        })
    
    return {"query": query, "results": results}

