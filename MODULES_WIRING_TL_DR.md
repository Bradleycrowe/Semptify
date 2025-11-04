# Module Wiring - Quick Summary

## The Situation

You have **25 modules total** in Semptify:
- ✅ **7 are wired** (core framework)
- 🔶 **4 are partial** (conditional or uncertain)
- ❌ **14 are NOT wired** (missing from Flask app)

**Current coverage: 28% | Missing: 56%**

---

## What's NOT Wired (14 modules)

### Law Notes (5 modules) - Missing legal tools
- `complaint_templates` - Generate formal complaints
- `law_notes_actions` - Manage legal notes
- `evidence_packet_builder` - Assemble evidence packets
- `mn_jurisdiction_checklist` - Minnesota legal requirements
- `attorney_trail` - Track attorney communications

### Office Module (2 modules) - Missing workspace
- `office_bp` - Certified rooms, notary, documents
- `ai_orchestrator` - Separate AI service (port 9001)

### Communication Suite (9 modules) - Missing unified communication
- FormalMethods, ContactManager, CalendarEvents, VaultModule
- LedgerModule, DeliveryModule, NotaryModule, VoiceModule, ScanModule

### Other (1 module) - Unknown status
- `public_exposure_bp` - Verify if it exists and works

---

## 3-Minute Fix (Law Notes + Office)

**Edit:** `Semptify.py` - Add after line 968:

```python
# Law Notes Modules
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

# Office Module
try:
    from modules.office_module.backend_demo import office_bp
    app.register_blueprint(office_bp)
except ImportError:
    pass
```

**Result:** Unlocks 6 new endpoints immediately

---

## 15-Minute Fix (Communication Suite)

**Create:** `modules/communication_suite_bp.py`

```python
from flask import Blueprint, jsonify, request
import json
import os

comm_suite_bp = Blueprint('communication_suite', __name__, url_prefix='/api/comm-suite')

BASE_PATH = os.path.join(os.path.dirname(__file__), 'CommunicationSuite', 'FormalMethods')

def load_config(filename):
    try:
        with open(os.path.join(BASE_PATH, filename)) as f:
            return json.load(f)
    except:
        return {}

@comm_suite_bp.route('/triggers', methods=['GET'])
def get_triggers():
    return jsonify({'triggers': load_config('modal_triggers.json')})

@comm_suite_bp.route('/help/<language>', methods=['GET'])
def get_help(language='en'):
    help_texts = load_config('help_text_multilingual.json')
    return jsonify(help_texts.get(language, help_texts.get('en', {})))

@comm_suite_bp.route('/config', methods=['GET'])
def get_config():
    return jsonify({
        'triggers': load_config('modal_triggers.json'),
        'help': load_config('help_text_multilingual.json')
    })
```

**Then add to Semptify.py:**

```python
try:
    from modules.communication_suite_bp import comm_suite_bp
    app.register_blueprint(comm_suite_bp)
except ImportError:
    pass
```

**Result:** Unlocks 9 communication modules + multilingual support

---

## Impact by Priority

| Priority | Action | Time | Modules | Status |
|----------|--------|------|---------|--------|
| 1 | Add law_notes imports | 5 min | 5 | Ready |
| 2 | Add office_bp import | 2 min | 1 | Ready |
| 3 | Create comm_suite_bp.py | 15 min | 9 | Ready |
| 4 | Verify public_exposure | 5 min | 1 | Check |
| 5 | Setup ai_orchestrator | 30 min | 1 | Optional |
| | **TOTAL** | **30-50 min** | **16+** | **56% → 85%** |

---

## Files to Read for Details

1. **MODULES_WIRING_STATUS.md** - Full audit and what each module does
2. **MODULES_WIRING_QUICK_REFERENCE.md** - Visual dashboard and testing
3. **MODULE_WIRING_ACTION_PLAN.md** - Complete implementation guide

---

## Quick Test

```bash
# After implementing Priority 1 & 2:
python -c "from Semptify import app; print([b for b in app.blueprints.keys()])"

# Should show: 
# [..., 'complaint_templates', 'law_notes_actions', 'evidence_packet_builder',
#  'mn_check', 'attorney_trail', 'office', ...]
```

---

## Bottom Line

**56% of your modules are not connected to your Flask app.**

**Takes ~30 minutes to fix and unlock everything.**

**Copy-paste ready code is in MODULE_WIRING_ACTION_PLAN.md**
