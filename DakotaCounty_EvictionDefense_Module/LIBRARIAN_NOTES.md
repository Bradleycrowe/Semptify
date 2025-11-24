# For Semptify Librarian: Dakota County Eviction Defense Module

**Date:** 2025-11-21  
**Module Version:** 1.0.0  
**Status:** Ready for library integration

---

## 📦 What You Received

A complete **Dakota County Eviction Defense Module** with attorney-level resources for tenants facing eviction in Dakota County, Minnesota.

### Files Provided

| File | Purpose | Library Use |
|------|---------|-------------|
| `README.md` | Overview, integration guide | Index/catalog entry |
| `process_flow.md` | Eviction timeline with deadlines | Reference doc, searchable |
| `motions_actions.md` | Motion templates (Dismiss, Continue, Escrow, Expungement, Counterclaim) | Template library, form generator |
| `proactive_tactics.md` | Defense checklists and triggers | Strategy guide, decision trees |
| `statutes_forms.md` | MN Chapter 504B statute summaries + form links | Legal reference, citation index |
| `ui_strings.json` | Multilingual labels (EN/ES/SO/HM) | Localization, UI translation |
| `build_dakota_module.ps1` | Packaging script | Distribution, backup |
| `LIBRARIAN_NOTES.md` | This file | Integration instructions |

### Blueprint File (Separate)

`dakota_eviction_library_routes.py` — Flask blueprint in parent directory  
Provides REST API for document retrieval and search.

---

## �� Integration Options

### Option 1: Add to Existing `doc_explorer` Module

If you have `doc_explorer_routes.py` with a `DOCUMENT_CATEGORIES` structure:

```python
# In doc_explorer_routes.py
DOCUMENT_CATEGORIES = {
    # ... existing categories ...
    "eviction_defense": {
        "name": "Eviction Defense",
        "icon": "⚖️",
        "subcategories": {
            "dakota_county_mn": {
                "name": "Dakota County, MN",
                "documents": [
                    {
                        "file": "DakotaCounty_EvictionDefense_Module/process_flow.md",
                        "title": "Process Flow",
                        "description": "Eviction case timeline with statutory deadlines",
                        "tags": ["timeline", "deadlines", "court-process"]
                    },
                    {
                        "file": "DakotaCounty_EvictionDefense_Module/motions_actions.md",
                        "title": "Motion Templates",
                        "description": "Dismiss, Continue, Escrow, Expungement, Counterclaims",
                        "tags": ["motions", "templates", "court-filings"]
                    },
                    {
                        "file": "DakotaCounty_EvictionDefense_Module/proactive_tactics.md",
                        "title": "Proactive Tactics",
                        "description": "Defense checklists and triggers",
                        "tags": ["checklists", "evidence", "defense"]
                    },
                    {
                        "file": "DakotaCounty_EvictionDefense_Module/statutes_forms.md",
                        "title": "Statutes & Forms",
                        "description": "MN Chapter 504B reference",
                        "tags": ["statutes", "forms", "chapter-504b"]
                    }
                ]
            }
        }
    }
}
```

### Option 2: Register Standalone Blueprint

If you prefer a dedicated endpoint:

```python
# In Semptify.py, add after other blueprint registrations:
try:
    from dakota_eviction_library_routes import dakota_bp
    app.register_blueprint(dakota_bp)
    print("[OK] Dakota County Eviction Defense Library registered at /library/dakota_eviction")
except ImportError as e:
    print(f"[WARN] Dakota Eviction Library not available: {e}")
```

**Access URLs:**
- Index: `http://localhost:8080/library/dakota_eviction/`
- Get document: `http://localhost:8080/library/dakota_eviction/doc/<doc_id>`
- Get motion: `http://localhost:8080/library/dakota_eviction/motion/<motion_type>`
- Search: `http://localhost:8080/library/dakota_eviction/search?q=<query>`
- UI strings: `http://localhost:8080/library/dakota_eviction/ui_strings/<lang>`

### Option 3: Hybrid Approach

Register blueprint AND add entries to `doc_explorer` for unified browsing. Best of both worlds.

---

## 📊 Suggested Library Metadata

**Primary Category:** Eviction Defense  
**Jurisdiction:** Dakota County, Minnesota  
**Language Support:** English, Spanish, Somali, Hmong  
**Target Users:** Tenants, organizers, legal advocates  
**Statutory Basis:** Minnesota Statutes Chapter 504B

**Tags/Keywords:**
- `eviction`
- `housing`
- `minnesota`
- `tenant-rights`
- `chapter-504b`
- `motion-templates`
- `dakota-county`
- `habitability`
- `retaliation`
- `expungement`

---

## 🔍 Search & Discovery Hooks

### Auto-Suggestions Based on User Context

**Trigger:** Service date within 7 days of hearing  
**Suggest:** Motion to Dismiss (`motions_actions.md` → Section 1)

**Trigger:** 3+ habitability vault tags in last 30 days  
**Suggest:** Rent Escrow Motion (`motions_actions.md` → Section 3)

**Trigger:** Eviction filed <30 days after complaint timestamp  
**Suggest:** Retaliation Counterclaim (`motions_actions.md` → Section 5)

**Trigger:** Case outcome = "dismissed"  
**Suggest:** Expungement Motion (`motions_actions.md` → Section 4)

### Full-Text Search Targets

| User Query | Target Document | Key Section |
|------------|-----------------|-------------|
| "service defect" | `motions_actions.md` | Motion to Dismiss |
| "habitability" | `statutes_forms.md`, `motions_actions.md` | § 504B.161, Rent Escrow |
| "retaliation" | `statutes_forms.md`, `motions_actions.md` | § 504B.285, Counterclaim |
| "expungement" | `motions_actions.md`, `statutes_forms.md` | § 484.014, Motion template |
| "hearing timeline" | `process_flow.md` | Phase 5 |
| "rent escrow" | `proactive_tactics.md`, `motions_actions.md` | Trigger Matrix, Motion 3 |

---

## 🌐 Multilingual Support

Use `ui_strings.json` for translated labels in:
- Library browse UI
- Motion template headers
- Form field labels
- Help tooltips

**Available Languages:**
- English (`en`)
- Spanish (`es`)
- Somali (`so`)
- Hmong (`hm`)

**API Endpoint:**  
`GET /library/dakota_eviction/ui_strings/<lang>`

---

## 📈 Analytics Opportunities

Track usage metrics to measure impact:

- **Most accessed documents** → Identify high-value resources
- **Motion template downloads** → Which defenses most common
- **Search queries** → Discover gaps in coverage
- **Language preference** → Prioritize translations

---

## 🔗 Integration with Existing Semptify Features

### Vault System
Tag uploads with categories from module:
- `service` → Links to Motion to Dismiss
- `habitability` → Links to Rent Escrow Motion
- `payments` → Evidence for payment disputes
- `retaliation` → Links to Counterclaim
- `hearing` → Timeline event
- `judgment` → Outcome tracking
- `expungement` → Post-case remedy

### Timeline Feature
Auto-populate case events:
- Filing date
- Service date (trigger: <7 days = red flag)
- Hearing date
- Judgment date
- Enforcement date
- Expungement eligibility date

### Profile Manager
Auto-fill motion templates:
- `{{TENANT_NAME}}` from active profile
- `{{CASE_NO}}` from timeline entry
- `{{HEARING_DATE}}` from calendar
- `{{SERVICE_DATE}}` from vault metadata

### Complaint Filing System
Cross-reference:
- If user location = Dakota County → Surface eviction defense module
- If issue type = "eviction" → Show timeline + motions

---

## ✅ Quality Assurance Checklist

Before adding to production library:

- ☐ All 7 files present in `DakotaCounty_EvictionDefense_Module/`
- ☐ Blueprint file `dakota_eviction_library_routes.py` in root
- ☐ Markdown files render correctly in UI
- ☐ Motion placeholders (e.g., `{{CASE_NO}}`) display as expected
- ☐ Multilingual strings load from JSON
- ☐ Search endpoint returns relevant results
- ☐ Links to MN Judicial Branch forms functional
- ☐ Disclaimer visible on all motion templates

---

## 📞 Support & Updates

**Module Maintainer:** Semptify Development Team  
**Version:** 1.0.0  
**Last Updated:** 2025-11-21

**Future Enhancements:**
- Additional Minnesota counties (Hennepin, Ramsey)
- Federal eviction defenses (CARES Act, HUD)
- Interactive decision tree wizard
- Automated court filing integration

**Statutory Update Check:**
- Monitor Minnesota Legislature for amendments to Chapter 504B
- Update `statutes_forms.md` if new provisions added
- Notify users of changes via in-app alerts

---

## 🚀 Quick Start Commands

### Test Blueprint Registration

```powershell
# From Semptify root directory
.\.venv\Scripts\python.exe -c "from dakota_eviction_library_routes import dakota_bp; print('Blueprint loaded:', dakota_bp.name)"
```

### Build Distribution Zip

```powershell
Push-Location 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module'
.\build_dakota_module.ps1
Pop-Location
```

### Test API Endpoints (After Server Start)

```powershell
# List documents
Invoke-RestMethod -Uri "http://localhost:8080/library/dakota_eviction/" -Method GET

# Get specific document
Invoke-RestMethod -Uri "http://localhost:8080/library/dakota_eviction/doc/motions" -Method GET

# Get motion template
Invoke-RestMethod -Uri "http://localhost:8080/library/dakota_eviction/motion/dismiss" -Method GET

# Search
Invoke-RestMethod -Uri "http://localhost:8080/library/dakota_eviction/search?q=habitability" -Method GET

# Get Spanish UI strings
Invoke-RestMethod -Uri "http://localhost:8080/library/dakota_eviction/ui_strings/es" -Method GET
```

---

## 📝 Librarian Action Items

1. **Review Module Contents**
   - Read `README.md` for overview
   - Scan `motions_actions.md` for template quality
   - Verify multilingual strings in `ui_strings.json`

2. **Choose Integration Method**
   - Option 1: Add to `doc_explorer`
   - Option 2: Register standalone blueprint
   - Option 3: Hybrid approach

3. **Implement Integration**
   - Edit `Semptify.py` (if standalone blueprint)
   - Edit `doc_explorer_routes.py` (if existing library)
   - Test endpoints after server restart

4. **Update Library Index**
   - Add category "Eviction Defense"
   - Create subcategory "Dakota County, MN"
   - Link to documents

5. **Test User Experience**
   - Navigate to library from GUI
   - Verify documents load correctly
   - Test search functionality
   - Check multilingual labels

6. **Configure Auto-Suggestions**
   - Implement trigger logic (service date, habitability tags, etc.)
   - Test suggestions appear in context

7. **Document for Users**
   - Add library tour/walkthrough
   - Create quick start guide
   - Highlight motion templates

---

**End of Librarian Notes**
