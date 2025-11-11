"""
Calendar & Ledger Timeline System for Semptify
Visualizes rent payments, court dates, deadlines, and notices on an interactive timeline
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CalendarTimelineEngine:
    """
    Manages timeline events for rent, court, deadlines, and notices.
    Supports filtering, searching, and exporting to PDF/iCal formats.
    """
    
    def __init__(self, data_file='data/timeline_events.json'):
        self.data_file = data_file
        self.events = self._load_events()
        
        # Event type configuration with colors and icons
        self.event_types = {
            'rent_payment': {
                'label': 'Rent Payment',
                'color': '#3b82f6',  # Blue
                'icon': '💵',
                'category': 'financial'
            },
            'court_date': {
                'label': 'Court Appearance',
                'color': '#ef4444',  # Red
                'icon': '⚖️',
                'category': 'legal'
            },
            'deadline': {
                'label': 'Deadline',
                'color': '#f59e0b',  # Orange
                'icon': '⏰',
                'category': 'administrative'
            },
            'notice_received': {
                'label': 'Notice Received',
                'color': '#8b5cf6',  # Purple
                'icon': '📄',
                'category': 'communication'
            },
            'inspection': {
                'label': 'Inspection',
                'color': '#10b981',  # Green
                'icon': '🔍',
                'category': 'property'
            },
            'maintenance_request': {
                'label': 'Maintenance Request',
                'color': '#06b6d4',  # Cyan
                'icon': '🔧',
                'category': 'property'
            },
            'lease_milestone': {
                'label': 'Lease Milestone',
                'color': '#6366f1',  # Indigo
                'icon': '📋',
                'category': 'legal'
            }
        }
    
    def _load_events(self) -> List[Dict]:
        """Load events from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_events(self):
        """Save events to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
    
    def add_event(self, event_type: str, date: str, title: str, 
                  description: str = '', amount: Optional[float] = None,
                  status: str = 'upcoming', user_id: str = None,
                  metadata: Dict = None) -> Dict:
        """
        Add a new timeline event.
        
        Args:
            event_type: Type of event (rent_payment, court_date, etc.)
            date: ISO format date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
            title: Event title
            description: Optional description
            amount: Optional dollar amount (for payments)
            status: upcoming, completed, missed, cancelled
            user_id: Associated user ID
            metadata: Additional data (tracking numbers, case numbers, etc.)
        
        Returns:
            Created event dict with generated ID
        """
        event_id = f"evt_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        event = {
            'id': event_id,
            'type': event_type,
            'date': date,
            'title': title,
            'description': description,
            'amount': amount,
            'status': status,
            'user_id': user_id,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.events.append(event)
        self._save_events()
        return event
    
    def get_events(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None,
                   event_types: Optional[List[str]] = None,
                   status: Optional[str] = None,
                   user_id: Optional[str] = None) -> List[Dict]:
        """
        Get filtered timeline events.
        
        Args:
            start_date: Filter events after this date (ISO format)
            end_date: Filter events before this date (ISO format)
            event_types: List of event types to include
            status: Filter by status
            user_id: Filter by user
        
        Returns:
            List of matching events, sorted by date
        """
        filtered = self.events
        
        # Filter by date range
        if start_date:
            filtered = [e for e in filtered if e['date'] >= start_date]
        if end_date:
            filtered = [e for e in filtered if e['date'] <= end_date]
        
        # Filter by event type
        if event_types:
            filtered = [e for e in filtered if e['type'] in event_types]
        
        # Filter by status
        if status:
            filtered = [e for e in filtered if e['status'] == status]
        
        # Filter by user
        if user_id:
            filtered = [e for e in filtered if e.get('user_id') == user_id]
        
        # Sort by date
        return sorted(filtered, key=lambda x: x['date'])
    
    def update_event(self, event_id: str, updates: Dict) -> bool:
        """Update an existing event"""
        for event in self.events:
            if event['id'] == event_id:
                event.update(updates)
                event['updated_at'] = datetime.now().isoformat()
                self._save_events()
                return True
        return False
    
    def delete_event(self, event_id: str) -> bool:
        """Delete an event"""
        initial_len = len(self.events)
        self.events = [e for e in self.events if e['id'] != event_id]
        if len(self.events) < initial_len:
            self._save_events()
            return True
        return False
    
    def get_rent_ledger(self, user_id: Optional[str] = None) -> Dict:
        """
        Get rent payment history and calculate totals.
        
        Returns:
            Dict with payments list, total paid, total due, balance
        """
        rent_events = self.get_events(
            event_types=['rent_payment'],
            user_id=user_id
        )
        
        total_paid = sum(e.get('amount', 0) for e in rent_events if e['status'] == 'completed')
        total_due = sum(e.get('amount', 0) for e in rent_events if e['status'] in ['upcoming', 'missed'])
        
        return {
            'payments': rent_events,
            'total_paid': total_paid,
            'total_due': total_due,
            'balance': total_due - total_paid,
            'payment_count': len(rent_events),
            'missed_count': len([e for e in rent_events if e['status'] == 'missed'])
        }
    
    def get_upcoming_deadlines(self, days_ahead: int = 30, user_id: Optional[str] = None) -> List[Dict]:
        """Get deadlines in the next N days"""
        today = datetime.now().date().isoformat()
        end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
        
        deadlines = self.get_events(
            start_date=today,
            end_date=end_date,
            event_types=['deadline', 'court_date'],
            status='upcoming',
            user_id=user_id
        )
        
        # Add urgency level
        for event in deadlines:
            event_date = datetime.fromisoformat(event['date'][:10])
            days_until = (event_date.date() - datetime.now().date()).days
            
            if days_until <= 3:
                event['urgency'] = 'critical'
            elif days_until <= 7:
                event['urgency'] = 'high'
            elif days_until <= 14:
                event['urgency'] = 'medium'
            else:
                event['urgency'] = 'low'
        
        return deadlines
    
    def export_to_ical(self, event_ids: Optional[List[str]] = None) -> str:
        """
        Export events to iCalendar format.
        
        Args:
            event_ids: Optional list of specific event IDs to export
        
        Returns:
            iCal formatted string
        """
        if event_ids:
            events_to_export = [e for e in self.events if e['id'] in event_ids]
        else:
            events_to_export = self.events
        
        ical = []
        ical.append("BEGIN:VCALENDAR")
        ical.append("VERSION:2.0")
        ical.append("PRODID:-//Semptify//Calendar Timeline//EN")
        ical.append("CALSCALE:GREGORIAN")
        ical.append("METHOD:PUBLISH")
        ical.append("X-WR-CALNAME:Semptify Timeline")
        ical.append("X-WR-TIMEZONE:America/New_York")
        
        for event in events_to_export:
            ical.append("BEGIN:VEVENT")
            ical.append(f"UID:{event['id']}@semptify.com")
            
            # Format datetime
            event_dt = datetime.fromisoformat(event['date'])
            ical.append(f"DTSTART:{event_dt.strftime('%Y%m%dT%H%M%S')}")
            ical.append(f"DTEND:{(event_dt + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')}")
            
            ical.append(f"SUMMARY:{event['title']}")
            if event.get('description'):
                ical.append(f"DESCRIPTION:{event['description']}")
            
            # Add category
            event_config = self.event_types.get(event['type'], {})
            ical.append(f"CATEGORIES:{event_config.get('category', 'general')}")
            
            ical.append(f"STATUS:{event['status'].upper()}")
            ical.append("END:VEVENT")
        
        ical.append("END:VCALENDAR")
        return "\n".join(ical)
    
    def get_statistics(self, user_id: Optional[str] = None) -> Dict:
        """Get timeline statistics"""
        events = self.events if not user_id else [e for e in self.events if e.get('user_id') == user_id]
        
        return {
            'total_events': len(events),
            'by_type': {
                event_type: len([e for e in events if e['type'] == event_type])
                for event_type in self.event_types.keys()
            },
            'by_status': {
                'upcoming': len([e for e in events if e['status'] == 'upcoming']),
                'completed': len([e for e in events if e['status'] == 'completed']),
                'missed': len([e for e in events if e['status'] == 'missed']),
                'cancelled': len([e for e in events if e['status'] == 'cancelled'])
            },
            'total_rent_paid': sum(e.get('amount', 0) for e in events if e['type'] == 'rent_payment' and e['status'] == 'completed'),
            'upcoming_deadlines': len(self.get_upcoming_deadlines(30, user_id))
        }


# Global instance
_timeline_engine = None

def get_timeline_engine() -> CalendarTimelineEngine:
    """Get or create timeline engine instance"""
    global _timeline_engine
    if _timeline_engine is None:
        _timeline_engine = CalendarTimelineEngine()
    return _timeline_engine


if __name__ == '__main__':
    # Test the timeline engine
    engine = get_timeline_engine()
    
    # Add sample events
    print("Adding sample timeline events...")
    
    engine.add_event(
        'rent_payment',
        '2025-12-01',
        'December Rent Payment',
        description='Monthly rent due',
        amount=1200.00,
        status='upcoming',
        user_id='test_user_001'
    )
    
    engine.add_event(
        'court_date',
        '2025-12-15 09:00:00',
        'Eviction Defense Hearing',
        description='Room 304, bring all evidence',
        status='upcoming',
        user_id='test_user_001',
        metadata={'case_number': 'CV-2025-12345', 'court': 'District Court'}
    )
    
    engine.add_event(
        'deadline',
        '2025-11-20',
        'Response to Notice Due',
        description='Must respond to 30-day notice',
        status='upcoming',
        user_id='test_user_001'
    )
    
    # Get all events
    all_events = engine.get_events()
    print(f"\n✅ Added {len(all_events)} events")
    
    # Get upcoming deadlines
    deadlines = engine.get_upcoming_deadlines(30)
    print(f"\n⏰ {len(deadlines)} upcoming deadlines:")
    for d in deadlines:
        print(f"  - {d['date']}: {d['title']} (urgency: {d['urgency']})")
    
    # Get rent ledger
    ledger = engine.get_rent_ledger('test_user_001')
    print(f"\n💵 Rent Ledger:")
    print(f"  Total Paid: ${ledger['total_paid']:.2f}")
    print(f"  Total Due: ${ledger['total_due']:.2f}")
    print(f"  Balance: ${ledger['balance']:.2f}")
    
    # Get statistics
    stats = engine.get_statistics('test_user_001')
    print(f"\n📊 Statistics:")
    print(f"  Total Events: {stats['total_events']}")
    print(f"  Upcoming Deadlines: {stats['upcoming_deadlines']}")
    
    # Export to iCal
    ical = engine.export_to_ical()
    print(f"\n📅 iCal Export: {len(ical.split('BEGIN:VEVENT'))-1} events exported")
    
    print("\n✅ Calendar Timeline Engine test complete!")
