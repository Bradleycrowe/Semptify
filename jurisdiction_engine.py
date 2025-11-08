"""
Jurisdiction Engine for Semptify
Determines which laws apply and in what order.
Resolves conflicts between federal, state, county, and city laws.

ADAPTIVE VERSION: Automatically learns laws for ANY location from user data.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from location_intelligence import get_location_intelligence


@dataclass
class LegalAuthority:
    """Represents a law or regulation at a specific level."""
    level: str  # "federal", "state", "county", "city", "lease"
    jurisdiction: str  # "USA", "California", "Sacramento County", "Sacramento City"
    statute: str  # "Civil Code §1942", "Ordinance §8.100.070"
    title: str
    requirement: str
    deadline: Optional[str] = None
    penalty: Optional[str] = None
    category: Optional[str] = None  # "health_hazard", "general_repair", "payment"
    protective_level: int = 0  # Higher = more protective to tenant


class JurisdictionEngine:
    """
    Determines which laws apply based on location and issue type.
    Resolves conflicts by applying most protective standard.
    """

    HIERARCHY = {
        "federal": 5,
        "state": 4,
        "county": 3,
        "city": 2,
        "lease": 1
    }

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.laws_file = os.path.join(data_dir, "laws_database.json")
        self.laws = self._load_laws()
        self.location_intel = get_location_intelligence()  # Adaptive learning

    def _load_laws(self) -> Dict:
        """
        Load legal database.
        NOW ADAPTIVE: Discovers laws for any location automatically.
        """
        if os.path.exists(self.laws_file):
            try:
                with open(self.laws_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Baseline federal laws (apply everywhere)
        return {
            "federal": {
                "fair_housing": {
                    "statute": "Fair Housing Act (42 U.S.C. §3604)",
                    "requirement": "No discrimination based on race, color, religion, sex, disability, familial status, or national origin",
                    "applies_to": "all"
                },
                "ada": {
                    "statute": "Americans with Disabilities Act",
                    "requirement": "Reasonable accommodations for disabled tenants",
                    "applies_to": "all"
                }
            }
            # State/County/City laws discovered dynamically based on user location
        }

    def determine_applicable_laws(
        self,
        issue_category: str,
        user_location: Dict[str, str] = None,
        city: str = None,
        county: str = None,
        state: str = None
    ) -> List[LegalAuthority]:
        """
        ADAPTIVE VERSION: Determine which laws apply to a specific issue.
        Automatically discovers laws if not already known.

        Args:
            issue_category: Type of issue (habitability, security_deposit, etc.)
            user_location: Dict with city, county, state, zip (PREFERRED)
            city/county/state: Legacy parameters (will be deprecated)

        Returns:
            List ordered by precedence (most protective first).
        """
        applicable = []

        # Extract location info
        if user_location:
            city = user_location.get("city")
            county = user_location.get("county")
            state = user_location.get("state")
            zip_code = user_location.get("zip")

        # If we don't know about this location yet, discover it!
        location_key = f"{city}_{state}_{zip_code}"
        if location_key not in self.location_intel.locations:
            print(f"🔍 New location detected: {city}, {state} - discovering resources...")
            location_data = self.location_intel.discover_resources({
                "city": city,
                "county": county,
                "state": state,
                "zip": zip_code
            })
        else:
            location_data = self.location_intel.locations[location_key]

        # Federal laws (always apply)
        for key, law in self.laws.get("federal", {}).items():
            if law.get("applies_to") == "all" or issue_category in law.get("applies_to", []):
                applicable.append(LegalAuthority(
                    level="federal",
                    jurisdiction="USA",
                    statute=law.get("statute"),
                    title=key,
                    requirement=law.get("requirement"),
                    deadline=law.get("deadline"),
                    penalty=law.get("penalty"),
                    category=law.get("category"),
                    protective_level=law.get("protective_level", 5)
                ))

        # State laws (from discovered location data)
        state_laws = location_data.get("laws", {}).get("state", {})
        for key, law in state_laws.items():
            if isinstance(law, dict) and (
                law.get("category") == issue_category or
                issue_category in ["all", law.get("category")]
            ):
                applicable.append(LegalAuthority(
                    level="federal",
                    jurisdiction="USA",
                    statute=law.get("statute"),
                    title=key,
                    requirement=law.get("requirement"),
                    deadline=law.get("deadline"),
                    penalty=law.get("penalty"),
                    category=law.get("category"),
                    protective_level=law.get("protective_level", 5)
                ))

        # State laws
        for key, law in self.laws.get(state, {}).items():
            if law.get("category") == issue_category or issue_category in ["all", law.get("category")]:
                applicable.append(LegalAuthority(
                    level="state",
                    jurisdiction=state.title(),
                    statute=law.get("statute"),
                    title=key,
                    requirement=law.get("requirement"),
                    deadline=law.get("deadline"),
                    penalty=law.get("penalty"),
                    category=law.get("category"),
                    protective_level=law.get("protective_level", 4)
                ))

        # County laws
        county_key = county.lower().replace(" ", "_")
        for key, law in self.laws.get(county_key, {}).items():
            if law.get("category") == issue_category:
                applicable.append(LegalAuthority(
                    level="county",
                    jurisdiction=county,
                    statute=law.get("statute"),
                    title=key,
                    requirement=law.get("requirement"),
                    deadline=law.get("deadline"),
                    penalty=law.get("penalty"),
                    category=law.get("category"),
                    protective_level=law.get("protective_level", 3)
                ))

        # City laws
        city_key = city.lower().replace(" ", "_")
        for key, law in self.laws.get(city_key, {}).items():
            if law.get("category") == issue_category:
                applicable.append(LegalAuthority(
                    level="city",
                    jurisdiction=city,
                    statute=law.get("statute"),
                    title=key,
                    requirement=law.get("requirement"),
                    deadline=law.get("deadline"),
                    penalty=law.get("penalty"),
                    category=law.get("category"),
                    protective_level=law.get("protective_level", 2)
                ))

        # Sort by protective level (highest first), then by hierarchy
        applicable.sort(key=lambda x: (x.protective_level, self.HIERARCHY[x.level]), reverse=True)

        return applicable

    def resolve_conflict(
        self,
        laws: List[LegalAuthority]
    ) -> Tuple[LegalAuthority, str]:
        """
        When multiple laws apply, determine which takes precedence.
        Returns: (winning_law, explanation)
        """
        if not laws:
            return None, "No applicable laws found"

        if len(laws) == 1:
            return laws[0], f"Only {laws[0].statute} applies"

        # Most protective law wins
        winner = laws[0]

        explanation = f"Multiple laws apply:\n"
        for law in laws:
            explanation += f"  - {law.level.upper()}: {law.statute} ({law.requirement})\n"

        explanation += f"\n✅ APPLICABLE: {winner.statute}\n"
        explanation += f"   Reason: Most protective standard (level {winner.protective_level})\n"

        if winner.level == "city":
            explanation += "   Local ordinance is stricter than state law (allowed)\n"
        elif winner.level == "state":
            explanation += "   State law applies (no stricter local ordinance)\n"

        return winner, explanation

    def get_procedural_requirements(
        self,
        issue_type: str,
        location: Dict[str, str]
    ) -> Dict:
        """
        Get step-by-step procedural requirements for an issue.
        Returns complete compliance path.
        """
        city = location.get("city", "")
        county = location.get("county", "")
        state = location.get("state", "california")

        # Determine category
        category_map = {
            "mold": "health_hazard",
            "no_heat": "health_hazard",
            "no_water": "health_hazard",
            "lead_paint": "health_hazard",
            "leaky_faucet": "general_repair",
            "broken_window": "general_repair",
            "rent_increase": "payment",
            "security_deposit": "payment",
            "complaint": "notice"
        }

        category = category_map.get(issue_type, "general")

        # Get applicable laws
        laws = self.determine_applicable_laws(category, city, county, state)
        winner, explanation = self.resolve_conflict(laws)

        if not winner:
            return {
                "error": "No applicable laws found",
                "category": category
            }

        return {
            "issue_type": issue_type,
            "category": category,
            "location": location,
            "applicable_law": {
                "statute": winner.statute,
                "jurisdiction": f"{winner.jurisdiction} ({winner.level})",
                "requirement": winner.requirement,
                "deadline": winner.deadline,
                "penalty": winner.penalty
            },
            "conflict_resolution": explanation,
            "all_laws": [
                {
                    "level": law.level,
                    "statute": law.statute,
                    "requirement": law.requirement,
                    "deadline": law.deadline
                }
                for law in laws
            ],
            "procedural_steps": self._generate_steps(winner, category)
        }

    def _generate_steps(
        self,
        law: LegalAuthority,
        category: str
    ) -> List[Dict]:
        """Generate procedural steps based on applicable law."""
        steps = []

        # Step 1: Always document
        steps.append({
            "step": 1,
            "action": "Document the issue",
            "required": "Photos, dates, detailed description",
            "legal_basis": law.statute,
            "deadline": "Immediately",
            "validation": "Minimum 10 photos with timestamps"
        })

        # Step 2: Notice requirement
        if category in ["health_hazard", "general_repair"]:
            steps.append({
                "step": 2,
                "action": "Send written notice to landlord",
                "required": "Certified mail with return receipt OR hand delivery with witness",
                "legal_basis": "Civil Code §1942.4",
                "deadline": "Before any rent action or complaint",
                "validation": "Keep tracking number and copy of notice"
            })

        # Step 3: Wait period
        if law.deadline:
            steps.append({
                "step": 3,
                "action": f"Wait for landlord response",
                "required": f"Landlord has {law.deadline} to respond/repair",
                "legal_basis": law.statute,
                "deadline": law.deadline,
                "validation": "Document all communication during wait"
            })

        # Step 4: File complaint if ignored
        if category in ["health_hazard", "general_repair"]:
            steps.append({
                "step": 4,
                "action": "File complaint with authority",
                "required": "Health Department OR Rent Board",
                "legal_basis": law.statute,
                "deadline": f"After {law.deadline} if landlord doesn't respond",
                "validation": "Keep complaint filing receipt"
            })

        return steps


# Global instance
_jurisdiction_engine = None

def get_jurisdiction_engine() -> JurisdictionEngine:
    """Get global jurisdiction engine instance."""
    global _jurisdiction_engine
    if _jurisdiction_engine is None:
        _jurisdiction_engine = JurisdictionEngine()
    return _jurisdiction_engine


# Backward compatibility
def get_jurisdiction() -> JurisdictionEngine:
    """Alias for get_jurisdiction_engine."""
    return get_jurisdiction_engine()
