# Module Wiring Action Plan

## Overview

**Current State:** 44% of modules wired and configured  
**Missing:** 14 modules (5 law_notes, 2 office, 1 public_exposure, 9 communication suite)  
**Estimated Fix Time:** 30-40 minutes  
**Difficulty:** Low to Medium

---

## PRIORITY 1: Wire Law Notes Modules (5 min)

### Location: Semptify.py, after line 968

### Add this code block:

```python
# Register Law Notes Blueprints (Priority 1 - 5 min)
try:
    from modules.law_notes.complaint_templates import complaint_templates
    app.register_blueprint(complaint_templates)
except ImportError:
    pass

try:
    from modules.law_notes.law_notes_actions import law_notes_actions
    app.register_blueprint(law_notes_actions)
except ImportError:
    pass

try:
    from modules.law_notes.evidence_packet_builder import evidence_packet_builder
    app.register_blueprint(evidence_packet_builder)
except ImportError:
    pass

try:
    from modules.law_notes.mn_jurisdiction_checklist import mn_check
    app.register_blueprint(mn_check)
except ImportError:
    pass

try:
    from modules.law_notes.attorney_trail import attorney_trail
    app.register_blueprint(attorney_trail)
except ImportError:
    pass
```

### What it enables:
- Complaint template generation
- Legal note management
- Evidence packet assembly
- Minnesota jurisdiction checklists
- Attorney communication tracking

---

## PRIORITY 2: Wire Office Module (2 min)

### Location: Semptify.py, after Priority 1 block

### Add this code:

```python
# Register Office Module Blueprint (Priority 2 - 2 min)
try:
    from modules.office_module.backend_demo import office_bp
    app.register_blueprint(office_bp)
except ImportError:
    pass
```

### What it enables:
- Certified video rooms
- Notary station
- Document center with SHA-256 verification
- Live review and annotations

---

## PRIORITY 3: Create Communication Suite Wrapper (15 min)

### Step 1: Create new file `modules/communication_suite_bp.py`

```python
"""
Communication Suite Flask Blueprint Wrapper

Provides API endpoints for:
- Modal triggers (multilingual)
- Help texts (9 languages)
- Voice commands
- Form controls
"""

from flask import Blueprint, jsonify, request
import json
import os

# Create blueprint
comm_suite_bp = Blueprint(
    'communication_suite',
    __name__,
    url_prefix='/api/communication-suite'
)

# Configuration paths
BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    'CommunicationSuite',
    'FormalMethods'
)

def load_json_config(filename):
    """Load JSON configuration file from Communication Suite."""
    filepath = os.path.join(BASE_PATH, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Cache configurations
_modal_triggers_cache = None
_help_texts_cache = None

def get_modal_triggers():
    """Get modal triggers configuration."""
    global _modal_triggers_cache
    if _modal_triggers_cache is None:
        _modal_triggers_cache = load_json_config('modal_triggers.json')
    return _modal_triggers_cache

def get_help_texts():
    """Get multilingual help texts."""
    global _help_texts_cache
    if _help_texts_cache is None:
        _help_texts_cache = load_json_config('help_text_multilingual.json')
    return _help_texts_cache

# ============================================================
# API ENDPOINTS
# ============================================================

@comm_suite_bp.route('/triggers', methods=['GET'])
def get_triggers():
    """Get all modal trigger configurations."""
    return jsonify({
        'triggers': get_modal_triggers(),
        'status': 'ok'
    })

@comm_suite_bp.route('/triggers/<trigger_id>', methods=['GET'])
def get_trigger(trigger_id):
    """Get specific modal trigger by ID."""
    triggers = get_modal_triggers()
    trigger = triggers.get(trigger_id, {})
    if not trigger:
        return jsonify({'error': 'Trigger not found'}), 404
    return jsonify(trigger)

@comm_suite_bp.route('/help', methods=['GET'])
def get_help():
    """Get help texts for specified language."""
    language = request.args.get('lang', 'en')
    help_texts = get_help_texts()
    lang_help = help_texts.get(language, help_texts.get('en', {}))
    return jsonify({
        'language': language,
        'help': lang_help,
        'available_languages': list(help_texts.keys())
    })

@comm_suite_bp.route('/help/<language>', methods=['GET'])
def get_help_by_language(language):
    """Get help texts for specific language."""
    help_texts = get_help_texts()
    if language not in help_texts:
        return jsonify({
            'error': f'Language {language} not available',
            'available': list(help_texts.keys())
        }), 404
    return jsonify({
        'language': language,
        'help': help_texts[language]
    })

@comm_suite_bp.route('/config', methods=['GET'])
def get_all_config():
    """Get all Communication Suite configurations."""
    return jsonify({
        'triggers': get_modal_triggers(),
        'help_texts': get_help_texts(),
        'status': 'ok'
    })

@comm_suite_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of available languages."""
    help_texts = get_help_texts()
    return jsonify({
        'languages': list(help_texts.keys()),
        'count': len(help_texts)
    })

@comm_suite_bp.route('/status', methods=['GET'])
def get_status():
    """Get Communication Suite status."""
    triggers = get_modal_triggers()
    help_texts = get_help_texts()
    return jsonify({
        'status': 'ok',
        'triggers_count': len(triggers),
        'languages': list(help_texts.keys()),
        'languages_count': len(help_texts)
    })
```

### Step 2: Register in Semptify.py

```python
# Register Communication Suite Blueprint (Priority 3 - already in init)
try:
    from modules.communication_suite_bp import comm_suite_bp
    app.register_blueprint(comm_suite_bp)
except ImportError:
    pass
```

### What it enables:
- 9 communication modules unified under one API
- Multilingual support (9 languages)
- Modal triggers for UI
- Voice command configuration
- Help text endpoints

### Test endpoints:
```bash
GET http://localhost:5000/api/communication-suite/triggers
GET http://localhost:5000/api/communication-suite/help?lang=es
GET http://localhost:5000/api/communication-suite/languages
```

---

## PRIORITY 4: Verify & Fix Public Exposure Module (5 min)

### Step 1: Check if module exists

```bash
# In PowerShell, from c:\Semptify\Semptify:
Test-Path .\modules\public_exposure_module.py
```

### Step 2: If exists, verify it exports correct blueprint

```python
# Check what it exports:
python -c "from modules.public_exposure_module import public_exposure_bp; print('OK')"
```

### Step 3: If import fails, fix in Semptify.py

The current code (line 958-961) should work if module exports correctly:
```python
try:
    from modules.public_exposure_module import public_exposure_bp
    app.register_blueprint(public_exposure_bp)
except ImportError:
    pass
```

---

## PRIORITY 5: Configure Separate Services (15-30 min)

### The AI Orchestrator (Optional, separate service)

**File:** `modules/office_module/ai_orchestrator.py`

**Current Setup:** Standalone FastAPI app (not part of Flask)

**Three deployment options:**

#### Option A: Local Development
```bash
# Terminal 1: Run main Flask app
python .\Semptify.py

# Terminal 2: Run AI orchestrator on port 9001
uvicorn modules.office_module.ai_orchestrator:app --reload --port 9001 --host 127.0.0.1
```

#### Option B: Docker Compose
```yaml
# Add to docker-compose.yml:
ai_orchestrator:
  build: .
  command: uvicorn modules.office_module.ai_orchestrator:app --reload --port 9001 --host 0.0.0.0
  ports:
    - "9001:9001"
  environment:
    - AI_PROVIDER=openai
    - OPENAI_API_KEY=${OPENAI_API_KEY}
```

#### Option C: Reverse Proxy (Production)
```nginx
# nginx config to proxy ai_orchestrator requests to Flask
location /api/ai {
    proxy_pass http://localhost:9001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

---

## Complete Implementation Checklist

```
[ ] Priority 1: Wire Law Notes Modules (5 min)
    [ ] Add complaint_templates import
    [ ] Add law_notes_actions import
    [ ] Add evidence_packet_builder import
    [ ] Add mn_jurisdiction_checklist import
    [ ] Add attorney_trail import
    [ ] Test: python -c "from Semptify import app; print(list(app.blueprints.keys()))"

[ ] Priority 2: Wire Office Module (2 min)
    [ ] Add office_bp import
    [ ] Test: curl http://localhost:5000/office

[ ] Priority 3: Create Communication Suite Wrapper (15 min)
    [ ] Create modules/communication_suite_bp.py
    [ ] Add endpoint implementations
    [ ] Register blueprint in Semptify.py
    [ ] Test: curl http://localhost:5000/api/communication-suite/status

[ ] Priority 4: Verify Public Exposure (5 min)
    [ ] Check module exists
    [ ] Verify blueprint export
    [ ] Test import in Python REPL

[ ] Priority 5: Configure AI Orchestrator (Optional, 15-30 min)
    [ ] Choose deployment option
    [ ] Set environment variables
    [ ] Test endpoint connectivity
```

---

## Testing After Wiring

```bash
# Verify all blueprints registered
python scripts/list_endpoints.py

# Run Flask app
python .\Semptify.py

# In another terminal, test endpoints:
curl http://localhost:5000/api/data-flow/registry          # Core (already works)
curl http://localhost:5000/api/communication-suite/status  # New
curl http://localhost:5000/api/law-notes-actions/...       # New
curl http://localhost:5000/office/...                      # New

# Check for errors
python -c "from Semptify import app; print('✅ App loads successfully')"
```

---

## Summary

| Priority | Task | Time | Status |
|----------|------|------|--------|
| 1 | Wire 5 law_notes modules | 5 min | Ready ✅ |
| 2 | Wire office_bp | 2 min | Ready ✅ |
| 3 | Create comm_suite wrapper | 15 min | Code ready ✅ |
| 4 | Verify public_exposure | 5 min | Ready ✅ |
| 5 | Configure ai_orchestrator | 15-30 min | Optional |
| **TOTAL** | **Full Implementation** | **30-50 min** | **Low risk** |

---

## Success Criteria

After completing all priorities:

✅ All 5 law_notes modules accessible via API  
✅ Office module endpoints working  
✅ Communication Suite providing triggers and help texts  
✅ Public Exposure module verified or documented  
✅ No import errors in Flask app  
✅ All new endpoints return valid responses  

**Estimated module availability increase:** 44% → 85%+

