"""
PERSPECTIVE REASONING ENGINE
============================

Multi-angle document analysis: Same document, 4 different viewpoints.

Analyzes EVERY clause from:
- 👤 Tenant perspective (rights, risks, protections)
- 🏢 Landlord perspective (rights, obligations, enforceability)
- ⚖️ Legal perspective (validity, compliance, enforceability)
- 👨‍⚖️ Judge perspective (likely outcome, evidence needed, precedents)

The "little things" often determine who wins in court.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================

class Perspective(Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    LEGAL = "legal"
    JUDGE = "judge"

class ClauseImpact(Enum):
    FAVORABLE = "favorable"
    NEUTRAL = "neutral"
    UNFAVORABLE = "unfavorable"
    ILLEGAL = "illegal"

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ClauseAnalysis:
    """Analysis of a single clause from one perspective"""
    clause_text: str
    perspective: str
    impact: str  # ClauseImpact
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    score: float = 0.0  # -100 to +100 (negative=bad for this party, positive=good)

@dataclass
class PerspectiveInsight:
    """Complete perspective analysis of entire document"""
    perspective: str
    overall_score: float = 0.0  # -100 to +100
    favorable_clauses: List[str] = field(default_factory=list)
    unfavorable_clauses: List[str] = field(default_factory=list)
    illegal_clauses: List[str] = field(default_factory=list)
    key_strengths: List[str] = field(default_factory=list)
    key_weaknesses: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    win_probability: float = 0.0  # 0-100% chance of winning in court

@dataclass
class DocumentPerspectives:
    """All perspectives on a document"""
    tenant_view: PerspectiveInsight
    landlord_view: PerspectiveInsight
    legal_view: PerspectiveInsight
    judge_view: PerspectiveInsight
    
    # Comparative analysis
    tenant_advantage: float = 0.0  # -100 to +100 (who has upper hand?)
    likely_outcome: str = "uncertain"
    key_disputed_clauses: List[str] = field(default_factory=list)
    settlement_recommendation: Optional[str] = None

# ============================================================================
# PERSPECTIVE REASONING ENGINE
# ============================================================================

class PerspectiveReasoningEngine:
    """
    Multi-angle document analysis engine.
    
    Reads document holistically, then analyzes from 4 perspectives.
    Each perspective asks different questions about same content.
    """
    
    def __init__(self):
        # Tenant rights knowledge base
        self.tenant_rights = {
            "notice_requirements": {
                "entry": 24,  # hours
                "eviction": 30,  # days (varies by state)
                "rent_increase": 60  # days
            },
            "protected_rights": [
                "quiet enjoyment",
                "habitable premises",
                "privacy",
                "retaliation protection",
                "discrimination protection"
            ],
            "illegal_clauses": [
                "waive right to sue",
                "waive statutory rights",
                "unlimited landlord liability waiver",
                "automatic rent increases without notice",
                "entry without notice"
            ]
        }
        
        # Landlord rights knowledge base
        self.landlord_rights = {
            "protected_rights": [
                "collect rent",
                "inspect property",
                "evict for cause",
                "security deposit deductions",
                "enforce lease terms"
            ],
            "obligations": [
                "maintain habitable premises",
                "make repairs",
                "provide notice for entry",
                "return security deposit",
                "follow eviction procedures"
            ]
        }
        
        # Legal compliance knowledge
        self.legal_requirements = {
            "required_disclosures": [
                "lead paint (pre-1978 buildings)",
                "bedbug history",
                "mold",
                "security deposit terms"
            ],
            "unenforceable_clauses": [
                "tenant pays all repairs",
                "no refund of security deposit",
                "landlord not liable for anything",
                "tenant cannot have guests"
            ]
        }
    
    # ========================================================================
    # MAIN ANALYSIS
    # ========================================================================
    
    def analyze_document(self, document_intelligence) -> DocumentPerspectives:
        """
        Analyze document from all 4 perspectives.
        
        Args:
            document_intelligence: DocumentIntelligence object from document_intelligence.py
        
        Returns:
            DocumentPerspectives with all 4 viewpoints
        """
        # Analyze from each perspective
        tenant_view = self._analyze_tenant_perspective(document_intelligence)
        landlord_view = self._analyze_landlord_perspective(document_intelligence)
        legal_view = self._analyze_legal_perspective(document_intelligence)
        judge_view = self._analyze_judge_perspective(document_intelligence)
        
        # Comparative analysis
        tenant_advantage = tenant_view.overall_score - landlord_view.overall_score
        likely_outcome = self._predict_outcome(tenant_view, landlord_view, legal_view)
        disputed_clauses = self._find_disputed_clauses(tenant_view, landlord_view)
        settlement_rec = self._generate_settlement_recommendation(
            tenant_advantage, tenant_view, landlord_view
        )
        
        return DocumentPerspectives(
            tenant_view=tenant_view,
            landlord_view=landlord_view,
            legal_view=legal_view,
            judge_view=judge_view,
            tenant_advantage=tenant_advantage,
            likely_outcome=likely_outcome,
            key_disputed_clauses=disputed_clauses,
            settlement_recommendation=settlement_rec
        )
    
    # ========================================================================
    # TENANT PERSPECTIVE
    # ========================================================================
    
    def _analyze_tenant_perspective(self, intel) -> PerspectiveInsight:
        """Analyze from tenant's viewpoint: What are MY rights and risks?"""
        insight = PerspectiveInsight(perspective="tenant")
        
        # Check signatures (tenant signed under duress?)
        if intel.signatures:
            if len(intel.signatures) >= 2:
                insight.key_strengths.append("Document properly executed by all parties")
            else:
                insight.key_weaknesses.append("Missing signatures - validity questionable")
        
        # Check contract terms
        if intel.contract_terms:
            terms = intel.contract_terms
            
            # Rent amount
            if terms.rent_amount:
                insight.favorable_clauses.append(f"Rent clearly stated: ${terms.rent_amount}")
            else:
                insight.key_weaknesses.append("Rent amount not clear - dispute risk")
            
            # Security deposit
            if terms.security_deposit:
                if terms.security_deposit <= terms.rent_amount * 2:
                    insight.favorable_clauses.append(f"Security deposit reasonable: ${terms.security_deposit}")
                else:
                    insight.unfavorable_clauses.append(f"Security deposit excessive: ${terms.security_deposit}")
                    insight.key_weaknesses.append("Excessive deposit may violate state law")
            
            # Lease dates
            if terms.start_date and terms.end_date:
                insight.favorable_clauses.append("Lease term clearly defined")
            else:
                insight.unfavorable_clauses.append("Lease term unclear - could be month-to-month")
            
            # Utilities
            if terms.utilities_included:
                insight.favorable_clauses.append(f"Utilities included: {', '.join(terms.utilities_included)}")
            
            # Pets
            if terms.pets_allowed is True:
                insight.favorable_clauses.append("Pets allowed")
            elif terms.pets_allowed is False:
                insight.unfavorable_clauses.append("No pets allowed")
        
        # Check jurisdiction
        if intel.jurisdiction.state:
            insight.key_strengths.append(f"State law protections apply: {intel.jurisdiction.state}")
            
            # Check for arbitration clause
            if intel.jurisdiction.arbitration_clause:
                insight.unfavorable_clauses.append("Forced arbitration - limits right to sue")
                insight.key_weaknesses.append("May not be able to go to court")
                insight.action_items.append("Consult attorney about arbitration clause validity")
        
        # Check for illegal clauses
        text_lower = intel.full_text.lower()
        for illegal in self.tenant_rights["illegal_clauses"]:
            if illegal.lower() in text_lower:
                insight.illegal_clauses.append(f"Illegal clause: {illegal}")
                insight.key_strengths.append(f"Unenforceable clause found: {illegal}")
        
        # Check legal validation
        if intel.legal_validation:
            if intel.legal_validation.status.value in ["invalid", "incomplete"]:
                insight.key_strengths.append("Document has validity issues - may be unenforceable")
            
            for issue in intel.legal_validation.issues:
                insight.key_weaknesses.append(f"Legal issue: {issue}")
        
        # Calculate scores
        insight.overall_score = self._calculate_tenant_score(insight)
        insight.win_probability = max(0, min(100, 50 + (insight.overall_score / 2)))
        
        # Generate action items
        if not insight.action_items:
            if insight.overall_score < 0:
                insight.action_items.append("Consult with tenant rights attorney")
                insight.action_items.append("Document all communication with landlord")
            else:
                insight.action_items.append("Keep all receipts and documentation")
                insight.action_items.append("Take photos of property condition")
        
        return insight
    
    # ========================================================================
    # LANDLORD PERSPECTIVE
    # ========================================================================
    
    def _analyze_landlord_perspective(self, intel) -> PerspectiveInsight:
        """Analyze from landlord's viewpoint: How enforceable is this?"""
        insight = PerspectiveInsight(perspective="landlord")
        
        # Check signatures (is it binding?)
        if intel.signatures and len(intel.signatures) >= 2:
            insight.key_strengths.append("Binding agreement - all parties signed")
            insight.favorable_clauses.append("Properly executed contract")
        else:
            insight.key_weaknesses.append("Missing signatures - may not be enforceable")
        
        # Check contract terms
        if intel.contract_terms:
            terms = intel.contract_terms
            
            # Clear terms favor landlord
            if terms.rent_amount and terms.rent_due_day:
                insight.favorable_clauses.append("Rent terms clearly defined")
            
            if terms.late_fee:
                insight.favorable_clauses.append(f"Late fee provision: ${terms.late_fee}")
            
            if terms.security_deposit:
                insight.favorable_clauses.append(f"Security deposit authorized: ${terms.security_deposit}")
            
            # Lease duration
            if terms.start_date and terms.end_date:
                insight.favorable_clauses.append("Fixed term lease - tenant bound to term")
            else:
                insight.unfavorable_clauses.append("No fixed term - tenant can leave anytime")
        
        # Check jurisdiction
        if intel.jurisdiction.state:
            insight.key_strengths.append(f"Governed by {intel.jurisdiction.state} law")
        
        if intel.jurisdiction.arbitration_clause:
            insight.favorable_clauses.append("Arbitration clause reduces litigation risk")
        
        # Check for obligations
        if "maintain" in intel.full_text.lower() or "repair" in intel.full_text.lower():
            insight.key_weaknesses.append("Maintenance obligations may be extensive")
        
        # Legal validation
        if intel.legal_validation and intel.legal_validation.status.value == "valid":
            insight.key_strengths.append("Legally valid contract")
        else:
            insight.key_weaknesses.append("Validity issues may affect enforceability")
        
        # Calculate scores
        insight.overall_score = self._calculate_landlord_score(insight)
        insight.win_probability = max(0, min(100, 50 + (insight.overall_score / 2)))
        
        # Action items
        if insight.overall_score < 0:
            insight.action_items.append("Consult attorney about contract validity")
        
        return insight
    
    # ========================================================================
    # LEGAL PERSPECTIVE
    # ========================================================================
    
    def _analyze_legal_perspective(self, intel) -> PerspectiveInsight:
        """Analyze from legal viewpoint: Is this valid and enforceable?"""
        insight = PerspectiveInsight(perspective="legal")
        
        # Signature requirements
        if intel.legal_validation:
            if intel.legal_validation.all_parties_signed:
                insight.favorable_clauses.append("All required parties signed")
            else:
                insight.illegal_clauses.append("Missing required signatures")
            
            if intel.legal_validation.has_legal_language:
                insight.favorable_clauses.append("Contains proper legal language")
            
            for issue in intel.legal_validation.issues:
                insight.illegal_clauses.append(issue)
            
            for warning in intel.legal_validation.warnings:
                insight.unfavorable_clauses.append(warning)
        
        # Check for illegal clauses
        text_lower = intel.full_text.lower()
        
        for illegal in self.legal_requirements["unenforceable_clauses"]:
            if illegal.lower() in text_lower:
                insight.illegal_clauses.append(f"Unenforceable: {illegal}")
        
        # Jurisdiction requirements
        if not intel.jurisdiction.state:
            insight.unfavorable_clauses.append("No jurisdiction specified - may cause disputes")
        
        if not intel.jurisdiction.governing_law:
            insight.unfavorable_clauses.append("No governing law clause")
        
        # Required disclosures (context dependent)
        if intel.doc_type == "lease":
            for disclosure in self.legal_requirements["required_disclosures"]:
                if disclosure.lower() not in text_lower:
                    insight.unfavorable_clauses.append(f"Missing required disclosure: {disclosure}")
        
        # Calculate enforceability score
        total_clauses = (len(insight.favorable_clauses) + 
                        len(insight.unfavorable_clauses) + 
                        len(insight.illegal_clauses))
        
        if total_clauses > 0:
            enforceability = ((len(insight.favorable_clauses) - 
                             len(insight.illegal_clauses) * 2) / total_clauses) * 100
            insight.overall_score = enforceability
        
        # Summary
        if len(insight.illegal_clauses) > 0:
            insight.key_weaknesses.append(f"{len(insight.illegal_clauses)} unenforceable clauses found")
        
        if len(insight.illegal_clauses) == 0 and len(insight.unfavorable_clauses) <= 2:
            insight.key_strengths.append("Document is legally sound")
        
        return insight
    
    # ========================================================================
    # JUDGE PERSPECTIVE
    # ========================================================================
    
    def _analyze_judge_perspective(self, intel) -> PerspectiveInsight:
        """Analyze from judge's viewpoint: How would court rule?"""
        insight = PerspectiveInsight(perspective="judge")
        
        # Evaluate evidence quality
        if intel.signatures:
            insight.key_strengths.append("Signed document - strong evidence")
            
            for sig in intel.signatures:
                if sig.is_notarized:
                    insight.key_strengths.append("Notarized signature - high credibility")
                if sig.is_witnessed:
                    insight.key_strengths.append("Witnessed signature - additional credibility")
        
        # Contract clarity
        if intel.contract_terms:
            terms = intel.contract_terms
            clarity_score = 0
            
            if terms.rent_amount:
                clarity_score += 20
            if terms.start_date and terms.end_date:
                clarity_score += 20
            if terms.security_deposit:
                clarity_score += 15
            if intel.jurisdiction.state:
                clarity_score += 25
            if len(intel.contacts) >= 2:
                clarity_score += 20
            
            if clarity_score >= 80:
                insight.favorable_clauses.append("Clear, unambiguous terms")
            elif clarity_score >= 50:
                insight.unfavorable_clauses.append("Some ambiguous terms - may require interpretation")
            else:
                insight.unfavorable_clauses.append("Vague terms - significant interpretation needed")
        
        # Legal compliance
        if intel.legal_validation:
            if intel.legal_validation.status.value == "valid":
                insight.favorable_clauses.append("Meets legal requirements")
            else:
                insight.unfavorable_clauses.append("Legal validity concerns")
        
        # Likely ruling
        if len(insight.key_strengths) > len(insight.unfavorable_clauses):
            insight.key_strengths.append("Court likely to enforce as written")
            insight.overall_score = 60
        elif len(insight.unfavorable_clauses) > len(insight.key_strengths):
            insight.key_weaknesses.append("Court may not enforce - validity issues")
            insight.overall_score = 30
        else:
            insight.key_weaknesses.append("Outcome uncertain - depends on specific circumstances")
            insight.overall_score = 50
        
        # Evidence recommendations
        insight.action_items.append("Preserve original signed document")
        if intel.contract_terms and intel.contract_terms.rent_amount:
            insight.action_items.append("Keep all payment records")
        
        return insight
    
    # ========================================================================
    # COMPARATIVE ANALYSIS
    # ========================================================================
    
    def _calculate_tenant_score(self, insight: PerspectiveInsight) -> float:
        """Calculate overall score for tenant position"""
        score = 0.0
        
        score += len(insight.favorable_clauses) * 10
        score -= len(insight.unfavorable_clauses) * 10
        score += len(insight.illegal_clauses) * 15  # Illegal clauses help tenant!
        score += len(insight.key_strengths) * 5
        score -= len(insight.key_weaknesses) * 5
        
        return max(-100, min(100, score))
    
    def _calculate_landlord_score(self, insight: PerspectiveInsight) -> float:
        """Calculate overall score for landlord position"""
        score = 0.0
        
        score += len(insight.favorable_clauses) * 10
        score -= len(insight.unfavorable_clauses) * 10
        score -= len(insight.illegal_clauses) * 15  # Illegal clauses hurt landlord!
        score += len(insight.key_strengths) * 5
        score -= len(insight.key_weaknesses) * 5
        
        return max(-100, min(100, score))
    
    def _predict_outcome(self, tenant_view, landlord_view, legal_view) -> str:
        """Predict likely court outcome"""
        tenant_score = tenant_view.overall_score
        landlord_score = landlord_view.overall_score
        legal_score = legal_view.overall_score
        
        # If document is invalid, nobody wins
        if legal_score < 30:
            return "Document validity in question - may be dismissed"
        
        # Strong tenant position
        if tenant_score > landlord_score + 30:
            return "Tenant likely to prevail"
        
        # Strong landlord position
        if landlord_score > tenant_score + 30:
            return "Landlord likely to prevail"
        
        # Close call
        if abs(tenant_score - landlord_score) < 20:
            return "Outcome uncertain - depends on additional evidence"
        
        # Slight advantage
        if tenant_score > landlord_score:
            return "Slight advantage to tenant"
        else:
            return "Slight advantage to landlord"
    
    def _find_disputed_clauses(self, tenant_view, landlord_view) -> List[str]:
        """Find clauses where perspectives differ significantly"""
        disputed = []
        
        # Clauses tenant likes but landlord doesn't
        for clause in tenant_view.favorable_clauses:
            if clause in landlord_view.unfavorable_clauses:
                disputed.append(f"DISPUTED: {clause}")
        
        # Clauses landlord likes but tenant doesn't
        for clause in landlord_view.favorable_clauses:
            if clause in tenant_view.unfavorable_clauses:
                disputed.append(f"DISPUTED: {clause}")
        
        return disputed[:5]  # Top 5 most disputed
    
    def _generate_settlement_recommendation(
        self, 
        tenant_advantage: float, 
        tenant_view, 
        landlord_view
    ) -> str:
        """Generate settlement recommendation based on analysis"""
        if abs(tenant_advantage) < 20:
            return "Settlement recommended - outcome uncertain, high litigation risk for both sides"
        elif tenant_advantage > 50:
            return "Tenant has strong position - landlord should consider settlement to avoid loss"
        elif tenant_advantage < -50:
            return "Landlord has strong position - tenant should consider settlement to avoid loss"
        elif tenant_advantage > 0:
            return "Tenant has advantage but outcome not certain - settlement could benefit both"
        else:
            return "Landlord has advantage but outcome not certain - settlement could benefit both"

# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def analyze_perspectives(document_intelligence) -> DocumentPerspectives:
    """Analyze document from all 4 perspectives"""
    engine = PerspectiveReasoningEngine()
    return engine.analyze_document(document_intelligence)

# ============================================================================
# MAIN - Testing
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  🎭 PERSPECTIVE REASONING ENGINE")
    print("=" * 70)
    print()
    print("Multi-angle document analysis:")
    print("  • Tenant perspective (rights & risks)")
    print("  • Landlord perspective (enforceability)")
    print("  • Legal perspective (validity)")
    print("  • Judge perspective (likely outcome)")
    print()
    print("Ready to analyze documents from all angles!")
    print()
