# Comprehensive Complaint Filing Engine
# Multi-venue, always up-to-date, maximum impact strategy

"""
PHILOSOPHY:
User has an issue → System identifies ALL possible filing venues
→ Provides current procedures for EACH venue
→ Tracks which venues get results
→ Learns optimal filing strategy

VENUES COVERED:
- HUD (Section 8, Fair Housing Act violations)
- ADA (Americans with Disabilities Act)
- Local code enforcement
- State housing agencies
- County health departments
- Housing courts
- Attorney General
- Consumer protection
- Licensing boards
- Media/public pressure
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class VenueType(Enum):
    """All possible complaint venues."""
    FEDERAL_HUD = "federal_hud"
    FEDERAL_ADA = "federal_ada"
    FEDERAL_FTC = "federal_ftc"
    STATE_AG = "state_attorney_general"
    STATE_HOUSING = "state_housing_agency"
    COUNTY_HEALTH = "county_health"
    COUNTY_COURT = "county_court"
    CITY_CODE = "city_code_enforcement"
    CITY_LICENSING = "city_rental_licensing"
    HOUSING_COURT = "housing_court"
    SMALL_CLAIMS = "small_claims_court"
    TENANT_UNION = "tenant_union"
    LEGAL_AID = "legal_aid"
    MEDIA = "media_exposure"


@dataclass
class FilingVenue:
    """Represents a place where complaints can be filed."""
    venue_type: VenueType
    name: str
    jurisdiction: str  # "federal", "minnesota", "dakota_county", "eagan"
    contact: Dict  # phone, email, website, address
    filing_methods: List[str]  # ["online", "mail", "phone", "in_person"]
    typical_timeline: str
    effectiveness_score: float  # 0-1 based on outcomes
    last_updated: str
    forms_required: List[Dict]
    fees: Optional[str]
    notes: str


class ComplaintFilingEngine:
    """
    Determines ALL venues where user can file complaints.
    Provides up-to-date procedures for each.
    Learns which venues get results.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.venues_file = os.path.join(data_dir, "filing_venues.json")
        self.procedures_file = os.path.join(data_dir, "filing_procedures.json")
        self.outcomes_file = os.path.join(data_dir, "filing_outcomes.json")

        self.venues = self._load_venues()
        self.procedures = self._load_procedures()
        self.outcomes = self._load_outcomes()

    def _load_venues(self) -> Dict:
        """Load filing venue database."""
        if os.path.exists(self.venues_file):
            with open(self.venues_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._initialize_default_venues()

    def _load_procedures(self) -> Dict:
        """Load filing procedures (updated automatically)."""
        if os.path.exists(self.procedures_file):
            with open(self.procedures_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_outcomes(self) -> Dict:
        """Load outcome tracking (which venues work)."""
        if os.path.exists(self.outcomes_file):
            with open(self.outcomes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_venues(self):
        """Persist venue database."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.venues_file, 'w', encoding='utf-8') as f:
            json.dump(self.venues, f, indent=2)

    def _save_procedures(self):
        """Persist procedures."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.procedures_file, 'w', encoding='utf-8') as f:
            json.dump(self.procedures, f, indent=2)

    def _save_outcomes(self):
        """Persist outcome tracking."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.outcomes_file, 'w', encoding='utf-8') as f:
            json.dump(self.outcomes, f, indent=2)

    # ========================================================================
    # INITIALIZE DEFAULT VENUES (Updated from user outcomes)
    # ========================================================================

    def _initialize_default_venues(self) -> Dict:
        """
        Initialize with known federal/state venues.
        Local venues discovered automatically per location.
        """
        return {
            # FEDERAL VENUES (Apply everywhere)
            "federal_hud_fair_housing": {
                "venue_type": "federal_hud",
                "name": "HUD Fair Housing Complaint",
                "jurisdiction": "federal",
                "contact": {
                    "phone": "800-669-9777",
                    "tty": "800-927-9275",
                    "website": "https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint",
                    "email": "via online form"
                },
                "filing_methods": ["online", "mail", "phone"],
                "typical_timeline": "100 days investigation",
                "effectiveness_score": 0.85,
                "last_updated": datetime.now().isoformat(),
                "applies_to": [
                    "discrimination_race",
                    "discrimination_disability",
                    "discrimination_familial",
                    "discrimination_national_origin",
                    "discrimination_religion",
                    "discrimination_sex",
                    "reasonable_accommodation_denied"
                ],
                "forms_required": [
                    {
                        "name": "HUD-903 Online Form",
                        "url": "https://portalapps.hud.gov/FHEO903/Form903/Form903Start.action",
                        "fillable": True
                    }
                ],
                "fees": "Free",
                "deadline": "1 year from discrimination date",
                "notes": "Federal protection - landlord cannot retaliate"
            },

            "federal_hud_section8": {
                "venue_type": "federal_hud",
                "name": "HUD Section 8 Complaint",
                "jurisdiction": "federal",
                "contact": {
                    "phone": "800-685-8470",
                    "website": "https://www.hud.gov/topics/rental_assistance/phprog",
                    "local": "Contact your local Public Housing Authority"
                },
                "filing_methods": ["phone", "mail", "in_person_at_pha"],
                "typical_timeline": "30-60 days",
                "effectiveness_score": 0.75,
                "last_updated": datetime.now().isoformat(),
                "applies_to": [
                    "section8_voucher_discrimination",
                    "section8_pha_issues",
                    "section8_payment_issues",
                    "habitability_with_section8"
                ],
                "forms_required": [
                    {
                        "name": "Grievance form from local PHA",
                        "url": "varies_by_location",
                        "contact_pha": True
                    }
                ],
                "fees": "Free",
                "notes": "Also file with local PHA simultaneously"
            },

            "federal_ada_complaint": {
                "venue_type": "federal_ada",
                "name": "ADA Complaint (Department of Justice)",
                "jurisdiction": "federal",
                "contact": {
                    "website": "https://civilrights.justice.gov/report/",
                    "phone": "855-856-1247",
                    "mail": "U.S. Department of Justice, Civil Rights Division, 950 Pennsylvania Avenue NW, Washington, DC 20530"
                },
                "filing_methods": ["online", "mail", "phone"],
                "typical_timeline": "Variable (6-12 months)",
                "effectiveness_score": 0.80,
                "last_updated": datetime.now().isoformat(),
                "applies_to": [
                    "disability_discrimination",
                    "reasonable_accommodation_denied",
                    "service_animal_denied",
                    "accessibility_issues"
                ],
                "forms_required": [
                    {
                        "name": "Online complaint form",
                        "url": "https://civilrights.justice.gov/report/",
                        "fillable": True
                    }
                ],
                "fees": "Free",
                "notes": "Can also file private lawsuit under ADA"
            },

            # STATE-LEVEL (Minnesota example - system learns others)
            "minnesota_ag_consumer": {
                "venue_type": "state_ag",
                "name": "Minnesota Attorney General Consumer Complaint",
                "jurisdiction": "minnesota",
                "contact": {
                    "phone": "651-296-3353",
                    "toll_free": "800-657-3787",
                    "website": "https://www.ag.state.mn.us/Office/Complaint.asp",
                    "online_form": "https://www.ag.state.mn.us/Office/Complaint.asp"
                },
                "filing_methods": ["online", "mail", "phone"],
                "typical_timeline": "30-90 days",
                "effectiveness_score": 0.70,
                "last_updated": datetime.now().isoformat(),
                "applies_to": [
                    "fraud",
                    "deceptive_practices",
                    "security_deposit_violations",
                    "illegal_fees"
                ],
                "forms_required": [
                    {
                        "name": "Consumer Complaint Form",
                        "url": "https://www.ag.state.mn.us/Office/Complaint.asp",
                        "fillable": True
                    }
                ],
                "fees": "Free",
                "notes": "AG may investigate or refer to other agencies"
            },

            # TEMPLATE for local venues (discovered per location)
            "local_code_enforcement_template": {
                "venue_type": "city_code",
                "name": "[City] Code Enforcement",
                "jurisdiction": "city",
                "contact": {
                    "phone": "discovered_per_city",
                    "website": "discovered_per_city"
                },
                "filing_methods": ["phone", "online", "in_person"],
                "typical_timeline": "3-14 days",
                "effectiveness_score": 0.90,  # Usually very effective
                "applies_to": [
                    "habitability",
                    "health_hazard",
                    "code_violations",
                    "mold",
                    "pest_infestation",
                    "no_heat",
                    "no_water",
                    "structural_issues"
                ],
                "fees": "Free",
                "notes": "Most effective for health/safety issues"
            }
        }

    # ========================================================================
    # IDENTIFY ALL APPLICABLE VENUES FOR ISSUE
    # ========================================================================

    def identify_venues(
        self,
        issue_type: str,
        location: Dict[str, str],
        user_situation: Dict
    ) -> List[Dict]:
        """
        Identify ALL venues where user can file complaint.
        Returns ordered by effectiveness (most effective first).

        Args:
            issue_type: "discrimination_disability", "no_heat", "illegal_eviction", etc.
            location: {city, county, state, zip}
            user_situation: {has_section8, has_disability, issue_details}

        Returns:
            List of applicable venues with current procedures
        """
        applicable_venues = []

        # Check each venue in database
        for venue_key, venue_data in self.venues.items():
            if self._venue_applies(venue_data, issue_type, location, user_situation):
                # Get most current procedures
                procedures = self._get_current_procedures(venue_key, location)

                # Get effectiveness score from outcomes
                effectiveness = self._get_effectiveness_score(venue_key, location, issue_type)

                applicable_venues.append({
                    "venue_key": venue_key,
                    "venue_data": venue_data,
                    "procedures": procedures,
                    "effectiveness": effectiveness,
                    "confidence": procedures.get("confidence", 0.5)
                })

        # Discover local venues if not yet in database
        local_venues = self._discover_local_venues(location, issue_type)
        applicable_venues.extend(local_venues)

        # Sort by effectiveness (best first)
        applicable_venues.sort(key=lambda x: x["effectiveness"], reverse=True)

        return applicable_venues

    def _venue_applies(
        self,
        venue_data: Dict,
        issue_type: str,
        location: Dict,
        user_situation: Dict
    ) -> bool:
        """Check if venue applies to this issue."""
        # Check issue type match
        if "applies_to" in venue_data:
            if issue_type not in venue_data["applies_to"]:
                return False

        # Check jurisdiction match
        jurisdiction = venue_data.get("jurisdiction")
        if jurisdiction == "federal":
            return True  # Federal applies everywhere
        elif jurisdiction == "state":
            return venue_data.get("state") == location.get("state")
        elif jurisdiction in ["county", "city"]:
            return venue_data.get("location_key") == f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"

        return True

    def _get_current_procedures(
        self,
        venue_key: str,
        location: Dict
    ) -> Dict:
        """
        Get most up-to-date filing procedures for venue.
        Learns from user outcomes and updates automatically.
        """
        location_key = f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"
        proc_key = f"{venue_key}:{location_key}"

        if proc_key in self.procedures:
            procedures = self.procedures[proc_key]

            # Check if procedures are recent (< 90 days old)
            last_updated = datetime.fromisoformat(procedures.get("last_updated", "2020-01-01T00:00:00"))
            age_days = (datetime.now() - last_updated).days

            if age_days < 90:
                return procedures
            else:
                # Procedures may be outdated - flag for verification
                procedures["needs_verification"] = True
                procedures["last_verified"] = f"{age_days} days ago"
                return procedures

        # No procedures yet - use template or discover
        return {
            "status": "discovering",
            "last_updated": None,
            "confidence": 0.3,
            "needs_user_validation": True
        }

    def _get_effectiveness_score(
        self,
        venue_key: str,
        location: Dict,
        issue_type: str
    ) -> float:
        """
        Get effectiveness score based on actual outcomes.
        Returns 0-1 score (higher = more effective).
        """
        location_key = f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"
        outcome_key = f"{venue_key}:{location_key}:{issue_type}"

        if outcome_key not in self.outcomes:
            # No outcome data - use default from venue config
            return self.venues.get(venue_key, {}).get("effectiveness_score", 0.5)

        outcome_data = self.outcomes[outcome_key]
        success_count = outcome_data.get("success_count", 0)
        total_count = outcome_data.get("total_count", 0)

        if total_count == 0:
            return 0.5

        return success_count / total_count

    def _discover_local_venues(
        self,
        location: Dict,
        issue_type: str
    ) -> List[Dict]:
        """
        Discover local venues (city code enforcement, county health, etc.)
        that aren't yet in database.
        """
        from location_intelligence import get_location_intelligence

        location_intel = get_location_intelligence()
        location_key = f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"

        # Get discovered resources for this location
        if location_key not in location_intel.locations:
            location_data = location_intel.discover_resources(location)
        else:
            location_data = location_intel.locations[location_key]

        discovered_venues = []

        # City code enforcement (very effective for habitability)
        if issue_type in ["habitability", "no_heat", "no_water", "mold", "pest_infestation"]:
            for agency in location_data.get("resources", {}).get("government_agencies", []):
                if "code" in agency.get("name", "").lower() or "enforcement" in agency.get("name", "").lower():
                    discovered_venues.append({
                        "venue_key": f"city_code_{location_key}",
                        "venue_data": {
                            "venue_type": "city_code",
                            "name": agency.get("name"),
                            "contact": {
                                "phone": agency.get("phone"),
                                "website": agency.get("website")
                            },
                            "effectiveness_score": 0.90  # Usually very effective
                        },
                        "procedures": {
                            "status": "call_to_file",
                            "confidence": 0.7
                        },
                        "effectiveness": 0.90
                    })

        return discovered_venues

    # ========================================================================
    # GENERATE FILING STRATEGY (Multi-venue approach)
    # ========================================================================

    def generate_filing_strategy(
        self,
        issue_type: str,
        location: Dict,
        user_situation: Dict,
        urgency: str = "normal",  # "emergency", "urgent", "normal"
        landlord_responsiveness: str = "unknown",  # "excellent", "good", "fair", "poor", "hostile", "unknown"
        landlord_id: Optional[str] = None,
        days_since_reported: int = 0
    ) -> Dict:
        """
        Generate comprehensive filing strategy with ADAPTIVE INTENSITY.
        Not all situations require full legal pressure!

        Good landlords get positive recognition.
        Bad landlords get escalating pressure.

        Returns strategy with:
        - Intensity level (positive, collaborative, assertive, escalated, maximum)
        - Primary venue (most effective)
        - Secondary venues (file simultaneously IF NEEDED)
        - Escalation path (if primary doesn't work)
        - Timeline for each step
        """
        # ADAPTIVE INTENSITY - Scale response to situation
        from engines.adaptive_intensity_engine import get_adaptive_intensity_engine

        intensity_engine = get_adaptive_intensity_engine()

        # Map urgency to severity
        severity_map = {
            "normal": "minor",
            "urgent": "moderate",
            "emergency": "critical"
        }
        issue_severity = severity_map.get(urgency, "moderate")

        # Determine appropriate intensity level
        intensity_guidance = intensity_engine.determine_intensity(
            issue_severity=issue_severity,
            landlord_responsiveness=landlord_responsiveness if landlord_responsiveness != "unknown" else "fair",
            landlord_id=landlord_id,
            days_since_reported=days_since_reported,
            user_preference=user_situation.get("intensity_preference")  # "gentle", "normal", "aggressive"
        )

        intensity_level = intensity_guidance["intensity_level"]

        # POSITIVE INTENSITY - No formal filing needed!
        if intensity_level == "positive":
            return {
                "intensity_level": "positive",
                "message": intensity_guidance["message"],
                "recommended_actions": intensity_guidance["recommended_actions"],
                "tone": "positive",
                "no_filing_needed": True,
                "landlord_recognition": intensity_engine.generate_landlord_recognition_certificate(landlord_id) if landlord_id else None
            }

        # COLLABORATIVE INTENSITY - Friendly communication first
        if intensity_level == "collaborative":
            return {
                "intensity_level": "collaborative",
                "message": intensity_guidance["message"],
                "recommended_actions": intensity_guidance["recommended_actions"],
                "avoid_actions": intensity_guidance["avoid_actions"],
                "tone": "helpful",
                "communication_template": intensity_guidance.get("communication_template"),
                "formal_filing": "not_recommended_yet",
                "suggestion": "Try friendly communication first. Most responsive landlords will fix minor issues when notified."
            }

        # Get all applicable venues
        venues = self.identify_venues(issue_type, location, user_situation)

        # Get all applicable venues
        venues = self.identify_venues(issue_type, location, user_situation)

        if not venues:
            return {
                "error": "No applicable filing venues found",
                "suggestion": "Contact legal aid for guidance"
            }

        # Categorize by effectiveness and jurisdiction
        federal_venues = [v for v in venues if v["venue_data"].get("jurisdiction") == "federal"]
        local_venues = [v for v in venues if v["venue_data"].get("jurisdiction") in ["city", "county"]]
        state_venues = [v for v in venues if v["venue_data"].get("jurisdiction") == "state"]

        strategy = {
            "issue_type": issue_type,
            "urgency": urgency,
            "intensity_level": intensity_level,
            "intensity_guidance": intensity_guidance,
            "recommended_approach": self._get_approach_for_intensity(intensity_level),
            "strategy_overview": self._get_strategy_overview(intensity_level, urgency, len(venues)),

            "immediate_actions": [],
            "simultaneous_filings": [],
            "escalation_path": [],

            "timeline": self._generate_timeline(urgency, venues),
            "success_probability": self._calculate_success_probability(venues),
            "verified_by": f"{sum(v.get('confidence', 0) > 0.75 for v in venues)} verified procedures"
        }

        # ASSERTIVE INTENSITY - Formal documentation, selective filing
        if intensity_level == "assertive":
            if local_venues:
                strategy["immediate_actions"].append({
                    "priority": 1,
                    "action": "File with local code enforcement (most effective)",
                    "venue": local_venues[0],
                    "why": "Fastest response, highest success rate",
                    "timeline": local_venues[0]["venue_data"].get("typical_timeline", "3-14 days")
                })
            # Only 1-2 venues at this level (not overwhelming landlord yet)
            if federal_venues and urgency != "normal":
                strategy["simultaneous_filings"].append({
                    "priority": 2,
                    "action": f"File with {federal_venues[0]['venue_data']['name']}",
                    "venue": federal_venues[0],
                    "why": "Federal protection if needed",
                    "timeline": federal_venues[0]["venue_data"].get("typical_timeline")
                })

        # ESCALATED INTENSITY - Multi-venue filing
        elif intensity_level == "escalated":
            # IMMEDIATE ACTION (Most effective venue)
            if local_venues:
                strategy["immediate_actions"].append({
                    "priority": 1,
                    "action": "File with local code enforcement",
                    "venue": local_venues[0],
                    "why": "Fastest response, highest success rate for health/safety issues",
                    "timeline": local_venues[0]["venue_data"].get("typical_timeline", "3-14 days")
                })

            # SIMULTANEOUS FILINGS (Multiple venues at once)
            if federal_venues:
                for fed_venue in federal_venues[:2]:  # Top 2 federal venues
                    strategy["simultaneous_filings"].append({
                        "priority": 2,
                        "action": f"File with {fed_venue['venue_data']['name']}",
                        "venue": fed_venue,
                        "why": "Federal protection, cannot be retaliated against",
                        "timeline": fed_venue["venue_data"].get("typical_timeline")
                    })

            if state_venues:
                strategy["simultaneous_filings"].append({
                    "priority": 2,
                    "action": f"File with {state_venues[0]['venue_data']['name']}",
                    "venue": state_venues[0],
                    "why": "State-level enforcement authority",
                    "timeline": state_venues[0]["venue_data"].get("typical_timeline")
                })

        # MAXIMUM INTENSITY - All venues + media
        elif intensity_level == "maximum":
            # File with EVERYTHING
            if local_venues:
                for local in local_venues:
                    strategy["immediate_actions"].append({
                        "priority": 1,
                        "action": f"File with {local['venue_data']['name']}",
                        "venue": local,
                        "why": "EMERGENCY - file everywhere immediately",
                        "timeline": "URGENT"
                    })

            if federal_venues:
                for fed in federal_venues:
                    strategy["simultaneous_filings"].append({
                        "priority": 1,
                        "action": f"File with {fed['venue_data']['name']}",
                        "venue": fed,
                        "why": "Federal protection + enforcement",
                        "timeline": fed["venue_data"].get("typical_timeline")
                    })

            if state_venues:
                for state in state_venues:
                    strategy["simultaneous_filings"].append({
                        "priority": 1,
                        "action": f"File with {state['venue_data']['name']}",
                        "venue": state,
                        "why": "State enforcement",
                        "timeline": state["venue_data"].get("typical_timeline")
                    })

            # Add media/public pressure option
            strategy["simultaneous_filings"].append({
                "priority": 2,
                "action": "Consider media/public pressure",
                "why": "Public accountability for serious violations",
                "note": "Contact local news, post on social media (with documentation)"
            })

        # ESCALATION PATH (If first attempts fail)
        strategy["escalation_path"] = self._generate_escalation_path(intensity_level)

        return strategy

    def _get_approach_for_intensity(self, intensity_level: str) -> str:
        """Get filing approach based on intensity."""
        if intensity_level == "assertive":
            return "selective_filing"
        elif intensity_level == "escalated":
            return "multi_venue_filing"
        elif intensity_level == "maximum":
            return "all_venues_plus_media"
        return "collaborative"

    def _get_strategy_overview(self, intensity_level: str, urgency: str, venue_count: int) -> str:
        """Get strategy summary based on intensity."""
        if intensity_level == "assertive":
            return f"FORMAL DOCUMENTATION: File with 1-2 most effective venues. Issue persists after initial communication."
        elif intensity_level == "escalated":
            return f"MULTI-VENUE FILING: File with {min(venue_count, 5)} venues simultaneously. Serious issues or unresponsive landlord."
        elif intensity_level == "maximum":
            return f"MAXIMUM PRESSURE: File with ALL {venue_count} venues immediately. Critical safety issues or hostile landlord."
        return f"File with {venue_count} venues as appropriate."

    def _generate_escalation_path(self, intensity_level: str) -> List[Dict]:
        """Generate escalation path based on intensity."""
        if intensity_level == "assertive":
            return [
                {
                    "step": 1,
                    "trigger": "No response within 7 days",
                    "action": "Follow up in writing with deadline",
                    "method": "Email + certified mail"
                },
                {
                    "step": 2,
                    "trigger": "No action within 14 days",
                    "action": "File with code enforcement or health department",
                    "why": "Formal agency involvement"
                },
                {
                    "step": 3,
                    "trigger": "No action within 30 days",
                    "action": "Consider legal aid or housing court",
                    "why": "Force legal resolution"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "trigger": "No response within 14 days",
                    "action": "Follow up with all filed venues",
                    "method": "Phone call + email with case numbers"
                },
                {
                    "step": 2,
                    "trigger": "No action within 30 days",
                    "action": "File in housing court or small claims",
                    "why": "Force legal resolution"
                },
                {
                    "step": 3,
                    "trigger": "Court ruling in your favor but landlord doesn't comply",
                    "action": "Request enforcement/garnishment",
                    "why": "Court can force compliance"
                }
            ]

    def _get_strategy_overview_old(self, urgency: str, venue_count: int) -> str:
        """Get strategy summary."""
        if urgency == "emergency":
            return f"EMERGENCY: File with all {venue_count} venues TODAY. Call for immediate inspection."
        elif urgency == "urgent":
            return f"File with {venue_count} venues this week. Multiple filings increase pressure."
        else:
            return f"File with {venue_count} venues. Multi-venue approach proven most effective."

    def _generate_timeline(self, urgency: str, venues: List[Dict]) -> Dict:
        """Generate expected timeline."""
        if urgency == "emergency":
            return {
                "day_1": "File all complaints, call for emergency inspection",
                "day_2": "Follow up with local authorities",
                "day_7": "Expect first response/inspection",
                "day_14": "Issue should be resolved or in enforcement"
            }
        else:
            return {
                "week_1": "File with all recommended venues",
                "week_2": "Expect initial responses",
                "week_4": "Follow up if no action",
                "week_6": "Escalate if needed"
            }

    def _calculate_success_probability(self, venues: List[Dict]) -> str:
        """Calculate overall success probability."""
        if not venues:
            return "Unknown"

        # Average effectiveness of top 3 venues
        top_venues = venues[:3]
        avg_effectiveness = sum(v["effectiveness"] for v in top_venues) / len(top_venues)

        if avg_effectiveness >= 0.85:
            return "Very High (85%+)"
        elif avg_effectiveness >= 0.70:
            return "High (70-85%)"
        elif avg_effectiveness >= 0.50:
            return "Moderate (50-70%)"
        else:
            return "Variable (needs more data)"

    # ========================================================================
    # TRACK OUTCOMES (Learn what works)
    # ========================================================================

    def track_filing_outcome(
        self,
        venue_key: str,
        location: Dict,
        issue_type: str,
        outcome: Dict
    ):
        """
        Track outcome of filing to learn effectiveness.

        Args:
            venue_key: Which venue was used
            location: Where
            issue_type: What issue
            outcome: {success: bool, timeline: str, resolution: str, notes: str}
        """
        location_key = f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"
        outcome_key = f"{venue_key}:{location_key}:{issue_type}"

        if outcome_key not in self.outcomes:
            self.outcomes[outcome_key] = {
                "success_count": 0,
                "total_count": 0,
                "outcomes": []
            }

        outcome_data = self.outcomes[outcome_key]

        if outcome.get("success"):
            outcome_data["success_count"] += 1

        outcome_data["total_count"] += 1
        outcome_data["outcomes"].append({
            "timestamp": datetime.now().isoformat(),
            "success": outcome.get("success"),
            "timeline": outcome.get("timeline"),
            "resolution": outcome.get("resolution"),
            "notes": outcome.get("notes", "")
        })

        # Calculate new effectiveness score
        outcome_data["effectiveness"] = outcome_data["success_count"] / outcome_data["total_count"]

        self._save_outcomes()

    def update_procedures_from_outcome(
        self,
        venue_key: str,
        location: Dict,
        updated_procedure: Dict
    ):
        """
        Update filing procedures based on user experience.
        Keeps procedures current and accurate.
        """
        location_key = f"{location.get('city')}_{location.get('state')}_{location.get('zip')}"
        proc_key = f"{venue_key}:{location_key}"

        self.procedures[proc_key] = {
            **updated_procedure,
            "last_updated": datetime.now().isoformat(),
            "verified_by": "user_outcome",
            "confidence": 0.8
        }

        self._save_procedures()


# Global instance
_filing_engine = None

def get_filing_engine() -> ComplaintFilingEngine:
    """Get global filing engine instance."""
    global _filing_engine
    if _filing_engine is None:
        _filing_engine = ComplaintFilingEngine()
    return _filing_engine
