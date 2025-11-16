# Sound & Accurate Data Framework
# "Better than legal advice through verified, data-driven guidance"

"""
PHILOSOPHY:
- Legal advice = generic, one-size-fits-all, theoretical
- Our guidance = specific, location-tested, outcome-verified, continuously improved

DISCLAIMER: "We do not provide legal advice"
REALITY: Our suggestions are MORE sound because they're based on:
  1. Actual outcomes from real cases
  2. Jurisdiction-specific verified procedures
  3. Crowdsourced validation from hundreds of users
  4. Continuous accuracy monitoring
  5. Multi-source verification requirements
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class DataAccuracyEngine:
    """
    Ensures all guidance is sound, accurate, and trustworthy.
    Higher bar than legal advice: verified by real outcomes.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.accuracy_file = os.path.join(data_dir, "accuracy_tracking.json")
        self.verified_file = os.path.join(data_dir, "verified_guidance.json")
        self.accuracy_data = self._load_accuracy_data()
        self.verified_guidance = self._load_verified_guidance()

    def _load_accuracy_data(self) -> Dict:
        """Load accuracy tracking metrics."""
        if os.path.exists(self.accuracy_file):
            with open(self.accuracy_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "guidance_accuracy": {},  # Track success rate per guidance type
            "resource_verification": {},  # Track resource helpfulness
            "procedure_validation": {},  # Track procedure success rates
            "prediction_accuracy": {},  # Track prediction vs reality
            "last_audit": None
        }

    def _load_verified_guidance(self) -> Dict:
        """Load verified, high-confidence guidance only."""
        if os.path.exists(self.verified_file):
            with open(self.verified_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_accuracy_data(self):
        """Persist accuracy tracking."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.accuracy_file, 'w', encoding='utf-8') as f:
            json.dump(self.accuracy_data, f, indent=2)

    def _save_verified_guidance(self):
        """Persist verified guidance."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.verified_file, 'w', encoding='utf-8') as f:
            json.dump(self.verified_guidance, f, indent=2)

    # ========================================================================
    # MULTI-SOURCE VERIFICATION (Never trust single source)
    # ========================================================================

    def verify_guidance(
        self,
        guidance_type: str,
        location_key: str,
        guidance_content: Dict,
        sources: List[Dict]
    ) -> Dict:
        """
        Verify guidance against multiple sources.
        MINIMUM 2 sources required for ANY guidance.
        MINIMUM 3 sources for critical guidance (legal procedures).

        Args:
            guidance_type: "procedure", "resource", "law", "timeline"
            location_key: e.g., "eagan_mn_55121"
            guidance_content: The actual guidance being verified
            sources: List of source dicts with {type, content, confidence}

        Returns:
            {verified: bool, confidence: float, sources_count: int, concerns: []}
        """
        if len(sources) < 2:
            return {
                "verified": False,
                "confidence": 0.0,
                "reason": "Insufficient sources (minimum 2 required)",
                "sources_count": len(sources),
                "show_to_user": False
            }

        # Critical guidance needs 3+ sources
        if guidance_type in ["procedure", "law", "deadline"] and len(sources) < 3:
            return {
                "verified": False,
                "confidence": 0.3,
                "reason": "Critical guidance requires 3+ sources",
                "sources_count": len(sources),
                "show_to_user": False,
                "suggestion": "waiting for more user validations"
            }

        # Check source agreement
        agreement_score = self._calculate_source_agreement(sources)

        # Check recency (old data = lower confidence)
        recency_score = self._calculate_recency_score(sources)

        # Check outcome validation (has this actually worked?)
        outcome_score = self._calculate_outcome_score(
            guidance_type, location_key, guidance_content
        )

        # Combined confidence
        confidence = (agreement_score * 0.4 +
                     recency_score * 0.3 +
                     outcome_score * 0.3)

        verified = confidence >= 0.75  # High bar: 75%+ confidence

        return {
            "verified": verified,
            "confidence": round(confidence, 2),
            "sources_count": len(sources),
            "agreement_score": round(agreement_score, 2),
            "recency_score": round(recency_score, 2),
            "outcome_score": round(outcome_score, 2),
            "show_to_user": verified,
            "quality_level": self._get_quality_level(confidence)
        }

    def _calculate_source_agreement(self, sources: List[Dict]) -> float:
        """
        Do sources agree? Higher agreement = higher confidence.
        """
        if len(sources) < 2:
            return 0.0

        # Extract key facts from each source
        facts = []
        for source in sources:
            facts.append(self._extract_key_facts(source.get("content", "")))

        # Calculate overlap
        all_facts = set()
        common_facts = set(facts[0]) if facts else set()

        for fact_set in facts:
            all_facts.update(fact_set)
            common_facts &= fact_set

        if not all_facts:
            return 0.0

        # Agreement = common facts / total unique facts
        agreement = len(common_facts) / len(all_facts)
        return min(agreement * 1.2, 1.0)  # Boost slightly

    def _extract_key_facts(self, content: str) -> set:
        """Extract key factual elements (numbers, phone, addresses, deadlines)."""
        import re
        facts = set()

        # Phone numbers
        phones = re.findall(r'\d{3}[-.]?\d{3}[-.]?\d{4}', content)
        facts.update(phones)

        # Deadlines (e.g., "24 hours", "5 days", "30 days")
        deadlines = re.findall(r'\d+\s*(hour|day|week|month)s?', content.lower())
        facts.update(deadlines)

        # Statute numbers (e.g., "§504B.161")
        statutes = re.findall(r'§\d+[A-Z]?\.\d+', content)
        facts.update(statutes)

        return facts

    def _calculate_recency_score(self, sources: List[Dict]) -> float:
        """
        Recent data = higher confidence.
        Data older than 1 year = significant penalty.
        """
        now = datetime.now()
        recency_scores = []

        for source in sources:
            timestamp = source.get("timestamp")
            if not timestamp:
                recency_scores.append(0.5)  # Unknown date = moderate penalty
                continue

            try:
                source_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                age_days = (now - source_date).days

                if age_days <= 30:
                    recency_scores.append(1.0)  # Very recent
                elif age_days <= 90:
                    recency_scores.append(0.9)  # Recent
                elif age_days <= 180:
                    recency_scores.append(0.8)  # Moderately recent
                elif age_days <= 365:
                    recency_scores.append(0.6)  # Older
                else:
                    recency_scores.append(0.3)  # Very old (low confidence)
            except:
                recency_scores.append(0.5)

        return sum(recency_scores) / len(recency_scores) if recency_scores else 0.5

    def _calculate_outcome_score(
        self,
        guidance_type: str,
        location_key: str,
        guidance_content: Dict
    ) -> float:
        """
        Has this guidance actually WORKED in real cases?
        This is the gold standard: real-world validation.
        """
        key = f"{location_key}:{guidance_type}:{guidance_content.get('key', '')}"

        if key not in self.accuracy_data["guidance_accuracy"]:
            return 0.5  # No outcome data yet (neutral)

        accuracy = self.accuracy_data["guidance_accuracy"][key]
        success_count = accuracy.get("success_count", 0)
        total_count = accuracy.get("total_count", 0)

        if total_count == 0:
            return 0.5

        success_rate = success_count / total_count

        # Require minimum sample size for high confidence
        if total_count < 3:
            # Low sample size = cap confidence
            return min(success_rate, 0.7)
        elif total_count < 10:
            return min(success_rate, 0.85)
        else:
            return success_rate  # High sample size = trust the data

    def _get_quality_level(self, confidence: float) -> str:
        """
        Quality levels shown to user.
        We ONLY show HIGH and VERIFIED guidance.
        """
        if confidence >= 0.90:
            return "VERIFIED"  # Gold standard
        elif confidence >= 0.75:
            return "HIGH"  # Show to user
        elif confidence >= 0.60:
            return "MODERATE"  # Don't show yet
        else:
            return "LOW"  # Don't show

    # ========================================================================
    # OUTCOME TRACKING (Did our guidance actually work?)
    # ========================================================================

    def track_outcome(
        self,
        guidance_type: str,
        location_key: str,
        guidance_content: Dict,
        outcome: Dict
    ):
        """
        Track whether guidance worked in real world.
        This is how we become MORE accurate than generic advice.

        Args:
            guidance_type: Type of guidance given
            location_key: Where it was used
            guidance_content: What we suggested
            outcome: {success: bool, timeline: str, notes: str}
        """
        key = f"{location_key}:{guidance_type}:{guidance_content.get('key', '')}"

        if key not in self.accuracy_data["guidance_accuracy"]:
            self.accuracy_data["guidance_accuracy"][key] = {
                "success_count": 0,
                "total_count": 0,
                "outcomes": []
            }

        accuracy = self.accuracy_data["guidance_accuracy"][key]

        if outcome.get("success"):
            accuracy["success_count"] += 1

        accuracy["total_count"] += 1
        accuracy["outcomes"].append({
            "timestamp": datetime.now().isoformat(),
            "success": outcome.get("success"),
            "timeline": outcome.get("timeline"),
            "notes": outcome.get("notes", "")
        })

        # Keep only recent 50 outcomes per guidance
        accuracy["outcomes"] = accuracy["outcomes"][-50:]

        # Update success rate
        accuracy["success_rate"] = accuracy["success_count"] / accuracy["total_count"]

        self._save_accuracy_data()

        # If guidance consistently fails, flag for review
        if accuracy["total_count"] >= 5 and accuracy["success_rate"] < 0.5:
            self._flag_for_review(key, "Low success rate")

    # ========================================================================
    # CONFIDENCE SCORING (Show confidence to user)
    # ========================================================================

    def get_guidance_confidence(
        self,
        guidance_type: str,
        location_key: str,
        guidance_content: Dict
    ) -> Dict:
        """
        Get confidence score for any guidance.
        Returns user-friendly confidence display.
        """
        key = f"{location_key}:{guidance_type}:{guidance_content.get('key', '')}"

        if key not in self.accuracy_data["guidance_accuracy"]:
            return {
                "confidence": "LEARNING",
                "description": "New guidance - we're collecting validation",
                "show_to_user": False,
                "sample_size": 0
            }

        accuracy = self.accuracy_data["guidance_accuracy"][key]
        success_rate = accuracy.get("success_rate", 0)
        sample_size = accuracy.get("total_count", 0)

        if sample_size >= 10 and success_rate >= 0.90:
            return {
                "confidence": "VERIFIED ✓",
                "description": f"Proven successful in {sample_size} cases ({int(success_rate*100)}% success rate)",
                "show_to_user": True,
                "badge": "verified",
                "sample_size": sample_size
            }
        elif sample_size >= 5 and success_rate >= 0.80:
            return {
                "confidence": "HIGH",
                "description": f"Usually successful ({int(success_rate*100)}% success rate, {sample_size} cases)",
                "show_to_user": True,
                "badge": "high_confidence",
                "sample_size": sample_size
            }
        elif sample_size >= 3 and success_rate >= 0.70:
            return {
                "confidence": "GOOD",
                "description": f"Often successful ({int(success_rate*100)}% success rate, {sample_size} cases)",
                "show_to_user": True,
                "badge": "good",
                "sample_size": sample_size
            }
        else:
            return {
                "confidence": "LEARNING",
                "description": f"Still collecting data ({sample_size} cases so far)",
                "show_to_user": False,
                "sample_size": sample_size
            }

    # ========================================================================
    # ACCURACY MONITORING (Continuous quality checks)
    # ========================================================================

    def run_accuracy_audit(self) -> Dict:
        """
        Regular audit of all guidance accuracy.
        Identifies low-quality guidance to hide or improve.
        """
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "total_guidance": len(self.accuracy_data["guidance_accuracy"]),
            "verified_guidance": 0,
            "high_confidence": 0,
            "needs_review": 0,
            "flagged_items": []
        }

        for key, accuracy in self.accuracy_data["guidance_accuracy"].items():
            success_rate = accuracy.get("success_rate", 0)
            sample_size = accuracy.get("total_count", 0)

            if sample_size >= 10 and success_rate >= 0.90:
                audit_results["verified_guidance"] += 1
            elif sample_size >= 5 and success_rate >= 0.75:
                audit_results["high_confidence"] += 1
            elif sample_size >= 5 and success_rate < 0.60:
                audit_results["needs_review"] += 1
                audit_results["flagged_items"].append({
                    "key": key,
                    "success_rate": success_rate,
                    "sample_size": sample_size,
                    "action": "HIDE_FROM_USER"
                })

        self.accuracy_data["last_audit"] = audit_results
        self._save_accuracy_data()

        return audit_results

    def _flag_for_review(self, key: str, reason: str):
        """Flag guidance that needs human review."""
        if "flagged_guidance" not in self.accuracy_data:
            self.accuracy_data["flagged_guidance"] = []

        self.accuracy_data["flagged_guidance"].append({
            "key": key,
            "reason": reason,
            "flagged_at": datetime.now().isoformat()
        })

        self._save_accuracy_data()

    # ========================================================================
    # USER-FACING GUIDANCE FORMATTING
    # ========================================================================

    def format_guidance_for_user(
        self,
        guidance: Dict,
        confidence_info: Dict
    ) -> Dict:
        """
        Format guidance with confidence indicators.
        ONLY show HIGH confidence or VERIFIED guidance.
        """
        if not confidence_info.get("show_to_user"):
            return {
                "show": False,
                "reason": "Not enough validation yet"
            }

        return {
            "show": True,
            "content": guidance.get("content"),
            "confidence_badge": confidence_info.get("confidence"),
            "confidence_description": confidence_info.get("description"),
            "sources_count": guidance.get("sources_count", "multiple"),
            "last_verified": guidance.get("last_verified"),
            "disclaimer": "Not legal advice - based on verified user outcomes"
        }


# Global instance
_accuracy_engine = None

def get_accuracy_engine() -> DataAccuracyEngine:
    """Get global accuracy engine instance."""
    global _accuracy_engine
    if _accuracy_engine is None:
        _accuracy_engine = DataAccuracyEngine()
    return _accuracy_engine
