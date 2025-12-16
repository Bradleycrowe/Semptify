"""
SEMPTIFY - FastAPI Version
Modern async web framework replacing Flask
All your features, zero Flask issues
"""

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
import shutil
from typing import Optional, List
import os

# Initialize FastAPI
app = FastAPI(
    title="Semptify - Tenant Rights Platform",
    description="Modern tenant rights protection platform",
    version="2.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
DB_PATH = "semptify_fastapi.db"

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Documents
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_hash TEXT,
            category TEXT,
            size INTEGER,
            upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Payments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Timeline
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Calendar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    """Run on app startup"""
    init_db()
    
    # Create directories
    Path("uploads/vault").mkdir(parents=True, exist_ok=True)
    Path("uploads/evidence").mkdir(parents=True, exist_ok=True)
    Path("exports").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    
    print("✅ Semptify FastAPI Started")
    print("📁 Directories initialized")
    print("💾 Database ready")

# ============================================================================
# HOME / DASHBOARD
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page / Dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get stats
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(size), 0) FROM documents')
    doc_count, doc_size = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM payments')
    pay_count, pay_total = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(*) FROM timeline_events')
    event_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM calendar_events WHERE date >= date("now")')
    upcoming_count = cursor.fetchone()[0]
    
    # Recent activity
    cursor.execute('SELECT date, title, category FROM timeline_events ORDER BY created_at DESC LIMIT 10')
    recent_events = cursor.fetchall()
    
    conn.close()
    
    return templates.TemplateResponse("fastapi_home.html", {
        "request": request,
        "doc_count": doc_count,
        "doc_size": doc_size / 1024 / 1024,  # MB
        "pay_count": pay_count,
        "pay_total": pay_total,
        "event_count": event_count,
        "upcoming_count": upcoming_count,
        "recent_events": recent_events
    })

# ============================================================================
# DOCUMENT VAULT
# ============================================================================

@app.get("/vault", response_class=HTMLResponse)
async def vault_page(request: Request):
    """Document vault page"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, category, upload_date, size, file_hash FROM documents ORDER BY upload_date DESC')
    documents = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("fastapi_vault.html", {
        "request": request,
        "documents": documents
    })

@app.post("/vault/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("Document")
):
    """Upload document to vault"""
    try:
        # Read file content
        content = await file.read()
        
        # Calculate hash
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Save file
        filename = file.filename
        filepath = Path(f"uploads/vault/{filename}")
        
        # Handle duplicates
        counter = 1
        while filepath.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            filepath = Path(f"uploads/vault/{stem}_{counter}{suffix}")
            counter += 1
        
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (filename, filepath, file_hash, category, size, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filepath.name, str(filepath), file_hash, category, len(content), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return JSONResponse({
            "success": True,
            "message": f"Uploaded: {filepath.name}",
            "hash": file_hash[:16] + "..."
        })
    
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/vault/download/{doc_id}")
async def download_document(doc_id: int):
    """Download document"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT filepath, filename FROM documents WHERE id = ?', (doc_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    
    filepath, filename = result
    
    if not Path(filepath).exists():
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(filepath, filename=filename)

@app.delete("/vault/delete/{doc_id}")
async def delete_document(doc_id: int):
    """Delete document"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT filepath FROM documents WHERE id = ?', (doc_id,))
    result = cursor.fetchone()
    
    if result:
        try:
            Path(result[0]).unlink()
        except:
            pass
        
        cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
        conn.commit()
    
    conn.close()
    
    return JSONResponse({"success": True, "message": "Document deleted"})

# ============================================================================
# PAYMENT LEDGER
# ============================================================================

@app.get("/ledger", response_class=HTMLResponse)
async def ledger_page(request: Request):
    """Payment ledger page"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, amount, type, notes FROM payments ORDER BY date DESC')
    payments = cursor.fetchall()
    
    cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM payments')
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return templates.TemplateResponse("fastapi_ledger.html", {
        "request": request,
        "payments": payments,
        "total": total
    })

@app.post("/ledger/add")
async def add_payment(
    date: str = Form(...),
    amount: float = Form(...),
    payment_type: str = Form(...),
    notes: str = Form("")
):
    """Add payment"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payments (date, amount, type, notes, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, amount, payment_type, notes, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return JSONResponse({
        "success": True,
        "message": f"Added payment: ${amount:.2f}"
    })

# ============================================================================
# TIMELINE
# ============================================================================

@app.get("/timeline", response_class=HTMLResponse)
async def timeline_page(request: Request):
    """Timeline page"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, title, category, description FROM timeline_events ORDER BY date DESC')
    events = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("fastapi_timeline.html", {
        "request": request,
        "events": events
    })

@app.post("/timeline/add")
async def add_timeline_event(
    date: str = Form(...),
    title: str = Form(...),
    category: str = Form("Issue"),
    description: str = Form("")
):
    """Add timeline event"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline_events (date, title, category, description, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, title, category, description, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return JSONResponse({
        "success": True,
        "message": f"Added event: {title}"
    })

# ============================================================================
# CALENDAR / REMINDERS
# ============================================================================

@app.get("/calendar", response_class=HTMLResponse)
async def calendar_page(request: Request):
    """Calendar page"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, title, description, priority FROM calendar_events ORDER BY date')
    events = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("fastapi_calendar.html", {
        "request": request,
        "events": events
    })

@app.post("/calendar/add")
async def add_calendar_event(
    date: str = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Normal")
):
    """Add calendar event"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calendar_events (date, title, description, priority, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, title, description, priority, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return JSONResponse({
        "success": True,
        "message": f"Added reminder: {title}"
    })

# ============================================================================
# API ENDPOINTS (for AJAX/JSON requests)
# ============================================================================

@app.get("/api/stats")
async def api_stats():
    """Get statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM documents')
    docs = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM payments')
    payments = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM timeline_events')
    events = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM calendar_events')
    reminders = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "documents": docs,
        "payments": payments,
        "events": events,
        "reminders": reminders,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/documents")
async def api_documents():
    """Get all documents"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, category, upload_date, size FROM documents ORDER BY upload_date DESC')
    docs = cursor.fetchall()
    conn.close()
    
    return {
        "documents": [
            {
                "id": d[0],
                "filename": d[1],
                "category": d[2],
                "upload_date": d[3],
                "size": d[4]
            }
            for d in docs
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "framework": "FastAPI",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🛡️  SEMPTIFY - FastAPI Edition")
    print("="*60)
    print("✅ Modern async web framework")
    print("✅ Better than Flask - faster & more stable")
    print("✅ Auto-generated API docs at /docs")
    print("✅ OpenAPI schema at /openapi.json")
    print("="*60)
    print("\n🚀 Starting server...\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
