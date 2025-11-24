"""
Learning Dashboard API for Semptify
Mobile-first intelligent assistant that shows what the learning system is doing
"""

from flask import Blueprint, request, jsonify
from engines.learning_engine import get_learning
from engines.adaptive_intensity_engine import AdaptiveIntensityEngine
from engines.curiosity_engine import CuriosityEngine
from preliminary_learning import PreliminaryLearningModule
from user_database import log_user_interaction
from datetime import datetime

learning_dashboard_bp = Blueprint('learning_dashboard_api', __name__, url_prefix='/api/learning')


@learning_dashboard_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """
    Get intelligent next-action suggestions for the user.
    Returns what they should do next based on learned patterns.
    """
    user_id = request.args.get('user_id', 'demo_user')
    
    try:
        learning = get_learning()
        
        # Get user's last action from their history
        # In production, query user_interactions table
        last_action = request.args.get('last_action', 'register')
        
        # Get next suggestion
        next_action = learning.suggest_next_action(user_id, last_action)
        
        # Get all relevant suggestions
        suggestions = [
            {
                'id': 'document',
                'title': 'Document Everything',
                'icon': '📄',
                'reason': '83% of similar cases succeeded with thorough documentation',
                'priority': 1,
                'url': '/evidence/gallery'
            },
            {
                'id': 'timeline',
                'title': 'Build Timeline',
                'icon': '⏰',
                'reason': 'Clear timelines make your case 2x stronger',
                'priority': 2,
                'url': '/calendar-timeline'
            },
            {
                'id': 'evidence',
                'title': 'Gather Evidence',
                'icon': '📸',
                'reason': 'Photos and receipts win cases',
                'priority': 3,
                'url': '/evidence/gallery'
            }
        ]
        
        # Personalize based on learned patterns
        if next_action:
            # Promote the suggested action
            action_map = {
                'upload_evidence': 'evidence',
                'create_timeline': 'timeline',
                'file_complaint': 'document'
            }
            
            suggested_id = action_map.get(next_action, 'document')
            
            # Move suggested action to top
            suggestions = sorted(suggestions, 
                               key=lambda x: (x['id'] != suggested_id, x['priority']))
        
        return jsonify({
            'success': True,
            'next_action': {
                'id': suggestions[0]['id'],
                'title': suggestions[0]['title'],
                'icon': suggestions[0]['icon'],
                'reason': suggestions[0]['reason'],
                'action_text': 'Start Now',
                'url': suggestions[0]['url']
            },
            'suggestions': suggestions,
            'personalized': next_action is not None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'next_action': None,
            'suggestions': []
        }), 500


@learning_dashboard_bp.route('/intensity', methods=['GET'])
def get_intensity():
    """
    Get current intensity level based on situation.
    Shows how aggressive/collaborative the approach should be.
    """
    user_id = request.args.get('user_id', 'demo_user')
    
    try:
        intensity_engine = AdaptiveIntensityEngine()
        
        # In production, get actual landlord ID and situation from database
        landlord_id = request.args.get('landlord_id', 'demo_landlord')
        
        # Get current intensity recommendation
        situation_severity = request.args.get('severity', 'moderate')
        landlord_responsiveness = request.args.get('responsiveness', 'fair')
        
        # Determine intensity
        intensity = intensity_engine.determine_intensity(
            landlord_id=landlord_id,
            situation_severity=situation_severity,
            landlord_responsiveness=landlord_responsiveness
        )
        
        return jsonify({
            'success': True,
            'current_intensity': intensity.get('intensity_level', 'collaborative'),
            'description': intensity.get('description', 'Working together to resolve'),
            'actions': intensity.get('recommended_actions', []),
            'can_escalate': intensity.get('can_escalate', True),
            'can_deescalate': intensity.get('can_deescalate', False)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'current_intensity': 'collaborative'
        }), 500


@learning_dashboard_bp.route('/progress', methods=['GET'])
def get_progress():
    """
    Get user's progress through their journey.
    Shows how many steps completed, what's next.
    """
    user_id = request.args.get('user_id', 'demo_user')
    
    try:
        # In production, query user_learning_profiles table
        # For now, return demo data
        
        return jsonify({
            'success': True,
            'completed': 3,
            'total': 8,
            'current_step': 'Document evidence',
            'steps': [
                {'name': 'Create account', 'status': 'completed', 'icon': '✅'},
                {'name': 'Set up profile', 'status': 'completed', 'icon': '✅'},
                {'name': 'Upload lease', 'status': 'completed', 'icon': '✅'},
                {'name': 'Document evidence', 'status': 'in-progress', 'icon': '🔄'},
                {'name': 'Build timeline', 'status': 'pending', 'icon': '⏸️'},
                {'name': 'Prepare complaint', 'status': 'pending', 'icon': '⏸️'},
                {'name': 'File complaint', 'status': 'pending', 'icon': '⏸️'},
                {'name': 'Track outcome', 'status': 'pending', 'icon': '⏸️'}
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'completed': 0,
            'total': 0
        }), 500


@learning_dashboard_bp.route('/curiosity/questions', methods=['GET'])
def get_curiosity_questions():
    """
    Get what the system is currently researching/learning.
    Shows curiosity questions being investigated.
    """
    try:
        curiosity = CuriosityEngine()
        
        # Get pending questions
        questions = curiosity.questions.get('pending', [])
        researching = curiosity.questions.get('researching', [])
        
        # Format for display
        display_questions = []
        
        for q in researching[:3]:  # Show top 3 active research
            display_questions.append({
                'question': q.get('question', ''),
                'research_status': f"Analyzing {q.get('context', {}).get('sample_size', 'data')}...",
                'icon': '🔍'
            })
        
        for q in questions[:2]:  # Show 2 pending
            display_questions.append({
                'question': q.get('question', ''),
                'research_status': 'Queued for research',
                'icon': '⏳'
            })
        
        return jsonify({
            'success': True,
            'questions': display_questions,
            'total_researching': len(researching),
            'total_pending': len(questions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'questions': []
        }), 500


@learning_dashboard_bp.route('/curiosity/ask', methods=['POST'])
def ask_curiosity_question():
    """
    Let users ask questions for the system to research.
    Adds to curiosity queue.
    """
    try:
        data = request.get_json()
        question = data.get('question')
        user_id = data.get('user_id', 'demo_user')
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        curiosity = CuriosityEngine()
        
        # Add user-submitted question
        question_entry = {
            'id': f"user_{datetime.now().timestamp()}",
            'type': 'user_submitted',
            'question': question,
            'submitted_by': user_id,
            'submitted_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        curiosity.questions['pending'].append(question_entry)
        curiosity._save_questions()
        
        # Log interaction
        log_user_interaction(
            user_id=user_id,
            interaction_type='question_asked',
            module_name='curiosity',
            metadata={'question': question}
        )
        
        return jsonify({
            'success': True,
            'message': 'Question added to research queue',
            'question_id': question_entry['id']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@learning_dashboard_bp.route('/track', methods=['POST'])
def track_interaction():
    """
    Track user interactions for learning.
    Called when user clicks suggestions, completes actions, etc.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        interaction_type = data.get('interaction_type')
        
        if not interaction_type:
            return jsonify({'success': False, 'error': 'No interaction type'}), 400
        
        # Log to learning engine
        learning = get_learning()
        learning.observe_action(
            user_id=user_id,
            action=interaction_type,
            context=data
        )
        
        # Log to database
        log_user_interaction(
            user_id=user_id,
            interaction_type=interaction_type,
            module_name=data.get('module_name', 'learning_dashboard'),
            success=data.get('success', True),
            metadata=data.get('metadata', {})
        )
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@learning_dashboard_bp.route('/knowledge', methods=['GET'])
def get_knowledge():
    """
    Get what the system knows about a topic.
    Access to preliminary learning knowledge base.
    """
    topic = request.args.get('topic', 'rental_procedures')
    
    try:
        preliminary = PreliminaryLearningModule()
        
        # Get knowledge for topic
        knowledge = preliminary.get_knowledge_by_category(topic)
        
        return jsonify({
            'success': True,
            'topic': topic,
            'knowledge': knowledge
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'knowledge': {}
        }), 500


@learning_dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get overall learning system statistics.
    How many patterns learned, predictions made, etc.
    """
    try:
        learning = get_learning()
        curiosity = CuriosityEngine()
        
        return jsonify({
            'success': True,
            'patterns_learned': len(learning.patterns.get('sequences', {})),
            'users_helped': len(learning.patterns.get('user_habits', {})),
            'questions_researched': len(curiosity.questions.get('answered', [])),
            'success_rate': _calculate_success_rate(learning),
            'active_research': len(curiosity.questions.get('researching', []))
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _calculate_success_rate(learning) -> float:
    """Calculate overall success rate from learning patterns"""
    success_rates = learning.patterns.get('success_rates', {})
    
    if not success_rates:
        return 0.0
    
    total_attempts = sum(r['attempts'] for r in success_rates.values())
    total_successes = sum(r['successes'] for r in success_rates.values())
    
    if total_attempts == 0:
        return 0.0
    
    return round((total_successes / total_attempts) * 100, 1)


def get_learning_engine():
    """Get or create learning engine instance"""
    return get_learning()


def register_learning_dashboard_api(app):
    """Register learning dashboard blueprint with Flask app"""
    app.register_blueprint(learning_dashboard_bp)
    print("✅ Learning dashboard API registered at /api/learning/*")
