"""
Admin Control Panel - GUI for managing Semptify settings without terminal
Provides toggles, checkboxes, and easy controls for all system options
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from security import validate_admin_token, _get_or_create_csrf_token
import json
import os
from datetime import datetime
from user_database import _get_db

admin_panel_bp = Blueprint('admin_panel', __name__, url_prefix='/admin/panel')

CONFIG_FILE = 'data/admin_config.json'

def _load_config():
    """Load admin configuration"""
    os.makedirs('data', exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    # Default config
    return {
        'user_verification': {
            'email_enabled': True,
            'phone_enabled': False,  # Not ready yet
            'sms_enabled': False,
            'require_verification': True
        },
        'registration': {
            'allow_registration': True,
            'require_email': False,
            'require_phone': False,
            'manual_approval_required': False
        },
        'storage': {
            'allow_system_storage': True,
            'allow_user_storage': True,
            'require_storage_qualification': False,
            'default_backend': 'local'  # local, r2, google
        },
        'security': {
            'security_mode': 'open',  # open or enforced
            'rate_limiting_enabled': True,
            'csrf_enabled': True,
            'force_https': False
        },
        'features': {
            'vault_enabled': True,
            'complaint_filing_enabled': True,
            'timeline_enabled': True,
            'ai_assistance_enabled': True,
            'learning_engine_enabled': True
        }
    }

def _save_config(config):
    """Save admin configuration"""
    os.makedirs('data', exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

@admin_panel_bp.route('/')
def index():
    """Main admin control panel"""
    # Check admin token
    admin_token = request.args.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return "Unauthorized - Admin token required", 401
    
    config = _load_config()
    csrf_token = _get_or_create_csrf_token()
    
    return render_template('admin_control_panel.html', 
                         config=config, 
                         csrf_token=csrf_token,
                         admin_token=admin_token)

@admin_panel_bp.route('/update', methods=['POST'])
def update_config():
    """Update configuration from form"""
    admin_token = request.form.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    config = _load_config()
    
    # Update user verification settings
    config['user_verification']['email_enabled'] = request.form.get('email_enabled') == 'on'
    config['user_verification']['phone_enabled'] = request.form.get('phone_enabled') == 'on'
    config['user_verification']['require_verification'] = request.form.get('require_verification') == 'on'
    
    # Update registration settings
    config['registration']['allow_registration'] = request.form.get('allow_registration') == 'on'
    config['registration']['require_email'] = request.form.get('require_email') == 'on'
    config['registration']['manual_approval_required'] = request.form.get('manual_approval_required') == 'on'
    
    # Update storage settings
    config['storage']['allow_system_storage'] = request.form.get('allow_system_storage') == 'on'
    config['storage']['allow_user_storage'] = request.form.get('allow_user_storage') == 'on'
    config['storage']['default_backend'] = request.form.get('default_backend', 'local')
    
    # Update security settings
    config['security']['security_mode'] = request.form.get('security_mode', 'open')
    config['security']['rate_limiting_enabled'] = request.form.get('rate_limiting_enabled') == 'on'
    config['security']['csrf_enabled'] = request.form.get('csrf_enabled') == 'on'
    config['security']['force_https'] = request.form.get('force_https') == 'on'
    
    # Update feature toggles
    config['features']['vault_enabled'] = request.form.get('vault_enabled') == 'on'
    config['features']['complaint_filing_enabled'] = request.form.get('complaint_filing_enabled') == 'on'
    config['features']['timeline_enabled'] = request.form.get('timeline_enabled') == 'on'
    config['features']['ai_assistance_enabled'] = request.form.get('ai_assistance_enabled') == 'on'
    config['features']['learning_engine_enabled'] = request.form.get('learning_engine_enabled') == 'on'
    
    _save_config(config)
    
    return redirect(url_for('admin_panel.index', admin_token=admin_token, saved='true'))

@admin_panel_bp.route('/users')
def manage_users():
    """User management interface"""
    admin_token = request.args.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return "Unauthorized", 401
    
    # Get all users from database
    db = _get_db()
    cursor = db.execute('SELECT id, email, created_at, last_login FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    
    return render_template('admin_user_management.html',
                         users=users,
                         admin_token=admin_token)

@admin_panel_bp.route('/users/<int:user_id>/verify', methods=['POST'])
def verify_user(user_id):
    """Manually verify a user"""
    admin_token = request.form.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = _get_db()
    db.execute('UPDATE users SET verified = 1, verified_at = ? WHERE id = ?',
               (datetime.now().isoformat(), user_id))
    db.commit()
    
    return jsonify({'success': True, 'message': f'User {user_id} verified'})

@admin_panel_bp.route('/users/<int:user_id>/storage', methods=['POST'])
def toggle_user_storage(user_id):
    """Toggle user storage access"""
    admin_token = request.form.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    allowed = request.form.get('allowed') == 'true'
    
    db = _get_db()
    db.execute('UPDATE users SET storage_allowed = ? WHERE id = ?',
               (1 if allowed else 0, user_id))
    db.commit()
    
    return jsonify({'success': True, 'message': f'User {user_id} storage {"enabled" if allowed else "disabled"}'})

@admin_panel_bp.route('/users/create', methods=['POST'])
def create_user_manual():
    """Manually create and verify a user"""
    admin_token = request.form.get('admin_token') or request.headers.get('X-Admin-Token')
    if not validate_admin_token(admin_token):
        return jsonify({'error': 'Unauthorized'}), 401
    
    email = request.form.get('email')
    auto_verify = request.form.get('auto_verify') == 'on'
    storage_allowed = request.form.get('storage_allowed') == 'on'
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    db = _get_db()
    try:
        cursor = db.execute(
            'INSERT INTO users (email, created_at, verified, verified_at, storage_allowed) VALUES (?, ?, ?, ?, ?)',
            (email, datetime.now().isoformat(), 
             1 if auto_verify else 0,
             datetime.now().isoformat() if auto_verify else None,
             1 if storage_allowed else 0)
        )
        db.commit()
        user_id = cursor.lastrowid
        
        return jsonify({'success': True, 'user_id': user_id, 'message': f'User created: {email}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper function to check config in other modules
def get_config(section=None, key=None):
    """Get config value - can be imported by other modules"""
    config = _load_config()
    if section and key:
        return config.get(section, {}).get(key)
    elif section:
        return config.get(section, {})
    return config
