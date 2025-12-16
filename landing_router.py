"""
Landing FastAPI Router - Main landing/welcome page
Converted from Flask blueprint: landing_routes.py
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(tags=["landing"])
templates = Jinja2Templates(directory="templates")

WELCOME_HTML = """<!DOCTYPE html><html><head><title>Semptify</title><style>body{font-family:system-ui;max-width:900px;margin:50px auto;padding:20px;background:#f5f5f5}.container{background:white;padding:40px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}h1{color:#2c5aa0;margin-bottom:10px}.subtitle{color:#666;margin-bottom:30px}.card{background:#f8f9fa;padding:25px;border-radius:8px;margin:20px 0;border-left:4px solid #2c5aa0}.card h3{margin-top:0;color:#2c5aa0}textarea{width:100%;padding:12px;border:2px solid #ddd;border-radius:6px;font-family:inherit;font-size:14px}.voice-btn{background:#2c5aa0;color:white;border:none;padding:12px 24px;border-radius:6px;cursor:pointer;margin:10px 5px}.voice-btn:hover{background:#1e4070}.features{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin:20px 0}.feature{background:white;border:2px solid #e0e0e0;padding:20px;border-radius:8px;cursor:pointer;transition:all 0.2s}.feature:hover{border-color:#2c5aa0;transform:translateY(-2px);box-shadow:0 4px 8px rgba(0,0,0,0.1)}.feature h4{margin:0 0 10px 0;color:#2c5aa0}.info{background:#e3f2fd;padding:15px;border-radius:6px;margin:20px 0}</style></head><body><div class="container"><h1>Welcome to Semptify</h1><p class="subtitle">How can we help protect your tenant rights?</p><div class="card"><h3>📋 Current Situation</h3><textarea id="situation" rows="4" placeholder="Describe your situation... (e.g., 'My landlord is threatening eviction')"></textarea><button class="voice-btn" onclick="startVoice()">🎤 Or Ask Vocally</button><button class="voice-btn" onclick="analyzeSituation()">→ Get Help</button></div><div class="features"><div class="feature" onclick="location.href='/vault?user_token={{ token }}'"><h4>📄 Document Vault</h4><p>Analyze & organize your paperwork</p></div><div class="feature" onclick="location.href='/journey?user_token={{ token }}'"><h4>🗺️ Interactive Journey</h4><p>Guided help for your situation</p></div><div class="feature" onclick="location.href='/research?user_token={{ token }}'"><h4>🔍 Research</h4><p>Landlord, building, property info</p></div><div class="feature" onclick="location.href='/calendar?user_token={{ token }}'"><h4>📅 Calendar</h4><p>Track events & deadlines</p></div></div><div class="info">✅ Connected: Data encrypted in your storage<br>🔐 Token: <code>{{ token }}</code></div></div><script>function startVoice(){if(!('webkitSpeechRecognition' in window)){alert('Voice not supported. Use Chrome/Edge.');return}const r=new webkitSpeechRecognition();r.continuous=false;r.interimResults=false;r.onresult=(e)=>{document.getElementById('situation').value=e.results[0][0].transcript};r.start()}function analyzeSituation(){const t=document.getElementById('situation').value.trim();if(!t){alert('Please describe your situation first');return}location.href='/analyze?text='+encodeURIComponent(t)+'&user_token={{ token }}'}</script></body></html>"""


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    user_token: Optional[str] = Query(None)
):
    """
    Main landing/welcome page
    
    If user has token: Shows personalized welcome with feature access
    If no token: Redirects to setup
    
    Features:
    - Situation analysis with voice input
    - Quick access to vault, journey, research, calendar
    - Token display
    """
    # Check for token in query param or session
    token = user_token
    if hasattr(request, 'session'):
        token = token or request.session.get('user_token')
        if not token and hasattr(request, 'state'):
            token = getattr(request.state, 'user_token', None)
    
    if token:
        # Store in session if available
        if hasattr(request, 'session'):
            request.session['user_token'] = token
        # Render welcome page with Jinja2-style substitution
        html = WELCOME_HTML.replace('{{ token }}', token)
        return HTMLResponse(content=html)
    
    return RedirectResponse(url='/setup')
