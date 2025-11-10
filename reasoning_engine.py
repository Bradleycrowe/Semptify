"""
Reasoning Engine - Connects all learning modules for intelligent analysis
Processes user situation through multiple learning engines to generate
smart recommendations and action plans.
"""

from learning_engine import get_learning
from preliminary_learning import get_preliminary_learning_module
from adaptive_intensity_engine import get_adaptive_intensity_engine
from curiosity_engine import get_curiosity
import json
from datetime import datetime


class ReasoningEngine:
    """
    Multi-layer reasoning system that processes user data through
    5 learning engines to generate intelligent insights and actions.

    Flow:
    1. LearningEngine - Analyzes patterns and user behavior
    2. PreliminaryLearning - Provides legal knowledge and facts
    3. AdaptiveIntensity - Determines response approach level
    4. CuriosityEngine - Identifies knowledge gaps and questions
    5. AdaptiveRegistration - Location-specific context

    Output: Structured reasoning with situation analysis and action plan
    """

    def __init__(self):
        self.learning = get_learning()
        self.preliminary = get_preliminary_learning_module()
        self.intensity = get_adaptive_intensity_engine()
        self.curiosity = get_curiosity()

    def analyze_situation(self, user_id: str, context: dict = None) -> dict:
        """
        Analyze user situation through all learning engines.

        Args:
            user_id: User identifier
            context: Additional context (location, issue_type, etc.)

        Returns:
            {
                "situation": {
                    "facts": [...],
                    "statistics": [...],
                    "legal_context": {...}
                },
                "analysis": {
                    "impact": "...",
                    "severity": "...",
                    "urgency": "..."
                },
                "actions": [
                    {
                        "priority": 1,
                        "action": "...",
                        "why": "...",
                        "how": "..."
                    }
                ],
                "intensity_level": "...",
                "questions": [...]
            }
        """
        context = context or {}

        # Step 1: Get behavior patterns (LearningEngine)
        patterns = self._get_user_patterns(user_id)

        # Step 2: Get legal knowledge (PreliminaryLearning)
        legal_context = self._get_legal_context(context)

        # Step 3: Determine intensity level (AdaptiveIntensity)
        intensity = self._get_intensity_level(user_id, context)

        # Step 4: Identify knowledge gaps (CuriosityEngine)
        questions = self._get_curiosity_questions(user_id, context)

        # Step 5: Location-specific context (AdaptiveRegistration)
        location_context = self._get_location_context(context)

        # Synthesize reasoning
        return self._synthesize_reasoning(
            patterns, legal_context, intensity,
            questions, location_context, context
        )

    def _get_user_patterns(self, user_id: str) -> dict:
        """Extract user behavior patterns."""
        try:
            interactions = self.learning.get_user_interactions(user_id)
            return {
                "interaction_count": len(interactions),
                "patterns": self.learning.analyze_patterns(user_id),
                "journey_stage": self.learning.get_journey_stage(user_id)
            }
        except:
            return {"interaction_count": 0, "patterns": {}, "journey_stage": "new"}

    def _get_legal_context(self, context: dict) -> dict:
        """Get relevant legal information."""
        issue_type = context.get("issue_type", "eviction")
        location = context.get("location", "general")

        # Get relevant info from preliminary learning
        procedures = self.preliminary.get_procedures(issue_type)
        forms = self.preliminary.get_forms(issue_type)
        agencies = self.preliminary.get_agencies_for_issue(issue_type)

        # Build facts from available data
        facts = []
        if procedures:
            facts.append(f"Procedure: {procedures.get('description', 'Available')}")
        if agencies:
            facts.extend([f"Contact: {agency.get('name')}" for agency in agencies[:2]])

        return {
            "facts": facts,
            "statistics": {},  # Will enhance later
            "rights": forms[:3] if forms else []  # Use forms as "rights" for now
        }

    def _get_intensity_level(self, user_id: str, context: dict) -> dict:
        """Determine appropriate response intensity."""
        situation_severity = context.get("severity", "medium")

        # Use determine_intensity method
        level_info = self.intensity.determine_intensity(user_id, context)

        return {
            "current": level_info.get("level", "positive_support"),
            "recommended": level_info.get("level", "positive_support"),
            "reason": level_info.get("reasoning", "Based on situation analysis")
        }

    def _get_curiosity_questions(self, user_id: str, context: dict) -> list:
        """Get questions system should research for user."""
        return self.curiosity.get_active_questions(user_id, context)

    def _get_location_context(self, context: dict) -> dict:
        """Get location-specific context."""
        location = context.get("location")
        if not location:
            return {}

        return {
            "jurisdiction": location,
            "local_resources": self.adaptive.get_local_resources(location),
            "court_info": self.adaptive.get_court_info(location)
        }

    def _synthesize_reasoning(
        self, patterns, legal_context, intensity,
        questions, location_context, original_context
    ) -> dict:
        """
        Synthesize all inputs into actionable intelligence.
        This is where the "smart" happens - connecting dots across modules.
        """

        # Build situation summary (Cell A data)
        situation = {
            "facts": legal_context.get("facts", []),
            "statistics": legal_context.get("statistics", {}),
            "your_rights": legal_context.get("rights", []),
            "journey_stage": patterns.get("journey_stage", "new")
        }

        # Analyze impact (Cell B preparation)
        analysis = self._analyze_impact(situation, intensity, patterns)

        # Generate prioritized actions (Cell B main content)
        actions = self._generate_actions(
            situation, analysis, intensity,
            location_context, original_context
        )

        # Package everything
        return {
            "situation": situation,
            "analysis": analysis,
            "actions": actions,
            "intensity_level": intensity.get("recommended"),
            "questions_researching": questions[:3],  # Top 3
            "location_context": location_context,
            "timestamp": datetime.now().isoformat()
        }

    def _analyze_impact(self, situation, intensity, patterns) -> dict:
        """Analyze how situation impacts user."""
        facts_count = len(situation.get("facts", []))
        rights_count = len(situation.get("your_rights", []))
        intensity_level = intensity.get("recommended", "medium")

        # Impact assessment
        if intensity_level in ["maximum", "firm"]:
            impact = "CRITICAL - Immediate action required to protect your rights"
            severity = "high"
            urgency = "immediate"
        elif intensity_level == "legal":
            impact = "SERIOUS - Legal protections available, take action soon"
            severity = "medium-high"
            urgency = "within 48 hours"
        else:
            impact = "MANAGEABLE - Stay informed and document everything"
            severity = "medium"
            urgency = "within 1 week"

        return {
            "impact_statement": impact,
            "severity": severity,
            "urgency": urgency,
            "facts_available": facts_count,
            "rights_available": rights_count,
            "recommended_approach": intensity_level
        }

    def _generate_actions(
        self, situation, analysis, intensity,
        location_context, context
    ) -> list:
        """
        Generate prioritized action plan based on reasoning.
        This is the "what to do" that goes in Cell B.
        """
        actions = []
        intensity_level = intensity.get("recommended", "medium")

        # Action 1: ALWAYS document
        actions.append({
            "priority": 1,
            "action": "Document Everything NOW",
            "why": "Evidence is your strongest protection. Photos, videos, texts, emails - save it all.",
            "how": "Use the Evidence Vault to store photos, documents, and communications.",
            "link": "/vault",
            "urgency": "immediate"
        })

        # Action 2: Know deadlines (if urgent)
        if analysis["urgency"] in ["immediate", "within 48 hours"]:
            actions.append({
                "priority": 2,
                "action": "Check Your Deadlines",
                "why": "Missing a court deadline can cost you your case.",
                "how": "Review the timeline to see all upcoming deadlines and court dates.",
                "link": "/calendar-timeline",
                "urgency": analysis["urgency"]
            })

        # Action 3: File appropriate forms (if legal/firm/maximum)
        if intensity_level in ["legal", "firm", "maximum"]:
            actions.append({
                "priority": 3,
                "action": "File the Right Legal Forms",
                "why": "You have legal protections - but you must file the paperwork to use them.",
                "how": "Use the complaint filing system to generate and submit the correct forms.",
                "link": "/complaint-filing",
                "urgency": "within 48 hours"
            })

        # Action 4: Know your rights (always)
        actions.append({
            "priority": 4,
            "action": "Study Your Tenant Rights",
            "why": f"You have {situation['your_rights'][:1] if situation.get('your_rights') else 'several'} specific rights in your situation.",
            "how": "Review the knowledge base for laws and protections specific to your case.",
            "link": "/knowledge-base",
            "urgency": "within 24 hours"
        })

        # Action 5: Track payments (if rent-related)
        if context.get("issue_type") in ["eviction", "rent", "payment"]:
            actions.append({
                "priority": 5,
                "action": "Track All Rent Payments",
                "why": "Proof of payment protects you from false claims.",
                "how": "Use the rent ledger to record every payment you've made.",
                "link": "/rent-ledger",
                "urgency": "within 1 week"
            })

        return actions

    def _explain_intensity(self, level: str, severity: str) -> str:
        """Explain why this intensity level is recommended."""
        explanations = {
            "working_together": "Your situation is manageable with cooperation.",
            "positive_support": "Proactive support will help resolve this positively.",
            "legal": "Legal protections are needed to defend your rights.",
            "firm": "Firm legal action is required to protect you.",
            "maximum": "Maximum legal intensity - this is serious and urgent."
        }
        return explanations.get(level, "Recommended based on situation analysis.")


# Global instance
_reasoning_engine = None

def get_reasoning_engine() -> ReasoningEngine:
    """Get or create global reasoning engine instance."""
    global _reasoning_engine
    if _reasoning_engine is None:
        _reasoning_engine = ReasoningEngine()
    return _reasoning_engine
