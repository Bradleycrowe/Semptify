# 🧠 Semptify Learning Module Extensibility Guide

## Overview

The Semptify learning system is **fully designed for extensibility** - you can wire in new information sources and create new modules on demand. The system is modular, API-based, and follows a plug-and-play architecture.

---

## Architecture: How It's Currently Structured

### 1. Core Learning Modules

```
Semptify Learning System
├── preliminary_learning.py          ← Information acquisition module
│   └── PreliminaryLearningModule   (extensible knowledge base)
│
├── learning_adapter.py              ← Stage-based personalization
│   └── LearningAdapter             (connects to dashboard)
│
├── dashboard_components.py          ← Visual output layer
│   └── 5 Component Types
│
├── learning_routes.py               ← API endpoints
│   └── Flask routes for JSON access
│
└── preliminary_learning_routes.py   ← Module-specific routes
    └── REST API for module data
```

### 2. Information Flow

```
External Information Sources
        ↓
   Wire-in Point #1
        ↓
Knowledge Base (JSON files)
        ↓
   Learning Module API
        ↓
Dashboard Components
        ↓
User Interface
```

---

## How to Wire In New Information Sources

### Method 1: Add to Existing JSON Knowledge Base

**Most Simple - No Code Required**

```python
# In preliminary_learning.py, expand the knowledge base dict:

"funding_sources": {
    "NEW_FUNDING_TYPE": {
        "title": "Your New Funding Source",
        "description": "Details here...",
        "eligibility": [...],
        "access": [...],
        # Your custom fields here
    }
}
```

Then access via API:
```python
module = PreliminaryLearningModule()
funding_info = module.get_procedures("funding_sources", "NEW_FUNDING_TYPE")
```

**Pros**: No code changes needed, dynamic, JSON-persistent
**Cons**: Manual data entry, no real-time updates

---

### Method 2: Add New Category to Knowledge Base

**Simple - Extends Existing Module**

Example: Add "immigration_considerations" category:

```python
def _initialize_knowledge_base(self) -> dict:
    return {
        # ... existing categories ...

        "immigration_considerations": {
            "tenant_rights_for_immigrants": {
                "title": "Rights for Immigrants (Regardless of Status)",
                "content": {
                    "habitability_rights": "All tenants have right to safe housing",
                    "repair_rights": "All tenants can request repairs",
                    "privacy_protections": "No landlord can demand immigration status",
                    "wage_protection": "Wages cannot be withheld for immigration reasons"
                },
                "action_items": [...],
                "agencies": [...]
            },
            "documentation_needs": {
                "title": "What Documentation You Need",
                "items": [...]
            }
        },

        # ... rest of knowledge base ...
    }
```

Then use:
```python
immigration_info = module.get_procedures("immigration_considerations", "tenant_rights_for_immigrants")
```

**Pros**: Integrates seamlessly with existing system
**Cons**: Still manual data entry

---

### Method 3: Create New Learning Module Class

**Advanced - Full Extensibility**

Create a new module file: `specialized_learning_module.py`

```python
"""
Specialized Learning Module - Example: Court Procedure Learning
Can be wired into Semptify to extend learning capabilities
"""

from preliminary_learning import PreliminaryLearningModule
from typing import Dict, List, Optional
import json
from datetime import datetime

class SpecializedLearningModule(PreliminaryLearningModule):
    """
    Extends the base learning module with domain-specific knowledge.
    Example: Court procedures, eviction processes, etc.
    """

    def __init__(self, data_dir: str = "data"):
        super().__init__(data_dir)
        self.specialized_file = f"{data_dir}/specialized_knowledge.json"
        self.specialized_knowledge = self._load_specialized_knowledge()

    def _load_specialized_knowledge(self) -> dict:
        """Load specialized knowledge from file."""
        # Load from JSON, database, external API, etc.
        try:
            with open(self.specialized_file, 'r') as f:
                return json.load(f)
        except:
            return self._initialize_specialized_knowledge()

    def _initialize_specialized_knowledge(self) -> dict:
        """Initialize specialized knowledge base."""
        return {
            "court_procedures": {
                "small_claims": {
                    "title": "Small Claims Court for Tenant Disputes",
                    "jurisdiction": "Typically up to $10,000 (varies by state)",
                    "process": [
                        "File claim with court",
                        "Pay filing fee ($50-$200)",
                        "Serve defendant with notice",
                        "Attend hearing (may not need lawyer)",
                        "Judge decides",
                        "Collect judgment if you win"
                    ],
                    "costs": [
                        {"item": "Filing fee", "amount": "$75", "refundable": False},
                        {"item": "Service fee", "amount": "$50-100", "refundable": True}
                    ],
                    "evidence_needed": [
                        "Lease copy",
                        "Photos/videos",
                        "Email/text correspondence",
                        "Payment records",
                        "Receipts"
                    ],
                    "timeline_days": 30
                },
                # Add more court procedures as needed
            },
            "evidence_requirements": {
                "photo_quality": {
                    "resolution": "1920x1080 minimum",
                    "lighting": "Natural light preferred",
                    "metadata": "EXIF data should be preserved",
                    "dating": "Include visible timestamp when possible"
                },
                "video_quality": {
                    "format": "MP4, MOV, or AVI",
                    "resolution": "720p minimum",
                    "audio": "Clear audio helps (witness narration)",
                    "stabilization": "Use tripod or stabilization"
                },
                "documentation": {
                    "written": "Keep copies of all written communications",
                    "receipts": "Document all payments and expenses",
                    "timestamps": "Record dates and times of all incidents",
                    "witnesses": "Get contact info of any witnesses"
                }
            }
        }

    def get_court_procedure(self, procedure_type: str) -> Dict:
        """Get court procedure information."""
        procedures = self.specialized_knowledge.get("court_procedures", {})
        return procedures.get(procedure_type, {"error": "Procedure not found"})

    def calculate_small_claims_viability(self, claim_amount: float, issue_type: str) -> Dict:
        """Determine if small claims is viable option."""
        return {
            "claim_amount": claim_amount,
            "issue_type": issue_type,
            "is_viable": claim_amount <= 10000,  # Varies by state
            "recommended_action": "File in small claims court" if claim_amount <= 10000 else "Consult attorney",
            "timeline_weeks": 6,
            "success_factors": [
                "Complete documentation",
                "Clear evidence",
                "Written communication trail",
                "Accurate damages calculation"
            ]
        }

    def add_custom_knowledge(self, category: str, subcategory: str, data: Dict) -> bool:
        """Dynamically add new knowledge to the module."""
        if category not in self.specialized_knowledge:
            self.specialized_knowledge[category] = {}

        self.specialized_knowledge[category][subcategory] = data
        self._save_specialized_knowledge()
        return True

    def _save_specialized_knowledge(self):
        """Persist specialized knowledge."""
        with open(self.specialized_file, 'w') as f:
            json.dump(self.specialized_knowledge, f, indent=2)

    def fact_check_court_rule(self, claim: str, jurisdiction: str) -> Dict:
        """Fact-check a court rule."""
        # Query specialized knowledge
        result = {
            "claim": claim,
            "jurisdiction": jurisdiction,
            "verified": False,
            "details": "",
            "source": "Specialized Learning Module"
        }

        # Check against knowledge base
        claim_lower = claim.lower()
        all_knowledge = json.dumps(self.specialized_knowledge).lower()

        if claim_lower in all_knowledge:
            result["verified"] = True
            result["details"] = "Found in specialized court knowledge base"

        return result
```

**Usage in Flask:**

```python
# In preliminary_learning_routes.py

from specialized_learning_module import SpecializedLearningModule

specialized_module = SpecializedLearningModule()

@app.route('/api/learning/court/<procedure_type>')
def get_court_procedure(procedure_type):
    """Get court procedure from specialized module."""
    proc = specialized_module.get_court_procedure(procedure_type)
    return jsonify(proc)

@app.route('/api/learning/small-claims-check', methods=['POST'])
def check_small_claims_viability():
    """Check if case is viable for small claims."""
    data = request.json
    result = specialized_module.calculate_small_claims_viability(
        data.get('amount'),
        data.get('issue_type')
    )
    return jsonify(result)
```

**Pros**:
- Fully extensible with custom logic
- Can inherit from base module
- Dynamic data addition
- Can connect to databases/APIs

**Cons**:
- Requires Python development
- Must follow module interface

---

### Method 4: Wire In External Data Sources

**Advanced - Real-Time Integration**

```python
class ExternalDataLearningModule(PreliminaryLearningModule):
    """
    Connects to external data sources for real-time information.
    Examples: Legal databases, government APIs, etc.
    """

    def __init__(self, data_dir: str = "data"):
        super().__init__(data_dir)
        self.cache = {}  # Cache external API responses
        self.cache_ttl = 86400  # 24 hours

    def fetch_from_government_api(self, endpoint: str, params: dict) -> Dict:
        """
        Fetch information from government APIs.
        Example: HUD, CFPB, State Attorney General offices
        """
        import requests
        from datetime import datetime

        cache_key = f"{endpoint}_{json.dumps(params)}"

        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_ttl:
                return {"cached": True, "data": cached_data}

        # Fetch from external API
        try:
            response = requests.get(endpoint, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.cache[cache_key] = (data, datetime.now())
                return {"cached": False, "data": data}
        except Exception as e:
            return {"error": str(e)}

        return {"error": "Failed to fetch data"}

    def fetch_legal_aid_info(self, state: str) -> Dict:
        """
        Fetch legal aid information for a state.
        Sources: Legal Aid organizations, state bar associations
        """
        # Example: Query legal aid database API
        endpoint = f"https://legal-aid-api.example.com/state/{state}"
        return self.fetch_from_government_api(endpoint, {})

    def fetch_court_records(self, case_id: str, jurisdiction: str) -> Dict:
        """
        Fetch court records from public databases.
        Could integrate with:
        - PACER (federal courts)
        - State court record systems
        - County clerk databases
        """
        # Placeholder for court record integration
        return {
            "case_id": case_id,
            "jurisdiction": jurisdiction,
            "status": "Active research needed",
            "note": "Can integrate with specific court APIs"
        }

    def fetch_statute_updates(self, state: str, area: str) -> Dict:
        """
        Fetch recent statute updates.
        Could integrate with:
        - State legislative websites
        - Legal databases (LexisNexis, Westlaw)
        - Government repositories
        """
        # Placeholder for statute integration
        return {
            "state": state,
            "area": area,
            "last_updated": datetime.now().isoformat(),
            "note": "Can wire to legal information databases"
        }

    def fetch_agency_contact_info(self, agency_name: str, state: str) -> Dict:
        """
        Fetch current contact info for agencies.
        Could integrate with:
        - Government directories
        - Agency websites (scraped)
        - OpenRefine data
        """
        # Placeholder for agency info
        return {
            "agency": agency_name,
            "state": state,
            "contact_methods": ["phone", "email", "web", "in-person"],
            "note": "Can wire to government.info APIs"
        }
```

**Usage:**

```python
# In routes:

external_module = ExternalDataLearningModule()

@app.route('/api/learning/legal-aid/<state>')
def get_legal_aid(state):
    """Get current legal aid info for state."""
    info = external_module.fetch_legal_aid_info(state)
    return jsonify(info)

@app.route('/api/learning/court-records/<case_id>/<jurisdiction>')
def get_court_records(case_id, jurisdiction):
    """Look up court records."""
    records = external_module.fetch_court_records(case_id, jurisdiction)
    return jsonify(records)

@app.route('/api/learning/statute-updates/<state>/<area>')
def get_statute_updates(state, area):
    """Get recent statute updates."""
    updates = external_module.fetch_statute_updates(state, area)
    return jsonify(updates)
```

**Possible Data Sources to Wire:**

- **Legal Databases**
  - Google Scholar (scholar.google.com) - Free access to statutes
  - State Legislature websites
  - Legal Aid organizations

- **Government APIs**
  - HUD.gov API for housing data
  - CFPB API for complaints/data
  - OpenFDA for consumer product data
  - Data.gov for federal datasets

- **Court Records**
  - PACER (Federal courts)
  - State court systems
  - County clerks (many have APIs)

- **Real Estate Data**
  - Zillow API (limited free access)
  - County assessor databases
  - Property tax databases

- **Organizations**
  - Legal aid organizations
  - Tenant unions and advocacy groups
  - Fair housing centers
  - Community action agencies

**Pros**:
- Real-time data
- Always current
- Integrates multiple sources
- Can query on-demand

**Cons**:
- Requires API keys/access
- May have rate limits
- Dependency on external services
- Caching required for performance

---

### Method 5: Create Custom Fact-Checking Module

**Advanced - Validation Layer**

```python
class FactCheckingModule:
    """
    Extensible fact-checking system for verifying claims
    about housing procedures, legal requirements, etc.
    """

    def __init__(self):
        self.checks = {}
        self.sources = {}

    def register_check(self, claim_category: str, check_func: callable) -> None:
        """
        Register a custom fact-checking function.

        Example:
            module.register_check(
                "eviction_timeline",
                my_eviction_timeline_checker
            )
        """
        self.checks[claim_category] = check_func

    def register_source(self, source_name: str, source_data: dict) -> None:
        """Register a knowledge source."""
        self.sources[source_name] = source_data

    def fact_check(self, claim: str, category: str) -> Dict:
        """Execute fact-check with registered function."""
        if category in self.checks:
            check_func = self.checks[category]
            return check_func(claim)
        return {"status": "NO_CHECKER_REGISTERED"}

    # Example custom checks

    def check_eviction_timeline(self, claim: str) -> Dict:
        """Fact-check eviction timeline claims."""
        # Custom logic to verify eviction timelines
        return {
            "claim": claim,
            "verified": True/False,
            "correct_timeline": "...",
            "source": "MN Statutes § 504B.135"
        }

    def check_repair_rights(self, claim: str) -> Dict:
        """Fact-check tenant repair rights claims."""
        # Custom logic to verify repair rights
        return {
            "claim": claim,
            "verified": True/False,
            "tenant_remedy": "repair-and-deduct",
            "timeline_days": 14
        }

    def check_illegal_clause(self, clause_text: str) -> Dict:
        """Determine if a lease clause is illegal."""
        illegal_keywords = [
            "no repairs", "waive rights", "landlord entry anytime",
            "no retaliation clause", "no pets service animal"
        ]

        is_illegal = any(kw in clause_text.lower() for kw in illegal_keywords)

        return {
            "clause": clause_text,
            "is_illegal": is_illegal,
            "reason": "If illegal, why",
            "remedy": "Tenant recourse options"
        }

# Usage:

fact_checker = FactCheckingModule()

# Register custom checks
fact_checker.register_check("eviction", fact_checker.check_eviction_timeline)
fact_checker.register_check("repair", fact_checker.check_repair_rights)
fact_checker.register_check("illegal_clause", fact_checker.check_illegal_clause)

# Use in Flask:
@app.route('/api/fact-check/<category>', methods=['POST'])
def fact_check(category):
    data = request.json
    result = fact_checker.fact_check(data.get('claim'), category)
    return jsonify(result)
```

---

## How to Add New Modules at Runtime

### Step 1: Create Module File

```bash
# Example: Create new funding sources module
touch additional_funding_module.py
```

### Step 2: Implement Module Class

```python
# additional_funding_module.py

class AdditionalFundingModule:
    """New module for emerging funding sources."""

    def __init__(self):
        self.funding_sources = self._load_sources()

    def _load_sources(self):
        return {
            "emergency_assistance": [...],
            "community_programs": [...],
            "nonprofit_grants": [...]
        }

    def get_sources_for_situation(self, situation: str):
        """Get funding sources matching situation."""
        # Implementation
        pass
```

### Step 3: Register with Flask

```python
# In Semptify.py

from additional_funding_module import AdditionalFundingModule

funding_module = AdditionalFundingModule()

@app.route('/api/learning/funding/<situation>')
def get_funding(situation):
    sources = funding_module.get_sources_for_situation(situation)
    return jsonify(sources)
```

### Step 4: Wire to Dashboard

```python
# In learning_adapter.py

def _build_funding_component(self):
    """Include funding info in dashboard."""
    from additional_funding_module import AdditionalFundingModule

    funding_module = AdditionalFundingModule()
    sources = funding_module.get_sources_for_situation(self.issue_type)

    component = InformationComponent()
    for source in sources:
        component.add_guidance(source["name"], source["description"])

    return component
```

---

## Summary: Extensibility Levels

| Level | Method | Effort | Power | Example |
|-------|--------|--------|-------|---------|
| **1** | Edit JSON | ⭐ | ⭐ | Add funding source to knowledge base |
| **2** | Add Category | ⭐⭐ | ⭐⭐ | Add "immigration" category |
| **3** | New Module Class | ⭐⭐⭐ | ⭐⭐⭐ | Court procedures module |
| **4** | External Data Sources | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Wire HUD.gov API |
| **5** | Custom Fact-Checking | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Verify legal claims |

---

## Current Wiring: What's Connected Now

✅ **Already Wired In:**
- Rental procedures (lease, move-in, rent payment, deposits)
- Legal procedures (tenant rights, maintenance rights, harassment)
- Court procedures (small claims, eviction, summary judgment)
- Complaint filing (housing authority, attorney general, tenant union)
- Funding sources (legal aid, grants, pro bono)
- Governing agencies (federal, state, local)
- Fact-checking (illegal clauses, timelines, verification)

⏳ **Ready to Wire:**
- Immigration-specific information
- Employment-related housing issues
- Disability/ADA accommodations
- Section 8/public housing procedures
- Eviction defense strategies
- Evidence preservation guides
- Court room preparation guides
- Appeal procedures

🔌 **Can Be Wired:**
- Real-time statute updates (via state legislature APIs)
- Court record lookups (via PACER or state courts)
- Legal aid contact info (via organization APIs)
- Complaint status tracking (via agency portals)
- Evidence storage and analysis
- Timeline visualization
- AI-powered legal advice (via LLM integration)

---

## Example: Wire New Module in 5 Minutes

### Scenario: Add "Eviction Defense" module

```python
# Step 1: Create module file
# File: eviction_defense_module.py

class EvictionDefenseModule:
    DEFENSES = {
        "illegal_notice": {
            "name": "Illegal Notice",
            "how_to_use": "Challenge the notice format or service",
            "success_rate": "High if notice improper",
            "action_required": "File response in court"
        },
        "no_cause": {
            "name": "No Cause Provided",
            "how_to_use": "Require landlord to state legal reason",
            "success_rate": "Medium",
            "action_required": "Demand valid notice"
        },
        "retaliation": {
            "name": "Retaliation Defense",
            "how_to_use": "Prove eviction is retaliation for rights exercise",
            "success_rate": "High if evidence exists",
            "action_required": "File affidavit in court"
        }
    }

    def get_applicable_defenses(self, eviction_reason):
        # Return relevant defenses
        pass

# Step 2: Add route
# In Semptify.py

from eviction_defense_module import EvictionDefenseModule

defense_module = EvictionDefenseModule()

@app.route('/api/learning/eviction-defenses/<reason>')
def get_eviction_defenses(reason):
    defenses = defense_module.get_applicable_defenses(reason)
    return jsonify(defenses)

# Step 3: Use it!
# In dashboard:

defenses = defense_module.get_applicable_defenses("non-payment")
# Display to user in eviction scenario
```

**That's it! Module is wired and ready to use.**

---

## Best Practices for Adding Modules

1. **Start with JSON** - Use JSON knowledge base for simple data
2. **Inherit from Base** - Extend `PreliminaryLearningModule` for consistency
3. **Create Routes** - Wire new modules via Flask routes
4. **Add Tests** - Create unit tests for new modules
5. **Document** - Include docstrings and usage examples
6. **Version** - Track changes in `data/` directory
7. **Cache** - Cache external API responses to avoid rate limits
8. **Validate** - Fact-check all new information
9. **Monitor** - Track usage and accuracy

---

## Next Steps: What to Build

**High Priority:**
- [ ] Eviction defense module
- [ ] Evidence preservation guide
- [ ] Court appearance preparation
- [ ] Appeal procedures

**Medium Priority:**
- [ ] Immigration-specific module
- [ ] Disability accommodations module
- [ ] Public housing/Section 8 module
- [ ] Employment-related housing issues

**Low Priority (Advanced):**
- [ ] Real-time statute integration
- [ ] Court record API integration
- [ ] AI-powered legal analysis
- [ ] Predictive outcome modeling

---

**Conclusion**: The Semptify learning system is fully extensible. You can wire in new information sources, create new modules, and connect external data APIs. Start simple with JSON, then scale up to sophisticated integrations as needed.
