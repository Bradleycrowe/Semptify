"""
Semptify Calendar UI Module

Provides human-facing views of the calendar and timeline:
- 12-Month Calendar View (grid/month)
- Timeline View (chronological list)
- Calendar Event Details View
- SQL Query View (data inspection)
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from engines.ledger_calendar_engine import get_calendar, get_ledger
from engines.data_flow_engine import get_data_flow


class CalendarUIManager:
    """Manager for rendering calendar and timeline views."""

    def get_12month_calendar(self, year: int) -> Dict[str, Any]:
        """Get 12-month calendar view with all events.

        Returns: Dict with months 1-12 and events for each day
        """
        calendar = get_calendar()
        result = {"year": year, "months": {}}

        for month in range(1, 13):
            month_events = {}

            # Get all days in month
            if month == 12:
                days_in_month = 31
            else:
                days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day

            for day in range(1, days_in_month + 1):
                date = datetime(year, month, day)
                month_events[day] = {
                    "date": date.isoformat(),
                    "day_name": date.strftime("%A"),
                    "events": [],
                }

            # Get all events for this month
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

            events = calendar.get_events(start_date=start_date, end_date=end_date)

            # Assign events to days
            for event in events:
                day = event.event_date.day
                if day in month_events:
                    month_events[day]["events"].append(self._format_event(event))

            result["months"][month] = {
                "month_name": datetime(year, month, 1).strftime("%B"),
                "days": month_events,
            }

        return result

    def get_timeline_view(
        self,
        days: int = 90,
        include_completed: bool = False,
        priority: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get chronological timeline view of upcoming events.

        Args:
            days: Number of days to include (default 90)
            include_completed: Include completed events
            priority: Filter by priority (0, 1, 2)

        Returns: Timeline with events ordered by date
        """
        calendar = get_calendar()
        now = datetime.now()
        end_date = now + timedelta(days=days)

        events = calendar.get_events(
            start_date=now,
            end_date=end_date,
            completed=False if not include_completed else None,
            priority=priority,
        )

        # Group by date
        timeline_by_date = {}
        for event in events:
            date_key = event.event_date.strftime("%Y-%m-%d")
            if date_key not in timeline_by_date:
                timeline_by_date[date_key] = {
                    "date": event.event_date.isoformat(),
                    "date_display": event.event_date.strftime("%A, %B %d, %Y"),
                    "events": [],
                }
            timeline_by_date[date_key]["events"].append(self._format_event(event))

        # Sort by date
        sorted_dates = sorted(timeline_by_date.keys())
        timeline = {
            "start_date": now.isoformat(),
            "end_date": end_date.isoformat(),
            "days_span": days,
            "total_events": len(events),
            "timeline": [timeline_by_date[date] for date in sorted_dates],
        }

        return timeline

    def get_event_details(self, event_id: str) -> Dict[str, Any]:
        """Get detailed view of a single event with related data.

        Returns: Event details with linked documents and ledger entries
        """
        calendar = get_calendar()

        # Find event
        for event in calendar.get_events():
            if event.id == event_id:
                details = self._format_event(event)

                # Get related ledger entries
                ledger = get_ledger()
                if event.related_entry_id:
                    for entry in ledger.get_entries():
                        if entry.id == event.related_entry_id:
                            details["ledger_entry"] = entry.to_dict()
                            break

                # Get data flow information
                flow = get_data_flow()
                if event.related_entry_id:
                    flow_info = flow.get_document_flow(event.related_entry_id)
                    details["data_flow"] = flow_info

                return details

        return {"error": "Event not found"}

    def get_calendar_query_view(
        self,
        event_type: Optional[str] = None,
        priority: Optional[int] = None,
        completed: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """SQL-style query view of calendar data.

        Returns: Structured query results with full event data
        """
        calendar = get_calendar()
        ledger = get_ledger()
        flow = get_data_flow()

        events = calendar.get_events(
            event_type=event_type,
            priority=priority,
            completed=completed,
            start_date=start_date,
            end_date=end_date,
        )

        # Build query results with joined data
        results = []
        for event in events:
            row = self._format_event(event)

            # Join with ledger if available
            if event.related_entry_id:
                for entry in ledger.get_entries():
                    if entry.id == event.related_entry_id:
                        row["ledger"] = {
                            "id": entry.id,
                            "type": entry.entry_type,
                            "actor": entry.actor,
                            "hash": entry.hash,
                            "files": entry.files,
                        }
                        break

            # Join with data flow if available
            if event.related_entry_id:
                flow_info = flow.get_document_flow(event.related_entry_id)
                if "flow_events" in flow_info:
                    row["flow_event_count"] = len(flow_info["flow_events"])

            results.append(row)

        return {
            "query": {
                "event_type": event_type,
                "priority": priority,
                "completed": completed,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
            },
            "result_count": len(results),
            "results": results,
        }

    def get_actor_calendar(self, actor_id: str, days: int = 90) -> Dict[str, Any]:
        """Get calendar view for a specific actor (user).

        Shows all events and documents associated with the actor.
        """
        calendar = get_calendar()
        ledger = get_ledger()
        flow = get_data_flow()

        # Get actor's events
        actor_events = calendar.get_events(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=days),
        )
        actor_events = [e for e in actor_events if e.related_entry_id]

        # Get actor's ledger entries
        actor_entries = ledger.get_entries(actor=actor_id)

        # Get actor's data flow
        actor_flow = flow.get_actor_flow(actor_id)

        return {
            "actor_id": actor_id,
            "period_days": days,
            "events": {
                "count": len(actor_events),
                "items": [self._format_event(e) for e in actor_events],
            },
            "ledger_entries": {
                "count": len(actor_entries),
                "items": [e.to_dict() for e in actor_entries],
            },
            "data_flow": actor_flow,
        }

    def get_priority_summary(self) -> Dict[str, Any]:
        """Get summary of high-priority upcoming events."""
        calendar = get_calendar()

        high_priority = calendar.get_upcoming_high_priority()
        upcoming_7days = calendar.get_upcoming_events(days=7)
        upcoming_30days = calendar.get_upcoming_events(days=30)

        return {
            "high_priority": {
                "count": len(high_priority),
                "events": [self._format_event(e) for e in high_priority],
            },
            "upcoming_7days": {
                "count": len(upcoming_7days),
                "events": [self._format_event(e) for e in upcoming_7days],
            },
            "upcoming_30days": {
                "count": len(upcoming_30days),
                "events": [self._format_event(e) for e in upcoming_30days],
            },
        }

    def _format_event(self, event) -> Dict[str, Any]:
        """Format event for display."""
        return {
            "id": event.id,
            "title": event.title,
            "date": event.event_date.isoformat(),
            "date_display": event.event_date.strftime("%a, %b %d, %Y at %I:%M %p"),
            "type": event.event_type,
            "priority": event.priority,
            "priority_label": ["Low", "Medium", "High"][event.priority],
            "description": event.description,
            "completed": event.completed,
            "completed_at": event.completed_at.isoformat() if event.completed_at else None,
            "days_until": (event.event_date.date() - datetime.now().date()).days,
        }

    def export_calendar_csv(self, days: int = 365) -> str:
        """Export calendar to CSV format for external tools."""
        calendar = get_calendar()
        now = datetime.now()
        events = calendar.get_events(
            start_date=now, end_date=now + timedelta(days=days)
        )

        csv_lines = ["Date,Title,Type,Priority,Description,Status"]
        for event in events:
            status = "Completed" if event.completed else "Pending"
            csv_lines.append(
                f'{event.event_date.strftime("%Y-%m-%d")},'
                f'"{event.title}",'
                f'{event.event_type},'
                f'{["Low", "Medium", "High"][event.priority]},'
                f'"{event.description}",'
                f'{status}'
            )

        return "\n".join(csv_lines)


def get_calendar_ui() -> CalendarUIManager:
    """Get calendar UI manager instance."""
    return CalendarUIManager()
