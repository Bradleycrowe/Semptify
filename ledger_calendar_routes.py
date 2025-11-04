"""
Flask Blueprint: Ledger & Calendar API endpoints

Provides REST API for:
- Viewing ledger entries
- Querying calendar events
- Adding new events
- Exporting for legal review
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from ledger_calendar import (
    get_ledger,
    get_calendar,
    log_action,
    schedule_event,
    LedgerEntry,
    CalendarEvent,
)

ledger_calendar_bp = Blueprint("ledger_calendar", __name__, url_prefix="/api/ledger-calendar")


@ledger_calendar_bp.route("/ledger", methods=["GET"])
def get_ledger_entries():
    """Get ledger entries with optional filters.

    Query params:
    - type: entry type filter (document, payment, complaint, evidence, notice, action)
    - actor: actor filter (user_id)
    - start_time: start timestamp
    - end_time: end timestamp
    - limit: max results
    """
    entry_type = request.args.get("type")
    actor = request.args.get("actor")
    start_time = request.args.get("start_time", type=float)
    end_time = request.args.get("end_time", type=float)
    limit = request.args.get("limit", 100, type=int)

    ledger = get_ledger()
    entries = ledger.get_entries(
        entry_type=entry_type,
        actor=actor,
        start_time=start_time,
        end_time=end_time,
    )

    # Return only last N entries
    entries = entries[-limit:]

    return jsonify(
        {
            "total": len(entries),
            "entries": [e.to_dict() for e in entries],
        }
    )


@ledger_calendar_bp.route("/ledger/<entry_id>", methods=["GET"])
def get_ledger_entry(entry_id):
    """Get a specific ledger entry by ID."""
    ledger = get_ledger()
    for entry in ledger.get_entries():
        if entry.id == entry_id:
            return jsonify(entry.to_dict())

    return jsonify({"error": "Entry not found"}), 404


@ledger_calendar_bp.route("/ledger/export", methods=["POST"])
def export_ledger():
    """Export ledger entries for legal review (court-admissible format).

    Body (optional):
    {
        "entry_ids": ["id1", "id2"]  # specific entries to export
    }
    """
    data = request.get_json() or {}
    entry_ids = data.get("entry_ids")

    ledger = get_ledger()
    export = ledger.export_for_court(entry_ids)

    return jsonify(export)


@ledger_calendar_bp.route("/calendar", methods=["GET"])
def get_calendar_events():
    """Get calendar events with optional filters.

    Query params:
    - start_date: ISO datetime string
    - end_date: ISO datetime string
    - type: event type (deadline, reminder, action_needed, completed)
    - priority: 0 (low), 1 (medium), 2 (high)
    - completed: true/false
    - upcoming_days: get events in next N days
    """
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    event_type = request.args.get("type")
    priority = request.args.get("priority", type=int)
    completed = request.args.get("completed", type=lambda x: x.lower() == "true")
    upcoming_days = request.args.get("upcoming_days", type=int)

    start_date = None
    end_date = None

    if start_date_str:
        start_date = datetime.fromisoformat(start_date_str)
    if end_date_str:
        end_date = datetime.fromisoformat(end_date_str)

    calendar = get_calendar()

    if upcoming_days:
        events = calendar.get_upcoming_events(days=upcoming_days)
    else:
        events = calendar.get_events(
            start_date=start_date,
            end_date=end_date,
            event_type=event_type,
            priority=priority,
            completed=completed,
        )

    return jsonify(
        {
            "total": len(events),
            "events": [e.to_dict() for e in events],
        }
    )


@ledger_calendar_bp.route("/calendar/upcoming", methods=["GET"])
def get_upcoming_events():
    """Get upcoming high-priority events due in next 3 days."""
    calendar = get_calendar()
    events = calendar.get_upcoming_high_priority()

    return jsonify(
        {
            "total": len(events),
            "events": [e.to_dict() for e in events],
        }
    )


@ledger_calendar_bp.route("/calendar/event", methods=["POST"])
def create_calendar_event():
    """Create a new calendar event.

    Body:
    {
        "title": "Send Notice to Landlord",
        "event_date": "2025-11-15T10:00:00",
        "type": "action_needed",  # deadline, reminder, action_needed, completed
        "description": "Follow up on maintenance request",
        "priority": 2,  # 0=low, 1=medium, 2=high
        "related_entry_id": "ledger-entry-uuid"  # optional
    }
    """
    data = request.get_json() or {}

    title = data.get("title")
    event_date_str = data.get("event_date")
    event_type = data.get("type", "action_needed")
    description = data.get("description", "")
    priority = data.get("priority", 0)
    related_entry_id = data.get("related_entry_id")

    if not title or not event_date_str:
        return jsonify({"error": "title and event_date required"}), 400

    try:
        event_date = datetime.fromisoformat(event_date_str)
    except ValueError:
        return jsonify({"error": "Invalid event_date format (use ISO datetime)"}), 400

    calendar = get_calendar()
    event = schedule_event(
        title=title,
        event_date=event_date,
        event_type=event_type,
        description=description,
        related_entry_id=related_entry_id,
        priority=priority,
    )

    return jsonify(event.to_dict()), 201


@ledger_calendar_bp.route("/calendar/event/<event_id>/complete", methods=["POST"])
def mark_event_completed(event_id):
    """Mark a calendar event as completed."""
    calendar = get_calendar()
    calendar.mark_completed(event_id)

    return jsonify({"status": "completed"})


@ledger_calendar_bp.route("/action/log", methods=["POST"])
def log_action_endpoint():
    """Log an action to the ledger.

    Body:
    {
        "action_type": "document",  # document, payment, complaint, evidence, notice, action
        "actor": "user-123",
        "description": "Uploaded lease agreement",
        "data": {
            "document_name": "lease.pdf",
            "file_path": "/path/to/file",
            "size_bytes": 125000
        },
        "files": ["/path/to/file"]  # optional
    }
    """
    data = request.get_json() or {}

    action_type = data.get("action_type")
    actor = data.get("actor")
    description = data.get("description")
    action_data = data.get("data", {})
    files = data.get("files", [])

    if not action_type or not actor:
        return jsonify({"error": "action_type and actor required"}), 400

    entry = log_action(
        action_type=action_type,
        actor=actor,
        description=description,
        data=action_data,
        files=files,
    )

    return jsonify(entry.to_dict()), 201


@ledger_calendar_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """Get dashboard summary: recent ledger entries and upcoming calendar events."""
    ledger = get_ledger()
    calendar = get_calendar()

    # Get recent entries
    recent_entries = ledger.get_entries()[-10:]

    # Get upcoming events
    upcoming_events = calendar.get_upcoming_events(days=7)
    high_priority = calendar.get_upcoming_high_priority()

    return jsonify(
        {
            "ledger": {
                "total_entries": len(ledger.get_entries()),
                "recent_entries": [e.to_dict() for e in recent_entries],
            },
            "calendar": {
                "total_events": len(calendar.get_events()),
                "upcoming_events": [e.to_dict() for e in upcoming_events],
                "high_priority_events": [e.to_dict() for e in high_priority],
            },
        }
    )
