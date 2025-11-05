"""
Ledger Tracking and Weather/Sensitivity API Routes

Exposes:
- Money/Time/Service Date ledgers
- Statute of limitations tracking
- Weather conditions and caching
- Time-sensitive deadline calculations
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from typing import Optional

from ledger_tracking import (
    get_money_ledger,
    get_time_ledger,
    get_service_date_ledger,
    get_statute_tracker,
)
from weather_and_time import (
    get_weather_manager,
    get_time_sensitivity_manager,
)

ledger_tracking_bp = Blueprint("ledger_tracking", __name__, url_prefix="/api/ledger-tracking")


# =====================
# MONEY LEDGER ROUTES
# =====================


@ledger_tracking_bp.route("/money/balance/<actor_id>", methods=["GET"])
def get_money_balance(actor_id: str):
    """Get current money balance for an actor."""
    ledger = get_money_ledger()
    balance = ledger.get_balance(actor_id=actor_id)
    return jsonify(
        {
            "actor_id": actor_id,
            "balance_usd": balance,
            "currency": "USD",
        }
    )


@ledger_tracking_bp.route("/money/add", methods=["POST"])
def add_money_transaction():
    """Add a money transaction.

    JSON body:
    {
        "actor_id": "tenant-123",
        "description": "Rent payment",
        "amount": 1200.00,
        "doc_id": "doc-uuid-1",
        "context": {
            "rent_period": "2025-01",
            "property_id": "prop-456"
        }
    }
    """
    data = request.get_json()
    ledger = get_money_ledger()

    trans = ledger.add_transaction(
        actor_id=data["actor_id"],
        description=data["description"],
        amount=data["amount"],
        unit="USD",
        related_doc_id=data.get("doc_id"),
        context=data.get("context", {}),
    )

    return jsonify(trans.to_dict()), 201


@ledger_tracking_bp.route("/money/transactions/<actor_id>", methods=["GET"])
def get_money_transactions(actor_id: str):
    """Get transactions for an actor."""
    days = request.args.get("days", 90, type=int)
    cutoff = datetime.now() - timedelta(days=days)

    ledger = get_money_ledger()
    transactions = ledger.get_transactions(actor_id=actor_id, start_date=cutoff)

    return jsonify(
        {
            "actor_id": actor_id,
            "period_days": days,
            "transaction_count": len(transactions),
            "total": sum(t.amount for t in transactions),
            "transactions": [t.to_dict() for t in transactions],
        }
    )


@ledger_tracking_bp.route("/money/summary/<actor_id>", methods=["GET"])
def get_money_summary(actor_id: str):
    """Get money ledger summary."""
    days = request.args.get("days", 90, type=int)
    ledger = get_money_ledger()
    return jsonify(ledger.get_summary(actor_id=actor_id, days=days))


# =====================
# TIME LEDGER ROUTES
# =====================


@ledger_tracking_bp.route("/time/add", methods=["POST"])
def add_time_transaction():
    """Add a time transaction (days, hours worked, etc).

    JSON body:
    {
        "actor_id": "tenant-123",
        "description": "Service attempts",
        "amount": 3,
        "unit": "attempts",
        "doc_id": "doc-uuid-1"
    }
    """
    data = request.get_json()
    ledger = get_time_ledger()

    trans = ledger.add_transaction(
        actor_id=data["actor_id"],
        description=data["description"],
        amount=data["amount"],
        unit=data.get("unit", "days"),
        related_doc_id=data.get("doc_id"),
        context=data.get("context", {}),
    )

    return jsonify(trans.to_dict()), 201


@ledger_tracking_bp.route("/time/summary/<actor_id>", methods=["GET"])
def get_time_summary(actor_id: str):
    """Get time ledger summary."""
    days = request.args.get("days", 90, type=int)
    ledger = get_time_ledger()
    return jsonify(ledger.get_summary(actor_id=actor_id, days=days))


# =====================
# SERVICE DATE LEDGER
# =====================


@ledger_tracking_bp.route("/service-date/add", methods=["POST"])
def add_service_date():
    """Record a service attempt or successful service.

    JSON body:
    {
        "actor_id": "process-server-789",
        "description": "Defendant successfully served",
        "amount": 1,
        "context": {
            "method": "personal_delivery",
            "address": "123 Main St",
            "date_served": "2025-01-15"
        }
    }
    """
    data = request.get_json()
    ledger = get_service_date_ledger()

    trans = ledger.add_transaction(
        actor_id=data["actor_id"],
        description=data["description"],
        amount=data["amount"],
        unit=data.get("unit", "count"),
        related_doc_id=data.get("doc_id"),
        context=data.get("context", {}),
    )

    return jsonify(trans.to_dict()), 201


# =====================
# STATUTE OF LIMITATIONS
# =====================


@ledger_tracking_bp.route("/statute/create", methods=["POST"])
def create_statute():
    """Create a statute of limitations tracker.

    JSON body:
    {
        "action_type": "eviction_notice",
        "start_date": "2025-01-15",
        "jurisdiction": "CA",
        "doc_id": "doc-uuid-1"
    }
    """
    data = request.get_json()
    tracker = get_statute_tracker()

    statute = tracker.create_statute(
        action_type=data["action_type"],
        start_date=datetime.fromisoformat(data["start_date"]),
        jurisdiction=data.get("jurisdiction", "US"),
        doc_id=data.get("doc_id"),
    )

    return jsonify(statute.to_dict()), 201


@ledger_tracking_bp.route("/statute/active", methods=["GET"])
def get_active_statutes():
    """Get all non-expired statutes."""
    tracker = get_statute_tracker()
    statutes = tracker.get_active_statutes()

    return jsonify(
        {
            "count": len(statutes),
            "statutes": [s.to_dict() for s in statutes],
        }
    )


@ledger_tracking_bp.route("/statute/expiring-soon", methods=["GET"])
def get_expiring_statutes():
    """Get statutes expiring within N days."""
    days = request.args.get("days", 30, type=int)
    tracker = get_statute_tracker()
    statutes = tracker.get_expiring_soon(days=days)

    return jsonify(
        {
            "window_days": days,
            "count": len(statutes),
            "statutes": [s.to_dict() for s in statutes],
        }
    )


@ledger_tracking_bp.route("/statute/<statute_id>/toll", methods=["POST"])
def toll_statute(statute_id: str):
    """Pause the clock on a statute (tolling).

    JSON body:
    {
        "reason": "Appeal filed - clock paused"
    }
    """
    data = request.get_json()
    tracker = get_statute_tracker()
    tracker.toll_statute(statute_id, reason=data.get("reason", ""))

    statute = tracker.statutes.get(statute_id)
    if statute:
        return jsonify(statute.to_dict())
    else:
        return jsonify({"error": "Statute not found"}), 404


# =====================
# WEATHER ROUTES
# =====================


@ledger_tracking_bp.route("/weather/add", methods=["POST"])
def add_weather():
    """Add or update weather for a date/location.

    JSON body:
    {
        "date": "2025-01-15",
        "location": "123 Main St, San Francisco, CA",
        "temperature_f": 65,
        "condition": "rain",
        "humidity_percent": 75,
        "wind_speed_mph": 12,
        "precipitation_inches": 0.5,
        "visibility_miles": 5,
        "alerts": ["flood_watch"]
    }
    """
    data = request.get_json()
    weather_mgr = get_weather_manager()

    weather = weather_mgr.add_weather_condition(
        date=datetime.fromisoformat(data["date"]),
        location=data["location"],
        temperature_f=data["temperature_f"],
        condition=data["condition"],
        humidity_percent=data.get("humidity_percent", 50),
        wind_speed_mph=data.get("wind_speed_mph", 0),
        precipitation_inches=data.get("precipitation_inches", 0),
        visibility_miles=data.get("visibility_miles", 10),
        alerts=data.get("alerts", []),
        source=data.get("source", "api"),
    )

    return jsonify(weather.to_dict()), 201


@ledger_tracking_bp.route("/weather/<date>/<location>", methods=["GET"])
def get_weather(date: str, location: str):
    """Get weather for specific date and location."""
    weather_mgr = get_weather_manager()
    weather = weather_mgr.get_weather(datetime.fromisoformat(date), location)

    if weather:
        return jsonify(weather.to_dict())
    else:
        return jsonify({"error": "Weather data not found"}), 404


@ledger_tracking_bp.route("/weather/period", methods=["GET"])
def get_weather_period():
    """Get weather for date range.

    Query params:
    - start_date: ISO date
    - end_date: ISO date
    - location: Address or coordinate
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    location = request.args.get("location")

    if not all([start_date, end_date, location]):
        return (
            jsonify(
                {"error": "Missing required params: start_date, end_date, location"}
            ),
            400,
        )

    weather_mgr = get_weather_manager()
    conditions = weather_mgr.get_weather_for_period(
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date),
        location,
    )

    has_severe = weather_mgr.has_severe_weather(
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date),
        location,
    )

    return jsonify(
        {
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "condition_count": len(conditions),
            "has_severe_weather": has_severe,
            "conditions": [c.to_dict() for c in conditions],
        }
    )


# =====================
# TIME SENSITIVITY & DEADLINES
# =====================


@ledger_tracking_bp.route("/sensitivity/list", methods=["GET"])
def list_sensitivities():
    """List all time sensitivities."""
    sens_mgr = get_time_sensitivity_manager()

    return jsonify(
        {
            "count": len(sens_mgr.sensitivities),
            "sensitivities": [s.to_dict() for s in sens_mgr.sensitivities.values()],
        }
    )


@ledger_tracking_bp.route("/sensitivity/deadline", methods=["GET"])
def calculate_deadline():
    """Calculate deadline with weather/sensitivity adjustments.

    Query params:
    - sensitivity: Name of sensitivity (e.g., "service_deadline")
    - start_date: ISO date
    - location: Address (for weather lookup)
    """
    sensitivity = request.args.get("sensitivity")
    start_date = request.args.get("start_date")
    location = request.args.get("location")

    if not all([sensitivity, start_date]):
        return (
            jsonify({"error": "Missing required params: sensitivity, start_date"}),
            400,
        )

    sens_mgr = get_time_sensitivity_manager()
    weather_mgr = get_weather_manager() if location else None

    result = sens_mgr.calculate_deadline(
        sensitivity_name=sensitivity,
        start_date=datetime.fromisoformat(start_date),
        location=location,
        weather_manager=weather_mgr,
    )

    return jsonify(result)


# =====================
# COURT PACKET DATA
# =====================


@ledger_tracking_bp.route("/court-packet/<doc_id>", methods=["GET"])
def get_court_packet_data(doc_id: str):
    """Get all ledger and weather data for a court packet.

    Returns relevant financial, timing, and environmental context.
    """
    money_ledger = get_money_ledger()
    time_ledger = get_time_ledger()
    service_ledger = get_service_date_ledger()
    statute_tracker = get_statute_tracker()

    # Get all related entries for this document
    money_trans = [
        t
        for t in money_ledger.transactions
        if t.related_doc_id == doc_id
    ]
    time_trans = [
        t for t in time_ledger.transactions if t.related_doc_id == doc_id
    ]
    service_trans = [
        t
        for t in service_ledger.transactions
        if t.related_doc_id == doc_id
    ]

    return jsonify(
        {
            "doc_id": doc_id,
            "money_transactions": {
                "count": len(money_trans),
                "total": sum(t.amount for t in money_trans),
                "items": [t.to_dict() for t in money_trans],
            },
            "time_transactions": {
                "count": len(time_trans),
                "total": sum(t.amount for t in time_trans),
                "items": [t.to_dict() for t in time_trans],
            },
            "service_transactions": {
                "count": len(service_trans),
                "total": sum(t.amount for t in service_trans),
                "items": [t.to_dict() for t in service_trans],
            },
            "relevant_statutes": [
                s.to_dict()
                for s in statute_tracker.statutes.values()
            ],
        }
    )
