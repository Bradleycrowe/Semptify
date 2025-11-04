"""
Communication Suite Flask Blueprint Wrapper

Provides API endpoints for:
- Modal triggers (multilingual)
- Help texts (9 languages)
- Voice commands
- Form controls

All data flows through the calendar/ledger system.
"""

from flask import Blueprint, jsonify, request
import json
import os

# Create blueprint
comm_suite_bp = Blueprint(
    'communication_suite',
    __name__,
    url_prefix='/api/communication-suite'
)

# Configuration paths
BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    'CommunicationSuite',
    'FormalMethods'
)

def load_json_config(filename):
    """Load JSON configuration file from Communication Suite."""
    filepath = os.path.join(BASE_PATH, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Cache configurations
_modal_triggers_cache = None
_help_texts_cache = None

def get_modal_triggers():
    """Get modal triggers configuration."""
    global _modal_triggers_cache
    if _modal_triggers_cache is None:
        _modal_triggers_cache = load_json_config('modal_triggers.json')
    return _modal_triggers_cache

def get_help_texts():
    """Get multilingual help texts."""
    global _help_texts_cache
    if _help_texts_cache is None:
        _help_texts_cache = load_json_config('help_text_multilingual.json')
    return _help_texts_cache

# ============================================================
# API ENDPOINTS - All flow through calendar
# ============================================================

@comm_suite_bp.route('/triggers', methods=['GET'])
def get_triggers():
    """Get all modal trigger configurations."""
    return jsonify({
        'triggers': get_modal_triggers(),
        'status': 'ok'
    })

@comm_suite_bp.route('/triggers/<trigger_id>', methods=['GET'])
def get_trigger(trigger_id):
    """Get specific modal trigger by ID."""
    triggers = get_modal_triggers()
    trigger = triggers.get(trigger_id, {})
    if not trigger:
        return jsonify({'error': 'Trigger not found'}), 404
    return jsonify(trigger)

@comm_suite_bp.route('/help', methods=['GET'])
def get_help():
    """Get help texts for specified language."""
    language = request.args.get('lang', 'en')
    help_texts = get_help_texts()
    lang_help = help_texts.get(language, help_texts.get('en', {}))
    return jsonify({
        'language': language,
        'help': lang_help,
        'available_languages': list(help_texts.keys())
    })

@comm_suite_bp.route('/help/<language>', methods=['GET'])
def get_help_by_language(language):
    """Get help texts for specific language."""
    help_texts = get_help_texts()
    if language not in help_texts:
        return jsonify({
            'error': f'Language {language} not available',
            'available': list(help_texts.keys())
        }), 404
    return jsonify({
        'language': language,
        'help': help_texts[language]
    })

@comm_suite_bp.route('/config', methods=['GET'])
def get_all_config():
    """Get all Communication Suite configurations."""
    return jsonify({
        'triggers': get_modal_triggers(),
        'help_texts': get_help_texts(),
        'status': 'ok'
    })

@comm_suite_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of available languages."""
    help_texts = get_help_texts()
    return jsonify({
        'languages': list(help_texts.keys()),
        'count': len(help_texts)
    })

@comm_suite_bp.route('/status', methods=['GET'])
def get_status():
    """Get Communication Suite status."""
    triggers = get_modal_triggers()
    help_texts = get_help_texts()
    return jsonify({
        'status': 'ok',
        'triggers_count': len(triggers),
        'languages': list(help_texts.keys()),
        'languages_count': len(help_texts)
    })
