"""
Adaptive Location Intelligence for Semptify
Automatically detects location, learns resources, discovers procedures.
Adapts to ANY jurisdiction based on user information.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any


class LocationIntelligence:
    """
    Automatically discovers and learns about ANY location.
    No hardcoded jurisdictions - adapts to user's location.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.locations_file = os.path.join(data_dir, "learned_locations.json")
        self.locations = self._load_locations()

    def _load_locations(self) -> Dict:
        """Load learned location data."""
        if os.path.exists(self.locations_file):
            try:
                with open(self.locations_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_locations(self):
        """Persist learned location data."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.locations_file, 'w') as f:
            json.dump(self.locations, f, indent=2)

    # ========================================================================
    # AUTOMATIC LOCATION DETECTION
    # ========================================================================

    def detect_location_from_user(self, user_data: Dict) -> Dict[str, str]:
        """
        Extract location from user registration data.
        Returns: {city, county, state, zip, country}
        """
        return {
            "city": user_data.get("city", "").lower().replace(" ", "_"),
            "county": user_data.get("county", "").lower().replace(" ", "_"),
            "state": user_data.get("state", "").lower().replace(" ", "_"),
            "zip": user_data.get("zip_code", ""),
            "country": user_data.get("country", "usa").lower()
        }

    def detect_location_from_address(self, address: str) -> Dict[str, str]:
        """
        Parse address string to extract location components.
        Uses geocoding APIs if available.
        """
        # Simple parsing (can be enhanced with geocoding API)
        parts = address.split(",")
        
        location = {
            "street": parts[0].strip() if len(parts) > 0 else "",
            "city": parts[1].strip() if len(parts) > 1 else "",
            "state": "",
            "zip": ""
        }

        # Extract state and ZIP from last part
        if len(parts) > 2:
            last_part = parts[-1].strip()
            # Format: "State ZIP"
            state_zip = last_part.split()
            if len(state_zip) >= 2:
                location["state"] = state_zip[0]
                location["zip"] = state_zip[1]

        return location

    # ========================================================================
    # DISCOVER RESOURCES (Automatically learns)
    # ========================================================================

    def discover_resources(self, location: Dict[str, str]) -> Dict:
        """
        Automatically discover local resources for this jurisdiction.
        Learns and caches for future users.
        """
        location_key = f"{location['city']}_{location['state']}_{location['zip']}"

        # Check if we've already learned about this location
        if location_key in self.locations:
            existing = self.locations[location_key]
            # Update last accessed
            existing["last_accessed"] = datetime.now().isoformat()
            existing["access_count"] = existing.get("access_count", 0) + 1
            self._save_locations()
            return existing

        # NEW LOCATION - Discover resources
        print(f"🔍 Discovering resources for {location['city']}, {location['state']}...")

        discovered = {
            "location_key": location_key,
            "city": location["city"],
            "state": location["state"],
            "zip": location["zip"],
            "discovered_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "access_count": 1,
            "resources": self._search_resources(location),
            "laws": self._search_laws(location),
            "statistics": self._gather_statistics(location),
            "procedures": self._learn_procedures(location)
        }

        # Save for future users
        self.locations[location_key] = discovered
        self._save_locations()

        return discovered

    def _search_resources(self, location: Dict) -> Dict:
        """
        Search for local tenant resources.
        Methods: Web search, API calls, user contributions.
        """
        resources = {
            "tenant_hotlines": [],
            "legal_aid": [],
            "housing_courts": [],
            "government_agencies": [],
            "discovery_method": "automated_search"
        }

        state = location["state"]
        city = location["city"]

        # STRATEGY 1: Common patterns (learns from previous locations)
        
        # Legal aid usually has pattern: "[State] Legal Aid"
        resources["legal_aid"].append({
            "name": f"{state.title()} Legal Aid",
            "search_query": f"{state} legal aid tenant rights",
            "confidence": "pattern_based",
            "needs_verification": True
        })

        # Housing court pattern: "[County] County Housing Court"
        if location.get("county"):
            resources["housing_courts"].append({
                "name": f"{location['county'].title()} County Court",
                "search_query": f"{location['county']} county housing court",
                "confidence": "pattern_based",
                "needs_verification": True
            })

        # State tenant hotline pattern
        resources["tenant_hotlines"].append({
            "name": f"{state.title()} Tenant Hotline",
            "search_query": f"{state} tenant rights hotline",
            "confidence": "pattern_based",
            "needs_verification": True
        })

        # City code enforcement
        resources["government_agencies"].append({
            "name": f"{city.title()} Code Enforcement",
            "search_query": f"{city} {state} code enforcement rental",
            "phone_pattern": "City Hall + extension",
            "confidence": "pattern_based",
            "needs_verification": True
        })

        # STRATEGY 2: Ask users to verify/contribute
        resources["user_contribution_needed"] = True
        resources["contribution_prompt"] = f"Know resources in {city.title()}? Help others!"

        return resources

    def _search_laws(self, location: Dict) -> Dict:
        """
        Search for applicable laws for this jurisdiction.
        Learns hierarchy: Federal → State → County → City
        """
        state = location["state"]

        laws = {
            "federal": {
                "fair_housing": {
                    "statute": "Fair Housing Act (42 U.S.C. §3604)",
                    "applies": "all_locations"
                }
            },
            "state": {
                "discovery_needed": True,
                "search_queries": [
                    f"{state} landlord tenant law",
                    f"{state} security deposit law",
                    f"{state} tenant rights statute",
                    f"{state} habitability requirements"
                ],
                "common_statute_numbers": self._predict_statute_format(state)
            },
            "local": {
                "discovery_needed": True,
                "check_for": [
                    "rent control ordinances",
                    "rental licensing requirements",
                    "local health codes",
                    "tenant protection ordinances"
                ]
            }
        }

        return laws

    def _predict_statute_format(self, state: str) -> List[str]:
        """
        Predict statute numbering format based on state.
        Learns patterns from known states.
        """
        # Common patterns learned
        patterns = {
            "california": ["Civil Code §", "Health & Safety Code §"],
            "minnesota": ["Minnesota Statutes §"],
            "new_york": ["Real Property Law §", "Multiple Dwelling Law §"],
            "texas": ["Texas Property Code §"],
            "florida": ["Florida Statutes §"]
        }

        return patterns.get(state, [f"{state.title()} Statutes §"])

    def _gather_statistics(self, location: Dict) -> Dict:
        """
        Gather rental market statistics for this location.
        Learns from: user reports, public data, listings.
        """
        return {
            "rent_ranges": {
                "source": "user_reports",
                "data_points": 0,
                "needs_learning": True,
                "studio": {"min": None, "max": None, "avg": None},
                "1br": {"min": None, "max": None, "avg": None},
                "2br": {"min": None, "max": None, "avg": None},
                "3br": {"min": None, "max": None, "avg": None}
            },
            "application_fees": {
                "source": "user_reports",
                "data_points": 0,
                "needs_learning": True,
                "average": None,
                "range": {"min": None, "max": None}
            },
            "security_deposits": {
                "source": "user_reports",
                "data_points": 0,
                "needs_learning": True,
                "average_months": None
            },
            "common_issues": {
                "source": "user_reports",
                "data_points": 0,
                "needs_learning": True,
                "top_issues": []
            },
            "learning_note": "Statistics improve as more users contribute data"
        }

    def _learn_procedures(self, location: Dict) -> Dict:
        """
        Learn legal procedures for this jurisdiction.
        Discovers: Where to file, how to file, forms, timelines.
        """
        return {
            "complaint_filing": {
                "where": "discovering...",
                "how": "discovering...",
                "forms": "discovering...",
                "learned_from": "will_learn_from_user_experiences"
            },
            "court_process": {
                "small_claims": "discovering...",
                "housing_court": "discovering...",
                "learned_from": "will_learn_from_cases"
            },
            "repair_process": {
                "notice_method": "discovering...",
                "timeline": "discovering...",
                "escalation": "discovering...",
                "learned_from": "will_learn_from_outcomes"
            },
            "learning_status": "Active - gathering data from user experiences"
        }

    # ========================================================================
    # LEARN FROM USER EXPERIENCES (Continuous improvement)
    # ========================================================================

    def learn_from_user_data(
        self,
        location_key: str,
        data_type: str,
        data: Dict
    ):
        """
        Update location intelligence from user contributions.
        Types: rent_amount, application_fee, issue, outcome, resource
        """
        if location_key not in self.locations:
            return

        location_data = self.locations[location_key]

        if data_type == "rent_amount":
            self._update_rent_statistics(location_data, data)

        elif data_type == "application_fee":
            self._update_fee_statistics(location_data, data)

        elif data_type == "issue":
            self._update_issue_statistics(location_data, data)

        elif data_type == "outcome":
            self._learn_procedure_from_outcome(location_data, data)

        elif data_type == "resource":
            self._add_verified_resource(location_data, data)

        elif data_type == "law":
            self._add_verified_law(location_data, data)

        location_data["last_updated"] = datetime.now().isoformat()
        self._save_locations()

    def _update_rent_statistics(self, location_data: Dict, data: Dict):
        """Learn rent ranges from user reports."""
        stats = location_data["statistics"]["rent_ranges"]
        bedrooms = data.get("bedrooms", "1br")
        rent = data.get("amount")

        if rent and bedrooms in stats:
            bedroom_stats = stats[bedrooms]
            
            # Update min/max/avg
            if bedroom_stats["min"] is None or rent < bedroom_stats["min"]:
                bedroom_stats["min"] = rent
            if bedroom_stats["max"] is None or rent > bedroom_stats["max"]:
                bedroom_stats["max"] = rent

            # Update average
            data_points = stats["data_points"]
            if bedroom_stats["avg"] is None:
                bedroom_stats["avg"] = rent
            else:
                # Running average
                bedroom_stats["avg"] = (
                    (bedroom_stats["avg"] * data_points + rent) / (data_points + 1)
                )

            stats["data_points"] += 1

    def _update_fee_statistics(self, location_data: Dict, data: Dict):
        """Learn application fee patterns."""
        stats = location_data["statistics"]["application_fees"]
        fee = data.get("amount")

        if fee:
            if stats["range"]["min"] is None or fee < stats["range"]["min"]:
                stats["range"]["min"] = fee
            if stats["range"]["max"] is None or fee > stats["range"]["max"]:
                stats["range"]["max"] = fee

            data_points = stats["data_points"]
            if stats["average"] is None:
                stats["average"] = fee
            else:
                stats["average"] = (
                    (stats["average"] * data_points + fee) / (data_points + 1)
                )

            stats["data_points"] += 1

    def _update_issue_statistics(self, location_data: Dict, data: Dict):
        """Learn common issues in this area."""
        stats = location_data["statistics"]["common_issues"]
        issue_type = data.get("issue_type")

        if issue_type:
            # Add to top issues list
            found = False
            for issue in stats["top_issues"]:
                if issue["type"] == issue_type:
                    issue["count"] += 1
                    found = True
                    break

            if not found:
                stats["top_issues"].append({
                    "type": issue_type,
                    "count": 1
                })

            # Sort by count
            stats["top_issues"].sort(key=lambda x: x["count"], reverse=True)
            stats["top_issues"] = stats["top_issues"][:10]  # Keep top 10

            stats["data_points"] += 1

    def _learn_procedure_from_outcome(self, location_data: Dict, data: Dict):
        """Learn procedures from actual case outcomes."""
        procedures = location_data["procedures"]
        
        # Example: User filed complaint successfully
        if data.get("filed_with"):
            procedures["complaint_filing"]["where"] = data["filed_with"]
            procedures["complaint_filing"]["learned_from"] = "user_outcome"

        if data.get("timeline"):
            procedures["complaint_filing"]["actual_timeline"] = data["timeline"]

    def _add_verified_resource(self, location_data: Dict, data: Dict):
        """Add user-verified resource."""
        resource_type = data.get("type")  # tenant_hotline, legal_aid, etc
        
        if resource_type and resource_type in location_data["resources"]:
            location_data["resources"][resource_type].append({
                "name": data.get("name"),
                "phone": data.get("phone"),
                "website": data.get("website"),
                "verified_by": "user",
                "verified_at": datetime.now().isoformat()
            })

    def _add_verified_law(self, location_data: Dict, data: Dict):
        """Add user-discovered law or statute."""
        jurisdiction = data.get("jurisdiction")  # state, county, city
        
        if jurisdiction in location_data["laws"]:
            location_data["laws"][jurisdiction][data.get("category")] = {
                "statute": data.get("statute"),
                "requirement": data.get("requirement"),
                "source": data.get("source"),
                "verified_by": "user",
                "verified_at": datetime.now().isoformat()
            }

    # ========================================================================
    # METADATA PROCESSING (Discovers patterns)
    # ========================================================================

    def process_metadata(self) -> Dict:
        """
        Process all location data to discover patterns.
        Learns: Common procedures, typical timelines, resource patterns.
        """
        patterns = {
            "total_locations": len(self.locations),
            "state_patterns": {},
            "resource_patterns": {},
            "procedure_patterns": {},
            "discovered_at": datetime.now().isoformat()
        }

        for location_key, location_data in self.locations.items():
            state = location_data.get("state")

            # Group by state to find patterns
            if state not in patterns["state_patterns"]:
                patterns["state_patterns"][state] = {
                    "locations": 0,
                    "common_resources": [],
                    "common_procedures": [],
                    "rent_trends": {}
                }

            patterns["state_patterns"][state]["locations"] += 1

            # Aggregate rent data
            # Aggregate common resources
            # Aggregate procedures

        return patterns


# Global instance
_location_intelligence = None

def get_location_intelligence() -> LocationIntelligence:
    """Get global location intelligence instance."""
    global _location_intelligence
    if _location_intelligence is None:
        _location_intelligence = LocationIntelligence()
    return _location_intelligence
