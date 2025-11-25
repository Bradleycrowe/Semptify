# Routes for comprehensive complaint filing system
# Multi-venue filing, always up-to-date procedures

from flask import Blueprint, render_template, request, jsonify, session
from engines.complaint_filing_engine import get_filing_engine, VenueType
from engines.accuracy_engine import get_accuracy_engine
import json

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
