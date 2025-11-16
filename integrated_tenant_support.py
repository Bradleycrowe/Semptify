"""
Integration between Complaint Filing, Adaptive Intensity, and Housing Programs

This module connects the three systems to provide comprehensive tenant support:

1. User has an issue
2. Adaptive Intensity determines appropriate response level
3. Housing Programs provides assistance resources
4. Complaint Filing handles formal action if needed

INTEGRATION FLOW:

POSITIVE Intensity → Housing Programs (proactive resources) + Recognition
COLLABORATIVE Intensity → Housing Programs (assistance) + Communication templates
ASSERTIVE Intensity → Housing Programs (legal aid, emergency funds) + Selective filing
ESCALATED Intensity → Housing Programs (ALL emergency resources) + Multi-venue filing
MAXIMUM Intensity → Housing Programs (crisis resources) + All venues + Media

This ensures users get ASSISTANCE first when appropriate,
and COMPLAINTS only when necessary.
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class IntegratedTenantSupport:
    """
    Provides comprehensive tenant support by coordinating:
    - Adaptive intensity assessment
    - Housing assistance programs
    - Complaint filing strategy
    """
    
    def __init__(self):
        # Import engines (lazy import to avoid circular dependencies)
        from engines.adaptive_intensity_engine import AdaptiveIntensityEngine
        from engines.housing_programs_engine import HousingProgramsEngine
        from engines.complaint_filing_engine import ComplaintFilingEngine
        
        self.intensity_engine = AdaptiveIntensityEngine()
        self.programs_engine = HousingProgramsEngine()
        self.complaints_engine = ComplaintFilingEngine()
        
        logger.info("IntegratedTenantSupport initialized")
    
    def get_comprehensive_solution(
        self,
        issue_type: str,
        location: Dict,
        situation: Dict,
        landlord_id: Optional[str] = None,
        landlord_responsiveness: str = "unknown",
        days_since_reported: int = 0
    ) -> Dict:
        """
        Get comprehensive solution combining programs and complaints.
        
        Args:
            issue_type: "no_heat", "mold", "discrimination", etc.
            location: {"city": "...", "county": "...", "state": "...", "zip": "..."}
            situation: {
                "urgency": "emergency" | "urgent" | "soon" | "routine",
                "household_size": int,
                "annual_income": float,
                "special_needs": ["veteran", "disability"],
                "section_8": bool,
                "intensity_preference": "gentle" | "normal" | "aggressive"
            }
            landlord_id: Optional landlord identifier
            landlord_responsiveness: "excellent" | "good" | "fair" | "poor" | "hostile"
            days_since_reported: Days since issue was first reported
        
        Returns:
            {
                "intensity_level": "POSITIVE" | "COLLABORATIVE" | "ASSERTIVE" | "ESCALATED" | "MAXIMUM",
                "recommended_path": {...},
                "assistance_programs": [...],
                "complaint_strategy": {...} or None,
                "first_steps": [...],
                "timeline": {...}
            }
        """
        logger.info(f"Getting comprehensive solution for {issue_type} in {location.get('city', 'unknown')}")
        
        # Map issue urgency to severity
        urgency = situation.get("urgency", "routine")
        severity_map = {
            "routine": "minor",
            "soon": "minor",
            "urgent": "moderate",
            "emergency": "critical"
        }
        
        # Special severity overrides for serious issues
        if issue_type in ["no_heat", "no_water", "no_electricity"]:
            if urgency in ["urgent", "emergency"]:
                severity = "critical"
            else:
                severity = "serious"
        elif issue_type in ["mold", "bed_bugs", "structural_unsafe"]:
            severity = "serious"
        elif issue_type in ["discrimination", "retaliation", "illegal_eviction"]:
            severity = "serious"
        else:
            severity = severity_map.get(urgency, "moderate")
        
        # Determine intensity level
        intensity_guidance = self.intensity_engine.determine_intensity(
            issue_severity=severity,
            landlord_responsiveness=landlord_responsiveness if landlord_responsiveness != "unknown" else "fair",
            landlord_id=landlord_id,
            days_since_reported=days_since_reported,
            user_preference=situation.get("intensity_preference")
        )
        
        intensity_level = intensity_guidance["intensity_level"]
        
        # Get housing programs recommendations (intensity-based)
        programs_recommendations = self.programs_engine.get_intensity_based_recommendations(
            intensity_level=intensity_level,
            situation={
                "issue": issue_type,
                "days": days_since_reported,
                "location": location
            }
        )
        
        # Search for specific programs
        categories = self._determine_needed_program_categories(issue_type, intensity_level)
        
        assistance_programs = self.programs_engine.discover_programs(
            location=location,
            categories=categories,
            urgency=urgency,
            household_size=situation.get("household_size"),
            annual_income=situation.get("annual_income"),
            special_needs=situation.get("special_needs"),
            for_landlord=False
        )
        
        # Build comprehensive solution
        solution = {
            "intensity_level": intensity_level,
            "intensity_guidance": intensity_guidance,
            "recommended_path": self._build_recommended_path(
                intensity_level,
                issue_type,
                programs_recommendations,
                assistance_programs
            ),
            "assistance_programs": assistance_programs,
            "complaint_strategy": None,
            "first_steps": [],
            "timeline": {}
        }
        
        # POSITIVE: No complaints, just recognition and resources
        if intensity_level == "POSITIVE":
            solution["recommended_path"]["message"] = "Everything is going well! Here are resources to keep it that way."
            solution["first_steps"] = [
                {
                    "step": 1,
                    "action": "Rate your landlord positively",
                    "why": "Good landlords deserve recognition for their investment in the community"
                },
                {
                    "step": 2,
                    "action": "Consider applying for Section 8 now (even with good situation)",
                    "why": "Waitlists are long - get on the list while everything is stable"
                },
                {
                    "step": 3,
                    "action": "Build emergency fund with help of HUD counselor",
                    "why": "Proactive planning prevents future issues"
                }
            ]
            if landlord_id:
                solution["landlord_recognition"] = self.intensity_engine.generate_landlord_recognition_certificate(landlord_id)
        
        # COLLABORATIVE: Programs first, no formal complaints yet
        elif intensity_level == "COLLABORATIVE":
            solution["recommended_path"]["message"] = "Let's try to resolve this cooperatively before formal action."
            solution["first_steps"] = [
                {
                    "step": 1,
                    "action": "Apply for assistance programs",
                    "why": "If issue is financial, assistance can resolve it without conflict",
                    "programs": programs_recommendations.get("recommended_programs", [])[:3]
                },
                {
                    "step": 2,
                    "action": "Try friendly communication with landlord",
                    "why": "Most responsive landlords will fix issues when notified",
                    "template": intensity_guidance.get("communication_template")
                },
                {
                    "step": 3,
                    "action": "Contact HUD housing counselor",
                    "why": "Get expert advice on rights and communication strategies"
                },
                {
                    "step": 4,
                    "action": "Consider mediation",
                    "why": "Neutral third party can resolve disputes without formal complaints"
                }
            ]
            solution["timeline"] = {
                "try_communication": "Days 1-7",
                "apply_for_assistance": "Days 1-7",
                "mediation_if_needed": "Days 7-14",
                "reassess": "Day 14 - If not resolved, escalate to formal complaints"
            }
        
        # ASSERTIVE: Programs + selective formal complaints
        elif intensity_level == "ASSERTIVE":
            complaint_strategy = self.complaints_engine.generate_filing_strategy(
                issue_type=issue_type,
                location=location,
                user_situation=situation,
                urgency=urgency,
                landlord_responsiveness=landlord_responsiveness,
                landlord_id=landlord_id,
                days_since_reported=days_since_reported
            )
            solution["complaint_strategy"] = complaint_strategy
            
            solution["first_steps"] = [
                {
                    "step": 1,
                    "action": "Apply for emergency assistance programs",
                    "why": "Get financial help while pursuing formal action",
                    "programs": programs_recommendations.get("recommended_programs", [])[:3]
                },
                {
                    "step": 2,
                    "action": "Contact legal aid IMMEDIATELY",
                    "why": "You need legal representation for this issue"
                },
                {
                    "step": 3,
                    "action": "File formal written notice to landlord",
                    "why": "Creates legal paper trail"
                },
                {
                    "step": 4,
                    "action": f"File with {len(complaint_strategy.get('venues', []))} enforcement agencies",
                    "why": "Formal complaints get landlord's attention",
                    "venues": [v.get("name") for v in complaint_strategy.get("venues", [])[:2]]
                }
            ]
        
        # ESCALATED: All programs + multi-venue complaints
        elif intensity_level == "ESCALATED":
            complaint_strategy = self.complaints_engine.generate_filing_strategy(
                issue_type=issue_type,
                location=location,
                user_situation=situation,
                urgency=urgency,
                landlord_responsiveness=landlord_responsiveness,
                landlord_id=landlord_id,
                days_since_reported=days_since_reported
            )
            solution["complaint_strategy"] = complaint_strategy
            
            solution["first_steps"] = [
                {
                    "step": 1,
                    "action": "Call 211 RIGHT NOW",
                    "why": "Connect to ALL emergency resources immediately",
                    "phone": "211"
                },
                {
                    "step": 2,
                    "action": "Contact legal aid emergency line",
                    "why": "You need immediate legal help"
                },
                {
                    "step": 3,
                    "action": "Apply to ALL emergency assistance programs simultaneously",
                    "why": "Get help from every available source",
                    "programs": programs_recommendations.get("recommended_programs", [])
                },
                {
                    "step": 4,
                    "action": f"File with ALL {len(complaint_strategy.get('venues', []))} enforcement agencies",
                    "why": "Multi-venue pressure forces response",
                    "venues": [v.get("name") for v in complaint_strategy.get("venues", [])]
                }
            ]
        
        # MAXIMUM: Crisis resources + all venues + media
        elif intensity_level == "MAXIMUM":
            complaint_strategy = self.complaints_engine.generate_filing_strategy(
                issue_type=issue_type,
                location=location,
                user_situation=situation,
                urgency="emergency",
                landlord_responsiveness=landlord_responsiveness,
                landlord_id=landlord_id,
                days_since_reported=days_since_reported
            )
            solution["complaint_strategy"] = complaint_strategy
            
            solution["first_steps"] = [
                {
                    "step": 1,
                    "action": "DIAL 211 IMMEDIATELY",
                    "why": "Emergency connection to crisis resources",
                    "phone": "211",
                    "priority": "CRITICAL"
                },
                {
                    "step": 2,
                    "action": "Contact legal aid EMERGENCY line",
                    "why": "Immediate legal intervention needed"
                },
                {
                    "step": 3,
                    "action": "File with EVERY enforcement agency",
                    "why": "Maximum pressure from all government sources",
                    "venues": [v.get("name") for v in complaint_strategy.get("venues", [])]
                },
                {
                    "step": 4,
                    "action": "Contact media and elected officials",
                    "why": "Public pressure forces immediate action",
                    "contacts": programs_recommendations.get("media_contacts", [])
                },
                {
                    "step": 5,
                    "action": "Document everything for potential lawsuit",
                    "why": "This may go to court - preserve all evidence"
                }
            ]
            
            solution["emergency_contacts"] = assistance_programs.get("emergency_contacts", [])
        
        return solution
    
    def _determine_needed_program_categories(
        self,
        issue_type: str,
        intensity_level: str
    ) -> List[str]:
        """Determine which program categories are needed for this issue"""
        categories = []
        
        # Issue-specific categories
        issue_category_map = {
            "cant_pay_rent": ["rent_assistance", "emergency_funds", "housing_counseling"],
            "utility_shutoff": ["utility_assistance", "emergency_funds"],
            "eviction": ["legal_aid", "emergency_funds", "homeless_prevention", "rent_assistance"],
            "discrimination": ["legal_aid", "housing_counseling"],
            "no_heat": ["utility_assistance", "legal_aid", "housing_counseling"],
            "no_water": ["emergency_funds", "legal_aid"],
            "mold": ["legal_aid", "housing_counseling"],
            "unsafe_conditions": ["legal_aid", "housing_counseling"],
            "retaliation": ["legal_aid"]
        }
        
        categories.extend(issue_category_map.get(issue_type, ["housing_counseling"]))
        
        # Intensity-based additions
        if intensity_level in ["ASSERTIVE", "ESCALATED", "MAXIMUM"]:
            if "legal_aid" not in categories:
                categories.append("legal_aid")
        
        if intensity_level in ["ESCALATED", "MAXIMUM"]:
            if "emergency_funds" not in categories:
                categories.append("emergency_funds")
            if "homeless_prevention" not in categories:
                categories.append("homeless_prevention")
        
        return categories
    
    def _build_recommended_path(
        self,
        intensity_level: str,
        issue_type: str,
        programs_recommendations: Dict,
        assistance_programs: Dict
    ) -> Dict:
        """Build recommended path based on intensity level"""
        return {
            "intensity_level": intensity_level,
            "approach": programs_recommendations.get("tone"),
            "guidance": programs_recommendations.get("guidance"),
            "recommended_actions": programs_recommendations.get("recommended_actions"),
            "programs_summary": {
                "federal": len(assistance_programs.get("federal_programs", [])),
                "state": len(assistance_programs.get("state_programs", [])),
                "county": len(assistance_programs.get("county_programs", [])),
                "city": len(assistance_programs.get("city_programs", [])),
                "nonprofit": len(assistance_programs.get("nonprofit_resources", []))
            }
        }


# Singleton instance
_integrated_support = None

def get_integrated_support() -> IntegratedTenantSupport:
    """Get singleton instance of integrated support"""
    global _integrated_support
    if _integrated_support is None:
        _integrated_support = IntegratedTenantSupport()
    return _integrated_support
