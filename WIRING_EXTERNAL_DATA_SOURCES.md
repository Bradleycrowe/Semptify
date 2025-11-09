# 🔌 Wiring External Data Sources - Code Examples

## Table of Contents

1. [Public APIs (No Auth Needed)](#public-apis)
2. [Government APIs (With Auth)](#government-apis)
3. [Database Integration](#database-integration)
4. [Real-time Data Feeds](#real-time-data)
5. [Community/Organization APIs](#community-apis)
6. [Error Handling & Caching](#error-handling)

---

## Public APIs (No Auth Needed)

### Example 1: State Statutes (OpenStates Project)

```python
# File: statute_module.py

from preliminary_learning import PreliminaryLearningModule
import requests
from typing import Dict, List
import json

class StatuteModule(PreliminaryLearningModule):
    """Wire in state statute information via OpenStates API."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://openstates.org/api/v3"
        self.cache = {}

    def get_statutes_for_state(self, state_code: str, topic: str) -> Dict:
        """
        Fetch statutes for a state on a given topic.

        Example:
            get_statutes_for_state("MN", "tenant rights")
        """
        cache_key = f"{state_code}_{topic}"

        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Query OpenStates API
            endpoint = f"{self.base_url}/bills"
            params = {
                "jurisdiction": state_code,
                "query": topic,
                "classification": "bill",
                "per_page": 10
            }

            response = requests.get(endpoint, params=params, timeout=5)

            if response.status_code == 200:
                bills = response.json()["results"]

                # Extract relevant statutes
                statutes = []
                for bill in bills:
                    statute = {
                        "id": bill.get("id"),
                        "title": bill.get("title"),
                        "identifier": bill.get("identifier"),
                        "state": state_code,
                        "topic": topic,
                        "url": bill.get("openstates_url"),
                        "status": bill.get("latest_action", {}).get("classification")
                    }
                    statutes.append(statute)

                result = {
                    "status": "success",
                    "state": state_code,
                    "topic": topic,
                    "count": len(statutes),
                    "statutes": statutes
                }

                # Cache for 24 hours
                self.cache[cache_key] = result
                return result

            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def search_statutes(self, state_code: str, keyword: str) -> List[Dict]:
        """Search for statutes by keyword."""
        result = self.get_statutes_for_state(state_code, keyword)
        return result.get("statutes", [])

# Wire into Flask:
# In preliminary_learning_routes.py

statute_module = StatuteModule()

@app.route('/api/learning/statutes/<state>/<topic>')
def get_statutes(state, topic):
    """Get statutes for state and topic."""
    result = statute_module.get_statutes_for_state(state, topic)
    return jsonify(result)

@app.route('/api/learning/statutes/search/<state>/<keyword>')
def search_statutes(state, keyword):
    """Search for statutes."""
    results = statute_module.search_statutes(state, keyword)
    return jsonify({"results": results})

# Usage:
# GET /api/learning/statutes/MN/tenant+rights
# GET /api/learning/statutes/search/CA/eviction
```

### Example 2: Property Tax Data (County Assessors)

```python
# File: property_module.py

class PropertyModule(PreliminaryLearningModule):
    """Wire in property tax and assessment data."""

    def __init__(self):
        super().__init__()
        # Different counties have different APIs
        self.county_apis = {
            "hennepin_county": "https://www.hennepin.us/residents/property-taxes",
            "ramsey_county": "https://www.ramseycounty.us/public-administrators/property-records"
        }
        self.cache = {}

    def lookup_property(self, address: str, county: str) -> Dict:
        """
        Lookup property tax and assessment info.
        Note: Each county has different format, so this is simplified.
        """
        cache_key = f"{address}_{county}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        # For real implementation, you'd scrape or API each county
        # Here's the pattern:

        try:
            # Example: Some counties expose GIS APIs
            response = requests.get(
                f"https://gis-api.{county}.gov/property",
                params={"address": address},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                result = {
                    "address": address,
                    "county": county,
                    "parcel_number": data.get("parcel_id"),
                    "estimated_value": data.get("market_value"),
                    "tax_amount": data.get("annual_tax"),
                    "zoning": data.get("zoning_classification"),
                    "unit_count": data.get("number_of_units")
                }
                self.cache[cache_key] = result
                return result

        except:
            pass

        return {
            "status": "not_found",
            "address": address,
            "county": county,
            "note": "Check county assessor website directly"
        }

    def is_multifamily(self, address: str, county: str) -> bool:
        """Check if property is multifamily (tenant protections)."""
        prop = self.lookup_property(address, county)
        units = prop.get("unit_count", 1)
        return units > 1

# Wire into Flask:
property_module = PropertyModule()

@app.route('/api/learning/property/<address>/<county>')
def lookup_property(address, county):
    """Lookup property info."""
    result = property_module.lookup_property(address, county)
    return jsonify(result)
```

---

## Government APIs (With Auth)

### Example 3: HUD Data (Fair Housing)

```python
# File: hud_module.py

import os
from dotenv import load_dotenv

load_dotenv()

class HUDModule(PreliminaryLearningModule):
    """Wire in HUD fair housing data."""

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HUD_API_KEY")
        self.base_url = "https://data.hud.gov/api/v1"

    def search_fair_housing_complaints(self, state: str) -> Dict:
        """
        Search fair housing complaints by state.
        Requires HUD API key from https://data.hud.gov/
        """
        try:
            endpoint = f"{self.base_url}/fairhousing/complaints"

            response = requests.get(
                endpoint,
                params={
                    "state": state,
                    "api_key": self.api_key
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                return {
                    "state": state,
                    "total_complaints": data.get("count", 0),
                    "complaints": data.get("results", []),
                    "data_source": "HUD Fair Housing Data"
                }

            return {"error": "HUD API request failed"}

        except Exception as e:
            return {"error": str(e)}

    def get_fha_protected_classes(self) -> List[str]:
        """Get list of Fair Housing Act protected classes."""
        return [
            "Race",
            "Color",
            "National Origin",
            "Religion",
            "Sex",
            "Familial Status",
            "Disability"
        ]

    def check_if_protected(self, discrimination_type: str) -> Dict:
        """Check if discrimination type is FHA-protected."""
        protected_classes = self.get_fha_protected_classes()

        is_protected = discrimination_type.title() in protected_classes

        return {
            "discrimination_type": discrimination_type,
            "is_protected": is_protected,
            "protected_classes": protected_classes if is_protected else None,
            "next_steps": [
                "File complaint with HUD",
                "Contact local fair housing center"
            ] if is_protected else ["Consult attorney"]
        }

# Wire into Flask:
# Add to .env file:
# HUD_API_KEY=your_key_here

hud_module = HUDModule()

@app.route('/api/learning/fha/complaints/<state>')
def get_fha_complaints(state):
    """Get fair housing complaints for state."""
    result = hud_module.search_fair_housing_complaints(state)
    return jsonify(result)

@app.route('/api/learning/fha/protected/<discrimination_type>')
def check_fha_protected(discrimination_type):
    """Check if discrimination is FHA-protected."""
    result = hud_module.check_if_protected(discrimination_type)
    return jsonify(result)
```

### Example 4: Census Bureau (Demographics & Poverty Data)

```python
# File: census_module.py

class CensusModule(PreliminaryLearningModule):
    """Wire in Census Bureau demographic and poverty data."""

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CENSUS_API_KEY")
        self.cache = {}

    def get_poverty_level(self, year: int = 2023) -> Dict:
        """
        Get current poverty level for eligibility determination.
        Important for legal aid, housing assistance, etc.
        """
        cache_key = f"poverty_{year}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        # Federal poverty levels (simplified - normally fetched from Census)
        poverty_guidelines = {
            2023: {
                "1_person": 13,820,
                "2_person": 18,600,
                "3_person": 23,380,
                "4_person": 28,160,
                "5_person": 32,940,
                "6_person": 37,720,
                "7_person": 42,500,
                "8_person": 47,280
            }
        }

        result = {
            "year": year,
            "guidelines": poverty_guidelines.get(year, {}),
            "source": "U.S. Census Bureau",
            "percent_of_poverty": 125  # 125% typical for legal aid eligibility
        }

        self.cache[cache_key] = result
        return result

    def check_legal_aid_eligibility(self, household_size: int, income: float, year: int = 2023) -> Dict:
        """
        Check if income qualifies for legal aid.
        Most legal aid uses 125-200% of poverty line.
        """
        poverty_data = self.get_poverty_level(year)
        guidelines = poverty_data["guidelines"]

        # Get poverty level for household size
        key = f"{household_size}_person"
        poverty_line = guidelines.get(key, guidelines.get("4_person"))

        # Legal aid typically at 125% of poverty
        legal_aid_threshold = poverty_line * 1.25

        is_eligible = income <= legal_aid_threshold

        return {
            "household_size": household_size,
            "annual_income": income,
            "poverty_line": poverty_line,
            "legal_aid_threshold": legal_aid_threshold,
            "is_eligible": is_eligible,
            "percentage_of_poverty": (income / poverty_line) * 100
        }

# Wire into Flask:
census_module = CensusModule()

@app.route('/api/learning/poverty-levels/<int:year>')
def get_poverty_levels(year):
    """Get poverty guidelines for year."""
    result = census_module.get_poverty_level(year)
    return jsonify(result)

@app.route('/api/learning/legal-aid-check')
def check_legal_aid_eligibility():
    """Check legal aid eligibility."""
    household_size = request.args.get('household_size', 1, type=int)
    income = request.args.get('income', 0, type=float)

    result = census_module.check_legal_aid_eligibility(household_size, income)
    return jsonify(result)

# Usage:
# GET /api/learning/legal-aid-check?household_size=3&income=30000
# Returns: {"is_eligible": true, "legal_aid_threshold": 23380, ...}
```

---

## Database Integration

### Example 5: Legal Aid Organization Directory

```python
# File: legal_aid_module.py

import sqlite3
from typing import List

class LegalAidModule(PreliminaryLearningModule):
    """Wire in local legal aid organizations from database."""

    def __init__(self, db_path: str = "data/legal_aid_orgs.db"):
        super().__init__()
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database with legal aid organization data."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Create table if doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS legal_aid_orgs (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                state TEXT NOT NULL,
                city TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                website TEXT,
                services TEXT,
                income_limit_percent REAL,
                coverage_area TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def add_organization(self, org_data: Dict) -> bool:
        """Add legal aid organization to database."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('''
                INSERT INTO legal_aid_orgs
                (name, state, city, address, phone, email, website, services, income_limit_percent, coverage_area)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                org_data.get('name'),
                org_data.get('state'),
                org_data.get('city'),
                org_data.get('address'),
                org_data.get('phone'),
                org_data.get('email'),
                org_data.get('website'),
                org_data.get('services'),
                org_data.get('income_limit_percent', 125),
                org_data.get('coverage_area')
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding organization: {e}")
            return False

    def find_legal_aid(self, state: str, city: str = None) -> List[Dict]:
        """Find legal aid organizations in area."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            if city:
                # Search by state and city
                c.execute('''
                    SELECT * FROM legal_aid_orgs
                    WHERE state = ? AND city = ?
                    ORDER BY name
                ''', (state, city))
            else:
                # Search by state only
                c.execute('''
                    SELECT * FROM legal_aid_orgs
                    WHERE state = ?
                    ORDER BY city, name
                ''', (state,))

            results = [dict(row) for row in c.fetchall()]
            conn.close()

            return results

        except Exception as e:
            return []

    def get_organization(self, org_id: int) -> Dict:
        """Get organization details."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM legal_aid_orgs WHERE id = ?', (org_id,))

            row = c.fetchone()
            conn.close()

            return dict(row) if row else {"error": "Not found"}

        except Exception as e:
            return {"error": str(e)}

    def check_if_covered(self, state: str, city: str, income: float, household_size: int) -> Dict:
        """Check if area has coverage and if income qualifies."""
        orgs = self.find_legal_aid(state, city)

        if not orgs:
            # Fallback to state-level search
            orgs = self.find_legal_aid(state)

        # Check income eligibility
        from census_module import CensusModule  # Reuse census module
        census = CensusModule()
        eligibility = census.check_legal_aid_eligibility(household_size, income)

        return {
            "state": state,
            "city": city,
            "covered": len(orgs) > 0,
            "organizations": orgs,
            "income_eligible": eligibility["is_eligible"],
            "income_details": eligibility
        }

# Wire into Flask:
legal_aid_module = LegalAidModule()

@app.route('/api/learning/legal-aid/<state>')
def find_legal_aid(state):
    """Find legal aid in state."""
    city = request.args.get('city')
    result = legal_aid_module.find_legal_aid(state, city)
    return jsonify({"organizations": result})

@app.route('/api/learning/legal-aid/<state>/coverage-check')
def check_coverage(state):
    """Check if area has legal aid coverage."""
    city = request.args.get('city', '')
    income = request.args.get('income', 0, type=float)
    household = request.args.get('household_size', 1, type=int)

    result = legal_aid_module.check_if_covered(state, city, income, household)
    return jsonify(result)

@app.route('/api/learning/legal-aid/org/<int:org_id>', methods=['POST'])
def add_legal_aid_org(org_id):
    """Add new legal aid organization."""
    data = request.json
    success = legal_aid_module.add_organization(data)
    return jsonify({"success": success})
```

---

## Real-time Data Feeds

### Example 6: Court Calendar Events

```python
# File: court_calendar_module.py

class CourtCalendarModule(PreliminaryLearningModule):
    """Wire in court calendars and hearing schedules."""

    def __init__(self):
        super().__init__()
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour for court data

    def get_court_calendar(self, jurisdiction: str, date_start: str, date_end: str) -> Dict:
        """
        Get court calendar for jurisdiction.

        Some courts expose public calendar APIs or RSS feeds.
        Example format: date_start="2024-01-01", date_end="2024-01-31"
        """
        cache_key = f"{jurisdiction}_{date_start}_{date_end}"

        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            age = (datetime.now() - timestamp).seconds
            if age < self.cache_ttl:
                return cached_data

        # Try to fetch from court API or scrape calendar
        try:
            # Different jurisdictions have different APIs
            if "minneapolis" in jurisdiction.lower():
                url = "https://www1.minneapolismn.gov/courts/calendar"
                # Parse calendar (varies by court)
                events = self._parse_court_calendar(url, date_start, date_end)

            result = {
                "jurisdiction": jurisdiction,
                "date_range": {"start": date_start, "end": date_end},
                "events": events,
                "cached": False
            }

            # Cache result
            self.cache[cache_key] = (result, datetime.now())
            return result

        except Exception as e:
            return {
                "error": "Could not fetch calendar",
                "jurisdiction": jurisdiction,
                "suggestion": "Visit court website directly"
            }

    def _parse_court_calendar(self, url: str, date_start: str, date_end: str) -> List[Dict]:
        """Parse court calendar from website."""
        # This would use BeautifulSoup or similar to scrape
        # Placeholder implementation
        return [
            {
                "date": "2024-01-15",
                "time": "10:00 AM",
                "event": "Housing Court - Eviction Hearings",
                "judge": "Judge Smith",
                "courtroom": "Room 302"
            }
        ]

    def get_next_hearing(self, jurisdiction: str, case_type: str) -> Dict:
        """Get next scheduled hearing in jurisdiction."""
        import datetime as dt

        today = dt.date.today()
        next_month = today + dt.timedelta(days=30)

        calendar = self.get_court_calendar(
            jurisdiction,
            today.isoformat(),
            next_month.isoformat()
        )

        # Filter for case type
        hearings = [e for e in calendar.get("events", []) if case_type.lower() in e.get("event", "").lower()]

        if hearings:
            return {
                "jurisdiction": jurisdiction,
                "case_type": case_type,
                "next_hearing": hearings[0],
                "additional_hearings": len(hearings) - 1
            }

        return {
            "jurisdiction": jurisdiction,
            "case_type": case_type,
            "next_hearing": None,
            "message": "No hearings scheduled"
        }

# Wire into Flask:
court_module = CourtCalendarModule()

@app.route('/api/learning/court-calendar/<jurisdiction>')
def get_court_calendar(jurisdiction):
    """Get court calendar."""
    date_start = request.args.get('start', datetime.now().date().isoformat())
    date_end = request.args.get('end', (datetime.now() + timedelta(days=30)).date().isoformat())

    result = court_module.get_court_calendar(jurisdiction, date_start, date_end)
    return jsonify(result)

@app.route('/api/learning/next-hearing/<jurisdiction>/<case_type>')
def get_next_hearing(jurisdiction, case_type):
    """Get next hearing."""
    result = court_module.get_next_hearing(jurisdiction, case_type)
    return jsonify(result)
```

---

## Community/Organization APIs

### Example 7: Tenant Union & Advocacy Groups

```python
# File: advocacy_module.py

class AdvocacyModule(PreliminaryLearningModule):
    """Wire in tenant unions, advocacy groups, and resources."""

    def __init__(self):
        super().__init__()
        self.organizations = self._load_organizations()

    def _load_organizations(self) -> Dict:
        """Load tenant unions and advocacy groups."""
        return {
            "national": [
                {
                    "name": "National Alliance of HUD Tenants",
                    "website": "https://www.nationaltenants.org",
                    "services": ["Advocacy", "Resources", "Training"],
                    "contact": "contact@nationaltenants.org"
                },
                {
                    "name": "National Low Income Housing Coalition",
                    "website": "https://nlihc.org",
                    "services": ["Advocacy", "Research", "Recommendations"],
                    "contact": "info@nlihc.org"
                }
            ],
            "regional": {
                "minneapolis": [
                    {
                        "name": "Minneapolis Tenants Union",
                        "website": "https://minneapolistenants.org",
                        "services": ["Tenant rights", "Organizing", "Legal support"],
                        "contact": "contact@minneapolistenants.org"
                    }
                ],
                "california": [
                    {
                        "name": "California Tenants Union",
                        "website": "https://catenants.org",
                        "services": ["Rights", "Organizing", "Education"],
                        "contact": "info@catenants.org"
                    }
                ]
            }
        }

    def find_advocacy_groups(self, state: str, city: str = None) -> List[Dict]:
        """Find tenant unions and advocacy groups."""
        groups = []

        # Add national groups
        groups.extend(self.organizations.get("national", []))

        # Add regional groups
        regional = self.organizations.get("regional", {})
        if city:
            city_key = city.lower().replace(" ", "_")
            if city_key in regional:
                groups.extend(regional[city_key])

        # Add state-level if available
        state_key = state.lower()
        if state_key in regional:
            groups.extend(regional[state_key])

        return groups

    def get_tenant_rights_guide(self, state: str) -> Dict:
        """Get tenant rights guide for state."""
        guides = {
            "MN": {
                "url": "https://www.shelterforce.org/article/minnesota-tenants-bill-rights/",
                "key_rights": [
                    "Right to habitability",
                    "Right to reasonable notice",
                    "Right to privacy",
                    "Protection from retaliation"
                ]
            },
            "CA": {
                "url": "https://www.dca.ca.gov/publications/landlordbook/index.shtml",
                "key_rights": [
                    "Right to habitability",
                    "Right to non-harassment",
                    "Just cause for eviction",
                    "Rent increase limitations"
                ]
            }
        }

        return guides.get(state, {
            "url": "Consult state housing authority",
            "key_rights": []
        })

# Wire into Flask:
advocacy_module = AdvocacyModule()

@app.route('/api/learning/advocacy-groups/<state>')
def find_advocacy_groups(state):
    """Find advocacy groups."""
    city = request.args.get('city')
    result = advocacy_module.find_advocacy_groups(state, city)
    return jsonify({"groups": result})

@app.route('/api/learning/tenant-rights/<state>')
def get_tenant_rights(state):
    """Get tenant rights guide."""
    result = advocacy_module.get_tenant_rights_guide(state)
    return jsonify(result)
```

---

## Error Handling & Caching

### Complete Module with Best Practices

```python
# File: robust_external_module.py

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustExternalModule(PreliminaryLearningModule):
    """
    Best practices for wiring external data sources:
    - Proper error handling
    - Intelligent caching
    - Rate limiting
    - Fallback data
    - Logging
    """

    def __init__(self, cache_ttl: int = 86400):
        super().__init__()
        self.cache = {}
        self.cache_ttl = cache_ttl  # 24 hours default
        self.request_log = []
        self.max_retries = 3

    def fetch_with_retry(self, url: str, params: Dict = None, timeout: int = 5) -> Optional[Dict]:
        """Fetch from external API with retry logic."""

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.max_retries})")

                response = requests.get(
                    url,
                    params=params,
                    timeout=timeout,
                    headers={"User-Agent": "Semptify Learning Module"}
                )

                # Log request
                self.request_log.append({
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "status": response.status_code,
                    "attempt": attempt + 1
                })

                if response.status_code == 200:
                    logger.info(f"Success from {url}")
                    return response.json()

                elif response.status_code == 429:
                    # Rate limited - back off exponentially
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited. Waiting {wait_time}s before retry")
                    time.sleep(wait_time)
                    continue

                elif response.status_code >= 500:
                    # Server error - retry
                    logger.warning(f"Server error {response.status_code}. Retrying...")
                    continue

                else:
                    logger.error(f"HTTP {response.status_code}: {response.text}")
                    return None

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    continue

            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    continue

            except Exception as e:
                logger.error(f"Error: {e}")
                return None

        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None

    def get_cached_or_fetch(self, cache_key: str, url: str, params: Dict = None) -> Dict:
        """Get from cache or fetch fresh data."""

        # Check cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            age = (datetime.now() - timestamp).seconds

            if age < self.cache_ttl:
                logger.info(f"Cache hit for {cache_key} (age: {age}s)")
                return {"status": "success", "cached": True, "data": data}

        # Fetch fresh
        logger.info(f"Cache miss for {cache_key}. Fetching fresh...")
        result = self.fetch_with_retry(url, params)

        if result:
            # Store in cache
            self.cache[cache_key] = (result, datetime.now())
            logger.info(f"Cached {cache_key}")
            return {"status": "success", "cached": False, "data": result}

        # Return cached data even if expired, if available
        if cache_key in self.cache:
            data, _ = self.cache[cache_key]
            logger.warning(f"Using stale cache for {cache_key}")
            return {"status": "warning", "cached": True, "stale": True, "data": data}

        # No data available
        logger.error(f"No data available for {cache_key}")
        return {"status": "error", "message": "Could not fetch data"}

    def clear_old_cache(self, older_than_hours: int = 24):
        """Clear old cache entries."""
        cutoff = datetime.now() - timedelta(hours=older_than_hours)

        keys_to_delete = []
        for key, (data, timestamp) in self.cache.items():
            if timestamp < cutoff:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.cache[key]
            logger.info(f"Cleared old cache: {key}")

        logger.info(f"Cleared {len(keys_to_delete)} cache entries")

# Wire into Flask with error handling:

robust_module = RobustExternalModule()

@app.route('/api/learning/external/<source>/<query>')
def query_external_source(source, query):
    """Query external source with error handling."""
    try:
        cache_key = f"{source}_{query}"
        url = f"https://api.example.com/{source}"

        result = robust_module.get_cached_or_fetch(
            cache_key,
            url,
            params={"q": query}
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@app.route('/api/learning/cache/clear', methods=['POST'])
def clear_cache():
    """Clear old cache entries."""
    hours = request.json.get('older_than_hours', 24)
    robust_module.clear_old_cache(hours)
    return jsonify({"status": "cleared"})

@app.route('/api/learning/cache/status')
def cache_status():
    """Get cache status."""
    return jsonify({
        "total_entries": len(robust_module.cache),
        "requests_logged": len(robust_module.request_log),
        "cache_ttl_hours": robust_module.cache_ttl / 3600
    })
```

---

## Summary: Wiring Pattern

1. **Create module class** inheriting from `PreliminaryLearningModule`
2. **Add fetch method** with error handling and caching
3. **Add processing logic** to transform external data
4. **Add routes** to expose via Flask API
5. **Test locally** via `curl` or Python
6. **Deploy** by pushing to git
7. **Monitor** cache and request logs

---

## External Data Sources Ready to Wire

| Source | Type | Effort | Examples |
|--------|------|--------|----------|
| OpenStates (Statutes) | Public API | Easy | State laws, bills |
| HUD (Fair Housing) | Gov API | Medium | Discrimination, complaints |
| Census Bureau (Demographics) | Gov API | Medium | Poverty levels, income data |
| County Assessors (Property) | Various | Hard | Tax data, property records |
| Court Systems (Calendars) | Web scrape | Hard | Hearing schedules, calendars |
| Legal Aid Orgs | Database | Medium | Organization directory |
| Tenant Unions | Web scrape | Easy | Advocacy resources |

---

**All examples follow the same pattern - pick your data source and wire it in!**
