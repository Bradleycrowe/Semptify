"""Tests for Ledger & Calendar system."""
import pytest
import json
import tempfile
from datetime import datetime, timedelta
from engines.ledger_calendar_engine import (
    Ledger,
    Calendar,
    LedgerEntry,
    CalendarEvent,
    log_action,
    schedule_event,
    init_ledger_calendar,
)


class TestLedgerEntry:
    """Test LedgerEntry class."""

    def test_create_entry(self):
        """Verify ledger entry creation and certificate generation."""
        entry = LedgerEntry(
            entry_type="document",
            actor="user-123",
            data={"file": "lease.pdf", "size": 1024},
        )

        assert entry.id
        assert entry.timestamp > 0
        assert entry.entry_type == "document"
        assert entry.actor == "user-123"
        assert entry.hash  # SHA256 hash
        assert "entry_id" in entry.certificate
        assert entry.certificate["sha256"] == entry.hash

    def test_entry_to_dict(self):
        """Verify entry serialization."""
        entry = LedgerEntry(
            entry_type="payment",
            actor="tenant",
            data={"amount": 1200, "date": "2025-01-01"},
        )
        d = entry.to_dict()

        assert "id" in d
        assert "timestamp" in d
        assert "hash" in d
        assert "certificate" in d
        assert d["entry_type"] == "payment"


class TestLedger:
    """Test Ledger class."""

    def test_add_and_get_entry(self):
        """Verify adding and retrieving entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Ledger(tmpdir)

            entry = LedgerEntry(
                entry_type="document",
                actor="user-1",
                data={"doc": "test.pdf"},
            )
            ledger.add_entry(entry)

            retrieved = ledger.get_entries()
            assert len(retrieved) == 1
            assert retrieved[0].id == entry.id

    def test_filter_by_type(self):
        """Verify filtering by entry type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Ledger(tmpdir)

            ledger.add_entry(LedgerEntry("document", "user-1", {"file": "a.pdf"}))
            ledger.add_entry(LedgerEntry("payment", "user-1", {"amount": 100}))
            ledger.add_entry(LedgerEntry("document", "user-2", {"file": "b.pdf"}))

            docs = ledger.get_entries(entry_type="document")
            payments = ledger.get_entries(entry_type="payment")

            assert len(docs) == 2
            assert len(payments) == 1

    def test_filter_by_actor(self):
        """Verify filtering by actor."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Ledger(tmpdir)

            ledger.add_entry(LedgerEntry("document", "user-1", {"file": "a.pdf"}))
            ledger.add_entry(LedgerEntry("document", "user-1", {"file": "b.pdf"}))
            ledger.add_entry(LedgerEntry("document", "user-2", {"file": "c.pdf"}))

            user1_entries = ledger.get_entries(actor="user-1")
            user2_entries = ledger.get_entries(actor="user-2")

            assert len(user1_entries) == 2
            assert len(user2_entries) == 1

    def test_export_for_court(self):
        """Verify court-admissible export format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Ledger(tmpdir)

            entry1 = LedgerEntry("document", "user-1", {"file": "a.pdf"})
            entry2 = LedgerEntry("payment", "user-1", {"amount": 100})
            ledger.add_entry(entry1)
            ledger.add_entry(entry2)

            export = ledger.export_for_court()

            assert "export_timestamp" in export
            assert "entry_count" in export
            assert len(export["entries"]) == 2

    def test_persistence(self):
        """Verify ledger persists to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger1 = Ledger(tmpdir)
            entry = LedgerEntry("document", "user-1", {"file": "test.pdf"})
            ledger1.add_entry(entry)

            # Create new instance, should reload
            ledger2 = Ledger(tmpdir)
            entries = ledger2.get_entries()

            assert len(entries) == 1
            assert entries[0].id == entry.id


class TestCalendarEvent:
    """Test CalendarEvent class."""

    def test_create_event(self):
        """Verify calendar event creation."""
        date = datetime.now() + timedelta(days=7)
        event = CalendarEvent(
            title="Send Notice",
            event_date=date,
            event_type="action_needed",
            priority=2,
        )

        assert event.id
        assert event.title == "Send Notice"
        assert event.event_type == "action_needed"
        assert event.priority == 2
        assert not event.completed

    def test_event_to_dict(self):
        """Verify event serialization."""
        date = datetime.now()
        event = CalendarEvent("Test Event", date, "deadline")
        d = event.to_dict()

        assert "id" in d
        assert "title" in d
        assert "event_date" in d
        assert "event_type" in d


class TestCalendar:
    """Test Calendar class."""

    def test_add_and_get_event(self):
        """Verify adding and retrieving events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calendar = Calendar(tmpdir)
            date = datetime.now() + timedelta(days=7)

            event = CalendarEvent("Test", date, "deadline")
            calendar.add_event(event)

            retrieved = calendar.get_events()
            assert len(retrieved) == 1
            assert retrieved[0].id == event.id

    def test_upcoming_events(self):
        """Verify getting upcoming events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calendar = Calendar(tmpdir)

            today = datetime.now()
            calendar.add_event(CalendarEvent("Tomorrow", today + timedelta(days=1), "action_needed"))
            calendar.add_event(CalendarEvent("Next week", today + timedelta(days=10), "action_needed"))

            upcoming = calendar.get_upcoming_events(days=3)
            assert len(upcoming) == 1  # Only "Tomorrow" within 3 days

    def test_mark_completed(self):
        """Verify marking event as completed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calendar = Calendar(tmpdir)
            event = CalendarEvent("Test", datetime.now(), "action_needed")
            calendar.add_event(event)

            calendar.mark_completed(event.id)

            completed = calendar.get_events(completed=True)
            assert len(completed) == 1

    def test_high_priority_upcoming(self):
        """Verify filtering high-priority upcoming events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calendar = Calendar(tmpdir)
            today = datetime.now()

            calendar.add_event(CalendarEvent("Low priority", today + timedelta(days=1), "action_needed", priority=0))
            calendar.add_event(CalendarEvent("High priority soon", today + timedelta(days=1), "action_needed", priority=2))
            calendar.add_event(CalendarEvent("High priority later", today + timedelta(days=10), "action_needed", priority=2))

            high_priority = calendar.get_upcoming_high_priority()
            assert len(high_priority) == 1
            assert high_priority[0].title == "High priority soon"

    def test_persistence(self):
        """Verify calendar persists to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calendar1 = Calendar(tmpdir)
            date = datetime.now() + timedelta(days=7)
            event = CalendarEvent("Test", date, "deadline")
            calendar1.add_event(event)

            # Create new instance, should reload
            calendar2 = Calendar(tmpdir)
            events = calendar2.get_events()

            assert len(events) == 1
            assert events[0].id == event.id


class TestIntegrationEndpoints:
    """Test Ledger & Calendar API endpoints."""

    def test_ledger_api_endpoint(self, client):
        """Verify /api/ledger-calendar/ledger endpoint."""
        resp = client.get("/api/ledger-calendar/ledger")
        assert resp.status_code == 200

        data = resp.get_json()
        assert "entries" in data
        assert "total" in data

    def test_calendar_api_endpoint(self, client):
        """Verify /api/ledger-calendar/calendar endpoint."""
        resp = client.get("/api/ledger-calendar/calendar")
        assert resp.status_code == 200

        data = resp.get_json()
        assert "events" in data
        assert "total" in data

    def test_create_calendar_event_api(self, client):
        """Verify creating calendar event via API."""
        resp = client.post(
            "/api/ledger-calendar/calendar/event",
            json={
                "title": "Test Event",
                "event_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "type": "action_needed",
                "priority": 2,
            },
        )

        assert resp.status_code == 201
        data = resp.get_json()
        assert data["title"] == "Test Event"
        assert data["priority"] == 2

    def test_log_action_api(self, client):
        """Verify logging action via API."""
        resp = client.post(
            "/api/ledger-calendar/action/log",
            json={
                "action_type": "document",
                "actor": "test-user",
                "description": "Uploaded test document",
                "data": {"file": "test.pdf", "size": 1024},
            },
        )

        assert resp.status_code == 201
        data = resp.get_json()
        assert data["entry_type"] == "document"
        assert "certificate" in data
        assert "hash" in data

    def test_dashboard_api(self, client):
        """Verify /api/ledger-calendar/dashboard endpoint."""
        resp = client.get("/api/ledger-calendar/dashboard")
        assert resp.status_code == 200

        data = resp.get_json()
        assert "ledger" in data
        assert "calendar" in data
        assert "recent_entries" in data["ledger"]
        assert "upcoming_events" in data["calendar"]
