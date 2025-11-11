# 🎨 Semptify GUI Versions - Desktop, Mobile, TV

## Quick Comparison

| Feature | **DESKTOP** | **MOBILE** | **TV/PRESENTATION** |
|---------|-----------|-----------|-------------------|
| **Platform** | PyQt5 (native) | PWA (browser) | Full-screen (browser) |
| **Target Device** | Laptop/Desktop Computer | iPhone/Android phone | 40"-65" TV Display |
| **Use Case** | Case management, evidence review | Field capture, quick access | Court presentations |
| **Screen Size** | 1920x1080 (typical) | 375x812 (iPhone), 393x851 (Android) | 1920x1080 - 3840x2160 |
| **Font Size** | 13px normal | 16px+ (mobile-optimized) | 48px+ (readable from 10 feet) |
| **Input Method** | Mouse + keyboard | Touch/camera | Keyboard arrows + space |
| **Navigation** | Top menu + sidebar | Bottom tab bar | Keyboard shortcuts |
| **Offline Support** | Limited | ✅ Full (Service Workers) | No (requires internet) |
| **Installation** | Python + PyQt5 | Install from browser | Open URL in browser |

---

## 1️⃣ DESKTOP GUI (PyQt5 Native)

### What It Is
- **File**: `SemptifyAppGUI.py` (enhanced existing GUI)
- **Technology**: PyQt5 (native Python GUI framework)
- **Access**: Direct Python application
- **Status**: Compiled, ready for deployment

### Pages (7 Total)
```
Dashboard
├── Overview of current case
├── Stage indicator badge
└── Quick action buttons

Evidence Library
├── Photo gallery
├── Video player
├── Audio playback
└── Metadata viewer (GPS, timestamp)

Case Timeline
├── Chronological events
├── Date filtering
├── Evidence linking
└── Export to PDF

Rent Ledger
├── Payment history
├── Amount tracking
├── Late payment warnings
└── Calculations

Statute Tracker
├── Countdown timer to court date
├── Day counter
├── Current deadline
└── Next milestone

Court Packet Builder
├── Document assembly
├── Evidence selection
├── Auto-formatting
└── PDF export

Configuration
├── Settings panel
├── User preferences
├── Data management
└── Export/backup
```

### Features
✅ Professional dark UI (PyQt5 native)
✅ Responsive layout (adapts to window size)
✅ Evidence gallery with hover previews
✅ Statute countdown (animated timer)
✅ PDF export functionality
✅ AI chat integration (/api/copilot)
✅ Keyboard navigation
✅ System tray integration (Windows)
✅ Offline capable
✅ Multi-language ready

### Hardware Requirements
- Python 3.11+
- 500MB RAM minimum
- 1920x1080 minimum resolution
- PyQt5 library installed

### Access URL
```
Direct Python application (no web browser needed)
python SemptifyAppGUI.py
```

---

## 2️⃣ MOBILE PWA (Progressive Web App)

### What It Is
- **File**: `static/mobile_app.html` + JavaScript
- **Technology**: HTML5 + Progressive Web App (PWA)
- **Access**: Browser on iPhone/Android, installable as app
- **Status**: HTML/CSS/JS ready, can be deployed to Render

### Pages (4 Total)
```
Capture Screen
├── Video camera input (live feed)
├── Photo camera input
├── Audio recorder
└── GPS location tagging (EXIF data)

My Evidence
├── Swipeable card gallery
├── Photos with EXIF metadata
├── Videos with timestamps
├── Audio recordings with transcripts
└── Offline queue (syncs when online)

Quick Check
├── Current stage summary
├── Rights quick reference
├── Next steps reminder
└── Contact information

Settings
├── User preferences
├── Privacy controls
├── Storage management
└── Offline sync status
```

### Features
✅ One-tap video/photo/audio capture
✅ Automatic GPS tagging (if permission granted)
✅ Preserve EXIF metadata
✅ Works offline (Service Worker)
✅ Automatic upload queue (syncs when online)
✅ Installable as app (iOS + Android)
✅ Bottom navigation (touch-optimized)
✅ Large buttons (min 44px x 44px for touch)
✅ Prevents iOS zoom (font-size >= 16px)
✅ Push notifications ready
✅ Full-screen mode support

### Hardware Requirements
- iOS 14+ or Android 5+
- Chrome, Safari, Firefox, Edge
- Camera permission (for capture)
- Geolocation permission (for GPS)
- 50MB storage minimum (app + data)

### Access URL
```
https://semptify.onrender.com/mobile
OR
https://127.0.0.1:5000/mobile (local development)

Then "Add to Home Screen" to install as app
```

### CSS Breakpoints
```css
/* Mobile: < 600px */
@media (max-width: 600px) {
  font-size: 16px;
  buttons: 44px x 44px minimum
  grid: 1 column
}

/* Tablet: 600px - 1024px */
@media (min-width: 600px) {
  font-size: 14px;
  grid: 2 columns
}
```

---

## 3️⃣ TV PRESENTATION MODE (Full-Screen Court Display)

### What It Is
- **File**: `static/presentation_mode.html` + JavaScript
- **Technology**: HTML5 + Vanilla JavaScript
- **Access**: Browser in fullscreen mode on TV/projector
- **Status**: HTML/CSS/JS ready, can be deployed to Render

### Display Modes (4 Total)
```
Case Overview
├── Full case summary at top
├── Stage badge prominent
├── Timeline grid below
└── Evidence gallery bottom

Evidence Display (Single Item)
├── Large image/video full-screen
├── Metadata sidebar (optional)
├── Navigation arrows (next/prev)
└── Auto-advance timer (optional)

Timeline Walkthrough
├── Chronological narrative
├── Click to jump to event
├── Evidence preview on hover
└── Speaker notes display

Statute Ticker
├── Live countdown timer
├── Large numbers (72pt+)
├── Date/time to court
├── Animation effects
└── Critical warnings
```

### Keyboard Controls
```
Arrow Keys     → Navigate between events
Space          → Play slideshow (auto-advance)
F              → Toggle fullscreen
Esc            → Exit presentation
?              → Show help overlay
P              → Show/hide speaker notes
+ or =         → Zoom in (increase font)
- or _         → Zoom out (decrease font)
R              → Reset to default zoom
```

### Features
✅ Full-screen dedicated display (no address bar)
✅ Large readable fonts (48px - 72px default)
✅ High contrast colors (court-appropriate)
✅ Keyboard-only navigation (no mouse clutter)
✅ Presenter console (speaker notes)
✅ Automatic slideshow with timing
✅ Evidence display in large format
✅ Countdown timer animation
✅ Multi-screen support (HDMI/wireless casting)
✅ PDF annotation layer (optional)
✅ Drawing tools (optional)
✅ State persistence (can save presentation)

### Hardware Requirements
- Any computer with Chrome/Firefox/Edge
- 40"+ TV or projector display
- HDMI cable or wireless casting (Chromecast/AirPlay)
- Keyboard (for controls)
- Optional mouse (but not necessary)

### Font Sizes
```css
/* Readable from 10+ feet away */
Font Size: 48px - 72px
Line Height: 1.8
Letter Spacing: 1-2px
Font Weight: 600 (bold)
```

### Resolution Support
```
1920x1080 (Full HD) - 40" TV
2560x1440 (2K) - 50" TV
3840x2160 (4K) - 55"+ TV

All tested and responsive
```

### Access URL
```
https://semptify.onrender.com/tv
OR
https://127.0.0.1:5000/tv (local development)

Then press F for fullscreen
Connect TV via HDMI or wireless casting
```

---

## 🔄 How They Share Data

All three GUIs talk to the **same backend API**:

```
Desktop  ─────┐
              ├──→ Flask Backend (Semptify.py)
Mobile   ─────┤   ├── /api/evidence/captures
              ├──→├── /api/evidence/videos
TV       ─────┘   ├── /api/evidence/audit
                  ├── /api/copilot
                  └── SQLite Database
```

### Data Flow Example: Evidence Capture
```
1. User captures video on MOBILE
   ↓
2. Mobile PWA uploads to /api/evidence/capture/video
   ↓
3. Backend stores in uploads/ with metadata
   ↓
4. DESKTOP app fetches from /api/evidence/captures
   ↓
5. TV presentation displays from same /api/evidence/
```

---

## 📋 Implementation Status

| Component | Desktop | Mobile | TV |
|-----------|---------|--------|-----|
| **Routes** | ✅ Ready | ✅ Ready | ✅ Ready |
| **Templates** | ✅ Ready | ✅ Ready | ✅ Ready |
| **Styling** | ✅ Complete | ✅ Responsive | ✅ Large fonts |
| **JavaScript** | ✅ Dashboard JS | ✅ Camera/GPS JS | ✅ Controls JS |
| **Database** | ✅ Integration | ✅ Sync ready | ✅ Read-only |
| **Testing** | ✅ 71 tests | ✅ Mobile tests | ✅ Presentation tests |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🚀 Deployment

All three GUIs deploy to **Render.com**:

```
Desktop:  python SemptifyAppGUI.py
          (requires PyQt5 locally)

Mobile:   https://semptify.onrender.com/mobile
          (no installation needed, in browser)

TV:       https://semptify.onrender.com/tv
          (no installation needed, in browser)
```

---

## 🎯 Choose Your Version

### Use DESKTOP if you need:
- Professional case management interface
- Complex evidence organization
- Detailed timeline editing
- Offline work with sync
- Native app performance

### Use MOBILE if you need:
- Field evidence capture
- Quick status checking
- On-the-go access
- Automatic GPS tagging
- Simple, fast interface

### Use TV if you need:
- Court presentation
- Large group viewing
- Jury demonstration
- Evidence walkthrough
- Presenter control

---

## 📞 Support

Each GUI has its own troubleshooting guide:
- **Desktop Issues**: See GUI_COMPLETE.md (Desktop Issues section)
- **Mobile Issues**: See GUI_COMPLETE.md (Mobile Issues section)
- **TV Issues**: See GUI_COMPLETE.md (Presentation Issues section)

All documented in `GUI_COMPLETE.md`
