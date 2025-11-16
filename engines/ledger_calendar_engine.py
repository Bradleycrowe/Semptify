"""
Semptify Ledger & Calendar System

Central record-keeping for all actions, documents, and legal events.
- Ledger: Append-only log with SHA256 hashes and certificates
- Calendar: Time-based view of events and deadlines
- Integration: All modules feed data into ledger/calendar
"""

import os
import json
import hashlib
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading

# Thread-safe access to ledger data
_ledger_lock = threading.Lock()


class LedgerEntry:
    """A single record in the ledger (tamper-proof, timestamped)."""

    def __init__(
        self,
        entry_type: str,  # "document", "payment", "complaint", "evidence", "notice", "action"
        actor: str,  # who made the action (user_id, system, admin)
        data: Dict[str, Any],  # action-specific data
        files: Optional[List[str]] = None,  # file paths associated with entry
    ):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.entry_type = entry_type
        self.actor = actor
        self.data = data
        self.files = files or []
        self.hash = self._compute_hash()
        self.certificate = self._generate_certificate()

    def _compute_hash(self) -> str:
        """Compute SHA256 hash of entry data (for tamper-proofing)."""
        content = json.dumps(
            {
                "timestamp": self.timestamp,
                "type": self.entry_type,
                "actor": self.actor,
                "data": self.data,
            },
            sort_keys=True,
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _generate_certificate(self) -> Dict[str, Any]:
        """Generate a certificate for this entry (legal audit trail)."""
        return {
            "entry_id": self.id,
            "timestamp": self.timestamp,
            "timestamp_iso": datetime.fromtimestamp(self.timestamp).isoformat(),
            "entry_type": self.entry_type,
            "actor": self.actor,
            "sha256": self.hash,
            "files_count": len(self.files),
            "data_summary": {k: v for k, v in self.data.items() if k != "content"},
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary for storage/export."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "entry_type": self.entry_type,
            "actor": self.actor,
            "data": self.data,
            "files": self.files,
            "hash": self.hash,
            "certificate": self.certificate,
        }


class Ledger:
    """Central ledger: append-only record of all actions."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.ledger_file = self.data_dir / "ledger.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._entries: List[LedgerEntry] = []
        self._load()

    def _load(self) -> None:
        """Load existing ledger entries from disk."""
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            entry_dict = json.loads(line)
                            # Recreate entry object (minimal reconstruction)
                            entry = LedgerEntry(
                                entry_type=entry_dict["entry_type"],
                                actor=entry_dict["actor"],
                                data=entry_dict["data"],
                                files=entry_dict.get("files", []),
                            )
                            entry.id = entry_dict["id"]
                            entry.timestamp = entry_dict["timestamp"]
                            entry.hash = entry_dict["hash"]
                            self._entries.append(entry)
            except Exception as e:
                print(f"Warning: Failed to load ledger: {e}")

    def add_entry(self, entry: LedgerEntry) -> None:
        """Add a new entry to the ledger (thread-safe, append-only)."""
        with _ledger_lock:
            self._entries.append(entry)
            # Append to file (atomic write)
            with open(self.ledger_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")

    def get_entries(
        self,
        entry_type: Optional[str] = None,
        actor: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> List[LedgerEntry]:
        """Query ledger entries with optional filters."""
        with _ledger_lock:
            results = self._entries

            if entry_type:
                results = [e for e in results if e.entry_type == entry_type]
            if actor:
                results = [e for e in results if e.actor == actor]
            if start_time:
                results = [e for e in results if e.timestamp >= start_time]
            if end_time:
                results = [e for e in results if e.timestamp <= end_time]

            return sorted(results, key=lambda e: e.timestamp)

    def export_for_court(self, entry_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Export ledger entries suitable for legal/court review."""
        with _ledger_lock:
            entries_to_export = self._entries
            if entry_ids:
                entries_to_export = [e for e in entries_to_export if e.id in entry_ids]

        return {
            "export_timestamp": time.time(),
            "export_timestamp_iso": datetime.now().isoformat(),
            "entry_count": len(entries_to_export),
            "entries": [e.to_dict() for e in entries_to_export],
        }


class CalendarEvent:
    """A calendar event (deadline, reminder, action needed)."""

    def __init__(
        self,
        title: str,
        event_date: datetime,
        event_type: str,  # "deadline", "reminder", "action_needed", "completed"
        description: str = "",
        related_entry_id: Optional[str] = None,
        priority: int = 0,  # 0=low, 1=medium, 2=high
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.event_date = event_date
        self.event_type = event_type
        self.description = description
        self.related_entry_id = related_entry_id
        self.priority = priority
        self.created_at = datetime.now()
        self.completed = False
        self.completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "event_type": self.event_type,
            "description": self.description,
            "related_entry_id": self.related_entry_id,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "completed": self.completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class Calendar:
    """Calendar: time-based view of events and deadlines."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.calendar_file = self.data_dir / "calendar.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._events: List[CalendarEvent] = []
        self._load()

    def _load(self) -> None:
        """Load existing calendar events from disk."""
        if self.calendar_file.exists():
            try:
                with open(self.calendar_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            event_dict = json.loads(line)
                            event = CalendarEvent(
                                title=event_dict["title"],
                                event_date=datetime.fromisoformat(event_dict["event_date"]),
                                event_type=event_dict["event_type"],
                                description=event_dict.get("description", ""),
                                related_entry_id=event_dict.get("related_entry_id"),
                                priority=event_dict.get("priority", 0),
                            )
                            event.id = event_dict["id"]
                            event.created_at = datetime.fromisoformat(event_dict["created_at"])
                            event.completed = event_dict.get("completed", False)
                            if event_dict.get("completed_at"):
                                event.completed_at = datetime.fromisoformat(event_dict["completed_at"])
                            self._events.append(event)
            except Exception as e:
                print(f"Warning: Failed to load calendar: {e}")

    def add_event(self, event: CalendarEvent) -> None:
        """Add a new calendar event (thread-safe, append-only)."""
        with _ledger_lock:
            self._events.append(event)
            # Append to file
            with open(self.calendar_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.to_dict()) + "\n")

    def get_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        event_type: Optional[str] = None,
        priority: Optional[int] = None,
        completed: Optional[bool] = None,
    ) -> List[CalendarEvent]:
        """Query calendar events with optional filters."""
        with _ledger_lock:
            results = self._events

            if start_date:
                results = [e for e in results if e.event_date >= start_date]
            if end_date:
                results = [e for e in results if e.event_date <= end_date]
            if event_type:
                results = [e for e in results if e.event_type == event_type]
            if priority is not None:
                results = [e for e in results if e.priority == priority]
            if completed is not None:
                results = [e for e in results if e.completed == completed]

            return sorted(results, key=lambda e: e.event_date)

    def get_upcoming_events(self, days: int = 7) -> List[CalendarEvent]:
        """Get upcoming events within N days."""
        now = datetime.now()
        future = now + timedelta(days=days)
        return self.get_events(start_date=now, end_date=future, completed=False)

    def mark_completed(self, event_id: str) -> None:
        """Mark an event as completed."""
        with _ledger_lock:
            for event in self._events:
                if event.id == event_id:
                    event.completed = True
                    event.completed_at = datetime.now()
                    # Re-write calendar file
                    with open(self.calendar_file, "w", encoding="utf-8") as f:
                        for e in self._events:
                            f.write(json.dumps(e.to_dict()) + "\n")
                    break

    def get_upcoming_high_priority(self) -> List[CalendarEvent]:
        """Get high-priority events due soon."""
        return self.get_events(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=3),
            priority=2,
            completed=False,
        )


# Global instances
_ledger: Optional[Ledger] = None
_calendar: Optional[Calendar] = None


def init_ledger_calendar(data_dir: str = None) -> tuple[Ledger, Calendar]:
    """Initialize global ledger and calendar instances."""
    global _ledger, _calendar

    if data_dir is None:
        data_dir = os.path.join(os.getcwd(), "data")

    _ledger = Ledger(data_dir)
    _calendar = Calendar(data_dir)

    return _ledger, _calendar


def get_ledger() -> Ledger:
    """Get the global ledger instance."""
    global _ledger
    if _ledger is None:
        init_ledger_calendar()
    return _ledger


def get_calendar() -> Calendar:
    """Get the global calendar instance."""
    global _calendar
    if _calendar is None:
        init_ledger_calendar()
    return _calendar


def log_action(
    action_type: str,
    actor: str,
    description: str,
    data: Dict[str, Any],
    files: Optional[List[str]] = None,
) -> LedgerEntry:
    """Convenience function: log an action to the ledger."""
    entry = LedgerEntry(entry_type=action_type, actor=actor, data=data, files=files)
    get_ledger().add_entry(entry)
    return entry


def schedule_event(
    title: str,
    event_date: datetime,
    event_type: str = "action_needed",
    description: str = "",
    related_entry_id: Optional[str] = None,
    priority: int = 0,
) -> CalendarEvent:
    """Convenience function: add an event to the calendar."""
    event = CalendarEvent(
        title=title,
        event_date=event_date,
        event_type=event_type,
        description=description,
        related_entry_id=related_entry_id,
        priority=priority,
    )
    get_calendar().add_event(event)
    return event
