"""
Chat Integration for Jurisdiction Engine
Auto-detects when user asks about courts/evictions and triggers module generation
"""

import re
from jurisdiction_engine.jurisdiction_generator import JurisdictionEngine

engine = JurisdictionEngine()

# Trigger keywords
TRIGGER_PHRASES = [
    'eviction', 'court', 'summons', 'landlord', 'tenant rights',
    'housing court', 'unlawful detainer', 'forcible entry',
    'district court', 'county court', 'facing eviction'
]

def should_trigger_jurisdiction_detection(user_message):
    """Check if message should trigger jurisdiction detection"""
    message_lower = user_message.lower()
    return any(phrase in message_lower for phrase in TRIGGER_PHRASES)

def process_jurisdiction_request(user_message):
    """
    Main entry point for chat integration
    Returns: dict with response and actions
    """
    
    # Check if we should process this
    if not should_trigger_jurisdiction_detection(user_message):
        return None
    
    # Detect jurisdiction
    jurisdiction = engine.detect_jurisdiction(user_message)
    
    if not jurisdiction:
        return {
            'type': 'jurisdiction_not_detected',
            'message': "I can help with eviction defense! Which county or state are you in?",
            'suggest_clarification': True
        }
    
    # Check if module exists
    module_exists = engine.module_exists(jurisdiction)
    
    if module_exists:
        module_name = engine._get_module_name(jurisdiction)
        return {
            'type': 'module_exists',
            'jurisdiction': jurisdiction,
            'message': f"Great! I have resources for {jurisdiction['full_name']}.",
            'action': 'redirect',
            'url': f"/library/{module_name}",
            'quick_links': {
                'Answer Builder': f"/jurisdiction_modules/{module_name}/flows/counterclaim_builder.html",
                'Timeline': f"/jurisdiction_modules/{module_name}/flows/timeline_tracker.html",
                'Resources': f"/library/{module_name}/resources"
            }
        }
    
    else:
        # Generate module on the fly!
        try:
            print(f"🚀 Auto-generating module for {jurisdiction['full_name']}")
            metadata = engine.generate_module(jurisdiction, user_context=user_message)
            
            return {
                'type': 'module_generated',
                'jurisdiction': jurisdiction,
                'message': f"✅ I just created a complete eviction defense toolkit for {jurisdiction['full_name']}! Give me one moment to set it up...",
                'action': 'redirect_after_setup',
                'url': metadata['url_prefix'],
                'metadata': metadata,
                'setup_required': True
            }
            
        except Exception as e:
            return {
                'type': 'generation_failed',
                'jurisdiction': jurisdiction,
                'message': f"I detected {jurisdiction['full_name']}, but encountered an issue setting up resources. I can still help with general eviction defense information.",
                'error': str(e),
                'fallback_url': '/eviction-help'
            }

# Example usage in chat endpoint
def chat_handler_with_jurisdiction(user_message, chat_history=None):
    """
    Enhanced chat handler that auto-generates jurisdiction modules
    Integrate this into your existing chat endpoint
    """
    
    # Check for jurisdiction request
    jurisdiction_response = process_jurisdiction_request(user_message)
    
    if jurisdiction_response:
        if jurisdiction_response['type'] == 'module_generated':
            # Module was just created - need to register blueprint
            from flask import current_app
            from jurisdiction_engine_routes import _register_module_blueprint
            _register_module_blueprint(jurisdiction_response['metadata'])
        
        return jurisdiction_response
    
    # Otherwise, proceed with normal chat handling
    return None

# Integration with existing Copilot chat
def enhance_copilot_response(user_query, copilot_response):
    """
    Post-process Copilot responses to add jurisdiction-specific resources
    """
    jurisdiction_info = process_jurisdiction_request(user_query)
    
    if jurisdiction_info and jurisdiction_info.get('type') in ['module_exists', 'module_generated']:
        # Append jurisdiction links to Copilot response
        copilot_response += f"\n\n📍 **Local Resources for {jurisdiction_info['jurisdiction']['full_name']}:**\n"
        for name, url in jurisdiction_info.get('quick_links', {}).items():
            copilot_response += f"- [{name}]({url})\n"
    
    return copilot_response
