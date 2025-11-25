import os
import json
import time
import uuid
import secrets
from datetime import datetime, timedelta
# ============================================================================
# removed PERSISTENCE_OVERRIDE auto-set (using real R2 now)
# CRITICAL: Enforce persistent storage requirement
# App will NOT START without R2/GCS/Persistent Disk configured
# ============================================================================
from services.storage_enforcer import enforce_storage_requirement
enforce_storage_requirement(strict=False)  # Warn in dev, block in prod (RENDER/PRODUCTION env)
# ============================================================================
from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session, send_file, Response
from security import _get_or_create_csrf_token, _load_json, ADMIN_FILE, incr_metric, validate_admin_token, validate_user_token, _hash_token, check_rate_limit, is_breakglass_active, consume_breakglass, log_event, record_request_latency, _require_admin_or_401, _atomic_write_json
from engines.prime_learning_engine import create_seed_data
import hashlib
import requests
from user_database import (
    create_pending_user, verify_code, get_pending_user, get_user,
    resend_verification_code, mask_contact, update_user_login, log_user_interaction,
    check_existing_user, generate_verification_code, hash_code)
from user_database import _get_db as get_user_db
from learning_adapter import generate_dashboard_for_user, LearningAdapter
from preliminary_learning_routes import learning_module_bp
from engines.ledger_calendar_engine import init_ledger_calendar
from ledger_calendar_routes import ledger_calendar_bp
from engines.data_flow_engine import init_data_flow
from data_flow_routes import data_flow_bp
from ledger_tracking_routes import ledger_tracking_bp
from ledger_admin_routes import ledger_admin_bp
from av_routes import av_routes_bp
from engines.learning_engine import init_learning
from learning_routes import learning_bp
from adaptive_registration import (
    register_user_adaptive,
    report_issue_adaptive,
    report_outcome_adaptive,
    contribute_resource_adaptive)
# Cards catalog model
try:
    from cards_model import get_cards_grouped, get_cards, init_cards_tables, seed_default_cards, seed_expanded_cards
except Exception:
    get_cards_grouped = None
    get_cards = None
    def init_cards_tables():
        pass
    def seed_default_cards():
        pass
    def seed_expanded_cards():
        pass
# Route Discovery & Dynamic Data Source Integration
# Route Discovery & Dynamic Data Source Integration\ntry:\n    from route_discovery_routes import route_discovery_bp, init_route_discovery_api\nexcept ImportError:\n    route_discovery_bp = None\n    init_route_discovery_api = None\n\n

app = Flask(__name__)


def _build_evidence_prompt(prompt: str, location: str, timestamp: str, form_type: str, form_data: dict) -> str:
    """Build an AI prompt for evidence collection guidance."""
    parts = [
        "You are a helpful assistant for tenant rights and evidence collection.",
        f"User request: {prompt}",
    ]
    
    if location:
        parts.append(f"Location: {location}")
    
    if timestamp:
        parts.append(f"Timestamp: {timestamp}")
    
    if form_type:
        form_type_readable = form_type.replace("_", " ")
        parts.append(f"Form type: {form_type_readable}")
    
    if form_data:
        parts.append(f"Form data provided: {', '.join(form_data.keys())}")
        for key, value in form_data.items():
            if value and len(str(value)) < 100:
                parts.append(f"  - {key}: {value}")
    
    parts.append("What evidence to collect and how to document it properly?")
    
    return "\n".join(parts)


app.secret_key = os.getenv('FLASK_SECRET_KEY') or os.getenv('FLASK_SECRET') or 'dev-secret'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FORCE_HTTPS') == '1' or os.getenv('SESSION_COOKIE_SECURE') == '1'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_DOMAIN'] = None  # Allow localhost
app.config['SESSION_TYPE'] = 'filesystem'  # Persist sessions
app.config['PERMANENT_SESSION_LIFETIME'] = 7 * 24 * 60 * 60  # 7 days (604800 seconds)

# Dev: make changes show immediately
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Register blueprints
try:
    app.register_blueprint(dashboard_api_bp)
    print('[OK] Dashboard API registered')
except NameError:
    print('[WARN] Dashboard API not available')


# REMOVED: Legacy registration - Semptify uses storage-based identity
# try:
#     from register import register_bp
#     app.register_blueprint(register_bp)
#     print('[OK] Registration blueprint registered')
# except ImportError as e:
#     print(f'[WARN] Registration blueprint not available: {e}')

try:
    from vault import vault_bp
    app.register_blueprint(vault_bp)
    print('[OK] Vault blueprint registered')
except ImportError as e:
    print(f'[WARN] Vault blueprint not available: {e}')


# ============================================================================
# BLUEPRINT REGISTRATION - Auto-discover and register available blueprints
# ============================================================================

# Core Features
blueprints_to_register = [
    ('calendar_api', 'calendar_api_bp'),
    ('calendar_hub_routes', 'calendar_hub_bp'),
    ('calendar_master', 'calendar_master_bp'),
    ('calendar_storage_routes', 'calendar_storage_bp'),
    ('calendar_timeline_routes', 'calendar_timeline_bp'),
    ('calendar_vault_api', 'calendar_vault_api'),
    ('calendar_vault_ui_routes', 'calendar_vault_ui_bp'),
    ('complaint_filing_routes', 'complaint_filing_bp'),
    ('data_flow_routes', 'data_flow_bp'),
    ('legal_routes', 'legal_bp'),
    ('ledger_routes', 'ledger_bp'),
    ('learning_routes', 'learning_bp'),
    ('learning_dashboard_routes', 'learning_dashboard_bp'),
    ('ollama_routes', 'ollama_bp'),
    ('brad_gui_routes', 'brad_bp'),
    ('help_hub_routes', 'help_hub_bp'),
    ('improvement_routes', 'improvement_bp'),
    ('journey_routes', 'journey_bp'),
    ('housing_programs_routes', 'housing_programs_bp'),
    ('demo_routes', 'demo_bp'),
    ('library_routes', 'library_bp'),
    ('library_hub_routes', 'library_hub_bp'),
    ('main_dashboard_routes', 'main_dashboard_bp'),
    ('storage_setup_routes', 'storage_setup_bp'),
    ('storage_autologin', 'storage_autologin_bp'),
    ('modern_gui_routes', 'modern_gui_bp'),

    # Additional Feature Blueprints
    ('ledger_tracking_routes', 'ledger_tracking_bp'),
    ('ledger_admin_routes', 'ledger_admin_bp'),
    ('ledger_calendar_routes', 'ledger_calendar_bp'),
    ('av_routes', 'av_routes_bp'),
    ('brad_integration_routes', 'integration_bp'),
    ('system_integration_routes', 'system_bp'),
    ('ai_orchestrator_routes', 'orchestrator_bp'),
    ('maintenance_routes', 'maintenance_bp'),
    ('migration_routes', 'migration_bp'),
    ('feature_admin_routes', 'feature_admin_bp'),
    ('doc_explorer_routes', 'doc_explorer_bp'),
    ('route_discovery_routes', 'route_discovery_bp'),
]

for module_name, bp_name in blueprints_to_register:
    try:
        module = __import__(module_name, fromlist=[bp_name])
        bp = getattr(module, bp_name)
        app.register_blueprint(bp)
        print(f'[OK] {bp_name} registered')
    except (ImportError, AttributeError) as e:
        print(f'[SKIP] {bp_name}: {e}')


# Add more blueprint registrations here...



# Complaint Context API - Auto-fill complaints using Context System
try:
    from complaint_context_api import complaint_context_api_bp
    app.register_blueprint(complaint_context_api_bp)
    print("[OK] Complaint Context API registered (/api/complaint/*)")
except ImportError as e:
    print(f"[WARN] Complaint Context API not available: {e}")

# Dakota County Eviction Defense Library
try:
    from dakota_eviction_library_routes import dakota_bp
    app.register_blueprint(dakota_bp)
    print('[OK] Dakota County Eviction Defense Library registered at /library/dakota')
except ImportError as e:
    print(f'[WARN] Dakota Library not available: {e}')
# Jurisdiction Engine - Auto-generate modules for any county/state
try:
    from jurisdiction_engine_routes import jurisdiction_engine_bp
    app.register_blueprint(jurisdiction_engine_bp)
    print('[OK] Jurisdiction Engine registered at /jurisdiction/*')
    print('     → Auto-generates modules for any county/state on-demand')
except ImportError as e:
    print(f'[WARN] Jurisdiction Engine not available: {e}')
# GUI Hub - Landing page and interface launcher
try:
    from gui_hub_routes import gui_hub_bp
    app.register_blueprint(gui_hub_bp)
    print('[OK] GUI Hub registered')
except ImportError as e:
    print(f'[WARN] GUI Hub not available: {e}')

# Master Admin - Control panel
try:
    from master_admin_routes import master_admin_bp
    app.register_blueprint(master_admin_bp)
    print('[OK] Master Admin registered')
except ImportError as e:
    print(f'[WARN] Master Admin not available: {e}')
# Context API - Context Data System™ access
try:
    from context_api_routes import context_api_bp
    app.register_blueprint(context_api_bp)
    print("[OK] Context API registered (/api/context/*)")
except ImportError as e:
    print(f"[WARN] Context API not available: {e}")

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/tools/court-packet-builder')
def court_packet_builder():
    return render_template('court_packet_builder.html')

@app.route('/')
def index():
    return render_template('dashboard_home.html')

@app.route('/admin')
def admin():
    if not _require_admin_or_401():
        return jsonify({"error": "Unauthorized"}), 401
    return render_template('admin.html', security_mode=os.getenv('SECURITY_MODE', 'open'), csrf_token=_get_or_create_csrf_token())



@app.route('/admin/status')
def admin_status():
    if not _require_admin_or_401():
        return jsonify({"error": "Unauthorized"}), 401
    from security import get_metrics
    return jsonify({"status": "ok", "metrics": get_metrics()})

# DISABLED (OAuth storage identity only) - @app.route('/register')
# 
# 
# DISABLED (OAuth storage identity only) - @app.route('/verify', methods=['GET', 'POST'])
# def verify():
    '''Verify user registration via email or phone'''
    if request.method == 'GET':
        return render_template('verify.html')
    # Process verification
    return redirect(url_for('index'))
# REMOVED: Legacy registration function
# def register():
#     return render_template('register.html')


@app.route('/copilot')
def copilot():
    return render_template('copilot.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/metrics')
def metrics():
    from security import get_metrics
    format_type = request.args.get("format", "json")
    accept = request.headers.get("Accept", "")
    if "text/plain" in accept or format_type == "prometheus":
        # Return Prometheus format
        metrics_data = get_metrics()
        output = []
        for key, value in metrics_data.items():
            if isinstance(value, (int, float)):
                output.append(f"{key} {value}")
        return Response("\n".join(output), mimetype="text/plain; charset=utf-8")
    metrics = get_metrics()
    from security import get_latency_stats
    metrics['latency_stats'] = get_latency_stats()
    return jsonify(metrics)

@app.route('/readyz')


# ============================================================================
# MISSING ROUTES - Stubs for incomplete features
# ============================================================================

@app.route('/vault/certificates')
def vault_certificates():
    '''List certificates for authenticated user'''
    from security import validate_user_token
    token = request.args.get('user_token') or request.headers.get('X-User-Token')
    user_id = validate_user_token(token)
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    # Return empty list for now
    return jsonify({"certificates": []}), 200

@app.route('/certified_post', methods=['GET', 'POST'])
def certified_post():
    '''Certified post tracking'''
    from security import validate_user_token
    token = request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')
    if not validate_user_token(token):
        return jsonify({"error": "unauthorized"}), 401
    if request.method == 'GET':
        return render_template('certified_post.html')
    return jsonify({"status": "created"}), 201

@app.route('/court_clerk', methods=['GET', 'POST'])
def court_clerk():
    '''Court clerk filing interface'''
    from security import validate_user_token
    token = request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')
    if not validate_user_token(token):
        return jsonify({"error": "unauthorized"}), 401
    if request.method == 'GET':
        return render_template('court_clerk.html')
    return jsonify({"status": "filed"}), 200

@app.route('/resources/witness_statement', methods=['GET'])
def witness_statement():
    '''Witness statement form'''
    return render_template('witness_statement.html')

@app.route('/resources/witness_statement_save', methods=['POST'])
def witness_statement_save():
    '''Save witness statement'''
    from security import validate_user_token
    token = request.form.get('user_token')
    if not validate_user_token(token):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"status": "saved"}), 200

@app.route('/api/evidence-copilot', methods=['POST'])
def evidence_copilot():
    '''AI evidence collection guidance'''
    # Check CSRF in enforced mode
    if os.getenv('SECURITY_MODE') == 'enforced':
        csrf = request.json.get('csrf_token') if request.is_json else request.form.get('csrf_token')
        if not csrf:
            return jsonify({"error": "CSRF token required"}), 400
    return jsonify({"error": "AI provider not configured"}), 501

@app.route('/resources/download/<filename>')
def resource_download(filename):
    '''Download resource templates'''
    return jsonify({"error": "not found"}), 404
@app.route('/readyz')
def readyz():
    return jsonify({'status': 'ready'})

# Add more routes as needed...







# Research Tools - Landlord/property lookup
try:
    from research_routes import research_bp
    app.register_blueprint(research_bp)
    print("[OK] research_bp registered")
except ImportError as e:
    print(f"[WARN] Research routes not available: {e}")


