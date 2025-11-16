"""
Tenant Journey System for Semptify
Maps the complete tenant experience and applies intelligence at each stage.
Integrates: learning_engine, curiosity_engine, intelligence_engine, jurisdiction_engine
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import all intelligence systems
from engines.learning_engine import get_learning
from engines.curiosity_engine import get_curiosity
from engines.intelligence_engine import get_intelligence
from engines.jurisdiction_engine import get_jurisdiction


class TenantJourney:
    """
    Tracks tenant's journey from search to move-out.
    Applies learning and intelligence at each stage.
    """

    JOURNEY_STAGES = [
        "searching",      # Looking for apartment
        "applying",       # Submitted application
        "screening",      # Landlord reviewing
        "approved",       # Application approved
        "signing",        # Reviewing/signing lease
        "moving_in",      # Move-in inspection, deposits
        "living",         # Day-to-day tenancy
        "issue",          # Problem arises
        "resolving",      # Working on resolution
        "moving_out",     # End of tenancy
        "dispute",        # Post-move-out dispute
        "closed"          # Journey complete
    ]

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.journeys_file = os.path.join(data_dir, "tenant_journeys.json")
        self.journeys = self._load_journeys()

        # Load intelligence systems
        self.learning = get_learning()
        self.curiosity = get_curiosity()
        self.intelligence = get_intelligence()
        self.jurisdiction = get_jurisdiction()

    def _load_journeys(self) -> Dict:
        """Load tenant journey data."""
        if os.path.exists(self.journeys_file):
            try:
                with open(self.journeys_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_journeys(self):
        """Persist journey data."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.journeys_file, 'w') as f:
            json.dump(self.journeys, f, indent=2)

    # ========================================================================
    # JOURNEY TRACKING
    # ========================================================================

    def start_journey(
        self,
        user_id: str,
        location: Dict[str, str],
        context: Dict[str, Any] = None
    ) -> Dict:
        """
        Start tracking a tenant's journey.
        Returns: Journey ID and initial guidance
        """
        journey_id = f"journey_{user_id}_{int(datetime.now().timestamp())}"

        journey = {
            "id": journey_id,
            "user_id": user_id,
            "stage": "searching",
            "location": location,
            "context": context or {},
            "timeline": [{
                "stage": "searching",
                "timestamp": datetime.now().isoformat(),
                "notes": "Journey started"
            }],
            "learned_data": {},  # What we learn from this journey
            "warnings": [],
            "guidance": []
        }

        self.journeys[journey_id] = journey
        self._save_journeys()

        # Get initial guidance
        guidance = self.get_stage_guidance(journey_id, "searching")

        return {
            "journey_id": journey_id,
            "stage": "searching",
            "guidance": guidance
        }

    def advance_stage(
        self,
        journey_id: str,
        new_stage: str,
        data: Dict[str, Any] = None
    ) -> Dict:
        """
        Move tenant to next journey stage.
        Learns from data provided and gives new guidance.
        """
        if journey_id not in self.journeys:
            return {"error": "Journey not found"}

        journey = self.journeys[journey_id]
        old_stage = journey["stage"]

        # Record stage transition
        journey["stage"] = new_stage
        journey["timeline"].append({
            "stage": new_stage,
            "timestamp": datetime.now().isoformat(),
            "from": old_stage,
            "data": data
        })

        # LEARN from this stage transition
        self._learn_from_transition(journey_id, old_stage, new_stage, data)

        # Get guidance for new stage
        guidance = self.get_stage_guidance(journey_id, new_stage)

        journey["guidance"] = guidance
        self._save_journeys()

        return {
            "journey_id": journey_id,
            "old_stage": old_stage,
            "new_stage": new_stage,
            "guidance": guidance
        }

    # ========================================================================
    # STAGE-SPECIFIC GUIDANCE (Learning Applied)
    # ========================================================================

    def get_stage_guidance(
        self,
        journey_id: str,
        stage: str
    ) -> List[Dict]:
        """
        Get intelligent guidance for current stage.
        Uses all learning systems to provide smart advice.
        """
        journey = self.journeys.get(journey_id)
        if not journey:
            return []

        guidance_methods = {
            "searching": self._guidance_searching,
            "applying": self._guidance_applying,
            "screening": self._guidance_screening,
            "approved": self._guidance_approved,
            "signing": self._guidance_signing,
            "moving_in": self._guidance_moving_in,
            "living": self._guidance_living,
            "issue": self._guidance_issue,
            "resolving": self._guidance_resolving,
            "moving_out": self._guidance_moving_out,
            "dispute": self._guidance_dispute
        }

        handler = guidance_methods.get(stage)
        if not handler:
            return [{"type": "info", "message": f"Stage: {stage}"}]

        return handler(journey)

    def _guidance_searching(self, journey: Dict) -> List[Dict]:
        """Guidance: Looking for apartment"""
        location = journey.get("location", {})

        # Learn from past user searches in this area
        patterns = self.learning.get_user_patterns(journey["user_id"])

        guidance = [
            {
                "type": "checklist",
                "title": "🔍 Apartment Search Checklist",
                "items": [
                    "Check landlord/property manager reputation",
                    "Verify rent is within local averages",
                    "Look for building code violations",
                    "Research neighborhood tenant laws"
                ]
            }
        ]

        # INTELLIGENCE: Check if we know about common issues in this area
        area_intel = self.intelligence.lookup(
            entity_type="location",
            entity_id=f"{location.get('city', '')}_{location.get('zip', '')}"
        )

        if area_intel:
            guidance.append({
                "type": "warning",
                "title": "⚠️ Area Intelligence",
                "message": f"Based on {area_intel.get('data_points', 0)} reports in this area",
                "insights": area_intel.get("common_issues", [])
            })

        return guidance

    def _guidance_applying(self, journey: Dict) -> List[Dict]:
        """Guidance: Submitted application"""
        context = journey.get("context", {})
        agency = context.get("agency", "")

        guidance = []

        # INTELLIGENCE: Lookup this agency/landlord
        if agency:
            intel = self.intelligence.lookup(
                entity_type="agency",
                entity_id=agency
            )

            if intel:
                # LEARNING: What do we know about this agency?
                known_issues = intel.get("known_issues", [])
                avg_fee = intel.get("average_application_fee", 0)

                if known_issues:
                    guidance.append({
                        "type": "warning",
                        "title": f"⚠️ {agency} - Known Issues",
                        "issues": known_issues,
                        "recommendation": "Document everything from this point forward"
                    })

                if avg_fee:
                    guidance.append({
                        "type": "info",
                        "title": "💰 Application Fee Intelligence",
                        "message": f"Average fee for {agency}: ${avg_fee}",
                        "legal_max": self._get_legal_max_fee(journey["location"])
                    })

        # CURIOSITY: If we don't know about this agency, get curious
        if agency and not intel:
            self.curiosity.detect_knowledge_gap(
                topic=f"Agency reputation: {agency}",
                why_needed="User is applying, needs risk assessment"
            )

        guidance.append({
            "type": "action",
            "title": "📋 What to Do Now",
            "actions": [
                "Keep copy of application",
                "Document application fee amount",
                "Note who you spoke with",
                "Get timeline for decision"
            ]
        })

        return guidance

    def _guidance_signing(self, journey: Dict) -> List[Dict]:
        """Guidance: Reviewing lease"""
        context = journey.get("context", {})
        location = journey["location"]

        guidance = [
            {
                "type": "critical",
                "title": "🚨 LEASE REVIEW - DO NOT RUSH",
                "message": "Most tenant problems come from lease issues. Take your time."
            }
        ]

        # JURISDICTION: What laws apply to this lease?
        jurisdiction_info = self.jurisdiction.get_procedural_requirements(
            issue_type="security_deposit",
            location=location
        )

        guidance.append({
            "type": "legal",
            "title": "⚖️ Legal Limits in Your Area",
            "jurisdiction": jurisdiction_info.get("applicable_law", {})
        })

        # LEARNING: What lease clauses cause problems?
        problematic_clauses = self.learning.get_pattern("problematic_lease_clauses")

        if problematic_clauses:
            guidance.append({
                "type": "warning",
                "title": "⚠️ Watch Out For These Clauses",
                "learned_from": f"{problematic_clauses.get('sample_size', 0)} cases",
                "clauses": problematic_clauses.get("common_problems", [
                    "Excessive late fees",
                    "Waiver of repair rights",
                    "Mandatory arbitration",
                    "Automatic rent increases"
                ])
            })

        guidance.append({
            "type": "action",
            "title": "✅ Before You Sign",
            "actions": [
                "Read ENTIRE lease (don't skim)",
                "Check security deposit amount vs legal max",
                "Verify rent increase limits",
                "Look for illegal clauses",
                "Take photos of lease",
                "Ask questions about anything unclear"
            ]
        })

        return guidance

    def _guidance_moving_in(self, journey: Dict) -> List[Dict]:
        """Guidance: Move-in inspection"""
        guidance = [
            {
                "type": "critical",
                "title": "📸 MOVE-IN INSPECTION IS CRITICAL",
                "message": "This protects your security deposit. Document EVERYTHING."
            },
            {
                "type": "checklist",
                "title": "Move-In Documentation Checklist",
                "items": [
                    "Photo/video of EVERY room (10+ photos per room)",
                    "Zoom in on any damage (scratches, stains, cracks)",
                    "Test all appliances",
                    "Check all locks",
                    "Run water in all sinks/showers",
                    "Check smoke/carbon monoxide detectors",
                    "Document meter readings",
                    "Get dated signatures on inspection form"
                ]
            }
        ]

        # LEARNING: What do people forget to document?
        common_mistakes = self.learning.get_pattern("move_in_mistakes")
        if common_mistakes:
            guidance.append({
                "type": "tip",
                "title": "💡 Don't Forget (learned from others)",
                "items": common_mistakes.get("forgotten_items", [
                    "Carpet stains (85% of deposit disputes)",
                    "Window screens (often missing)",
                    "Cabinet damage",
                    "Existing mold"
                ])
            })

        return guidance

    def _guidance_issue(self, journey: Dict) -> List[Dict]:
        """Guidance: Problem arises"""
        context = journey.get("context", {})
        issue_type = context.get("issue_type", "general")
        location = journey["location"]

        guidance = []

        # JURISDICTION: What's the legal process?
        legal_path = self.jurisdiction.get_procedural_requirements(
            issue_type=issue_type,
            location=location
        )

        guidance.append({
            "type": "legal",
            "title": "⚖️ Legal Process for Your Issue",
            "applicable_law": legal_path.get("applicable_law", {}),
            "steps": legal_path.get("procedural_steps", [])
        })

        # INTELLIGENCE: Similar cases
        similar = self.intelligence.find_similar_situations(
            issue_type=issue_type,
            context=context
        )

        if similar:
            guidance.append({
                "type": "intelligence",
                "title": f"📊 Intelligence from {similar.get('count', 0)} Similar Cases",
                "success_rate": similar.get("success_rate", "N/A"),
                "common_strategies": similar.get("successful_strategies", []),
                "warnings": similar.get("common_pitfalls", [])
            })

        # CURIOSITY: If we don't have data on this issue, get curious
        if not similar or similar.get("count", 0) < 5:
            self.curiosity.detect_knowledge_gap(
                topic=f"Outcomes for {issue_type} in {location.get('city', 'unknown')}",
                why_needed="Need more data to provide better guidance"
            )

        return guidance

    def _guidance_resolving(self, journey: Dict) -> List[Dict]:
        """Guidance: Working on resolution"""
        # Get current approach
        # Provide real-time feedback based on learned patterns
        return []

    def _guidance_moving_out(self, journey: Dict) -> List[Dict]:
        """Guidance: End of tenancy"""
        return []

    def _guidance_dispute(self, journey: Dict) -> List[Dict]:
        """Guidance: Post-move-out dispute"""
        return []

    def _guidance_approved(self, journey: Dict) -> List[Dict]:
        """Guidance: Application approved"""
        return [{"type": "info", "message": "Application approved! Moving to lease review."}]

    def _guidance_screening(self, journey: Dict) -> List[Dict]:
        """Guidance: Landlord reviewing application"""
        return [{"type": "info", "message": "Screening in progress. Check back soon."}]

    def _guidance_living(self, journey: Dict) -> List[Dict]:
        """Guidance: Day-to-day tenancy"""
        return [{"type": "info", "message": "Keep documentation of all communications."}]

    # ========================================================================
    # LEARNING FROM JOURNEY
    # ========================================================================

    def _learn_from_transition(
        self,
        journey_id: str,
        old_stage: str,
        new_stage: str,
        data: Dict[str, Any]
    ):
        """
        Learn from each stage transition.
        Updates learning engines with new knowledge.
        """
        journey = self.journeys[journey_id]
        user_id = journey["user_id"]

        # Record observation
        self.learning.observe_action(
            user_id=user_id,
            action=f"{old_stage}_to_{new_stage}",
            context=data or {}
        )

        # Special learning based on stage
        if new_stage == "applying" and data:
            # Learn about application fees
            fee = data.get("application_fee")
            agency = data.get("agency")
            address = data.get("address")

            if fee and agency:
                self.intelligence.add_entity_data(
                    entity_type="agency",
                    entity_id=agency,
                    data={
                        "application_fee": fee,
                        "address": address,
                        "reported_at": datetime.now().isoformat()
                    }
                )

        elif new_stage == "issue" and data:
            # Learn about problems
            issue_type = data.get("issue_type")
            landlord = data.get("landlord")

            if issue_type and landlord:
                self.intelligence.add_entity_data(
                    entity_type="landlord",
                    entity_id=landlord,
                    data={
                        "issue": issue_type,
                        "reported_at": datetime.now().isoformat()
                    }
                )

    def _get_legal_max_fee(self, location: Dict) -> str:
        """Get legal maximum application fee for location."""
        # In California (2025): $58.23 max
        # This would query jurisdiction_engine in real implementation
        return "$58.23 (California 2025)"

    # ========================================================================
    # OUTCOMES & CONTINUOUS LEARNING
    # ========================================================================

    def record_outcome(
        self,
        journey_id: str,
        outcome_type: str,
        outcome_data: Dict[str, Any]
    ):
        """
        Record journey outcome and trigger learning.
        This is where curiosity engine learns from results.
        """
        if journey_id not in self.journeys:
            return

        journey = self.journeys[journey_id]

        # Record outcome
        journey["outcome"] = {
            "type": outcome_type,
            "data": outcome_data,
            "timestamp": datetime.now().isoformat()
        }

        # LEARN from outcome
        self.learning.observe_outcome(
            user_id=journey["user_id"],
            journey_data=journey,
            outcome=outcome_data
        )

        # CURIOSITY: Did outcome match predictions?
        # (This would check predictions made earlier in journey)

        self._save_journeys()


# Global instance
_tenant_journey = None

def get_tenant_journey() -> TenantJourney:
    """Get global tenant journey tracker."""
    global _tenant_journey
    if _tenant_journey is None:
        _tenant_journey = TenantJourney()
    return _tenant_journey
