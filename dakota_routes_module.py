"""
Dakota County Eviction Defense Routes
Complete module with eviction guide, motions library, and countersuits
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Create router
dakota_router = APIRouter(prefix="/library/dakota", tags=["Dakota County"])

# Initialize templates
templates = Jinja2Templates(directory="templates")

@dakota_router.get("", response_class=HTMLResponse)
@dakota_router.get("/", response_class=HTMLResponse)
async def dakota_library(request: Request):
    """Dakota County resources library homepage"""
    return templates.TemplateResponse("fastapi_dakota.html", {"request": request})

@dakota_router.get("/eviction", response_class=HTMLResponse)
async def dakota_eviction(request: Request):
    """Dakota County eviction defense complete guide"""
    return templates.TemplateResponse("fastapi_dakota_eviction.html", {"request": request})

@dakota_router.get("/motions", response_class=HTMLResponse)
async def dakota_motions(request: Request):
    """Dakota County defensive motions library"""
    return templates.TemplateResponse("fastapi_dakota_motions.html", {"request": request})

@dakota_router.get("/countersuits", response_class=HTMLResponse)
async def dakota_countersuits(request: Request):
    """Dakota County offensive countersuits library"""
    return templates.TemplateResponse("fastapi_dakota_countersuits.html", {"request": request})
