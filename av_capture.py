"""
Semptify Audio/Visual Capture Module

Handles evidence capture from mobile devices (Android, iOS, Windows):
- Video/audio recording with GPS location and timestamp
- Photo capture with EXIF metadata preservation
- QR code scanning and barcode generation
- File upload from mobile devices
- Metadata extraction and enrichment
- Tamper-proof storage with SHA256 hashing
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import mimetypes

_capture_lock = threading.Lock()

CAPTURE_DIR = Path("evidence_capture")
CAPTURE_METADATA_DIR = CAPTURE_DIR / "metadata"
CAPTURE_DIR.mkdir(exist_ok=True)
CAPTURE_METADATA_DIR.mkdir(exist_ok=True)


@dataclass
class LocationData:
    """GPS location information."""

    latitude: float
    longitude: float
    accuracy_meters: float
    altitude_meters: Optional[float] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy_meters": self.accuracy_meters,
            "altitude_meters": self.altitude_meters,
            "timestamp": self.timestamp.isoformat(),
            "map_url": f"https://maps.google.com/?q={self.latitude},{self.longitude}",
        }


@dataclass
class CaptureMetadata:
    """Metadata for captured evidence."""

    id: str
    capture_type: str  # "video", "audio", "photo", "qr_scan", "text", "voicemail", "sms", "email", "chat"
    source_type: str  # "android", "ios", "windows", "web", "email_import", "sms_import", "chat_import"
    timestamp: datetime
    device_name: Optional[str] = None
    app_version: Optional[str] = None
    location: Optional[LocationData] = None
    actor_id: Optional[str] = None
    description: str = ""
    duration_seconds: Optional[float] = None  # For audio/video
    file_path: Optional[str] = None
    file_size_bytes: int = 0
    mime_type: str = "application/octet-stream"
    hash_sha256: str = ""
    original_filename: str = ""
    metadata_extra: Dict[str, Any] = None
    linked_docs: List[str] = None  # Other doc IDs this is related to

    def __post_init__(self):
        if self.metadata_extra is None:
            self.metadata_extra = {}
        if self.linked_docs is None:
            self.linked_docs = []
        if not self.timestamp:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "capture_type": self.capture_type,
            "source_type": self.source_type,
            "timestamp": self.timestamp.isoformat(),
            "device_name": self.device_name,
            "app_version": self.app_version,
            "location": self.location.to_dict() if self.location else None,
            "actor_id": self.actor_id,
            "description": self.description,
            "duration_seconds": self.duration_seconds,
            "file_path": self.file_path,
            "file_size_bytes": self.file_size_bytes,
            "mime_type": self.mime_type,
            "hash_sha256": self.hash_sha256,
            "original_filename": self.original_filename,
            "metadata_extra": self.metadata_extra,
            "linked_docs": self.linked_docs,
        }


@dataclass
class VoicemailImport:
    """Imported voicemail message."""

    id: str
    timestamp: datetime
    from_phone: str
    to_phone: str
    duration_seconds: float
    transcription: Optional[str] = None
    audio_file_path: Optional[str] = None
    source_system: str = "phone"  # Which phone system
    raw_metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.raw_metadata is None:
            self.raw_metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "from_phone": self.from_phone,
            "to_phone": self.to_phone,
            "duration_seconds": self.duration_seconds,
            "transcription": self.transcription,
            "audio_file_path": self.audio_file_path,
            "source_system": self.source_system,
            "raw_metadata": self.raw_metadata,
        }


@dataclass
class TextMessageImport:
    """Imported SMS/text message."""

    id: str
    timestamp: datetime
    from_phone: str
    to_phone: str
    message_text: str
    is_outbound: bool
    source_system: str = "sms"
    raw_metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.raw_metadata is None:
            self.raw_metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "from_phone": self.from_phone,
            "to_phone": self.to_phone,
            "message_text": self.message_text,
            "is_outbound": self.is_outbound,
            "source_system": self.source_system,
            "raw_metadata": self.raw_metadata,
        }


@dataclass
class EmailImport:
    """Imported email message."""

    id: str
    timestamp: datetime
    from_email: str
    to_email: List[str]
    cc_email: List[str]
    subject: str
    body_text: str
    attachments: List[Dict[str, str]] = None  # {filename, hash, size}
    raw_headers: Dict[str, str] = None
    source_system: str = "email"

    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []
        if self.raw_headers is None:
            self.raw_headers = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "from_email": self.from_email,
            "to_email": self.to_email,
            "cc_email": self.cc_email,
            "subject": self.subject,
            "body_text": self.body_text,
            "attachments": self.attachments,
            "raw_headers": self.raw_headers,
            "source_system": self.source_system,
        }


@dataclass
class ChatMessageImport:
    """Imported chat message (Slack, Teams, Signal, etc)."""

    id: str
    timestamp: datetime
    from_user: str
    platform: str  # "slack", "teams", "signal", "whatsapp", "telegram", etc
    channel_or_thread: str
    message_text: str
    attachments: List[Dict[str, str]] = None  # {filename, hash, url}
    raw_metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []
        if self.raw_metadata is None:
            self.raw_metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "from_user": self.from_user,
            "platform": self.platform,
            "channel_or_thread": self.channel_or_thread,
            "message_text": self.message_text,
            "attachments": self.attachments,
            "raw_metadata": self.raw_metadata,
        }


class AVCaptureManager:
    """Manages all audio/visual capture and imports."""

    def __init__(self):
        self.metadata_file = CAPTURE_METADATA_DIR / "capture_metadata.json"
        self.voicemail_file = CAPTURE_METADATA_DIR / "voicemails.json"
        self.sms_file = CAPTURE_METADATA_DIR / "text_messages.json"
        self.email_file = CAPTURE_METADATA_DIR / "emails.json"
        self.chat_file = CAPTURE_METADATA_DIR / "chat_messages.json"

        self.captures: Dict[str, CaptureMetadata] = {}
        self.voicemails: Dict[str, VoicemailImport] = {}
        self.text_messages: Dict[str, TextMessageImport] = {}
        self.emails: Dict[str, EmailImport] = {}
        self.chat_messages: Dict[str, ChatMessageImport] = {}

        self.load()

    def register_capture(
        self,
        capture_type: str,
        source_type: str,
        file_path: Optional[str] = None,
        file_content: Optional[bytes] = None,
        actor_id: Optional[str] = None,
        location: Optional[LocationData] = None,
        device_name: Optional[str] = None,
        description: str = "",
        duration_seconds: Optional[float] = None,
        metadata_extra: Optional[Dict[str, Any]] = None,
        original_filename: str = "",
    ) -> CaptureMetadata:
        """Register a captured file (video, audio, photo).

        Args:
            capture_type: "video", "audio", "photo"
            source_type: "android", "ios", "windows", "web"
            file_path: Path where file is stored
            file_content: Raw file bytes (if not file_path)
            actor_id: Who captured it
            location: GPS location data
            device_name: Device identifier
            description: What was captured
            duration_seconds: For audio/video
            metadata_extra: Additional metadata
            original_filename: Original filename from device

        Returns: CaptureMetadata object
        """
        with _capture_lock:
            capture_id = str(uuid.uuid4())

            # Calculate hash
            hash_sha256 = ""
            file_size = 0

            if file_content:
                hash_sha256 = hashlib.sha256(file_content).hexdigest()
                file_size = len(file_content)
            elif file_path and Path(file_path).exists():
                hash_sha256 = self._hash_file(file_path)
                file_size = Path(file_path).stat().st_size

            mime_type, _ = mimetypes.guess_type(
                original_filename or file_path or capture_type
            )
            mime_type = mime_type or "application/octet-stream"

            capture = CaptureMetadata(
                id=capture_id,
                capture_type=capture_type,
                source_type=source_type,
                timestamp=datetime.now(),
                device_name=device_name,
                actor_id=actor_id,
                location=location,
                description=description,
                duration_seconds=duration_seconds,
                file_path=file_path,
                file_size_bytes=file_size,
                mime_type=mime_type,
                hash_sha256=hash_sha256,
                original_filename=original_filename,
                metadata_extra=metadata_extra or {},
            )

            self.captures[capture_id] = capture
            self._persist_captures()
            return capture

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
    ) -> VoicemailImport:
        """Import a voicemail message."""
        with _capture_lock:
            voicemail_id = str(uuid.uuid4())

            voicemail = VoicemailImport(
                id=voicemail_id,
                timestamp=timestamp,
                from_phone=from_phone,
                to_phone=to_phone,
                duration_seconds=duration_seconds,
                transcription=transcription,
                audio_file_path=audio_file_path,
                source_system=source_system,
                raw_metadata=raw_metadata or {},
            )

            self.voicemails[voicemail_id] = voicemail
            self._persist_voicemails()
            return voicemail

    def import_text_message(
        self,
        from_phone: str,
        to_phone: str,
        message_text: str,
        timestamp: datetime,
        is_outbound: bool,
        source_system: str = "sms",
        raw_metadata: Optional[Dict[str, Any]] = None,
    ) -> TextMessageImport:
        """Import an SMS/text message."""
        with _capture_lock:
            message_id = str(uuid.uuid4())

            message = TextMessageImport(
                id=message_id,
                timestamp=timestamp,
                from_phone=from_phone,
                to_phone=to_phone,
                message_text=message_text,
                is_outbound=is_outbound,
                source_system=source_system,
                raw_metadata=raw_metadata or {},
            )

            self.text_messages[message_id] = message
            self._persist_text_messages()
            return message

    def import_email(
        self,
        from_email: str,
        to_email: List[str],
        subject: str,
        body_text: str,
        timestamp: datetime,
        cc_email: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, str]]] = None,
        raw_headers: Optional[Dict[str, str]] = None,
        source_system: str = "email",
    ) -> EmailImport:
        """Import an email message."""
        with _capture_lock:
            email_id = str(uuid.uuid4())

            email = EmailImport(
                id=email_id,
                timestamp=timestamp,
                from_email=from_email,
                to_email=to_email,
                cc_email=cc_email or [],
                subject=subject,
                body_text=body_text,
                attachments=attachments or [],
                raw_headers=raw_headers or {},
                source_system=source_system,
            )

            self.emails[email_id] = email
            self._persist_emails()
            return email

    def import_chat_message(
        self,
        from_user: str,
        platform: str,
        channel_or_thread: str,
        message_text: str,
        timestamp: datetime,
        attachments: Optional[List[Dict[str, str]]] = None,
        raw_metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatMessageImport:
        """Import a chat message (Slack, Teams, Signal, etc)."""
        with _capture_lock:
            chat_id = str(uuid.uuid4())

            chat = ChatMessageImport(
                id=chat_id,
                timestamp=timestamp,
                from_user=from_user,
                platform=platform,
                channel_or_thread=channel_or_thread,
                message_text=message_text,
                attachments=attachments or [],
                raw_metadata=raw_metadata or {},
            )

            self.chat_messages[chat_id] = chat
            self._persist_chat_messages()
            return chat

    def get_capture(self, capture_id: str) -> Optional[CaptureMetadata]:
        """Get capture metadata by ID."""
        with _capture_lock:
            return self.captures.get(capture_id)

    def get_captures_by_type(self, capture_type: str) -> List[CaptureMetadata]:
        """Get all captures of a specific type."""
        with _capture_lock:
            return [c for c in self.captures.values() if c.capture_type == capture_type]

    def get_captures_by_actor(self, actor_id: str) -> List[CaptureMetadata]:
        """Get all captures by a specific actor."""
        with _capture_lock:
            return [c for c in self.captures.values() if c.actor_id == actor_id]

    def get_captures_in_timerange(
        self, start: datetime, end: datetime
    ) -> List[CaptureMetadata]:
        """Get all captures within a time range."""
        with _capture_lock:
            return [
                c
                for c in self.captures.values()
                if start <= c.timestamp <= end
            ]

    def get_communications_for_number(self, phone_number: str) -> Dict[str, Any]:
        """Get all communications (voicemail, SMS, etc) for a phone number."""
        with _capture_lock:
            voicemails = [
                v
                for v in self.voicemails.values()
                if v.from_phone == phone_number or v.to_phone == phone_number
            ]
            messages = [
                m
                for m in self.text_messages.values()
                if m.from_phone == phone_number or m.to_phone == phone_number
            ]

            return {
                "phone_number": phone_number,
                "voicemails": [v.to_dict() for v in voicemails],
                "text_messages": [m.to_dict() for m in messages],
            }

    def get_communications_for_email(self, email_address: str) -> Dict[str, Any]:
        """Get all communications (email) for an email address."""
        with _capture_lock:
            emails = [
                e
                for e in self.emails.values()
                if e.from_email == email_address
                or email_address in e.to_email
                or email_address in e.cc_email
            ]

            return {
                "email_address": email_address,
                "emails": [e.to_dict() for e in emails],
            }

    def get_all_evidence_by_date(self, days: int = 90) -> Dict[str, List]:
        """Get all evidence (captures + communications) for past N days."""
        cutoff = datetime.now() - timedelta(days=days)

        with _capture_lock:
            captures = [
                c for c in self.captures.values() if c.timestamp >= cutoff
            ]
            voicemails = [
                v for v in self.voicemails.values() if v.timestamp >= cutoff
            ]
            texts = [
                m for m in self.text_messages.values() if m.timestamp >= cutoff
            ]
            emails = [
                e for e in self.emails.values() if e.timestamp >= cutoff
            ]
            chats = [
                c for c in self.chat_messages.values() if c.timestamp >= cutoff
            ]

            return {
                "period_days": days,
                "captures": [c.to_dict() for c in captures],
                "voicemails": [v.to_dict() for v in voicemails],
                "text_messages": [m.to_dict() for m in texts],
                "emails": [e.to_dict() for e in emails],
                "chat_messages": [c.to_dict() for c in chats],
                "total_items": len(captures)
                + len(voicemails)
                + len(texts)
                + len(emails)
                + len(chats),
            }

    def _hash_file(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"Error hashing file {file_path}: {e}")
            return ""

    def load(self):
        """Load all metadata from persistent storage."""
        with _capture_lock:
            self._load_captures()
            self._load_voicemails()
            self._load_text_messages()
            self._load_emails()
            self._load_chat_messages()

    def _load_captures(self):
        """Load capture metadata."""
        if self.metadata_file.exists():
            try:
                data = json.loads(self.metadata_file.read_text())
                for item in data:
                    location_data = None
                    if item.get("location"):
                        loc = item["location"]
                        location_data = LocationData(
                            latitude=loc["latitude"],
                            longitude=loc["longitude"],
                            accuracy_meters=loc["accuracy_meters"],
                            altitude_meters=loc.get("altitude_meters"),
                            timestamp=datetime.fromisoformat(loc["timestamp"]),
                        )

                    self.captures[item["id"]] = CaptureMetadata(
                        id=item["id"],
                        capture_type=item["capture_type"],
                        source_type=item["source_type"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        device_name=item.get("device_name"),
                        app_version=item.get("app_version"),
                        location=location_data,
                        actor_id=item.get("actor_id"),
                        description=item.get("description", ""),
                        duration_seconds=item.get("duration_seconds"),
                        file_path=item.get("file_path"),
                        file_size_bytes=item.get("file_size_bytes", 0),
                        mime_type=item.get("mime_type", "application/octet-stream"),
                        hash_sha256=item.get("hash_sha256", ""),
                        original_filename=item.get("original_filename", ""),
                        metadata_extra=item.get("metadata_extra", {}),
                        linked_docs=item.get("linked_docs", []),
                    )
            except Exception as e:
                print(f"Error loading captures: {e}")

    def _load_voicemails(self):
        """Load voicemail metadata."""
        if self.voicemail_file.exists():
            try:
                data = json.loads(self.voicemail_file.read_text())
                for item in data:
                    self.voicemails[item["id"]] = VoicemailImport(
                        id=item["id"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        from_phone=item["from_phone"],
                        to_phone=item["to_phone"],
                        duration_seconds=item["duration_seconds"],
                        transcription=item.get("transcription"),
                        audio_file_path=item.get("audio_file_path"),
                        source_system=item.get("source_system", "phone"),
                        raw_metadata=item.get("raw_metadata", {}),
                    )
            except Exception as e:
                print(f"Error loading voicemails: {e}")

    def _load_text_messages(self):
        """Load text message metadata."""
        if self.sms_file.exists():
            try:
                data = json.loads(self.sms_file.read_text())
                for item in data:
                    self.text_messages[item["id"]] = TextMessageImport(
                        id=item["id"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        from_phone=item["from_phone"],
                        to_phone=item["to_phone"],
                        message_text=item["message_text"],
                        is_outbound=item["is_outbound"],
                        source_system=item.get("source_system", "sms"),
                        raw_metadata=item.get("raw_metadata", {}),
                    )
            except Exception as e:
                print(f"Error loading text messages: {e}")

    def _load_emails(self):
        """Load email metadata."""
        if self.email_file.exists():
            try:
                data = json.loads(self.email_file.read_text())
                for item in data:
                    self.emails[item["id"]] = EmailImport(
                        id=item["id"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        from_email=item["from_email"],
                        to_email=item["to_email"],
                        cc_email=item.get("cc_email", []),
                        subject=item["subject"],
                        body_text=item["body_text"],
                        attachments=item.get("attachments", []),
                        raw_headers=item.get("raw_headers", {}),
                        source_system=item.get("source_system", "email"),
                    )
            except Exception as e:
                print(f"Error loading emails: {e}")

    def _load_chat_messages(self):
        """Load chat message metadata."""
        if self.chat_file.exists():
            try:
                data = json.loads(self.chat_file.read_text())
                for item in data:
                    self.chat_messages[item["id"]] = ChatMessageImport(
                        id=item["id"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        from_user=item["from_user"],
                        platform=item["platform"],
                        channel_or_thread=item["channel_or_thread"],
                        message_text=item["message_text"],
                        attachments=item.get("attachments", []),
                        raw_metadata=item.get("raw_metadata", {}),
                    )
            except Exception as e:
                print(f"Error loading chat messages: {e}")

    def _persist_captures(self):
        """Save capture metadata to disk."""
        with _capture_lock:
            data = [c.to_dict() for c in self.captures.values()]
            self.metadata_file.write_text(json.dumps(data, indent=2))

    def _persist_voicemails(self):
        """Save voicemail metadata to disk."""
        with _capture_lock:
            data = [v.to_dict() for v in self.voicemails.values()]
            self.voicemail_file.write_text(json.dumps(data, indent=2))

    def _persist_text_messages(self):
        """Save text message metadata to disk."""
        with _capture_lock:
            data = [m.to_dict() for m in self.text_messages.values()]
            self.sms_file.write_text(json.dumps(data, indent=2))

    def _persist_emails(self):
        """Save email metadata to disk."""
        with _capture_lock:
            data = [e.to_dict() for e in self.emails.values()]
            self.email_file.write_text(json.dumps(data, indent=2))

    def _persist_chat_messages(self):
        """Save chat message metadata to disk."""
        with _capture_lock:
            data = [c.to_dict() for c in self.chat_messages.values()]
            self.chat_file.write_text(json.dumps(data, indent=2))


# Global instance
_av_manager: Optional[AVCaptureManager] = None


def get_av_manager() -> AVCaptureManager:
    """Get or create global AV manager."""
    global _av_manager
    if _av_manager is None:
        _av_manager = AVCaptureManager()
    return _av_manager
