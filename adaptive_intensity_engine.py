# Adaptive Intensity System - Scale response to situation
# Good landlords get positive recognition, bad ones get escalating pressure

"""
PHILOSOPHY:
Not all situations require full legal intensity.

INTENSITY LEVELS:
1. POSITIVE - Everything going well, landlord responsive → Recognition
2. COLLABORATIVE - Minor issues, landlord trying → Gentle guidance
3. ASSERTIVE - Issues persist, landlord slow → Formal documentation
4. ESCALATED - Serious issues, landlord ignoring → Multi-venue filing
5. MAXIMUM - Dangerous/illegal, landlord hostile → All venues + media

GOOD LANDLORD RECOGNITION:
- Landlords who maintain properties deserve recognition
- Being a landlord is a community investment
- Good landlords should be celebrated, not hassled
- Bad tenants exist too - system recognizes both sides
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum


class IntensityLevel(Enum):
    """Response intensity levels - scale to situation."""
    POSITIVE = "positive"  # Everything good - recognition mode
    COLLABORATIVE = "collaborative"  # Minor issues - friendly guidance
    ASSERTIVE = "assertive"  # Persistent issues - formal documentation
    ESCALATED = "escalated"  # Serious issues - multi-venue filing
    MAXIMUM = "maximum"  # Dangerous/illegal - all venues + pressure


class SituationSeverity(Enum):
    """How severe is the actual issue?"""
    GOOD = "good"  # No issues, or resolved quickly
    MINOR = "minor"  # Small issues, not urgent
    MODERATE = "moderate"  # Real issues, needs attention
    SERIOUS = "serious"  # Significant problems, health/safety concerns
    CRITICAL = "critical"  # Immediate danger, illegal activity


class LandlordResponsiveness(Enum):
    """How responsive is the landlord?"""
    EXCELLENT = "excellent"  # Proactive, fixes before asked
    GOOD = "good"  # Responsive, fixes within reasonable time
    FAIR = "fair"  # Eventually responds, needs reminders
    POOR = "poor"  # Slow to respond, makes excuses
    HOSTILE = "hostile"  # Ignores, retaliates, threatens


class AdaptiveIntensityEngine:
    """
    Determines appropriate response intensity based on:
    - Issue severity
    - Landlord responsiveness
    - History of relationship
    - User preferences
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.landlord_ratings_file = os.path.join(data_dir, "landlord_ratings.json")
        self.intensity_history_file = os.path.join(data_dir, "intensity_history.json")

        self.landlord_ratings = self._load_landlord_ratings()
        self.intensity_history = self._load_intensity_history()

    def _load_landlord_ratings(self) -> Dict:
        """Load landlord ratings (good/bad history)."""
        if os.path.exists(self.landlord_ratings_file):
            with open(self.landlord_ratings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_intensity_history(self) -> Dict:
        """Load intensity escalation history per situation."""
        if os.path.exists(self.intensity_history_file):
            with open(self.intensity_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_landlord_ratings(self):
        """Persist landlord ratings."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.landlord_ratings_file, 'w', encoding='utf-8') as f:
            json.dump(self.landlord_ratings, f, indent=2)

    def _save_intensity_history(self):
        """Persist intensity history."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.intensity_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.intensity_history, f, indent=2)

    # ========================================================================
    # DETERMINE APPROPRIATE INTENSITY
    # ========================================================================

    def determine_intensity(
        self,
        issue_severity: str,  # "good", "minor", "moderate", "serious", "critical"
        landlord_responsiveness: str,  # "excellent", "good", "fair", "poor", "hostile"
        landlord_id: Optional[str] = None,
        days_since_reported: int = 0,
        user_preference: Optional[str] = None  # "gentle", "normal", "aggressive"
    ) -> Dict:
        """
        Determine appropriate response intensity.

        Returns:
            {
                "intensity_level": "positive|collaborative|assertive|escalated|maximum",
                "reason": "Why this intensity level",
                "recommended_actions": [...],
                "avoid_actions": [...],
                "tone": "positive|helpful|firm|serious|urgent"
            }
        """
        severity = SituationSeverity(issue_severity)
        responsiveness = LandlordResponsiveness(landlord_responsiveness)

        # Get landlord history if available
        landlord_history = None
        if landlord_id and landlord_id in self.landlord_ratings:
            landlord_history = self.landlord_ratings[landlord_id]

        # Calculate base intensity from severity + responsiveness
        intensity_score = self._calculate_intensity_score(
            severity,
            responsiveness,
            landlord_history,
            days_since_reported
        )

        # Adjust for user preference
        if user_preference == "gentle":
            intensity_score -= 1
        elif user_preference == "aggressive":
            intensity_score += 1

        # Clamp to valid range (0-4)
        intensity_score = max(0, min(4, intensity_score))

        # Map score to intensity level
        intensity_levels = [
            IntensityLevel.POSITIVE,
            IntensityLevel.COLLABORATIVE,
            IntensityLevel.ASSERTIVE,
            IntensityLevel.ESCALATED,
            IntensityLevel.MAXIMUM
        ]
        intensity_level = intensity_levels[intensity_score]

        # Generate guidance for this intensity level
        guidance = self._generate_intensity_guidance(
            intensity_level,
            severity,
            responsiveness,
            landlord_history,
            days_since_reported
        )

        return guidance

    def _calculate_intensity_score(
        self,
        severity: SituationSeverity,
        responsiveness: LandlordResponsiveness,
        landlord_history: Optional[Dict],
        days_since_reported: int
    ) -> int:
        """
        Calculate intensity score (0-4).

        0 = POSITIVE (everything good)
        1 = COLLABORATIVE (minor issues, responsive landlord)
        2 = ASSERTIVE (moderate issues or slow landlord)
        3 = ESCALATED (serious issues or unresponsive landlord)
        4 = MAXIMUM (critical issues or hostile landlord)
        """
        score = 0

        # Base score from severity
        severity_scores = {
            SituationSeverity.GOOD: 0,
            SituationSeverity.MINOR: 1,
            SituationSeverity.MODERATE: 2,
            SituationSeverity.SERIOUS: 3,
            SituationSeverity.CRITICAL: 4
        }
        score = severity_scores[severity]

        # Adjust for responsiveness
        if responsiveness == LandlordResponsiveness.EXCELLENT:
            score -= 1  # Lower intensity for great landlords
        elif responsiveness == LandlordResponsiveness.GOOD:
            score += 0  # No change
        elif responsiveness == LandlordResponsiveness.FAIR:
            score += 0  # No change initially
        elif responsiveness == LandlordResponsiveness.POOR:
            score += 1  # Increase intensity
        elif responsiveness == LandlordResponsiveness.HOSTILE:
            score += 2  # Significant increase

        # Adjust for time elapsed (if issue not resolved)
        if days_since_reported > 30:
            score += 2  # Escalate after 30 days
        elif days_since_reported > 14:
            score += 1  # Escalate after 14 days
        elif days_since_reported > 7:
            score += 0.5  # Slight escalation after 7 days

        # Adjust for landlord history
        if landlord_history:
            avg_rating = landlord_history.get("average_rating", 3.0)
            if avg_rating >= 4.5:
                score -= 1  # Proven good landlord - give benefit of doubt
            elif avg_rating <= 2.0:
                score += 1  # Proven bad landlord - escalate faster

        return int(round(score))

    def _generate_intensity_guidance(
        self,
        intensity_level: IntensityLevel,
        severity: SituationSeverity,
        responsiveness: LandlordResponsiveness,
        landlord_history: Optional[Dict],
        days_since_reported: int
    ) -> Dict:
        """Generate specific guidance for intensity level."""

        if intensity_level == IntensityLevel.POSITIVE:
            return {
                "intensity_level": "positive",
                "reason": "No issues or landlord is excellent - recognition mode",
                "recommended_actions": [
                    "Leave positive review for landlord",
                    "Recognize good property maintenance",
                    "Build positive relationship",
                    "No formal action needed"
                ],
                "avoid_actions": [
                    "Filing formal complaints",
                    "Threatening legal action",
                    "Confrontational communication"
                ],
                "tone": "positive",
                "message": "Your landlord is doing a great job! Consider leaving a positive review to recognize good property management.",
                "landlord_message": "Thank you for maintaining your property well and being responsive to tenant needs."
            }

        elif intensity_level == IntensityLevel.COLLABORATIVE:
            return {
                "intensity_level": "collaborative",
                "reason": "Minor issues with generally responsive landlord - friendly guidance",
                "recommended_actions": [
                    "Friendly communication (call or text)",
                    "Document issue with photos",
                    "Give reasonable timeline for fix",
                    "Offer to be flexible if landlord needs time"
                ],
                "avoid_actions": [
                    "Filing formal complaints prematurely",
                    "Threatening legal action",
                    "Demanding immediate action for non-urgent issues"
                ],
                "tone": "helpful",
                "message": "Start with friendly communication. Most responsive landlords will address minor issues quickly when notified.",
                "communication_template": "Hi [Landlord], just wanted to let you know about [issue]. When you have a chance, could you take a look? Thanks!"
            }

        elif intensity_level == IntensityLevel.ASSERTIVE:
            return {
                "intensity_level": "assertive",
                "reason": f"Issue persists ({days_since_reported} days) or landlord slow to respond - formal documentation needed",
                "recommended_actions": [
                    "Send written notice (email or certified mail)",
                    "Document everything (photos, videos, communications)",
                    "Set clear deadline for repairs",
                    "Keep records of all communications",
                    "Mention legal obligations (habitability, lease terms)"
                ],
                "avoid_actions": [
                    "Withholding rent without legal grounds",
                    "Making repairs yourself without permission",
                    "Being confrontational"
                ],
                "tone": "firm",
                "message": "Time for formal documentation. Send written notice with clear deadline and document everything.",
                "communication_template": "Dear [Landlord], I am writing to formally notify you of [issue]. This issue affects [habitability/safety/lease terms]. Please address within [X] days. Required by [relevant law/lease section]."
            }

        elif intensity_level == IntensityLevel.ESCALATED:
            return {
                "intensity_level": "escalated",
                "reason": "Serious issues or unresponsive landlord - multi-venue filing recommended",
                "recommended_actions": [
                    "File with city code enforcement (if habitability)",
                    "File with relevant agency (HUD, health dept, etc.)",
                    "Contact tenant legal aid",
                    "Consider escrow/rent withholding (with legal advice)",
                    "Document EVERYTHING",
                    "Keep communication formal and written"
                ],
                "avoid_actions": [
                    "Taking illegal action (breaking lease without grounds)",
                    "Damaging property",
                    "Harassing landlord"
                ],
                "tone": "serious",
                "message": "Formal complaints needed. File with appropriate agencies and document everything. Consider legal aid.",
                "venues": "multiple"  # Signal to use multi-venue filing
            }

        else:  # IntensityLevel.MAXIMUM
            return {
                "intensity_level": "maximum",
                "reason": "Critical safety issues or hostile landlord - all venues + maximum pressure",
                "recommended_actions": [
                    "File with ALL applicable venues immediately",
                    "City code enforcement (emergency inspection)",
                    "County health department (health hazards)",
                    "HUD (if discrimination/Section 8)",
                    "Contact legal aid immediately",
                    "Consider media/public pressure",
                    "Emergency court action if needed",
                    "Document EVERYTHING with photos/videos"
                ],
                "avoid_actions": [
                    "Staying in dangerous conditions",
                    "Taking illegal action",
                    "Being alone for inspections (bring witness)"
                ],
                "tone": "urgent",
                "message": "URGENT: Critical safety issue or illegal landlord activity. File with all venues immediately and seek legal help.",
                "venues": "all",  # Signal to use all applicable venues
                "urgency": "emergency"
            }

    # ========================================================================
    # GOOD LANDLORD RECOGNITION SYSTEM
    # ========================================================================

    def rate_landlord(
        self,
        landlord_id: str,
        rating: float,  # 1-5 stars
        category: str,  # "responsiveness", "maintenance", "communication", "fairness"
        comment: Optional[str] = None,
        tenant_id: Optional[str] = None
    ):
        """
        Rate landlord in specific category.
        Good landlords deserve recognition!
        """
        if landlord_id not in self.landlord_ratings:
            self.landlord_ratings[landlord_id] = {
                "landlord_id": landlord_id,
                "ratings": [],
                "average_rating": 0.0,
                "total_ratings": 0,
                "category_averages": {},
                "recognition": None
            }

        landlord_data = self.landlord_ratings[landlord_id]

        # Add rating
        landlord_data["ratings"].append({
            "rating": rating,
            "category": category,
            "comment": comment,
            "timestamp": datetime.now().isoformat(),
            "tenant_id": tenant_id
        })

        # Recalculate averages
        all_ratings = [r["rating"] for r in landlord_data["ratings"]]
        landlord_data["average_rating"] = sum(all_ratings) / len(all_ratings)
        landlord_data["total_ratings"] = len(all_ratings)

        # Calculate category averages
        categories = {}
        for r in landlord_data["ratings"]:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r["rating"])

        landlord_data["category_averages"] = {
            cat: sum(ratings) / len(ratings)
            for cat, ratings in categories.items()
        }

        # Determine recognition level
        avg = landlord_data["average_rating"]
        total = landlord_data["total_ratings"]

        if avg >= 4.5 and total >= 5:
            landlord_data["recognition"] = "EXCELLENT - Community Asset"
        elif avg >= 4.0 and total >= 3:
            landlord_data["recognition"] = "GOOD - Reliable Landlord"
        elif avg >= 3.0:
            landlord_data["recognition"] = "FAIR - Meets Basic Standards"
        elif avg >= 2.0:
            landlord_data["recognition"] = "POOR - Frequent Issues"
        else:
            landlord_data["recognition"] = "PROBLEM - Persistent Violations"

        self._save_landlord_ratings()

    def get_landlord_profile(self, landlord_id: str) -> Optional[Dict]:
        """Get landlord profile with ratings and recognition."""
        if landlord_id not in self.landlord_ratings:
            return None

        profile = self.landlord_ratings[landlord_id].copy()

        # Add recognition message
        avg = profile["average_rating"]
        if avg >= 4.5:
            profile["message"] = "🌟 EXCELLENT LANDLORD - Maintains property well, responsive, fair. A community asset!"
        elif avg >= 4.0:
            profile["message"] = "✅ GOOD LANDLORD - Generally responsive and maintains property. Reliable."
        elif avg >= 3.0:
            profile["message"] = "⚠️ FAIR LANDLORD - Meets basic requirements but has room for improvement."
        elif avg >= 2.0:
            profile["message"] = "❌ POOR LANDLORD - Frequent issues with responsiveness or maintenance."
        else:
            profile["message"] = "🚫 PROBLEM LANDLORD - Persistent violations, unresponsive, or hostile."

        return profile

    def generate_landlord_recognition_certificate(self, landlord_id: str) -> Optional[Dict]:
        """
        Generate recognition certificate for excellent landlords.
        Being a good landlord is an investment in community!
        """
        profile = self.get_landlord_profile(landlord_id)

        if not profile or profile["average_rating"] < 4.0:
            return None

        return {
            "certificate_type": "Good Landlord Recognition",
            "landlord_id": landlord_id,
            "average_rating": profile["average_rating"],
            "total_ratings": profile["total_ratings"],
            "recognition_level": profile["recognition"],
            "message": f"""
            🏆 GOOD LANDLORD RECOGNITION 🏆

            This certificate recognizes exceptional property management and tenant care.

            Rating: {profile['average_rating']:.1f}/5.0 stars ({profile['total_ratings']} reviews)
            Recognition: {profile['recognition']}

            Category Ratings:
            {self._format_category_ratings(profile['category_averages'])}

            Being a landlord is an investment in community, the future, and fair monetary gain.
            Thank you for maintaining your property well and treating tenants with respect.

            Issued: {datetime.now().strftime('%B %d, %Y')}
            """,
            "issued_date": datetime.now().isoformat()
        }

    def _format_category_ratings(self, category_averages: Dict) -> str:
        """Format category ratings for certificate."""
        lines = []
        for category, avg in category_averages.items():
            stars = "⭐" * int(round(avg))
            lines.append(f"  • {category.title()}: {stars} ({avg:.1f}/5.0)")
        return "\n".join(lines)

    # ========================================================================
    # BAD TENANT RECOGNITION (Landlords have issues too!)
    # ========================================================================

    def report_tenant_issue(
        self,
        tenant_id: str,
        issue_type: str,  # "late_rent", "property_damage", "lease_violation", "noise", etc.
        severity: str,  # "minor", "moderate", "serious"
        description: str,
        landlord_id: str
    ):
        """
        Landlords can report tenant issues too.
        Bad tenants exist - system recognizes both sides.
        """
        # This ensures fairness - not all tenants are angels
        # Not all landlords are bad
        # System should recognize both good and bad on BOTH sides

        # Store tenant issue report (for future reference)
        # Not implemented fully yet, but placeholder for fairness
        pass


# Global instance
_adaptive_intensity_engine = None

def get_adaptive_intensity_engine() -> AdaptiveIntensityEngine:
    """Get global adaptive intensity engine instance."""
    global _adaptive_intensity_engine
    if _adaptive_intensity_engine is None:
        _adaptive_intensity_engine = AdaptiveIntensityEngine()
    return _adaptive_intensity_engine
