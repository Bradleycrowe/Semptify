# 🧪 Semptify Live Testing Checklist
**Server Running:** http://127.0.0.1:5000  
**Test Date:** November 11, 2025

---

## ✅ TESTED ROUTES

### 🏠 Core Pages
- [ ] `/` (home) → renders `index_simple.html`
- [ ] `/register` → registration form
- [ ] `/login` → login form
- [ ] `/dashboard` → main dashboard
- [ ] `/vault` → document vault

### 👤 Authentication Flow
- [ ] **New User:**
  1. `/register` → fill form
  2. POST `/register` → send verification
  3. `/verify` → enter code
  4. POST `/verify` → verify code
  5. Redirect to `/dashboard`
  
- [ ] **Returning User:**
  1. `/login` → enter credentials
  2. POST `/login` → authenticate
  3. Redirect to `/dashboard`

- [ ] `/recover` → password recovery
- [ ] `/resend-code` (POST) → resend verification

### 📄 Resources
- [ ] `/resources` → resource hub
- [ ] `/resources/witness_statement` → witness form
- [ ] `/resources/filing_packet` → packet form
- [ ] `/resources/service_animal` → service animal form
- [ ] `/resources/move_checklist` → move checklist

### 🛠️ Tools
- [ ] `/tools` → tools hub
- [ ] `/tools/complaint-generator`
- [ ] `/tools/statute-calculator`
- [ ] `/tools/court-packet`
- [ ] `/tools/rights-explorer`

### 📅 Calendar
- [ ] `/calendar-timeline` → timeline view
- [ ] `/ledger-calendar` → rent ledger
- [ ] `/calendar-widgets` → widget view
- [ ] `/timeline` → timeline
- [ ] `/timeline-simple` → simple timeline

### 🎓 Learning
- [ ] `/learning` → learning dashboard
- [ ] `/learning-dashboard` → alternate view

### 🏛️ Complaints & Housing
- [ ] `/file-complaint` → complaint filing
- [ ] `/housing-programs` → housing programs

### 📖 Information Pages
- [ ] `/about` → about page
- [ ] `/how-it-works`
- [ ] `/features`
- [ ] `/faq`
- [ ] `/privacy`
- [ ] `/terms`
- [ ] `/help`

### 🔐 Admin Panel
- [ ] `/admin` → admin dashboard
- [ ] `/admin/storage-db` → storage panel
- [ ] `/admin/users-panel` → users panel
- [ ] `/admin/email` → email panel
- [ ] `/admin/security` → security panel
- [ ] `/admin/human` → human perspective panel
- [ ] `/admin/learning` → learning admin

### 📊 System
- [ ] `/health` → health check (JSON)
- [ ] `/healthz` → health check (JSON)
- [ ] `/readyz` → readiness check (JSON)
- [ ] `/metrics` → Prometheus metrics

### 🤖 AI/Copilot
- [ ] `/copilot` → copilot interface

---

## 🔴 BROKEN ROUTES (404s)

_List any routes that return 404:_

---

## ⚠️ ERROR ROUTES (500s)

_List any routes that error:_

---

## 🔗 MISSING LINKS

_Links that should exist but don't:_

---

## 📝 NOTES & OBSERVATIONS

### Template Status
✅ **Confirmed templates exist:**
- index_simple.html
- register.html
- login.html
- verify_code.html
- dashboard_welcome.html
- vault.html
- witness_statement.html
- filing_packet.html
- service_animal.html
- move_checklist.html
- resources.html
- calendar_timeline.html
- learning_dashboard.html
- file_complaint.html
- housing_programs.html
- welcome.html
- All admin templates (dashboard, storage_db, users_panel, email_panel, security_panel, human_perspective)

❓ **Need to check which template for:**
- `/tools` routes
- `/about`, `/how-it-works`, `/features`, `/faq` pages
- `/copilot` interface

### Blueprint Registration Status (from logs)
✅ Registered:
- auth_bp (/register, /login, /verify)
- ai_bp (/api/copilot with Ollama)
- vault_bp (/vault, /notary, /certified_post, /court_clerk)
- Onboarding flow
- Calendar timeline routes
- Learning dashboard API
- Dashboard API

❓ Not confirmed in logs:
- av_routes_bp
- complaint_filing_bp (BUT route works)
- housing_programs_bp (BUT route works) 
- data_flow_bp
- enforcement_bp
- admin_bp

---

## 🎯 TESTING PRIORITY

### CRITICAL (Must work for launch)
1. Home page → Register → Verify → Dashboard
2. Login → Dashboard
3. Dashboard → Vault
4. Dashboard → Resources
5. Admin panel access

### HIGH (Core features)
6. Resources → all document forms
7. Calendar/Timeline views
8. Learning dashboard
9. Complaint filing
10. Housing programs

### MEDIUM (Nice to have)
11. Tools section
12. Information pages
13. Help system
14. Settings

### LOW (Can fix post-launch)
15. Alternative views (dashboard-grid, dashboard-old)
16. Theme registration pages
17. Test routes
18. Deprecated routes

---

## 🚀 NEXT ACTIONS

1. ⏳ Open browser to http://127.0.0.1:5000
2. ⏳ Test home page
3. ⏳ Test registration flow
4. ⏳ Test login flow
5. ⏳ Navigate through all main features
6. ⏳ Document any issues found
7. ⏳ Create bug list with priorities

