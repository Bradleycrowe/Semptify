"""
Journey Automation - Track user progression through 5 stages
Newcomer → Documenting → Learning → Organizing → Ready
"""
import json
import os
from datetime import datetime

class JourneyAutomation:
    def __init__(self, data_path='data/journey'):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
        
        # 5-stage progression
        self.stages = {
            'newcomer': {
                'name': 'Newcomer',
                'description': 'Getting started with Semptify',
                'milestones': ['register', 'setup_storage', 'first_upload']
            },
            'documenting': {
                'name': 'Documenting',
                'description': 'Building your evidence vault',
                'milestones': ['upload_5_docs', 'add_timeline_event', 'create_notary_cert']
            },
            'learning': {
                'name': 'Learning',
                'description': 'Understanding your rights',
                'milestones': ['complete_module', 'read_3_laws', 'watch_video']
            },
            'organizing': {
                'name': 'Organizing',
                'description': 'Tracking everything systematically',
                'milestones': ['track_rent_payment', 'log_maintenance', 'calendar_event']
            },
            'ready': {
                'name': 'Ready',
                'description': 'Prepared to take action',
                'milestones': ['all_docs_organized', 'know_rights', 'action_plan']
            }
        }
    
    def get_user_file(self, user_token):
        return os.path.join(self.data_path, f'{user_token}_journey.json')
    
    def get_user_stage(self, user_token):
        """Get current stage for user"""
        filepath = self.get_user_file(user_token)
        if not os.path.exists(filepath):
            return 'newcomer'
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get('current_stage', 'newcomer')
        except:
            return 'newcomer'
    
    def get_stage_progress(self, user_token):
        """Get milestones completed for current stage"""
        filepath = self.get_user_file(user_token)
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get('completed_milestones', [])
        except:
            return []
    
    def check_and_advance(self, user_token, milestone):
        """Record milestone completion and check if stage should advance"""
        filepath = self.get_user_file(user_token)
        
        # Load existing data
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'current_stage': 'newcomer',
                'completed_milestones': [],
                'stage_history': []
            }
        
        # Add milestone if not already completed
        if milestone not in data['completed_milestones']:
            data['completed_milestones'].append(milestone)
        
        # Check if ready to advance stage
        current_stage = data['current_stage']
        required_milestones = self.stages[current_stage]['milestones']
        
        completed_for_stage = [m for m in required_milestones if m in data['completed_milestones']]
        
        if len(completed_for_stage) >= len(required_milestones):
            # Advance to next stage
            stage_order = ['newcomer', 'documenting', 'learning', 'organizing', 'ready']
            current_idx = stage_order.index(current_stage)
            
            if current_idx < len(stage_order) - 1:
                new_stage = stage_order[current_idx + 1]
                data['stage_history'].append({
                    'stage': current_stage,
                    'completed_at': datetime.now().isoformat()
                })
                data['current_stage'] = new_stage
        
        # Save
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def get_next_milestone(self, user_token):
        """Get next uncompleted milestone for current stage"""
        current_stage = self.get_user_stage(user_token)
        completed = self.get_stage_progress(user_token)
        required = self.stages[current_stage]['milestones']
        
        for milestone in required:
            if milestone not in completed:
                return milestone
        
        return None

# Global instance
_journey = None

def get_user_stage(user_token):
    global _journey
    if _journey is None:
        _journey = JourneyAutomation()
    return _journey.get_user_stage(user_token)

def get_stage_progress(user_token):
    global _journey
    if _journey is None:
        _journey = JourneyAutomation()
    return _journey.get_stage_progress(user_token)

def check_and_advance(user_token, milestone):
    global _journey
    if _journey is None:
        _journey = JourneyAutomation()
    return _journey.check_and_advance(user_token, milestone)

def get_next_milestone(user_token):
    global _journey
    if _journey is None:
        _journey = JourneyAutomation()
    return _journey.get_next_milestone(user_token)
