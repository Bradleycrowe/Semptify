"""
Audio/Visual Capture and Communication Import Module

Provides evidence capture and import capabilities for:
- Video, audio, and photo captures from mobile devices
- Voicemail imports
- SMS/text message imports
- Email imports
- Chat message imports

All imports are linked to calendar events for timeline tracking.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


# =====================
# DATA CLASSES
# =====================


@dataclass
class LocationData:
    """GPS location data from mobile device."""

    latitude: float = 0.0
    longitude: float = 0.0
    accuracy_meters: float = 0.0
    altitude_meters: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)


@dataclass
class AVCapture:
    """Represents a video/audio/photo capture."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capture_type: str = "video"  # video, audio, photo
    source_type: str = "mobile"  # mobile, webcam, phone_call, etc.
    file_path: str = ""
    original_filename: str = ""
    actor_id: Optional[str] = None
    location: Optional[LocationData] = None
    device_name: Optional[str] = None
    description: str = ""
    duration_seconds: Optional[float] = None
    file_size_bytes: int = 0
    mime_type: str = ""
    metadata_extra: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        if self.location:
            data["location"] = self.location.to_dict()
        return data


@dataclass
class VoicemailCapture:
    """Represents a voicemail message."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_phone: str = ""
    to_phone: str = ""
    duration_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    transcription: Optional[str] = None
    audio_file_path: Optional[str] = None
    source_system: str = "phone"  # phone, google_voice, etc.
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class TextMessage:
    """Represents an SMS/text message."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_phone: str = ""
    to_phone: str = ""
    message_text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    is_outbound: bool = False
    source_system: str = "sms"  # sms, imessage, whatsapp, etc.
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class EmailMessage:
    """Represents an email message."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_email: str = ""
    to_email: List[str] = field(default_factory=list)
    cc_email: List[str] = field(default_factory=list)
    subject: str = ""
    body_text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    raw_headers: Dict[str, Any] = field(default_factory=dict)
    source_system: str = "email"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class ChatMessage:
    """Represents a chat platform message."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_user: str = ""
    platform: str = ""  # slack, teams, signal, whatsapp, telegram
    channel_or_thread: str = ""
    message_text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


# =====================
# MANAGER CLASS
# =====================


class AVManager:
    """Manages all audio/visual captures and communication imports."""

    def __init__(self):
        self.captures: Dict[str, AVCapture] = {}
        self.voicemails: Dict[str, VoicemailCapture] = {}
        self.text_messages: Dict[str, TextMessage] = {}
        self.emails: Dict[str, EmailMessage] = {}
        self.chat_messages: Dict[str, ChatMessage] = {}

    # =====================
    # CAPTURE REGISTRATION
    # =====================

    def register_capture(
        self,
        capture_type: str,
        source_type: str,
        file_path: str,
        original_filename: str = "",
        actor_id: Optional[str] = None,
        location: Optional[LocationData] = None,
        device_name: Optional[str] = None,
        description: str = "",
        duration_seconds: Optional[float] = None,
        file_size_bytes: int = 0,
        mime_type: str = "",
        metadata_extra: Optional[Dict[str, Any]] = None,
    ) -> AVCapture:
        """Register a new A/V capture."""
        capture = AVCapture(
            capture_type=capture_type,
            source_type=source_type,
            file_path=file_path,
            original_filename=original_filename or file_path.split("/")[-1],
            actor_id=actor_id,
            location=location,
            device_name=device_name,
            description=description,
            duration_seconds=duration_seconds,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            metadata_extra=metadata_extra or {},
        )

        self.captures[capture.id] = capture
        return capture

    # =====================
    # COMMUNICATION IMPORTS
    # =====================

    def import_voicemail(
        self,
        from_phone: str,
        to_phone: str,
        duration_seconds: float,
        timestamp: datetime,
        transcription: Optional[str] = None,
        audio_file_path: Optional[str] = None,
        source_system: str = "phone",
        raw_metadata: Optional[Dict[str, Any]] = None,
    ) -> VoicemailCapture:
        """Import a voicemail message."""
        voicemail = VoicemailCapture(
            from_phone=from_phone,
            to_phone=to_phone,
            duration_seconds=duration_seconds,
            timestamp=timestamp,
            transcription=transcription,
            audio_file_path=audio_file_path,
            source_system=source_system,
            raw_metadata=raw_metadata or {},
        )

        self.voicemails[voicemail.id] = voicemail
        return voicemail

    def import_text_message(
        self,
        from_phone: str,
        to_phone: str,
        message_text: str,
        timestamp: datetime,
        is_outbound: bool = False,
        source_system: str = "sms",
        raw_metadata: Optional[Dict[str, Any]] = None,
    ) -> TextMessage:
        """Import an SMS/text message."""
        message = TextMessage(
            from_phone=from_phone,
            to_phone=to_phone,
            message_text=message_text,
            timestamp=timestamp,
            is_outbound=is_outbound,
            source_system=source_system,
            raw_metadata=raw_metadata or {},
        )

        self.text_messages[message.id] = message
        return message

    def import_email(
        self,
        from_email: str,
        to_email: List[str],
        subject: str,
        body_text: str,
        timestamp: datetime,
        cc_email: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        raw_headers: Optional[Dict[str, Any]] = None,
        source_system: str = "email",
    ) -> EmailMessage:
        """Import an email message."""
        email = EmailMessage(
            from_email=from_email,
            to_email=to_email,
            cc_email=cc_email or [],
            subject=subject,
            body_text=body_text,
            timestamp=timestamp,
            attachments=attachments or [],
            raw_headers=raw_headers or {},
            source_system=source_system,
        )

        self.emails[email.id] = email
        return email

    def import_chat_message(
        self,
        from_user: str,
        platform: str,
        channel_or_thread: str,
        message_text: str,
        timestamp: datetime,
        attachments: Optional[List[Dict[str, Any]]] = None,
        raw_metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatMessage:
        """Import a chat platform message."""
        chat = ChatMessage(
            from_user=from_user,
            platform=platform,
            channel_or_thread=channel_or_thread,
            message_text=message_text,
            timestamp=timestamp,
            attachments=attachments or [],
            raw_metadata=raw_metadata or {},
        )

        self.chat_messages[chat.id] = chat
        return chat

    # =====================
    # RETRIEVAL METHODS
    # =====================

    def get_capture(self, capture_id: str) -> Optional[AVCapture]:
        """Get capture by ID."""
        return self.captures.get(capture_id)

    def get_captures_by_type(self, capture_type: str) -> List[AVCapture]:
        """Get all captures of a specific type."""
        return [c for c in self.captures.values() if c.capture_type == capture_type]

    def get_captures_by_actor(self, actor_id: str) -> List[AVCapture]:
        """Get all captures by a specific actor."""
        return [c for c in self.captures.values() if c.actor_id == actor_id]

    def get_communications_for_number(self, phone_number: str) -> Dict[str, Any]:
        """Get all communications (voicemail, SMS) for a phone number."""
        voicemails = [
            v for v in self.voicemails.values()
            if v.from_phone == phone_number or v.to_phone == phone_number
        ]

        text_messages = [
            t for t in self.text_messages.values()
            if t.from_phone == phone_number or t.to_phone == phone_number
        ]

        return {
            "phone_number": phone_number,
            "voicemail_count": len(voicemails),
            "text_message_count": len(text_messages),
            "voicemails": [v.to_dict() for v in voicemails],
            "text_messages": [t.to_dict() for t in text_messages],
        }

    def get_communications_for_email(self, email_address: str) -> Dict[str, Any]:
        """Get all email communications for an email address."""
        emails = [
            e for e in self.emails.values()
            if e.from_email == email_address or email_address in e.to_email
        ]

        return {
            "email_address": email_address,
            "email_count": len(emails),
            "emails": [e.to_dict() for e in emails],
        }

    def get_all_evidence_by_date(self, days: int = 90) -> Dict[str, Any]:
        """Get summary of all evidence within date range."""
        cutoff = datetime.now() - timedelta(days=days)

        recent_captures = [c for c in self.captures.values() if c.timestamp >= cutoff]
        recent_voicemails = [v for v in self.voicemails.values() if v.timestamp >= cutoff]
        recent_texts = [t for t in self.text_messages.values() if t.timestamp >= cutoff]
        recent_emails = [e for e in self.emails.values() if e.timestamp >= cutoff]
        recent_chats = [c for c in self.chat_messages.values() if c.timestamp >= cutoff]

        return {
            "period_days": days,
            "cutoff_date": cutoff.isoformat(),
            "summary": {
                "captures": len(recent_captures),
                "voicemails": len(recent_voicemails),
                "text_messages": len(recent_texts),
                "emails": len(recent_emails),
                "chat_messages": len(recent_chats),
                "total": (
                    len(recent_captures)
                    + len(recent_voicemails)
                    + len(recent_texts)
                    + len(recent_emails)
                    + len(recent_chats)
                ),
            },
            "captures": [c.to_dict() for c in recent_captures],
            "voicemails": [v.to_dict() for v in recent_voicemails],
            "text_messages": [t.to_dict() for t in recent_texts],
            "emails": [e.to_dict() for e in recent_emails],
            "chat_messages": [c.to_dict() for c in recent_chats],
        }


# =====================
# SINGLETON INSTANCE
# =====================

_av_manager: Optional[AVManager] = None


def get_av_manager() -> AVManager:
    """Get the singleton AV manager instance."""
    global _av_manager
    if _av_manager is None:
        _av_manager = AVManager()
    return _av_manager


def reset_av_manager() -> None:
    """Reset AV manager (useful for testing)."""
    global _av_manager
    _av_manager = None
