# Semptify Route Inventory & User Flow Analysis
**Generated:** November 11, 2025  
**Purpose:** Complete inventory of all routes, user flows, and system connections

---

## 🎯 NEW USER FLOW (From Landing → First Dashboard)

### Step 1: Landing Page
- **Route:** `/` (Semptify.py line 244)
- **Template:** Unknown - need to check what renders
- **Links expected:**
  - Register button → `/register`
  - Login link → `/login`
  - Learn more → `/about`, `/how-it-works`, `/features`

### Step 2: Registration
- **Route:** `/register` (auth_bp.py line 20) - GET + POST
- **Template:** Should have registration form
- **Process:**
  1. User fills form (email, name, password)
  2. POST to `/register`
  3. Sends verification code
  4. Redirects to → `/verify`

### Step 3: Verification
- **Route:** `/verify` (auth_bp.py line 98 GET, line 112 POST)
- **Process:**
  1. Shows verification code input
  2. POST code to `/verify`
  3. On success → `/dashboard` (first login)
- **Backup:** `/resend-code` (POST, line 143)

### Step 4: First Login Dashboard
- **Route:** `/dashboard` (Semptify.py line 357)
- **Template:** Should show dashboard_welcome.html (with smart suggestions)
- **Features:**
  - Smart suggestions widget
  - Quick steps (expandable)
  - Main navigation to all features

---

## 🔁 RETURNING USER FLOW

### Login
- **Route:** `/login` (auth_bp.py line 75) - GET + POST
- **Alt routes:**
  - `/signin` (Semptify.py line 280) - duplicate?
  - `/test-login` (line 262) - test route?
- **Process:**
  1. Enter email/password
  2. POST to `/login`
  3. Success → `/dashboard`

### Dashboard
- **Route:** `/dashboard` (Semptify.py line 357)
- **API:** `/api/dashboard` (line 383) - GET dashboard data
- **Update:** `/api/dashboard/update` (POST, line 434)
- **Alt views:**
  - `/dashboard-grid` (line 257)
  - `/dashboard-old` (line 692)

### Main Features Access
From dashboard, user can navigate to:
1. **Document Vault** → `/vault`
2. **Calendar/Timeline** → `/calendar-timeline` or `/ledger-calendar`
3. **Resources** → `/resources`
4. **Tools** → `/tools`
5. **Learning** → `/learning` or `/learning-dashboard`
6. **Help** → `/help`

---

## 📁 VAULT SYSTEM (Document Storage)

### Main Vault
- **Route:** `/vault` (MULTIPLE definitions found - ISSUE!)
  - Semptify.py line 611 (commented out?)
  - Semptify.py line 1428 (endpoint="vault_get")
  - Semptify.py line 1784 (endpoint='vault_blueprint.vault')
  - vault_bp.py line 31 (blueprint version)
- **❗ POTENTIAL CONFLICT:** Multiple vault route definitions

### Vault Features
- `/vault/upload` (POST, Semptify.py line 1452)
- `/vault/certificates` (GET, vault_bp.py line 41)
- `/vault/certificates/<cert>` (GET, line 42)
- `/vault/export_bundle` (POST, line 72)

### Notary Services
- `/notary` (GET + POST, vault_bp.py line 104)
  - Also: Semptify.py line 1794 (endpoint='notary')
- `/notary/upload` (POST, vault_bp.py line 136)
- `/notary/attest_existing` (POST, line 161)
- `/legal_notary` (GET + POST, line 192)
- `/legal_notary/start` (POST, Semptify.py line 926)
- `/legal_notary/return` (GET, vault_bp.py line 230)
- `/webhooks/ron` (POST, line 243) - Remote Online Notary webhook

### Document Delivery
- `/certified_post` (GET + POST, vault_bp.py line 280)
- `/court_clerk` (GET + POST, line 307)

---

## 📄 RESOURCES & TEMPLATES

### Resource Hub
- **Route:** `/resources` (Semptify.py line 707)
- **Sub-routes:**
  - `/resources/witness_statement` (line 712)
  - `/resources/witness_statement_save` (POST, line 717)
  - `/resources/filing_packet` (line 723)
  - `/resources/service_animal` (line 728)
  - `/resources/move_checklist` (line 733)

### Download Links
- `/resources/download/witness_statement.txt` (line 935)
- `/resources/download/filing_packet_checklist.txt` (line 1347)
- `/resources/download/filing_packet_timeline.txt` (line 1390)

### Form Routes (Legacy?)
- `/witness_form` (GET + POST, line 827)
- `/packet_form` (GET + POST, line 835)
- `/service_animal_form` (GET + POST, line 842)
- `/move_checklist_form` (GET + POST, line 849)

---

## 🛠️ TOOLS

### Tools Hub
- **Route:** `/tools` (Semptify.py line 745)
- **Individual Tools:**
  - `/tools/complaint-generator` (line 750)
  - `/tools/statute-calculator` (line 755)
  - `/tools/court-packet` (line 760)
  - `/tools/rights-explorer` (line 765)

### Rights Information
- `/know-your-rights` (line 770)

---

## 📅 CALENDAR & TIMELINE

### Calendar Views
- `/calendar-timeline` (Semptify.py line 658)
- `/calendar-timeline-horizontal` (line 663)
- `/calendar-widgets` (line 653)
- `/ledger-calendar` (line 647)
- `/timeline` (line 673)
- `/timeline-simple` (line 668)
- `/timeline-ruler` (line 678)

### Calendar API (calendar_timeline_routes.py)
- `/api/calendar/events` (GET + POST, lines 14, 51)
- `/api/calendar/events/<event_id>` (PUT + DELETE, lines 103, 124)
- `/api/calendar/rent-ledger` (GET, line 137)
- `/api/calendar/deadlines` (GET, line 155)
- `/api/calendar/statistics` (GET, line 177)
- `/api/calendar/export/ical` (GET + POST, line 195)
- `/api/calendar/types` (GET, line 232)

### Alternative Calendar API (calendar_api.py)
- `/api/calendar-alt/events` (GET + POST, lines 47, 81)
- `/api/calendar-alt/events/<event_id>` (GET + PUT + DELETE, lines 132, 149, 186)
- `/api/calendar-alt/upcoming` (GET, line 207)
- `/api/calendar-alt/types` (GET, line 244)
- `/api/calendar-alt/admin/all-events` (GET, line 282)

**❗ NOTE:** Two calendar API systems - may need consolidation

---

## 🎓 LEARNING SYSTEM

### Learning Dashboard
- `/learning` (Semptify.py line 1807)
- `/learning-dashboard` (line 683)

### Admin Learning Controls
- `/admin/learning` (GET, Semptify.py line 1093)
- `/admin/prime_learning` (POST, line 1026)
- `/admin/learning/reset` (POST, line 1147)
- `/admin/learning/download` (GET, line 1195)

---

## 🏛️ COMPLAINT FILING SYSTEM

### Main Interface
- `/file-complaint` (complaint_filing_routes.py line 11)

### API Endpoints
- `/api/complaint/identify-venues` (POST, line 20)
- `/api/complaint/get-procedures/<venue_key>` (POST, line 54)
- `/api/complaint/track-outcome` (POST, line 88)
- `/api/complaint/update-procedure` (POST, line 129)

### Library Views
- `/complaint-library` (line 158)
- `/filing-success-stories` (line 183)

---

## 🏠 HOUSING PROGRAMS

### Main Interface
- `/housing-programs` (housing_programs_routes.py line 28)

### API Endpoints
- `/api/programs/search` (POST, line 34)
- `/api/programs/category/<category>` (GET, line 108)
- `/api/programs/guide/<program_id>` (GET, line 160)
- `/api/programs/track-outcome` (POST, line 201)
- `/api/programs/intensity-recommendations` (POST, line 250)
- `/api/programs/eligibility-check` (POST, line 293)

---

## 📸 AUDIO/VIDEO CAPTURE SYSTEM

All routes prefixed with `/av/` (av_routes.py)

### Capture Routes
- `/av/capture/video` (POST, line 31)
- `/av/capture/audio` (POST, line 92)
- `/av/capture/photo` (POST, line 144)

### Import Routes
- `/av/import/voicemail` (POST, line 190)
- `/av/import/text-message` (POST, line 231)
- `/av/import/email` (POST, line 270)
- `/av/import/chat` (POST, line 315)

### Retrieval Routes
- `/av/captures/<capture_id>` (GET, line 362)
- `/av/captures/type/<capture_type>` (GET, line 374)
- `/av/captures/actor/<actor_id>` (GET, line 389)
- `/av/communications/phone/<phone_number>` (GET, line 404)
- `/av/communications/email/<email_address>` (GET, line 413)
- `/av/evidence/summary` (GET, line 422)
- `/av/evidence/by-date` (GET, line 433)
- `/av/health` (GET, line 455)

---

## 🔄 DATA FLOW ENGINE

All routes prefixed with `/data-flow/` (data_flow_routes.py)

- `/data-flow/register-functions` (POST, line 17)
- `/data-flow/functions` (GET, line 54)
- `/data-flow/process-document` (POST, line 81)
- `/data-flow/document/<doc_id>/flow` (GET, line 142)
- `/data-flow/actor/<actor_id>/flow` (GET, line 154)
- `/data-flow/registry` (GET, line 163)
- `/data-flow/statistics` (GET, line 182)

---

## 🎨 ADAPTIVE REGISTRATION

### Themed Registration Pages
- `/register-navy` (Semptify.py line 486)
- `/register-forest` (line 490)
- `/register-burgundy` (line 494)
- `/register-slate` (line 498)

### API
- `/api/register/adaptive` (POST, line 506)

---

## 📊 DASHBOARD API

All routes prefixed with `/api/dashboard-api/` (dashboard_api_routes.py)

- `/api/dashboard-api/layout/<user_id>` (GET, line 10)
- `/api/dashboard-api/cell/<user_id>/<cell>` (GET, line 27)
- `/api/dashboard-api/progress/<user_id>` (POST, line 37)
- `/api/dashboard-api/widgets` (GET, line 45)

---

## 🤖 AI / COPILOT SYSTEM

### Copilot Interface
- `/copilot` (GET, Semptify.py line 1342)
- `/api/copilot` (POST, ai_bp.py line 15)
- `/api/evidence-copilot` (POST, Semptify.py line 1395)

**AI Provider:** Ollama (from startup logs)

---

## 🔐 ADMIN PANEL

### Main Admin Routes (admin/routes.py)
- `/admin` (MULTIPLE definitions)
  - admin_bp.route line 54
  - admin_bp.route line 84
  - Semptify.py line 620
  - Semptify.py line 963
- `/admin/release_now` (POST, admin_bp line 69)
- `/admin/status` (GET, Semptify.py line 1015)
- `/admin/logs` (GET, admin_bp line 93)
- `/admin/metrics` (GET, admin_bp line 103)
- `/admin/users` (GET + POST, admin_bp line 116)

### Storage & Database Panel
- `/admin/storage-db` (admin_bp line 138)
- `/admin/storage-db/sync` (POST, line 151)
- `/admin/storage-db/download` (GET, line 162)

### Users Panel
- `/admin/users-panel` (admin_bp line 175)
- `/admin/users-panel/export` (GET, line 195)

### Email Panel
- `/admin/email` (GET + POST, admin_bp line 214)

### Security Panel
- `/admin/security` (admin_bp line 242)

### Human Perspective Panel
- `/admin/human` (GET + POST, admin_bp line 256)

---

## 📈 SYSTEM MONITORING

### Health Checks
- `/health` (Semptify.py line 1292)
- `/healthz` (line 1293)
- `/readyz` (line 1306)
- `/av/health` (av_routes.py line 455)

### Metrics
- `/metrics` (Semptify.py line 1216) - Prometheus-style metrics

---

## 💬 COMMUNICATION SYSTEM

- `/comm` (Semptify.py line 907)
- `/comm/metadata` (line 912)
- `/group/<group_id>` (line 902)

---

## 📖 INFORMATIONAL PAGES

### Static Pages
- `/about` (Semptify.py line 791)
  - Also: app.py line 13 (conflict?)
- `/privacy` (Semptify.py line 796)
- `/terms` (line 801)
- `/faq` (line 806)
- `/how-it-works` (line 811)
- `/features` (line 816)
- `/get-started` (line 821)
- `/office` (line 786)

### Library
- `/library` (line 740)

### Evidence Gallery
- `/evidence/gallery` (line 702)

### Help & Settings
- `/help` (line 780)
- `/settings` (line 775)

---

## 🔧 UTILITY ROUTES

### Token Management
- `/rotate_token` (POST, Semptify.py line 1353)

### Recovery
- `/recover` (Semptify.py line 249)
  - Also: auth_bp.py line 163 (conflict?)

### All Pages List
- `/all` (Semptify.py line 859)
- `/_html_list` (GET, line 866)

---

## 🚨 ENFORCEMENT / PUBLIC EXPOSURE

- `/enforcement/` (enforcement/public_exposure_module.py line 5)

---

## 📦 DELIVERY SYSTEM (app-backend/)

**Note:** These may be separate/unused
- `/api/deliveries` (POST)
- `/api/deliveries/<deliveryId>` (GET)
- `/api/deliveries/<deliveryId>/methods/<methodId>/attempt` (POST)
- `/api/deliveries/<deliveryId>/methods/<methodId>/confirm` (POST)
- `/api/cases/<caseId>/deliveries` (GET)
- `/api/files` (POST)
- `/webhooks/delivery-events` (POST)

---

## 🔴 IDENTIFIED ISSUES

### 1. **Route Conflicts/Duplicates**
- `/admin` - defined 4 times
- `/vault` - defined 3 times  
- `/signin` vs `/login` - both exist
- `/about` - defined in Semptify.py and app.py
- `/recover` - defined in Semptify.py and auth_bp.py
- `/notary` - defined twice

### 2. **Potential Dead Routes**
- Theme registration pages (navy, forest, burgundy, slate) - are these used?
- `/test-login` - test route should be removed in production
- `/dashboard-old` - old version, still needed?
- `/dashboard-grid` - alternate layout, documented?
- app-backend/delivery_api.py - appears separate, is it integrated?

### 3. **Missing Templates Check Needed**
Need to verify these templates exist:
- Landing page template for `/`
- Registration templates
- Dashboard templates (multiple versions)
- All resource templates
- All tool templates
- Admin panel templates

### 4. **API Consistency**
- Two calendar API systems (calendar_api.py and calendar_timeline_routes.py)
- Multiple dashboard APIs
- Need to document which is primary

### 5. **Blueprint Registration**
Need to verify all blueprints are registered in Semptify.py:
- ✅ auth_bp (confirmed in logs)
- ✅ ai_bp (confirmed in logs)
- ✅ vault_bp (confirmed in logs)
- ✅ admin_bp (need to verify)
- ❓ av_routes_bp (not seen in logs)
- ❓ complaint_filing_bp (not seen in logs)
- ❓ housing_programs_bp (not seen in logs)
- ❓ data_flow_bp (not seen in logs)
- ❓ enforcement_bp (not seen in logs)
- ❓ calendar_bp (not seen in logs)
- ❓ dashboard_api_bp (confirmed in logs - "Learning dashboard API")

---

## 📋 NEXT STEPS FOR TESTING

### Phase 1: New User Flow
1. Visit `/` - check landing page renders
2. Click register → verify `/register` works
3. Complete registration → check `/verify` flow
4. Verify code → confirm redirect to `/dashboard`
5. Check dashboard shows smart suggestions

### Phase 2: Returning User Flow
1. Visit `/login`
2. Enter credentials
3. Confirm `/dashboard` loads
4. Test navigation to main sections

### Phase 3: Feature Testing
1. **Vault:** `/vault` → upload/download
2. **Resources:** `/resources` → each document type
3. **Tools:** `/tools` → each tool
4. **Calendar:** `/calendar-timeline` → events
5. **Learning:** `/learning-dashboard` → suggestions
6. **Admin:** `/admin` → all panels

### Phase 4: Admin Panel Testing
1. Storage/DB panel - check R2 status
2. Users panel - verify user list
3. Email panel - test email send
4. Security panel - check security mode
5. Human perspective panel - test humanization

### Phase 5: API Testing
1. Dashboard APIs
2. Calendar APIs
3. Complaint filing APIs
4. Housing programs APIs
5. Copilot API

---

## 🎯 RECOMMENDED ACTIONS

1. **Resolve Route Conflicts:** Consolidate duplicate route definitions
2. **Remove Dead Code:** Clean up test routes and old versions
3. **Blueprint Audit:** Verify all blueprints are properly registered
4. **Template Audit:** Ensure all routes have corresponding templates
5. **API Documentation:** Document primary vs alternate API endpoints
6. **Navigation Flow:** Create sitemap showing all user paths
7. **Link Testing:** Verify all internal links work
8. **Error Handling:** Add 404 page for missing routes

---

## 📊 STATISTICS

- **Total Routes Found:** 200+
- **Blueprints Identified:** 11+
- **API Endpoints:** 50+
- **Admin Routes:** 15+
- **User-Facing Pages:** 30+
- **Route Conflicts:** 6+

