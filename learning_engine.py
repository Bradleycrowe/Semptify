"""
Self-Learning Engine for Semptify
Analyzes user behavior and improves suggestions over time.
Uses existing event logs and data flow to learn patterns.
"""

import os
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional

class LearningEngine:
    """
    Lightweight ML that learns from user behavior WITHOUT external dependencies.
    Learns patterns from logs/events.log and data flow engine.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.patterns_file = os.path.join(data_dir, "learning_patterns.json")
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> dict:
        """Load learned patterns from disk."""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "user_habits": {},       # user_id -> {action: count}
            "sequences": {},         # "action1->action2": frequency
            "time_patterns": {},     # hour -> most_common_actions
            "success_rates": {},     # action -> success_percentage
            "suggestions": {}        # context -> suggested_next_action
        }

    def _save_patterns(self):
        """Persist learned patterns to disk."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)

    # ========================================================================
    # OBSERVE: Learn from user actions
    # ========================================================================

    def observe_action(self, user_id: str, action: str, context: dict = None):
        """
        Record a user action to learn patterns.

        Args:
            user_id: User performing the action
            action: What they did (e.g., "upload_lease", "file_complaint")
            context: Additional context (time, success, etc.)
        """
        context = context or {}

        # Track user habits
        if user_id not in self.patterns["user_habits"]:
            self.patterns["user_habits"][user_id] = {}

        habits = self.patterns["user_habits"][user_id]
        habits[action] = habits.get(action, 0) + 1

        # Track time patterns
        hour = datetime.now().hour
        if hour not in self.patterns["time_patterns"]:
            self.patterns["time_patterns"][hour] = Counter()
        self.patterns["time_patterns"][hour][action] += 1

        # Track success rate
        if action not in self.patterns["success_rates"]:
            self.patterns["success_rates"][action] = {"attempts": 0, "successes": 0}

        self.patterns["success_rates"][action]["attempts"] += 1
        if context.get("success", True):
            self.patterns["success_rates"][action]["successes"] += 1

        self._save_patterns()

    def observe_sequence(self, user_id: str, action1: str, action2: str):
        """
        Learn action sequences (e.g., upload lease → file complaint).
        This helps predict what user wants to do next.
        """
        seq_key = f"{action1}->{action2}"
        self.patterns["sequences"][seq_key] = self.patterns["sequences"].get(seq_key, 0) + 1
        self._save_patterns()

    # ========================================================================
    # SUGGEST: Provide intelligent recommendations
    # ========================================================================

    def suggest_next_action(self, user_id: str, last_action: str) -> Optional[str]:
        """
        Based on learned patterns, suggest what user should do next.

        Returns:
            Suggested action string or None
        """
        # Find most common sequence after last_action
        relevant_sequences = {
            seq: count for seq, count in self.patterns["sequences"].items()
            if seq.startswith(last_action + "->")
        }

        if relevant_sequences:
            # Return most common next action
            best_seq = max(relevant_sequences.items(), key=lambda x: x[1])[0]
            return best_seq.split("->")[1]

        return None

    def get_personalized_suggestions(self, user_id: str) -> List[str]:
        """
        Get suggestions based on user's habits.

        Returns:
            List of actions this user commonly performs
        """
        habits = self.patterns["user_habits"].get(user_id, {})
        if not habits:
            return []

        # Return top 3 most common actions
        sorted_habits = sorted(habits.items(), key=lambda x: x[1], reverse=True)
        return [action for action, count in sorted_habits[:3]]

    def get_time_based_suggestion(self) -> Optional[str]:
        """
        Suggest action based on time of day patterns.

        Returns:
            Most common action for this hour
        """
        hour = datetime.now().hour
        if hour in self.patterns["time_patterns"]:
            actions = self.patterns["time_patterns"][hour]
            if actions:
                return actions.most_common(1)[0][0]
        return None

    # ========================================================================
    # ANALYZE: Generate insights
    # ========================================================================

    def analyze_success_rates(self) -> Dict[str, float]:
        """
        Calculate success rate for each action.

        Returns:
            Dict of {action: success_percentage}
        """
        results = {}
        for action, stats in self.patterns["success_rates"].items():
            if stats["attempts"] > 0:
                rate = (stats["successes"] / stats["attempts"]) * 100
                results[action] = round(rate, 2)
        return results

    def get_common_mistakes(self, threshold: float = 50.0) -> List[str]:
        """
        Find actions with low success rates (common mistakes).

        Args:
            threshold: Success rate below this is considered a mistake

        Returns:
            List of problematic actions
        """
        success_rates = self.analyze_success_rates()
        return [
            action for action, rate in success_rates.items()
            if rate < threshold and self.patterns["success_rates"][action]["attempts"] >= 3
        ]

    def get_insights(self, user_id: str = None) -> dict:
        """
        Generate learning insights for display.

        Returns:
            Dict with insights about user behavior and suggestions
        """
        insights = {
            "total_actions_tracked": sum(
                sum(habits.values())
                for habits in self.patterns["user_habits"].values()
            ),
            "most_common_sequences": sorted(
                self.patterns["sequences"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "success_rates": self.analyze_success_rates(),
            "common_mistakes": self.get_common_mistakes(),
            "peak_hours": self._get_peak_hours()
        }

        if user_id:
            insights["personalized_suggestions"] = self.get_personalized_suggestions(user_id)

        return insights

    def _get_peak_hours(self) -> List[int]:
        """Find hours with most activity."""
        if not self.patterns["time_patterns"]:
            return []

        hour_totals = {
            hour: sum(actions.values())
            for hour, actions in self.patterns["time_patterns"].items()
        }

        sorted_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, count in sorted_hours[:3]]

    # ========================================================================
    # FEEDBACK: Learn from user corrections
    # ========================================================================

    def record_feedback(self, suggestion: str, helpful: bool):
        """
        Learn from user feedback on suggestions.

        Args:
            suggestion: The suggestion that was made
            helpful: Whether user found it helpful
        """
        if suggestion not in self.patterns["suggestions"]:
            self.patterns["suggestions"][suggestion] = {"shown": 0, "helpful": 0}

        self.patterns["suggestions"][suggestion]["shown"] += 1
        if helpful:
            self.patterns["suggestions"][suggestion]["helpful"] += 1

        self._save_patterns()

    def get_best_suggestions(self, min_shown: int = 3) -> List[str]:
        """
        Get suggestions with highest helpfulness rating.

        Args:
            min_shown: Minimum times shown to be considered

        Returns:
            List of best suggestions
        """
        rated = {}
        for suggestion, stats in self.patterns["suggestions"].items():
            if stats["shown"] >= min_shown:
                rate = stats["helpful"] / stats["shown"]
                rated[suggestion] = rate

        return sorted(rated.keys(), key=lambda s: rated[s], reverse=True)


# ============================================================================
# Global Instance
# ============================================================================

_learning_engine: Optional[LearningEngine] = None

def init_learning(data_dir: str = "data") -> LearningEngine:
    """Initialize the learning engine."""
    global _learning_engine
    _learning_engine = LearningEngine(data_dir)
    return _learning_engine

def get_learning() -> LearningEngine:
    """Get the learning engine instance."""
    if _learning_engine is None:
        return init_learning()
    return _learning_engine
