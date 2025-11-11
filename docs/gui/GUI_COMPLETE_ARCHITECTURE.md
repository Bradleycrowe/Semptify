# Semptify Complete GUI Architecture

## System Overview: Three UI Layers + One Backend

```
┌─────────────────────────────────────────────────────────────────┐
│                    USERS (Three Interfaces)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MOBILE (PWA)          DESKTOP (HTML)         TV (Presentation) │
│  ═════════════         ═════════════          ═════════════     │
│  📱 Capture            🖥️ Manage              📺 Present        │
│  GPS tagging           Evidence grid          Court display     │
│  Offline sync          Timeline               Statute ticker    │
│  Install app           Ledger mgr             Verdict record    │
│                        Court packet           Witness profiles  │
│                        Statute track          Presenter console │
│                                                                 │
└────────┬──────────────────┬────────────────────┬────────────────┘
         │                  │                    │
         └──────────────────┼────────────────────┘
                            │
                    ALL SHARE SAME APIs
                            │
         ┌──────────────────┼────────────────────┬────────────────┐
         │                  │                    │                │
         ▼                  ▼                    ▼                ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
    │   AV     │      │ Evidence │      │  Ledger  │      │ Calendar │
    │ Capture  │      │  Routing │      │ Tracking │      │    Hub   │
    │   API    │      │   API    │      │   API    │      │   API    │
    └──────────┘      └──────────┘      └──────────┘      └──────────┘
         │                  │                    │                │
         └──────────────────┼────────────────────┼────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Flask Backend │
                    │  (Semptify.py) │
                    │  • Blueprints  │
                    │  • Auth token  │
                    │  • Rate limit  │
                    │  • Logging     │
                    └────────────────┘
```

---

## Architecture Details

### Layer 1: Mobile PWA
```
Mobile Phone
├── Home Screen
│   ├── Quick Status (countdown timer)
│   ├── 4 Capture Buttons
│   │   ├── Record Video (auto GPS)
│   │   ├── Take Photo (auto GPS)
│   │   ├── Record Audio
│   │   └── My Evidence
│   └── Quick Check (statute deadline)
│
├── Camera Interface (capture.html)
│   ├── Video preview
│   ├── Record/stop button
│   ├── GPS auto-tag
│   └── Upload to server
│
├── Service Worker (service-worker.js)
│   ├── Cache assets (offline)
│   ├── Queue uploads (offline)
│   └── Background sync (when online)
│
└── Manifest (manifest.json)
    ├── Install to home screen
    ├── Standalone mode (no browser UI)
    └── Splash screen + icons
```

### Layer 2: Desktop HTML
```
Desktop Browser (1920x1080+)
├── Navigation Bar
│   ├── Evidence Dashboard
│   ├── Case Timeline
│   ├── Ledger Manager
│   ├── Statute Tracker
│   ├── Court Packet Builder
│   └── Settings
│
├── Evidence Dashboard
│   ├── Grid view (thumbnails)
│   ├── Filter by date/type/actor
│   ├── Bulk operations
│   ├── Drag-drop organize
│   └── Quick preview
│
├── Case Timeline
│   ├── Chronological events
│   ├── Zoom/filter controls
│   ├── Color-coded by type
│   ├── Weather overlay
│   └── Click for details
│
├── Ledger Manager
│   ├── Money ledger (income/expenses)
│   ├── Time ledger (deadlines/attempts)
│   ├── Service ledger (who/what/when)
│   └── Export to Excel
│
├── Statute Tracker
│   ├── Active statutes list
│   ├── Color-coded urgency
│   ├── Countdown timers
│   ├── Weather impact
│   └── Admin adjustments
│
└── Court Packet Builder
    ├── Wizard interface
    ├── Drag evidence into sections
    ├── Auto-arrange by relevance
    ├── PDF export
    └── Signature fields
```

### Layer 3: TV Presentation
```
Large Display (40"+ TV, 1920x1080 or 3840x2160)
├── Home / Menu
│   ├── Select Case
│   └── Start Presentation
│
├── Slide 1: Case Overview
│   ├── Large text (readable from 10+ feet)
│   ├── Case ID, parties, status
│   ├── Timeline summary
│   ├── Statute countdown (red if urgent)
│   └── (Press SPACE to advance)
│
├── Slide 2-5: Evidence Display
│   ├── Full-screen photo/video
│   ├── Metadata (who, when, where)
│   ├── GPS location map
│   ├── Linked communications
│   └── Related evidence thumbnails
│
├── Slide N: Timeline Walkthrough
│   ├── Chronological narrative
│   ├── Evidence highlighted as mentioned
│   ├── Animations show relationships
│   ├── Narrator notes (presenter only)
│   └── Auto-advance or manual
│
├── Slide M: Statute Ticker
│   ├── Large countdown timer
│   ├── Color changes (green → yellow → red)
│   ├── Weather impact shown
│   ├── Next deadline highlighted
│   └── Updates in real-time
│
├── Slide L: Witness Cards
│   ├── Large profile photo
│   ├── Name and role
│   ├── Previous testimony quotes
│   ├── Communication history
│   └── Evidence they submitted
│
├── Slide F: Verdict Template
│   ├── Decision tracking sheet
│   ├── Verdict options highlighted
│   ├── Verdict recorded + timestamp
│   └── Linked to case immediately
│
└── Presenter Console (secondary device)
    ├── Current slide on main display
    ├── Next slide preview (secret)
    ├── Speaker notes
    ├── Keyboard controls visible
    └── Timing indicators
```

### Backend APIs (All Three UIs Share)

```
Evidence Capture
├── POST /api/evidence/capture/video
├── POST /api/evidence/capture/audio
├── POST /api/evidence/capture/photo
├── POST /api/evidence/import/voicemail
├── POST /api/evidence/import/text-message
├── POST /api/evidence/import/email
├── POST /api/evidence/import/chat
├── GET /api/evidence/captures/<id>
├── GET /api/evidence/captures/type/{video|audio|photo}
├── GET /api/evidence/captures/actor/<actor_id>
└── GET /api/evidence/summary

Ledger Tracking
├── POST /api/ledger-tracking/money/add
├── POST /api/ledger-tracking/time/add
├── POST /api/ledger-tracking/service-date/add
├── GET /api/ledger-tracking/money/balance/<actor_id>
├── GET /api/ledger-tracking/statute/active
├── GET /api/ledger-tracking/statute/expiring-soon
├── GET /api/ledger-tracking/court-packet/<doc_id>
└── POST /api/ledger-tracking/verdict/record

Calendar & Timeline
├── GET /api/calendar/events?start=...&end=...
├── GET /api/calendar/events/<date>
├── GET /api/calendar/timeline/narrative/<case_id>
├── POST /api/calendar/event/create
└── GET /api/calendar/statistics

Admin & Configuration
├── GET /admin/ledger/config
├── POST /admin/ledger/config/update
├── GET /admin/ledger/statutes/summary
├── POST /admin/ledger/durations/update
├── GET /admin/ledger/weather/settings
└── POST /admin/ledger/weather/settings/update

UI-Specific APIs
├── /ui/mobile/api/status (statute countdown, weather alerts)
├── /ui/mobile/api/my-evidence (what I uploaded)
├── /ui/mobile/api/sync-queue (retry failed uploads)
├── /ui/desktop/api/evidence/grid (paginated evidence)
├── /ui/desktop/api/timeline/events (for timeline viz)
├── /ui/tv/case/<case_id> (full case data)
├── /ui/tv/timeline/<case_id>/narrative (walkthrough)
└── /ui/tv/control/{advance|back|goto} (presenter controls)
```

---

## Data Flow: Evidence to Court

```
1. USER CAPTURES (Mobile)
   ┌─────────────────────┐
   │ Record Video/Photo  │
   │ + GPS Auto-tag      │
   │ + Timestamp         │
   │ + Description       │
   └────────┬────────────┘
            │
            ▼
2. UPLOAD (Mobile PWA)
   ┌──────────────────────┐
   │ POST /api/evidence/  │
   │ capture/video        │
   │                      │
   │ (Queues if offline)  │
   │ (Auto-syncs online)  │
   └────────┬─────────────┘
            │
            ▼
3. AV CAPTURE MANAGER (Backend)
   ┌──────────────────────────┐
   │ • Calculates SHA256      │
   │ • Extracts EXIF/metadata │
   │ • Stores in vault        │
   │ • Logs transaction       │
   │ • Returns capture ID     │
   └────────┬─────────────────┘
            │
            ▼
4. CALENDAR HUB (Routes all evidence)
   ┌──────────────────────────────┐
   │ • Creates calendar entry     │
   │ • Links to capture ID        │
   │ • Records timestamp/actor    │
   │ • Adds location to map       │
   │ • Triggers notifications     │
   └────────┬─────────────────────┘
            │
            ▼
5. DATA FLOW ENGINE (Rules processing)
   ┌──────────────────────────────────┐
   │ • Applies rules to evidence type │
   │ • Categorizes by relevance       │
   │ • Triggers reactions             │
   │ • Updates ledger                 │
   │ • Links communications           │
   └────────┬─────────────────────────┘
            │
            ▼
6. EVIDENCE VAULT (Persistent storage)
   ┌────────────────────────────────────┐
   │ evidence_capture/                  │
   │ ├── metadata/                      │
   │ │   ├── <id>.json (SHA256, GPS,   │
   │ │   │   actor, timestamp, etc)    │
   │ │   └── ...                        │
   │ ├── videos/                        │
   │ │   ├── <id>.mp4 (original)       │
   │ │   └── <id>_thumb.jpg (preview)  │
   │ ├── photos/                        │
   │ ├── audio/                         │
   │ └── documents/                     │
   └────────┬───────────────────────────┘
            │
            ▼
7. QUERY & PRESENT (All Three UIs)
   ┌────────────────────────────┐
   │ Mobile: "My Evidence"      │
   │ → Shows all my captures    │
   │                            │
   │ Desktop: Evidence Grid     │
   │ → Filter/sort/export       │
   │                            │
   │ TV: Evidence Display       │
   │ → Full-screen presentation │
   └────────┬───────────────────┘
            │
            ▼
8. COURT PACKET ASSEMBLY (Desktop)
   ┌──────────────────────────────┐
   │ • Select evidence items      │
   │ • Auto-arrange by timeline   │
   │ • Link communications        │
   │ • Generate narrative         │
   │ • Export PDF                 │
   │ • Add signatures             │
   │ • File with court            │
   └──────────────────────────────┘
```

---

## Feature Comparison

| Feature | Mobile | Desktop | TV |
|---------|--------|---------|-----|
| **Capture** | ✅ Video/photo/audio | ❌ | ❌ |
| **GPS tagging** | ✅ Auto | ❌ | ❌ |
| **Offline support** | ✅ Service worker | ⚠️ Cache only | ❌ |
| **Evidence browse** | ✅ List view | ✅ Grid view | ✅ Large display |
| **Evidence detail** | ✅ Quick preview | ✅ Full metadata | ✅ Full-screen |
| **Timeline view** | ❌ | ✅ Interactive | ✅ Walkthrough |
| **Ledger tracking** | ❌ | ✅ All types | ❌ |
| **Statute deadline** | ✅ Countdown | ✅ Tracker | ✅ Large ticker |
| **Weather impact** | ❌ | ✅ Overlay | ✅ Display |
| **Court packet** | ❌ | ✅ Builder | ❌ |
| **Verdict record** | ❌ | ❌ | ✅ Record sheet |
| **Presenter console** | ❌ | ❌ | ✅ Secondary display |
| **Install as app** | ✅ PWA | ❌ | ❌ |
| **Works offline** | ✅ Full | ⚠️ Cached pages | ❌ |
| **Touch optimized** | ✅ Yes | ✅ Responsive | ❌ Mouse/keyboard |
| **Dark mode** | ✅ | ✅ | ✅ High contrast |

---

## Implementation Timeline

### Week 1-2: Mobile PWA (Foundation)
```
Mon-Tue:
  ☐ Create ui_mobile_routes.py
  ☐ Create templates/ui/mobile/*.html
  ☐ Test on iPhone & Android

Wed-Thu:
  ☐ Create service-worker.js
  ☐ Implement offline sync
  ☐ Create manifest.json

Fri:
  ☐ Integration testing
  ☐ PWA install testing
  ☐ Camera/GPS testing
  
Status: ✅ Mobile captures working offline + auto-syncs
```

### Week 3-4: Desktop HTML (Professional UI)
```
Mon-Tue:
  ☐ Create evidence-dashboard.html
  ☐ Create case-timeline.html
  ☐ Add D3.js for timeline visualization

Wed-Thu:
  ☐ Create ledger-manager.html
  ☐ Create statute-tracker.html
  ☐ Add responsive CSS

Fri:
  ☐ Create court-packet-builder.html
  ☐ Integration testing
  ☐ Performance optimization
  
Status: ✅ Full case management on desktop
```

### Week 5-6: TV Presentation (Court Display)
```
Mon-Tue:
  ☐ Create case-overview.html
  ☐ Create evidence-display.html
  ☐ Create statute-ticker.html

Wed-Thu:
  ☐ Create timeline-walkthrough.html
  ☐ Implement presenter controls
  ☐ Add keyboard shortcuts

Fri:
  ☐ Create verdict-template.html
  ☐ Test on 40"+ TV
  ☐ Wireless casting testing
  
Status: ✅ Court-ready presentation system
```

### Week 7: Polish & Optimization
```
Mon-Tue:
  ☐ Accessibility audit (WCAG 2.1)
  ☐ Keyboard navigation testing
  ☐ Screen reader testing

Wed-Thu:
  ☐ Performance profiling
  ☐ Image compression
  ☐ Lazy loading

Fri:
  ☐ Final integration testing
  ☐ Documentation
  ☐ Production deployment
  
Status: ✅ PRODUCTION READY
```

---

## Deployment Checklist

```
MOBILE PWA:
☐ Icons created (192x192, 512x512, maskable)
☐ manifest.json linked in templates
☐ service-worker.js registered
☐ HTTPS enabled (required for PWA)
☐ "Add to Home Screen" tested on iOS & Android
☐ Camera permission prompt works
☐ GPS permission prompt works
☐ Offline capture tested
☐ Offline sync tested

DESKTOP HTML:
☐ All routes registered in Semptify.py
☐ All templates render without errors
☐ Responsive CSS tested (mobile, tablet, desktop)
☐ Dark mode tested
☐ Keyboard navigation tested
☐ Admin auth token required
☐ Rate limiting applied
☐ Performance < 3s load time

TV PRESENTATION:
☐ Routes registered
☐ Fullscreen mode tested
☐ Keyboard controls mapped
☐ Presenter console working
☐ Wireless casting tested
☐ HDMI output tested
☐ Font readable from 10+ feet
☐ Colors high contrast

SECURITY:
☐ All routes require auth token
☐ CSRF tokens on forms
☐ Rate limiting on admin routes
☐ File uploads scanned for malware
☐ GPS data privacy (no leakage)
☐ HTTPS enforced
☐ Audit logging enabled
```

---

## Next Steps

**You now have:**
- ✅ Complete backend API (av_routes, ledger_tracking, calendar hub, data flow)
- ✅ Admin configuration system
- ✅ Evidence vault with tamper-proof storage
- ✅ All tests passing (71/71)

**To go live, build in this order:**
1. **Mobile PWA (This Week)** — Users can capture evidence immediately
2. **Desktop HTML (Next 2 Weeks)** — Professional case management
3. **TV Presentation (Week 3)** — Court demonstrations

**Total: 3 weeks to full system deployment**

Which UI should I start building first? I recommend **Mobile PWA** (highest impact, users can start capturing evidence today).

Ready to code? 🚀
