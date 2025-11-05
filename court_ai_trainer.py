"""
Court AI Training Module - Trains AI for courtroom procedures, clerk duties & legal protocols

This module provides:
1. Document validation against court rules
2. Timeline/deadline compliance checking
3. Evidence quality assessment
4. Case strength prediction based on facts
5. AI training data and prompts for various LLM providers
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import hashlib


# ============================================================================
# Data Structures for Court Training
# ============================================================================

@dataclass
class CourtDocument:
    """Represents a court document for validation."""
    doc_type: str  # complaint, answer, motion, affidavit, etc.
    case_type: str  # eviction, debt, small-claims, etc.
    filed_date: str
    response_due_date: Optional[str] = None
    filing_fee_paid: bool = False
    signature_present: bool = False
    notarized: bool = False
    service_documented: bool = False
    has_table_of_contents: bool = False


@dataclass
class CourtEvidence:
    """Represents evidence for admissibility assessment."""
    evidence_type: str  # photo, video, document, testimony, email, etc.
    description: str
    collection_date: str
    collected_by: str
    gps_coordinates: Optional[str] = None
    timestamp_visible: bool = False
    authenticated: bool = False
    chain_of_custody_documented: bool = False
    is_original: bool = False
    quality_score: float = 0.0  # 0-1 scale


@dataclass
class EvictionCase:
    """Represents an eviction case for strength prediction."""
    case_id: str
    case_type: str  # non-payment, lease-violation, end-of-lease, etc.
    landlord_defects: List[str] = None  # formatting errors, service failures, etc.
    tenant_defenses: List[str] = None  # habitability, retaliation, discrimination, etc.
    evidence_strength: float = 0.5  # 0-1 scale
    landlord_win_probability: float = 0.5  # 0-1 scale


# ============================================================================
# Court Rules Database (State-Specific)
# ============================================================================

COURT_RULES = {
    "federal": {
        "response_deadline_days": 20,
        "notice_requirement_days": 7,
        "font_size_min": 12,
        "margin_min_inches": 1.0,
        "page_limit": None,  # No limit for federal
        "filing_fee_required": True,
        "notarization_required": False,
    },
    "state_default": {
        "response_deadline_days": 20,
        "notice_requirement_days": 7,
        "font_size_min": 11,
        "margin_min_inches": 0.75,
        "page_limit": None,
        "filing_fee_required": True,
        "notarization_required": False,
    },
    "small_claims": {
        "response_deadline_days": 20,
        "notice_requirement_days": 7,
        "font_size_min": 10,
        "margin_min_inches": 0.5,
        "page_limit": None,
        "filing_fee_required": True,
        "notarization_required": False,
    },
    "MN": {  # Minnesota specific
        "response_deadline_days": 20,
        "notice_requirement_days": 7,
        "font_size_min": 11,
        "margin_min_inches": 1.0,
        "page_limit": None,
        "filing_fee_required": True,
        "notarization_required": True,  # MN requires notarization for affidavits
        "eviction_notice_days": 30,  # Notice to Quit: 30 days
    },
    "NY": {  # New York specific
        "response_deadline_days": 30,  # NY allows 30 days to respond (CPLR § 213)
        "notice_requirement_days": 3,  # 3-day notice to cure for non-payment
        "font_size_min": 11,
        "margin_min_inches": 1.0,
        "page_limit": None,
        "filing_fee_required": True,
        "notarization_required": False,  # NY does not require notarization for filings
        "eviction_notice_days": 30,  # Notice to Quit: 30 days minimum
        "pre_litigation_notice_days": 10,  # 10-day demand notice before eviction
        "answer_deadline_days": 5,  # Answer must be filed within 5 days of service
        "court_type": "Civil Court or Supreme Court (depending on amount)",
        "small_claims_limit": 5000,  # Small claims limit in NY
        "marshal_fee_required": True,  # Marshal/sheriff fee for eviction
        "specials_allowed": True,  # Can claim special damages (excess rent)
        "habitability_threshold": "Substantial breach affecting health/safety",  # NY standard
    }
}

EVIDENCE_RULES = {
    "photo": {
        "requires_authentication": True,
        "requires_timestamp": True,
        "requires_location": False,  # Recommended but not required
        "requires_chain_of_custody": True,
        "admissibility_score": 0.9,  # Very admissible if authenticated
    },
    "video": {
        "requires_authentication": True,
        "requires_timestamp": True,
        "requires_location": False,
        "requires_chain_of_custody": True,
        "admissibility_score": 0.95,  # Highest evidence strength
    },
    "document": {
        "requires_authentication": True,
        "requires_timestamp": False,
        "requires_location": False,
        "requires_chain_of_custody": False,
        "admissibility_score": 0.8,  # Medium-high, depends on content
    },
    "email": {
        "requires_authentication": True,
        "requires_timestamp": True,  # Must show full header
        "requires_location": False,
        "requires_chain_of_custody": False,
        "admissibility_score": 0.75,  # Medium, hearsay concerns possible
    },
    "text_message": {
        "requires_authentication": True,
        "requires_timestamp": True,
        "requires_location": False,
        "requires_chain_of_custody": False,
        "admissibility_score": 0.7,  # Medium, hearsay concerns
    },
    "testimony": {
        "requires_authentication": True,  # Under oath
        "requires_timestamp": False,
        "requires_location": False,
        "requires_chain_of_custody": False,
        "admissibility_score": 0.85,  # High if credible witness
    },
}

# ============================================================================
# Document Validator
# ============================================================================

class DocumentValidator:
    """Validates court documents for compliance with rules."""
    
    def __init__(self, court_type: str = "state_default", state: str = "MN"):
        self.rules = COURT_RULES.get(state, COURT_RULES.get(court_type, COURT_RULES["state_default"]))
    
    def validate_document(self, doc: CourtDocument) -> Dict:
        """Validate a court document and return compliance report."""
        issues = []
        warnings = []
        
        # Check basic requirements
        if not doc.signature_present:
            issues.append("Document missing signature - CRITICAL: Document will be rejected")
        
        if self.rules.get("notarization_required") and not doc.notarized:
            issues.append("Document requires notarization per court rules - CRITICAL: Will be rejected")
        
        if not doc.filing_fee_paid:
            issues.append("Filing fee not paid - Document will be rejected")
        
        if not doc.service_documented:
            warnings.append("Service of defendant not documented - Response deadline may not start")
        
        # Check formatting recommendations
        if doc.doc_type == "complaint" and not doc.has_table_of_contents:
            warnings.append("Complaint should include table of contents for complex cases")
        
        # Calculate response deadline if not provided
        if doc.response_due_date is None and doc.filed_date:
            deadline = self._calculate_response_deadline(doc.filed_date)
            return {
                "is_compliant": len(issues) == 0,
                "issues": issues,
                "warnings": warnings,
                "calculated_response_deadline": deadline,
                "compliance_score": self._calculate_compliance_score(issues),
            }
        
        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "compliance_score": self._calculate_compliance_score(issues),
        }
    
    def _calculate_response_deadline(self, filed_date: str) -> str:
        """Calculate when response is due."""
        try:
            date = datetime.strptime(filed_date, "%Y-%m-%d")
            deadline = date + timedelta(days=self.rules["response_deadline_days"])
            return deadline.strftime("%Y-%m-%d")
        except:
            return "Unable to calculate"
    
    def _calculate_compliance_score(self, issues: List[str]) -> float:
        """Calculate compliance score (0-1)."""
        if not issues:
            return 1.0
        return max(0.0, 1.0 - (len(issues) * 0.25))


# ============================================================================
# Evidence Assessor
# ============================================================================

class EvidenceAssessor:
    """Assesses evidence quality and admissibility."""
    
    def assess_evidence(self, evidence: CourtEvidence) -> Dict:
        """Assess evidence for admissibility and quality."""
        rules = EVIDENCE_RULES.get(evidence.evidence_type, {})
        issues = []
        
        # Check authentication
        if rules.get("requires_authentication") and not evidence.authenticated:
            issues.append(f"Evidence not authenticated - {evidence.evidence_type} requires witness to verify")
        
        # Check timestamp
        if rules.get("requires_timestamp") and not evidence.timestamp_visible:
            issues.append(f"No visible timestamp - {evidence.evidence_type} should show date/time")
        
        # Check chain of custody
        if rules.get("requires_chain_of_custody") and not evidence.chain_of_custody_documented:
            issues.append("Chain of custody not documented - Evidence admissibility questionable")
        
        # Calculate admissibility score
        base_score = rules.get("admissibility_score", 0.5)
        penalty = len(issues) * 0.15
        final_score = max(0.0, base_score - penalty)
        
        return {
            "evidence_type": evidence.evidence_type,
            "is_admissible": final_score > 0.6,
            "admissibility_score": final_score,
            "issues": issues,
            "recommendation": self._get_recommendation(final_score, issues),
            "next_steps": self._get_next_steps(evidence, issues),
        }
    
    def _get_recommendation(self, score: float, issues: List[str]) -> str:
        """Get recommendation based on score."""
        if score > 0.8:
            return "STRONG EVIDENCE - Highly admissible in court"
        elif score > 0.6:
            return "ACCEPTABLE EVIDENCE - Should be admitted with proper authentication"
        elif score > 0.4:
            return "WEAK EVIDENCE - May be challenged; needs supplementation"
        else:
            return "INADMISSIBLE - Likely to be excluded; major issues present"
    
    def _get_next_steps(self, evidence: CourtEvidence, issues: List[str]) -> List[str]:
        """Get specific next steps to improve evidence."""
        steps = []
        if not evidence.authenticated:
            steps.append("Get witness statement/affidavit authenticating the evidence")
        if not evidence.timestamp_visible:
            steps.append("Provide date/time evidence was collected")
        if not evidence.chain_of_custody_documented:
            steps.append("Document who collected, stored, and handled evidence")
        if evidence.quality_score < 0.7:
            steps.append("Consider recollecting or supplementing with higher quality evidence")
        return steps


# ============================================================================
# Case Strength Predictor
# ============================================================================

class CaseStrengthPredictor:
    """Predicts case strength based on facts and evidence."""
    
    def predict_eviction_case(self, case: EvictionCase) -> Dict:
        """Predict eviction case outcome."""
        
        # Landlord score factors
        landlord_score = 0.5  # Start at neutral
        
        # Deduct for landlord defects
        if case.landlord_defects:
            defect_penalties = {
                "no_proper_service": -0.15,
                "no_proof_of_service": -0.20,
                "formatting_errors": -0.05,
                "no_valid_notice": -0.25,
                "improper_jurisdiction": -0.30,
                "wrong_court": -0.30,
            }
            for defect in case.landlord_defects:
                landlord_score += defect_penalties.get(defect, -0.10)
        
        # Tenant score factors
        tenant_score = 0.5  # Start at neutral
        
        # Add for strong defenses
        if case.tenant_defenses:
            defense_bonuses = {
                "habitability_violation": 0.25,
                "retaliation": 0.30,
                "discrimination": 0.35,
                "improper_notice": 0.20,
                "partial_payment_accepted": 0.15,
            }
            for defense in case.tenant_defenses:
                tenant_score += defense_bonuses.get(defense, 0.05)
        
        # Factor in evidence strength
        landlord_score = landlord_score * (1 + (case.evidence_strength * 0.2))
        tenant_score = tenant_score * (1 + ((1 - case.evidence_strength) * 0.2))
        
        # Normalize to 0-1 range
        total = landlord_score + tenant_score
        if total > 0:
            landlord_prob = landlord_score / total
        else:
            landlord_prob = 0.5
        
        tenant_prob = 1 - landlord_prob
        
        return {
            "case_type": case.case_type,
            "landlord_win_probability": min(1.0, max(0.0, landlord_prob)),
            "tenant_win_probability": min(1.0, max(0.0, tenant_prob)),
            "strength": self._strength_assessment(landlord_prob),
            "landlord_defects": case.landlord_defects,
            "tenant_defenses": case.tenant_defenses,
            "key_issues": self._identify_key_issues(case),
            "recommendations": self._generate_recommendations(case, landlord_prob),
        }
    
    def _strength_assessment(self, landlord_prob: float) -> str:
        """Assess case strength."""
        if landlord_prob > 0.8:
            return "VERY STRONG for landlord"
        elif landlord_prob > 0.6:
            return "STRONG for landlord"
        elif landlord_prob > 0.4:
            return "MODERATE for landlord"
        elif landlord_prob > 0.2:
            return "STRONG for tenant"
        else:
            return "VERY STRONG for tenant"
    
    def _identify_key_issues(self, case: EvictionCase) -> List[str]:
        """Identify key issues in the case."""
        issues = []
        if case.landlord_defects:
            issues.append(f"Landlord has {len(case.landlord_defects)} procedural issues")
        if case.tenant_defenses:
            issues.append(f"Tenant has {len(case.tenant_defenses)} viable defenses")
        return issues
    
    def _generate_recommendations(self, case: EvictionCase, landlord_prob: float) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        if landlord_prob < 0.3:
            recommendations.append("Strong case for tenant - Consider defense and potential counterclaim")
            recommendations.append("Focus on documenting all defenses with evidence")
        elif landlord_prob > 0.7:
            recommendations.append("Case strongly favors landlord - Consider settlement/move")
            recommendations.append("If tenant, file counterclaim for habitability violations if applicable")
        else:
            recommendations.append("Case is competitive - Evidence quality will determine outcome")
            recommendations.append("Collect and organize all relevant evidence immediately")
        
        return recommendations


# ============================================================================
# AI Training Prompt Generator
# ============================================================================

class AITrainingPromptGenerator:
    """Generates training prompts for AI/LLM providers."""
    
    @staticmethod
    def generate_court_clerk_system_prompt(state: str = "MN") -> str:
        """Generate system prompt for training AI as court clerk."""
        rules = COURT_RULES.get(state, COURT_RULES["state_default"])
        
        return f"""You are an expert AI Court Clerk Assistant for {state} courts. Your role:

PRIMARY RESPONSIBILITIES:
1. Validate all documents for compliance with {state} court rules
2. Track deadlines and alert when responses are due
3. Assess evidence admissibility based on rules of evidence
4. Provide timeline guidance (filing deadlines, notice periods)
5. Flag potential issues in case submissions before they reach court
6. Predict case outcomes based on evidence strength

COURT RULES FOR {state}:
- Response deadline: {rules.get('response_deadline_days', 20)} days
- Notice requirement: {rules.get('notice_requirement_days', 7)} days
- Minimum font size: {rules.get('font_size_min', 11)}pt
- Minimum margins: {rules.get('margin_min_inches', 1.0)} inches
- Filing fee required: {rules.get('filing_fee_required', True)}
- Notarization required: {rules.get('notarization_required', False)}

EVIDENCE STANDARDS:
- Photos: Require timestamp, authentication, chain of custody
- Videos: Highest evidence strength; must show authenticity
- Documents: Require notarization if affidavit; originals preferred
- Emails/Texts: Require full headers, authentication, reliability

Your goal: Help parties submit compliant documents and strong evidence."""
    
    @staticmethod
    def generate_evidence_validation_prompt(evidence: CourtEvidence) -> str:
        """Generate prompt for validating specific evidence."""
        return f"""Analyze this evidence for court admissibility:

EVIDENCE TYPE: {evidence.evidence_type}
DESCRIPTION: {evidence.description}
COLLECTED: {evidence.collection_date} by {evidence.collected_by}

METADATA:
- GPS coordinates: {evidence.gps_coordinates or 'Not present'}
- Timestamp visible: {evidence.timestamp_visible}
- Authenticated: {evidence.authenticated}
- Chain of custody documented: {evidence.chain_of_custody_documented}
- Original document: {evidence.is_original}

ASSESSMENT NEEDED:
1. Is this evidence admissible in court?
2. What are the strengths/weaknesses?
3. What documentation is needed?
4. How strong is it as evidence (0-100)?
5. What specific improvements would strengthen it?

Provide actionable recommendations."""
    
    @staticmethod
    def generate_case_analysis_prompt(case: EvictionCase) -> str:
        """Generate prompt for analyzing case strength."""
        return f"""Analyze this eviction case and predict outcome:

CASE ID: {case.case_id}
CASE TYPE: {case.case_type}

LANDLORD'S ISSUES (if any):
{json.dumps(case.landlord_defects or [], indent=2)}

TENANT'S DEFENSES (if any):
{json.dumps(case.tenant_defenses or [], indent=2)}

EVIDENCE STRENGTH: {case.evidence_strength * 100:.0f}%

ANALYSIS NEEDED:
1. What is the likely outcome? (landlord % vs tenant %)
2. Which side has stronger legal position?
3. What are the critical issues?
4. What evidence would strengthen each side?
5. What are realistic settlement ranges?
6. What are the next recommended steps?

Consider Minnesota eviction law and local court practices."""


# ============================================================================
# Training Data Repository
# ============================================================================

class TrainingDataRepository:
    """Stores and retrieves training data for AI models."""
    
    def __init__(self, json_file: str = "data/court_training_data.json"):
        self.json_file = json_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load training data from JSON."""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except:
            return self._initialize_data()
    
    def _initialize_data(self) -> Dict:
        """Initialize default training data."""
        return {
            "eviction_cases": [],
            "documents": [],
            "evidence_samples": [],
            "common_defects": [],
            "defense_strategies": [],
        }
    
    def add_case(self, case: EvictionCase) -> None:
        """Add case to training repository."""
        self.data["eviction_cases"].append(asdict(case))
        self._save_data()
    
    def add_document(self, doc: CourtDocument, validation: Dict) -> None:
        """Add document and validation result."""
        entry = {
            "document": asdict(doc),
            "validation": validation,
            "timestamp": datetime.now().isoformat(),
        }
        self.data["documents"].append(entry)
        self._save_data()
    
    def add_evidence(self, evidence: CourtEvidence, assessment: Dict) -> None:
        """Add evidence and assessment."""
        entry = {
            "evidence": asdict(evidence),
            "assessment": assessment,
            "timestamp": datetime.now().isoformat(),
        }
        self.data["evidence_samples"].append(entry)
        self._save_data()
    
    def _save_data(self) -> None:
        """Save training data to JSON."""
        try:
            with open(self.json_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving training data: {e}")
    
    def get_similar_cases(self, case_type: str, limit: int = 5) -> List[Dict]:
        """Get similar cases for precedent."""
        similar = [c for c in self.data["eviction_cases"] if c.get("case_type") == case_type]
        return similar[:limit]


# ============================================================================
# Integrated Court AI Trainer (Main Interface)
# ============================================================================

class CourtAITrainer:
    """Main interface for court AI training."""
    
    def __init__(self, state: str = "MN"):
        self.state = state
        self.validator = DocumentValidator(state=state)
        self.assessor = EvidenceAssessor()
        self.predictor = CaseStrengthPredictor()
        self.repository = TrainingDataRepository()
    
    def analyze_submission(self, doc: CourtDocument, evidence_list: List[CourtEvidence]) -> Dict:
        """Comprehensive analysis of court submission."""
        
        # Validate document
        doc_validation = self.validator.validate_document(doc)
        
        # Assess all evidence
        evidence_assessments = [self.assessor.assess_evidence(e) for e in evidence_list]
        
        # Calculate overall strength
        avg_evidence_score = sum(e["admissibility_score"] for e in evidence_assessments) / len(evidence_assessments) if evidence_assessments else 0.5
        
        return {
            "submission_type": doc.doc_type,
            "document_compliance": doc_validation,
            "evidence_assessments": evidence_assessments,
            "average_evidence_strength": avg_evidence_score,
            "overall_readiness": self._calculate_readiness(doc_validation, evidence_assessments),
            "recommendations": self._generate_submission_recommendations(doc_validation, evidence_assessments),
        }
    
    def _calculate_readiness(self, doc_validation: Dict, evidence_assessments: List[Dict]) -> str:
        """Calculate readiness for court submission."""
        if not doc_validation["is_compliant"]:
            return "NOT READY - Fix document compliance issues first"
        
        if not evidence_assessments:
            return "NOT READY - No evidence submitted"
        
        avg_score = sum(e["admissibility_score"] for e in evidence_assessments) / len(evidence_assessments)
        
        if avg_score > 0.8:
            return "READY FOR COURT - Strong submission"
        elif avg_score > 0.6:
            return "MOSTLY READY - Minor improvements recommended"
        else:
            return "NOT READY - Evidence quality insufficient"
    
    def _generate_submission_recommendations(self, doc_validation: Dict, evidence_assessments: List[Dict]) -> List[str]:
        """Generate recommendations for submission."""
        recs = []
        recs.extend(doc_validation.get("warnings", []))
        
        for evidence_assessment in evidence_assessments:
            recs.extend(evidence_assessment.get("next_steps", []))
        
        return recs


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Create trainer
    trainer = CourtAITrainer(state="MN")
    
    # Example: Validate a court document
    doc = CourtDocument(
        doc_type="answer",
        case_type="eviction",
        filed_date="2025-11-05",
        signature_present=True,
        notarized=True,
        filing_fee_paid=True,
        service_documented=True,
    )
    
    # Example: Assess evidence
    evidence = CourtEvidence(
        evidence_type="photo",
        description="Mold damage in bathroom",
        collection_date="2025-11-04",
        collected_by="tenant",
        timestamp_visible=True,
        authenticated=True,
        chain_of_custody_documented=True,
        is_original=True,
        quality_score=0.95,
    )
    
    # Analyze submission
    analysis = trainer.analyze_submission(doc, [evidence])
    print(json.dumps(analysis, indent=2))
    
    # Generate AI training prompt
    prompt = AITrainingPromptGenerator.generate_court_clerk_system_prompt(state="MN")
    print("\n" + prompt)
