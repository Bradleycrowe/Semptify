# timeline_intelligence.py
# Auto-detect deadlines, calculate days remaining, suggest next steps

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class TimelineIntelligence:
    """
    Intelligent deadline detection and timeline management.
    Auto-detects critical dates from documents and calculates urgency.
    """
    
    DEADLINE_KEYWORDS = [
        'due date', 'deadline', 'must respond by', 'answer due',
        'court date', 'hearing date', 'trial date', 'appearance date',
        'eviction date', 'move-out date', 'vacate by',
        'notice period', 'days to respond', 'file by'
    ]
    
    def __init__(self):
        self.today = datetime.now().date()
    
    def detect_deadlines_from_intelligence(self, intelligence_data: Dict) -> List[Dict]:
        """
        Extract deadlines from document intelligence data.
        Returns list of {date, type, urgency, days_remaining, description}
        """
        deadlines = []
        
        if not intelligence_data or 'key_dates' not in intelligence_data:
            return deadlines
        
        for date_obj in intelligence_data.get('key_dates', []):
            deadline = self._parse_deadline(date_obj)
            if deadline:
                deadlines.append(deadline)
        
        # Sort by urgency (soonest first)
        deadlines.sort(key=lambda x: x['days_remaining'])
        
        return deadlines
    
    def _parse_deadline(self, date_obj: Dict) -> Optional[Dict]:
        """Parse a date object into a deadline with urgency calculation"""
        try:
            date_str = date_obj.get('date')
            label = date_obj.get('label', '').lower()
            
            if not date_str:
                return None
            
            # Parse date string (handle various formats)
            deadline_date = self._parse_date_string(date_str)
            if not deadline_date:
                return None
            
            # Calculate days remaining
            days_remaining = (deadline_date - self.today).days
            
            # Determine urgency level
            if days_remaining < 0:
                urgency = 'OVERDUE'
                urgency_score = 100
            elif days_remaining <= 3:
                urgency = 'CRITICAL'
                urgency_score = 90
            elif days_remaining <= 7:
                urgency = 'URGENT'
                urgency_score = 70
            elif days_remaining <= 14:
                urgency = 'IMPORTANT'
                urgency_score = 50
            elif days_remaining <= 30:
                urgency = 'UPCOMING'
                urgency_score = 30
            else:
                urgency = 'FUTURE'
                urgency_score = 10
            
            # Determine deadline type
            deadline_type = self._classify_deadline(label)
            
            return {
                'date': deadline_date.isoformat(),
                'date_formatted': deadline_date.strftime('%B %d, %Y'),
                'type': deadline_type,
                'label': date_obj.get('label'),
                'urgency': urgency,
                'urgency_score': urgency_score,
                'days_remaining': days_remaining,
                'description': self._generate_deadline_description(deadline_type, days_remaining),
                'action_required': self._suggest_action(deadline_type, days_remaining)
            }
        
        except Exception as e:
            print(f"[WARN] Failed to parse deadline: {e}")
            return None
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime.date]:
        """Parse various date formats into datetime.date"""
        formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        return None
    
    def _classify_deadline(self, label: str) -> str:
        """Classify deadline type from label"""
        label_lower = label.lower()
        
        if any(word in label_lower for word in ['court', 'hearing', 'trial', 'appearance']):
            return 'COURT_DATE'
        elif any(word in label_lower for word in ['respond', 'answer', 'reply']):
            return 'RESPONSE_DUE'
        elif any(word in label_lower for word in ['eviction', 'vacate', 'move-out']):
            return 'EVICTION_DATE'
        elif any(word in label_lower for word in ['file', 'submit']):
            return 'FILING_DUE'
        elif any(word in label_lower for word in ['rent', 'payment']):
            return 'PAYMENT_DUE'
        else:
            return 'GENERAL_DEADLINE'
    
    def _generate_deadline_description(self, deadline_type: str, days_remaining: int) -> str:
        """Generate human-readable description"""
        if days_remaining < 0:
            return f"⚠️ OVERDUE by {abs(days_remaining)} days!"
        elif days_remaining == 0:
            return "🚨 DUE TODAY!"
        elif days_remaining == 1:
            return "⏰ Due TOMORROW"
        else:
            return f"📅 {days_remaining} days remaining"
    
    def _suggest_action(self, deadline_type: str, days_remaining: int) -> str:
        """Suggest next action based on deadline type and urgency"""
        if days_remaining < 0:
            return "Contact court immediately about late filing options"
        
        actions = {
            'COURT_DATE': "Prepare documents, confirm appearance time, arrange transportation",
            'RESPONSE_DUE': "Complete and file your response form immediately",
            'EVICTION_DATE': "File emergency stay motion if you haven't already",
            'FILING_DUE': "Gather all documents and file as soon as possible",
            'PAYMENT_DUE': "Make payment or file motion to set payment plan",
            'GENERAL_DEADLINE': "Review requirements and complete necessary actions"
        }
        
        return actions.get(deadline_type, "Take appropriate action before deadline")
    
    def get_user_deadlines(self, user_id: str) -> Dict:
        """
        Get all deadlines for a user from their documents and timeline.
        Returns comprehensive deadline analysis.
        """
        deadlines = []
        
        # Load vault documents with intelligence
        vault_dir = f"uploads/vault/{user_id}"
        if os.path.exists(vault_dir):
            intel_path = os.path.join(vault_dir, "intelligence.json")
            if os.path.exists(intel_path):
                try:
                    with open(intel_path, 'r') as f:
                        intelligence = json.load(f)
                        deadlines.extend(self.detect_deadlines_from_intelligence(intelligence))
                except Exception as e:
                    print(f"[WARN] Failed to load intelligence for deadlines: {e}")
        
        # Load timeline events that might have deadlines
        from user_database import get_user_db
        try:
            conn = get_user_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT event_type, title, description, event_date
                FROM timeline_events
                WHERE user_id = ? AND event_date >= date('now')
                ORDER BY event_date ASC
            ''', (user_id,))
            
            for row in cursor.fetchall():
                event_date = datetime.fromisoformat(row[3]).date()
                days_remaining = (event_date - self.today).days
                
                deadlines.append({
                    'date': row[3],
                    'date_formatted': event_date.strftime('%B %d, %Y'),
                    'type': row[0],
                    'label': row[1],
                    'urgency': 'UPCOMING' if days_remaining > 7 else 'URGENT',
                    'days_remaining': days_remaining,
                    'description': f"{days_remaining} days remaining",
                    'action_required': row[2] or "Review event details"
                })
            
            conn.close()
        except Exception as e:
            print(f"[WARN] Failed to load timeline deadlines: {e}")
        
        # Sort by urgency
        deadlines.sort(key=lambda x: x.get('days_remaining', 999))
        
        # Calculate summary statistics
        critical = [d for d in deadlines if d['days_remaining'] <= 3]
        urgent = [d for d in deadlines if 3 < d['days_remaining'] <= 7]
        upcoming = [d for d in deadlines if d['days_remaining'] > 7]
        
        return {
            'deadlines': deadlines,
            'total_count': len(deadlines),
            'critical_count': len(critical),
            'urgent_count': len(urgent),
            'upcoming_count': len(upcoming),
            'next_deadline': deadlines[0] if deadlines else None,
            'requires_immediate_action': len(critical) > 0
        }

