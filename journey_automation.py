"""
Phase 5: Journey Automation
Auto-advances user progress based on completed actions
"""
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class JourneyAutomation:
    """Automatically advance user journey based on completed milestones"""
    
    def __init__(self, data_path=''data/journey''):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
        
        # Define journey stages and requirements
        self.journey_stages = {
            ''newcomer'': {
                ''title'': ''Getting Started'',
                ''requirements'': [],
                ''next'': ''documenting''
            },
            ''documenting'': {
                ''title'': ''Building Your Evidence'',
                ''requirements'': [
                    {''type'': ''vault_upload'', ''count'': 1},
                    {''type'': ''calendar_event'', ''count'': 1}
                ],
                ''next'': ''learning''
            },
            ''learning'': {
                ''title'': ''Understanding Your Rights'',
                ''requirements'': [
                    {''type'': ''vault_upload'', ''count'': 3},
                    {''type'': ''learning_module'', ''count'': 1}
                ],
                ''next'': ''organizing''
            },
            ''organizing'': {
                ''title'': ''Organizing Your Case'',
                ''requirements'': [
                    {''type'': ''calendar_event'', ''count'': 5},
                    {''type'': ''vault_upload'', ''count'': 5},
                    {''type'': ''learning_module'', ''count'': 2}
                ],
                ''next'': ''ready''
            },
            ''ready'': {
                ''title'': ''Case Ready'',
                ''requirements'': [
                    {''type'': ''vault_upload'', ''count'': 10},
                    {''type'': ''calendar_event'', ''count'': 10},
                    {''type'': ''learning_module'', ''count'': 3}
                ],
                ''next'': None
            }
        }
    
    def check_and_advance(self, user_id: str, action_type: str) -> Optional[Dict]:
        """
        Check if action completes a milestone and advances journey
        
        Args:
            user_id: User identifier
            action_type: Type of action (vault_upload, calendar_event, learning_module)
            
        Returns:
            Dict with advancement info if stage advanced, None otherwise
        """
        # Load user progress
        progress = self._load_progress(user_id)
        
        # Increment action count
        if action_type not in progress[''actions'']:
            progress[''actions''][action_type] = 0
        progress[''actions''][action_type] += 1
        
        # Check if current stage is complete
        current_stage = progress[''current_stage'']
        stage_info = self.journey_stages[current_stage]
        
        if self._stage_complete(progress[''actions''], stage_info[''requirements'']):
            # Advance to next stage
            next_stage = stage_info[''next'']
            if next_stage:
                progress[''current_stage''] = next_stage
                progress[''stage_history''].append({
                    ''stage'': next_stage,
                    ''timestamp'': datetime.utcnow().isoformat(),
                    ''trigger_action'': action_type
                })
                
                self._save_progress(user_id, progress)
                
                return {
                    ''advanced'': True,
                    ''new_stage'': next_stage,
                    ''title'': self.journey_stages[next_stage][''title''],
                    ''message'': f"🎉 You''ve advanced to: {self.journey_stages[next_stage][''title'']}!"
                }
        
        # Save progress even if not advancing
        self._save_progress(user_id, progress)
        
        # Return progress update
        return {
            ''advanced'': False,
            ''current_stage'': current_stage,
            ''progress'': self._calculate_stage_progress(progress[''actions''], stage_info[''requirements''])
        }
    
    def get_next_milestone(self, user_id: str) -> Dict:
        """Get what user needs to do next"""
        progress = self._load_progress(user_id)
        current_stage = progress[''current_stage'']
        stage_info = self.journey_stages[current_stage]
        
        milestones = []
        for req in stage_info[''requirements'']:
            current = progress[''actions''].get(req[''type''], 0)
            needed = req[''count'']
            milestones.append({
                ''action'': req[''type''],
                ''current'': current,
                ''needed'': needed,
                ''complete'': current >= needed
            })
        
        return {
            ''stage'': current_stage,
            ''title'': stage_info[''title''],
            ''milestones'': milestones,
            ''progress_percent'': self._calculate_stage_progress(progress[''actions''], stage_info[''requirements''])
        }
    
    def _stage_complete(self, actions: Dict, requirements: List[Dict]) -> bool:
        """Check if all requirements met"""
        for req in requirements:
            if actions.get(req[''type''], 0) < req[''count'']:
                return False
        return True
    
    def _calculate_stage_progress(self, actions: Dict, requirements: List[Dict]) -> int:
        """Calculate percentage complete for current stage"""
        if not requirements:
            return 100
        
        total_needed = sum(r[''count''] for r in requirements)
        total_complete = sum(min(actions.get(r[''type''], 0), r[''count'']) for r in requirements)
        
        return int((total_complete / total_needed) * 100)
    
    def _load_progress(self, user_id: str) -> Dict:
        """Load user journey progress"""
        progress_file = os.path.join(self.data_path, f''{user_id}_progress.json'')
        
        if os.path.exists(progress_file):
            with open(progress_file, ''r'') as f:
                return json.load(f)
        
        # Initialize new user
        return {
            ''user_id'': user_id,
            ''current_stage'': ''newcomer'',
            ''actions'': {},
            ''stage_history'': [{
                ''stage'': ''newcomer'',
                ''timestamp'': datetime.utcnow().isoformat()
            }]
        }
    
    def _save_progress(self, user_id: str, progress: Dict):
        """Save user journey progress"""
        progress_file = os.path.join(self.data_path, f''{user_id}_progress.json'')
        with open(progress_file, ''w'') as f:
            json.dump(progress, f, indent=2)
