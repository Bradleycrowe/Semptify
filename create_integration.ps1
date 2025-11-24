# Create unified integration routes
$integration_code = @'
"""
system_integration_routes.py
Unified routes that work across all GUIs
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect
from system_architecture import (
    UserRole, CaseStatus, SystemState, NavigationMenu,
    UserProfile, NotificationPriority, Notification
)
from user_database import get_user_db
import json

system_bp = Blueprint('system', __name__, url_prefix='/system')

# Global system state
_system_state = SystemState()

# ============================================================================
# UNIFIED USER CONTEXT
# ============================================================================

@system_bp.route('/context')
def get_context():
    """Get complete user context for any GUI"""
    user_id = session.get('user_id') or request.args.get('user_token')
    
    if not user_id:
        return jsonify({"error": "authentication required"}), 401
    
    context = _system_state.get_user_context(user_id)
    
    # Add real-time data
    context.update({
        "navigation": NavigationMenu.get_menu_for_role(context['profile'].role if context['profile'] else UserRole.TENANT),
        "notifications": _get_unread_notifications(user_id),
        "progress": _calculate_progress(user_id),
        "next_actions": _get_next_actions(user_id),
    })
    
    return jsonify(context)

# ============================================================================
# CROSS-GUI NAVIGATION
# ============================================================================

@system_bp.route('/navigate/<destination>')
def navigate(destination):
    """Smart navigation with state preservation"""
    user_id = session.get('user_id')
    
    # Map destinations to URLs
    routes = {
        "home": "/",
        "vault": "/vault",
        "timeline": "/timeline/assistant",
        "learn": "/app",
        "brad": "/brad",
        "court": "/complaint_filing",
        "evidence": "/witness_statement",
        "admin": "/admin",
    }
    
    target = routes.get(destination, "/")
    
    # Preserve user token in query string if not in session
    if not user_id:
        user_token = request.args.get('user_token')
        if user_token:
            target += f"?user_token={user_token}"
    
    return redirect(target)

# ============================================================================
# UNIFIED DASHBOARD
# ============================================================================

@system_bp.route('/dashboard')
def unified_dashboard():
    """Single dashboard showing all system status"""
    user_id = session.get('user_id') or request.args.get('user_token')
    
    if not user_id:
        return redirect('/register')
    
    # Get user profile
    profile = _system_state.active_users.get(user_id)
    if not profile:
        profile = _load_user_profile(user_id)
    
    # Get stats from all subsystems
    stats = {
        "documents": _count_documents(user_id),
        "timeline_events": _count_timeline_events(user_id),
        "tasks_pending": _count_tasks(user_id),
        "completion": _calculate_progress(user_id),
        "case_status": profile.case_status if profile else CaseStatus.INTAKE,
        "legal_stage": profile.legal_stage if profile else None,
    }
    
    # Get recommended next actions
    next_actions = _get_next_actions(user_id)
    
    # Get notifications
    notifications = _get_unread_notifications(user_id)
    
    return render_template('system/unified_dashboard.html',
                         profile=profile,
                         stats=stats,
                         next_actions=next_actions,
                         notifications=notifications,
                         navigation=NavigationMenu.get_menu_for_role(profile.role if profile else UserRole.TENANT))

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

@system_bp.route('/progress')
def progress():
    """Get user progress across all areas"""
    user_id = session.get('user_id') or request.args.get('user_token')
    
    if not user_id:
        return jsonify({"error": "authentication required"}), 401
    
    progress_data = {
        "overall": _calculate_progress(user_id),
        "documents": _calculate_document_progress(user_id),
        "timeline": _calculate_timeline_progress(user_id),
        "learning": _calculate_learning_progress(user_id),
        "legal_prep": _calculate_legal_prep_progress(user_id),
    }
    
    return jsonify(progress_data)

# ============================================================================
# NOTIFICATIONS
# ============================================================================

@system_bp.route('/notifications')
def get_notifications():
    """Get all notifications for user"""
    user_id = session.get('user_id') or request.args.get('user_token')
    
    if not user_id:
        return jsonify({"error": "authentication required"}), 401
    
    notifications = _get_all_notifications(user_id)
    
    return jsonify({
        "notifications": [n.__dict__ for n in notifications],
        "unread_count": len([n for n in notifications if not n.read])
    })

@system_bp.route('/notifications/<notif_id>/read', methods=['POST'])
def mark_notification_read(notif_id):
    """Mark notification as read"""
    user_id = session.get('user_id') or request.args.get('user_token')
    
    if not user_id:
        return jsonify({"error": "authentication required"}), 401
    
    # Mark as read in database
    _mark_notification_read(notif_id, user_id)
    
    return jsonify({"success": True})

# ============================================================================
# TASK ROUTING
# ============================================================================

@system_bp.route('/task/<task_type>')
def route_task(task_type):
    """Route user to appropriate GUI for task"""
    gui_url = _system_state.get_gui_for_task(task_type)
    
    user_token = request.args.get('user_token')
    if user_token:
        gui_url += f"?user_token={user_token}"
    
    return redirect(gui_url)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _load_user_profile(user_id):
    """Load user profile from database"""
    # TODO: Implement database loading
    return UserProfile(user_id, UserRole.TENANT)

def _count_documents(user_id):
    """Count documents in vault"""
    # TODO: Query vault
    return 0

def _count_timeline_events(user_id):
    """Count timeline events"""
    # TODO: Query calendar
    return 0

def _count_tasks(user_id):
    """Count pending tasks"""
    # TODO: Query task system
    return 0

def _calculate_progress(user_id):
    """Calculate overall progress percentage"""
    # TODO: Aggregate from all subsystems
    return 0

def _calculate_document_progress(user_id):
    """Documents collected vs required"""
    return {"collected": 0, "required": 10, "percent": 0}

def _calculate_timeline_progress(user_id):
    """Timeline completeness"""
    return {"events": 0, "gaps": 5, "percent": 0}

def _calculate_learning_progress(user_id):
    """Learning topics mastered"""
    return {"mastered": 0, "total": 20, "percent": 0}

def _calculate_legal_prep_progress(user_id):
    """Court preparation checklist"""
    return {"completed": 0, "total": 15, "percent": 0}

def _get_next_actions(user_id):
    """Get recommended next steps"""
    # TODO: Implement smart recommendations
    return [
        {"title": "Upload your lease", "url": "/vault", "priority": "high"},
        {"title": "Add rent payment dates", "url": "/timeline/assistant", "priority": "normal"},
        {"title": "Learn about your rights", "url": "/app", "priority": "normal"},
    ]

def _get_unread_notifications(user_id):
    """Get unread notifications"""
    # TODO: Query notification system
    return []

def _get_all_notifications(user_id):
    """Get all notifications"""
    # TODO: Query notification database
    return []

def _mark_notification_read(notif_id, user_id):
    """Mark notification as read in database"""
    # TODO: Update database
    pass
'@

Set-Content -Path system_integration_routes.py -Value $integration_code -Encoding utf8
Write-Host "✓ Created system_integration_routes.py" -ForegroundColor Green
