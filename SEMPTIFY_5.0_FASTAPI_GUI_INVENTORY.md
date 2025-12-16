# Semptify 5.0 - Full FastAPI & GUI Inventory Assessment

**Generated:** November 30, 2025  
**Project:** Semptify - Tenant Rights Protection Platform  
**Architecture:** Hybrid Flask/FastAPI with multiple GUI interfaces

---

## 📊 Executive Summary

| Category | Count |
|----------|-------|
| **Total Python Files** | 339 |
| **FastAPI Router Files** | 33 |
| **Flask Route Files** | 75+ |
| **HTML Templates (Total)** | 236 |
| **FastAPI-Specific Templates** | 18 |
| **GUI Modules** | 16 |
| **Static JS Files** | 11 |

---

## 🏗️ Application Entry Points

### Primary Entry Points
| File | Size | Framework | Purpose |
|------|------|-----------|---------|
| `Semptify.py` | 17.7 KB | Flask | Main Flask application, blueprint registration |
| `main.py` | 6.1 KB | FastAPI | FastAPI application with router registration |
| `semptify_app.py` | **650.5 KB** | FastAPI | Large FastAPI app with inline routes |
| `semptify_fastapi.py` | 13.7 KB | FastAPI | FastAPI version with basic routes |
| `semptify_complete.py` | 48.6 KB | FastAPI | Complete FastAPI integration |
| `semptify_complete_fixed.py` | 47.6 KB | FastAPI | Fixed version of complete integration |

### Production Runners
| File | Purpose |
|------|---------|
| `run_prod.py` | Waitress production server |
| `run_dev_ssl.py` | HTTPS development with self-signed certs |
| `SemptifyStartApp.py` | GUI launcher with production server spawn |

---

## 🚀 FastAPI Router Inventory (33 Routers)

### Core Application Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `vault_router.py` | 18.3 KB | `/api/vault` | Document vault with encryption |
| `ledger_router.py` | 8.0 KB | `/api/ledger` | Rent payment tracking |
| `complaint_filing_router.py` | 13.3 KB | `/api/complaint` | Complaint wizard system |
| `profile_router.py` | 4.6 KB | `/api/profile` | Client/case profile management |
| `dashboard_router.py` | 2.2 KB | `/api/dashboard` | Dynamic cell-based dashboard |
| `timeline_router.py` | 2.6 KB | `/api/timeline` | Deadline intelligence |

### Admin & System Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `admin_panel_router.py` | 10.0 KB | `/api/admin` | System configuration |
| `master_admin_router.py` | 1.1 KB | `/admin` | Master admin interface |
| `learning_router.py` | 9.2 KB | `/api/learning` | Adaptive learning engine |
| `metrics_router.py` | 0.6 KB | `/api/metrics` | Prometheus metrics |
| `readyz_router.py` | 1.3 KB | `/api/ready` | Health/readiness checks |
| `settings_router.py` | 2.2 KB | `/api/settings` | User preferences |

### GUI & UI Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `gui_hub_router.py` | 1.9 KB | `/gui` | Main GUI hub |
| `landing_router.py` | 4.4 KB | `/landing` | Landing/welcome page |
| `adaptive_gui_router.py` | 7.6 KB | `/api/gui/adaptive` | Adaptive interface system |
| `self_building_gui_router.py` | 11.9 KB | `/api/gui/self-building` | Self-constructing GUI |
| `unified_dashboard_router.py` | 1.8 KB | `/api/unified-dashboard` | 5-role dashboard |
| `main_dashboard_router.py` | 2.6 KB | `/dashboard` | Primary dashboard routes |
| `onboarding_router.py` | 4.2 KB | `/api/onboarding` | User onboarding flow |
| `journey_router.py` | 3.2 KB | `/api/journey` | User journey tracking |
| `themes_router.py` | 2.3 KB | `/api/themes` | Dashboard theme variants |

### Calendar & Timeline Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `calendar_hub_router.py` | 0.8 KB | `/api/calendar` | Unified calendar page |
| `calendar_storage_router.py` | 6.3 KB | `/api/calendar/storage` | Calendar with vault storage |
| `calendar_timeline_router.py` | 7.7 KB | `/api/calendar/timeline` | Timeline events & rent ledger |
| `calendar_vault_ui_router.py` | 3.0 KB | `/api/calendar/vault` | Timeline assistant dashboard |

### Tools & Utilities Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `tools_hub_router.py` | 0.7 KB | `/api/tools` | AI & utilities hub |
| `rent_calculator_router.py` | 1.2 KB | `/api/rent-calculator` | Rent calculation tools |
| `research_router.py` | 0.9 KB | `/api/research` | Landlord/property lookup |
| `context_router.py` | 2.0 KB | `/api/context` | Document perspective analysis |
| `legal_router.py` | 0.8 KB | `/api/legal` | Privacy and terms pages |

### Help & Library Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `help_hub_router.py` | 0.7 KB | `/api/help` | Crisis resources |
| `library_hub_router.py` | 1.5 KB | `/api/library` | Legal resource library |

### Specialized Routers
| Router File | Size | Prefix | Description |
|-------------|------|--------|-------------|
| `mc2_setup_router.py` | 6.8 KB | `/api/mc2` | MC2 setup wizard |

---

## 🎨 GUI Module Inventory (16 Modules)

### Desktop GUI Applications (Tkinter/PyQt)
| File | Size | Framework | Description |
|------|------|-----------|-------------|
| `SemptifyAppGUI.py` | 29.0 KB | PyQt5 | Full desktop application |
| `semptify_modern_gui.py` | 33.9 KB | Tkinter | Modern web-style desktop GUI |
| `semptify_standalone_gui.py` | 8.0 KB | Tkinter | No-Flask standalone GUI |
| `SemptifyCleanupGUI.py` | 1.8 KB | Tkinter | Cleanup utility GUI |

### Web GUI Route Modules
| File | Size | Description |
|------|------|-------------|
| `gui_hub_routes.py` | 0.8 KB | Flask GUI hub routes |
| `brad_gui_routes.py` | 12.3 KB | Brad GUI interface routes |
| `modern_gui_routes.py` | 2.9 KB | Modern GUI routes |
| `document_upload_gui_routes.py` | 5.7 KB | Document upload interface |
| `emergency_gui_routes.py` | 0.7 KB | Emergency mode GUI |

### GUI Support Modules
| File | Size | Description |
|------|------|-------------|
| `gui_assessment.py` | 6.0 KB | GUI state assessment |
| `gui_components.py` | 13.5 KB | Reusable GUI components |
| `adaptive_gui_router.py` | 7.6 KB | Adaptive interface logic |
| `self_building_gui_router.py` | 11.9 KB | Self-constructing GUI logic |

---

## 📁 Template Directory Structure

### Root Templates (159 files)
```
templates/
├── fastapi_*.html (18 files) - FastAPI-specific templates
├── dakota_*.html (6 files) - Dakota County defense
├── base*.html - Base layouts
├── index.html - Main landing
└── [150+ other templates]
```

### Subdirectories (77 additional templates)
| Directory | Templates | Purpose |
|-----------|-----------|---------|
| `admin/` | Various | Admin panel pages |
| `ai/` | Various | AI interface templates |
| `brad_gui/` | 6 | Brad GUI dashboards |
| `calendar_vault/` | 3 | Calendar/vault interface |
| `components/` | Various | Reusable components |
| `doc_explorer/` | Various | Document explorer |
| `includes/` | Various | Template partials |
| `law_notes/` | Various | Legal note templates |
| `ledger/` | Various | Ledger interface |
| `legal/` | Various | Legal pages |
| `main_dashboard/` | 1 | Main dashboard home |
| `modern_gui/` | 2 | Modern GUI templates |
| `modules/` | Various | Module templates |
| `pages/` | Various | Static pages |
| `storage_setup/` | Various | Storage setup wizard |
| `themes/` | Various | Theme templates |

### FastAPI-Specific Templates (18 files)
```
fastapi_404.html          fastapi_housing.html
fastapi_ai.html           fastapi_hub.html
fastapi_brad.html         fastapi_jurisdiction.html
fastapi_calendar.html     fastapi_ledger.html
fastapi_complaint.html    fastapi_maintenance.html
fastapi_dakota.html       fastapi_timeline.html
fastapi_dakota_eviction.html  fastapi_vault.html
fastapi_demo.html         
fastapi_evidence.html     
fastapi_help.html         
fastapi_home.html         
```

---

## 🏛️ Dakota County Module System

### Route Files
| File | Size | Description |
|------|------|-------------|
| `dakota_interactive_routes.py` | 31.5 KB | Interactive defense system |
| `dakota_full_interactive_routes.py` | 31.5 KB | Full interactive with Court Companion |
| `dakota_zip_export_routes.py` | 15.2 KB | Learning-enabled ZIP export |
| `dakota_eviction_complete_routes.py` | 9.7 KB | Complete eviction defense |
| `dakota_learning_routes.py` | 7.4 KB | Learning integration |
| `dakota_eviction_library_routes.py` | 4.0 KB | Defense library |
| `dakota_routes_complete.py` | 3.6 KB | Complete route set |
| `dakota_court_routes.py` | 2.6 KB | Court-specific routes |
| `dakota_routes_module.py` | 1.4 KB | Module routes |

### Features
- 9 interactive panels
- Court Companion feature
- Multilingual support (EN/ES/SO)
- Learning engine integration
- ZIP export for court packets

---

## 📦 Router Package Structure

### `/routers` Package
```
routers/
├── __init__.py
├── storage.py (17.0 KB) - Core storage API
├── session.py (10.6 KB) - Session management
├── oauth.py (5.8 KB) - OAuth integration
└── vault.py (5.1 KB) - Vault operations
```

### `/blueprints` Package
```
blueprints/
├── __init__.py
├── auth_bp.py (7.2 KB) - Authentication
├── ai_bp.py (3.9 KB) - AI features
└── vault_bp.py (0.5 KB) - Vault blueprint
```

---

## 🎯 Static Assets Inventory

### Directory Structure
```
static/
├── admin/          - Admin panel assets
├── css/            - Stylesheets
├── images/         - Image assets
├── js/             - JavaScript modules
└── pages/          - Static HTML pages
```

### JavaScript Modules (11 files)
| File | Purpose |
|------|---------|
| `app.js` | Main application logic |
| `spa.js` | Single Page Application router |
| `auth-propagate.js` | Token propagation |
| `brad_metrics.js` | Brad GUI metrics |
| `brad_storage.js` | Brad storage integration |
| `brad_timeline.js` | Brad timeline widget |
| `evidence-collector.js` | Evidence collection |
| `evidence-system.js` | Evidence management |
| `help-panel.js` | Help panel widget |
| `service-worker.js` | PWA service worker |
| `timeline_widget.js` | Timeline widget |

### Static HTML Files
```
static/
├── access.html          - Access point
├── index.html           - Static index
├── mobile_app.html      - Mobile app page
├── presentation_mode.html - Presentation view
└── timeline.html        - Timeline standalone
```

---

## 🔄 Application Architecture

### Dual-Framework Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Semptify 5.0                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────────┐     │
│  │   Flask (Primary)    │    │   FastAPI (Modern)       │    │
│  │   Semptify.py        │    │   main.py / semptify_app │    │
│  │   75+ Blueprints     │    │   33 Routers             │    │
│  │   Port 5000 (dev)    │    │   Port 8000 (API)        │    │
│  └─────────────────────┘    └─────────────────────────┘     │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Shared Components                     │ │
│  │  • 236 HTML Templates                                   │ │
│  │  • Learning Engine (LearningMiddleware)                 │ │
│  │  • Security Module (tokens, CSRF, rate-limiting)        │ │
│  │  • SQLite Database (user_database.py)                   │ │
│  │  • Document Vault (uploads/vault/)                      │ │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Desktop GUIs                          │ │
│  │  • SemptifyAppGUI.py (PyQt5)                            │ │
│  │  • semptify_modern_gui.py (Tkinter)                     │ │
│  │  • semptify_standalone_gui.py (Tkinter)                 │ │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Integration Points
1. **Learning Engine** - Middleware that observes all interactions
2. **Security Module** - Shared tokens, CSRF, rate limiting
3. **Vault System** - Document storage with encryption
4. **Timeline System** - Deadline tracking across all GUIs

---

## ⚠️ Issues & Recommendations

### 1. Code Duplication
- `semptify_app.py` is 650KB with massive duplication (GUI router registered 100+ times)
- Multiple Dakota route files with similar functionality
- Consider refactoring to single source of truth

### 2. Framework Fragmentation
- Flask and FastAPI running in parallel
- Some routes exist in both frameworks
- Recommend: Choose one framework or create clear separation

### 3. Large Files
| File | Size | Recommendation |
|------|------|----------------|
| `semptify_app.py` | 650 KB | Split into modules |
| `semptify_complete.py` | 48 KB | Refactor inline routes |
| `dakota_interactive_routes.py` | 31 KB | Break into sub-modules |

### 4. Template Management
- 236 templates with potential duplicates
- Some templates prefix with `fastapi_` but could be unified
- Consider: Template inheritance cleanup

### 5. Dead Code
- Multiple backup files (`.bak`, `.BROKEN_BACKUP.py`, `.ORIGINAL.py`)
- Should be cleaned up or moved to `/archive`

---

## 📈 Quick Stats

```
Total Python Files:               339
FastAPI Router Endpoints:         116 (in router files)
Flask Route Endpoints:            505 (in routes files)
Main App Blueprints:              39 registrations
Total HTML Templates:             236
GUI Interfaces:                   5+ distinct interfaces
Database Tables:                  3-5 (users, tokens, timeline)
Active Features:                  20+ major features
```

---

## 🛠️ Development Commands

```powershell
# Run Flask app
python Semptify.py

# Run FastAPI app
python main.py
# or
uvicorn main:app --reload --port 8000

# Run tests
python -m pytest -q

# Run production
python run_prod.py
```

---

*This inventory was generated by analyzing the Semptify 5.0 codebase.*
