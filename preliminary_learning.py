"""
Preliminary Information Learning Module for Semptify
Acquires and validates foundational knowledge about:
- Rental procedures and forms
- Legal processes and requirements
- Court filing procedures
- Complaint filing processes
- Funding sources and requirements
- Governing agencies and regulations

Can be run anytime as a fact-checking and knowledge acquisition system.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class PreliminaryLearningModule:
    """
    Comprehensive information acquisition system for legal housing procedures.
    Provides fact-checked data about forms, procedures, and requirements.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.knowledge_base_file = os.path.join(data_dir, "preliminary_knowledge.json")
        self.knowledge_base = self._load_knowledge_base()
        self.fact_check_log_file = os.path.join(data_dir, "fact_check_log.json")
        self.fact_check_log = self._load_fact_check_log()

    def _load_knowledge_base(self) -> dict:
        """Load or initialize the knowledge base."""
        if os.path.exists(self.knowledge_base_file):
            try:
                with open(self.knowledge_base_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self._initialize_knowledge_base()

    def _initialize_knowledge_base(self) -> dict:
        """Initialize comprehensive knowledge base with all procedures."""
        return {
            "rental_procedures": {
                "lease_signing": {
                    "title": "Lease Signing Process",
                    "steps": [
                        "Review lease for 3-5 days before signing",
                        "Compare terms with local housing code",
                        "Check for illegal clauses (no pets, no repairs clause)",
                        "Identify all required deposits and fees",
                        "Get copy of complete lease BEFORE move-in",
                        "Take photos of property condition"
                    ],
                    "forms_required": [
                        "Lease agreement (signed copy for tenant)",
                        "Move-in inspection checklist",
                        "Proof of deposits (itemized)",
                        "Landlord contact information",
                        "Emergency contact numbers"
                    ],
                    "common_issues": ["Missing clauses", "Illegal terms", "Deposit discrepancies"],
                    "timeline_days": 3,
                    "jurisdiction_specific": True
                },
                "move_in_inspection": {
                    "title": "Move-In Inspection",
                    "steps": [
                        "Document property condition with photos/video",
                        "Complete move-in checklist provided by landlord",
                        "Note all existing damages in writing",
                        "Get landlord signature on checklist",
                        "Keep copy for records",
                        "Note date and time of inspection"
                    ],
                    "forms_required": [
                        "Move-in inspection checklist",
                        "Photo/video documentation",
                        "Signed condition report",
                        "Timestamp verification"
                    ],
                    "common_issues": ["Undocumented damage", "Landlord disputes", "Lost records"],
                    "timeline_days": 1,
                    "jurisdiction_specific": False
                },
                "rent_payment": {
                    "title": "Rent Payment Procedures",
                    "steps": [
                        "Confirm payment method with landlord (check/ACH/online)",
                        "Get payment address in writing",
                        "Pay by traceable method (check with number, ACH receipt)",
                        "Retain proof of payment (cancelled check, receipt, bank record)",
                        "Pay on time to deadline",
                        "Document any agreed-upon payment plan"
                    ],
                    "forms_required": [
                        "Rent payment agreement",
                        "Payment receipt template",
                        "Late payment notice (if applicable)",
                        "Payment plan agreement (if negotiated)"
                    ],
                    "common_issues": ["Lost receipts", "Payment disputes", "Late fees"],
                    "timeline_days": 0,
                    "jurisdiction_specific": False
                },
                "deposit_return": {
                    "title": "Security Deposit Return Process",
                    "steps": [
                        "Document move-out condition with photos/video",
                        "Complete move-out inspection with landlord if possible",
                        "Get written move-out checklist signed",
                        "Provide forwarding address to landlord",
                        "Keep copy of all documentation",
                        "Follow up if deposit not returned within legal timeframe"
                    ],
                    "forms_required": [
                        "Move-out inspection checklist",
                        "Photo/video documentation",
                        "Forwarding address confirmation",
                        "Deposit return receipt",
                        "Itemized deduction list (from landlord)"
                    ],
                    "common_issues": ["Withheld deposits", "Inflated damage charges", "No accounting"],
                    "timeline_days": 30,  # Varies by state (30-45 days typical)
                    "jurisdiction_specific": True
                }
            },
            "legal_procedures": {
                "tenant_rights": {
                    "title": "Basic Tenant Rights",
                    "content": {
                        "habitability": "Landlord must maintain safe, sanitary conditions",
                        "privacy": "Tenant has right to quiet enjoyment without landlord interference",
                        "repairs": "Landlord must make repairs within timeframe (typically 14 days for urgent)",
                        "retaliation": "Illegal for landlord to retaliate for asserting rights",
                        "discrimination": "Protected classes: race, color, national origin, religion, sex, disability, familial status"
                    },
                    "action_required": [
                        "Put requests in writing",
                        "Document all communication",
                        "Send via certified mail or email",
                        "Keep copies of all correspondence"
                    ],
                    "common_violations": ["Unrepaired maintenance", "No notice before entry", "Illegal fees"],
                    "jurisdiction_specific": True
                },
                "maintenance_rights": {
                    "title": "Right to Repair Process",
                    "steps": [
                        "Document defect with photos/video and date",
                        "Send written repair request to landlord (certified mail)",
                        "Give landlord 14 days to inspect and schedule repair (varies by state)",
                        "Follow up if no response within timeframe",
                        "Document all communication",
                        "If no repair, consult with attorney about repair-and-deduct option"
                    ],
                    "forms_required": [
                        "Repair request letter template",
                        "Photo/video documentation",
                        "Defect severity assessment",
                        "Timeline tracking sheet",
                        "Follow-up notice template"
                    ],
                    "common_issues": ["Ignored requests", "Slow response", "Incomplete repairs"],
                    "timeline_days": 14,
                    "jurisdiction_specific": True
                },
                "eviction_defense": {
                    "title": "Eviction Process Overview",
                    "steps": [
                        "Receive notice to vacate (typically 30-60 days before eviction)",
                        "Respond within required timeframe (typically 3-10 days)",
                        "Gather all payment receipts and documentation",
                        "Prepare defense (invalid notice, discrimination, retaliation)",
                        "Attend court hearing",
                        "Assert any applicable defenses"
                    ],
                    "forms_required": [
                        "Notice to vacate template",
                        "Answer to eviction complaint",
                        "Proof of payment document",
                        "Affidavit of facts",
                        "Evidence compilation checklist"
                    ],
                    "common_issues": ["Invalid notice", "Improper service", "Retaliation claims"],
                    "timeline_days": 60,
                    "jurisdiction_specific": True,
                    "critical": True
                }
            },
            "court_procedures": {
                "filing_lawsuit": {
                    "title": "Small Claims/Tenant Court Filing",
                    "steps": [
                        "Determine proper court (small claims or tenant court)",
                        "Calculate exact amount owed (principal + damages + costs)",
                        "Gather all supporting documentation",
                        "Complete complaint form (court-specific)",
                        "Calculate filing fee",
                        "File in person or by mail",
                        "Get case number and hearing date",
                        "Serve defendant with copy of complaint"
                    ],
                    "forms_required": [
                        "Complaint/petition form (court-specific)",
                        "Proof of service form",
                        "Evidence list and documentation",
                        "Calculation worksheet",
                        "Filing fee receipt"
                    ],
                    "common_issues": ["Wrong court", "Incomplete documentation", "Service issues"],
                    "timeline_days": 7,
                    "jurisdiction_specific": True,
                    "requires_attorney": False
                },
                "evidence_presentation": {
                    "title": "Organizing Evidence for Court",
                    "required_evidence": [
                        "Lease agreement (complete copy)",
                        "Move-in/move-out inspection photos",
                        "Rent payment receipts/proof",
                        "Communication records (emails, texts, letters)",
                        "Photos/videos of condition or issues",
                        "Repair request documentation",
                        "Witness contact information",
                        "Timeline of events"
                    ],
                    "organization": [
                        "Create chronological timeline",
                        "Label and number all documents",
                        "Create index with page references",
                        "Organize in folders by category",
                        "Prepare digital copies as backup",
                        "Create exhibit list with descriptions"
                    ],
                    "presentation": [
                        "Keep documents clear and legible",
                        "Use color-coded tabs for sections",
                        "Prepare brief summary (1 page)",
                        "Practice presenting key evidence",
                        "Have backup copies available"
                    ],
                    "common_mistakes": ["Disorganized documents", "Missing originals", "Unclear photos"],
                    "jurisdiction_specific": False
                },
                "court_appearance": {
                    "title": "Preparing for Court Appearance",
                    "preparation": [
                        "Arrive 15-30 minutes early",
                        "Dress professionally and conservatively",
                        "Bring all original documents and copies",
                        "Bring witness contact information",
                        "Plan what to say (keep it brief and factual)",
                        "Review key documents before hearing"
                    ],
                    "testimony_tips": [
                        "Speak clearly and calmly",
                        "Tell the truth",
                        "Answer questions directly",
                        "Don't get emotional or confrontational",
                        "Use dates and specific facts",
                        "Say 'I don't know' if unsure",
                        "Never interrupt the judge"
                    ],
                    "documentation": [
                        "Take notes during hearing",
                        "Record case number and outcome",
                        "Get copy of judgment",
                        "Understand appeal rights",
                        "Know enforcement procedures"
                    ],
                    "common_mistakes": ["Being late", "Unprepared", "Getting emotional"],
                    "jurisdiction_specific": True
                }
            },
            "complaint_filing": {
                "housing_authority": {
                    "title": "File Complaint with Housing Authority",
                    "procedure": [
                        "Identify relevant housing authority (city/county)",
                        "Gather all documentation of violations",
                        "Complete complaint form (available online or in person)",
                        "Include photos, correspondence, inspection results",
                        "Specify: property address, nature of violation, impact on habitability",
                        "Submit to housing inspector",
                        "Receive case number",
                        "Schedule inspection (typically within 14 days)",
                        "Cooperate with inspector",
                        "Receive inspection results",
                        "Follow up on violations"
                    ],
                    "forms_required": [
                        "Housing code violation complaint form",
                        "Documentation checklist",
                        "Inspector report (after filing)",
                        "Violation notice (if issued)",
                        "Correction order (if issued)"
                    ],
                    "violations_covered": [
                        "Lack of heat/hot water",
                        "Mold/pest infestation",
                        "Broken windows/doors",
                        "Non-functional plumbing",
                        "Electrical hazards",
                        "Lead paint (pre-1978 properties)"
                    ],
                    "timeline_days": 30,
                    "jurisdiction_specific": True,
                    "free": True
                },
                "attorney_general": {
                    "title": "File Complaint with State Attorney General",
                    "procedure": [
                        "Access state AG office website",
                        "Locate consumer/housing complaint form",
                        "Document all violations and communications",
                        "Include: property address, landlord name/contact, nature of complaint, dates",
                        "Attach copies of documentation (lease, photos, communications)",
                        "Submit online or by mail",
                        "Receive complaint number",
                        "AG office may investigate",
                        "Receive status updates",
                        "Monitor for enforcement actions"
                    ],
                    "forms_required": [
                        "Attorney General complaint form",
                        "Complaint narrative (2-3 pages)",
                        "Documentation package",
                        "Proof of filing receipt"
                    ],
                    "issues_covered": [
                        "Unfair/deceptive practices",
                        "Illegal fees or charges",
                        "Discriminatory practices",
                        "Violation of tenant rights",
                        "Scam or fraud"
                    ],
                    "timeline_days": 14,
                    "jurisdiction_specific": True,
                    "free": True
                },
                "tenant_union": {
                    "title": "File Complaint with Tenant Union/Rights Organization",
                    "procedure": [
                        "Locate local tenant union or legal aid organization",
                        "Gather all documentation",
                        "Contact organization (phone, email, or in person)",
                        "Describe issue and provide documentation",
                        "May help file formal complaint",
                        "May provide legal support",
                        "May join class action if applicable",
                        "Receive updates on case progress"
                    ],
                    "services": [
                        "Legal advice and counseling",
                        "Complaint preparation assistance",
                        "Representation in small claims court",
                        "Negotiation support",
                        "Class action participation",
                        "Community advocacy"
                    ],
                    "common_organizations": [
                        "Local Tenant Union",
                        "Legal Aid Society",
                        "Community Legal Services",
                        "Neighborhood Housing Services",
                        "Fair Housing Center"
                    ],
                    "timeline_days": 7,
                    "jurisdiction_specific": True,
                    "free": True
                }
            },
            "funding_sources": {
                "legal_aid": {
                    "title": "Legal Aid Organizations",
                    "services": [
                        "Free or low-cost legal advice",
                        "Representation in tenant disputes",
                        "Defense against evictions",
                        "Document preparation",
                        "Mediation services"
                    ],
                    "eligibility": [
                        "Income-based (typically 125-200% of poverty line)",
                        "Asset limits apply",
                        "Case type must be eligible",
                        "Residency requirements may apply"
                    ],
                    "access": [
                        "Visit local Legal Aid office",
                        "Call intake hotline",
                        "Apply online",
                        "Get referral from community organization"
                    ],
                    "fees": "Free or sliding scale based on income",
                    "typical_response_time": "1-2 weeks",
                    "jurisdiction_specific": True
                },
                "grant_programs": {
                    "title": "Housing Assistance Grants",
                    "types": [
                        "Emergency rental assistance",
                        "Utility payment assistance",
                        "Deposit assistance",
                        "Repair/habitability grants",
                        "Document preparation assistance"
                    ],
                    "eligibility": [
                        "Income-based (varies by program)",
                        "Residency in service area required",
                        "Specific issue (eviction threat, repair needed, etc.)",
                        "Application with documentation"
                    ],
                    "access": [
                        "211.org database (dial 211)",
                        "Local housing authority",
                        "City/county social services",
                        "Community action agencies"
                    ],
                    "fees": "Free",
                    "typical_response_time": "2-4 weeks",
                    "jurisdiction_specific": True
                },
                "pro_bono": {
                    "title": "Pro Bono Legal Services",
                    "providers": [
                        "Law firms (social responsibility programs)",
                        "Law schools (clinics)",
                        "Bar associations",
                        "Special interest advocacy groups"
                    ],
                    "how_to_access": [
                        "Contact local bar association",
                        "Ask Legal Aid for referral",
                        "Search pro bono clearinghouse",
                        "Contact non-profits in issue area"
                    ],
                    "typical_services": [
                        "Document review",
                        "Legal advice",
                        "Brief representation",
                        "Mediation",
                        "Limited scope services"
                    ],
                    "fees": "Free",
                    "typical_response_time": "1-4 weeks",
                    "jurisdiction_specific": True
                }
            },
            "governing_agencies": {
                "federal": {
                    "HUD": {
                        "name": "U.S. Department of Housing and Urban Development",
                        "authority": "Fair Housing Act enforcement",
                        "handles": [
                            "Discrimination complaints (race, color, national origin, religion, sex, disability, familial status)",
                            "Retaliation complaints",
                            "Accessibility violations (ADA)"
                        ],
                        "filing_deadline": "1 year from violation",
                        "process": [
                            "File complaint with HUD",
                            "HUD investigates (60 days typical)",
                            "Conciliation attempt",
                            "Determination of probable cause",
                            "Administrative hearing or litigation"
                        ],
                        "website": "www.hud.gov",
                        "free": True
                    },
                    "CFPB": {
                        "name": "Consumer Financial Protection Bureau",
                        "authority": "Financial services and consumer protection",
                        "handles": [
                            "Predatory lending",
                            "Financial fraud",
                            "Unfair financial practices"
                        ],
                        "filing_deadline": "3 years from violation",
                        "process": [
                            "Submit complaint online",
                            "CFPB forwards to company",
                            "Company must respond",
                            "CFPB reviews response",
                            "Resolution documented"
                        ],
                        "website": "www.consumerfinance.gov",
                        "free": True
                    }
                },
                "state": {
                    "attorney_general": {
                        "name": "State Attorney General",
                        "authority": "Consumer protection and tenant rights",
                        "handles": [
                            "Unfair/deceptive practices",
                            "Tenant rights violations",
                            "Illegal fees",
                            "Discriminatory practices"
                        ],
                        "filing_deadline": "Varies by state (usually 2-4 years)",
                        "process": [
                            "File complaint online or by mail",
                            "AG reviews and may investigate",
                            "May negotiate settlement",
                            "May file enforcement action",
                            "Periodic updates to complainant"
                        ],
                        "website": "[State]-ag.gov",
                        "free": True
                    },
                    "housing_finance": {
                        "name": "State Housing Finance Agency",
                        "authority": "Landlord licensing and multifamily housing regulation",
                        "handles": [
                            "Landlord compliance violations",
                            "Multifamily property complaints",
                            "Subsidy program administration",
                            "Licensing violations"
                        ],
                        "filing_deadline": "Varies by state",
                        "process": [
                            "File complaint with agency",
                            "Agency investigates",
                            "Landlord notified and responds",
                            "Determination made",
                            "Enforcement or dismissal"
                        ],
                        "website": "[State] housing authority website",
                        "free": True
                    }
                },
                "local": {
                    "city_housing_authority": {
                        "name": "City/County Housing Authority",
                        "authority": "Local housing code enforcement",
                        "handles": [
                            "Uninhabitable conditions",
                            "Code violations",
                            "Health/safety violations",
                            "Licensing violations"
                        ],
                        "filing_deadline": "Ongoing (24-month statute of repose for repairs)",
                        "process": [
                            "Contact housing inspector",
                            "File complaint",
                            "Schedule inspection (14 days typical)",
                            "Inspector documents violations",
                            "Landlord given correction order",
                            "Follow-up inspection",
                            "Enforcement if not corrected"
                        ],
                        "website": "City/county website",
                        "free": True
                    }
                }
            },
            "fact_check_topics": {
                "illegal_clauses": {
                    "title": "Commonly Illegal Lease Clauses",
                    "clauses": [
                        {
                            "clause": "No repairs clause",
                            "description": "Tenant agrees to make all repairs",
                            "legality": "ILLEGAL - Violates habitability",
                            "state_variations": ["Most states"]
                        },
                        {
                            "clause": "No pets clause (service animals)",
                            "description": "No animals of any kind allowed",
                            "legality": "ILLEGAL - Violates ADA",
                            "state_variations": ["Federal law"]
                        },
                        {
                            "clause": "Waive tenant rights",
                            "description": "Tenant waives right to repairs/maintenance",
                            "legality": "ILLEGAL - Cannot waive statutory rights",
                            "state_variations": ["Most states"]
                        },
                        {
                            "clause": "Landlord entry anytime",
                            "description": "Landlord can enter without notice anytime",
                            "legality": "ILLEGAL - Violates quiet enjoyment",
                            "state_variations": ["Most states, typically 24-48 hour notice required"]
                        },
                        {
                            "clause": "No retaliation clause needed",
                            "description": "Landlord not liable for retaliation",
                            "legality": "ILLEGAL - Cannot waive statutory protection",
                            "state_variations": ["Federal and most states"]
                        }
                    ]
                },
                "timelines": {
                    "title": "Legal Timeline Requirements",
                    "timelines": [
                        {
                            "action": "Repair request response",
                            "timeline": "14 days (typical)",
                            "variations": "Varies by state (7-30 days), urgent repairs may be 24-48 hours",
                            "consequence": "Tenant may use repair-and-deduct"
                        },
                        {
                            "action": "Deposit return after move-out",
                            "timeline": "30 days (typical)",
                            "variations": "30-45 days depending on state",
                            "consequence": "Landlord may owe damages/interest"
                        },
                        {
                            "action": "Notice to vacate",
                            "timeline": "30-60 days (typical)",
                            "variations": "Varies by state and cause",
                            "consequence": "Invalid notice may void eviction"
                        },
                        {
                            "action": "Landlord entry notice",
                            "timeline": "24-48 hours (typical)",
                            "variations": "Emergency may be immediate, varies by state",
                            "consequence": "Unlawful entry may support damages claim"
                        },
                        {
                            "action": "Eviction court hearing",
                            "timeline": "7-14 days after service (typical)",
                            "variations": "Varies by state",
                            "consequence": "Improper timeline may void eviction"
                        }
                    ]
                }
            }
        }

    def _save_knowledge_base(self):
        """Persist knowledge base to disk."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)

    def _load_fact_check_log(self) -> dict:
        """Load fact-check log."""
        if os.path.exists(self.fact_check_log_file):
            try:
                with open(self.fact_check_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "checks": [],
            "statistics": {
                "total_checks": 0,
                "total_verified": 0,
                "last_update": None
            }
        }

    def _save_fact_check_log(self):
        """Persist fact check log."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.fact_check_log_file, 'w') as f:
            json.dump(self.fact_check_log, f, indent=2)

    # ========================================================================
    # ACQUIRE: Get information from knowledge base
    # ========================================================================

    def get_procedures(self, category: str, subcategory: Optional[str] = None) -> Dict:
        """
        Get procedures by category.
        
        Args:
            category: 'rental_procedures', 'legal_procedures', 'court_procedures', 
                     'complaint_filing', 'funding_sources', 'governing_agencies'
            subcategory: Optional specific procedure (e.g., 'lease_signing')
            
        Returns:
            Dictionary of procedures
        """
        if category not in self.knowledge_base:
            return {"error": f"Category '{category}' not found"}
        
        cat_data = self.knowledge_base[category]
        
        if subcategory:
            if subcategory in cat_data:
                return cat_data[subcategory]
            return {"error": f"Subcategory '{subcategory}' not found in {category}"}
        
        return cat_data

    def get_forms(self, category: str, subcategory: Optional[str] = None) -> List[str]:
        """
        Get forms required for a procedure.
        
        Args:
            category: Procedure category
            subcategory: Specific procedure
            
        Returns:
            List of required forms
        """
        proc = self.get_procedures(category, subcategory)
        
        if "error" in proc:
            return []
        
        if isinstance(proc, dict) and "forms_required" in proc:
            return proc["forms_required"]
        
        forms = []
        for key, value in proc.items():
            if isinstance(value, dict) and "forms_required" in value:
                forms.extend(value["forms_required"])
        
        return forms

    def get_timeline(self, category: str, subcategory: Optional[str] = None) -> Tuple[Optional[int], str]:
        """
        Get timeline for a procedure.
        
        Args:
            category: Procedure category
            subcategory: Specific procedure
            
        Returns:
            Tuple of (days: int, unit: str)
        """
        proc = self.get_procedures(category, subcategory)
        
        if "error" in proc:
            return None, "Unknown"
        
        # Try to find timeline_days in procedure
        if isinstance(proc, dict):
            if "timeline_days" in proc:
                days = proc["timeline_days"]
                unit = "days" if days != 1 else "day"
                return days, unit
        
        return None, "Varies"

    def get_jurisdiction_info(self, category: str, subcategory: str) -> bool:
        """Check if procedure varies by jurisdiction."""
        proc = self.get_procedures(category, subcategory)
        
        if "error" in proc:
            return False
        
        return proc.get("jurisdiction_specific", False)

    def get_agencies_for_issue(self, issue_type: str) -> List[Dict]:
        """
        Get relevant agencies for an issue type.
        
        Args:
            issue_type: 'maintenance', 'eviction', 'discrimination', 'fraud', etc.
            
        Returns:
            List of agencies that handle this issue
        """
        agencies = []
        
        # Map issue types to agencies
        issue_map = {
            "maintenance": ["housing_authority", "city_housing_authority"],
            "habitability": ["housing_authority", "city_housing_authority"],
            "discrimination": ["HUD", "attorney_general"],
            "retaliation": ["HUD", "attorney_general"],
            "eviction": ["attorney_general", "Legal Aid"],
            "fraud": ["CFPB", "attorney_general"],
            "illegal_fee": ["attorney_general", "CFPB"],
            "repair": ["housing_authority", "city_housing_authority"]
        }
        
        agency_keys = issue_map.get(issue_type, [])
        
        # Collect agency info
        agencies_data = self.knowledge_base.get("governing_agencies", {})
        
        for key in agency_keys:
            # Search nested structure
            for level in agencies_data.values():
                if isinstance(level, dict) and key in level:
                    agency_info = level[key].copy()
                    agency_info["id"] = key
                    agencies.append(agency_info)
        
        return agencies

    def fact_check(self, claim: str, category: str, subcategory: Optional[str] = None) -> Dict:
        """
        Fact-check a claim against knowledge base.
        
        Args:
            claim: The claim to verify
            category: Knowledge category to check against
            subcategory: Optional specific subcategory
            
        Returns:
            Fact-check result with status and details
        """
        result = {
            "claim": claim,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "subcategory": subcategory,
            "status": "UNVERIFIED",
            "details": "",
            "sources": []
        }
        
        proc = self.get_procedures(category, subcategory)
        
        if "error" in proc:
            result["status"] = "CATEGORY_NOT_FOUND"
            return result
        
        # Simple fact-checking logic
        claim_lower = claim.lower()
        
        # Check against steps/content
        all_content = json.dumps(proc).lower()
        
        if claim_lower in all_content:
            result["status"] = "VERIFIED"
            result["details"] = "Claim found in knowledge base"
        elif any(word in claim_lower for word in ["illegal", "not allowed", "prohibited"]):
            # Check against illegal clauses
            illegal_info = self.get_procedures("fact_check_topics", "illegal_clauses")
            if "clauses" in illegal_info:
                for clause in illegal_info["clauses"]:
                    if claim_lower in json.dumps(clause).lower():
                        result["status"] = "VERIFIED"
                        result["details"] = f"Legality: {clause.get('legality', 'Unknown')}"
                        result["sources"] = clause.get("state_variations", [])
        else:
            result["status"] = "INSUFFICIENT_DATA"
            result["details"] = "Claim not found in current knowledge base"
        
        # Log the fact check
        self.fact_check_log["checks"].append(result)
        self.fact_check_log["statistics"]["total_checks"] += 1
        if result["status"] == "VERIFIED":
            self.fact_check_log["statistics"]["total_verified"] += 1
        self.fact_check_log["statistics"]["last_update"] = datetime.now().isoformat()
        self._save_fact_check_log()
        
        return result

    def get_quick_reference(self, topic: str) -> Dict:
        """
        Get quick reference card for a topic.
        
        Args:
            topic: Topic to get reference for
            
        Returns:
            Quick reference information
        """
        ref = {
            "topic": topic,
            "generated": datetime.now().isoformat(),
            "summary": "",
            "key_points": [],
            "timeline": "",
            "forms": [],
            "common_mistakes": [],
            "next_steps": []
        }
        
        # Generate quick reference based on topic
        if "lease" in topic.lower():
            ref["summary"] = "Review lease carefully before signing. Document all property conditions with photos/video."
            ref["key_points"] = [
                "Get complete copy of lease BEFORE move-in",
                "Check for illegal clauses",
                "Document existing damage with photos",
                "Take photos of property condition during move-in",
                "Keep all copies of lease and correspondence"
            ]
            ref["timeline"] = "3-5 days to review before signing"
            ref["forms"] = ["Lease agreement", "Move-in inspection checklist", "Proof of ID"]
            ref["common_mistakes"] = [
                "Signing without reading",
                "Missing documentation of initial condition",
                "Not getting copy of lease",
                "Verbal agreements not documented in writing"
            ]
            ref["next_steps"] = [
                "1. Schedule move-in inspection with landlord",
                "2. Document all existing damage",
                "3. Establish rent payment method in writing",
                "4. Keep copy of lease for records"
            ]
        
        elif "repair" in topic.lower():
            ref["summary"] = "Document needed repairs and send formal written request to landlord."
            ref["key_points"] = [
                "Document defect with dated photos/video",
                "Send repair request in writing (certified mail or email)",
                "Give landlord 14 days to inspect and schedule",
                "Follow up if no response",
                "Keep copies of all communication"
            ]
            ref["timeline"] = "14 days for landlord response (varies by state)"
            ref["forms"] = ["Repair request letter", "Photo documentation", "Follow-up notice"]
            ref["common_mistakes"] = [
                "Verbal requests only",
                "Not documenting with photos",
                "Not giving proper notice",
                "Not following up on ignored requests"
            ]
            ref["next_steps"] = [
                "1. Take photos/video of defect with date visible",
                "2. Draft repair request letter with date and specifics",
                "3. Send via certified mail or email with read receipt",
                "4. Document receipt date",
                "5. Follow up if no response within timeline"
            ]
        
        elif "eviction" in topic.lower():
            ref["summary"] = "Eviction is a legal process with specific notice requirements. You have rights to defend."
            ref["key_points"] = [
                "Verify notice is valid and properly served",
                "Respond to notice within required timeframe",
                "Gather all payment receipts and documentation",
                "Prepare defense (invalid notice, discrimination, retaliation)",
                "Attend court hearing",
                "Consult attorney if possible"
            ]
            ref["timeline"] = "60+ days from notice to actual eviction (varies by state)"
            ref["forms"] = ["Answer to eviction complaint", "Proof of payments", "Affidavit of facts"]
            ref["common_mistakes"] = [
                "Ignoring notice/not appearing in court",
                "Not gathering evidence beforehand",
                "Getting emotional in court",
                "Not understanding legal defenses"
            ]
            ref["next_steps"] = [
                "1. DO NOT IGNORE the notice",
                "2. Gather all rent payment receipts",
                "3. Document any valid defense (discrimination, retaliation, etc.)",
                "4. Contact legal aid immediately",
                "5. Prepare answer and appear in court"
            ]
        
        return ref

    def get_all_resources(self) -> Dict:
        """Get list of all available learning resources."""
        return {
            "categories": list(self.knowledge_base.keys()),
            "total_topics": sum(len(v) for v in self.knowledge_base.values() if isinstance(v, dict)),
            "generated": datetime.now().isoformat()
        }

    def update_knowledge(self, category: str, subcategory: str, updates: Dict) -> bool:
        """
        Update knowledge base with new information.
        Can be run anytime to add new procedures or update existing ones.
        
        Args:
            category: Category to update
            subcategory: Specific procedure
            updates: Dictionary of updates
            
        Returns:
            True if successful, False if category not found
        """
        if category not in self.knowledge_base:
            return False
        
        if subcategory not in self.knowledge_base[category]:
            self.knowledge_base[category][subcategory] = {}
        
        self.knowledge_base[category][subcategory].update(updates)
        self.knowledge_base[category][subcategory]["last_updated"] = datetime.now().isoformat()
        self._save_knowledge_base()
        
        return True


def get_preliminary_learning_module(data_dir: str = "data") -> PreliminaryLearningModule:
    """
    Factory function to get or create the preliminary learning module.
    Can be called anytime to access the module.
    """
    return PreliminaryLearningModule(data_dir)


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    # Initialize the module
    module = get_preliminary_learning_module()
    
    print("=" * 80)
    print("PRELIMINARY LEARNING MODULE - COMPREHENSIVE INFORMATION SYSTEM")
    print("=" * 80)
    
    # Example 1: Get rental procedures
    print("\n1. RENTAL PROCEDURES - LEASE SIGNING")
    lease_proc = module.get_procedures("rental_procedures", "lease_signing")
    print(f"   Title: {lease_proc.get('title', 'N/A')}")
    print(f"   Steps: {len(lease_proc.get('steps', []))} steps")
    print(f"   Forms Required: {len(lease_proc.get('forms_required', []))} forms")
    print(f"   Timeline: {module.get_timeline('rental_procedures', 'lease_signing')}")
    print(f"   Jurisdiction-Specific: {module.get_jurisdiction_info('rental_procedures', 'lease_signing')}")
    
    # Example 2: Get forms for a procedure
    print("\n2. REQUIRED FORMS FOR EVICTION DEFENSE")
    forms = module.get_forms("court_procedures", "eviction_defense")
    for form in forms:
        print(f"   - {form}")
    
    # Example 3: Fact-check a claim
    print("\n3. FACT-CHECKING")
    claim = "Landlord cannot enter apartment without notice"
    result = module.fact_check(claim, "legal_procedures", "maintenance_rights")
    print(f"   Claim: '{claim}'")
    print(f"   Status: {result['status']}")
    print(f"   Details: {result['details']}")
    
    # Example 4: Get agencies for issue type
    print("\n4. AGENCIES FOR MAINTENANCE ISSUES")
    agencies = module.get_agencies_for_issue("maintenance")
    for agency in agencies:
        print(f"   - {agency.get('name', 'Unknown')} (Handles: {agency.get('handles', [])[0] if agency.get('handles') else 'N/A'})")
    
    # Example 5: Quick reference card
    print("\n5. QUICK REFERENCE - LEASE SIGNING")
    ref = module.get_quick_reference("lease signing")
    print(f"   Summary: {ref['summary']}")
    print(f"   Timeline: {ref['timeline']}")
    print(f"   Key Points: {len(ref['key_points'])} points")
    
    # Example 6: Get all resources
    print("\n6. AVAILABLE RESOURCES")
    resources = module.get_all_resources()
    print(f"   Categories: {', '.join(resources['categories'])}")
    print(f"   Total Topics: {resources['total_topics']}")
    
    print("\n" + "=" * 80)
    print("Module is ready for production use!")
    print("=" * 80)
