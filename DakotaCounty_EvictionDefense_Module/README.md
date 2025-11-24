# Dakota County Eviction Defense Module

**Version:** 1.0.0  
**Release Date:** 2025-11-21  
**Jurisdiction:** Dakota County District Court, Minnesota  
**Governing Law:** Minnesota Statutes Chapter 504B

---

## 🎯 Purpose

This module equips tenants and organizers in Eagan/Dakota County with **attorney-level tools** to defend against eviction actions. It provides process flows, motion templates, proactive tactics, and statutory anchors.

### Emotional Introduction (Multi-Language)

**English:**  
> Facing eviction is overwhelming. This module equips you with attorney‑grade tactics to defend your home.

**Spanish:**  
> Enfrentar un desalojo es abrumador. Este módulo te brinda tácticas de nivel legal para defender tu hogar.

**Somali:**  
> Ka saarista guri waa adag. Qaybtani waxa ay ku siinaysaa xeelado heer qareen si aad u difaacdo gurigaaga.

**Hmong:**  
> Kev raug ntiab tawm tsev yog ntxhov siab. Module no pab koj nrog tswv yim qib kws lij choj tiv thaiv koj lub tsev.

---

## 📦 Module Contents

| File | Purpose |
|------|---------|
| `process_flow.md` | Timeline of eviction case steps with statutory anchors |
| `motions_actions.md` | Templates for tenant motions (Dismiss, Continue, Escrow, Expungement, Counterclaims) |
| `proactive_tactics.md` | Defense checklists, evidence prep, triggers for motions |
| `statutes_forms.md` | Key statutes summary + form links |
| `ui_strings.json` | Multilingual UI labels (EN/ES/SO/HM) |
| `build_dakota_module.ps1` | Packaging script → checkpoint zip |
| `README.md` | This file |

---

## 🏛️ Jurisdiction & Workflow

**Court:** Dakota County District Court (Minnesota Judicial Branch)  
**Hearing Mode:** Remote (online hearings)  
**Key Statutes:** Minn. Stat. §§ 504B.001–504B.395, § 484.014 (expungement)

### Standard Workflow

1. **Complaint filed** by landlord
2. **Summons served** (≥7 days before hearing per § 504B.321)
3. **Online hearing** (tenant must appear via MN Judicial Branch platform)
4. **Judgment issued** (dismissal, continuance, or writ of recovery)
5. **Sheriff enforcement** if writ granted
6. **Post-case remedies** (expungement, escrow release)

---

## ⚡ Proactive Strategy

- **File responses early** via Guide & File
- **Prepare counterclaims** (habitability, retaliation, discrimination)
- **Gather evidence** (receipts, photos, inspection reports)
- **Anticipate landlord arguments** and prepare motions
- **Document all outcomes** for expungement

---

## 📚 For Semptify Librarian / Law Library Integration

### Recommended Library Placement

**Category:** `Eviction Defense`  
**Subcategory:** `Dakota County, MN`  
**Tags:** `eviction`, `housing`, `minnesota`, `tenant-rights`, `chapter-504b`, `motion-templates`

### Document Ingest Strategy

All module files (`.md`) can be indexed into the **Semptify document library** or **law library** system:

1. **Metadata Enrichment:**
   - Jurisdiction: Dakota County, MN
   - Document Type: Legal reference / motion template
   - Target Audience: Tenants, organizers, legal advocates
   - Language Support: English, Spanish, Somali, Hmong

2. **Full-Text Search Hooks:**
   - Service defects → `motions_actions.md` (Motion to Dismiss)
   - Habitability issues → `motions_actions.md` (Rent Escrow)
   - Retaliation timeline → `motions_actions.md` (Counterclaim)
   - Expungement eligibility → `motions_actions.md` + `statutes_forms.md`

3. **Auto-Suggestion Triggers:**
   - If user profile shows `service_date` within 7 days of `hearing_date` → Surface Motion to Dismiss
   - If 3+ `habitability` vault tags in last 30 days → Surface Rent Escrow Motion
   - If eviction filing date <30 days after tagged complaint → Surface Retaliation Counterclaim
   - If case outcome = "dismissed" → Surface Expungement Motion

4. **Citation Graph:**
   - Link `process_flow.md` → `motions_actions.md` (timeline-driven motion selection)
   - Link `statutes_forms.md` → official MN Judicial Branch forms
   - Link `proactive_tactics.md` → vault evidence categorization system

5. **Multilingual Indexing:**
   - Use `ui_strings.json` to provide translated labels in search/browse UI
   - Auto-detect user language preference from profile

### Integration with Existing Modules

**Vault System:**  
- Tag uploads with categories: `service`, `habitability`, `payments`, `retaliation`, `hearing`, `judgment`, `expungement`
- Auto-populate motion templates with vault evidence lists

**Timeline Feature:**  
- Log eviction case events (filing, service, hearing, judgment) with statutory deadlines
- Trigger motion suggestions based on timeline proximity

**Complaint Filing System:**  
- Cross-reference with Dakota County eviction defense when user location = Eagan/Dakota County

**Profile Manager:**  
- Auto-populate `{{TENANT_NAME}}`, `{{CASE_NO}}` in motion templates from active profile

---

## 🔧 Technical Integration (For Developers)

### Option 1: Standalone Blueprint

Create `dakota_eviction_library_routes.py`:

```python
from flask import Blueprint, render_template, jsonify, send_file
import os

dakota_bp = Blueprint('dakota_eviction', __name__, url_prefix='/library/dakota_eviction')

MODULE_DIR = os.path.join(os.path.dirname(__file__), 'DakotaCounty_EvictionDefense_Module')

@dakota_bp.route("/")
def index():
    """Browse module documents"""
    docs = [
        {"name": "Process Flow", "file": "process_flow.md", "desc": "Eviction case timeline"},
        {"name": "Motion Templates", "file": "motions_actions.md", "desc": "Dismiss, Continue, Escrow, Expungement"},
        {"name": "Proactive Tactics", "file": "proactive_tactics.md", "desc": "Checklists & triggers"},
        {"name": "Statutes & Forms", "file": "statutes_forms.md", "desc": "MN Chapter 504B reference"}
    ]
    return render_template('dakota_library_index.html', docs=docs)

@dakota_bp.route("/doc/<filename>")
def get_doc(filename):
    """Retrieve markdown document"""
    allowed = ['process_flow.md', 'motions_actions.md', 'proactive_tactics.md', 'statutes_forms.md']
    if filename not in allowed:
        return jsonify({"error": "Document not found"}), 404
    
    path = os.path.join(MODULE_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return jsonify({"filename": filename, "content": content})

@dakota_bp.route("/motion/<motion_type>")
def get_motion_template(motion_type):
    """Extract specific motion template with placeholders"""
    motion_map = {
        "dismiss": "Motion to Dismiss",
        "continue": "Motion to Continue",
        "escrow": "Motion for Rent Escrow",
        "expungement": "Motion for Expungement",
        "counterclaim": "Counterclaim"
    }
    
    if motion_type not in motion_map:
        return jsonify({"error": "Invalid motion type"}), 400
    
    # Parse motions_actions.md and extract template
    path = os.path.join(MODULE_DIR, 'motions_actions.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple extraction (could be enhanced with markdown parser)
    section_title = f"## {motion_map[motion_type]}"
    # ... parsing logic ...
    
    return jsonify({"motion_type": motion_type, "template": "..."})
```

Register in `Semptify.py`:

```python
try:
    from dakota_eviction_library_routes import dakota_bp
    app.register_blueprint(dakota_bp)
    print("[OK] Dakota County Eviction Defense Library registered at /library/dakota_eviction")
except ImportError as e:
    print(f"[WARN] Dakota Eviction Library not available: {e}")
```

### Option 2: Integrate with Existing `doc_explorer` Module

If `doc_explorer_routes.py` exists:

```python
# Add to doc_explorer_routes.py DOCUMENT_CATEGORIES
DOCUMENT_CATEGORIES = {
    # ... existing categories ...
    "eviction_defense": {
        "name": "Eviction Defense",
        "subcategories": {
            "dakota_county_mn": {
                "name": "Dakota County, MN",
                "documents": [
                    {"file": "DakotaCounty_EvictionDefense_Module/process_flow.md", "title": "Process Flow"},
                    {"file": "DakotaCounty_EvictionDefense_Module/motions_actions.md", "title": "Motion Templates"},
                    {"file": "DakotaCounty_EvictionDefense_Module/proactive_tactics.md", "title": "Proactive Tactics"},
                    {"file": "DakotaCounty_EvictionDefense_Module/statutes_forms.md", "title": "Statutes & Forms"}
                ]
            }
        }
    }
}
```

---

## �� Packaging & Deployment

Run the build script to create a checkpoint zip:

```powershell
.\DakotaCounty_EvictionDefense_Module\build_dakota_module.ps1
```

Output: `DakotaCounty_EvictionDefense_2025-11-21.zip`

### Contents of Checkpoint Zip

- All `.md` files
- `ui_strings.json`
- `README.md`
- Optional: Sample templates as standalone `.txt` files

---

## ⚠️ Disclaimer

**This module provides informational resources only. It is not legal advice and does not create an attorney-client relationship. Minnesota statutes may be amended after publication. Always verify current law and consult a licensed attorney for case-specific guidance.**

For legal assistance in Dakota County:
- [Minnesota Legal Aid](https://www.mylegalaid.org/)
- [LawHelp MN](https://www.lawhelpmn.org/)
- Dakota County Housing Court Self-Help Center

---

## 📞 Support & Updates

**Maintainer:** Semptify Development Team  
**Last Updated:** 2025-11-21  
**Version:** 1.0.0  

For updates, check:
- MN Judicial Branch Forms: https://www.mncourts.gov/getforms/housing-landlord-tenant
- LawHelp MN: https://www.lawhelpmn.org/

---

## 🌐 Multilingual UI Labels

See `ui_strings.json` for complete translations (English, Spanish, Somali, Hmong).

---

**End of README**
