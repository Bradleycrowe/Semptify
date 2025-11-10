"""
Dashboard Engine - Determines which widgets to show in each cell (A-F)
based on user progress, situation, and learning module analysis.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Widget registry - all available widgets
AVAILABLE_WIDGETS = {
    "welcome": {
        "name": "Welcome to Semptify",
        "description": "Introduction to what Semptify does",
        "type": "info"
    },
    "know_rights": {
        "name": "Know Your Rights",
        "description": "Tenant rights based on user location",
        "type": "info"
    },
    "document_evidence": {
        "name": "Document Everything",
        "description": "Upload photos, videos, texts",
        "type": "action"
    },
    "track_deadlines": {
        "name": "Track Deadlines",
        "description": "Court dates and filing deadlines",
        "type": "action"
    },
    "rent_ledger": {
        "name": "Rent Payment Tracker",
        "description": "Proof of rent payments",
        "type": "action"
    },
    "situation_questions": {
        "name": "Tell Us Your Situation",
        "description": "Answer questions to help us guide you",
        "type": "input"
    },
    "next_steps": {
        "name": "Your Next Steps",
        "description": "Recommended actions based on your situation",
        "type": "action"
    },
    "legal_forms": {
        "name": "File Legal Forms",
        "description": "Court documents and complaints",
        "type": "action"
    }
}

# Default dashboard layout for new users
DEFAULT_LAYOUT = {
    "a": "welcome",
    "b": "know_rights",
    "c": "situation_questions",
    "d": "document_evidence",
    "e": "track_deadlines",
    "f": "rent_ledger"
}

class DashboardEngine:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.layouts_file = os.path.join(data_dir, "dashboard_layouts.json")
        self.user_progress_file = os.path.join(data_dir, "user_progress.json")
        os.makedirs(data_dir, exist_ok=True)
        
    def get_user_layout(self, user_id: str) -> Dict[str, str]:
        """Get dashboard layout for a specific user."""
        # Check for custom layout
        layouts = self._load_layouts()
        if user_id in layouts:
            return layouts[user_id]
        
        # Check user progress to determine dynamic layout
        progress = self._get_user_progress(user_id)
        if progress:
            return self._generate_dynamic_layout(progress)
        
        # Default layout for new users
        return DEFAULT_LAYOUT.copy()
    
    def get_cell_content(self, user_id: str, cell: str) -> Dict:
        """Get widget content for a specific cell."""
        layout = self.get_user_layout(user_id)
        widget_id = layout.get(cell)
        
        if not widget_id or widget_id not in AVAILABLE_WIDGETS:
            return {"error": "Widget not found"}
        
        widget = AVAILABLE_WIDGETS[widget_id].copy()
        widget["id"] = widget_id
        widget["cell"] = cell
        
        # Add dynamic content based on widget type
        if widget_id == "situation_questions":
            widget["questions"] = self._get_situation_questions(user_id)
        elif widget_id == "next_steps":
            widget["steps"] = self._get_next_steps(user_id)
        elif widget_id == "know_rights":
            widget["rights"] = self._get_user_rights(user_id)
        
        return widget
    
    def set_user_layout(self, user_id: str, layout: Dict[str, str], admin: bool = False):
        """Set custom layout for a user (admin override or learning-based)."""
        layouts = self._load_layouts()
        layouts[user_id] = {
            **layout,
            "updated_at": datetime.now().isoformat(),
            "updated_by": "admin" if admin else "learning_module"
        }
        self._save_layouts(layouts)
    
    def update_user_progress(self, user_id: str, progress_data: Dict):
        """Update user progress (triggers layout recalculation)."""
        progress = self._load_progress()
        if user_id not in progress:
            progress[user_id] = {}
        
        progress[user_id].update(progress_data)
        progress[user_id]["updated_at"] = datetime.now().isoformat()
        
        self._save_progress(progress)
        
        # Recalculate layout based on new progress
        new_layout = self._generate_dynamic_layout(progress[user_id])
        self.set_user_layout(user_id, new_layout, admin=False)
    
    def _generate_dynamic_layout(self, progress: Dict) -> Dict[str, str]:
        """Generate layout based on user progress and situation."""
        layout = DEFAULT_LAYOUT.copy()
        
        # Example logic - adjust based on progress
        if progress.get("completed_intro"):
            layout["a"] = "next_steps"
        
        if progress.get("has_court_date"):
            layout["b"] = "track_deadlines"
            layout["c"] = "legal_forms"
        
        if progress.get("situation_analyzed"):
            layout["c"] = "next_steps"
        else:
            layout["c"] = "situation_questions"
        
        if progress.get("evidence_uploaded", 0) > 0:
            # User already uploading evidence, show rent tracker
            layout["d"] = "rent_ledger"
        
        return layout
    
    def _get_situation_questions(self, user_id: str) -> List[Dict]:
        """Get questions from learning module for user."""
        # TODO: Integrate with learning modules
        return [
            {"id": 1, "text": "Are you facing eviction?", "type": "yes_no"},
            {"id": 2, "text": "Do you have a court date?", "type": "yes_no"},
            {"id": 3, "text": "Have you received any notices?", "type": "yes_no"}
        ]
    
    def _get_next_steps(self, user_id: str) -> List[Dict]:
        """Get recommended next steps for user."""
        # TODO: Integrate with learning modules
        return [
            {"step": 1, "action": "Document all communications with landlord", "urgent": True},
            {"step": 2, "action": "Take photos of property conditions", "urgent": True},
            {"step": 3, "action": "Review your lease agreement", "urgent": False}
        ]
    
    def _get_user_rights(self, user_id: str) -> List[str]:
        """Get tenant rights based on user location."""
        # TODO: Integrate with location-based rights database
        return [
            "Right to habitable living conditions",
            "Right to privacy and quiet enjoyment",
            "Right to proper notice before eviction"
        ]
    
    def _get_user_progress(self, user_id: str) -> Optional[Dict]:
        """Load user progress data."""
        progress = self._load_progress()
        return progress.get(user_id)
    
    def _load_layouts(self) -> Dict:
        """Load saved layouts."""
        if os.path.exists(self.layouts_file):
            with open(self.layouts_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_layouts(self, layouts: Dict):
        """Save layouts to disk."""
        with open(self.layouts_file, 'w') as f:
            json.dump(layouts, f, indent=2)
    
    def _load_progress(self) -> Dict:
        """Load user progress."""
        if os.path.exists(self.user_progress_file):
            with open(self.user_progress_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_progress(self, progress: Dict):
        """Save user progress."""
        with open(self.user_progress_file, 'w') as f:
            json.dump(progress, f, indent=2)


# Singleton instance
_dashboard_engine = None

def get_dashboard_engine() -> DashboardEngine:
    """Get or create dashboard engine instance."""
    global _dashboard_engine
    if _dashboard_engine is None:
        _dashboard_engine = DashboardEngine()
    return _dashboard_engine
