"""
Flask routes for Calendar Timeline API
Provides REST endpoints for timeline events and rent ledger
"""

from flask import Blueprint, request, jsonify, send_file, Response
from calendar_timeline import get_timeline_engine
from datetime import datetime
import io

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')


@calendar_bp.route('/events', methods=['GET'])
def get_events():
    """
    GET /api/calendar/events
    Query params:
      - start_date: ISO date (YYYY-MM-DD)
      - end_date: ISO date
      - types: comma-separated event types
      - status: upcoming|completed|missed|cancelled
      - user_id: filter by user
    """
    engine = get_timeline_engine()
    
    # Parse query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    types_param = request.args.get('types')
    event_types = types_param.split(',') if types_param else None
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    
    # Get filtered events
    events = engine.get_events(
        start_date=start_date,
        end_date=end_date,
        event_types=event_types,
        status=status,
        user_id=user_id
    )
    
    return jsonify({
        'success': True,
        'count': len(events),
        'events': events
    })


@calendar_bp.route('/events', methods=['POST'])
def create_event():
    """
    POST /api/calendar/events
    Body: {
      "type": "rent_payment|court_date|deadline|...",
      "date": "2025-12-01",
      "title": "Event title",
      "description": "Optional description",
      "amount": 1200.00,  // Optional
      "status": "upcoming",  // Optional, default: upcoming
      "user_id": "user_123",  // Optional
      "metadata": {}  // Optional
    }
    """
    engine = get_timeline_engine()
    data = request.get_json()
    
    # Validate required fields
    required = ['type', 'date', 'title']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            'success': False,
            'error': f"Missing required fields: {', '.join(missing)}"
        }), 400
    
    # Create event
    try:
        event = engine.add_event(
            event_type=data['type'],
            date=data['date'],
            title=data['title'],
            description=data.get('description', ''),
            amount=data.get('amount'),
            status=data.get('status', 'upcoming'),
            user_id=data.get('user_id'),
            metadata=data.get('metadata')
        )
        
        return jsonify({
            'success': True,
            'event': event
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@calendar_bp.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """
    PUT /api/calendar/events/<event_id>
    Body: { "field": "new_value", ... }
    """
    engine = get_timeline_engine()
    data = request.get_json()
    
    # Don't allow changing ID or created_at
    data.pop('id', None)
    data.pop('created_at', None)
    
    success = engine.update_event(event_id, data)
    
    if success:
        return jsonify({'success': True, 'message': 'Event updated'})
    else:
        return jsonify({'success': False, 'error': 'Event not found'}), 404


@calendar_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """DELETE /api/calendar/events/<event_id>"""
    engine = get_timeline_engine()
    
    success = engine.delete_event(event_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Event deleted'})
    else:
        return jsonify({'success': False, 'error': 'Event not found'}), 404


@calendar_bp.route('/rent-ledger', methods=['GET'])
def get_rent_ledger():
    """
    GET /api/calendar/rent-ledger
    Query params:
      - user_id: filter by user
    """
    engine = get_timeline_engine()
    user_id = request.args.get('user_id')
    
    ledger = engine.get_rent_ledger(user_id)
    
    return jsonify({
        'success': True,
        'ledger': ledger
    })


@calendar_bp.route('/deadlines', methods=['GET'])
def get_deadlines():
    """
    GET /api/calendar/deadlines
    Query params:
      - days_ahead: int (default: 30)
      - user_id: filter by user
    """
    engine = get_timeline_engine()
    
    days_ahead = int(request.args.get('days_ahead', 30))
    user_id = request.args.get('user_id')
    
    deadlines = engine.get_upcoming_deadlines(days_ahead, user_id)
    
    return jsonify({
        'success': True,
        'count': len(deadlines),
        'deadlines': deadlines
    })


@calendar_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    GET /api/calendar/statistics
    Query params:
      - user_id: filter by user
    """
    engine = get_timeline_engine()
    user_id = request.args.get('user_id')
    
    stats = engine.get_statistics(user_id)
    
    return jsonify({
        'success': True,
        'statistics': stats
    })


@calendar_bp.route('/export/ical', methods=['GET', 'POST'])
def export_ical():
    """
    GET/POST /api/calendar/export/ical
    Query params (GET) or body (POST):
      - event_ids: comma-separated list of event IDs to export
    
    Returns iCal file for download
    """
    engine = get_timeline_engine()
    
    if request.method == 'POST':
        data = request.get_json()
        event_ids_param = data.get('event_ids')
    else:
        event_ids_param = request.args.get('event_ids')
    
    event_ids = event_ids_param.split(',') if event_ids_param else None
    
    # Generate iCal content
    ical_content = engine.export_to_ical(event_ids)
    
    # Create file-like object
    ical_file = io.BytesIO(ical_content.encode('utf-8'))
    ical_file.seek(0)
    
    # Generate filename with timestamp
    filename = f"semptify_timeline_{datetime.now().strftime('%Y%m%d')}.ics"
    
    return send_file(
        ical_file,
        mimetype='text/calendar',
        as_attachment=True,
        download_name=filename
    )


@calendar_bp.route('/types', methods=['GET'])
def get_event_types():
    """GET /api/calendar/types - List all available event types with metadata"""
    engine = get_timeline_engine()
    
    return jsonify({
        'success': True,
        'event_types': engine.event_types
    })


# Error handlers
@calendar_bp.errorhandler(400)
def bad_request(e):
    return jsonify({'success': False, 'error': 'Bad request'}), 400


@calendar_bp.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@calendar_bp.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


def register_calendar_routes(app):
    """Register calendar blueprint with Flask app"""
    app.register_blueprint(calendar_bp)
    print("✅ Calendar timeline routes registered at /api/calendar/*")
