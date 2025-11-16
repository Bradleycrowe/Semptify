"""
Simple Reasoning Engine - Works with actual Semptify learning modules
Generates Cell A (situation) and Cell B (actions) content
"""

from engines.learning_engine import get_learning
from engines.adaptive_intensity_engine import get_adaptive_intensity
import json


class SimpleReasoningEngine:
    """Generate smart content for dashboard cells A and B"""
    
    def __init__(self):
        self.learning = get_learning()
        self.intensity = get_adaptive_intensity()
    
    def get_cell_content(self, user_id: str, context: dict = None) -> dict:
        """
        Generate content for cells A and B.
        
        Returns:
            {
                "cell_a": {
                    "title": "Your Situation",
                    "facts": [...],
                    "stats": {...}
                },
                "cell_b": {
                    "title": "What To Do",
                    "actions": [...]
                }
            }
        """
        context = context or {}
        issue_type = context.get("issue_type", "eviction")
        
        # Get personalized suggestions from learning engine
        suggestions = self.learning.get_personalized_suggestions(user_id)
        
        # Get intensity level
        intensity_level = self.intensity.get_current_level(user_id)
        
        # Build Cell A: Situation
        cell_a = self._build_situation(issue_type, intensity_level)
        
        # Build Cell B: Actions
        cell_b = self._build_actions(issue_type, intensity_level, suggestions)
        
        return {
            "cell_a": cell_a,
            "cell_b": cell_b
        }
    
    def _build_situation(self, issue_type: str, intensity: str) -> dict:
        """Build Cell A content - situation facts"""
        
        # Facts based on issue type
        facts_db = {
            "eviction": [
                "In most states, landlords must give 30-60 days notice",
                "Illegal evictions (lockouts without court order) are criminal",
                "You have the right to respond in court",
                "Retaliatory evictions are illegal in most jurisdictions"
            ],
            "rent": [
                "Late fees are limited by state law (typically 5-10%)",
                "Landlords cannot charge arbitrary fees",
                "Rent increases must follow legal notice periods",
                "You have right to receipts for all payments"
            ],
            "repairs": [
                "Landlords must maintain habitable conditions",
                "You can withhold rent for serious repair issues",
                "Emergency repairs can be deducted from rent",
                "Document all repair requests in writing"
            ]
        }
        
        stats = {
            "eviction": {
                "win_rate": "60% of tenants who respond to eviction win or settle",
                "documentation": "Tenants with evidence are 3x more likely to win"
            },
            "rent": {
                "disputes": "40% of rent disputes favor tenant with proper records",
                "illegal_fees": "Landlords charge illegal fees in 30% of cases"
            },
            "repairs": {
                "violations": "70% of rental units have at least 1 code violation",
                "success": "80% of documented repair requests get resolved"
            }
        }
        
        return {
            "title": "Your Situation: What You Need to Know",
            "facts": facts_db.get(issue_type, facts_db["eviction"])[:3],
            "stats": stats.get(issue_type, stats["eviction"]),
            "intensity": intensity
        }
    
    def _build_actions(self, issue_type: str, intensity: str, suggestions: list) -> dict:
        """Build Cell B content - what to do"""
        
        actions = []
        
        # Action 1: Always document
        actions.append({
            "priority": 1,
            "icon": "📸",
            "action": "Document Everything NOW",
            "why": "Evidence is your strongest protection",
            "how": "Take photos, save texts/emails, keep receipts",
            "link": "/vault"
        })
        
        # Action 2: Check deadlines (if serious)
        if intensity in ["firm", "maximum", "legal"]:
            actions.append({
                "priority": 2,
                "icon": "⏰",
                "action": "Know Your Deadlines",
                "why": "Missing a deadline can lose your case",
                "how": "Check court dates and filing deadlines",
                "link": "/calendar-timeline"
            })
        
        # Action 3: File forms (if legal intensity)
        if intensity in ["firm", "maximum"]:
            actions.append({
                "priority": 3,
                "icon": "📋",
                "action": "File Legal Response",
                "why": "You must respond to protect your rights",
                "how": "Use complaint filing to generate forms",
                "link": "/complaint-filing"
            })
        
        # Action 4: Know rights
        actions.append({
            "priority": 4,
            "icon": "📚",
            "action": "Study Your Rights",
            "why": "Landlords count on you not knowing the law",
            "how": "Review tenant protections in your area",
            "link": "/knowledge-base"
        })
        
        # Action 5: Track payments (if rent issue)
        if issue_type in ["rent", "eviction"]:
            actions.append({
                "priority": 5,
                "icon": "💰",
                "action": "Track All Payments",
                "why": "Proof of payment stops false claims",
                "how": "Record every rent payment you've made",
                "link": "/rent-ledger"
            })
        
        return {
            "title": "How This Affects You & What To Do",
            "impact": self._get_impact_statement(intensity),
            "actions": actions[:4],  # Top 4 actions
            "personalized": suggestions[:2] if suggestions else []
        }
    
    def _get_impact_statement(self, intensity: str) -> str:
        """Get impact statement based on intensity"""
        impacts = {
            "working_together": "This situation is manageable with proper documentation and knowledge.",
            "positive_support": "Take proactive steps now to protect yourself.",
            "legal": "This requires legal action. Document everything and respond quickly.",
            "firm": "This is serious. Immediate legal response is critical.",
            "maximum": "URGENT: Take immediate action to protect your rights."
        }
        return impacts.get(intensity, impacts["positive_support"])


# Global instance
_reasoning = None

def get_reasoning() -> SimpleReasoningEngine:
    """Get reasoning engine instance"""
    global _reasoning
    if _reasoning is None:
        _reasoning = SimpleReasoningEngine()
    return _reasoning
