# 🧪 Quick Browser Testing Guide

Open this in your browser alongside http://127.0.0.1:5000

---

## 🏠 HOME PAGE TEST

**URL:** http://127.0.0.1:5000/

### Check:
- [ ] Page loads without errors
- [ ] "Get Started Free" button visible
- [ ] "Sign in" link visible
- [ ] Features list displays
- [ ] Gradient background shows
- [ ] Logo "Semptify" displays

### Click Test:
- [ ] Click "Get Started Free" → Should go to `/register`
- [ ] Click "Sign in" → Should go to `/login`

**Expected:** Clean landing page with purple gradient

---

## 📝 REGISTRATION TEST

**URL:** http://127.0.0.1:5000/register

### Check:
- [ ] Registration form displays
- [ ] Fields: Email, First Name, Last Name, Password
- [ ] Submit button works
- [ ] No console errors

### Submit Test:
- [ ] Fill in form with test data
- [ ] Click submit
- [ ] Should redirect to `/verify`
- [ ] Verification code should be sent (check logs)

**Expected:** Form submission works, redirects to verify page

---

## ✅ VERIFICATION TEST

**URL:** http://127.0.0.1:5000/verify

### Check:
- [ ] Verification code input field displays
- [ ] "Resend Code" button available
- [ ] Submit button works

### Submit Test:
- [ ] Enter code from email/logs
- [ ] Click verify
- [ ] Should redirect to `/dashboard`
- [ ] Welcome message should show

**Expected:** Successful verification, welcome dashboard appears

---

## 🎯 DASHBOARD TEST

**URL:** http://127.0.0.1:5000/dashboard

### Check:
- [ ] Welcome message with user name
- [ ] Motto: "Document everything!" displays
- [ ] Smart suggestions section visible
- [ ] Three step cards display (Vault, Evidence, Calendar)

### Navigation Test:
- [ ] Click "Open Vault" → `/vault`
- [ ] Click "Start Here" → `/resources/witness_statement`
- [ ] Click "Add Events" → `/calendar-timeline`
- [ ] Click "📚 Resources" → `/resources`
- [ ] Click "🏠 Housing Programs" → `/housing-programs`

**Expected:** All navigation buttons work, no 404s

---

## 📁 VAULT TEST

**URL:** http://127.0.0.1:5000/vault

### Check:
- [ ] Vault interface loads
- [ ] Upload form visible
- [ ] File list displays (if any files exist)
- [ ] Notary link visible

### Upload Test:
- [ ] Select a test file
- [ ] Click upload
- [ ] File should appear in vault
- [ ] No errors in console

**Expected:** File upload works, files listed

---

## 📄 RESOURCES TEST

**URL:** http://127.0.0.1:5000/resources

### Check:
- [ ] Resource hub page loads
- [ ] Links to all 4 resources visible
  - Witness Statement
  - Filing Packet
  - Service Animal
  - Move Checklist

### Navigation Test:
- [ ] Click "Witness Statement" → form loads
- [ ] Click "Filing Packet" → form loads
- [ ] Click "Service Animal" → form loads
- [ ] Click "Move Checklist" → form loads

**Expected:** All 4 resource pages load without errors

---

## 📅 CALENDAR TEST

**URL:** http://127.0.0.1:5000/calendar-timeline

### Check:
- [ ] Calendar interface loads
- [ ] Add event button visible
- [ ] Timeline displays

### Add Event Test:
- [ ] Click "Add Event"
- [ ] Fill in event details
- [ ] Submit
- [ ] Event should appear on timeline

**Expected:** Calendar functional, events can be added

---

## 🏛️ COMPLAINT FILING TEST

**URL:** http://127.0.0.1:5000/file-complaint

### Check:
- [ ] Complaint filing interface loads
- [ ] Form or wizard displays
- [ ] No template errors

**Expected:** Page loads (even if not fully functional yet)

---

## 🏠 HOUSING PROGRAMS TEST

**URL:** http://127.0.0.1:5000/housing-programs

### Check:
- [ ] Housing programs page loads
- [ ] Search interface visible
- [ ] Programs list displays

**Expected:** Page loads, basic interface functional

---

## 🔐 ADMIN PANEL TEST

**URL:** http://127.0.0.1:5000/admin

### Check:
- [ ] Admin dashboard loads
- [ ] Motto visible
- [ ] 6 panel cards display:
  - Storage / Database
  - Users Panel
  - Email Panel
  - Security Panel
  - Human Perspective
  - (Learning might be separate route)

### Panel Test:
- [ ] Click "Storage / Database" → `/admin/storage-db` loads
- [ ] Click "Users Panel" → `/admin/users-panel` loads
- [ ] Click "Email Panel" → `/admin/email` loads
- [ ] Click "Security Panel" → `/admin/security` loads
- [ ] Click "Human Perspective" → `/admin/human` loads

**Expected:** All 6 panels accessible, no 404s

---

## ❌ KNOWN BROKEN ROUTES

These will return 500 errors (template not found):

### Tools Section
- `/tools` ❌
- `/tools/complaint-generator` ❌
- `/tools/statute-calculator` ❌
- `/tools/court-packet` ❌
- `/tools/rights-explorer` ❌

### Information Pages
- `/about` ❌
- `/how-it-works` ❌
- `/features` ❌
- `/faq` ❌
- `/privacy` ❌
- `/terms` ❌

### Support Pages
- `/help` ❌
- `/settings` ❌

**Don't test these yet** - they need templates created first

---

## 📊 SYSTEM HEALTH TEST

### Health Check
**URL:** http://127.0.0.1:5000/health

- [ ] Returns JSON: `{"status": "ok"}`
- [ ] No errors

### Readiness Check
**URL:** http://127.0.0.1:5000/readyz

- [ ] Returns JSON with status
- [ ] Shows database writable
- [ ] Shows runtime dirs accessible

### Metrics
**URL:** http://127.0.0.1:5000/metrics

- [ ] Returns Prometheus-style metrics
- [ ] Shows request counts
- [ ] Shows uptime

**Expected:** All health endpoints return proper JSON/text

---

## 🤖 AI/COPILOT TEST

**URL:** http://127.0.0.1:5000/copilot

### Check:
- [ ] Copilot interface loads
- [ ] Input form visible
- [ ] Submit button works

### API Test:
```bash
curl -X POST http://127.0.0.1:5000/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test message"}'
```

- [ ] Returns JSON response
- [ ] Ollama provider responds

**Expected:** Copilot interface functional (if Ollama is running)

---

## 🔄 LOGIN/LOGOUT TEST

### Login
**URL:** http://127.0.0.1:5000/login

- [ ] Login form displays
- [ ] Email and password fields
- [ ] Submit works

### Test Login:
- [ ] Enter registered email/password
- [ ] Click login
- [ ] Redirects to dashboard
- [ ] Session active

### Logout (if implemented):
- [ ] Logout button/link visible
- [ ] Click logout
- [ ] Redirects to home
- [ ] Session cleared

**Expected:** Complete auth cycle works

---

## 📱 MOBILE TEST (Optional)

### Responsive Check:
- [ ] Open DevTools (F12)
- [ ] Toggle device toolbar
- [ ] Test at 375px width (mobile)
- [ ] Test at 768px width (tablet)
- [ ] Test at 1024px width (desktop)

### Check:
- [ ] Navigation accessible
- [ ] Forms usable
- [ ] Buttons clickable
- [ ] Text readable
- [ ] No horizontal scroll

**Expected:** Site usable on all screen sizes

---

## 🐛 BUG TRACKING

### Errors Found:

**Page:** _______________
**URL:** _______________
**Error:** _______________
**Console:** _______________

**Page:** _______________
**URL:** _______________
**Error:** _______________
**Console:** _______________

**Page:** _______________
**URL:** _______________
**Error:** _______________
**Console:** _______________

---

## ✅ SUMMARY

### Working Routes: _____ / 20
### Broken Routes: _____ / 20
### Critical Issues: _____
### Minor Issues: _____

### Overall Assessment:
- [ ] 🟢 Ready to deploy
- [ ] 🟡 Needs minor fixes
- [ ] 🔴 Needs major fixes

### Priority Fixes Needed:
1. _______________
2. _______________
3. _______________

---

## 🎯 NEXT ACTIONS

After testing, prioritize:

1. **Critical (Deploy Blocker):**
   - Fix any 500 errors on main paths
   - Create missing privacy/terms templates
   - Resolve authentication issues

2. **Important (Week 1):**
   - Create tools section templates
   - Fix broken navigation links
   - Mobile responsiveness issues

3. **Nice to Have (Post-Launch):**
   - Polish UI/UX
   - Add more features
   - Performance optimization

