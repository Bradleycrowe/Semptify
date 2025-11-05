"""
Audio/Visual Capture and Mobile Import Routes

Endpoints for:
- Video/audio/photo uploads from mobile devices
- Voicemail imports
- SMS/text message imports
- Email imports
- Chat message imports
- Evidence retrieval and linking to calendar
"""

from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from typing import Optional, Dict, Any
import os

from av_capture import (
    get_av_manager,
    LocationData,
)

av_routes_bp = Blueprint("av_capture", __name__, url_prefix="/api/evidence")


# =====================
# MOBILE DEVICE CAPTURE
# =====================


@av_routes_bp.route("/capture/video", methods=["POST"])
def upload_video():
    """Upload video from mobile device.

    Multipart form:
    - file: Video file
    - actor_id: Who captured (optional)
    - device_name: Device identifier
    - app_version: App version
    - description: What was captured
    - location_lat: Latitude (optional)
    - location_lon: Longitude (optional)
    - location_accuracy: GPS accuracy in meters
    - location_altitude: Altitude in meters (optional)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    # Parse location if provided
    location = None
    if request.form.get("location_lat"):
        try:
            location = LocationData(
                latitude=float(request.form["location_lat"]),
                longitude=float(request.form["location_lon"]),
                accuracy_meters=float(request.form.get("location_accuracy", 0)),
                altitude_meters=float(request.form.get("location_altitude"))
                if request.form.get("location_altitude")
                else None,
            )
        except (ValueError, TypeError):
            pass

    # Save file
    os.makedirs("uploads/evidence", exist_ok=True)
    file_path = f"uploads/evidence/{file.filename}"
    file.save(file_path)

    # Register capture
    manager = get_av_manager()
    capture = manager.register_capture(
        capture_type="video",
        source_type=request.form.get("source_type", "mobile"),
        file_path=file_path,
        actor_id=request.form.get("actor_id"),
        location=location,
        device_name=request.form.get("device_name"),
        description=request.form.get("description", ""),
        metadata_extra={
            "app_version": request.form.get("app_version"),
        },
        original_filename=file.filename,
    )

    return jsonify(capture.to_dict()), 201


@av_routes_bp.route("/capture/audio", methods=["POST"])
def upload_audio():
    """Upload audio from mobile device.

    Multipart form:
    - file: Audio file
    - duration_seconds: Duration of recording
    - actor_id: Who captured (optional)
    - device_name: Device identifier
    - description: What was captured
    - location_lat/lon/accuracy (optional)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Parse location if provided
    location = None
    if request.form.get("location_lat"):
        try:
            location = LocationData(
                latitude=float(request.form["location_lat"]),
                longitude=float(request.form["location_lon"]),
                accuracy_meters=float(request.form.get("location_accuracy", 0)),
            )
        except (ValueError, TypeError):
            pass

    # Save file
    os.makedirs("uploads/evidence", exist_ok=True)
    file_path = f"uploads/evidence/{file.filename}"
    file.save(file_path)

    # Register capture
    manager = get_av_manager()
    capture = manager.register_capture(
        capture_type="audio",
        source_type=request.form.get("source_type", "mobile"),
        file_path=file_path,
        actor_id=request.form.get("actor_id"),
        location=location,
        device_name=request.form.get("device_name"),
        description=request.form.get("description", ""),
        duration_seconds=float(request.form.get("duration_seconds", 0))
        or None,
        original_filename=file.filename,
    )

    return jsonify(capture.to_dict()), 201


@av_routes_bp.route("/capture/photo", methods=["POST"])
def upload_photo():
    """Upload photo from mobile device with EXIF metadata."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Parse location if provided
    location = None
    if request.form.get("location_lat"):
        try:
            location = LocationData(
                latitude=float(request.form["location_lat"]),
                longitude=float(request.form["location_lon"]),
                accuracy_meters=float(request.form.get("location_accuracy", 0)),
            )
        except (ValueError, TypeError):
            pass

    # Save file
    os.makedirs("uploads/evidence", exist_ok=True)
    file_path = f"uploads/evidence/{file.filename}"
    file.save(file_path)

    # Register capture
    manager = get_av_manager()
    capture = manager.register_capture(
        capture_type="photo",
        source_type=request.form.get("source_type", "mobile"),
        file_path=file_path,
        actor_id=request.form.get("actor_id"),
        location=location,
        device_name=request.form.get("device_name"),
        description=request.form.get("description", ""),
        original_filename=file.filename,
    )

    return jsonify(capture.to_dict()), 201


# =====================
# VOICEMAIL IMPORT
# =====================


@av_routes_bp.route("/import/voicemail", methods=["POST"])
def import_voicemail():
    """Import voicemail message.

    JSON body:
    {
        "from_phone": "+1234567890",
        "to_phone": "+1234567891",
        "duration_seconds": 45.5,
        "timestamp": "2025-01-15T10:30:00Z",
        "transcription": "Optional AI transcription",
        "audio_file_id": "optional-file-upload-id",
        "source_system": "phone"
    }
    """
    data = request.get_json()

    required = ["from_phone", "to_phone", "duration_seconds", "timestamp"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    manager = get_av_manager()
    voicemail = manager.import_voicemail(
        from_phone=data["from_phone"],
        to_phone=data["to_phone"],
        duration_seconds=data["duration_seconds"],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        transcription=data.get("transcription"),
        audio_file_path=data.get("audio_file_path"),
        source_system=data.get("source_system", "phone"),
        raw_metadata=data.get("raw_metadata", {}),
    )

    return jsonify(voicemail.to_dict()), 201


# =====================
# SMS/TEXT MESSAGE IMPORT
# =====================


@av_routes_bp.route("/import/text-message", methods=["POST"])
def import_text_message():
    """Import SMS/text message.

    JSON body:
    {
        "from_phone": "+1234567890",
        "to_phone": "+1234567891",
        "message_text": "Hello landlord...",
        "timestamp": "2025-01-15T10:30:00Z",
        "is_outbound": false,
        "source_system": "sms"
    }
    """
    data = request.get_json()

    required = ["from_phone", "to_phone", "message_text", "timestamp", "is_outbound"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    manager = get_av_manager()
    message = manager.import_text_message(
        from_phone=data["from_phone"],
        to_phone=data["to_phone"],
        message_text=data["message_text"],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        is_outbound=data["is_outbound"],
        source_system=data.get("source_system", "sms"),
        raw_metadata=data.get("raw_metadata", {}),
    )

    return jsonify(message.to_dict()), 201


# =====================
# EMAIL IMPORT
# =====================


@av_routes_bp.route("/import/email", methods=["POST"])
def import_email():
    """Import email message.

    JSON body:
    {
        "from_email": "sender@example.com",
        "to_email": ["recipient@example.com"],
        "cc_email": ["cc@example.com"],
        "subject": "Lease Notice",
        "body_text": "Full email body...",
        "timestamp": "2025-01-15T10:30:00Z",
        "attachments": [
            {"filename": "doc.pdf", "hash": "abc123", "size": 1024}
        ],
        "raw_headers": {}
    }
    """
    data = request.get_json()

    required = ["from_email", "to_email", "subject", "body_text", "timestamp"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    manager = get_av_manager()
    email = manager.import_email(
        from_email=data["from_email"],
        to_email=data["to_email"],
        subject=data["subject"],
        body_text=data["body_text"],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        cc_email=data.get("cc_email", []),
        attachments=data.get("attachments", []),
        raw_headers=data.get("raw_headers", {}),
        source_system=data.get("source_system", "email"),
    )

    return jsonify(email.to_dict()), 201


# =====================
# CHAT MESSAGE IMPORT
# =====================


@av_routes_bp.route("/import/chat", methods=["POST"])
def import_chat():
    """Import chat message.

    JSON body:
    {
        "from_user": "tenant123",
        "platform": "slack|teams|signal|whatsapp|telegram",
        "channel_or_thread": "#legal-issues or thread-id",
        "message_text": "Message content...",
        "timestamp": "2025-01-15T10:30:00Z",
        "attachments": [
            {"filename": "doc.pdf", "hash": "abc123", "url": "slack-url"}
        ]
    }
    """
    data = request.get_json()

    required = [
        "from_user",
        "platform",
        "channel_or_thread",
        "message_text",
        "timestamp",
    ]
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    manager = get_av_manager()
    chat = manager.import_chat_message(
        from_user=data["from_user"],
        platform=data["platform"],
        channel_or_thread=data["channel_or_thread"],
        message_text=data["message_text"],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        attachments=data.get("attachments", []),
        raw_metadata=data.get("raw_metadata", {}),
    )

    return jsonify(chat.to_dict()), 201


# =====================
# EVIDENCE RETRIEVAL
# =====================


@av_routes_bp.route("/captures/<capture_id>", methods=["GET"])
def get_capture(capture_id: str):
    """Get capture metadata by ID."""
    manager = get_av_manager()
    capture = manager.get_capture(capture_id)

    if not capture:
        return jsonify({"error": "Capture not found"}), 404

    return jsonify(capture.to_dict())


@av_routes_bp.route("/captures/type/<capture_type>", methods=["GET"])
def get_captures_by_type(capture_type: str):
    """Get all captures of specific type (video, audio, photo)."""
    manager = get_av_manager()
    captures = manager.get_captures_by_type(capture_type)

    return jsonify(
        {
            "capture_type": capture_type,
            "count": len(captures),
            "captures": [c.to_dict() for c in captures],
        }
    )


@av_routes_bp.route("/captures/actor/<actor_id>", methods=["GET"])
def get_captures_by_actor(actor_id: str):
    """Get all captures by a specific actor."""
    manager = get_av_manager()
    captures = manager.get_captures_by_actor(actor_id)

    return jsonify(
        {
            "actor_id": actor_id,
            "count": len(captures),
            "captures": [c.to_dict() for c in captures],
        }
    )


@av_routes_bp.route("/communications/phone/<phone_number>", methods=["GET"])
def get_phone_communications(phone_number: str):
    """Get all communications (voicemail, SMS) for a phone number."""
    manager = get_av_manager()
    comms = manager.get_communications_for_number(phone_number)

    return jsonify(comms)


@av_routes_bp.route("/communications/email/<email_address>", methods=["GET"])
def get_email_communications(email_address: str):
    """Get all email communications for an email address."""
    manager = get_av_manager()
    comms = manager.get_communications_for_email(email_address)

    return jsonify(comms)


@av_routes_bp.route("/evidence/summary", methods=["GET"])
def get_evidence_summary():
    """Get summary of all evidence captured."""
    days = request.args.get("days", 90, type=int)

    manager = get_av_manager()
    evidence = manager.get_all_evidence_by_date(days=days)

    return jsonify(evidence)


@av_routes_bp.route("/evidence/by-date", methods=["GET"])
def get_evidence_by_date():
    """Get evidence for specific date range.

    Query params:
    - days: Number of days to look back (default 90)
    - capture_types: Comma-separated types (video,audio,photo)
    """
    days = request.args.get("days", 90, type=int)
    capture_types = request.args.get("capture_types", "").split(",")

    manager = get_av_manager()
    evidence = manager.get_all_evidence_by_date(days=days)

    return jsonify(evidence)


# =====================
# HEALTH CHECK
# =====================


@av_routes_bp.route("/health", methods=["GET"])
def av_health():
    """Check health of AV capture system."""
    try:
        manager = get_av_manager()

        return jsonify(
            {
                "status": "healthy",
                "captures_count": len(manager.captures),
                "voicemails_count": len(manager.voicemails),
                "text_messages_count": len(manager.text_messages),
                "emails_count": len(manager.emails),
                "chat_messages_count": len(manager.chat_messages),
                "total_items": (
                    len(manager.captures)
                    + len(manager.voicemails)
                    + len(manager.text_messages)
                    + len(manager.emails)
                    + len(manager.chat_messages)
                ),
            }
        )

    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
