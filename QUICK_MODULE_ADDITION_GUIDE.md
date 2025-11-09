# ⚡ Quick Start: Add New Learning Module to Semptify

## 5-Minute Module Addition Checklist

You want to add information about **[NEW TOPIC]**? Follow this template.

---

## Option A: Simple (JSON Only - 2 Minutes)

### Step 1: Edit `preliminary_learning.py`

Find the `_initialize_knowledge_base()` method and add:

```python
"your_new_category": {
    "subcategory_name": {
        "title": "Display Name",
        "description": "What this is about",
        "steps": [
            "Step 1",
            "Step 2",
            "Step 3"
        ],
        "forms_required": [
            "Form 1",
            "Form 2"
        ],
        "timeline_days": 7,
        "jurisdiction_specific": True/False,
        "free": True/False
    }
}
```

### Step 2: Access via API

```bash
# Get your new data:
GET /api/learning/procedures/your_new_category/subcategory_name
```

### Step 3: Done! ✅

Your data is now:
- ✅ Searchable via fact-checking
- ✅ Available in API
- ✅ Can be displayed in dashboard
- ✅ Persistent (saves to JSON)

---

## Option B: Medium (New Module Class - 10 Minutes)

### Step 1: Create New File

**File**: `my_learning_module.py`

```python
from preliminary_learning import PreliminaryLearningModule
from typing import Dict, List
import json

class MyLearningModule(PreliminaryLearningModule):
    """Custom module for [YOUR TOPIC]"""

    def __init__(self, data_dir: str = "data"):
        super().__init__(data_dir)
        self.my_data_file = f"{data_dir}/my_knowledge.json"
        self.my_knowledge = self._load_my_knowledge()

    def _load_my_knowledge(self) -> dict:
        try:
            with open(self.my_data_file, 'r') as f:
                return json.load(f)
        except:
            return self._initialize_my_knowledge()

    def _initialize_my_knowledge(self) -> dict:
        """Your custom knowledge base"""
        return {
            "topic_1": {
                "title": "Title",
                "content": "Your content",
                "steps": []
            },
            "topic_2": {
                "title": "Title",
                "content": "Your content"
            }
        }

    def get_my_topic(self, topic_id: str) -> Dict:
        """Get specific topic."""
        return self.my_knowledge.get(topic_id, {"error": "Not found"})

    def add_to_my_knowledge(self, topic_id: str, data: Dict):
        """Add new topic dynamically."""
        self.my_knowledge[topic_id] = data
        self._save_my_knowledge()

    def _save_my_knowledge(self):
        import os
        os.makedirs("data", exist_ok=True)
        with open(self.my_data_file, 'w') as f:
            json.dump(self.my_knowledge, f, indent=2)

    # Add your custom methods here:
    def analyze_my_data(self, input_data: str) -> Dict:
        """Your custom analysis logic."""
        return {
            "input": input_data,
            "analysis": "Your results"
        }
```

### Step 2: Add Routes in `preliminary_learning_routes.py`

```python
from my_learning_module import MyLearningModule
from flask import jsonify, request

my_module = MyLearningModule()

@app.route('/api/learning/my-topic/<topic_id>')
def get_my_topic(topic_id):
    """Get your custom topic."""
    data = my_module.get_my_topic(topic_id)
    return jsonify(data)

@app.route('/api/learning/my-analysis', methods=['POST'])
def analyze_my_data():
    """Run custom analysis."""
    input_data = request.json.get('data')
    result = my_module.analyze_my_data(input_data)
    return jsonify(result)

@app.route('/api/learning/my-topic/<topic_id>', methods=['POST'])
def add_my_topic(topic_id):
    """Add new topic dynamically."""
    data = request.json
    my_module.add_to_my_knowledge(topic_id, data)
    return jsonify({"status": "added", "topic_id": topic_id})
```

### Step 3: Use in Flask App

```python
# In Semptify.py, add to imports:
from my_learning_module import MyLearningModule

my_module = MyLearningModule()
```

### Step 4: Done! ✅

Your module is now:
- ✅ Running on Flask backend
- ✅ Has custom API endpoints
- ✅ Can add data dynamically
- ✅ Inherits all base features

**Access it:**
```bash
GET /api/learning/my-topic/topic_1
POST /api/learning/my-analysis { "data": "input" }
POST /api/learning/my-topic/new_topic { ...data... }
```

---

## Option C: Advanced (Wire External Data - 15 Minutes)

### Step 1: Create Integration Module

**File**: `external_data_module.py`

```python
from preliminary_learning import PreliminaryLearningModule
from typing import Dict
import requests
import json
from datetime import datetime

class ExternalDataModule(PreliminaryLearningModule):
    """Connect to external APIs/databases"""

    def __init__(self, data_dir: str = "data"):
        super().__init__(data_dir)
        self.cache = {}
        self.cache_ttl = 86400  # 24 hours

        # Wire your data sources here:
        self.data_sources = {
            "source_1": "https://api.example.com/endpoint",
            "source_2": "https://api2.example.com/data"
        }

    def fetch_from_source(self, source_name: str, params: Dict = None) -> Dict:
        """Fetch data from external source with caching."""
        cache_key = f"{source_name}_{json.dumps(params or {})}"

        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            age = (datetime.now() - timestamp).seconds
            if age < self.cache_ttl:
                return {"cached": True, "age_seconds": age, "data": cached_data}

        # Fetch from source
        try:
            url = self.data_sources.get(source_name)
            if not url:
                return {"error": f"Source {source_name} not configured"}

            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.cache[cache_key] = (data, datetime.now())
                return {"cached": False, "data": data}

            return {"error": f"HTTP {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def register_data_source(self, name: str, url: str, headers: Dict = None):
        """Register new external data source."""
        self.data_sources[name] = {
            "url": url,
            "headers": headers or {}
        }

    def query_source(self, source_name: str, query: str, filters: Dict = None) -> Dict:
        """Query external source."""
        params = {
            "q": query,
            **(filters or {})
        }
        return self.fetch_from_source(source_name, params)

    # Example: Fetch legal aid info
    def get_legal_aid_by_state(self, state_code: str) -> Dict:
        """Example: Fetch legal aid info from external database."""
        # This would query your legal aid database/API
        result = self.fetch_from_source("legal_aid_api", {"state": state_code})
        return result

    # Example: Search court records
    def search_court_records(self, case_number: str, jurisdiction: str) -> Dict:
        """Example: Search for court records."""
        result = self.fetch_from_source("court_records_api", {
            "case": case_number,
            "jurisdiction": jurisdiction
        })
        return result
```

### Step 2: Add Routes

```python
# In preliminary_learning_routes.py

from external_data_module import ExternalDataModule

external_module = ExternalDataModule()

# Register your data sources:
external_module.register_data_source(
    "hud_data",
    "https://data.hud.gov/api/3/",
    {"Authorization": "Bearer YOUR_KEY"}
)

@app.route('/api/learning/external/<source>/<query>')
def query_external_source(source, query):
    """Query external data source."""
    result = external_module.query_source(source, query)
    return jsonify(result)

@app.route('/api/learning/legal-aid/<state>')
def get_legal_aid(state):
    """Get legal aid info for state."""
    result = external_module.get_legal_aid_by_state(state)
    return jsonify(result)

@app.route('/api/learning/court-records/<case>/<jurisdiction>')
def search_cases(case, jurisdiction):
    """Search court records."""
    result = external_module.search_court_records(case, jurisdiction)
    return jsonify(result)
```

### Step 3: Done! ✅

Your external data module:
- ✅ Fetches from real APIs
- ✅ Caches results (efficient)
- ✅ Handles errors gracefully
- ✅ Easy to add new sources

---

## Real-World Examples: What to Add

### Example 1: Immigration Resources Module

```python
# Quick add: JSON only

"immigration_resources": {
    "tenant_rights_for_immigrants": {
        "title": "Tenant Rights Regardless of Immigration Status",
        "key_points": [
            "All tenants have habitability rights",
            "Landlord cannot ask immigration status",
            "Cannot withhold wages",
            "Cannot discriminate based on national origin"
        ],
        "forms_required": [
            "Lease in your language (request)",
            "Habitability complaint form"
        ],
        "agencies": [
            "HUD (discrimination complaints)",
            "State Attorney General (tenant rights)"
        ]
    },
    "what_documentation_to_have": {
        "title": "Helpful Documentation",
        "documents": [
            "ID (any kind)",
            "Lease copy",
            "Photos of conditions",
            "Payment records"
        ]
    }
}
```

### Example 2: Evidence Preservation Module

```python
# Create class:

class EvidenceModule(PreliminaryLearningModule):
    """Guide for preserving evidence properly."""

    def __init__(self):
        super().__init__()

    def get_evidence_standards(self, evidence_type: str) -> Dict:
        """Get proper preservation standards."""
        standards = {
            "photo": {
                "resolution": "1920x1080 minimum",
                "format": "JPEG, PNG (lossless better)",
                "metadata": "Keep EXIF data",
                "dating": "Timestamp important"
            },
            "video": {
                "resolution": "720p minimum",
                "format": "MP4, MOV",
                "audio": "Clear is better",
                "stabilization": "Use tripod"
            },
            "written": {
                "keep_originals": "Always",
                "scan_copies": "300 DPI",
                "chain_of_custody": "Document who handled"
            }
        }
        return standards.get(evidence_type)

    def check_evidence_admissibility(self, evidence_type: str, court_type: str) -> Dict:
        """Check if evidence is likely admissible."""
        return {
            "evidence_type": evidence_type,
            "court": court_type,
            "likely_admissible": True/False,
            "conditions": ["Must have proper foundation", "..."]
        }
```

### Example 3: Complaint Filing Module

```python
# Medium complexity - Custom module

class ComplaintFilingModule(PreliminaryLearningModule):
    """Comprehensive complaint filing guide."""

    COMPLAINT_AGENCIES = {
        "housing_authority": {
            "name": "Local Housing Authority",
            "purpose": "Enforce housing code violations",
            "timeline": "14 days for inspection"
        },
        "ag_office": {
            "name": "State Attorney General",
            "purpose": "Consumer protection violations",
            "timeline": "30 days for review"
        },
        "hud": {
            "name": "HUD Fair Housing Office",
            "purpose": "Discrimination complaints",
            "timeline": "60 days investigation"
        }
    }

    def get_best_agency(self, issue_type: str) -> List[str]:
        """Recommend which agency to file with."""
        # Logic to recommend agencies based on issue
        pass

    def generate_complaint_checklist(self, agency: str) -> List[str]:
        """Generate filing checklist for agency."""
        # Return what's needed for that agency
        pass

    def track_complaint(self, complaint_id: str) -> Dict:
        """Get status of filed complaint."""
        # Query agency or internal database
        pass
```

---

## Testing Your New Module

### Quick Test

```bash
# Test in Python:
python

>>> from my_learning_module import MyLearningModule
>>> module = MyLearningModule()
>>> data = module.get_my_topic("topic_1")
>>> print(data)
```

### Test via API

```bash
# Start server:
python Semptify.py

# Test endpoint:
curl http://localhost:5000/api/learning/my-topic/topic_1

# Test POST:
curl -X POST http://localhost:5000/api/learning/my-analysis \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

---

## Adding to Dashboard

Once your module is wired, add it to the dashboard:

```python
# In learning_adapter.py

def _build_resources_component(self):
    """Include your module data in dashboard."""
    from my_learning_module import MyLearningModule

    module = MyLearningModule()

    component = InformationComponent()

    for topic_id in ["topic_1", "topic_2"]:
        data = module.get_my_topic(topic_id)
        component.add_guidance(data["title"], data.get("description", ""))

    return component
```

---

## Complexity vs. Benefit

| Approach | Time | Effort | Benefit | Use When |
|----------|------|--------|---------|----------|
| **JSON** | 2 min | Low | Static knowledge | Data doesn't change |
| **Class** | 10 min | Medium | Reusable logic | Custom processing needed |
| **External API** | 20 min | High | Real-time data | Need current info |

---

## Deployment

Once your module is working locally:

```bash
# Add to git
git add my_learning_module.py
git add preliminary_learning_routes.py

# Commit
git commit -m "Add my learning module"

# Push to Render
git push origin main

# Module is live at:
# https://semptify.onrender.com/api/learning/my-topic/...
```

---

## Quick Checklist for Your New Module

- [ ] Create module file (`my_module.py`)
- [ ] Define knowledge/data structure
- [ ] Add methods to retrieve/analyze data
- [ ] Create Flask routes in `preliminary_learning_routes.py`
- [ ] Test locally (`python Semptify.py`)
- [ ] Test API endpoints (curl or browser)
- [ ] Add to learning_adapter.py for dashboard integration
- [ ] Commit and push to main
- [ ] Verify live on Render
- [ ] Document in this file

---

## Questions? Examples?

Want to add:
- ✅ **More forms?** → Add to JSON in Step 1
- ✅ **Custom logic?** → Create class in Option B
- ✅ **Real-time data?** → Use Option C with API
- ✅ **User-contributed data?** → Add POST endpoint
- ✅ **Multi-language support?** → Add language field to data
- ✅ **Jurisdiction-specific info?** → Add state/jurisdiction field

**Just ask - the system is designed for extension!**
