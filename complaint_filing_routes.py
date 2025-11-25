# Routes for comprehensive complaint filing system
# Multi-venue filing, always up-to-date procedures

from flask import Blueprint, render_template, request, jsonify, session
from engines.complaint_filing_engine import get_filing_engine, VenueType
from engines.accuracy_engine import get_accuracy_engine
import json


# ============================================================================
# CONTEXT INTEGRATION - Auto-fill from uploaded documents
# ============================================================================

def get_user_context_data(user_token):
    """
    Fetch user's context data from unified Context System.
    Returns: {
        'user': user_info,
        'documents': [uploaded docs with intelligence],
        'timeline': timeline events,
        'case_data': extracted case information
    }
    """
    try:
        from security import validate_user_token
        user_id = validate_user_token(user_token)
        if not user_id:
            return None
        
        # Import context system
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from system_architecture import SystemState
        
        # Get comprehensive context
        context = {
            'user_id': user_id,
            'documents': [],
            'timeline': [],
            'case_data': {}
        }
        
        # Load vault documents with intelligence
        vault_dir = f"uploads/vault/{user_id}"
        if os.path.exists(vault_dir):
            for filename in os.listdir(vault_dir):
                if filename.endswith('.cert.json'):
                    cert_path = os.path.join(vault_dir, filename)
                    with open(cert_path, 'r') as f:
                        cert = json.load(f)
                        context['documents'].append(cert)
        
        # Load intelligence data
        intel_path = f"{vault_dir}/intelligence.json"
        if os.path.exists(intel_path):
            with open(intel_path, 'r') as f:
                intel = json.load(f)
                context['case_data']['intelligence'] = intel
        
        # Load timeline events
        from user_database import get_user_db
        conn = get_user_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT event_type, title, description, event_date, created_at
            FROM timeline_events
            WHERE user_id = ?
            ORDER BY event_date DESC
        ''', (user_id,))
        
        for row in cursor.fetchall():
            context['timeline'].append({
                'event_type': row[0],
                'title': row[1],
                'description': row[2],
                'event_date': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        
        # Extract key case data from documents
        context['case_data']['landlord_name'] = None
        context['case_data']['property_address'] = None
        context['case_data']['lease_start_date'] = None
        context['case_data']['monthly_rent'] = None
        context['case_data']['issue_description'] = None
        
        # Parse from intelligence if available
        if 'intelligence' in context['case_data']:
            intel = context['case_data']['intelligence']
            if 'parties' in intel:
                parties = intel.get('parties', [])
                for party in parties:
                    if party.get('role') == 'landlord':
                        context['case_data']['landlord_name'] = party.get('name')
            
            if 'monetary_amounts' in intel:
                amounts = intel.get('monetary_amounts', [])
                if amounts:
                    context['case_data']['monthly_rent'] = amounts[0].get('amount')
            
            if 'key_dates' in intel:
                dates = intel.get('key_dates', [])
                for date_obj in dates:
                    if 'lease_start' in date_obj.get('label', '').lower():
                        context['case_data']['lease_start_date'] = date_obj.get('date')
        
        return context
        
    except Exception as e:
        print(f"[ERROR] Context data fetch failed: {e}")
        return None

complaint_filing_bp = Blueprint('complaint_filing', __name__)

@complaint_filing_bp.route('/file-complaint', methods=['GET'])
def file_complaint_page():
    """
    Main complaint filing page.
    User describes issue, system identifies ALL venues.
    """
    return render_template('file_complaint.html')


@complaint_filing_bp.route('/api/complaint/identify-venues', methods=['POST'])
def identify_venues():
    """
    Identify all applicable filing venues for issue.
    Returns multi-venue strategy.
    """
    data = request.json

    issue_type = data.get('issue_type')
    location = data.get('location')  # {city, county, state, zip}
    user_situation = data.get('user_situation', {})
    urgency = data.get('urgency', 'normal')

    if not issue_type or not location:
        return jsonify({"error": "issue_type and location required"}), 400

    filing_engine = get_filing_engine()

    # Get comprehensive filing strategy
    strategy = filing_engine.generate_filing_strategy(
        issue_type=issue_type,
        location=location,
        user_situation=user_situation,
        urgency=urgency
    )

    return jsonify({
        "success": True,
        "strategy": strategy,
        "total_venues": len(strategy.get("immediate_actions", [])) + len(strategy.get("simultaneous_filings", [])),
        "confidence": strategy.get("success_probability")
    })


@complaint_filing_bp.route('/api/complaint/get-procedures/<venue_key>', methods=['POST'])
def get_filing_procedures(venue_key):
    """
    Get detailed step-by-step procedures for specific venue.
    Returns most up-to-date, verified procedures.
    """
    data = request.json
    location = data.get('location')

    filing_engine = get_filing_engine()
    accuracy_engine = get_accuracy_engine()

    # Get current procedures
    procedures = filing_engine._get_current_procedures(venue_key, location)

    # Verify accuracy
    verification = accuracy_engine.verify_guidance(
        guidance_type="filing_procedure",
        location_key=f"{location.get('city')}_{location.get('state')}",
        guidance_content=json.dumps(procedures),
        sources=[{"type": "official_website"}, {"type": "user_outcome"}]
    )

    return jsonify({
        "success": True,
        "procedures": procedures,
        "verification": {
            "confidence": verification.get("confidence"),
            "quality_level": verification.get("quality_level"),
            "last_verified": procedures.get("last_updated")
        }
    })


@complaint_filing_bp.route('/api/complaint/track-outcome', methods=['POST'])
def track_outcome():
    """
    User reports outcome of filing.
    System learns what works.
    """
    data = request.json

    venue_key = data.get('venue_key')
    location = data.get('location')
    issue_type = data.get('issue_type')
    outcome = data.get('outcome')  # {success, timeline, resolution, notes}

    if not all([venue_key, location, issue_type, outcome]):
        return jsonify({"error": "Missing required fields"}), 400

    filing_engine = get_filing_engine()

    # Track outcome for effectiveness scoring
    filing_engine.track_filing_outcome(
        venue_key=venue_key,
        location=location,
        issue_type=issue_type,
        outcome=outcome
    )

    # Also track in accuracy engine
    accuracy_engine = get_accuracy_engine()
    accuracy_engine.track_outcome(
        guidance_type="filing_venue",
        location_key=f"{location.get('city')}_{location.get('state')}",
        guidance_content=venue_key,
        outcome="success" if outcome.get("success") else "failure"
    )

    return jsonify({
        "success": True,
        "message": "Outcome recorded. Thank you for helping improve the system!"
    })


@complaint_filing_bp.route('/api/complaint/update-procedure', methods=['POST'])
def update_procedure():
    """
    User provides updated procedure info.
    Keeps procedures current.
    """
    data = request.json

    venue_key = data.get('venue_key')
    location = data.get('location')
    updated_procedure = data.get('procedure')

    if not all([venue_key, location, updated_procedure]):
        return jsonify({"error": "Missing required fields"}), 400

    filing_engine = get_filing_engine()

    filing_engine.update_procedures_from_outcome(
        venue_key=venue_key,
        location=location,
        updated_procedure=updated_procedure
    )

    return jsonify({
        "success": True,
        "message": "Procedure updated. Thank you!"
    })


@complaint_filing_bp.route('/complaint-library', methods=['GET'])
def complaint_library():
    """
    Browse all known venues and procedures.
    Searchable by issue type, location, agency.
    """
    filing_engine = get_filing_engine()

    # Get all venues
    all_venues = filing_engine.venues

    # Group by type
    federal_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') == 'federal'}
    state_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') == 'state'}
    local_venues = {k: v for k, v in all_venues.items() if v.get('jurisdiction') in ['city', 'county']}

    return render_template(
        'complaint_library.html',
        federal_venues=federal_venues,
        state_venues=state_venues,
        local_venues=local_venues,
        total_venues=len(all_venues)
    )


@complaint_filing_bp.route('/filing-success-stories', methods=['GET'])
def success_stories():
    """
    Show success stories by venue.
    Users see what works.
    """
    filing_engine = get_filing_engine()
    accuracy_engine = get_accuracy_engine()

    # Get outcomes data
    all_outcomes = filing_engine.outcomes

    # Find high-success venues
    success_stories = []
    for outcome_key, outcome_data in all_outcomes.items():
        if outcome_data.get("total_count", 0) >= 3:
            effectiveness = outcome_data.get("effectiveness", 0)
            if effectiveness >= 0.75:
                venue_key, location_key, issue_type = outcome_key.split(":")

                success_stories.append({
                    "venue_key": venue_key,
                    "location": location_key,
                    "issue_type": issue_type,
                    "success_rate": f"{int(effectiveness * 100)}%",
                    "case_count": outcome_data["total_count"],
                    "recent_outcomes": outcome_data.get("outcomes", [])[-3:]  # Last 3
                })

    # Sort by success rate
    success_stories.sort(key=lambda x: float(x["success_rate"].rstrip('%')), reverse=True)

    return render_template(
        'filing_success_stories.html',
        success_stories=success_stories
    )


@complaint_filing_bp.route('/api/complaint/autofill', methods=['POST'])
def autofill_complaint():
    """
    Auto-fill complaint form from user's context data.
    Returns pre-populated form fields from uploaded documents.
    """
    data = request.json
    user_token = data.get('user_token') or request.headers.get('X-User-Token')
    
    if not user_token:
        return jsonify({"error": "user_token required"}), 401
    
    # Get context data
    context = get_user_context_data(user_token)
    if not context:
        return jsonify({"error": "Could not load context data"}), 500
    
    # Build pre-filled form data
    form_data = {
        'tenant_name': None,  # Would come from user profile
        'landlord_name': context['case_data'].get('landlord_name'),
        'property_address': context['case_data'].get('property_address'),
        'lease_start_date': context['case_data'].get('lease_start_date'),
        'monthly_rent': context['case_data'].get('monthly_rent'),
        'issue_description': context['case_data'].get('issue_description'),
        'evidence_count': len(context['documents']),
        'evidence_files': [
            {
                'filename': doc.get('filename'),
                'doc_type': doc.get('intelligence', {}).get('doc_type'),
                'upload_date': doc.get('created')
            }
            for doc in context['documents']
            if doc.get('filename')
        ],
        'timeline_events': [
            {
                'date': event.get('event_date'),
                'description': event.get('title')
            }
            for event in context['timeline'][:10]  # Most recent 10
        ],
        'intelligence_available': 'intelligence' in context['case_data']
    }
    
    return jsonify({
        "success": True,
        "form_data": form_data,
        "context_loaded": True,
        "documents_found": len(context['documents']),
        "timeline_events_found": len(context['timeline'])
    })
