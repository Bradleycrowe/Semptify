"""
Dakota County Eviction Defense - FastAPI Application
Main application entry point with all routes and services.
"""

import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Request, Query, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import routes
from routes.flows import router as flows_router
from routes.forms import router as forms_router

# Import services
from services.i18n import get_string, get_all_strings, get_supported_languages, is_rtl

# ============================================================================
# Application Setup
# ============================================================================

app = FastAPI(
    title="Dakota County Eviction Defense",
    description="Interactive eviction defense system for tenants in Dakota County, Minnesota",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Base paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Add i18n functions to template globals
templates.env.globals["_"] = get_string
templates.env.globals["get_languages"] = get_supported_languages
templates.env.globals["is_rtl"] = is_rtl

# Register routers
app.include_router(flows_router, prefix="/flows", tags=["Defense Flows"])
app.include_router(forms_router, prefix="/forms", tags=["Court Forms"])


# ============================================================================
# Core Routes
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    lang: str = Query("en", description="Language code (en, es, so, ar)")
):
    """
    Home page - Entry point to Dakota County Eviction Defense system.
    Displays available defense pathways and resources.
    """
    strings = get_all_strings(lang)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lang": lang,
        "is_rtl": is_rtl(lang),
        "strings": strings,
        "languages": get_supported_languages(),
        "current_year": datetime.now().year
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "dakota-eviction-defense",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/strings/{lang}")
async def get_language_strings(lang: str):
    """Get all translated strings for a language."""
    if lang not in get_supported_languages():
        raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")
    
    return JSONResponse(content=get_all_strings(lang))


@app.get("/api/forms")
async def list_forms():
    """List all available court forms."""
    forms_path = ASSETS_DIR / "forms.json"
    
    if not forms_path.exists():
        raise HTTPException(status_code=500, detail="Forms manifest not found")
    
    with open(forms_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return JSONResponse(content=data)


@app.get("/api/resources")
async def list_resources():
    """List legal aid resources and contact information."""
    forms_path = ASSETS_DIR / "forms.json"
    
    if not forms_path.exists():
        return JSONResponse(content={"resources": []})
    
    with open(forms_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return JSONResponse(content={
        "resources": data.get("resources", []),
        "zoom_court": data.get("zoom_court", {})
    })


@app.get("/zoom-helper", response_class=HTMLResponse)
async def zoom_helper(
    request: Request,
    lang: str = Query("en", description="Language code")
):
    """
    Zoom Court Helper - Guidance for virtual court appearances.
    """
    strings = get_all_strings(lang)
    
    # Load Zoom tips from forms.json
    forms_path = ASSETS_DIR / "forms.json"
    zoom_tips = []
    
    if forms_path.exists():
        with open(forms_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            zoom_court = data.get("zoom_court", {}).get("dakota_county", {})
            zoom_tips = zoom_court.get("tips", [])
    
    return templates.TemplateResponse("flows/zoom_helper.html", {
        "request": request,
        "lang": lang,
        "is_rtl": is_rtl(lang),
        "strings": strings,
        "zoom_tips": zoom_tips,
        "languages": get_supported_languages()
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler."""
    lang = request.query_params.get("lang", "en")
    
    return templates.TemplateResponse("error.html", {
        "request": request,
        "lang": lang,
        "is_rtl": is_rtl(lang),
        "error_code": 404,
        "error_message": "Page not found"
    }, status_code=404)


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    """Custom 500 handler."""
    lang = request.query_params.get("lang", "en")
    
    return templates.TemplateResponse("error.html", {
        "request": request,
        "lang": lang,
        "is_rtl": is_rtl(lang),
        "error_code": 500,
        "error_message": "Something went wrong. Please try again."
    }, status_code=500)


# ============================================================================
# Startup Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print("=" * 60)
    print("🏠 Dakota County Eviction Defense System")
    print("=" * 60)
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"🌐 Languages: {', '.join(get_supported_languages())}")
    print(f"📄 Templates: {TEMPLATES_DIR}")
    print(f"📦 Assets: {ASSETS_DIR}")
    
    # Verify forms.json exists
    forms_path = ASSETS_DIR / "forms.json"
    if forms_path.exists():
        with open(forms_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            form_count = len(data.get("forms", []))
            print(f"✅ Forms manifest loaded: {form_count} forms")
    else:
        print("⚠️  Forms manifest not found - run setup script")
    
    print("=" * 60)
    print("🚀 Server ready at http://localhost:8001")
    print("📖 API docs at http://localhost:8001/docs")
    print("=" * 60)


# ============================================================================
# Run Configuration
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Separate port from main Semptify
        reload=True,
        reload_dirs=[str(BASE_DIR)]
    )
