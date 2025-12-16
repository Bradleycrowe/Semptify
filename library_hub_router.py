"""
Library Hub FastAPI Router - Legal resource library
Converted from Flask blueprint: library_hub_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import markdown

router = APIRouter(tags=["library"])
templates = Jinja2Templates(directory="templates")


@router.get("/library", response_class=HTMLResponse)
async def library_hub(request: Request):
    """
    Legal resource library hub
    
    Provides access to:
    - Court forms and templates
    - Sample legal documents
    - Educational materials
    - Tenant rights guides
    """
    return templates.TemplateResponse("library_hub.html", {"request": request})


@router.get("/library/court-forms", response_class=HTMLResponse)
async def court_forms(request: Request):
    """
    Minnesota court forms and templates
    
    Displays court forms reference with markdown-rendered content.
    """
    with open('data/court_forms.md', 'r', encoding='utf-8') as f:
        content = f.read()
    html_content = markdown.markdown(content)
    
    return templates.TemplateResponse(
        "library_resource.html",
        {
            "request": request,
            "title": "Minnesota Court Forms & Templates",
            "content": html_content
        }
    )


@router.get("/library/sample-documents")
async def sample_documents():
    """Redirect to court forms"""
    return RedirectResponse(url="/library/court-forms")
