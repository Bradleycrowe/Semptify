# Semptify Core Modules & Engines

## Single-User Mode Configuration
- **SECURITY_MODE**: Set to `open` in `.env` (no user login required)
- **Profile System**: Manage multiple client/case profiles via `/profiles`
- **Active Profile**: All data isolated per profile (stored in `data/profiles/<profile_id>/`)

---

## Core Functional Modules

### �� Document Management
- **Vault** (`vault_bp`) - Secure document storage with notary certificates
- **Doc Explorer** (`doc_explorer_bp`) - Browse and search uploaded documents
- **Evidence Packet Builder** (`evidence_packet_builder`) - Create court evidence packets
- **Library** (`library_bp`) - Legal document templates & resources

### ⚖️ Legal Tools
- **Complaint Filing** (`complaint_filing_bp`) - Multi-step wizard for court complaints
- **Legal Routes** (`legal_bp`) - Legal form generation & guidance
- **Attorney Finder** (`attorney_trail`) - Find and track attorney contacts
- **Housing Programs** (`housing_programs_bp`) - Tenant assistance programs
- **MN Check** (`mn_check`) - Minnesota-specific legal checks

### 💰 Financial Tracking
- **Ledger** (`ledger_routes_bp`) - Rent payment tracking
- **Ledger Admin** (`ledger_admin_bp`) - Payment history management
- **Ledger Calendar** (`ledger_calendar_bp`) - Payment schedule integration
- **Rent Calculator** (`rent_calculator_routes`) - Calculate rent adjustments

### 📅 Calendar & Timeline
- **Calendar Master** (`calendar_master_bp`) - Central calendar system
- **Calendar API** (`calendar_api_bp`) - Calendar data endpoints
- **Calendar Timeline** (`calendar_timeline_bp`) - Event timeline view
- **Calendar Vault UI** (`calendar_vault_ui_bp`) - Calendar-document bridge
- **AV Routes** (`av_routes_bp`) - Audio/visual event capture

### 🧠 Learning & AI
- **Learning Dashboard** (`learning_dashboard_bp`) - Adaptive learning interface
- **Learning Routes** (`learning_bp`) - Learning pattern management
- **Preliminary Learning** (`learning_module_bp`) - Info acquisition module
- **Curiosity API** - Self-learning reasoning engine
- **Ollama Routes** (`ollama_bp`) - Local LLM integration

### 📊 Dashboard & Navigation
- **Main Dashboard** (`main_dashboard_bp`) - Primary interface
- **Dashboard API** (`dashboard_api_bp`) - Dynamic cell-based widgets
- **Journey Routes** (`journey_bp`) - User journey tracking
- **Route Discovery** (`route_discovery_bp`) - Auto-discover all routes

### 🛠️ System & Admin
- **Admin** (`admin_bp`) - System administration
- **Feature Admin** (`feature_admin_routes`) - Feature flags
- **Themes** (`themes_bp`) - UI theme management
- **Maintenance** (`maintenance_bp`) - System maintenance tools
- **Migration** (`migration_bp`) - Data migration utilities

### 📱 Communication & Collaboration
- **Office Suite** (`office_bp`) - Communication tools
- **Communication Suite** (`comm_suite_bp`) - Message templates
- **Tenant Narrative** (`tenant_narrative_bp`) - Story documentation
- **Public Exposure** (`public_exposure_bp`) - Share case publicly (opt-in)

### 🗄️ Storage & Data
- **Storage Setup** (`storage_setup_bp`) - Configure storage backends
- **Storage Autologin** (`storage_autologin_bp`) - Auto-auth for storage
- **Data Flow** (`data_flow_bp`) - Data pipeline management
- **Packet Builder** (`packet_builder_bp`) - Build data packets

### 🧪 Development & Testing
- **Demo Routes** (`demo_bp`) - Feature demonstrations
- **Seed API** (`seed_api_bp`) - Seed test data
- **Onboarding** (`onboarding_bp`) - First-time user setup

---

## Engines (Business Logic)

### Core Engines
- `complaint_filing_engine.py` - Court complaint generation logic
- `reasoning_engine_simple.py` - Simple reasoning/inference
- `curiosity_reasoning_bridge.py` - Curiosity-based learning
- `doc_explorer_engine.py` - Document search/indexing
- `validated_engine_generator.py` - Engine validation framework
- `engine_generator.py` - Dynamic engine creation

### Specialized Engines
- `calendar_api.py` - Calendar data processing
- `calendar_master.py` - Calendar coordination
- `ledger_*.py` - Financial calculation engines
- `contextual_help.py` - Context-aware help system
- `adaptive_registration.py` - Smart registration flows

---

## How to Use Profiles

1. **Access Profile Manager**: Navigate to `/profiles`
2. **Create Profile**: Click "+" to add new client/case (e.g., "Smith Property Case")
3. **Switch Profiles**: Click "Switch to This" on any profile card
4. **Isolated Data**: Each profile has separate vault, ledger, timeline, etc.

---

## Disabling Multi-User Features

### Already Disabled
- Registration blueprint commented out in `Semptify.py`
- `SECURITY_MODE=open` bypasses all user auth

### To Fully Remove (Optional)
1. Comment out `auth_bp` registration in `Semptify.py`
2. Remove `@require_login` decorators from routes
3. Delete `user_database.py` dependencies

---

## Module Status Legend
- ✅ **Active**: Registered and functional
- ⚠️ **Commented**: Code exists but disabled
- 📦 **Standalone**: Utility module (no blueprint)

---

## Quick Start Single-User Mode

```powershell
# Set single-user mode
Set-Content -Path ".env" -Value "SECURITY_MODE=open`nFLASK_SECRET=dev_secret_key_123"

# Initialize profiles
.\.venv\Scripts\python.exe -c "from profile_manager import init_profiles; init_profiles(); print('✓ Profiles initialized')"

# Run app
.\.venv\Scripts\python.exe Semptify.py
```

Access: `http://localhost:5000` → `/profiles` to manage cases
