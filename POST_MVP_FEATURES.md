# Post-MVP Features Documentation

## Calendar Sync

### Status: Planned for Post-MVP Sprint 2

**Feature Overview:**
Enable users to sync court dates and deadlines to their personal calendars.

**Implementation Options:**

1. **.ics File Export (Simple)**
   - Generate .ics files from timeline events
   - User downloads and imports to any calendar app
   - Estimated time: 1-2 hours
   - Libraries: `icalendar` (already in requirements.txt)

2. **Google Calendar Integration (OAuth)**
   - Direct sync to Google Calendar
   - Automatic updates when deadlines change
   - Estimated time: 3-4 hours
   - Requires: Google Calendar API, OAuth setup

3. **Apple Calendar / Outlook Integration**
   - CalDAV protocol for Apple
   - Microsoft Graph API for Outlook
   - Estimated time: 4-6 hours per platform

**MVP Workaround:**
- Dashboard shows all upcoming deadlines
- Users can manually add to their calendar
- PDF court packets include deadline dates

**Post-MVP Implementation:**
1. Phase 1: .ics export (Sprint 2)
2. Phase 2: Google Calendar sync (Sprint 3)
3. Phase 3: Apple/Outlook support (Sprint 4)

---

## Email Notifications

### Status: Planned for Post-MVP Sprint 2

**Feature Overview:**
Automated email alerts for deadlines, document expiration, case updates.

**Notification Types:**

1. **Deadline Alerts**
   - 24 hours before court date
   - 1 week before response due
   - 3 days before document expiration

2. **Document Notifications**
   - New document analyzed
   - Case strength score updated
   - Evidence recommendations available

3. **Case Status Updates**
   - Case status changed
   - New next steps generated
   - Missing documents identified

**Implementation Options:**

1. **SendGrid (Recommended)**
   - Free tier: 100 emails/day
   - Template support
   - Delivery tracking
   - Estimated time: 2-3 hours

2. **AWS SES**
   - Pay-as-you-go pricing
   - High deliverability
   - Requires AWS account
   - Estimated time: 3-4 hours

3. **SMTP (Basic)**
   - Use any SMTP server
   - Gmail, Office365, etc.
   - Limited features
   - Estimated time: 1-2 hours

**MVP Workaround:**
- Dashboard shows notification badge for urgent items
- Users check dashboard for updates
- Browser notifications (if enabled)

**Post-MVP Implementation:**
1. Phase 1: SMTP basic notifications (Sprint 2)
2. Phase 2: SendGrid templates (Sprint 3)
3. Phase 3: SMS notifications via Twilio (Sprint 4)

**Email Templates Needed:**
- `deadline_reminder.html`
- `document_analyzed.html`
- `case_strength_update.html`
- `missing_documents.html`
- `weekly_summary.html`

---

## Background Check API

### Status: Not Needed for MVP

**Decision:** Feature not critical for tenant rights protection platform.

**Rationale:**
- Primary users are tenants, not landlords
- Landlords have commercial services for tenant screening
- Legal/privacy concerns with background checks
- Not core to complaint filing or document intelligence

**Recommendation:** Remove from roadmap or consider for separate landlord-facing product.

---

## Summary

**Deferred to Post-MVP:**
- ✅ Attorney Directory (documented in ATTORNEY_DIRECTORY_FUTURE.md)
- ✅ Calendar Sync (documented above)
- ✅ Email Notifications (documented above)

**Removed from Scope:**
- ❌ Background Check API (not aligned with product mission)

**MVP Focus:**
- ✅ Context Data System (100%)
- ✅ Document Intelligence (100%)
- ✅ Perspective Reasoning (100%)
- ✅ Complaint Filing Integration (100%)
- ✅ Vault + Timeline (100%)
- ✅ Case Assessment (100%)

**System Completion:** 95% MVP-ready

**Next Steps:**
1. Final testing (Context API, Complaint API, Perspective Analysis)
2. Production environment setup
3. Database backup strategy
4. Deployment to Render.com
5. User acceptance testing

**Time to MVP:** 2-3 hours (testing + deployment)