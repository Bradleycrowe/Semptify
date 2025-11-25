"""
Journey Progress Blueprint
Shows user's 5-stage progression: Newcomer → Documenting → Learning → Organizing → Ready
"""
from flask import
from curiosity_hooks import on_journey_step_completed Blueprint, render_template, request, jsonify
from journey_automation import get_user_stage, get_next_milestone, get_stage_progress, check_and_advance

journey_bp = Blueprint('journey', __name__, url_prefix='/journey')

@journey_bp.route('/')
def journey_home():
    """Display user's journey progress"""
    user_token = request.args.get('user_token') or request.form.get('user_token') or request.headers.get('X-User-Token')
    
    if not user_token:
        return render_template('journey_start.html')
    
    # Get user's journey data
    stage = get_user_stage(user_token) or 'newcomer'
    progress = get_stage_progress(user_token)
    milestone = get_next_milestone(user_token)
    
    stages = [
        {'name': 'Newcomer', 'value': 'newcomer', 'icon': 'fa-user-plus', 'color': 'secondary'},
        {'name': 'Documenting', 'value': 'documenting', 'icon': 'fa-upload', 'color': 'primary'},
        {'name': 'Learning', 'value': 'learning', 'icon': 'fa-graduation-cap', 'color': 'info'},
        {'name': 'Organizing', 'value': 'organizing', 'icon': 'fa-sitemap', 'color': 'warning'},
        {'name': 'Ready', 'value': 'ready', 'icon': 'fa-check-circle', 'color': 'success'}
    ]
    
    return render_template('journey_progress.html',
                         current_stage=stage,
                         stages=stages,
                         progress=progress,
                         next_milestone=milestone,
                         user_token=user_token)

@journey_bp.route('/api/check-progress', methods=['POST'])
def api_check_progress():
    """API endpoint to check and advance journey progress"""
    data = request.json
    user_token = data.get('user_token')
    action_type = data.get('action_type')  # 'upload', 'event', 'module_complete'
    
    if not user_token or not action_type:
        return jsonify({'error': 'Missing user_token or action_type'}), 400
    
    # Check if user advanced
    result = check_and_advance(user_token, action_type)

    # Trigger curiosity: What happens next in journey?
    try:
        if result.get('advanced'):
            question = on_journey_step_completed(user_token, result.get('new_stage', action_type), result)
            if question:
                print(f'[CURIOSITY] {question}')
    except Exception as e:
        print(f'[WARN] Curiosity hook failed: {e}')
    
    return jsonify(result)
