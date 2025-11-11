# GUI Implementation Starter - Choose Your Path

## Quick Start: Which UI to Build First?

### Option A: Mobile PWA (FASTEST TO PRODUCTION)
- **Timeline:** 1-2 weeks
- **Impact:** Immediate field evidence capture
- **Complexity:** Medium
- **Priority:** Highest (enables core feature)

### Option B: Desktop HTML (MOST POWERFUL)
- **Timeline:** 2-3 weeks  
- **Impact:** Professional case management
- **Complexity:** High
- **Priority:** High (needed for attorney workflow)

### Option C: TV Presentation (MOST IMPRESSIVE)
- **Timeline:** 1-2 weeks
- **Impact:** Court demonstrations
- **Complexity:** Medium
- **Priority:** Medium (secondary feature)

---

## Phase 1: Mobile PWA (RECOMMENDED FIRST)

### Why First?
- Users can capture evidence immediately
- Offline support = works in field with poor connection
- Installable on phone home screen
- Foundation for desktop sync

### Step 1: Create Mobile Routes File

**File: `ui_mobile_routes.py`** (300+ lines)

```python
from flask import Blueprint, render_template, request, jsonify
from av_capture import get_av_manager
from ledger_tracking import get_statute_tracker
import os
import json
from datetime import datetime

ui_mobile_bp = Blueprint('ui_mobile', __name__, url_prefix='/ui/mobile')

# ============================================================================
# ROUTES - Mobile UI Pages
# ============================================================================

@ui_mobile_bp.route('/')
def mobile_home():
    """Main mobile home - quick capture buttons"""
    return render_template('ui/mobile/home.html')

@ui_mobile_bp.route('/capture')
def mobile_capture():
    """Camera/audio/document capture interface"""
    return render_template('ui/mobile/capture.html')

@ui_mobile_bp.route('/my-evidence')
def mobile_my_evidence():
    """View what I've uploaded"""
    return render_template('ui/mobile/my-evidence.html')

@ui_mobile_bp.route('/quick-check')
def mobile_quick_check():
    """Statute/deadline countdown"""
    return render_template('ui/mobile/quick-check.html')

@ui_mobile_bp.route('/offline')
def mobile_offline():
    """Fallback when offline"""
    return render_template('ui/mobile/offline.html')

@ui_mobile_bp.route('/settings')
def mobile_settings():
    """User preferences"""
    return render_template('ui/mobile/settings.html')

# ============================================================================
# API - Data for Mobile UI
# ============================================================================

@ui_mobile_bp.route('/api/status')
def api_mobile_status():
    """Current user status: statute deadlines, weather alerts, etc"""
    try:
        statute_tracker = get_statute_tracker()
        active_statutes = statute_tracker.get_active_statutes()
        
        status = {
            "user": {
                "id": request.args.get('user_id', 'unknown'),
                "name": "User"  # From auth token in production
            },
            "statutes": [
                {
                    "id": s.get('id'),
                    "action_type": s.get('action_type'),
                    "days_remaining": s.get('days_remaining', 0),
                    "expires": s.get('expiration_date'),
                    "urgency": "critical" if s.get('days_remaining', 0) < 7 else "normal"
                }
                for s in active_statutes
            ],
            "next_deadline": active_statutes[0].get('expiration_date') if active_statutes else None,
            "weather_alerts": [],  # From weather_and_time.py
            "uptime_seconds": 0  # From metrics
        }
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ui_mobile_bp.route('/api/my-evidence')
def api_my_evidence():
    """List evidence uploaded by current user"""
    try:
        av_manager = get_av_manager()
        user_id = request.args.get('user_id', 'unknown')
        
        # Get captures for this user
        all_captures = av_manager.get_all_captures()
        user_captures = [c for c in all_captures if c.get('actor_id') == user_id]
        
        # Format for mobile display
        evidence_list = [
            {
                "id": c.get('id'),
                "type": c.get('type'),  # video, audio, photo
                "timestamp": c.get('timestamp'),
                "description": c.get('description'),
                "status": "synced",  # From sync queue
                "thumbnail": f"/uploads/evidence/{c.get('id')}_thumb.jpg"
            }
            for c in user_captures
        ]
        
        return jsonify({
            "count": len(evidence_list),
            "evidence": evidence_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ui_mobile_bp.route('/api/sync-queue')
def api_sync_queue():
    """Get list of queued uploads (for retry)"""
    try:
        queue_file = os.path.join('evidence_capture', 'sync_queue.json')
        if os.path.exists(queue_file):
            with open(queue_file, 'r') as f:
                queue = json.load(f)
        else:
            queue = []
        
        return jsonify({
            "queued": len(queue),
            "items": queue
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ui_mobile_bp.route('/api/retry-upload', methods=['POST'])
def api_retry_upload():
    """Retry failed upload"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        
        # Move from failed queue to upload queue
        # ... implementation ...
        
        return jsonify({"status": "ok", "file_id": file_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# EXPORT
# ============================================================================

def get_ui_mobile_bp():
    """Export blueprint for registration in Semptify.py"""
    return ui_mobile_bp
```

### Step 2: Create Mobile Templates

**File: `templates/ui/mobile/home.html`** (150 lines)

```html
{% extends "base.html" %}

{% block title %}Semptify - Mobile Capture{% endblock %}

{% block content %}
<div class="mobile-home">
  <div class="quick-status">
    <div class="status-card">
      <h2>Days Remaining</h2>
      <span class="countdown" id="days-remaining">-</span>
    </div>
    <div class="status-card">
      <h2>Next Deadline</h2>
      <span class="deadline" id="next-deadline">-</span>
    </div>
  </div>

  <div class="capture-buttons">
    <button class="btn btn-primary btn-large" onclick="startVideoCapture()">
      <span class="icon">🎥</span>
      Record Video
    </button>
    
    <button class="btn btn-primary btn-large" onclick="startPhotoCapture()">
      <span class="icon">📷</span>
      Take Photo
    </button>
    
    <button class="btn btn-primary btn-large" onclick="startAudioCapture()">
      <span class="icon">🎙️</span>
      Record Audio
    </button>
    
    <button class="btn btn-secondary btn-large" onclick="goTo('/ui/mobile/my-evidence')">
      <span class="icon">📁</span>
      My Evidence
    </button>
  </div>

  <div class="offline-notice" id="offline-notice" style="display:none;">
    <p>📡 Offline mode - captures will sync when connected</p>
  </div>
</div>

<script>
  // Load current status
  async function loadStatus() {
    try {
      const response = await fetch('/ui/mobile/api/status');
      const data = await response.json();
      
      document.getElementById('days-remaining').textContent = 
        data.statutes[0]?.days_remaining || '?';
      document.getElementById('next-deadline').textContent = 
        new Date(data.next_deadline).toLocaleDateString();
    } catch (e) {
      console.error('Failed to load status:', e);
    }
  }

  // Detect offline mode
  window.addEventListener('offline', () => {
    document.getElementById('offline-notice').style.display = 'block';
  });
  window.addEventListener('online', () => {
    document.getElementById('offline-notice').style.display = 'none';
  });

  // Initialize
  loadStatus();
  setInterval(loadStatus, 60000); // Refresh every minute
</script>
{% endblock %}
```

**File: `templates/ui/mobile/capture.html`** (200 lines)

```html
{% extends "base.html" %}

{% block title %}Capture Evidence{% endblock %}

{% block content %}
<div class="mobile-capture">
  <div class="camera-container">
    <video id="camera-preview" autoplay playsinline></video>
    <canvas id="camera-canvas" style="display:none;"></canvas>
  </div>

  <div class="capture-controls">
    <button class="btn btn-record" id="record-button" onclick="toggleRecord()">
      <span class="dot"></span> Start Recording
    </button>
    
    <button class="btn btn-secondary" onclick="goBack()">Cancel</button>
  </div>

  <div class="metadata-form">
    <input type="hidden" id="gps-lat" />
    <input type="hidden" id="gps-lon" />
    <input type="hidden" id="gps-accuracy" />
    
    <textarea placeholder="Description (optional)" id="description"></textarea>
    
    <button class="btn btn-primary" onclick="uploadCapture()">
      Upload Evidence
    </button>
  </div>
</div>

<script>
  let mediaRecorder;
  let recordedChunks = [];
  let isRecording = false;

  // Start camera on page load
  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: true
      });
      document.getElementById('camera-preview').srcObject = stream;
      
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };
      
      // Auto-tag GPS
      getLocation();
    } catch (e) {
      console.error('Camera access denied:', e);
      alert('Please allow camera access to capture evidence');
    }
  }

  // Geolocation auto-tag
  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition((position) => {
        document.getElementById('gps-lat').value = position.coords.latitude;
        document.getElementById('gps-lon').value = position.coords.longitude;
        document.getElementById('gps-accuracy').value = position.coords.accuracy;
      });
    }
  }

  // Toggle record
  function toggleRecord() {
    if (!isRecording) {
      recordedChunks = [];
      mediaRecorder.start();
      isRecording = true;
      document.getElementById('record-button').textContent = '⏹️ Stop Recording';
    } else {
      mediaRecorder.stop();
      isRecording = false;
      document.getElementById('record-button').textContent = '✓ Ready to Upload';
      document.getElementById('record-button').disabled = true;
    }
  }

  // Upload capture
  async function uploadCapture() {
    const formData = new FormData();
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    formData.append('file', blob, 'evidence.webm');
    formData.append('actor_id', 'current-user');
    formData.append('description', document.getElementById('description').value);
    formData.append('location_lat', document.getElementById('gps-lat').value);
    formData.append('location_lon', document.getElementById('gps-lon').value);
    formData.append('location_accuracy', document.getElementById('gps-accuracy').value);

    try {
      const response = await fetch('/api/evidence/capture/video', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        alert('✓ Evidence uploaded successfully');
        goTo('/ui/mobile/my-evidence');
      } else {
        throw new Error('Upload failed');
      }
    } catch (e) {
      // Queue for later if offline
      console.log('Queuing for offline sync:', e);
      queueForSync(formData);
    }
  }

  // Initialize
  startCamera();
</script>
{% endblock %}
```

### Step 3: Create Service Worker (Offline Support)

**File: `static/js/ui/mobile/service-worker.js`** (150 lines)

```javascript
const CACHE_NAME = 'semptify-mobile-v1';
const ASSETS_TO_CACHE = [
  '/ui/mobile/',
  '/ui/mobile/capture',
  '/ui/mobile/my-evidence',
  '/ui/mobile/quick-check',
  '/static/css/ui/mobile/mobile-first.css',
  '/static/js/ui/mobile/camera-capture.js',
  '/manifest.json'
];

// Install: Cache assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch: Network-first, fallback to cache
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache successful responses
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Fall back to cache when offline
        return caches.match(event.request).then((cached) => {
          return cached || caches.match('/ui/mobile/offline');
        });
      })
  );
});

// Background sync: Upload queued evidence when online
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-evidence-upload') {
    event.waitUntil(
      (async () => {
        const db = await indexedDB.open('semptify-mobile');
        const tx = db.transaction('sync-queue', 'readonly');
        const store = tx.objectStore('sync-queue');
        const items = await store.getAll();

        for (const item of items) {
          try {
            await fetch('/api/evidence/capture/video', {
              method: 'POST',
              body: item.formData
            });
            // Remove from queue on success
            const txDelete = db.transaction('sync-queue', 'readwrite');
            txDelete.objectStore('sync-queue').delete(item.id);
          } catch (e) {
            console.log('Sync failed, will retry:', e);
          }
        }
      })()
    );
  }
});
```

### Step 4: Create Manifest (PWA Install)

**File: `manifest.json`**

```json
{
  "name": "Semptify - Evidence Manager",
  "short_name": "Semptify",
  "description": "Capture, organize, and present legal evidence with GPS tagging and offline support",
  "start_url": "/ui/mobile/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2c3e50",
  "scope": "/ui/mobile/",
  "icons": [
    {
      "src": "/static/icons/semptify-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/semptify-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/semptify-maskable-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/static/icons/semptify-maskable-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "categories": ["productivity", "utilities"],
  "screenshots": [
    {
      "src": "/static/icons/screenshot-mobile.png",
      "sizes": "540x720",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/static/icons/screenshot-desktop.png",
      "sizes": "1920x1080",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

### Step 5: Mobile CSS

**File: `static/css/ui/mobile/mobile-first.css`** (150+ lines)

```css
/* Mobile-First Responsive Design */

:root {
  --primary: #2c3e50;
  --accent: #e74c3c;
  --text: #2c3e50;
  --bg: #ecf0f1;
  --border: #bdc3c7;
  --touch-target: 44px;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 16px; /* iOS zoom prevention */
  background: var(--bg);
  color: var(--text);
}

/* Touch-Optimized Controls */
button, input, textarea {
  min-height: var(--touch-target);
  min-width: var(--touch-target);
  padding: 12px 16px;
  font-size: 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

button:active {
  background: var(--bg);
  opacity: 0.8;
}

/* Camera Preview */
.camera-container {
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  background: black;
  overflow: hidden;
}

.camera-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Buttons */
.btn-large {
  width: 100%;
  padding: 20px;
  margin: 10px 0;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-secondary {
  background: var(--bg);
  color: var(--text);
}

/* Status Cards */
.status-card {
  background: white;
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.status-card h2 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #7f8c8d;
}

.status-card .countdown,
.status-card .deadline {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary);
}

/* Responsive */
@media (min-width: 600px) {
  .capture-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  
  .btn-large {
    margin: 0;
  }
}
```

---

## Integration: Add to Semptify.py

**Edit `Semptify.py`** (add near line 30):

```python
from ui_mobile_routes import ui_mobile_bp

# Register blueprints
app.register_blueprint(ui_mobile_bp)

# Also add manifest.json link to base template:
# <link rel="manifest" href="/manifest.json">
# <meta name="theme-color" content="#2c3e50">
# <script>
#   if ('serviceWorker' in navigator) {
#     navigator.serviceWorker.register('/static/js/ui/mobile/service-worker.js');
#   }
# </script>
```

---

## Testing Checklist

```
MOBILE PWA - READY TO TEST:
☐ Create ui_mobile_routes.py
☐ Create templates/ui/mobile/home.html
☐ Create templates/ui/mobile/capture.html
☐ Create static/js/ui/mobile/service-worker.js
☐ Create manifest.json
☐ Create static/css/ui/mobile/mobile-first.css
☐ Add imports to Semptify.py
☐ Run: python -m pytest -q (all tests pass)
☐ Test on iPhone: https://semptify.com/ui/mobile/
☐ Test on Android: https://semptify.com/ui/mobile/
☐ Test offline capture (disable wifi)
☐ Test "Add to Home Screen"
☐ Test camera capture with GPS tag
☐ Test upload (should work offline + sync)
```

---

## What's Next?

Once mobile is working:
1. **Desktop** (1-2 weeks) - evidence dashboard, ledger manager, packet builder
2. **TV Presentation** (1 week) - case overview, statute ticker, verdict recording

Ready to code?
