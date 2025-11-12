"""
Smart Suggestions Widget - Contextual Help Powered by Learning Engine

Shows users relevant next steps based on what they've done and their situation.
"""

from learning_engine import LearningEngine
from typing import List, Dict, Optional
import os

# Human perspective integration
try:
    from human_perspective import humanize_object
    HAS_HUMAN_PERSPECTIVE = True
except Exception:
    HAS_HUMAN_PERSPECTIVE = False

class SmartSuggestions:
    """Provides contextual suggestions based on learning patterns."""
    
    def __init__(self):
        self.engine = LearningEngine()
    
    def get_suggestions_for_user(self, user_id: str, context: dict = None) -> List[Dict]:
        """
        Get smart suggestions for a user based on their context and history.
        
        Args:
            user_id: User ID
            context: Current context (e.g., {'just_uploaded': 'photo', 'situation': 'eviction'})
        
        Returns:
            List of suggestions with actions, descriptions, and reasons
        """
        context = context or {}
        suggestions = []
        
        # Get user's recent actions
        habits = self.engine.patterns.get("user_habits", {}).get(user_id, {})
        last_action = max(habits, key=habits.get) if habits else None
        
        # 1. Context-based suggestions (highest priority)
        situation = context.get('situation')
        if situation:
            suggested_action = self.engine.patterns.get("suggestions", {}).get(situation)
            if suggested_action:
                suggestions.append(self._build_suggestion(
                    suggested_action,
                    reason=f"Recommended for your situation: {situation}",
                    priority="high"
                ))
        
        # 2. Last action-based suggestions
        just_did = context.get('just_uploaded') or last_action
        if just_did:
            # Find what commonly follows this action
            next_action = self.engine.suggest_next_action(user_id, just_did)
            if next_action and next_action not in [s['action'] for s in suggestions]:
                suggestions.append(self._build_suggestion(
                    next_action,
                    reason=f"Common next step after: {self._humanize(just_did)}",
                    priority="medium"
                ))
        
        # 3. High-success actions the user hasn't tried yet
        tried_actions = set(habits.keys()) if habits else set()
        success_rates = self.engine.patterns.get("success_rates", {})
        
        high_success = [
            action for action, stats in success_rates.items()
            if (stats["successes"] / stats["attempts"]) > 0.90
            and action not in tried_actions
        ]
        
        if high_success and len(suggestions) < 3:
            for action in high_success[:2]:
                suggestions.append(self._build_suggestion(
                    action,
                    reason="High success rate action",
                    priority="low"
                ))
        
        # 4. First-time user? Give them a starting point
        if not habits or len(habits) == 0:
            first_steps = [
                ("upload_lease", "Start by uploading your lease agreement"),
                ("document_with_photos", "Document issues with photos/videos"),
                ("explore_vault", "Explore your secure document vault"),
            ]
            for action, desc in first_steps[:2]:
                if action not in [s['action'] for s in suggestions]:
                    suggestions.append({
                        "action": action,
                        "title": self._humanize(action),
                        "description": desc,
                        "reason": "Great first step for new users",
                        "priority": "medium",
                        "icon": self._get_icon(action),
                        "tip": self.engine.patterns.get("action_tips", {}).get(action),
                        "warning": self.engine.patterns.get("warnings", {}).get(action),
                    })
        
        return suggestions[:5]  # Max 5 suggestions
    
    def _build_suggestion(self, action: str, reason: str, priority: str) -> Dict:
        """Build a complete suggestion dict."""
        suggestion = {
            "action": action,
            "title": self._humanize(action),
            "description": self._get_description(action),
            "reason": reason,
            "priority": priority,
            "icon": self._get_icon(action),
            "tip": self.engine.patterns.get("action_tips", {}).get(action),
            "warning": self.engine.patterns.get("warnings", {}).get(action),
            "success_rate": self._get_success_rate(action),
        }
        
        # Add human perspective if available
        if HAS_HUMAN_PERSPECTIVE:
            try:
                human_view = humanize_object(
                    {"action": action, "description": suggestion["description"]},
                    {"audience": "tenant", "reading_level": "plain"}
                )
                suggestion["human_explanation"] = human_view.get("summary", "")
                suggestion["human_next_steps"] = human_view.get("next_steps", [])[:3]
            except Exception:
                pass
        
        return suggestion
    
    def _humanize(self, action: str) -> str:
        """Convert action_name to Human Readable Title."""
        return action.replace('_', ' ').title()
    
    def _get_description(self, action: str) -> str:
        """Get a user-friendly description of the action."""
        descriptions = {
            "upload_lease": "Upload your lease agreement for reference and evidence",
            "document_with_photos": "Take photos or videos to document conditions or incidents",
            "create_witness_statement": "Write a detailed account of what happened",
            "organize_timeline": "Build a chronological record of events",
            "gather_rent_receipts": "Collect proof of rent payments",
            "upload_eviction_notice": "Upload the eviction notice you received",
            "find_legal_aid_nearby": "Search for free or low-cost legal help",
            "send_repair_demand": "Send a formal written repair request to landlord",
            "file_complaint": "File an official complaint with authorities",
            "prepare_evidence_packet": "Organize your evidence for court or filing",
        }
        return descriptions.get(action, f"Take action: {self._humanize(action)}")
    
    def _get_icon(self, action: str) -> str:
        """Get emoji icon for action."""
        icons = {
            "upload_lease": "📄",
            "document_with_photos": "📸",
            "create_witness_statement": "✍️",
            "organize_timeline": "📅",
            "gather_rent_receipts": "💰",
            "upload_eviction_notice": "⚠️",
            "find_legal_aid_nearby": "🤝",
            "send_repair_demand": "📧",
            "file_complaint": "⚖️",
            "prepare_evidence_packet": "📦",
            "explore_vault": "🔒",
            "upload_photo": "📷",
            "upload_video": "🎥",
        }
        return icons.get(action, "💡")
    
    def _get_success_rate(self, action: str) -> Optional[float]:
        """Get success rate percentage for an action."""
        stats = self.engine.patterns.get("success_rates", {}).get(action)
        if stats:
            return round((stats["successes"] / stats["attempts"]) * 100, 1)
        return None


def get_dashboard_suggestions(user_id: str, context: dict = None) -> List[Dict]:
    """
    Convenience function for dashboard to get suggestions.
    
    Usage in templates:
        suggestions = get_dashboard_suggestions(session['user_id'], {'situation': 'eviction'})
    """
    widget = SmartSuggestions()
    return widget.get_suggestions_for_user(user_id, context)


# Example usage
if __name__ == "__main__":
    widget = SmartSuggestions()
    
    print("🧪 Testing Smart Suggestions Widget\n")
    
    # Test 1: New user
    print("=== New User (no history) ===")
    suggestions = widget.get_suggestions_for_user("test_user_001")
    for s in suggestions:
        print(f"{s['icon']} {s['title']}")
        print(f"   → {s['description']}")
        if s.get('tip'):
            print(f"   💡 {s['tip']}")
        print()
    
    # Test 2: User who just uploaded a photo
    print("\n=== User Just Uploaded Photo ===")
    suggestions = widget.get_suggestions_for_user(
        "test_user_002",
        context={'just_uploaded': 'photo'}
    )
    for s in suggestions:
        print(f"{s['icon']} {s['title']} — {s['reason']}")
        print(f"   → {s['description']}")
        print()
    
    # Test 3: User facing eviction
    print("\n=== User Facing Eviction ===")
    suggestions = widget.get_suggestions_for_user(
        "test_user_003",
        context={'situation': 'facing_eviction'}
    )
    for s in suggestions:
        priority = "🔥" if s['priority'] == 'high' else "⭐" if s['priority'] == 'medium' else "💡"
        print(f"{priority} {s['icon']} {s['title']}")
        print(f"   → {s['description']}")
        print(f"   📊 Success rate: {s['success_rate']}%")
        if s.get('warning'):
            print(f"   ⚠️  {s['warning']}")
        print()
