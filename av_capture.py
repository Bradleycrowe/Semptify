"""
Audio/Visual Capture Management Module

Provides capture tracking for video, audio, photos, and other evidence from mobile devices.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import uuid
import os
import json


@dataclass
class LocationData:
    """GPS location data for a capture."""
    
    latitude: float = 0.0
    longitude: float = 0.0
    accuracy_meters: float = 0.0
    altitude_meters: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert location to dictionary."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy_meters": self.accuracy_meters,
            "altitude_meters": self.altitude_meters,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class Capture:
    """A captured piece of evidence (video, audio, photo, etc.)."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capture_type: str = "unknown"  # video, audio, photo, voicemail, sms, email, chat
    source_type: str = "mobile"  # mobile, desktop, email, web, api
    file_path: Optional[str] = None
    actor_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    location: Optional[LocationData] = None
    device_name: Optional[str] = None
    description: str = ""
    duration_seconds: Optional[float] = None
    file_size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    metadata_extra: Dict[str, Any] = field(default_factory=dict)
    original_filename: Optional[str] = None
    linked_doc_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert capture to dictionary."""
        return {
            "id": self.id,
            "capture_type": self.capture_type,
            "source_type": self.source_type,
            "file_path": self.file_path,
            "actor_id": self.actor_id,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location.to_dict() if self.location else None,
            "device_name": self.device_name,
            "description": self.description,
            "duration_seconds": self.duration_seconds,
            "file_size_bytes": self.file_size_bytes,
            "mime_type": self.mime_type,
            "metadata_extra": self.metadata_extra,
            "original_filename": self.original_filename,
            "linked_doc_ids": self.linked_doc_ids,
            "tags": self.tags
        }


@dataclass
class ImportedMessage:
    """An imported message (SMS, email, chat, voicemail)."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: str = "unknown"  # sms, email, chat, voicemail
    from_address: Optional[str] = None
    to_addresses: List[str] = field(default_factory=list)
    subject: Optional[str] = None
    body: Optional[str] = None
    timestamp: Optional[datetime] = None
    actor_id: Optional[str] = None
    thread_id: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "message_type": self.message_type,
            "from_address": self.from_address,
            "to_addresses": self.to_addresses,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "actor_id": self.actor_id,
            "thread_id": self.thread_id,
            "attachments": self.attachments,
            "metadata": self.metadata
        }


class AVManager:
    """Manages audio/visual captures and imports."""
    
    def __init__(self, storage_dir: str = "uploads/evidence"):
        self.storage_dir = storage_dir
        self.captures: Dict[str, Capture] = {}
        self.messages: Dict[str, ImportedMessage] = {}
        os.makedirs(storage_dir, exist_ok=True)
    
    def register_capture(
        self,
        capture_type: str,
        source_type: str,
        file_path: str,
        actor_id: Optional[str] = None,
        location: Optional[LocationData] = None,
        device_name: Optional[str] = None,
        description: str = "",
        duration_seconds: Optional[float] = None,
        metadata_extra: Optional[Dict[str, Any]] = None,
        original_filename: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Capture:
        """Register a new capture."""
        # Get file size if file exists
        file_size = None
        if file_path and os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        
        # Determine MIME type based on capture type
        mime_types = {
            "video": "video/mp4",
            "audio": "audio/mpeg",
            "photo": "image/jpeg",
            "voicemail": "audio/mpeg",
        }
        mime_type = mime_types.get(capture_type)
        
        capture = Capture(
            capture_type=capture_type,
            source_type=source_type,
            file_path=file_path,
            actor_id=actor_id,
            location=location,
            device_name=device_name,
            description=description,
            duration_seconds=duration_seconds,
            file_size_bytes=file_size,
            mime_type=mime_type,
            metadata_extra=metadata_extra or {},
            original_filename=original_filename or os.path.basename(file_path) if file_path else None,
            tags=tags or []
        )
        
        self.captures[capture.id] = capture
        return capture
    
    def get_capture(self, capture_id: str) -> Optional[Capture]:
        """Get a capture by ID."""
        return self.captures.get(capture_id)
    
    def list_captures(
        self,
        capture_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Capture]:
        """List captures with optional filters."""
        results = list(self.captures.values())
        
        if capture_type:
            results = [c for c in results if c.capture_type == capture_type]
        
        if actor_id:
            results = [c for c in results if c.actor_id == actor_id]
        
        if tags:
            results = [c for c in results if any(tag in c.tags for tag in tags)]
        
        if start_date:
            results = [c for c in results if c.timestamp >= start_date]
        
        if end_date:
            results = [c for c in results if c.timestamp <= end_date]
        
        return results
    
    def link_capture_to_document(self, capture_id: str, doc_id: str) -> bool:
        """Link a capture to a document."""
        if capture_id in self.captures:
            if doc_id not in self.captures[capture_id].linked_doc_ids:
                self.captures[capture_id].linked_doc_ids.append(doc_id)
            return True
        return False
    
    def add_tags_to_capture(self, capture_id: str, tags: List[str]) -> bool:
        """Add tags to a capture."""
        if capture_id in self.captures:
            for tag in tags:
                if tag not in self.captures[capture_id].tags:
                    self.captures[capture_id].tags.append(tag)
            return True
        return False
    
    def import_message(
        self,
        message_type: str,
        from_address: str,
        to_addresses: List[str],
        subject: Optional[str] = None,
        body: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        actor_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ImportedMessage:
        """Import a message (SMS, email, chat, voicemail)."""
        message = ImportedMessage(
            message_type=message_type,
            from_address=from_address,
            to_addresses=to_addresses,
            subject=subject,
            body=body,
            timestamp=timestamp or datetime.now(),
            actor_id=actor_id,
            thread_id=thread_id,
            attachments=attachments or [],
            metadata=metadata or {}
        )
        
        self.messages[message.id] = message
        return message
    
    def get_message(self, message_id: str) -> Optional[ImportedMessage]:
        """Get a message by ID."""
        return self.messages.get(message_id)
    
    def list_messages(
        self,
        message_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ImportedMessage]:
        """List messages with optional filters."""
        results = list(self.messages.values())
        
        if message_type:
            results = [m for m in results if m.message_type == message_type]
        
        if actor_id:
            results = [m for m in results if m.actor_id == actor_id]
        
        if thread_id:
            results = [m for m in results if m.thread_id == thread_id]
        
        if start_date:
            results = [m for m in results if m.timestamp and m.timestamp >= start_date]
        
        if end_date:
            results = [m for m in results if m.timestamp and m.timestamp <= end_date]
        
        return results
    
    def get_statistics(self) -> dict:
        """Get statistics on captures and messages."""
        capture_counts = {}
        for capture in self.captures.values():
            capture_counts[capture.capture_type] = capture_counts.get(capture.capture_type, 0) + 1
        
        message_counts = {}
        for message in self.messages.values():
            message_counts[message.message_type] = message_counts.get(message.message_type, 0) + 1
        
        total_size = sum(
            c.file_size_bytes for c in self.captures.values()
            if c.file_size_bytes
        )
        
        return {
            "total_captures": len(self.captures),
            "total_messages": len(self.messages),
            "capture_types": capture_counts,
            "message_types": message_counts,
            "total_storage_bytes": total_size,
            "storage_mb": round(total_size / 1024 / 1024, 2) if total_size else 0
        }


# Singleton instance
_av_manager: Optional[AVManager] = None


def get_av_manager() -> AVManager:
    """Get the AV manager singleton."""
    global _av_manager
    if _av_manager is None:
        _av_manager = AVManager()
    return _av_manager
