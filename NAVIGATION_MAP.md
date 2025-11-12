# 🗺️ Semptify Navigation Flow Map

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         HOME PAGE (/)                                    │
│                     index_simple.html                                    │
│                                                                          │
│  [Get Started] [Learn More] [Login]                                    │
└───────────┬──────────────┬────────────┬─────────────────────────────────┘
            │              │            │
            ▼              ▼            ▼
    ┌──────────────┐  ┌─────────┐  ┌────────┐
    │  /register   │  │ /about  │  │ /login │
    └──────┬───────┘  │ /how-it │  └───┬────┘
           │          │ /features│      │
           │          │ /faq     │      │
           ▼          └─────────┘      │
    ┌──────────────┐                   │
    │   /verify    │                   │
    │ (enter code) │                   │
    └──────┬───────┘                   │
           │                           │
           └───────────┬───────────────┘
                       ▼
            ┌─────────────────────┐
            │    /dashboard        │
            │ (Smart Suggestions) │
            │  [First-time tour]  │
            └──────────┬──────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│   VAULT    │  │ RESOURCES  │  │ CALENDAR   │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      │               │               │
      ▼               ▼               ▼
```

---

## 📁 VAULT SYSTEM

```
/vault (Main Hub)
├── 📤 Upload Document
├── 📥 Download Document
├── 📜 View Certificates
├── 📦 Export Bundle
│
├── ⚖️ NOTARY SERVICES
│   ├── /notary (Main)
│   ├── /notary/upload
│   ├── /notary/attest_existing
│   ├── /legal_notary (Remote Online Notary)
│   └── /legal_notary/return
│
├── 📮 DELIVERY
│   ├── /certified_post (Certified Mail)
│   └── /court_clerk (Court Filing)
│
└── 🔐 Security Features
    ├── SHA-256 hashing
    ├── Timestamp proof
    └── Evidence certification
```

---

## 📄 RESOURCES SECTION

```
/resources (Hub)
├── 📝 Witness Statement (/resources/witness_statement)
│   ├── Form with field helpers
│   ├── Inline tooltips (ℹ️)
│   └── Save: POST /resources/witness_statement_save
│
├── 📋 Filing Packet (/resources/filing_packet)
│   ├── Download checklist
│   └── Download timeline
│
├── 🐕 Service Animal (/resources/service_animal)
│   └── Documentation form
│
└── 📦 Move Checklist (/resources/move_checklist)
    └── Moving prep list
```

---

## 🛠️ TOOLS SECTION

```
/tools (Hub)
├── ⚖️ Complaint Generator (/tools/complaint-generator)
│   └── Generate legal complaints
│
├── 📊 Statute Calculator (/tools/statute-calculator)
│   └── Calculate deadlines
│
├── 📑 Court Packet (/tools/court-packet)
│   └── Prepare court documents
│
└── 🎓 Rights Explorer (/tools/rights-explorer)
    └── Know your tenant rights
    └── Link: /know-your-rights
```

---

## 📅 CALENDAR & TIMELINE

```
┌─────────────────────────────────────────────┐
│        CALENDAR SYSTEM (Multiple Views)     │
├─────────────────────────────────────────────┤
│                                             │
│  /calendar-timeline (Main Timeline)         │
│  ├── Add events                             │
│  ├── Edit events                            │
│  ├── Delete events                          │
│  └── Export to iCal                         │
│                                             │
│  /ledger-calendar (Rent Ledger Focus)       │
│  ├── Track rent payments                    │
│  ├── Track late fees                        │
│  └── Payment history                        │
│                                             │
│  /calendar-widgets (Widget View)            │
│  └── Embeddable components                  │
│                                             │
│  /timeline (Full Timeline)                  │
│  /timeline-simple (Simplified)              │
│  /timeline-ruler (With ruler)               │
│  /calendar-timeline-horizontal (Horizontal) │
│                                             │
└─────────────────────────────────────────────┘

API Endpoints:
├── GET/POST /api/calendar/events
├── PUT/DELETE /api/calendar/events/<id>
├── GET /api/calendar/rent-ledger
├── GET /api/calendar/deadlines
├── GET /api/calendar/statistics
└── GET /api/calendar/export/ical
```

---

## 🎓 LEARNING SYSTEM

```
/learning or /learning-dashboard
├── 📊 Smart Suggestions
│   ├── Based on user actions
│   ├── Time-of-day patterns
│   └── Success rate data
│
├── 💡 Quick Steps (Expandable)
│   ├── Next action recommendations
│   └── Human-friendly explanations
│
├── 📚 Learning Patterns
│   ├── 28 action sequences
│   ├── 16 success-rated actions
│   ├── 5 tenant success stories
│   └── 12 hourly activity patterns
│
└── 🎯 Progress Tracking
    ├── Actions completed
    ├── Success rate
    └── Time saved
```

---

## 🏛️ COMPLAINT FILING

```
/file-complaint (Main Interface)
├── 1️⃣ Identify Venues
│   └── POST /api/complaint/identify-venues
│
├── 2️⃣ Get Procedures
│   └── POST /api/complaint/get-procedures/<venue>
│
├── 3️⃣ Track Outcome
│   └── POST /api/complaint/track-outcome
│
├── 4️⃣ Update Procedure
│   └── POST /api/complaint/update-procedure
│
├── 📚 Library
│   └── /complaint-library (Past complaints)
│
└── ✅ Success Stories
    └── /filing-success-stories (What worked)
```

---

## 🏠 HOUSING PROGRAMS

```
/housing-programs (Main Hub)
├── 🔍 Search Programs
│   └── POST /api/programs/search
│
├── 📂 Browse by Category
│   └── GET /api/programs/category/<category>
│
├── 📖 Program Guide
│   └── GET /api/programs/guide/<program_id>
│
├── 📊 Track Outcome
│   └── POST /api/programs/track-outcome
│
├── 💪 Intensity Recommendations
│   └── POST /api/programs/intensity-recommendations
│
└── ✅ Eligibility Check
    └── POST /api/programs/eligibility-check
```

---

## 🔐 ADMIN PANEL

```
/admin (Main Dashboard)
├── 🎛️ Panels List (Grid Layout)
│   │
│   ├── 💾 Storage / Database (/admin/storage-db)
│   │   ├── SQLite file size
│   │   ├── R2 cloud status
│   │   ├── Sync to R2 (POST /admin/storage-db/sync)
│   │   └── Download DB (GET /admin/storage-db/download)
│   │
│   ├── 👥 Users Panel (/admin/users-panel)
│   │   ├── User list table
│   │   └── Export JSON (GET /admin/users-panel/export)
│   │
│   ├── 📧 Email Panel (/admin/email)
│   │   ├── Provider status (Ollama/SendGrid/etc)
│   │   └── Send test email (POST)
│   │
│   ├── 🔒 Security Panel (/admin/security)
│   │   ├── Security mode (open/enforced)
│   │   └── Breakglass flag status
│   │
│   ├── 🧠 Human Perspective (/admin/human)
│   │   ├── Test humanization
│   │   ├── Reading levels (plain→professional)
│   │   └── Audiences (tenant→judge)
│   │
│   └── 🎓 Learning Admin (/admin/learning)
│       ├── Prime learning (POST /admin/prime_learning)
│       ├── Reset learning (POST /admin/learning/reset)
│       └── Download patterns (GET /admin/learning/download)
│
├── 📊 Status (/admin/status)
├── 📜 Logs (/admin/logs)
└── 📈 Metrics (/admin/metrics)
```

---

## 🤖 AI / COPILOT

```
/copilot (Interface)
├── POST /api/copilot (Main API)
│   ├── Provider: Ollama (default)
│   ├── Alternative: OpenAI
│   └── Alternative: Azure
│
└── POST /api/evidence-copilot
    └── Evidence-specific AI assistance
```

---

## 📊 SYSTEM MONITORING

```
Health Checks:
├── /health or /healthz (JSON status)
├── /readyz (Readiness check)
│   ├── Database writable
│   ├── Runtime dirs accessible
│   └── Tokens loadable
│
└── /metrics (Prometheus format)
    ├── requests_total
    ├── admin_requests_total
    ├── errors_total
    ├── releases_total
    ├── rate_limited_total
    └── uptime_seconds
```

---

## 📸 AUDIO/VIDEO EVIDENCE

```
/av/ (Evidence Capture System)
├── 📹 Capture
│   ├── /av/capture/video (POST)
│   ├── /av/capture/audio (POST)
│   └── /av/capture/photo (POST)
│
├── 📥 Import
│   ├── /av/import/voicemail (POST)
│   ├── /av/import/text-message (POST)
│   ├── /av/import/email (POST)
│   └── /av/import/chat (POST)
│
└── 📤 Retrieve
    ├── /av/captures/<id>
    ├── /av/captures/type/<type>
    ├── /av/captures/actor/<actor_id>
    ├── /av/communications/phone/<number>
    ├── /av/communications/email/<email>
    ├── /av/evidence/summary
    └── /av/evidence/by-date
```

---

## 🔄 DATA FLOW ENGINE

```
/data-flow/ (Document Processing)
├── POST /data-flow/register-functions
│   └── Register processing functions
│
├── GET /data-flow/functions
│   └── List available functions
│
├── POST /data-flow/process-document
│   └── Process a document through pipeline
│
├── GET /data-flow/document/<id>/flow
│   └── Get document's processing history
│
├── GET /data-flow/actor/<id>/flow
│   └── Get actor's activity flow
│
├── GET /data-flow/registry
│   └── View function registry
│
└── GET /data-flow/statistics
    └── Processing statistics
```

---

## 🎨 ALTERNATIVE REGISTRATION VIEWS

```
Themed Registration Pages:
├── /register-navy (Navy blue theme)
├── /register-forest (Forest green theme)
├── /register-burgundy (Burgundy theme)
└── /register-slate (Slate gray theme)

API: POST /api/register/adaptive
```

---

## 🔗 NAVIGATION HIERARCHY

```
Level 1: Home
└── /

Level 2: Auth & Main Hub
├── /register → /verify → /dashboard
└── /login → /dashboard

Level 3: Major Sections (from dashboard)
├── /vault
├── /resources
├── /calendar-timeline
├── /learning-dashboard
├── /file-complaint
├── /housing-programs
└── /tools

Level 4: Feature Details
├── /vault → /notary → /certified_post → /court_clerk
├── /resources → [witness, packet, animal, checklist]
├── /calendar-timeline → [events, ledger, deadlines]
├── /tools → [complaint-gen, calculator, packet, rights]
└── /file-complaint → [venues, procedures, outcomes]

Level 5: Admin (separate auth)
└── /admin → [storage, users, email, security, human, learning]
```

---

## 📱 RESPONSIVE DESIGN NOTES

All templates should support:
- Desktop (full features)
- Tablet (optimized layout)
- Mobile (essential features, simplified nav)

Grid system used in:
- Dashboard layouts
- Admin panels
- Resource galleries
- Calendar views

---

## 🎯 KEY USER PATHS

### Path 1: New Tenant Needing Evidence
```
Home → Register → Dashboard → Vault → Upload Photos → Notarize → Download Certificate
```

### Path 2: Filing a Complaint
```
Home → Login → Dashboard → Complaint Filing → Identify Venue → Get Procedures → Track Outcome
```

### Path 3: Tracking Rent
```
Home → Login → Dashboard → Calendar → Rent Ledger → Add Payment → View History
```

### Path 4: Using Resources
```
Home → Login → Dashboard → Resources → Witness Statement → Fill Form → Save → Download
```

### Path 5: Admin Management
```
/admin (with token) → Storage Panel → Check R2 Status → Sync Database
```

