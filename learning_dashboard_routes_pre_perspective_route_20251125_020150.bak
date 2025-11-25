"""
Learning Dashboard API Routes
Mobile-first API for adaptive learning system
"""

from flask import Blueprint, jsonify, request, render_template
from engines.learning_engine import LearningEngine
from engines.adaptive_intensity_engine import AdaptiveIntensityEngine
from engines.curiosity_engine import CuriosityEngine
from learning_adapter import LearningAdapter
from user_database import _get_db  # Only for logging actions
from semptify_core import get_context  # Context Data System
from datetime import datetime, timedelta
import json

learning_dashboard_bp = Blueprint('learning_dashboard', __name__)

# Initialize engines (lazy loading)
_learning_engine = None
_intensity_engine = None
_curiosity_engine = None
_learning_adapter = None

def get_learning_engine():
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = LearningEngine()
    return _learning_engine

def get_intensity_engine():
    global _intensity_engine
    if _intensity_engine is None:
        _intensity_engine = AdaptiveIntensityEngine()
    return _intensity_engine

def get_curiosity_engine():
    global _curiosity_engine
    if _curiosity_engine is None:
        _curiosity_engine = CuriosityEngine()
    return _curiosity_engine

def get_learning_adapter():
    global _learning_adapter
    if _learning_adapter is None:
        _learning_adapter = LearningAdapter()
    return _learning_adapter


@learning_dashboard_bp.route('/dashboard')
def dashboard():
    """Render mobile-first learning dashboard"""
    return render_template('learning_dashboard.html')


@learning_dashboard_bp.route('/api/learning/dashboard')
def get_dashboard_data():
    """
    GET /api/learning/dashboard
    Returns personalized dashboard data for current user
    """
    user_id = request.args.get('user_id', 'demo_user')
    
    learning = get_learning_engine()
    intensity = get_intensity_engine()
    curiosity = get_curiosity_engine()
    
    # Get context from Context Data System
    context = get_context(str(user_id))
    
    # Extract user data
    user_row = context.user if context and context.user else None
    
    if not user_row:
        # Demo data for testing
        return jsonify({
            'success': True,
            'intensity': {
                'level': 'collaborative',
                'reason': 'Working with responsive landlord'
            },
            'stats': {
                'actions_today': 0,
                'progress': 10,
                'deadlines': 0,
                'streak': 1
            },
            'journey': {
                'stage': 'Getting Started',
                'progress': 10
            },
            'insights': [
                {
                    'icon': '👋',
                    'text': 'Welcome! I\'m learning about your situation to provide better guidance.'
                }
            ],
            'actions': [
                {
                    'id': 'complete_profile',
                    'text': 'Complete your profile to get personalized suggestions',
                    'confidence': 100
                }
            ],
            'curiosity': []
        })
    
    # Convert row to dict
    user_data = dict(user_row)
    
    # Get intensity level (check if we have situation data)
    intensity_level = 'collaborative'  # Default
    intensity_reason = 'Working on your case'
    
    # Get recent interactions
    cursor.execute('''
        SELECT interaction_type, COUNT(*) as count
        FROM user_interactions
        WHERE user_id = ?
          AND timestamp > datetime('now', '-1 day')
        GROUP BY interaction_type
    ''', (user_id,))
    
    today_actions = sum(row['count'] for row in cursor.fetchall())
    
    # Get journey progress
    stage = user_data.get('stage', 'SEARCHING')
    journey_progress = user_data.get('journey_progress', 0)
    
    # Calculate streak
    cursor.execute('''
        SELECT COUNT(DISTINCT DATE(timestamp)) as days
        FROM user_interactions
        WHERE user_id = ?
          AND timestamp > datetime('now', '-7 days')
    ''', (user_id,))
    
    streak_row = cursor.fetchone()
    streak = streak_row['days'] if streak_row else 0
    
    # Get upcoming deadlines from calendar
    cursor.execute('''
        SELECT COUNT(*) as count
        FROM timeline_events
        WHERE user_id = ?
          AND status = 'upcoming'
          AND date BETWEEN date('now') AND date('now', '+7 days')
    ''', (user_id,))
    
    deadlines_row = cursor.fetchone()
    deadlines = deadlines_row['count'] if deadlines_row else 0
    
    conn.close()
    
    # Generate insights based on learning patterns
    insights = generate_insights(user_id, learning)
    
    # Get suggested actions
    actions = generate_actions(user_id, stage, learning)
    
    # Get curiosity questions
    curiosity_questions = get_active_questions(curiosity, user_id)
    
    return jsonify({
        'success': True,
        'intensity': {
            'level': intensity_level,
            'reason': intensity_reason
        },
        'stats': {
            'actions_today': today_actions,
            'progress': journey_progress,
            'deadlines': deadlines,
            'streak': streak
        },
        'journey': {
            'stage': format_stage(stage),
            'progress': journey_progress
        },
        'insights': insights,
        'actions': actions,
        'curiosity': curiosity_questions
    })


@learning_dashboard_bp.route('/api/learning/action', methods=['POST'])
def log_action():
    """
    POST /api/learning/action
    Log user action for learning system
    Body: { "action_id": "upload_lease", "user_id": "user_123" }
    """
    data = request.get_json()
    action_id = data.get('action_id')
    user_id = data.get('user_id', 'demo_user')
    
    learning = get_learning_engine()
    
    # Observe the action
    learning.observe_action(user_id, action_id, {
        'timestamp': datetime.now().isoformat(),
        'success': True  # Will be updated by feedback
    })
    
    # Log to database
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_interactions (
            user_id, interaction_type, timestamp, success
        ) VALUES (?, ?, ?, ?)
    ''', (user_id, action_id, datetime.now().isoformat(), True))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'action': action_id})


@learning_dashboard_bp.route('/api/learning/feedback', methods=['POST'])
def submit_feedback():
    """
    POST /api/learning/feedback
    User feedback on suggestions
    Body: { "helpful": true/false, "user_id": "user_123" }
    """
    data = request.get_json()
    helpful = data.get('helpful', False)
    user_id = data.get('user_id', 'demo_user')
    
    learning = get_learning_engine()
    
    # Update success rate for recent actions
    # This helps the learning engine improve predictions
    
    # Log feedback
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_interactions (
            user_id, interaction_type, timestamp, success, metadata
        ) VALUES (?, ?, ?, ?, ?)
    ''', (
        user_id,
        'feedback',
        datetime.now().isoformat(),
        helpful,
        json.dumps({'helpful': helpful})
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'feedback': 'helpful' if helpful else 'not_helpful'})


@learning_dashboard_bp.route('/api/learning/curiosity/questions')
def get_curiosity_questions():
    """
    GET /api/learning/curiosity/questions
    Get active research questions from curiosity engine
    """
    curiosity = get_curiosity_engine()
    
    pending = curiosity.questions.get('pending', [])
    researching = curiosity.questions.get('researching', [])
    
    all_questions = pending[:3] + researching[:2]  # Top 5 questions
    
    return jsonify({
        'success': True,
        'questions': all_questions,
        'count': len(all_questions)
    })


@learning_dashboard_bp.route('/api/learning/curiosity/answer', methods=['POST'])
def answer_curiosity_question():
    """
    POST /api/learning/curiosity/answer
    Submit answer to research question
    Body: { "question_id": "q123", "answer": "...", "source": "..." }
    """
    data = request.get_json()
    question_id = data.get('question_id')
    answer = data.get('answer')
    source = data.get('source', 'user')
    
    curiosity = get_curiosity_engine()
    
    # Find and update question
    for q in curiosity.questions.get('researching', []):
        if q.get('id') == question_id:
            curiosity.answer_question(question_id, answer, source)
            return jsonify({'success': True, 'message': 'Answer recorded'})
    
    return jsonify({'success': False, 'error': 'Question not found'}), 404


# Helper functions

def generate_insights(user_id: str, learning: LearningEngine) -> list:
    """Generate personalized insights based on learning patterns"""
    insights = []
    
    # Check user habits
    if user_id in learning.patterns.get('user_habits', {}):
        habits = learning.patterns['user_habits'][user_id]
        
        # Most common action
        if habits:
            top_action = max(habits, key=habits.get)
            insights.append({
                'icon': '📊',
                'text': f'You often {format_action(top_action)}. Keep up the good work!'
            })
    
    # Check time patterns
    current_hour = datetime.now().hour
    if current_hour in learning.patterns.get('time_patterns', {}):
        common_actions = learning.patterns['time_patterns'][current_hour].most_common(1)
        if common_actions:
            action = common_actions[0][0]
            insights.append({
                'icon': '⏰',
                'text': f'Good time to {format_action(action)} - you\'re usually productive now.'
            })
    
    # Success rate feedback
    if not insights:
        insights.append({
            'icon': '🌟',
            'text': 'I\'m learning your preferences to provide better suggestions.'
        })
    
    return insights[:3]  # Top 3 insights


def generate_actions(user_id: str, stage: str, learning: LearningEngine) -> list:
    """Generate suggested next actions"""
    actions = []
    
    # Stage-specific actions
    stage_actions = {
        'SEARCHING': [
            {'id': 'search_housing', 'text': 'Search available housing in your area', 'confidence': 90},
            {'id': 'check_rights', 'text': 'Learn your rights as a tenant', 'confidence': 85},
        ],
        'HAVING_TROUBLE': [
            {'id': 'document_issue', 'text': 'Document the issue with photos and notes', 'confidence': 95},
            {'id': 'contact_landlord', 'text': 'Contact landlord in writing about the issue', 'confidence': 90},
        ],
        'MOVING_IN': [
            {'id': 'inspection', 'text': 'Complete move-in inspection checklist', 'confidence': 100},
            {'id': 'upload_lease', 'text': 'Upload your signed lease agreement', 'confidence': 95},
        ],
        'CONFLICT': [
            {'id': 'send_notice', 'text': 'Send formal written notice to landlord', 'confidence': 92},
            {'id': 'gather_evidence', 'text': 'Gather all evidence and communications', 'confidence': 95},
        ],
        'LEGAL': [
            {'id': 'file_complaint', 'text': 'File formal complaint with housing authority', 'confidence': 90},
            {'id': 'court_prep', 'text': 'Prepare for court hearing', 'confidence': 88},
        ]
    }
    
    actions = stage_actions.get(stage, [])
    
    # Use learning engine to suggest next action
    if user_id in learning.patterns.get('user_habits', {}):
        habits = learning.patterns['user_habits'][user_id]
        if habits:
            last_action = max(habits, key=habits.get)
            suggested = learning.suggest_next_action(user_id, last_action)
            
            if suggested:
                actions.insert(0, {
                    'id': suggested,
                    'text': f'Continue with: {format_action(suggested)}',
                    'confidence': 88
                })
    
    return actions[:5]  # Top 5 actions


def get_active_questions(curiosity: CuriosityEngine, user_id: str) -> list:
    """Get active curiosity questions"""
    questions = []
    
    for q in curiosity.questions.get('researching', [])[:3]:
        questions.append({
            'id': q.get('id'),
            'question': q.get('question'),
            'context': q.get('trigger', 'Learning')
        })
    
    return questions


def format_stage(stage: str) -> str:
    """Format stage name for display"""
    stage_names = {
        'SEARCHING': 'Searching for Housing',
        'HAVING_TROUBLE': 'Having Issues',
        'MOVING_IN': 'Moving In',
        'CONFLICT': 'Resolving Conflict',
        'LEGAL': 'Legal Process'
    }
    return stage_names.get(stage, stage.replace('_', ' ').title())


def format_action(action: str) -> str:
    """Format action name for display"""
    return action.replace('_', ' ').title()

