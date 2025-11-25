# SEMPTIFY - USER INTERACTION FLOW & ASSEMBLY PLAN
## Simplified Structure for Human-Friendly Navigation

---

## 1. CORE USER JOURNEYS (Primary Flows)

### Journey A: First-Time User Registration
**Goal**: Get user authenticated and ready to use Semptify

1. **Entry** → http://localhost:5000/
2. **OAuth Check** → No session detected
3. **Redirect** → /setup (Storage Setup)
4. **Choose Provider** → Google Drive OR Dropbox
5. **OAuth Flow** → External consent screen
6. **Callback** → Token exchange & encryption
7. **Success** → Welcome Home with user_token
8. **Result**: User is authenticated, has anonymous token, ready to use all features

**Key Pages**:
- `/` (entry)
- `/setup` (storage choice)
- `/oauth/google/start` or `/oauth/dropbox/start`
- `/oauth/google/callback` or `/oauth/dropbox/callback`
- `/` (welcome home with token)

**No Dead Ends**: Every step leads to next, or back to setup on error.

---

### Journey B: Document Vault Upload & Attestation
**Goal**: User uploads evidence, gets notarized certificate

1. **Start** → Welcome Home → Click "Vault"
2. **Vault Page** → /vault?user_token=...
3. **Upload Form** → Choose file(s)
4. **POST** → /api/vault/upload
5. **Processing** → Save to uploads/vault/<user_id>/
6. **OCR** → EasyOCR extracts handwriting (if image)
7. **Forensics** → Check metadata for tampering
8. **Certificate** → Generate notary_<timestamp>_<type>.json with SHA-256, timestamp, evidence context
9. **Timeline Update** → INSERT INTO timeline_events
10. **Cloud Backup** → Optional sync to Drive/Dropbox/R2
11. **Result** → User sees uploaded file, download certificate, view in timeline

**Key Pages & APIs**:
- `/vault` (main UI)
- `/api/vault/upload` (POST file)
- `/api/vault/list` (GET files)
- `/api/vault/download/<file_id>` (GET file)
- `/api/vault/attest` (POST attestation)
- `/api/timeline/events` (GET merged events)

**No Dead Ends**: After upload, user can download, view timeline, or upload more.

---

### Journey C: File a Complaint
**Goal**: User creates court-ready complaint packet

1. **Start** → Welcome Home → Click "File Complaint"
2. **Complaint Wizard** → /file-complaint?user_token=...
3. **Step 1** → Property details (address, landlord name)
4. **Step 2** → Violation details (type, date, description)
5. **Step 3** → Evidence selection (link vault files)
6. **Step 4** → Review & confirm
7. **POST** → /api/complaint/generate
8. **PDF Generation** → ReportLab creates court packet
9. **Save** → uploads/complaints/<user_id>/<packet>.pdf
10. **Database** → INSERT INTO cases
11. **Result** → User downloads PDF, sees in timeline, can file with court

**Key Pages & APIs**:
- `/file-complaint` (wizard UI)
- `/api/complaint/generate` (POST form data)
- `/api/complaint/download/<id>` (GET PDF)

**No Dead Ends**: After generation, user can download, start new complaint, or go to calendar to track deadlines.

---

### Journey D: Research & Legal Library
**Goal**: User finds legal info, statutes, and tenant rights

1. **Start** → Welcome Home → Click "Library"
2. **Library Hub** → /library?user_token=...
3. **Browse Sections**:
   - Eviction Law → /library/eviction-basics
   - Tenant Rights → /library/tenant-rights
   - Court Procedures → /library/court-procedures
   - Court Forms → /library/court-forms
4. **External Links** → .gov sources (revisor.mn.gov, mncourts.gov, hud.gov)
5. **Legal Aid** → SMRLS, HOME Line, Legal Aid Society
6. **Result** → User finds accurate, up-to-date legal info

**Key Pages**:
- `/library` (hub)
- `/library/eviction-basics`
- `/library/tenant-rights`
- `/library/court-procedures`
- `/library/court-forms`

**Research Tools**:
- `/research` → Landlord lookup, code violations, property history

**No Dead Ends**: All external links open in new tab, user stays on Semptify. Can always return to Library or Home.

---

### Journey E: Calendar & Timeline
**Goal**: Track deadlines, rent payments, and case events

1. **Start** → Welcome Home → Click "Calendar"
2. **Calendar Hub** → /calendar?user_token=...
3. **View Modes**:
   - Calendar view (month/week/day)
   - Timeline view (chronological events)
   - Rent ledger (payment tracking)
4. **Add Event** → POST /api/calendar/event
5. **Log Payment** → POST /api/calendar/rent-payment
6. **Export** → GET /api/calendar/export.ics (iCal file)
7. **Result** → User sees all deadlines, payments, and case events in one place

**Key Pages & APIs**:
- `/calendar` (main UI)
- `/api/calendar/events` (GET events)
- `/api/calendar/event` (POST new event)
- `/api/calendar/rent-payment` (POST payment)
- `/api/calendar/export.ics` (GET iCal)
- `/api/timeline/events` (GET timeline with vault certificates)

**No Dead Ends**: User can always add events, view timeline, or export to external calendar.

---

### Journey F: Admin & System Management
**Goal**: Admin manages users, views metrics, rotates tokens

1. **Entry** → /admin (requires admin token)
2. **Admin Token Check** → validate_admin_token() from security.py
3. **Admin Dashboard** → /admin/dashboard
4. **Sections**:
   - User Management → /admin/users
   - Learning System → /admin/learning
   - Security Panel → /admin/security
   - Metrics → /metrics (Prometheus/JSON)
   - Readiness → /readyz (health check)
5. **Actions**:
   - Create/delete users
   - Rotate admin tokens
   - Prime learning patterns
   - View rate limit stats
   - Check system health
6. **Result** → Admin maintains system, monitors health, manages access

**Key Pages & APIs**:
- `/admin` (dashboard)
- `/admin/users` (user management)
- `/admin/learning` (learning system)
- `/admin/security` (tokens, rate limits)
- `/metrics` (system metrics)
- `/readyz` (health check)

**No Dead Ends**: Admin can always return to dashboard or log out.

---

## 2. INFORMATION ARCHITECTURE

### Primary Navigation (Always Visible)
**Navbar** (in base_layout.html):
- Home → /
- Library → /library
- Calendar → /calendar
- Vault → /vault
- Help → /help_hub

### Secondary Navigation (Contextual)
- Research → /research (from Library or Home)
- File Complaint → /file-complaint (from Home or Help)
- Journey → /journey (from Home)
- Admin → /admin (if admin token)

### Footer (Educational Disclaimer)
**Yellow banner** on all pages:
"Semptify is for educational purposes only. Not a substitute for legal advice. Consult an attorney for legal representation."

---

## 3. DATA FLOW OPTIMIZATION

### User Data (User Token Flow)
1. **Generation** → 12-digit anonymous token on registration
2. **Storage** → SHA-256 hash in security/users.json
3. **Propagation** → Passed via query param (?user_token=...) on all internal links
4. **JavaScript** → goTo(path) function auto-appends user_token
5. **Forms** → Hidden input <input type="hidden" name="user_token" value="...">
6. **Result** → User session maintained across all pages

### Admin Data (Admin Token Flow)
1. **Generation** → SHA-256 hash in security/admin_tokens.json
2. **Validation** → validate_admin_token() checks hash
3. **Rate Limiting** → ADMIN_RATE_WINDOW, ADMIN_RATE_MAX
4. **Break-Glass** → Emergency access with special token (one-time use)
5. **Result** → Secure admin access with audit trail

### Document Data (Vault → Timeline → Cloud)
1. **Upload** → POST /api/vault/upload
2. **Local Storage** → uploads/vault/<user_id>/
3. **Certificate** → notary_<timestamp>.json with SHA-256, timestamp, evidence
4. **Database** → INSERT INTO timeline_events
5. **Cloud Sync** → Optional backup to Drive/Dropbox/R2
6. **Result** → User has local + cloud backup with cryptographic proof

### AI Data (Copilot → Providers)
1. **Request** → POST /api/copilot with {prompt, context}
2. **Provider Routing** → AI_PROVIDER env (openai | azure | ollama)
3. **External API** → OpenAI, Azure OpenAI, or local Ollama
4. **Response** → JSON {response, tokens, model}
5. **Result** → User gets AI assistance for legal questions

---

## 4. BROKEN LINKS & FIXES

### Fixed in This Session
- ✅ `/complaint_filing` → `/file-complaint` (welcome_home.html)
- ✅ `/ai-help` → `/copilot` (welcome_home.html)
- ✅ user_token added to all links in library_hub.html, research.html, help_hub.html
- ✅ goTo() function ensures user_token propagation

### Common Issues & Solutions
**Issue**: Links missing user_token → Session lost  
**Fix**: Add `?user_token={{ user_token or request.args.get('user_token') }}` to all href

**Issue**: Dead-end pages with no navigation  
**Fix**: Ensure all pages extend base_layout.html for consistent navbar

**Issue**: Broken external links  
**Fix**: Verify .gov URLs, open in new tab with target="_blank"

**Issue**: Forms don't pass user_token  
**Fix**: Add hidden input: `<input type="hidden" name="user_token" value="...">`

**Issue**: JavaScript navigation loses token  
**Fix**: Use goTo(path) function instead of direct location.href

---

## 5. EFFICIENT, NO-WASTE DESIGN PRINCIPLES

### Principle 1: Every Page Has a Purpose
- No "placeholder" or "coming soon" pages
- Every page provides value or leads to value
- Remove or complete incomplete features

### Principle 2: Clear Next Steps
- Every page tells user what to do next
- CTA buttons are visible and actionable
- No confusion about where to go

### Principle 3: Accurate, Up-to-Date Information
- All .gov links verified and current
- AI responses use latest models
- Database queries pull fresh data
- No stale or cached info

### Principle 4: Minimal Clicks, Maximum Value
- Common tasks are 1-2 clicks from home
- Wizards guide through complex flows
- Smart defaults reduce form filling
- Autosave prevents data loss

### Principle 5: Consistent Experience
- Same navbar on all pages
- Same disclaimer on all pages
- Same styling and interaction patterns
- Predictable behavior everywhere

---

## 6. PAGE STRUCTURE TEMPLATE

### Standard Page Layout (base_layout.html)
```html
{% extends "base_layout.html" %}

{% block title %}Page Title - Semptify{% endblock %}

{% block content %}
<div class="container">
    <h1>Page Title</h1>
    
    <!-- Breadcrumbs -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li><a href="/?user_token={{ user_token }}">Home</a></li>
            <li class="active">Current Page</li>
        </ol>
    </nav>
    
    <!-- Main Content -->
    <div class="content">
        <!-- Page-specific content here -->
    </div>
    
    <!-- Clear Next Steps -->
    <div class="next-steps">
        <h3>What's Next?</h3>
        <button onclick="goTo('/next-logical-step')">Continue</button>
        <button onclick="goTo('/')">Back to Home</button>
    </div>
</div>
{% endblock %}
```

---

## 7. TESTING & VALIDATION CHECKLIST

### For Every Page:
- [ ] Extends base_layout.html (navbar + disclaimer)
- [ ] Has clear page title
- [ ] All links include user_token
- [ ] External links open in new tab
- [ ] Forms have hidden user_token input
- [ ] Has clear CTA or next step
- [ ] No broken images or 404s
- [ ] Mobile responsive
- [ ] Accessible (ARIA labels, keyboard nav)

### For Every Feature:
- [ ] Fully implemented (no placeholders)
- [ ] Provides accurate, up-to-date info
- [ ] Has success and error states
- [ ] Logs to timeline or database
- [ ] Can be reached from main navigation
- [ ] Has clear user benefit

### For Every User Flow:
- [ ] Starts from Welcome Home
- [ ] Clear step-by-step progression
- [ ] No dead ends or loops
- [ ] Success leads to next logical action
- [ ] Error leads back to safe state
- [ ] Can be completed in < 5 minutes

---

## 8. MAINTENANCE & CONTINUOUS IMPROVEMENT

### Weekly:
- Check all external .gov links
- Review error logs for 404s
- Test OAuth flows
- Verify database backups

### Monthly:
- Update legal info if statutes change
- Review user feedback
- Optimize slow pages
- Update AI models/prompts

### Quarterly:
- Full security audit
- Load testing
- Accessibility audit
- User experience review

---

## SUMMARY: EFFICIENT, HUMAN-FRIENDLY SEMPTIFY

**Before**: Hundreds of pages, broken links, unclear flows, dead ends  
**After**: Streamlined, purposeful pages with clear navigation and no waste

**Key Improvements**:
1. Every page leads somewhere useful
2. All links work and pass user_token
3. Consistent navbar + disclaimer on all pages
4. Clear user journeys with no dead ends
5. Accurate, up-to-date information from verified sources
6. Minimal clicks for common tasks
7. Smart defaults and autosave
8. Mobile-friendly and accessible

**Result**: Users can accomplish their goals quickly, with confidence, and without frustration.

---

END OF WRITTEN OUTLINE
