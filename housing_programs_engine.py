"""
Housing Programs & Resources Discovery Engine

Discovers ALL available housing assistance programs and resources for any area:
- Federal programs (HUD, Section 8, LIHEAP, ERAP, Veterans, etc.)
- State programs (rental assistance, weatherization, legal aid)
- County programs (emergency funds, utility help, food assistance)
- City programs (local rent assistance, mediation services)
- Charity/nonprofit (Salvation Army, Catholic Charities, local food banks)

Provides complete details:
- Application procedures and deadlines
- Contact information (phone, email, address, website)
- Eligibility requirements (income limits, household size, etc.)
- Required documents
- Processing times
- Executive branch hierarchy (who to escalate to)

Integrates with adaptive intensity system:
- COLLABORATIVE: Recommend assistance before formal complaints
- ASSERTIVE: Include legal aid and advocacy resources
- ESCALATED: Fast-track emergency assistance contacts
- MAXIMUM: All resources + media contacts for public pressure

Used site-wide:
- Rent payment help
- Utility shutoff prevention
- Emergency housing/eviction prevention
- Complaint filing support
- Legal representation
- Landlord programs (rehab loans, tax credits)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProgramCategory(Enum):
    """Categories of housing assistance programs"""
    RENT_ASSISTANCE = "rent_assistance"
    UTILITY_ASSISTANCE = "utility_assistance"
    EMERGENCY_FUNDS = "emergency_funds"
    LEGAL_AID = "legal_aid"
    HOUSING_COUNSELING = "housing_counseling"
    WEATHERIZATION = "weatherization"
    DISABILITY_ACCESSIBILITY = "disability_accessibility"
    VETERAN_SERVICES = "veteran_services"
    SENIOR_SERVICES = "senior_services"
    HOMELESS_PREVENTION = "homeless_prevention"
    FOOD_ASSISTANCE = "food_assistance"
    HEALTHCARE = "healthcare"
    LANDLORD_REHAB = "landlord_rehab"
    LANDLORD_TAX_CREDITS = "landlord_tax_credits"
    MEDIATION = "mediation"


class ProgramLevel(Enum):
    """Government level of program"""
    FEDERAL = "federal"
    STATE = "state"
    COUNTY = "county"
    CITY = "city"
    NONPROFIT = "nonprofit"


class UrgencyLevel(Enum):
    """How quickly assistance is needed"""
    ROUTINE = "routine"  # General assistance, no deadline
    SOON = "soon"  # Within 30 days
    URGENT = "urgent"  # Within 7 days
    EMERGENCY = "emergency"  # Within 24-48 hours (eviction, shutoff)


class HousingProgramsEngine:
    """
    Engine to discover and recommend housing programs and resources.
    
    Discovers all available programs for a location, filters by need,
    provides complete application details, and integrates with intensity system.
    """
    
    def __init__(self, data_dir: str = "housing_programs_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Data files
        self.programs_file = os.path.join(data_dir, "programs.json")
        self.applications_file = os.path.join(data_dir, "applications.json")
        self.contacts_file = os.path.join(data_dir, "contacts.json")
        self.outcomes_file = os.path.join(data_dir, "outcomes.json")
        
        # Load data
        self.programs = self._load_programs()
        self.applications = self._load_applications()
        self.contacts = self._load_contacts()
        self.outcomes = self._load_outcomes()
        
        # Save initial database if just created
        if not os.path.exists(self.programs_file):
            self._save_programs()
        
        logger.info("HousingProgramsEngine initialized")
    
    def _load_programs(self) -> Dict:
        """Load program database"""
        if os.path.exists(self.programs_file):
            with open(self.programs_file, 'r') as f:
                return json.load(f)
        return self._initialize_programs_database()
    
    def _load_applications(self) -> Dict:
        """Load application tracking"""
        if os.path.exists(self.applications_file):
            with open(self.applications_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_contacts(self) -> Dict:
        """Load contact information"""
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_outcomes(self) -> Dict:
        """Load program effectiveness data"""
        if os.path.exists(self.outcomes_file):
            with open(self.outcomes_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_programs(self):
        """Save program database"""
        with open(self.programs_file, 'w') as f:
            json.dump(self.programs, f, indent=2)
    
    def _save_applications(self):
        """Save application tracking"""
        with open(self.applications_file, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def _save_contacts(self):
        """Save contact information"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def _save_outcomes(self):
        """Save outcomes data"""
        with open(self.outcomes_file, 'w') as f:
            json.dump(self.outcomes, f, indent=2)
    
    def _initialize_programs_database(self) -> Dict:
        """
        Initialize with comprehensive federal and state programs.
        
        This is the foundation - local programs will be discovered dynamically.
        """
        programs = {
            "federal": {
                "HUD_Section8": {
                    "name": "Section 8 Housing Choice Voucher",
                    "level": "federal",
                    "category": "rent_assistance",
                    "description": "Monthly rental assistance for low-income families, elderly, and disabled",
                    "eligibility": {
                        "income_limit": "50% of area median income",
                        "household_requirements": "All household members",
                        "citizenship": "US citizen or eligible immigrant",
                        "other": "Background check, landlord participation required"
                    },
                    "benefits": "Pays portion of rent directly to landlord",
                    "application_process": "Apply through local Public Housing Authority (PHA)",
                    "processing_time": "Variable - often 2+ year waitlist",
                    "required_docs": [
                        "Photo ID for all adults",
                        "Social Security cards for all members",
                        "Birth certificates for children",
                        "Proof of income (pay stubs, tax returns, benefits letters)",
                        "Proof of citizenship/immigration status",
                        "Landlord contact information"
                    ],
                    "contact": {
                        "website": "https://www.hud.gov/topics/housing_choice_voucher_program_section_8",
                        "phone": "1-800-955-2232 (HUD)",
                        "local_lookup": "Contact your local PHA - find at hud.gov/program_offices/public_indian_housing/pha/contacts"
                    },
                    "executive_escalation": [
                        "Local PHA Director",
                        "Regional HUD Office",
                        "HUD Secretary (cabinet level)"
                    ],
                    "for_landlords": {
                        "benefits": "Guaranteed rent payment, inspection standards",
                        "requirements": "Pass HUD inspection, accept voucher payment",
                        "contact": "Local PHA for landlord enrollment"
                    }
                },
                "HUD_PublicHousing": {
                    "name": "Public Housing",
                    "level": "federal",
                    "category": "rent_assistance",
                    "description": "HUD-owned affordable housing units",
                    "eligibility": {
                        "income_limit": "50% of area median income (very low income) or 80% (low income)",
                        "household_requirements": "All household members",
                        "citizenship": "US citizen or eligible immigrant"
                    },
                    "benefits": "Rent typically 30% of adjusted gross income",
                    "application_process": "Apply through local PHA",
                    "processing_time": "Variable - often long waitlists",
                    "contact": {
                        "website": "https://www.hud.gov/topics/rental_assistance/phprog",
                        "phone": "1-800-955-2232"
                    }
                },
                "LIHEAP": {
                    "name": "Low Income Home Energy Assistance Program",
                    "level": "federal",
                    "category": "utility_assistance",
                    "description": "Help with heating/cooling bills and energy crises",
                    "eligibility": {
                        "income_limit": "Varies by state - typically 150% of poverty line",
                        "crisis_assistance": "Shutoff notice, out of fuel, extreme weather"
                    },
                    "benefits": "One-time or seasonal payment to utility company",
                    "application_process": "Apply through state LIHEAP office",
                    "processing_time": "Emergency: 18-48 hours, Regular: 2-4 weeks",
                    "required_docs": [
                        "Photo ID",
                        "Social Security cards",
                        "Proof of income",
                        "Utility bills or shutoff notice",
                        "Proof of residence"
                    ],
                    "contact": {
                        "website": "https://www.acf.hhs.gov/ocs/liheap",
                        "phone": "Contact your state LIHEAP office",
                        "local_lookup": "Find at acf.hhs.gov/ocs/liheap-state-and-territory-contact-listing"
                    },
                    "executive_escalation": [
                        "Local LIHEAP administrator",
                        "State LIHEAP director",
                        "ACF Regional Office",
                        "ACF Director (federal)"
                    ]
                },
                "ERAP": {
                    "name": "Emergency Rental Assistance Program",
                    "level": "federal",
                    "category": "emergency_funds",
                    "description": "COVID-era program for rent/utility arrears (check if still available)",
                    "eligibility": {
                        "income_limit": "80% of area median income",
                        "hardship": "Financial hardship due to COVID-19",
                        "risk": "At risk of homelessness or housing instability"
                    },
                    "benefits": "Up to 18 months of rent/utility assistance",
                    "application_process": "Apply through local ERAP administrator",
                    "status": "Check local availability - funding may be exhausted",
                    "contact": {
                        "website": "https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program",
                        "local_lookup": "Search '[Your City/County] ERAP' to find local program"
                    }
                },
                "VA_Housing": {
                    "name": "VA Housing Assistance",
                    "level": "federal",
                    "category": "veteran_services",
                    "description": "Housing support for veterans and their families",
                    "eligibility": {
                        "veteran_status": "Veteran, active duty, or eligible family member",
                        "discharge": "Honorable discharge (for most programs)"
                    },
                    "programs": [
                        "VA Home Loans",
                        "VA Supportive Housing (HUD-VASH)",
                        "Homeless veteran programs",
                        "Adaptive housing grants (disabled veterans)"
                    ],
                    "contact": {
                        "website": "https://www.va.gov/housing-assistance/",
                        "phone": "1-877-827-3702",
                        "local": "Contact your local VA Medical Center"
                    }
                },
                "USDA_Rural": {
                    "name": "USDA Rural Housing Programs",
                    "level": "federal",
                    "category": "rent_assistance",
                    "description": "Housing assistance for rural areas",
                    "eligibility": {
                        "location": "Must be in USDA-defined rural area",
                        "income_limit": "Varies by program and area"
                    },
                    "programs": [
                        "Section 502 Direct Loan (homeownership)",
                        "Section 504 Home Repair Loans/Grants",
                        "Multi-Family Housing rental assistance"
                    ],
                    "contact": {
                        "website": "https://www.rd.usda.gov/programs-services/single-family-housing-programs",
                        "phone": "1-800-670-6553"
                    }
                },
                "SSI_Housing": {
                    "name": "SSI Housing Benefits",
                    "level": "federal",
                    "category": "rent_assistance",
                    "description": "Supplemental Security Income includes housing allowance",
                    "eligibility": {
                        "disability": "Disabled, blind, or age 65+",
                        "income_limit": "Very low income and resources"
                    },
                    "benefits": "Monthly cash benefit can be used for housing",
                    "contact": {
                        "website": "https://www.ssa.gov/ssi/",
                        "phone": "1-800-772-1213"
                    }
                },
                "Legal_Aid": {
                    "name": "Legal Services Corporation (LSC) Funded Legal Aid",
                    "level": "federal",
                    "category": "legal_aid",
                    "description": "Free legal help for low-income individuals",
                    "eligibility": {
                        "income_limit": "125% of poverty line (typically)",
                        "case_types": "Housing, eviction defense, discrimination, etc."
                    },
                    "services": [
                        "Eviction defense",
                        "Housing discrimination cases",
                        "Landlord-tenant disputes",
                        "Unsafe housing conditions",
                        "Fair housing violations"
                    ],
                    "contact": {
                        "website": "https://www.lsc.gov/what-legal-aid/find-legal-aid",
                        "phone": "Contact your local legal aid office"
                    }
                },
                "HUD_Counseling": {
                    "name": "HUD Housing Counseling",
                    "level": "federal",
                    "category": "housing_counseling",
                    "description": "Free or low-cost housing counseling from HUD-approved agencies",
                    "services": [
                        "Eviction prevention",
                        "Rental housing counseling",
                        "Budgeting and financial management",
                        "Fair housing rights",
                        "Homebuyer education"
                    ],
                    "contact": {
                        "website": "https://www.hud.gov/findacounselor",
                        "phone": "1-800-569-4287"
                    }
                }
            },
            "state_template": {
                "description": "State programs vary - these are common categories to look for",
                "common_programs": [
                    {
                        "name": "State Rental Assistance",
                        "category": "rent_assistance",
                        "typical_name": "[State] Emergency Rental Assistance",
                        "lookup": "Search '[State] rental assistance program'"
                    },
                    {
                        "name": "State Weatherization Program",
                        "category": "weatherization",
                        "typical_name": "[State] Weatherization Assistance Program",
                        "lookup": "Contact state energy office"
                    },
                    {
                        "name": "State Legal Aid",
                        "category": "legal_aid",
                        "typical_name": "[State] Legal Services or Legal Aid Society",
                        "lookup": "Search '[State] legal aid housing'"
                    },
                    {
                        "name": "State Utility Assistance",
                        "category": "utility_assistance",
                        "typical_name": "[State] LIHEAP or Energy Assistance",
                        "lookup": "Contact state social services department"
                    },
                    {
                        "name": "State Homeless Prevention",
                        "category": "homeless_prevention",
                        "typical_name": "[State] Homeless Prevention Program",
                        "lookup": "Contact state housing authority"
                    },
                    {
                        "name": "State Landlord Incentive Programs",
                        "category": "landlord_rehab",
                        "for_landlords": True,
                        "typical_name": "[State] Housing Rehabilitation Loan/Grant",
                        "lookup": "Contact state housing finance agency"
                    }
                ]
            },
            "county_template": {
                "description": "County programs - must be discovered locally",
                "common_programs": [
                    {
                        "name": "County Emergency Assistance",
                        "category": "emergency_funds",
                        "typical_contact": "County Department of Human Services"
                    },
                    {
                        "name": "County Health Services",
                        "category": "healthcare",
                        "typical_contact": "County Health Department"
                    },
                    {
                        "name": "County Food Assistance",
                        "category": "food_assistance",
                        "typical_contact": "County Social Services"
                    }
                ]
            },
            "city_template": {
                "description": "City programs - must be discovered locally",
                "common_programs": [
                    {
                        "name": "City Rental Assistance",
                        "category": "rent_assistance",
                        "typical_contact": "City Housing Authority or City Manager's Office"
                    },
                    {
                        "name": "City Mediation Services",
                        "category": "mediation",
                        "typical_contact": "City Attorney's Office or Community Relations"
                    },
                    {
                        "name": "City Landlord-Tenant Resources",
                        "category": "housing_counseling",
                        "typical_contact": "City Housing Department"
                    }
                ]
            },
            "nonprofit_template": {
                "description": "Common nonprofit resources in most areas",
                "organizations": [
                    {
                        "name": "Salvation Army",
                        "services": ["Emergency rent/utility assistance", "Food", "Clothing"],
                        "lookup": "Search 'Salvation Army [City/Zip]'"
                    },
                    {
                        "name": "Catholic Charities",
                        "services": ["Emergency financial assistance", "Food pantry", "Counseling"],
                        "lookup": "Search 'Catholic Charities [City/Zip]'"
                    },
                    {
                        "name": "St. Vincent de Paul",
                        "services": ["Emergency rent/utility help", "Food", "Furniture"],
                        "lookup": "Search 'St. Vincent de Paul [City/Zip]'"
                    },
                    {
                        "name": "United Way 211",
                        "services": ["Comprehensive referral service for all local resources"],
                        "contact": "Dial 211 or visit 211.org",
                        "description": "Best starting point - connects to ALL local resources"
                    },
                    {
                        "name": "Local Food Banks",
                        "services": ["Food assistance", "Sometimes utility/rent help"],
                        "lookup": "Search 'food bank [City/Zip]' or visit feedingamerica.org"
                    },
                    {
                        "name": "Community Action Agencies",
                        "services": ["Various assistance programs", "Energy help", "Housing counseling"],
                        "lookup": "Search 'Community Action Agency [County]'"
                    }
                ]
            }
        }
        
        # Return programs first, then save will happen after assignment
        return programs
    
    def discover_programs(
        self,
        location: Dict[str, str],
        categories: Optional[List[str]] = None,
        urgency: str = "routine",
        household_size: Optional[int] = None,
        annual_income: Optional[float] = None,
        special_needs: Optional[List[str]] = None,
        for_landlord: bool = False
    ) -> Dict:
        """
        Discover all available programs for a location.
        
        Args:
            location: {"city": "Minneapolis", "county": "Hennepin", "state": "MN", "zip": "55401"}
            categories: List of ProgramCategory values, or None for all
            urgency: routine, soon, urgent, emergency
            household_size: Number of people (for income eligibility)
            annual_income: Total household income (for eligibility)
            special_needs: ["veteran", "disability", "senior", "homeless"] for specialized programs
            for_landlord: True if looking for landlord programs (rehab loans, tax credits)
        
        Returns:
            {
                "federal_programs": [...],
                "state_programs": [...],
                "county_programs": [...],
                "city_programs": [...],
                "nonprofit_resources": [...],
                "recommended_first_steps": [...],
                "emergency_contacts": [...],  # If urgency is emergency
                "eligibility_guidance": {...}
            }
        """
        logger.info(f"Discovering programs for {location.get('city', 'unknown')}, {location.get('state', 'unknown')}")
        
        result = {
            "location": location,
            "search_date": datetime.now().isoformat(),
            "urgency": urgency,
            "federal_programs": [],
            "state_programs": [],
            "county_programs": [],
            "city_programs": [],
            "nonprofit_resources": [],
            "recommended_first_steps": [],
            "emergency_contacts": [],
            "eligibility_guidance": {}
        }
        
        # Get federal programs
        result["federal_programs"] = self._get_federal_programs(
            categories, household_size, annual_income, special_needs, for_landlord
        )
        
        # Get state programs (with location-specific lookup guidance)
        result["state_programs"] = self._get_state_programs(
            location.get("state"), categories, for_landlord
        )
        
        # Get county programs (guidance for local discovery)
        result["county_programs"] = self._get_county_programs(
            location.get("county"), location.get("state"), categories
        )
        
        # Get city programs (guidance for local discovery)
        result["city_programs"] = self._get_city_programs(
            location.get("city"), location.get("state"), categories, for_landlord
        )
        
        # Get nonprofit resources
        result["nonprofit_resources"] = self._get_nonprofit_resources(
            location, categories
        )
        
        # Generate recommended first steps based on urgency
        result["recommended_first_steps"] = self._get_first_steps(
            urgency, categories, special_needs
        )
        
        # Emergency contacts if urgent
        if urgency in ["urgent", "emergency"]:
            result["emergency_contacts"] = self._get_emergency_contacts(
                location, categories
            )
        
        # Eligibility guidance
        if household_size and annual_income:
            result["eligibility_guidance"] = self._calculate_eligibility(
                household_size, annual_income, location.get("state")
            )
        
        return result
    
    def _get_federal_programs(
        self,
        categories: Optional[List[str]],
        household_size: Optional[int],
        annual_income: Optional[float],
        special_needs: Optional[List[str]],
        for_landlord: bool
    ) -> List[Dict]:
        """Get applicable federal programs"""
        programs = []
        
        for program_id, program_data in self.programs.get("federal", {}).items():
            # Skip if not matching category filter
            if categories and program_data.get("category") not in categories:
                continue
            
            # Skip landlord programs if tenant, and vice versa
            if for_landlord and not program_data.get("for_landlords"):
                continue
            if not for_landlord and program_data.get("category") in ["landlord_rehab", "landlord_tax_credits"]:
                continue
            
            # Check special needs
            if special_needs:
                program_category = program_data.get("category")
                if "veteran" in special_needs and program_category != "veteran_services":
                    continue  # Skip unless veteran program
                if "senior" in special_needs and program_category != "senior_services":
                    # Senior can use general programs too, so don't skip
                    pass
            
            programs.append({
                "id": program_id,
                **program_data,
                "level": "federal",
                "effectiveness_score": self._get_effectiveness_score(program_id)
            })
        
        # Sort by effectiveness
        programs.sort(key=lambda x: x.get("effectiveness_score", 0), reverse=True)
        
        return programs
    
    def _get_state_programs(
        self,
        state: Optional[str],
        categories: Optional[List[str]],
        for_landlord: bool
    ) -> List[Dict]:
        """Get state-specific programs with lookup guidance"""
        if not state:
            return []
        
        # Check if we have state-specific data
        state_key = f"state_{state.upper()}"
        if state_key in self.programs:
            # We have specific data for this state
            return self.programs[state_key]
        
        # Otherwise, return template with lookup guidance
        template = self.programs.get("state_template", {})
        common_programs = template.get("common_programs", [])
        
        result = []
        for prog in common_programs:
            # Filter by category
            if categories and prog.get("category") not in categories:
                continue
            
            # Filter landlord vs tenant
            if for_landlord and not prog.get("for_landlords"):
                continue
            if not for_landlord and prog.get("for_landlords"):
                continue
            
            # Customize for state
            prog_copy = prog.copy()
            prog_copy["name"] = prog_copy.get("typical_name", prog_copy["name"]).replace("[State]", state.upper())
            prog_copy["lookup"] = prog_copy.get("lookup", "").replace("[State]", state)
            prog_copy["level"] = "state"
            prog_copy["note"] = f"Contact {state} state agencies for current programs"
            
            result.append(prog_copy)
        
        return result
    
    def _get_county_programs(
        self,
        county: Optional[str],
        state: Optional[str],
        categories: Optional[List[str]]
    ) -> List[Dict]:
        """Get county programs with local discovery guidance"""
        if not county:
            return []
        
        template = self.programs.get("county_template", {})
        common_programs = template.get("common_programs", [])
        
        result = []
        for prog in common_programs:
            if categories and prog.get("category") not in categories:
                continue
            
            prog_copy = prog.copy()
            prog_copy["name"] = f"{county} County {prog['name']}"
            prog_copy["level"] = "county"
            prog_copy["lookup"] = f"Contact {prog.get('typical_contact', 'county offices')} in {county} County, {state}"
            
            result.append(prog_copy)
        
        return result
    
    def _get_city_programs(
        self,
        city: Optional[str],
        state: Optional[str],
        categories: Optional[List[str]],
        for_landlord: bool
    ) -> List[Dict]:
        """Get city programs with local discovery guidance"""
        if not city:
            return []
        
        template = self.programs.get("city_template", {})
        common_programs = template.get("common_programs", [])
        
        result = []
        for prog in common_programs:
            if categories and prog.get("category") not in categories:
                continue
            
            prog_copy = prog.copy()
            prog_copy["name"] = f"{city} {prog['name']}"
            prog_copy["level"] = "city"
            prog_copy["lookup"] = f"Contact {prog.get('typical_contact', 'city offices')} in {city}, {state}"
            
            result.append(prog_copy)
        
        return result
    
    def _get_nonprofit_resources(
        self,
        location: Dict[str, str],
        categories: Optional[List[str]]
    ) -> List[Dict]:
        """Get nonprofit resources available in area"""
        template = self.programs.get("nonprofit_template", {})
        organizations = template.get("organizations", [])
        
        result = []
        for org in organizations:
            org_copy = org.copy()
            
            # Customize lookup for location
            city = location.get("city", "")
            zip_code = location.get("zip", "")
            
            if "lookup" in org_copy:
                org_copy["lookup"] = org_copy["lookup"].replace("[City/Zip]", city or zip_code)
            
            org_copy["level"] = "nonprofit"
            result.append(org_copy)
        
        return result
    
    def _get_first_steps(
        self,
        urgency: str,
        categories: Optional[List[str]],
        special_needs: Optional[List[str]]
    ) -> List[Dict]:
        """Generate recommended first steps based on situation"""
        steps = []
        
        if urgency == "emergency":
            steps.append({
                "priority": 1,
                "action": "Call United Way 211",
                "description": "Dial 211 for immediate connection to emergency resources",
                "phone": "211",
                "why": "Fastest way to get help - 24/7 service connects to all local emergency assistance"
            })
            
            if categories and "utility_assistance" in categories:
                steps.append({
                    "priority": 1,
                    "action": "Contact LIHEAP for emergency utility assistance",
                    "description": "If you have a shutoff notice, LIHEAP can provide emergency help within 18-48 hours",
                    "why": "Prevents utility shutoff"
                })
            
            if categories and ("rent_assistance" in categories or "homeless_prevention" in categories):
                steps.append({
                    "priority": 1,
                    "action": "Contact local legal aid immediately",
                    "description": "If facing eviction, you may have defenses or time to get assistance",
                    "why": "Eviction prevention - legal help can buy time and connect to emergency funds"
                })
        
        elif urgency == "urgent":
            steps.append({
                "priority": 1,
                "action": "Call United Way 211",
                "description": "Get connected to all available local resources quickly",
                "phone": "211"
            })
            
            steps.append({
                "priority": 2,
                "action": "Contact local Community Action Agency",
                "description": "They often have emergency funds and can process applications quickly",
                "why": "Fast access to multiple programs"
            })
        
        else:  # routine or soon
            steps.append({
                "priority": 1,
                "action": "Apply for Section 8 Housing Choice Voucher",
                "description": "Even with long waitlists, get on the list now - it's the most comprehensive assistance",
                "contact": "Local Public Housing Authority",
                "why": "Long-term solution - covers ongoing rent"
            })
            
            steps.append({
                "priority": 2,
                "action": "Contact HUD Housing Counseling agency",
                "description": "Free counseling to help you navigate all available programs and create a plan",
                "contact": "Call 1-800-569-4287 to find local counselor",
                "why": "Expert guidance on all options"
            })
        
        # Add special needs resources
        if special_needs:
            if "veteran" in special_needs:
                steps.append({
                    "priority": 1,
                    "action": "Contact VA Housing Assistance",
                    "description": "Veterans have specialized programs and priority access",
                    "phone": "1-877-827-3702",
                    "why": "Veterans get priority and specialized support"
                })
            
            if "disability" in special_needs:
                steps.append({
                    "priority": 2,
                    "action": "Check SSI eligibility",
                    "description": "If disabled, you may qualify for SSI which includes housing allowance",
                    "phone": "1-800-772-1213",
                    "why": "Monthly income for housing and living expenses"
                })
        
        return steps
    
    def _get_emergency_contacts(
        self,
        location: Dict[str, str],
        categories: Optional[List[str]]
    ) -> List[Dict]:
        """Get emergency contacts for urgent situations"""
        contacts = [
            {
                "name": "United Way 211",
                "phone": "211",
                "description": "24/7 connection to emergency resources",
                "services": "All emergency assistance - rent, utilities, food, shelter"
            },
            {
                "name": "National Domestic Violence Hotline",
                "phone": "1-800-799-7233",
                "description": "If housing emergency involves domestic violence",
                "services": "Safety planning, emergency shelter referrals"
            },
            {
                "name": "Homeless Prevention Hotline",
                "phone": "Contact local 211 for your area's hotline",
                "description": "Immediate help to prevent homelessness",
                "services": "Emergency shelter, rapid rehousing"
            }
        ]
        
        if categories:
            if "utility_assistance" in categories:
                contacts.append({
                    "name": "LIHEAP Crisis Line",
                    "phone": "Contact state LIHEAP office",
                    "description": "Emergency utility assistance within 18-48 hours",
                    "services": "Prevent utility shutoff"
                })
            
            if "legal_aid" in categories or "rent_assistance" in categories:
                contacts.append({
                    "name": "Legal Aid Housing Hotline",
                    "phone": "Contact local legal aid - find at lsc.gov",
                    "description": "Immediate legal help for eviction or unsafe housing",
                    "services": "Eviction defense, emergency legal representation"
                })
        
        return contacts
    
    def _calculate_eligibility(
        self,
        household_size: int,
        annual_income: float,
        state: Optional[str]
    ) -> Dict:
        """Calculate likely eligibility for programs"""
        # 2024 federal poverty guidelines (approximate - these update annually)
        poverty_line_base = 15060  # For 1 person
        poverty_line_per_additional = 5380
        
        poverty_line = poverty_line_base + (household_size - 1) * poverty_line_per_additional
        
        income_percent = (annual_income / poverty_line) * 100
        
        guidance = {
            "household_size": household_size,
            "annual_income": annual_income,
            "poverty_line": poverty_line,
            "percent_of_poverty": round(income_percent, 1),
            "likely_eligible_programs": []
        }
        
        # Determine eligibility
        if income_percent <= 50:
            guidance["likely_eligible_programs"].extend([
                "Section 8 Housing Choice Voucher (very low income)",
                "Public Housing",
                "Legal Aid (most programs)",
                "Most state and local assistance programs"
            ])
        
        if income_percent <= 80:
            guidance["likely_eligible_programs"].extend([
                "Section 8 (low income priority)",
                "ERAP (if still available)",
                "Some legal aid programs"
            ])
        
        if income_percent <= 125:
            guidance["likely_eligible_programs"].extend([
                "Legal Services Corporation funded legal aid"
            ])
        
        if income_percent <= 150:
            guidance["likely_eligible_programs"].extend([
                "LIHEAP (in most states)",
                "Weatherization programs",
                "Some state rental assistance"
            ])
        
        guidance["note"] = "Eligibility varies by program and location. Many programs have additional requirements beyond income. Apply even if you're close to the limits - some programs have flexibility."
        
        return guidance
    
    def _get_effectiveness_score(self, program_id: str) -> float:
        """Get effectiveness score from outcomes data"""
        if program_id in self.outcomes:
            total = self.outcomes[program_id].get("total_tracked", 0)
            if total > 0:
                approved = self.outcomes[program_id].get("approved", 0)
                return (approved / total) * 100
        return 50.0  # Default score if no data
    
    def generate_application_guide(
        self,
        program_id: str,
        location: Dict[str, str],
        household_info: Optional[Dict] = None
    ) -> Dict:
        """
        Generate detailed application guide for a specific program.
        
        Returns step-by-step instructions, required documents checklist,
        timeline, and tips for successful application.
        """
        # Find program
        program = None
        for level in ["federal", "state", "county", "city"]:
            if level in self.programs:
                if isinstance(self.programs[level], dict) and program_id in self.programs[level]:
                    program = self.programs[level][program_id]
                    break
        
        if not program:
            return {"error": "Program not found"}
        
        guide = {
            "program": program.get("name"),
            "program_id": program_id,
            "location": location,
            "steps": [],
            "required_documents": program.get("required_docs", []),
            "timeline": program.get("processing_time", "Contact program for timeline"),
            "tips": [],
            "contact_info": program.get("contact", {}),
            "executive_escalation": program.get("executive_escalation", [])
        }
        
        # Generate steps based on program type
        if program_id == "HUD_Section8":
            guide["steps"] = [
                {
                    "step": 1,
                    "action": "Find your local Public Housing Authority (PHA)",
                    "description": f"Search for '{location.get('city', location.get('county'))} PHA' or visit hud.gov/program_offices/public_indian_housing/pha/contacts",
                    "time": "10 minutes"
                },
                {
                    "step": 2,
                    "action": "Check if waitlist is open",
                    "description": "Call or visit PHA website - many have closed waitlists. If closed, ask when they'll reopen.",
                    "time": "5-15 minutes"
                },
                {
                    "step": 3,
                    "action": "Gather required documents",
                    "description": "Collect all items from the required documents list below",
                    "time": "1-3 days"
                },
                {
                    "step": 4,
                    "action": "Complete application",
                    "description": "Applications are usually online or at PHA office. Be thorough and accurate.",
                    "time": "1-2 hours"
                },
                {
                    "step": 5,
                    "action": "Submit application",
                    "description": "Keep a copy of your application and any confirmation number",
                    "time": "15 minutes"
                },
                {
                    "step": 6,
                    "action": "Wait for notification",
                    "description": "You'll be added to waitlist. Keep contact info current with PHA.",
                    "time": "Variable - often years"
                },
                {
                    "step": 7,
                    "action": "Respond immediately to PHA contact",
                    "description": "When your name comes up, you have limited time to respond or lose your spot",
                    "time": "Respond within their deadline"
                }
            ]
            
            guide["tips"] = [
                "Apply to MULTIPLE PHAs if you're willing to move - increases your chances",
                "Check for special preferences (veteran, elderly, disabled) that may move you up the list",
                "Keep your contact information updated with the PHA - if they can't reach you, you lose your spot",
                "While waiting, apply for other programs - don't put all eggs in one basket",
                "Some PHAs accept pre-applications even when waitlist is closed - check"
            ]
        
        elif program_id == "LIHEAP":
            guide["steps"] = [
                {
                    "step": 1,
                    "action": "Find your state LIHEAP office",
                    "description": f"Search '{location.get('state')} LIHEAP' or visit acf.hhs.gov/ocs/liheap-state-and-territory-contact-listing",
                    "time": "5 minutes"
                },
                {
                    "step": 2,
                    "action": "Check application period",
                    "description": "LIHEAP has seasonal application periods. Emergency assistance may be available year-round.",
                    "time": "5 minutes",
                    "note": "If you have a shutoff notice, mention it immediately - you may qualify for emergency assistance"
                },
                {
                    "step": 3,
                    "action": "Gather required documents",
                    "description": "Collect documents from list below, including utility bills or shutoff notice",
                    "time": "30 minutes"
                },
                {
                    "step": 4,
                    "action": "Apply",
                    "description": "Application may be online, by phone, or in person depending on your state",
                    "time": "30-60 minutes"
                },
                {
                    "step": 5,
                    "action": "Wait for processing",
                    "description": "Emergency: 18-48 hours. Regular: 2-4 weeks",
                    "time": "Variable"
                }
            ]
            
            guide["tips"] = [
                "If you have a shutoff notice, SAY SO IMMEDIATELY - you may get emergency processing",
                "Apply early in the season - funding can run out",
                "You can usually apply once per heating season and once per cooling season",
                "Some states allow online applications, others require in-person - check first",
                "Keep copies of all utility bills and shutoff notices"
            ]
        
        return guide
    
    def get_intensity_based_recommendations(
        self,
        intensity_level: str,
        situation: Dict
    ) -> Dict:
        """
        Integrate with adaptive intensity system.
        
        Returns program recommendations based on intensity level:
        - POSITIVE: Recognition resources, proactive assistance
        - COLLABORATIVE: Mediation, communication tools, assistance programs
        - ASSERTIVE: Legal aid, tenant rights resources, advocacy
        - ESCALATED: Emergency funds, legal representation, fast-track programs
        - MAXIMUM: All resources + media contacts for public pressure
        """
        recommendations = {
            "intensity_level": intensity_level,
            "recommended_programs": [],
            "recommended_actions": [],
            "tone": "",
            "guidance": ""
        }
        
        if intensity_level == "POSITIVE":
            recommendations["tone"] = "Proactive and supportive"
            recommendations["guidance"] = "Everything is going well! Here are resources to keep it that way and plan ahead."
            recommendations["recommended_programs"] = [
                "HUD Housing Counseling - financial planning and budgeting",
                "Local tenant education workshops",
                "Credit building programs"
            ]
            recommendations["recommended_actions"] = [
                "Consider applying for Section 8 now (even with good situation, waitlists are long)",
                "Build emergency fund with help of financial counselor",
                "Learn about tenant rights so you know them if needed"
            ]
        
        elif intensity_level == "COLLABORATIVE":
            recommendations["tone"] = "Helpful and solution-focused"
            recommendations["guidance"] = "Let's try to resolve this cooperatively before formal action. Assistance programs can help."
            recommendations["recommended_programs"] = [
                "City/County mediation services - neutral third party to resolve disputes",
                "HUD Housing Counseling - help communicating with landlord",
                "Rental assistance programs - if issue is financial",
                "LIHEAP - if utility bills are the problem",
                "Legal aid - to understand your rights without formal action yet"
            ]
            recommendations["recommended_actions"] = [
                "Mediation with landlord (free in many cities)",
                "Apply for rental/utility assistance if financial",
                "Document the issue (photos, dates) while trying cooperative resolution",
                "Get counseling on tenant rights before formal complaints"
            ]
        
        elif intensity_level == "ASSERTIVE":
            recommendations["tone"] = "Firm but measured"
            recommendations["guidance"] = "Formal action is appropriate. Combine legal resources with assistance programs."
            recommendations["recommended_programs"] = [
                "Legal Aid - formal legal representation",
                "Emergency rental assistance - if at risk of eviction",
                "LIHEAP emergency assistance - if utilities at risk",
                "HUD Housing Counseling - eviction prevention",
                "Local tenant rights organizations"
            ]
            recommendations["recommended_actions"] = [
                "Contact legal aid IMMEDIATELY",
                "Apply for emergency assistance programs",
                "Document everything in writing",
                "File formal complaints (see complaint filing system)",
                "Understand your legal defenses"
            ]
        
        elif intensity_level == "ESCALATED":
            recommendations["tone"] = "Urgent and comprehensive"
            recommendations["guidance"] = "This requires immediate comprehensive action. Access ALL available resources."
            recommendations["recommended_programs"] = [
                "Legal Aid - PRIORITY emergency legal help",
                "Emergency rental assistance - FAST TRACK",
                "LIHEAP crisis assistance - 18-48 hour processing",
                "United Way 211 - connect to ALL local emergency resources",
                "Homeless prevention programs",
                "Emergency shelter information (backup plan)"
            ]
            recommendations["recommended_actions"] = [
                "Call 211 IMMEDIATELY for emergency connection",
                "Contact legal aid with URGENT flag",
                "Apply to ALL emergency assistance programs simultaneously",
                "File complaints with ALL relevant agencies (see complaint system)",
                "Prepare emergency backup plan (family, shelter info)"
            ]
        
        elif intensity_level == "MAXIMUM":
            recommendations["tone"] = "CRISIS - all available resources"
            recommendations["guidance"] = "EMERGENCY. Deploy every available resource and public pressure."
            recommendations["recommended_programs"] = [
                "Legal Aid - EMERGENCY legal representation",
                "ALL emergency assistance programs",
                "LIHEAP crisis line",
                "United Way 211 - emergency",
                "Homeless prevention hotline",
                "Domestic violence resources (if applicable)",
                "Veterans crisis line (if veteran)"
            ]
            recommendations["recommended_actions"] = [
                "Dial 211 RIGHT NOW",
                "Contact legal aid emergency line",
                "File with EVERY possible complaint venue",
                "Contact local media (housing reporter, investigative journalists)",
                "Contact elected officials (city council, mayor, state rep)",
                "Post to social media with documentation (public pressure)",
                "Contact community advocacy groups for protest/public action"
            ]
            recommendations["media_contacts"] = [
                "Local TV news housing reporters",
                "Local newspaper investigative team",
                "Local radio talk shows",
                "Community Facebook groups",
                "NextDoor (neighborhood app)"
            ]
        
        return recommendations
    
    def track_application_outcome(
        self,
        program_id: str,
        outcome: str,
        timeline_days: Optional[int] = None,
        notes: Optional[str] = None
    ):
        """Track program application outcomes for effectiveness scoring"""
        if program_id not in self.outcomes:
            self.outcomes[program_id] = {
                "total_tracked": 0,
                "approved": 0,
                "denied": 0,
                "pending": 0,
                "avg_timeline_days": 0
            }
        
        self.outcomes[program_id]["total_tracked"] += 1
        
        if outcome == "approved":
            self.outcomes[program_id]["approved"] += 1
        elif outcome == "denied":
            self.outcomes[program_id]["denied"] += 1
        elif outcome == "pending":
            self.outcomes[program_id]["pending"] += 1
        
        if timeline_days:
            # Update average timeline
            current_avg = self.outcomes[program_id].get("avg_timeline_days", 0)
            total = self.outcomes[program_id]["total_tracked"]
            new_avg = ((current_avg * (total - 1)) + timeline_days) / total
            self.outcomes[program_id]["avg_timeline_days"] = round(new_avg, 1)
        
        self._save_outcomes()
        
        logger.info(f"Tracked outcome for {program_id}: {outcome}")


# Example usage
if __name__ == "__main__":
    engine = HousingProgramsEngine()
    
    # Example: Discover programs for Minneapolis resident
    location = {
        "city": "Minneapolis",
        "county": "Hennepin",
        "state": "MN",
        "zip": "55401"
    }
    
    programs = engine.discover_programs(
        location=location,
        categories=["rent_assistance", "utility_assistance", "legal_aid"],
        urgency="urgent",
        household_size=3,
        annual_income=28000,
        special_needs=["disability"]
    )
    
    print(json.dumps(programs, indent=2))
    
    # Example: Get application guide for Section 8
    guide = engine.generate_application_guide(
        program_id="HUD_Section8",
        location=location,
        household_info={"size": 3, "income": 28000}
    )
    
    print("\n" + "="*60)
    print("APPLICATION GUIDE:")
    print("="*60)
    print(json.dumps(guide, indent=2))
    
    # Example: Get intensity-based recommendations
    recommendations = engine.get_intensity_based_recommendations(
        intensity_level="ESCALATED",
        situation={"issue": "no_heat", "days": 15}
    )
    
    print("\n" + "="*60)
    print("INTENSITY-BASED RECOMMENDATIONS:")
    print("="*60)
    print(json.dumps(recommendations, indent=2))
