# Semptify GUI Strategy - Desktop, Mobile & TV Presentation

## Overview

Three-platform UI strategy with responsive design:

| Platform | Technology | Use Case | Deployment |
|----------|-----------|----------|-----------|
| **Desktop HTML** | Flask + Responsive HTML/CSS/JS | Case management, evidence review, configuration | `http://localhost:5000` |
| **Mobile Web** | Progressive Web App (PWA) | Evidence capture, quick access, on-field use | Android/iOS browsers + installable app |
| **TV Presentation** | Dedicated presentation mode | Court presentations, jury display, evidence walkthrough | Large screen display output |

---

## 1. DESKTOP HTML GUI

### Architecture

```
Semptify.py (Flask)
├── /ui/desktop/* (new routes)
├── templates/ui/desktop/
│   ├── evidence-dashboard.html
│   ├── case-timeline.html
│   ├── ledger-manager.html
│   ├── statute-tracker.html
│   └── court-packet-builder.html
├── static/js/ui/desktop/
│   ├── dashboard.js
│   ├── timeline.js
│   ├── evidence-grid.js
│   └── packet-builder.js
└── static/css/ui/desktop/
    ├── dashboard.css
    ├── timeline.css
    └── responsive.css
```

### Key Desktop Features

**1. Evidence Dashboard**
- Grid view of all captured evidence (photos, videos, audio, documents)
- Filter by: date range, type, actor, location, status
- Bulk operations: tag, organize, export
- Drag-drop to organize evidence
- Quick preview panel on hover

**2. Interactive Timeline**
- Chronological view of all events (evidence + communications)
- Timeline bar shows date range with zoom controls
- Click event to see details + linked evidence
- Color-coded by type (evidence, communication, statute, service)
- Weather conditions overlaid (shows service pauses)

**3. Ledger Manager**
- Money ledger: income/expenses, balances, interest calculations
- Time ledger: service attempts, deadlines, statute tracking
- Service ledger: who served what when
- Export to spreadsheet (CSV, Excel)
- Automatic calculations

**4. Statute Tracker**
- Dashboard showing all active statutes
- Color-coded by urgency (expires soon = red)
- Admin panel to adjust durations by jurisdiction
- Weather impact visualization
- Alert thresholds configurable

**5. Court Packet Builder**
- Wizard interface to assemble court filings
- Drag evidence into sections
- Auto-arrange by relevance
- PDF export with formatting
- Signature field placeholders
- Page numbering + table of contents

### Desktop UI Routes

```python
# New routes in Semptify.py or ui_routes.py

@app.route('/ui/desktop/evidence')
def desktop_evidence_dashboard():
    # List all evidence with filters
    return render_template('ui/desktop/evidence-dashboard.html')

@app.route('/ui/desktop/timeline')
def desktop_timeline():
    # Interactive timeline with zoom/filter
    return render_template('ui/desktop/case-timeline.html')

@app.route('/ui/desktop/ledger')
def desktop_ledger():
    # Financial/time ledger manager
    return render_template('ui/desktop/ledger-manager.html')

@app.route('/ui/desktop/statutes')
def desktop_statutes():
    # Statute tracking and deadline monitor
    return render_template('ui/desktop/statute-tracker.html')

@app.route('/ui/desktop/packet')
def desktop_packet_builder():
    # Court packet assembly wizard
    return render_template('ui/desktop/court-packet-builder.html')

# API routes for desktop UI
@app.route('/api/ui/evidence/grid')
def api_evidence_grid():
    # Return paginated evidence list with thumbnails
    return jsonify(evidence_list)

@app.route('/api/ui/timeline/events')
def api_timeline_events():
    # Return events for timeline display
    return jsonify(events)

@app.route('/api/ui/packet/assemble', methods=['POST'])
def api_packet_assemble():
    # Build court packet from selected evidence
    return jsonify(packet)
```

---

## 2. MOBILE WEB GUI (PWA)

### Architecture

```
Mobile-First Design
├── /ui/mobile/* (routes)
├── templates/ui/mobile/
│   ├── capture.html (video/audio/photo/comms)
│   ├── my-evidence.html (what I uploaded)
│   ├── quick-check.html (statue/deadline status)
│   ├── settings.html (preferences)
│   └── offline.html (when no connection)
├── static/js/ui/mobile/
│   ├── camera-capture.js (mobile camera API)
│   ├── offline-sync.js (queue uploads when offline)
│   ├── geolocation.js (auto GPS tagging)
│   └── service-worker.js (PWA caching)
└── static/css/ui/mobile/
    ├── mobile-first.css
    └── touch-optimized.css
```

### Key Mobile Features

**1. One-Tap Evidence Capture**
```
Home Screen
├── Record Video (30s/60s/unlimited)
├── Take Photo (auto GPS tag)
├── Record Audio (background OK)
├── Upload Evidence (existing)
└── Quick Status Check
```

**2. My Evidence**
- List of uploads I made
- Status (uploading, synced, processing)
- Retry failed uploads
- Local cache for offline access

**3. Quick Check**
- Statute expiration countdown
- Next deadline
- Unserved parties
- Weather alerts

**4. Settings**
- Auto-GPS on/off
- Upload quality (video bitrate, photo resolution)
- Notification preferences
- Offline mode
- Account settings

**5. Offline Capability**
- Queue captures while offline
- Auto-sync when connection returns
- Local timestamps preserved
- No data loss

### Mobile PWA Service Worker

```javascript
// service-worker.js - Offline access & caching

// Cache API assets on install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('semptify-mobile-v1').then((cache) => {
      return cache.addAll([
        '/ui/mobile/capture.html',
        '/static/js/ui/mobile/camera-capture.js',
        '/static/css/ui/mobile/mobile-first.css',
        '/offline.html'
      ]);
    })
  );
});

// Network-first, fallback to cache
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          caches.open('semptify-mobile-v1').then((cache) => {
            cache.put(event.request, response.clone());
          });
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

// Background sync for queued uploads
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-evidence') {
    event.waitUntil(syncQueuedEvidenceUploads());
  }
});
```

### Mobile Routes

```python
@app.route('/ui/mobile')
def mobile_home():
    return render_template('ui/mobile/capture.html')

@app.route('/ui/mobile/capture')
def mobile_capture():
    # Camera/audio/document capture interface
    return render_template('ui/mobile/capture.html')

@app.route('/ui/mobile/my-evidence')
def mobile_my_evidence():
    # What I've uploaded
    return render_template('ui/mobile/my-evidence.html')

@app.route('/ui/mobile/quick-check')
def mobile_quick_check():
    # Statute/deadline status
    return render_template('ui/mobile/quick-check.html')

@app.route('/ui/mobile/offline')
def mobile_offline():
    # Fallback when offline
    return render_template('ui/mobile/offline.html')

# API routes
@app.route('/api/ui/mobile/status')
def api_mobile_status():
    # User's statute/deadline info
    return jsonify(status)

@app.route('/api/ui/mobile/sync-queue', methods=['GET'])
def api_mobile_sync_queue():
    # What's queued locally? (for retry)
    return jsonify(queue)
```

---

## 3. TV PRESENTATION MODE

### Architecture

```
TV Mode (Full Screen, Large Text, High Contrast)
├── /ui/tv/* (routes)
├── templates/ui/tv/
│   ├── case-overview.html (full case summary)
│   ├── evidence-display.html (large format evidence)
│   ├── timeline-walkthrough.html (chronological narrative)
│   ├── statute-ticker.html (countdown for court)
│   ├── witness-card.html (speaker profiles + history)
│   └── verdict-template.html (decision tracking)
├── static/js/ui/tv/
│   ├── presentation-control.js (keyboard controls)
│   ├── auto-advance.js (timed transitions)
│   └── speaker-notes.js (presenter console)
└── static/css/ui/tv/
    ├── tv-fullscreen.css (large text, high contrast)
    └── presentation.css (timing animations)
```

### Key TV Features

**1. Case Overview Slide**
```
┌─────────────────────────────────────┐
│         CASE OVERVIEW               │
│                                     │
│ Case ID: EVT-2025-001              │
│ Parties: Smith v. Johnson           │
│ Status: Evidence Phase              │
│ Timeline: 180 days (60 remaining)   │
│                                     │
│ Key Dates:                          │
│ • Service Deadline: Jan 15, 2025    │
│ • Response Due: Feb 1, 2025         │
│ • Trial Date: May 1, 2025           │
│                                     │
│ Statute: 3 years (2 years 11 mo)   │
│                                     │
│ (Press SPACE to advance)            │
└─────────────────────────────────────┘
```

**2. Evidence Display (Full Screen)**
- Large photo/video with metadata
- Timestamp + location
- Actor who captured it
- Linked communications
- Zoom controls for details

**3. Timeline Walkthrough**
- Chronological narrative (paragraph format)
- Evidence highlighted as mentioned
- Animations show relationships
- Narrator notes visible to presenter
- Auto-advance or manual control

**4. Statute Ticker**
- Large countdown timer
- Color changes: green → yellow → red
- Weather impact shown
- Next deadline highlighted
- Updates in real-time

**5. Witness Card**
- Large profile photo/name
- Previous testimony quotes
- Communication history with this person
- Evidence they submitted
- Credibility indicators

**6. Verdict Template**
- Decision tracking sheet
- Verdict options highlighted
- Verdict recorded with timestamp
- Immediately linked to case

### TV Routes & Controls

```python
@app.route('/ui/tv/case/<case_id>')
def tv_case_overview(case_id):
    # Full case summary in presentation format
    return render_template('ui/tv/case-overview.html', case_id=case_id)

@app.route('/ui/tv/evidence/<evidence_id>')
def tv_evidence_display(evidence_id):
    # Single evidence item large format
    return render_template('ui/tv/evidence-display.html', 
                          evidence_id=evidence_id)

@app.route('/ui/tv/timeline/<case_id>')
def tv_timeline_walkthrough(case_id):
    # Narrative walkthrough
    return render_template('ui/tv/timeline-walkthrough.html', 
                          case_id=case_id)

@app.route('/ui/tv/statute/<case_id>')
def tv_statute_ticker(case_id):
    # Live countdown timer
    return render_template('ui/tv/statute-ticker.html', 
                          case_id=case_id)

@app.route('/ui/tv/witness/<witness_id>')
def tv_witness_card(witness_id):
    # Speaker profile
    return render_template('ui/tv/witness-card.html', 
                          witness_id=witness_id)

@app.route('/ui/tv/verdict/<case_id>')
def tv_verdict_template(case_id):
    # Verdict recording sheet
    return render_template('ui/tv/verdict-template.html', 
                          case_id=case_id)

# TV-specific API
@app.route('/api/ui/tv/case/<case_id>')
def api_tv_case_full(case_id):
    # All case data for presentation
    return jsonify(full_case_data)

@app.route('/api/ui/tv/timeline/<case_id>/narrative')
def api_tv_timeline_narrative(case_id):
    # Chronological narrative with linked evidence
    return jsonify(narrative)

@app.route('/api/ui/tv/statute/<case_id>/countdown')
def api_tv_statute_countdown(case_id):
    # Real-time countdown data
    return jsonify(countdown)

# Presenter controls
@app.route('/api/ui/tv/control/advance', methods=['POST'])
def api_tv_control_advance():
    # Next slide (keyboard or network)
    return jsonify({"status": "ok", "current_slide": next_slide})

@app.route('/api/ui/tv/control/back', methods=['POST'])
def api_tv_control_back():
    # Previous slide
    return jsonify({"status": "ok", "current_slide": prev_slide})

@app.route('/api/ui/tv/control/goto', methods=['POST'])
def api_tv_control_goto():
    # Jump to slide
    slide_num = request.json.get('slide')
    return jsonify({"status": "ok", "current_slide": slide_num})
```

### TV Presentation Control

```javascript
// presentation-control.js - Keyboard & remote controls

document.addEventListener('keydown', (e) => {
  if (e.code === 'ArrowRight' || e.code === 'Space') {
    advanceSlide();
  } else if (e.code === 'ArrowLeft') {
    previousSlide();
  } else if (e.key.match(/[0-9]/)) {
    // Jump to slide (number keys)
    gotoSlide(parseInt(e.key));
  } else if (e.code === 'Escape') {
    exitPresentation();
  }
});

// Presenter console (separate window)
window.presenterConsole = {
  currentSlide: 0,
  notes: [],
  
  advance: async function() {
    const response = await fetch('/api/ui/tv/control/advance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    this.currentSlide = data.current_slide;
    updatePresenterDisplay();
  },
  
  back: async function() {
    const response = await fetch('/api/ui/tv/control/back', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    this.currentSlide = data.current_slide;
    updatePresenterDisplay();
  },
  
  goto: async function(slideNum) {
    const response = await fetch('/api/ui/tv/control/goto', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slide: slideNum })
    });
    const data = await response.json();
    this.currentSlide = data.current_slide;
    updatePresenterDisplay();
  }
};

// Auto-advance with timing
function enableAutoAdvance(delaySeconds) {
  setInterval(() => {
    window.presenterConsole.advance();
  }, delaySeconds * 1000);
}
```

---

## 4. RESPONSIVE LAYOUT STRATEGY

### CSS Breakpoints

```css
/* Mobile first - then expand */

/* Mobile: < 600px */
@media (max-width: 600px) {
  .container { padding: 10px; }
  .sidebar { display: none; }
  .grid { grid-template-columns: 1fr; }
  font-size: 16px;
}

/* Tablet: 600px - 1024px */
@media (min-width: 600px) {
  .container { max-width: 90%; }
  .grid { grid-template-columns: repeat(2, 1fr); }
  font-size: 14px;
}

/* Desktop: > 1024px */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
  .sidebar { display: flex; width: 250px; }
  .grid { grid-template-columns: repeat(3, 1fr); }
  font-size: 13px;
}

/* TV Presentation: > 1920px + fullscreen */
@media (min-width: 1920px) and (display-mode: fullscreen) {
  .container { width: 100vw; height: 100vh; }
  .grid { grid-template-columns: repeat(4, 1fr); }
  font-size: 28px;
  line-height: 1.8;
}
```

### Touch-Optimized Mobile

```css
/* Mobile-specific optimizations */

@media (hover: none) and (pointer: coarse) {
  /* Touch devices */
  
  button, .clickable {
    min-height: 44px;
    min-width: 44px;
    padding: 15px;
    font-size: 18px;
  }
  
  .grid-item {
    aspect-ratio: 1;
    margin: 8px;
  }
  
  .modal {
    width: 95%;
    max-height: 90vh;
  }
  
  input, textarea {
    font-size: 16px; /* Prevent zoom on iOS */
    padding: 12px;
  }
}
```

---

## 5. IMPLEMENTATION ROADMAP

### Phase 1: Desktop HTML (Weeks 1-2)
- [ ] Create `ui_routes.py` with desktop routes
- [ ] Build evidence dashboard UI
- [ ] Build interactive timeline
- [ ] Build ledger manager
- [ ] Add responsive CSS

### Phase 2: Mobile PWA (Weeks 3-4)
- [ ] Create mobile routes
- [ ] Implement camera capture UI
- [ ] Add geolocation auto-tagging
- [ ] Build service worker (offline sync)
- [ ] Create manifest.json for installability

### Phase 3: TV Presentation (Weeks 5-6)
- [ ] Create TV routes
- [ ] Build case overview slide
- [ ] Build evidence display (fullscreen)
- [ ] Implement slide controls (keyboard + network)
- [ ] Build statute ticker
- [ ] Test on large screen

### Phase 4: Polish & Integration (Week 7)
- [ ] Add keyboard shortcuts reference
- [ ] Implement theme switcher (dark/light)
- [ ] Add accessibility features (ARIA labels, keyboard nav)
- [ ] Performance optimization (lazy loading, compression)
- [ ] Mobile app store packaging

---

## 6. TECHNOLOGY STACK

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend Routes** | Flask Blueprints | Already in use; modular |
| **Frontend (Desktop)** | HTML5/CSS3/Vanilla JS | No extra dependencies; responsive |
| **Interactive Graphs** | D3.js or Chart.js | Timeline, statute countdown, evidence grid |
| **Mobile Capture** | getUserMedia API | Browser-native camera access |
| **Offline Support** | Service Workers | PWA standard for offline-first |
| **State Management** | Fetch API + localStorage | Simple, no Redux needed |
| **Icons** | Font Awesome or SVG | Lightweight, scalable |
| **Video Playback** | HTML5 <video> | Native, no plugins |
| **PDF Export** | html2pdf.js | Client-side PDF generation |
| **Real-time Countdown** | WebSockets or polling | Statute ticker updates |

---

## 7. KEY FILES TO CREATE

```
NEW ROUTE FILE:
├── ui_routes.py (300+ lines)
│   ├── Desktop routes (evidence, timeline, ledger, statutes, packet)
│   ├── Mobile routes (capture, my-evidence, quick-check)
│   └── TV routes (case overview, evidence display, timeline, verdict)

DESKTOP TEMPLATES:
├── templates/ui/desktop/
│   ├── evidence-dashboard.html (300+ lines)
│   ├── case-timeline.html (250+ lines)
│   ├── ledger-manager.html (200+ lines)
│   ├── statute-tracker.html (200+ lines)
│   └── court-packet-builder.html (300+ lines)

MOBILE TEMPLATES:
├── templates/ui/mobile/
│   ├── capture.html (250+ lines)
│   ├── my-evidence.html (200+ lines)
│   ├── quick-check.html (150+ lines)
│   ├── settings.html (180+ lines)
│   └── offline.html (100+ lines)

TV TEMPLATES:
├── templates/ui/tv/
│   ├── case-overview.html (200+ lines)
│   ├── evidence-display.html (200+ lines)
│   ├── timeline-walkthrough.html (300+ lines)
│   ├── statute-ticker.html (150+ lines)
│   ├── witness-card.html (180+ lines)
│   └── verdict-template.html (150+ lines)

JAVASCRIPT:
├── static/js/ui/desktop/
│   ├── dashboard.js (150+ lines)
│   ├── timeline.js (200+ lines)
│   ├── evidence-grid.js (150+ lines)
│   └── packet-builder.js (180+ lines)
├── static/js/ui/mobile/
│   ├── camera-capture.js (200+ lines)
│   ├── offline-sync.js (150+ lines)
│   ├── geolocation.js (100+ lines)
│   └── service-worker.js (150+ lines)
├── static/js/ui/tv/
│   ├── presentation-control.js (200+ lines)
│   ├── auto-advance.js (100+ lines)
│   └── speaker-notes.js (150+ lines)

CSS:
├── static/css/ui/desktop/
│   ├── dashboard.css (150+ lines)
│   ├── timeline.css (180+ lines)
│   └── responsive.css (200+ lines)
├── static/css/ui/mobile/
│   ├── mobile-first.css (200+ lines)
│   └── touch-optimized.css (150+ lines)
└── static/css/ui/tv/
    ├── tv-fullscreen.css (180+ lines)
    └── presentation.css (150+ lines)

MANIFEST & CONFIG:
├── manifest.json (PWA app manifest)
├── service-worker.js (offline caching)
└── tv-controls.config.json (keyboard mappings, timing)

TOTAL: ~5500 lines of new UI code
```

---

## 8. INTEGRATION CHECKLIST

```
DESKTOP GUI:
☐ Register ui_routes_bp in Semptify.py
☐ /ui/desktop/evidence → evidence-dashboard.html
☐ /ui/desktop/timeline → case-timeline.html
☐ /ui/desktop/ledger → ledger-manager.html
☐ /ui/desktop/statutes → statute-tracker.html
☐ /ui/desktop/packet → court-packet-builder.html
☐ Add API routes: /api/ui/evidence/grid, /api/ui/timeline/events, etc.

MOBILE PWA:
☐ /ui/mobile routes registered
☐ manifest.json created and linked
☐ service-worker.js registered
☐ Camera API integration tested
☐ Offline sync tested
☐ Add to home screen tested on iOS & Android

TV PRESENTATION:
☐ /ui/tv/case/<case_id> route
☐ /ui/tv/evidence/<evidence_id> route
☐ /ui/tv/timeline/<case_id> route
☐ Presenter control API working
☐ Keyboard controls mapped
☐ Tested on 40"+ TV display
☐ HDMI/wireless casting working

COMMON:
☐ Navigation menu updated (/ui/desktop, /ui/mobile, /ui/tv)
☐ Responsive CSS tested on all breakpoints
☐ Accessibility tested (ARIA, keyboard nav, screen reader)
☐ Performance optimized (lazy loading, image compression)
☐ Security: all UI routes require auth token
☐ Logging: all user actions tracked
```

---

## 9. USER FLOWS

### Desktop User Journey

```
1. Login to https://semptify.example.com
2. Land on home page with quick stats
3. Click "Evidence" → evidence-dashboard
   • Filter by date/type/actor
   • Click evidence → preview + metadata
   • Drag to organize into collections
4. Click "Timeline" → case-timeline
   • See all events chronologically
   • Zoom to specific period
   • Hover over event → linked evidence
5. Click "Ledger" → ledger-manager
   • View money/time/service ledgers
   • Add new transaction
   • Export to Excel
6. Click "Statutes" → statute-tracker
   • See all deadlines
   • Color-coded by urgency
   • Admin adjust if needed
7. Click "Build Packet" → court-packet-builder
   • Select evidence items
   • Arrange in sections
   • Add narrative text
   • Export PDF with signatures
8. Submit court packet
```

### Mobile User Journey

```
1. Open https://semptify.example.com/ui/mobile
2. Tap "Capture Video" → camera app opens
   • Records video
   • Auto-tags GPS location
   • Auto-timestamps
3. Tap "Capture Photo" → photo app opens
   • Takes photo
   • EXIF preserved
4. Tap "Upload Evidence" → file picker
   • Select from device storage
   • Add description
   • Tap "Upload"
5. Tap "My Evidence" → see uploads
   • Status: uploading, synced, etc.
   • Retry if failed
6. Tap "Quick Check" → statute countdown
   • Days remaining
   • Next deadline
   • Weather alerts
7. Offline capture still works
   • Queue stored locally
   • Auto-syncs when online
8. Install app to home screen
   • "Add to Home Screen" prompt
   • Works like native app
```

### TV Presentation Journey

```
1. Lawyer launches https://semptify.example.com/ui/tv/case/EVT-001
2. Case overview slide displays (large text, high contrast)
   • Case ID, parties, dates, statute countdown
3. Press SPACE or arrow keys to advance
4. Evidence slide: large photo/video display
   • Metadata: who, when, where
   • Next: related communications
5. Timeline slide: narrative paragraph
   • Events highlighted as mentioned
   • Evidence thumbnails linked
6. Next: statute ticker (live countdown)
   • Red background if < 7 days
   • Updates in real-time
7. Witness card: speaker profile
   • Photo + name
   • Previous statements
   • Communication history
8. Next: verdict template
   • Judge/jury records decision
   • Linked to case immediately
9. Presenter console (separate window/device)
   • Shows current slide
   • Speaker notes
   • Next slide preview
   • Keyboard controls visible
```

---

## 10. BROWSER SUPPORT & TESTING

| Browser | Desktop | Mobile | TV | Notes |
|---------|---------|--------|----|----|
| Chrome | ✅ | ✅ | ✅ | Full support, PWA ready |
| Firefox | ✅ | ✅ | ✅ | Full support |
| Safari | ✅ | ✅ | ✅ | iOS 13.4+ for PWA |
| Edge | ✅ | ✅ | ✅ | Full support |
| Samsung TV | - | - | ✅ | Tizen browser |
| LG TV | - | - | ✅ | WebOS browser |

### Testing Checklist

```
DESKTOP:
☐ Chrome 1920x1080 (primary)
☐ Firefox 1920x1080
☐ Safari Mac 1440x900
☐ Edge Windows 1920x1080
☐ Tab through all elements (keyboard nav)
☐ Screen reader test (NVDA on Windows)

MOBILE:
☐ iPhone 12 (375x812) - Safari
☐ iPhone SE (375x667) - Safari
☐ Pixel 5 (393x851) - Chrome
☐ Galaxy S21 (360x800) - Chrome
☐ Camera API working
☐ Geolocation working
☐ Offline mode working
☐ Service worker installed
☐ Install to home screen working

TV:
☐ 40" Samsung TV 1920x1080
☐ 55" LG TV 3840x2160
☐ Presentation control working
☐ Font readable from 10+ feet
☐ Colors high contrast
☐ Keyboard controls responsive
☐ Wireless casting working (Chromecast/AirPlay)
```

---

## Summary

**Your three-tier GUI strategy:**

1. **Desktop HTML** (professional case management)
   - Evidence dashboard, timeline, ledger manager, statute tracker, court packet builder
   - Responsive, keyboard-friendly, dark mode option

2. **Mobile PWA** (field capture, quick status check)
   - One-tap video/photo/audio capture
   - Auto GPS tagging, offline sync, installable app
   - Fast & lightweight

3. **TV Presentation** (court demonstrations)
   - Full-screen case overview, evidence display, timeline walkthrough
   - Live statute countdown, witness cards, verdict recording
   - Presenter controls + speaker console

**All three interfaces feed the same backend APIs** — evidence captured on mobile syncs to desktop, displayed on TV. Complete integration.

Ready to build? Choose your starting point:
- Desktop first (most complex)
- Mobile first (highest priority for field use)
- TV first (most impressive demo)

Which phase should I start building?
