# ==== Auth Bypass (dev/demo) ================================================
try:
    import auth_bypass
    auth_bypass.enable()
except Exception as e:
    print(f"Auth bypass not applied: {e}")
# ============================================================================
"""
Semptify - Learning-Enabled Legal Defense Platform
Fresh FastAPI application with integrated learning engine
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from learning_engine import LearningMiddleware, get_learning_engine
import os
from pathlib import Path

# Create FastAPI app
app = FastAPI(
    title="Semptify - Dakota County Eviction Defense",
    description="Learning-enabled tenant rights protection platform",
    version="2.0.0"
)

# Add learning middleware - observes ALL interactions
app.add_middleware(LearningMiddleware)

# Template directory
templates = Jinja2Templates(directory="templates")

# Mount static files if directory exists
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Create required directories
REQUIRED_DIRS = [
    "uploads", "logs", "security", "data", 
    "copilot_sync", "final_notices",
    "learning_engine/knowledge", "exports/dakota"
]

for dir_path in REQUIRED_DIRS:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Semptify - Dakota County Eviction Defense"
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "learning": "enabled"}

@app.get("/api/learning/stats")
async def learning_stats():
    """Get learning engine statistics"""
    learning_engine = get_learning_engine()
    stats = learning_engine.get_statistics()
    return JSONResponse(stats)

@app.get("/api/learning/recommendations")
async def get_recommendations(situation: str = "eviction"):
    """Get adaptive recommendations based on learned patterns"""
    learning_engine = get_learning_engine()
    recommendations = learning_engine.get_recommendations({
        "situation": situation
    })
    return JSONResponse(recommendations)

# ============================================================================
# DAKOTA COUNTY MODULE REGISTRATION (FastAPI ONLY)
# ============================================================================

print("\n" + "="*60)
print("🏛 Registering Dakota County Eviction Defense Modules")
print("="*60)

# Register Dakota County Complete Routes
try:
    from dakota_eviction_complete_routes import dakota_eviction_router
    app.include_router(dakota_eviction_router)
    print("✓ Dakota County Complete Routes registered (/dakota/eviction/*)")
except ImportError as e:
    print(f"⚠ Dakota Complete Routes: {e}")

# Register Dakota Interactive (comprehensive module with Court Companion)
try:
    from dakota_interactive_routes import router as dakota_interactive_router
    app.include_router(dakota_interactive_router)
    print("√ Dakota Interactive registered (/dakota/interactive/*)")
    print("  Features: 9 panels, Court Companion, multilingual (EN/ES/SO)")
except ImportError as e:
    print(f"? Dakota Interactive: {e}")
# Register Dakota ZIP Export (learning-enabled)
try:
    from dakota_zip_export_routes import zip_export_router
    app.include_router(zip_export_router)
    print("✓ Dakota ZIP Export registered (/dakota/export/*)")
except ImportError as e:
    print(f"⚠ Dakota ZIP Export: {e}")

# Register AI Orchestrator (learning-enabled)
try:
    from ai_orchestrator_routes_fastapi import router as ai_orchestrator_router
    app.include_router(ai_orchestrator_router)
    print("✓ AI Orchestrator registered (/ai/*)")
except ImportError as e:
    print(f"⚠ AI Orchestrator: {e}")

# Register Document Processing (learning-enabled)
try:
    from document_processing_routes import router as document_processing_router
    app.include_router(document_processing_router)
    print("✓ Document Processing registered (/document/*)")
except ImportError as e:
    print(f"⚠ Document Processing: {e}")


# Register Fraud Detection (Azure Document Intelligence)
try:
    from fraud_detection_routes import router as fraud_router
    app.include_router(fraud_router)
    print("✓ Fraud Detection registered (/api/fraud/*)")
    print("  Azure Document Intelligence: Connected")
except ImportError as e:
    print(f"⚠ Fraud Detection: {e}")
# Register Unified Calendar System
try:
    from calendar_unified_routes import router as calendar_router
    app.include_router(calendar_router)
    print("✓ Calendar System registered (/calendar/*)")
except ImportError as e:
    print(f"⚠ Calendar System: {e}")
# Register Document Upload GUI
try:
    from document_upload_gui_routes import router as doc_gui_router
    app.include_router(doc_gui_router)
    print("✓ Document Upload GUI registered (/gui/documents/*)")
except ImportError as e:
    print(f"⚠ Document GUI: {e}")
# Register Storage Dashboard
try:
    from storage_dashboard_routes import router as storage_dashboard_router
    app.include_router(storage_dashboard_router)
    print("✓ Storage Dashboard registered (/storage/dashboard)")
except ImportError as e:
    print(f"⚠ Storage Dashboard: {e}")
# Register Multi-Tier Storage System
try:
    from oauth_storage_routes import router as oauth_storage_router
    app.include_router(oauth_storage_router)
    print("✓ OAuth Storage registered (Dropbox, Google Drive)")
except ImportError as e:
    print(f"⚠ OAuth Storage: {e}")

try:
    from r2_system_storage_routes import router as r2_storage_router
    app.include_router(r2_storage_router)
    print("✓ R2 System Storage registered (Admin only)")
except ImportError as e:
    print(f"⚠ R2 Storage: {e}")

try:
    from local_role_storage_routes import router as local_storage_router
    app.include_router(local_storage_router)
    print("✓ Local Role Storage registered (Manager/Advocate/Legal)")
except ImportError as e:
    print(f"⚠ Local Storage: {e}")
# Register Justice-Grade API Pack (learning-enabled)
try:
    from justice_grade_api_routes import router as justice_api_router
    app.include_router(justice_api_router)
    from complaint_filing_router import router as complaint_filing_router
    app.include_router(complaint_filing_router)
    from vault_router import router as vault_router
    app.include_router(vault_router)
    from ledger_router import router as ledger_router
    app.include_router(ledger_router)
    from timeline_router import router as timeline_router
    app.include_router(timeline_router)
    from profile_router import router as profile_router
    app.include_router(profile_router)
    from dashboard_router import router as dashboard_router
from admin_panel_router import router as admin_panel_router
from metrics_router import router as metrics_router
from readyz_router import router as readyz_router
from learning_router import router as learning_router
from context_router import router as context_router
from calendar_hub_router import router as calendar_hub_router
from calendar_storage_router import router as calendar_storage_router
from calendar_vault_ui_router import router as calendar_vault_ui_router
from calendar_timeline_router import router as calendar_timeline_router
from tools_hub_router import router as tools_hub_router
from help_hub_router import router as help_hub_router
from legal_router import router as legal_router
from research_router import router as research_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from research_router import router as research_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from legal_router import router as legal_router
from research_router import router as research_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from research_router import router as research_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from master_admin_router import router as master_admin_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from rent_calculator_router import router as rent_calculator_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from gui_hub_router import router as gui_hub_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from library_hub_router import router as library_hub_router
from themes_router import router as themes_router
from settings_router import router as settings_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from journey_router import router as journey_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from landing_router import router as landing_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from onboarding_router import router as onboarding_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
from main_dashboard_router import router as main_dashboard_router
from unified_dashboard_router import router as unified_dashboard_router
from adaptive_gui_router import router as adaptive_gui_router
from self_building_gui_router import router as self_building_gui_router
from mc2_setup_router import router as mc2_setup_router
    app.include_router(dashboard_router)
app.include_router(admin_panel_router)
app.include_router(metrics_router)
app.include_router(readyz_router)
app.include_router(learning_router)
app.include_router(context_router)
app.include_router(calendar_hub_router)
app.include_router(calendar_storage_router)
app.include_router(calendar_vault_ui_router)
app.include_router(calendar_timeline_router)
app.include_router(tools_hub_router)
app.include_router(help_hub_router)
app.include_router(legal_router)
app.include_router(research_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(research_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(legal_router)
app.include_router(research_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(research_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(master_admin_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(rent_calculator_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(gui_hub_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(library_hub_router)
app.include_router(themes_router)
app.include_router(settings_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(journey_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(landing_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(onboarding_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
app.include_router(main_dashboard_router)
app.include_router(unified_dashboard_router)
app.include_router(adaptive_gui_router)
app.include_router(self_building_gui_router)
app.include_router(mc2_setup_router)
    print("✓ Justice-Grade API Pack registered (/api/*)")
    print("  Categories: Legal, Landlord, Document, Multilingual, Finance, Housing, Utility, Fun")
except ImportError as e:
    print(f"⚠ Justice-Grade API Pack: {e}")
    print(f"⚠ Dakota ZIP Export: {e}")

# Note: Other Dakota modules use Flask Blueprints and need conversion
# For now, we have the core modules working:
# - dakota_eviction_complete_routes (9 routes with all features)
# - dakota_zip_export_routes (PDF generation with learning)

print("="*60)
print(f"✅ Semptify application initialized with learning engine")
print(f"📊 Learning engine tracking: ALL interactions")
print(f"🔧 Note: Some modules use Flask and need FastAPI conversion")
print("="*60 + "\n")

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize learning engine and log startup"""
    learning_engine = get_learning_engine()
    print(f"🧠 Learning Engine initialized")
    print(f"📁 Knowledge directory: learning_engine/knowledge/")
    
    # Get current stats
    stats = learning_engine.get_statistics()
    print(f"📊 Current learning stats:")
    print(f"   - Total interactions: {stats['total_interactions']}")
    print(f"   - Total cases: {stats['total_cases']}")
    print(f"   - Documents generated: {stats['documents_generated']}")
    print(f"   - Patterns learned: {stats['patterns_learned']}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5000"))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)






















































