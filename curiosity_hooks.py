"""
Curiosity Integration Helpers
Connects user actions throughout Semptify to the curiosity engine
"""
from engines.curiosity_engine import CuriosityEngine
from typing import Dict, Optional
import os

# Singleton instance
_curiosity = None

def get_curiosity() -> CuriosityEngine:
    """Get or create the global curiosity engine instance"""
    global _curiosity
    if _curiosity is None:
        _curiosity = CuriosityEngine(data_dir='data')
    return _curiosity

# ========================================================================
# USER ACTION HOOKS - Call these from blueprints
# ========================================================================

def on_document_uploaded(user_id: str, doc_info: Dict) -> Optional[str]:
    """
    Called when user uploads a document to vault
    Triggers curiosity about document type, patterns, next steps
    """
    curiosity = get_curiosity()
    
    filename = doc_info.get('filename', '').lower()
    doc_type = doc_info.get('category', 'unknown')
    
    # Detect if this is a new document type we haven't seen
    if doc_type == 'unknown' or 'eviction' in filename:
        question = curiosity.detect_knowledge_gap(
            topic=f"Document type: {filename}",
            why_needed=f"User uploaded {filename}, need to classify and suggest next steps"
        )
        return question
    
    return None

def on_calendar_event_added(user_id: str, event_data: Dict) -> Optional[str]:
    """
    Called when user adds calendar event
    Triggers curiosity about what documents they'll need, risks, next steps
    """
    curiosity = get_curiosity()
    
    event_type = event_data.get('event_type', '')
    
    # Ask what user should do next for this event type
    question = curiosity.detect_knowledge_gap(
        topic=f"Next steps after {event_type} event",
        why_needed=f"User added {event_type} to timeline, need to guide them"
    )
    
    return question

def on_learning_module_completed(user_id: str, module_name: str, outcome: Dict) -> Optional[str]:
    """
    Called when user completes a learning module
    Triggers curiosity about what they learned, if it helped, what's next
    """
    curiosity = get_curiosity()
    
    # Track that user learned this topic (for future suggestions)
    question = curiosity.detect_knowledge_gap(
        topic=f"Impact of learning module: {module_name}",
        why_needed=f"User completed {module_name}, need to measure if it helped their case"
    )
    
    return question

def on_user_diverges_from_suggestion(
    user_id: str, 
    our_suggestion: Dict, 
    user_action: Dict,
    result: Optional[Dict] = None
) -> Optional[str]:
    """
    Called when user does something different than what we suggested
    If it works better, learn from it!
    """
    curiosity = get_curiosity()
    
    if result and result.get('success'):
        question = curiosity.detect_user_correction(
            suggestion=our_suggestion,
            user_action=user_action,
            result=result
        )
        return question
    
    return None

def on_journey_step_completed(user_id: str, step_name: str, outcome: Dict) -> Optional[str]:
    """
    Called when user completes a step in their journey
    Tracks progress, suggests next steps, learns from outcomes
    """
    curiosity = get_curiosity()
    
    # Curiosity: What happens after users complete this step?
    question = curiosity.detect_knowledge_gap(
        topic=f"Outcomes after completing: {step_name}",
        why_needed=f"User finished {step_name}, need to predict what happens next"
    )
    
    return question

# ========================================================================
# SUGGESTION GETTERS - Call these to get curiosity-driven suggestions
# ========================================================================

def get_next_question_for_user(user_id: str, context: Dict) -> Optional[str]:
    """
    Get a smart follow-up question based on user's current context
    Returns: A question string, or None if no questions pending
    """
    curiosity = get_curiosity()
    
    # Get pending research questions
    pending = curiosity.questions.get('pending', [])
    
    if pending:
        # Return the highest priority question
        pending_sorted = sorted(pending, key=lambda q: {
            'high': 3, 'medium': 2, 'low': 1
        }.get(q.get('priority', 'low'), 0), reverse=True)
        
        return pending_sorted[0].get('question')
    
    return None

def get_learning_suggestions(user_id: str, recent_actions: list) -> list:
    """
    Based on what user has done, suggest what they should learn next
    Returns: List of learning module names
    """
    suggestions = []
    
    # Simple pattern matching for now
    for action in recent_actions:
        if action.get('type') == 'uploaded' and 'repair' in action.get('filename', '').lower():
            suggestions.append('habitability_laws')
        elif action.get('type') == 'calendar_event' and 'notice' in action.get('event_type', '').lower():
            suggestions.append('eviction_defenses')
    
    return list(set(suggestions))  # Remove duplicates
