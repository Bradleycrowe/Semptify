"""
Learning Engine Core - Knowledge Accumulation System for Semptify
Observes all interactions, extracts patterns, builds adaptive intelligence
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum

class InteractionType(Enum):
    DOCUMENT_GENERATION = "document_generation"
    FORM_SUBMISSION = "form_submission"
    ROUTE_ACCESS = "route_access"
    SEARCH_QUERY = "search_query"
    DEFENSE_SELECTED = "defense_selected"
    MOTION_FILED = "motion_filed"
    COUNTERCLAIM_FILED = "counterclaim_filed"
    OUTCOME_RECORDED = "outcome_recorded"
    DOCUMENT_UPLOAD = "document_upload"

class LearningEngine:
    """Central learning system that observes and learns from all user interactions"""
    
    def __init__(self, knowledge_dir: str = "learning_engine/knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Knowledge databases
        self.interaction_log = self.knowledge_dir / "interactions.jsonl"
        self.patterns_db = self.knowledge_dir / "patterns.json"
        self.outcomes_db = self.knowledge_dir / "outcomes.json"
        self.documents_db = self.knowledge_dir / "documents.json"
        self.user_profiles_db = self.knowledge_dir / "user_profiles.json"
        
        # Initialize knowledge structures
        self._init_knowledge_bases()
    
    def _init_knowledge_bases(self):
        """Initialize or load existing knowledge bases"""
        if not self.patterns_db.exists():
            self._save_json(self.patterns_db, {
                "defense_effectiveness": {},  # Track which defenses work
                "motion_success_rates": {},   # Track motion outcomes
                "judge_patterns": {},          # Track judge tendencies
                "landlord_tactics": {},        # Learn landlord strategies
                "document_preferences": {},    # User document choices
                "timing_patterns": {},         # When users need help
                "common_errors": [],           # Mistakes to prevent
                "success_strategies": []       # What works
            })
        
        if not self.outcomes_db.exists():
            self._save_json(self.outcomes_db, {
                "cases": [],
                "statistics": {
                    "total_cases": 0,
                    "dismissals": 0,
                    "settlements": 0,
                    "tenant_wins": 0,
                    "continuances_granted": 0
                }
            })
        
        if not self.documents_db.exists():
            self._save_json(self.documents_db, {
                "generated_count": 0,
                "popular_templates": {},
                "customization_patterns": []
            })
    
    def observe_interaction(self, 
                          interaction_type: InteractionType,
                          data: Dict[str, Any],
                          user_id: Optional[str] = None,
                          metadata: Optional[Dict] = None) -> str:
        """
        Observe and log an interaction for learning
        
        Args:
            interaction_type: Type of interaction
            data: Interaction data
            user_id: Optional user identifier
            metadata: Additional context
            
        Returns:
            interaction_id for tracking
        """
        interaction_id = f"{datetime.utcnow().isoformat()}_{interaction_type.value}"
        
        interaction_record = {
            "id": interaction_id,
            "timestamp": datetime.utcnow().isoformat(),
            "type": interaction_type.value,
            "user_id": user_id,
            "data": data,
            "metadata": metadata or {}
        }
        
        # Append to interaction log (JSONL format for streaming)
        with open(self.interaction_log, 'a') as f:
            f.write(json.dumps(interaction_record) + '\n')
        
        # Trigger pattern extraction
        self._extract_patterns(interaction_record)
        
        return interaction_id
    
    def _extract_patterns(self, interaction: Dict):
        """Extract learning patterns from interaction"""
        patterns = self._load_json(self.patterns_db)
        
        interaction_type = interaction['type']
        data = interaction['data']
        
        # Learn from document generation
        if interaction_type == InteractionType.DOCUMENT_GENERATION.value:
            doc_type = data.get('document_type')
            if doc_type:
                patterns['document_preferences'][doc_type] = \
                    patterns['document_preferences'].get(doc_type, 0) + 1
        
        # Learn from defense selections
        elif interaction_type == InteractionType.DEFENSE_SELECTED.value:
            defense = data.get('defense_name')
            context = data.get('context', {})
            
            if defense not in patterns['defense_effectiveness']:
                patterns['defense_effectiveness'][defense] = {
                    "selected_count": 0,
                    "contexts": []
                }
            
            patterns['defense_effectiveness'][defense]['selected_count'] += 1
            patterns['defense_effectiveness'][defense]['contexts'].append(context)
        
        # Learn from motion filings
        elif interaction_type == InteractionType.MOTION_FILED.value:
            motion_type = data.get('motion_type')
            if motion_type not in patterns['motion_success_rates']:
                patterns['motion_success_rates'][motion_type] = {
                    "filed_count": 0,
                    "outcomes": []
                }
            patterns['motion_success_rates'][motion_type]['filed_count'] += 1
        
        # Learn from outcomes
        elif interaction_type == InteractionType.OUTCOME_RECORDED.value:
            outcome = data.get('outcome')
            motion_type = data.get('motion_type')
            
            if motion_type and outcome:
                if motion_type in patterns['motion_success_rates']:
                    patterns['motion_success_rates'][motion_type]['outcomes'].append({
                        "outcome": outcome,
                        "timestamp": interaction['timestamp'],
                        "context": data.get('context', {})
                    })
        
        # Save updated patterns
        self._save_json(self.patterns_db, patterns)
    
    def get_recommendations(self, context: Dict[str, Any]) -> List[Dict]:
        """
        Get adaptive recommendations based on learned patterns
        
        Args:
            context: Current situation context
            
        Returns:
            List of recommendations ranked by learned effectiveness
        """
        patterns = self._load_json(self.patterns_db)
        recommendations = []
        
        # Recommend defenses based on success patterns
        if context.get('situation') == 'eviction':
            defense_effectiveness = patterns.get('defense_effectiveness', {})
            
            for defense, stats in defense_effectiveness.items():
                # Calculate effectiveness score
                selected_count = stats.get('selected_count', 0)
                
                if selected_count > 0:
                    recommendations.append({
                        "type": "defense",
                        "name": defense,
                        "score": selected_count,
                        "reason": f"Selected {selected_count} times by others"
                    })
        
        # Recommend motions based on success rates
        if context.get('need_motion'):
            motion_success = patterns.get('motion_success_rates', {})
            
            for motion, stats in motion_success.items():
                outcomes = stats.get('outcomes', [])
                successful = sum(1 for o in outcomes if o.get('outcome') == 'granted')
                total = len(outcomes)
                
                if total > 0:
                    success_rate = successful / total
                    recommendations.append({
                        "type": "motion",
                        "name": motion,
                        "score": success_rate,
                        "reason": f"Success rate: {success_rate:.1%} ({successful}/{total})"
                    })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def record_outcome(self, case_data: Dict[str, Any]):
        """Record case outcome for learning"""
        outcomes = self._load_json(self.outcomes_db)
        
        outcomes['cases'].append({
            "timestamp": datetime.utcnow().isoformat(),
            **case_data
        })
        
        # Update statistics
        stats = outcomes['statistics']
        stats['total_cases'] += 1
        
        outcome_type = case_data.get('outcome')
        if outcome_type in ['dismissed', 'dismissal']:
            stats['dismissals'] += 1
        elif outcome_type == 'settlement':
            stats['settlements'] += 1
        elif outcome_type in ['tenant_win', 'tenant_victory']:
            stats['tenant_wins'] += 1
        elif outcome_type in ['continuance', 'continued']:
            stats['continuances_granted'] += 1
        
        self._save_json(self.outcomes_db, outcomes)
        
        # Also log as interaction for pattern extraction
        self.observe_interaction(
            InteractionType.OUTCOME_RECORDED,
            case_data
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current learning statistics"""
        outcomes = self._load_json(self.outcomes_db)
        patterns = self._load_json(self.patterns_db)
        documents = self._load_json(self.documents_db)
        
        # Count interactions
        interaction_count = 0
        if self.interaction_log.exists():
            with open(self.interaction_log, 'r') as f:
                interaction_count = sum(1 for _ in f)
        
        return {
            "total_interactions": interaction_count,
            "total_cases": outcomes['statistics']['total_cases'],
            "documents_generated": documents.get('generated_count', 0),
            "patterns_learned": len(patterns.get('defense_effectiveness', {})),
            "success_rate": self._calculate_success_rate(outcomes),
            "most_effective_defense": self._get_top_defense(patterns),
            "most_successful_motion": self._get_top_motion(patterns)
        }
    
    def _calculate_success_rate(self, outcomes: Dict) -> float:
        """Calculate overall success rate"""
        stats = outcomes['statistics']
        total = stats['total_cases']
        if total == 0:
            return 0.0
        
        successes = stats['dismissals'] + stats['tenant_wins']
        return successes / total
    
    def _get_top_defense(self, patterns: Dict) -> Optional[str]:
        """Get most effective defense"""
        defenses = patterns.get('defense_effectiveness', {})
        if not defenses:
            return None
        
        return max(defenses.items(), 
                  key=lambda x: x[1].get('selected_count', 0))[0]
    
    def _get_top_motion(self, patterns: Dict) -> Optional[Dict]:
        """Get most successful motion"""
        motions = patterns.get('motion_success_rates', {})
        best_motion = None
        best_rate = 0.0
        
        for motion, stats in motions.items():
            outcomes = stats.get('outcomes', [])
            if not outcomes:
                continue
            
            successful = sum(1 for o in outcomes if o.get('outcome') == 'granted')
            rate = successful / len(outcomes)
            
            if rate > best_rate:
                best_rate = rate
                best_motion = motion
        
        if best_motion:
            return {
                "name": best_motion,
                "success_rate": best_rate
            }
        return None
    
    def _load_json(self, path: Path) -> Dict:
        """Load JSON file"""
        if not path.exists():
            return {}
        with open(path, 'r') as f:
            return json.load(f)
    
    def _save_json(self, path: Path, data: Dict):
        """Save JSON file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

# Global learning engine instance
_learning_engine: Optional[LearningEngine] = None

def get_learning_engine() -> LearningEngine:
    """Get or create global learning engine instance"""
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = LearningEngine()
    return _learning_engine
