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

# ========================================================================
# VAULT → LEARNING CONNECTION (Phase 3)
# ========================================================================

def suggest_learning_from_document(user_id: str, doc_info: Dict) -> Optional[Dict]:
    '''
    Analyze uploaded document and suggest relevant learning modules
    
    Args:
        user_id: User token
        doc_info: {filename, doc_type, category, doc_id}
    
    Returns:
        Dict with learning suggestions: {modules: [], resources: [], next_steps: []}
    '''
    from engines.learning_engine import get_learning
    
    filename = doc_info.get('filename', '').lower()
    doc_type = doc_info.get('doc_type', '').lower()
    category = doc_info.get('category', '').lower()
    
    suggestions = {
        'modules': [],
        'resources': [],
        'next_steps': []
    }
    
    # Pattern matching: Document type → Learning modules
    learning_triggers = {
        'eviction': {
            'modules': ['eviction_defenses', 'tenant_rights', 'court_procedures'],
            'resources': ['Legal aid contacts', 'Eviction timeline guide', 'Sample response letters'],
            'next_steps': [
                'Review your eviction notice for errors',
                'Calculate response deadline (usually 7-14 days)',
                'Gather evidence of rent payments',
                'Contact legal aid immediately'
            ]
        },
        'notice': {
            'modules': ['lease_termination', 'notice_requirements', 'your_options'],
            'resources': ['Notice period by state', 'Negotiation tips', 'Moving checklist'],
            'next_steps': [
                'Verify notice is legally valid',
                'Check your lease terms',
                'Respond in writing within 3 days',
                'Document the notice (photograph + save original)'
            ]
        },
        'repair': {
            'modules': ['habitability_laws', 'repair_requests', 'warranty_of_habitability'],
            'resources': ['Building code violations', 'Inspection request forms', 'Rent withholding laws'],
            'next_steps': [
                'Document the issue (photos/video)',
                'Send written repair request to landlord',
                'Give landlord 14 days to respond',
                'Keep all communication records'
            ]
        },
        'lease': {
            'modules': ['understanding_leases', 'common_lease_clauses', 'negotiation_strategies'],
            'resources': ['Lease clause red flags', 'Move-in checklist', 'Security deposit laws'],
            'next_steps': [
                'Read entire lease carefully',
                'Note any unusual clauses',
                'Take move-in photos/video',
                'Get everything in writing'
            ]
        },
        'payment': {
            'modules': ['payment_documentation', 'receipt_requirements', 'payment_disputes'],
            'resources': ['Rent receipt template', 'Payment tracking spreadsheet'],
            'next_steps': [
                'Always get written receipts',
                'Keep payment records for 7 years',
                'Note payment method and date',
                'Photograph checks before mailing'
            ]
        }
    }
    
    # Detect document type from filename/category
    detected_type = None
    for keyword, config in learning_triggers.items():
        if keyword in filename or keyword in doc_type or keyword in category:
            detected_type = keyword
            suggestions = config
            break
    
    # If no specific match, provide general guidance
    if not detected_type:
        suggestions = {
            'modules': ['document_organization', 'evidence_basics'],
            'resources': ['Documentation best practices', 'Evidence checklist'],
            'next_steps': [
                'Organize documents by date',
                'Keep originals safe',
                'Make copies for your records',
                'Note why this document is important'
            ]
        }
    
    # Record this in learning engine for future patterns
    learning = get_learning()
    learning.observe_action(
        user_id=user_id,
        action=f'uploaded_{detected_type or "document"}',
        context={'doc_id': doc_info.get('doc_id'), 'triggered_learning': True}
    )
    
    return suggestions
# ========================================================================
# PHASE 5: JOURNEY AUTOMATION - Auto-advance based on user progress
# ========================================================================

def auto_advance_journey(user_id: str, action: str, context: Dict) -> Optional[Dict]:
    '''
    Automatically detect milestones and advance user's journey
    
    Args:
        user_id: User token
        action: Action performed (upload, event, learning, etc.)
        context: Additional context about the action
    
    Returns:
        Dict with journey update: {advanced: bool, new_stage: str, milestone: str}
    '''
    from journey_automation import check_and_advance, get_user_stage
    
    # Map actions to journey milestones
    milestone_triggers = {
        'first_upload': lambda ctx: ctx.get('upload_count') == 1,
        'upload_5_docs': lambda ctx: ctx.get('upload_count', 0) >= 5,
        'add_timeline_event': lambda ctx: ctx.get('action_type') == 'calendar_event',
        'create_notary_cert': lambda ctx: ctx.get('has_certificate') == True,
        'complete_module': lambda ctx: ctx.get('action_type') == 'learning_complete',
        'track_rent_payment': lambda ctx: 'payment' in ctx.get('action_type', '').lower(),
        'log_maintenance': lambda ctx: 'repair' in ctx.get('action_type', '').lower() or 'maintenance' in ctx.get('action_type', '').lower(),
        'calendar_event': lambda ctx: ctx.get('action_type') == 'calendar_event'
    }
    
    # Detect which milestone was achieved
    milestone_detected = None
    for milestone, condition in milestone_triggers.items():
        if condition(context):
            milestone_detected = milestone
            break
    
    if milestone_detected:
        # Check and potentially advance journey
        result = check_and_advance(user_id, milestone_detected)
        
        old_stage = get_user_stage(user_id)
        new_stage = result.get('current_stage')
        
        return {
            'advanced': old_stage != new_stage,
            'new_stage': new_stage,
            'milestone': milestone_detected,
            'completed_milestones': result.get('completed_milestones', [])
        }
    
    return None

