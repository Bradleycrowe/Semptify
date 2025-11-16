"""Housing Journey API - Guided conversation that grows seed capabilities"""
from flask import Blueprint, request, jsonify, session
from engines.housing_journey_engine import HousingJourneyEngine
from seed_core import SeedCore
from seed_manager import SeedManager
from user_bucket_simulator import UserBucketSimulator
from engines.realtime_research_engine import RealTimeResearchEngine
from curiosity_reasoning_bridge import CuriosityReasoningBridge
import secrets

journey_bp = Blueprint('housing_journey', __name__, url_prefix='/api/journey')

# Session-based engines
_journey_engines = {}
_seed_managers = {}

def get_journey_engine():
    """Get or create journey engine for session."""
    session_id = session.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(16)
        session['session_id'] = session_id

    if session_id not in _journey_engines:
        _journey_engines[session_id] = HousingJourneyEngine()

    return _journey_engines[session_id]

def get_seed_manager():
    """Get or create seed manager for session."""
    session_id = session.get('session_id')
    if not session_id:
        return None

    if session_id not in _seed_managers:
        bucket = UserBucketSimulator(f"simulated_buckets/session_{session_id}")
        manager = SeedManager(bucket)
        manager.ensure_seed_exists({'session_id': session_id})
        _seed_managers[session_id] = manager

    return _seed_managers[session_id]

@journey_bp.route('/start', methods=['GET'])
def start_journey():
    """Start the housing journey conversation."""
    engine = get_journey_engine()
    start = engine.start_conversation()
    return jsonify(start)

@journey_bp.route('/respond', methods=['POST'])
def respond():
    """
    User responds to a journey question.
    Engine learns from response and grows needed capabilities.
    Now includes AI reasoning!
    """
    data = request.get_json()
    stage = data.get('stage')
    answer = data.get('answer')
    question_index = data.get('question_index', 0)

    # Apply client confirmation of jurisdiction, if provided
    if isinstance(data.get('jurisdiction_confirm'), dict):
        j = data['jurisdiction_confirm']
        session['jurisdiction_confirmed'] = bool(j.get('confirmed'))
        session['jurisdiction'] = j.get('state')

    if not stage or not answer:
        return jsonify({'error': 'Missing stage or answer'}), 400

    # Process with journey engine
    engine = get_journey_engine()
    result = engine.process_response(stage, answer, question_index)
    
    # Real-time official research (MN)
    try:
        research = RealTimeResearchEngine().research_holdover_rights(state='MN')
        result['citations'] = research.get('citations', [])
        result['presentations'] = research.get('presentations', {})
        result['verification_status'] = research.get('verification_status', 'unverified')
        result['preemption'] = research.get('preemption', {})
    except Exception as e:
        result['citations'] = []
        result['verification_status'] = 'unverified'
        result['research_error'] = str(e)
    
        # Passive assumptions (Phase 1): Jurisdiction candidate
    try:
        from engines.assumption_engine import AssumptionEngine
        ae = AssumptionEngine()
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        ctx = { 'text': answer, 'ip': ip }
        jur = ae.detect('jurisdiction', ctx) or {}
        jurisdiction_candidate = jur.get('state')
        jurisdiction_confidence = jur.get('confidence', 0.0)
        jurisdiction_sources = jur.get('sources', [])
    except Exception:
        jurisdiction_candidate = None
        jurisdiction_confidence = 0.0
        jurisdiction_sources = []
# NEW: AI Reasoning Integration
    try:
        bridge = CuriosityReasoningBridge()
        # Build facts from conversation
        facts = {
            'lease_status': 'ended' if stage == 'ended_lease' else stage,
            'still_in_unit': 'still in' in answer.lower() or 'not moved' in answer.lower(),
            'payment_current': 'paying' in answer.lower() or 'current' in answer.lower(),
            'paying_rent': 'paying rent' in answer.lower(),
            'notices_received': 'notice' in answer.lower() or 'eviction' in answer.lower(),
            'landlord_communication': 'threatening' if 'threat' in answer.lower() else 'accepting rent',
            'deposit_returned': 'deposit' in answer.lower() and 'returned' in answer.lower(),
            'timeline': answer  # Keep full answer for context
        }
        reasoning_result = bridge.analyze_with_context(facts, stage, answer)
        result['reasoning'] = reasoning_result
        result['assumptions'] = { 'jurisdiction': { 'candidate': jurisdiction_candidate, 'confidence': jurisdiction_confidence, 'sources': jurisdiction_sources } }
    except Exception as e:
        result['reasoning'] = None
        result['reasoning_error'] = str(e)
    
    # Grow capabilities in seed if needed
    seed_manager = get_seed_manager()
    grown_capabilities = []

    for capability_name in result['capabilities_to_grow']:
        if not seed_manager.seed.has_capability(capability_name):
            # Trigger seed to grow this capability
            grow_result = seed_manager.process_user_input(
                f"I need help with {capability_name.replace('_', ' ')}"
            )
            if grow_result.get('new_capability'):
                grown_capabilities.append(capability_name)

    # Add seed stats to response
    result['seed_stats'] = {
        'seed_id': seed_manager.seed.seed_id,
        'total_capabilities': len(seed_manager.seed.capabilities),
        'grown_this_turn': grown_capabilities
    }

    return jsonify(result)

@journey_bp.route('/execute/<capability>', methods=['POST'])
def execute_capability(capability):
    """Execute a grown capability with user's data."""
    data = request.get_json()

    seed_manager = get_seed_manager()
    if not seed_manager:
        return jsonify({'error': 'No session'}), 400

    # Check if capability exists
    if not seed_manager.seed.has_capability(capability):
        return jsonify({'error': 'Capability not found'}), 404

    # Execute
    result = seed_manager.process_user_input(data.get('input', ''))
    return jsonify(result)

@journey_bp.route('/status', methods=['GET'])
def status():
    """Get current session status."""
    engine = get_journey_engine()
    seed_manager = get_seed_manager()
    
    return jsonify({
        'facts_learned': len(engine.facts_learned),
        'capabilities': len(seed_manager.seed.capabilities) if seed_manager else 0
    })


@journey_bp.route('/jurisdiction', methods=['POST'])
def set_jurisdiction():
    """Set/confirm jurisdiction in session."""
    data = request.get_json() or {}
    state = (data.get('state') or '').upper() or None
    confirmed = bool(data.get('confirmed'))
    session['jurisdiction'] = state
    session['jurisdiction_confirmed'] = confirmed
    return jsonify({'ok': True, 'jurisdiction': state, 'confirmed': confirmed})



