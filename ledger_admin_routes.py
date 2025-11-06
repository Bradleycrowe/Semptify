"""
Ledger Admin Control Panel Routes

Allows administrators to:
- View and update ledger configuration
- Adjust statute durations and time sensitivities
- Configure weather alert thresholds
- Manage ledger retention policies
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ledger_config import get_ledger_config
    from ledger_tracking import (
        get_statute_tracker,
        get_money_ledger,
        get_time_ledger,
        get_service_date_ledger,
    )
    from weather_and_time import (
        get_weather_manager,
        get_time_sensitivity_manager,
    )
except ImportError as e:
    # Fallback for different import paths
    from . import ledger_config, ledger_tracking, weather_and_time
    get_ledger_config = ledger_config.get_ledger_config
    get_statute_tracker = ledger_tracking.get_statute_tracker
    get_money_ledger = ledger_tracking.get_money_ledger
    get_time_ledger = ledger_tracking.get_time_ledger
    get_service_date_ledger = ledger_tracking.get_service_date_ledger
    get_weather_manager = weather_and_time.get_weather_manager
    get_time_sensitivity_manager = weather_and_time.get_time_sensitivity_manager

# This blueprint integrates with the main admin panel
ledger_admin_bp = Blueprint("ledger_admin", __name__, url_prefix="/admin/ledger")


# =====================
# CONFIG MANAGEMENT
# =====================


@ledger_admin_bp.route("/config", methods=["GET"])
def get_config():
    """Get current ledger configuration."""
    config = get_ledger_config()

    return jsonify(
        {
            "status": "ok",
            "config": config.to_dict(),
            "loaded_at": datetime.now().isoformat(),
        }
    )


@ledger_admin_bp.route("/config/section/<section>", methods=["GET"])
def get_config_section(section: str):
    """Get specific config section (statute_durations, weather_settings, etc.)."""
    config = get_ledger_config()
    section_data = config.get_section(section)

    if not section_data:
        return jsonify({"error": f"Section not found: {section}"}), 404

    return jsonify(
        {
            "section": section,
            "data": section_data,
        }
    )


@ledger_admin_bp.route("/config/update", methods=["POST"])
def update_config():
    """Update configuration values.

    JSON body:
    {
        "updates": {
            "statute_durations.eviction_notice": 30,
            "weather_settings.wind_alert_threshold_mph": 45,
            "notification_settings.alert_days_before_statute_expiry": 45
        },
        "reason": "Updated thresholds for winter season"
    }
    """
    data = request.get_json()
    if not data or "updates" not in data:
        return jsonify({"error": "Missing 'updates' in request"}), 400

    config = get_ledger_config()
    changes = {}

    try:
        # Apply each update
        for path, value in data["updates"].items():
            old_value = config.get(path)
            config.set(path, value)
            changes[path] = {"old": old_value, "new": value}

        # Save to disk
        config.save()

        return jsonify(
            {
                "status": "ok",
                "changes_applied": len(changes),
                "changes": changes,
                "reason": data.get("reason", "Admin update"),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ledger_admin_bp.route("/config/reset", methods=["POST"])
def reset_config():
    """Reset all configuration to defaults."""
    data = request.get_json() or {}

    if not data.get("confirm_reset"):
        return (
            jsonify({"error": "Must include 'confirm_reset': true to reset"}),
            400,
        )

    config = get_ledger_config()
    config.reset_to_defaults()

    return jsonify(
        {
            "status": "ok",
            "message": "Configuration reset to defaults",
            "timestamp": datetime.now().isoformat(),
        }
    )


# =====================
# STATUTE MANAGEMENT
# =====================


@ledger_admin_bp.route("/statutes/summary", methods=["GET"])
def statute_summary():
    """Get summary of all active statutes."""
    tracker = get_statute_tracker()

    active = tracker.get_active_statutes()
    expiring_soon = tracker.get_expiring_soon(days=30)

    return jsonify(
        {
            "total_statutes": len(tracker.statutes),
            "active_statutes": len(active),
            "expiring_in_30_days": len(expiring_soon),
            "active": [s.to_dict() for s in active],
            "expiring_soon": [s.to_dict() for s in expiring_soon],
        }
    )


@ledger_admin_bp.route("/durations", methods=["GET"])
def get_statute_durations():
    """Get all configured statute durations."""
    config = get_ledger_config()
    durations = config.get_section("statute_durations")

    return jsonify(
        {
            "statute_durations": durations,
        }
    )


@ledger_admin_bp.route("/durations/update", methods=["POST"])
def update_statute_durations():
    """Update statute durations.

    JSON body:
    {
        "durations": {
            "eviction_notice": 30,
            "cure_period": 5,
            "complaint": 365
        },
        "reason": "Updated per jurisdiction requirements"
    }
    """
    data = request.get_json()
    if not data or "durations" not in data:
        return jsonify({"error": "Missing 'durations' in request"}), 400

    config = get_ledger_config()
    changes = {}

    try:
        for action_type, duration_days in data["durations"].items():
            old = config.get(f"statute_durations.{action_type}")
            config.set(f"statute_durations.{action_type}", duration_days)
            changes[action_type] = {"old": old, "new": duration_days}

        config.save()

        return jsonify(
            {
                "status": "ok",
                "changes": changes,
                "reason": data.get("reason", "Admin update"),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =====================
# TIME SENSITIVITY MANAGEMENT
# =====================


@ledger_admin_bp.route("/sensitivities", methods=["GET"])
def get_sensitivities():
    """Get all time sensitivities."""
    sens_mgr = get_time_sensitivity_manager()
    config = get_ledger_config()

    return jsonify(
        {
            "configured": config.get_section("time_sensitivities"),
            "active": [s.to_dict() for s in sens_mgr.sensitivities.values()],
        }
    )


@ledger_admin_bp.route("/sensitivities/update", methods=["POST"])
def update_sensitivities():
    """Update time sensitivity settings.

    JSON body:
    {
        "updates": {
            "service_deadline.weather_dependent": true,
            "response_deadline.duration_days": 21
        }
    }
    """
    data = request.get_json()
    if not data or "updates" not in data:
        return jsonify({"error": "Missing 'updates'"}), 400

    config = get_ledger_config()
    changes = {}

    try:
        for path, value in data["updates"].items():
            full_path = f"time_sensitivities.{path}"
            old = config.get(full_path)
            config.set(full_path, value)
            changes[path] = {"old": old, "new": value}

        config.save()

        return jsonify(
            {
                "status": "ok",
                "changes": changes,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =====================
# WEATHER MANAGEMENT
# =====================


@ledger_admin_bp.route("/weather/settings", methods=["GET"])
def get_weather_settings():
    """Get weather alert configuration."""
    config = get_ledger_config()

    return jsonify(
        {
            "severe_conditions": config.get("weather_settings.severe_conditions", []),
            "visibility_threshold_miles": config.get(
                "weather_settings.visibility_threshold_miles", 0.5
            ),
            "wind_alert_threshold_mph": config.get(
                "weather_settings.wind_alert_threshold_mph", 40
            ),
            "alert_types": config.get("weather_settings.alert_types", []),
        }
    )


@ledger_admin_bp.route("/weather/settings/update", methods=["POST"])
def update_weather_settings():
    """Update weather alert thresholds.

    JSON body:
    {
        "wind_alert_threshold_mph": 50,
        "visibility_threshold_miles": 0.25
    }
    """
    data = request.get_json()
    config = get_ledger_config()
    changes = {}

    try:
        for key, value in data.items():
            path = f"weather_settings.{key}"
            old = config.get(path)
            config.set(path, value)
            changes[key] = {"old": old, "new": value}

        config.save()

        return jsonify(
            {
                "status": "ok",
                "changes": changes,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =====================
# NOTIFICATION SETTINGS
# =====================


@ledger_admin_bp.route("/alerts/thresholds", methods=["GET"])
def get_alert_thresholds():
    """Get notification alert thresholds."""
    config = get_ledger_config()

    return jsonify(config.get_section("notification_settings"))


@ledger_admin_bp.route("/alerts/thresholds/update", methods=["POST"])
def update_alert_thresholds():
    """Update alert thresholds.

    JSON body:
    {
        "alert_days_before_statute_expiry": 45,
        "alert_days_before_service_deadline": 10
    }
    """
    data = request.get_json()
    config = get_ledger_config()
    changes = {}

    try:
        for key, value in data.items():
            path = f"notification_settings.{key}"
            old = config.get(path)
            config.set(path, value)
            changes[key] = {"old": old, "new": value}

        config.save()

        return jsonify(
            {
                "status": "ok",
                "changes": changes,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =====================
# LEDGER STATISTICS
# =====================


@ledger_admin_bp.route("/stats", methods=["GET"])
def get_ledger_stats():
    """Get statistics on ledger usage."""
    money = get_money_ledger()
    time_ledger = get_time_ledger()
    service = get_service_date_ledger()

    return jsonify(
        {
            "money_ledger": {
                "transaction_count": len(money.transactions),
                "total_tracked": sum(t.amount for t in money.transactions),
                "currency": "USD",
            },
            "time_ledger": {
                "transaction_count": len(time_ledger.transactions),
                "total_tracked": sum(t.amount for t in time_ledger.transactions),
            },
            "service_ledger": {
                "transaction_count": len(service.transactions),
                "total_tracked": sum(t.amount for t in service.transactions),
            },
            "timestamp": datetime.now().isoformat(),
        }
    )


# =====================
# HEALTH CHECK
# =====================


@ledger_admin_bp.route("/health", methods=["GET"])
def ledger_health():
    """Check health of ledger system."""
    try:
        config = get_ledger_config()
        tracker = get_statute_tracker()
        weather = get_weather_manager()

        return jsonify(
            {
                "status": "healthy",
                "config_loaded": config.config is not None,
                "statute_tracker_active": len(tracker.statutes) >= 0,
                "weather_cache_size": len(weather.conditions),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "unhealthy",
                "error": str(e),
            }
        ), 500
