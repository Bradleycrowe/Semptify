# Semptify System Architecture & Decisions
**Last Updated:** November 9, 2025
**Purpose:** Single source of truth to prevent rebuilding existing systems

---

## 🗄️ DATABASE ARCHITECTURE

### **DECISION: SQLite (NOT JSON)**
- **File:** `user_database.py` (392 lines)
- **Location:** `security/users.db`
- **Connection:** `_get_db()` returns `sqlite3.Connection` with `row_factory = sqlite3.Row`

### **Existing Tables:**
1. **`pending_users`** - Users awaiting verification
   - Columns: user_id, first_name, last_name, email, phone, address, city, county, state, zip, verification_method, code_hash, created_at, expires_at, attempts

2. **`users`** - Verified users
   - Columns: user_id, first_name, last_name, email (UNIQUE), phone, address, city, county, state, zip, verified_at, status, last_login, login_count, location, issue_type, stage, created_at

3. **`user_learning_profiles`** - Adaptive learning system
   - Columns: user_id (FK), complexity_preference, learning_style, completed_modules (JSON array as TEXT), current_journey, journey_progress, last_activity, total_sessions

4. **`user_interactions`** - Learning system adaptation log
   - Columns: id (AUTOINCREMENT), user_id, interaction_type, ... (check lines 91-100+ for full schema)

### **⚠️ CRITICAL: All new features MUST use SQLite**
- **NO JSON files for data storage** (only config/temp files)
- Use `user_database.py` pattern: create functions like `init_delivery_tables()`, `create_delivery_job()`, etc.
- All tables go in `security/users.db`

---

## 📁 EXISTING MODULES (DO NOT RECREATE)

### **Delivery System - ALREADY EXISTS**
**Files:**
- `app-backend/delivery_api.py` - Flask API endpoints (stubs, need SQLite backend)
- `api/specs/semptify-delivery-openapi.yaml` - OpenAPI spec
- `types/semptify-delivery.d.ts` - TypeScript definitions
- `docs/README_DELIVERY.md` - Full specification

**Status:** API stubs exist, need to add SQLite backend to `user_database.py`

**Tables needed:**
```sql
CREATE TABLE deliveries (
    id TEXT PRIMARY KEY,
    case_id TEXT,
    user_id TEXT,
    created_by TEXT,
    created_at TEXT,
    status TEXT,
    priority_order TEXT, -- JSON array as TEXT
    metadata TEXT, -- JSON as TEXT
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE delivery_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id TEXT,
    method_id TEXT,
    method_type TEXT, -- EMAIL, USPS, CERTIFIED, HAND, COURIER
    recipient_name TEXT,
    recipient_contact TEXT, -- JSON as TEXT
    instructions TEXT,
    status TEXT,
    delivered_at TEXT,
    confirmed_by TEXT,
    failure_reason TEXT,
    proof_file_ids TEXT, -- JSON array as TEXT
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
);

CREATE TABLE delivery_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id TEXT,
    method_id TEXT,
    attempt_at TEXT,
    actor TEXT,
    provider_response TEXT,
    tracking_number TEXT,
    proof_file_ids TEXT, -- JSON array as TEXT
    notes TEXT,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
);

CREATE TABLE delivery_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id TEXT,
    event TEXT, -- DELIVERY_CREATED, DELIVERY_ATTEMPTED, DELIVERY_CONFIRMED, DELIVERY_FAILED
    timestamp TEXT,
    actor TEXT,
    details TEXT, -- JSON as TEXT
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
);
```

### **Calendar/Timeline - JUST CREATED (needs SQLite conversion)**
**Files:**
- `calendar_timeline.py` - NEW (uses JSON, needs SQLite)
- `calendar_timeline_routes.py` - NEW Flask routes
- `templates/calendar_timeline.html` - NEW UI
- `calendar_api.py` - OLD API (already registered in Semptify.py)

**Status:** New version uses JSON file `data/timeline_events.json` - NEEDS to be converted to SQLite

**Tables needed:**
```sql
CREATE TABLE timeline_events (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    type TEXT, -- rent_payment, court_date, deadline, notice_received, inspection, maintenance_request, lease_milestone
    date TEXT,
    title TEXT,
    description TEXT,
    amount REAL,
    status TEXT, -- upcoming, completed, missed, cancelled
    metadata TEXT, -- JSON as TEXT
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### **OCR System - JUST CREATED (good as-is)**
**File:** `ocr_service.py`
**Status:** ✅ Complete, no database needed (processes files on-demand)
**Dependencies:** pytesseract, Pillow, PyPDF2 (added to requirements.txt)

### **Responsive GUI Modes - JUST CREATED**
**File:** `static/css/responsive_modes.css`
**Status:** ✅ Complete CSS with mobile (<768px), desktop (768-1920px), TV (>1920px) breakpoints

---

## 🔧 FLASK APP STRUCTURE

### **Main App:** `Semptify.py` (1920+ lines)
**Registered Blueprints:**
1. `ledger_calendar_bp` - Ledger calendar
2. `data_flow_bp` - Data flow
3. `ledger_tracking_bp` - Ledger tracking
4. `ledger_admin_bp` - Admin ledger
5. `av_routes_bp` - AV routes
6. `learning_bp` - Learning system
7. `learning_module_bp` - Preliminary learning module
8. `journey_bp` - Tenant journey
9. `route_discovery_bp` - Route discovery
10. `complaint_filing_bp` - Complaint filing
11. `housing_programs_bp` - Housing programs
12. `complaint_templates` - Complaint templates
13. `law_notes_actions` - Law notes actions
14. `evidence_packet_builder` - Evidence packet builder
15. `mn_check` - MN check
16. `attorney_trail` - Attorney trail
17. `office_bp` - Office
18. `comm_suite_bp` - Communication suite
19. `calendar_api_bp` - Calendar API (OLD)
20. `calendar_bp` - Calendar timeline (NEW - just added line ~153)
21. `veeper_bp` - Veeper

### **Runtime Directories (created at startup):**
- `uploads/` - File uploads
- `logs/` - Application logs
- `copilot_sync/` - Copilot sync
- `final_notices/` - Final notices
- `security/` - Security files, tokens, users.db

### **Logging:**
- `logs/init.log` - Initialization log
- `logs/events.log` - JSON event log (rotated)

---

## 🔐 SECURITY ARCHITECTURE

### **Security Modes:**
- `SECURITY_MODE=open` - Allow access, log events
- `SECURITY_MODE=enforced` - Require admin tokens, enforce CSRF

### **Admin Authentication:**
- **Tokens:** `security/admin_tokens.json` (hashed, multi-token support)
- **Legacy:** `ADMIN_TOKEN` env var (fallback)
- **Break-glass:** Create `security/breakglass.flag` file

### **CSRF Protection:**
- Enforced in `enforced` mode only
- Function: `_get_or_create_csrf_token()`
- Include in forms: `<input type="hidden" name="csrf_token" value="{{ csrf_token }}">`

### **Rate Limiting:**
- Sliding window via `ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX`
- Returns 429 with `Retry-After` header

---

## 📊 OBSERVABILITY

### **Metrics Endpoint:** `/metrics`
**Counters:**
- `requests_total`
- `admin_requests_total`
- `admin_actions_total`
- `errors_total`
- `releases_total`
- `rate_limited_total`
- `breakglass_used_total`
- `token_rotations_total`

**Gauges:**
- `uptime_seconds`

### **Health Checks:**
- `/health` - Basic health
- `/healthz` - Kubernetes health
- `/readyz` - Readiness check (verifies dirs writable, tokens/users load)

---

## 📦 DEPENDENCIES (requirements.txt)

**Core:**
- Flask>=3.1.2
- waitress>=2.1.2
- requests>=2.31.0
- pytest>=8.2.0

**OCR (new):**
- pytesseract>=0.3.10
- Pillow>=10.0.0
- PyPDF2>=3.0.0

**Calendar (new):**
- icalendar>=5.0.0
- reportlab>=4.0.0

**Existing:**
- beautifulsoup4>=4.12.3
- PyQt5>=5.15.11
- pyspellchecker>=0.8.1
- boto3>=1.34.0
- cryptography>=41.0.0

---

## 🚀 DEPLOYMENT

### **Render Service:**
- **Service ID:** `srv-d46m65pr0fns73fpp9e0`
- **API Key:** `rnd_7Luhbut1oa8ogUQnIHzVdBUKRioz`
- **Issue:** Auto-deploy not triggering on git push (webhook broken)
- **Workaround:** Manual deploy via API:
  ```bash
  curl -X POST "https://api.render.com/v1/services/srv-d46m65pr0fns73fpp9e0/deploys" \
    -H "Authorization: Bearer rnd_7Luhbut1oa8ogUQnIHzVdBUKRioz"
  ```

### **Production Run:**
- Dev: `python Semptify.py`
- Prod: `python run_prod.py` (waitress)
- HTTPS dev: `python run_dev_ssl.py` (requires `security/dev-local.crt|key`)

---

## ⚠️ CRITICAL RULES TO PREVENT REWORK

### **1. CHECK EXISTING FILES FIRST**
Before creating ANY new module, search:
```bash
# Search for similar files
file_search(**/<keyword>*.py)
grep_search(query="class <Feature>|def <feature>", isRegexp=true)
```

### **2. USE SQLite FOR ALL DATA**
- ✅ DO: Add tables to `user_database.py`, use `security/users.db`
- ❌ DON'T: Create JSON files in `data/` directory
- Exception: Config files, temp files only

### **3. FOLLOW EXISTING PATTERNS**
- Database functions in `user_database.py`
- Flask blueprints registered in `Semptify.py` lines 60-160
- Templates in `templates/`
- Static assets in `static/css/`, `static/js/`

### **4. UPDATE THIS FILE**
When making architectural decisions:
1. Update this `SYSTEM_ARCHITECTURE.md` immediately
2. Document table schemas
3. Note which files integrate where
4. Record decisions and reasons

### **5. CONSULT INSTRUCTION FILES**
- `.github/copilot-instructions.md` - Project conventions
- `docs/README_DELIVERY.md` - Delivery spec
- Other `docs/README_*.md` files for feature specs

---

## 📋 TODO: IMMEDIATE FIXES NEEDED

### **1. Convert calendar_timeline.py to SQLite**
- Remove JSON file usage
- Add `timeline_events` table to `user_database.py`
- Update `calendar_timeline.py` to use SQLite

### **2. Implement delivery system in SQLite**
- Add 4 delivery tables to `user_database.py` (see schema above)
- Update `app-backend/delivery_api.py` to use SQLite backend
- Remove `delivery_system.py` (JSON-based, wrong approach)

### **3. Admin Manual Generation**
- Scan 338 .md files discovered
- Generate `docs/admin_manual/INDEX.md`
- Compile `docs/admin_manual/ADMIN_MANUAL.md`

---

## 📝 DECISION LOG

### **November 9, 2025**
1. ✅ **SQLite confirmed as primary database** - All user data in `security/users.db`
2. ✅ **Calendar timeline system created** - Needs SQLite conversion
3. ✅ **OCR service created** - Using pytesseract, no DB needed
4. ✅ **Responsive CSS created** - Mobile/Desktop/TV modes in one file
5. ⚠️ **Delivery system created with JSON** - WRONG, needs SQLite rewrite
6. ⚠️ **Calendar created with JSON** - WRONG, needs SQLite rewrite

### **Action Items:**
- [ ] Convert calendar_timeline.py to SQLite
- [ ] Add delivery tables to user_database.py
- [ ] Update delivery_api.py to use SQLite
- [ ] Fix Render auto-deploy webhook
- [ ] Generate admin manual from 338 .md files

### **November 9, 2025 - Evening Update**
1. ✅ **Learning Dashboard Mobile-First UI Created**
   - Route: `/learning-dashboard` registered in Semptify.py
   - Template: `templates/learning_dashboard.html` (768 lines, already existed)
   - API: `learning_dashboard_api.py` with 8 endpoints
   - Blueprint: `learning_dashboard_bp` registered at `/api/learning/*`

2. ✅ **Learning Dashboard API Endpoints:**
   - `GET /api/learning/suggestions` - Next action suggestions
   - `GET /api/learning/intensity` - Current intensity level
   - `GET /api/learning/progress` - User progress tracking
   - `GET /api/learning/curiosity/questions` - What system is learning
   - `POST /api/learning/curiosity/ask` - User asks questions
   - `POST /api/learning/track` - Track interactions
   - `GET /api/learning/knowledge` - Access knowledge base
   - `GET /api/learning/stats` - System statistics

3. ✅ **Mobile-First Design:**
   - Touch-friendly 44px+ targets
   - Bottom navigation bar
   - Floating action button for questions
   - Responsive: works on mobile, tablet, desktop
   - Shows intensity level visually
   - Displays what system is researching (Curiosity Engine)
   - Smart suggestions based on learned patterns

---

## 🆘 WHEN YOU LOSE TRACK

**ASK THESE QUESTIONS:**
1. "Does this feature already exist?" → Search files first
2. "Should this use SQLite?" → YES (unless config/temp)
3. "Is there a spec file?" → Check `docs/README_*.md`
4. "Is this registered in Semptify.py?" → Check lines 60-160
5. "Did we decide this before?" → Read this file's Decision Log

**READ THESE FILES:**
1. `SYSTEM_ARCHITECTURE.md` (this file) - Overall structure
2. `.github/copilot-instructions.md` - Project conventions
3. `user_database.py` - Database schema reference
4. `Semptify.py` lines 1-200 - App initialization and blueprints

---

**🎯 GOLDEN RULE: When in doubt, search existing files and update this document.**
