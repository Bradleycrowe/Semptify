"""
CORE ENGINE: Orchestrates reasoning + curiosity across all of Semptify.

This is the brain that ties everything together:
- Reasoning: Multi-step analysis, risk assessment, decision-making
- Curiosity: Learning patterns, adapting questions, growing capabilities

Every feature in Semptify flows through this core.
"""
from __future__ import annotations
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import existing engines
from reasoning_engine import ReasoningEngine
from curiosity_engine import CuriosityEngine
from realtime_research_engine import RealTimeResearchEngine
from housing_journey_engine import HousingJourneyEngine
from official_sources import classify_source, is_official_source


class SemptifyCore:
    """
    The central brain of Semptify.
    
    Philosophy:
    1. REASON through every problem (don't just pattern-match)
    2. Be CURIOUS (learn from every interaction)
    3. Use OFFICIAL SOURCES for facts
    4. Show your WORK (transparent reasoning)
    5. Never give LEGAL ADVICE (inform, don't advise)
    """
    
    def __init__(self):
        self.reasoning = ReasoningEngine()
        self.curiosity = CuriosityEngine()
        self.research = RealTimeResearchEngine()
        self.journey = HousingJourneyEngine()
        
        self.session_memory = {}  # tracks ongoing conversations
        self.global_learning = {}  # patterns learned across all users
        
    def process_user_input(self, 
                          user_id: str,
                          stage: str, 
                          user_input: str,
                          session_facts: Dict) -> Dict[str, Any]:
        """
        Core processing flow for every user interaction.
        
        Flow:
        1. CURIOSITY: What are we learning from this input?
        2. REASONING: What does this mean for their situation?
        3. RESEARCH: What official sources apply?
        4. DECISION: What should we do/ask next?
        5. LEARNING: Update our knowledge
        """
        
        # Step 1: Curiosity - Learn from input
        curiosity_analysis = self.curiosity.analyze_input(
            user_input=user_input,
            context={'stage': stage, 'facts': session_facts}
        )
        
        # Step 2: Reasoning - Understand situation
        reasoning_chain = self.reasoning.analyze_situation(
            facts=session_facts,
            stage=stage,
            new_input=user_input
        )
        
        # Step 3: Research - Get official sources
        research_results = self.research.research_holdover_rights(
            state='MN',
            city=session_facts.get('city')
        )
        
        # Step 4: Decision - Next action
        next_action = self._determine_next_action(
            reasoning=reasoning_chain,
            research=research_results,
            curiosity=curiosity_analysis
        )
        
        # Step 5: Learning - Update knowledge
        self._update_learning(
            user_id=user_id,
            curiosity=curiosity_analysis,
            reasoning=reasoning_chain,
            outcome=next_action
        )
        
        return {
            'reasoning': reasoning_chain,
            'research': research_results,
            'curiosity': curiosity_analysis,
            'next_action': next_action,
            'timestamp': datetime.now().isoformat(),
            'sources_used': self._extract_sources(research_results),
            'disclaimer': 'This is information, not legal advice. Consult an attorney for advice about your situation.'
        }
    
    def _determine_next_action(self, reasoning, research, curiosity) -> Dict:
        """Synthesize reasoning + research + curiosity into next action."""
        # Priority order:
        # 1. Urgent legal timeline (eviction notice, court date)
        # 2. Missing critical facts (need more questions)
        # 3. Available options (present choices)
        # 4. Curiosity-driven exploration (learn their goals)
        
        if reasoning.get('urgency') == 'critical':
            return {
                'type': 'urgent_action',
                'message': reasoning['urgent_message'],
                'deadline': reasoning.get('deadline')
            }
        
        if curiosity.get('missing_facts'):
            return {
                'type': 'ask_question',
                'question': curiosity['next_question'],
                'why': curiosity['learning_goal']
            }
        
        if research.get('citations'):
            return {
                'type': 'present_options',
                'options': reasoning.get('options', []),
                'legal_basis': research['citations'],
                'recommendation': reasoning.get('recommendation')
            }
        
        return {
            'type': 'explore',
            'question': curiosity.get('exploratory_question', 'Tell me more about your situation')
        }
    
    def _update_learning(self, user_id, curiosity, reasoning, outcome):
        """Update global and session learning."""
        # Session memory
        if user_id not in self.session_memory:
            self.session_memory[user_id] = []
        
        self.session_memory[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'curiosity_insights': curiosity,
            'reasoning_steps': reasoning,
            'action_taken': outcome
        })
        
        # Global learning (patterns across users)
        pattern_key = f"{curiosity.get('stage')}_{curiosity.get('intent')}"
        if pattern_key not in self.global_learning:
            self.global_learning[pattern_key] = {'count': 0, 'successful_paths': []}
        
        self.global_learning[pattern_key]['count'] += 1
        
    def _extract_sources(self, research) -> List[Dict]:
        """Extract and classify all sources used."""
        sources = []
        for cite in research.get('citations', []):
            sources.append({
                'url': cite['url'],
                'type': classify_source(cite['url']),
                'used_for': 'legal_fact' if cite.get('official') else 'context',
                'title': cite.get('title'),
                'checked': cite.get('checked_date')
            })
        return sources


# Singleton instance
_core_instance = None

def get_core() -> SemptifyCore:
    """Get or create the core engine instance."""
    global _core_instance
    if _core_instance is None:
        _core_instance = SemptifyCore()
    return _core_instance
