"""
Calendar API for Semptify
Provides REST API for tenant calendar management, court dates, rent due dates, appointments
"""
from flask import Blueprint, request, jsonify, current_app
from security import _require_user_or_401, _require_admin_or_401
import json
import os
from datetime import datetime, timedelta
import secrets

calendar_api_bp = Blueprint('calendar_api', __name__, url_prefix='/api/calendar')


def _get_calendar_file(user_id=None):
    """Get path to calendar JSON file"""
    if user_id:
        # User-specific calendar
        path = os.path.join(current_app.root_path, 'uploads', 'calendars', f'{user_id}.json')
    else:
        # Global calendar (admin use)
        path = os.path.join(current_app.root_path, 'uploads', 'calendars', 'global.json')

    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def _load_calendar(user_id=None):
    """Load calendar events from file"""
    path = _get_calendar_file(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {'events': []}
    return {'events': []}


def _save_calendar(data, user_id=None):
    """Save calendar events to file"""
    path = _get_calendar_file(user_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@calendar_api_bp.route('/events', methods=['GET'])
def get_events():
    """Get all calendar events for user

    Query params:
    - start_date: ISO format (YYYY-MM-DD)
    - end_date: ISO format (YYYY-MM-DD)
    - type: court, rent, appointment, reminder
    """
    # Check if user or admin
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    calendar_data = _load_calendar(user_id)
    events = calendar_data.get('events', [])

    # Filter by date range if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    event_type = request.args.get('type')

    filtered = events

    if start_date:
        filtered = [e for e in filtered if e.get('date', '') >= start_date]
    if end_date:
        filtered = [e for e in filtered if e.get('date', '') <= end_date]
    if event_type:
        filtered = [e for e in filtered if e.get('type') == event_type]

    return jsonify({'events': filtered, 'count': len(filtered)})


@calendar_api_bp.route('/events', methods=['POST'])
def create_event():
    """Create a new calendar event

    JSON body:
    {
        "title": "Court Hearing",
        "date": "2025-12-01",
        "time": "10:00",
        "type": "court",
        "description": "Eviction hearing - Courtroom 3B",
        "location": "Multnomah County Courthouse",
        "reminder_days": 7
    }
    """
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    # Validate required fields
    required = ['title', 'date', 'type']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Create event
    event = {
        'id': secrets.token_hex(8),
        'title': data['title'],
        'date': data['date'],
        'time': data.get('time', ''),
        'type': data['type'],  # court, rent, appointment, reminder
        'description': data.get('description', ''),
        'location': data.get('location', ''),
        'reminder_days': data.get('reminder_days', 3),
        'created_at': datetime.now().isoformat(),
        'user_id': user_id,
        'status': 'active'
    }

    calendar_data = _load_calendar(user_id)
    calendar_data['events'].append(event)
    _save_calendar(calendar_data, user_id)

    return jsonify({'event': event, 'message': 'Event created'}), 201


@calendar_api_bp.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get specific event by ID"""
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    calendar_data = _load_calendar(user_id)
    events = calendar_data.get('events', [])

    event = next((e for e in events if e.get('id') == event_id), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    return jsonify({'event': event})


@calendar_api_bp.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    calendar_data = _load_calendar(user_id)
    events = calendar_data.get('events', [])

    # Find and update event
    for i, event in enumerate(events):
        if event.get('id') == event_id:
            # Update fields
            event.update({
                'title': data.get('title', event.get('title')),
                'date': data.get('date', event.get('date')),
                'time': data.get('time', event.get('time')),
                'type': data.get('type', event.get('type')),
                'description': data.get('description', event.get('description')),
                'location': data.get('location', event.get('location')),
                'reminder_days': data.get('reminder_days', event.get('reminder_days')),
                'status': data.get('status', event.get('status')),
                'updated_at': datetime.now().isoformat()
            })
            events[i] = event
            calendar_data['events'] = events
            _save_calendar(calendar_data, user_id)
            return jsonify({'event': event, 'message': 'Event updated'})

    return jsonify({'error': 'Event not found'}), 404


@calendar_api_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    calendar_data = _load_calendar(user_id)
    events = calendar_data.get('events', [])

    # Remove event
    new_events = [e for e in events if e.get('id') != event_id]
    if len(new_events) == len(events):
        return jsonify({'error': 'Event not found'}), 404

    calendar_data['events'] = new_events
    _save_calendar(calendar_data, user_id)

    return jsonify({'message': 'Event deleted'}), 200


@calendar_api_bp.route('/upcoming', methods=['GET'])
def get_upcoming():
    """Get upcoming events in next N days

    Query params:
    - days: number of days ahead to look (default 30)
    """
    user_id = _require_user_or_401()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    days = int(request.args.get('days', 30))
    today = datetime.now().date()
    end_date = today + timedelta(days=days)

    calendar_data = _load_calendar(user_id)
    events = calendar_data.get('events', [])

    # Filter to upcoming events
    upcoming = []
    for event in events:
        try:
            event_date = datetime.fromisoformat(event.get('date', '')).date()
            if today <= event_date <= end_date and event.get('status') == 'active':
                # Calculate days until
                days_until = (event_date - today).days
                event['days_until'] = days_until
                upcoming.append(event)
        except ValueError:
            continue

    # Sort by date
    upcoming.sort(key=lambda x: x.get('date', ''))

    return jsonify({'events': upcoming, 'count': len(upcoming)})


@calendar_api_bp.route('/types', methods=['GET'])
def get_event_types():
    """Get available event types and their descriptions"""
    types = {
        'court': {
            'name': 'Court Date',
            'description': 'Court hearings, trials, mediations',
            'icon': '⚖️',
            'color': '#e53e3e'
        },
        'rent': {
            'name': 'Rent Due',
            'description': 'Monthly rent payment due dates',
            'icon': '💵',
            'color': '#38a169'
        },
        'appointment': {
            'name': 'Appointment',
            'description': 'Meetings with lawyers, inspectors, etc.',
            'icon': '📅',
            'color': '#3182ce'
        },
        'inspection': {
            'name': 'Inspection',
            'description': 'Property inspections, walkthroughs',
            'icon': '🔍',
            'color': '#805ad5'
        },
        'reminder': {
            'name': 'Reminder',
            'description': 'General reminders and tasks',
            'icon': '⏰',
            'color': '#d69e2e'
        }
    }
    return jsonify({'types': types})


@calendar_api_bp.route('/admin/all-events', methods=['GET'])
def admin_get_all_events():
    """Admin: Get events for all users"""
    if not _require_admin_or_401():
        return jsonify({'error': 'Admin access required'}), 401

    calendar_dir = os.path.join(current_app.root_path, 'uploads', 'calendars')
    all_events = []

    if os.path.exists(calendar_dir):
        for filename in os.listdir(calendar_dir):
            if filename.endswith('.json'):
                user_id = filename.replace('.json', '')
                try:
                    with open(os.path.join(calendar_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        events = data.get('events', [])
                        for event in events:
                            event['_user_id'] = user_id
                        all_events.extend(events)
                except Exception:
                    continue

    return jsonify({'events': all_events, 'count': len(all_events)})
