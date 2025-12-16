"""
Semptify FastAPI Application
Storage-as-Identity - No signup, no tracking, no data breach liability
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import time

# Load .env file if exists
def load_env():
    for env_file in ['.env', '.env.production', '.env.local']:
        if os.path.exists(env_file):
            print(f"[Semptify] Loading {env_file}")
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key.strip(), value.strip())
            break

load_env()

# Create runtime directories
RUNTIME_DIRS = ['uploads', 'logs', 'uploads/user_storage', 'static', 'data']
for d in RUNTIME_DIRS:
    os.makedirs(d, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage_type = os.environ.get('STORAGE_TYPE', 'local')
    r2_configured = bool(os.environ.get('R2_ACCESS_KEY'))
    print(f"[Semptify] Starting - Storage: {storage_type}, R2: {'Yes' if r2_configured else 'No'}")
    yield
    print("[Semptify] Shutting down")

app = FastAPI(
    title="Semptify",
    description="Tenant Rights Platform - Storage-as-Identity",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - allow all for now (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Response-Time"] = f"{(time.time()-start)*1000:.1f}ms"
    return response

# Health endpoints
@app.get("/healthz")
async def health():
    return {"status": "ok", "model": "storage-as-identity"}

@app.get("/readyz")
async def ready():
    r2_ok = bool(os.environ.get('R2_ACCESS_KEY'))
    return {
        "status": "ready" if r2_ok else "degraded",
        "storage": os.environ.get('STORAGE_TYPE', 'local'),
        "r2_configured": r2_ok
    }

@app.get("/")
async def root():
    return {
        "service": "Semptify",
        "version": "2.0.0",
        "model": "Storage-as-Identity",
        "docs": "/docs",
        "access": "/static/access.html"
    }

# =============================================================================
# ROUTER REGISTRATION
# =============================================================================

def safe_register(module_name: str, prefix: str, tags: list):
    """Safely register a router with error handling"""
    try:
        module = __import__(module_name, fromlist=['router'])
        router = getattr(module, 'router', None)
        if router:
            app.include_router(router, prefix=prefix, tags=tags)
            print(f"[OK] {module_name}")
            return True
    except Exception as e:
        print(f"[SKIP] {module_name}: {e}")
    return False

# Core Storage (from routers package)
try:
    from routers.storage import router as storage_router
    app.include_router(storage_router, prefix="/api/storage", tags=["storage"])
    print("[OK] routers.storage")
except Exception as e:
    print(f"[SKIP] routers.storage: {e}")

# === HIGH PRIORITY - Core User Features ===
safe_register("vault_router", "/api/vault", ["vault"])
safe_register("ledger_router", "/api/ledger", ["ledger"])
safe_register("timeline_router", "/api/timeline", ["timeline"])
safe_register("profile_router", "/api/profile", ["profile"])
safe_register("dashboard_router", "/api/dashboard", ["dashboard"])
safe_register("complaint_filing_router", "/api/complaint", ["complaint"])

# === MEDIUM PRIORITY - Admin & Tools ===
safe_register("admin_panel_router", "/api/admin", ["admin"])
safe_register("master_admin_router", "/admin", ["admin"])
safe_register("learning_router", "/api/learning", ["learning"])
safe_register("metrics_router", "/api/metrics", ["metrics"])
safe_register("readyz_router", "/api/ready", ["health"])
safe_register("settings_router", "/api/settings", ["settings"])

# === GUI & UI Routers ===
safe_register("landing_router", "/landing", ["gui"])
safe_register("gui_hub_router", "/gui", ["gui"])
safe_register("adaptive_gui_router", "/api/gui/adaptive", ["gui"])
safe_register("self_building_gui_router", "/api/gui/self-building", ["gui"])
safe_register("unified_dashboard_router", "/api/unified-dashboard", ["dashboard"])
safe_register("main_dashboard_router", "/dashboard", ["dashboard"])
safe_register("onboarding_router", "/api/onboarding", ["onboarding"])
safe_register("journey_router", "/api/journey", ["journey"])

# === Calendar & Timeline ===
safe_register("calendar_hub_router", "/api/calendar", ["calendar"])
safe_register("calendar_storage_router", "/api/calendar/storage", ["calendar"])
safe_register("calendar_timeline_router", "/api/calendar/timeline", ["calendar"])
safe_register("calendar_vault_ui_router", "/api/calendar/vault", ["calendar"])

# === Tools & Utilities ===
safe_register("tools_hub_router", "/api/tools", ["tools"])
safe_register("rent_calculator_router", "/api/rent-calculator", ["tools"])
safe_register("legal_router", "/api/legal", ["legal"])
safe_register("research_router", "/api/research", ["research"])
safe_register("context_router", "/api/context", ["context"])

# === Help & Library ===
safe_register("help_hub_router", "/api/help", ["help"])
safe_register("library_hub_router", "/api/library", ["library"])

# === Themes & Misc ===
safe_register("themes_router", "/api/themes", ["themes"])
safe_register("mc2_setup_router", "/api/mc2", ["setup"])

print("\n[Semptify] Router registration complete!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
