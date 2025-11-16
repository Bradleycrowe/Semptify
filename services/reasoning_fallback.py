"""
Reasoning Fallback Service - Universal AI-powered problem solver
Automatically invokes reasoning engine when standard fixes fail.
"""
from typing import Dict, Any, Optional, List
import traceback


class ReasoningFallback:
    """Universal fallback using reasoning engine for failed operations."""
    
    def __init__(self):
        self._reasoner = None
    
    def _get_reasoner(self):
        """Lazy load reasoning system."""
        if self._reasoner is None:
            try:
                from reasoning_system import ReasoningSystem
                self._reasoner = ReasoningSystem()
            except ImportError as e:
                print(f"[REASONING-FALLBACK] Warning: Could not load reasoning system: {e}")
        return self._reasoner
    
    def solve(self, problem_type: str, facts: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """
        Universal problem solver using reasoning engine.
        
        Args:
            problem_type: Type of problem (route_broken, import_failed, test_failed, etc.)
            facts: All known facts about the problem
            context: Human-readable context for logging
        
        Returns:
            Dict with 'suggestions', 'confidence', 'reasoning', 'applied_fix'
        """
        reasoner = self._get_reasoner()
        if not reasoner:
            return {
                'status': 'unavailable',
                'suggestions': [],
                'confidence': 0,
                'message': 'Reasoning engine not available'
            }
        
        try:
            # Add problem type to facts for reasoning
            facts['problem_type'] = problem_type
            facts['stage'] = f'fallback_{problem_type}'
            
            # Invoke reasoning
            result = reasoner.analyze(facts, stage=facts['stage'])
            
            # Extract actionable suggestions
            suggestions = self._extract_suggestions(result, problem_type)
            confidence = result.get('action', {}).get('confidence', 0.5)
            
            print(f"[REASONING-FALLBACK] {context or problem_type}")
            print(f"[REASONING-FALLBACK]   Confidence: {confidence:.0%}")
            print(f"[REASONING-FALLBACK]   Suggestions: {len(suggestions)}")
            
            return {
                'status': 'success',
                'suggestions': suggestions,
                'confidence': confidence,
                'reasoning': result.get('action', {}).get('recommendation', ''),
                'raw_result': result
            }
            
        except Exception as e:
            print(f"[REASONING-FALLBACK] Error: {e}")
            print(f"[REASONING-FALLBACK] Traceback: {traceback.format_exc()}")
            return {
                'status': 'error',
                'suggestions': [],
                'confidence': 0,
                'error': str(e)
            }
    
    def _extract_suggestions(self, reasoning: Dict, problem_type: str) -> List[Dict[str, Any]]:
        """Extract actionable suggestions from reasoning result."""
        suggestions = []
        
        # Check options
        options = reasoning.get('options', {})
        if isinstance(options, dict):
            # Route repair suggestions
            if 'possible_routes' in options:
                for route in options['possible_routes']:
                    suggestions.append({
                        'type': 'route_fix',
                        'value': route,
                        'action': 'update_route'
                    })
        
        # Check action recommendations
        action = reasoning.get('action', {})
        if action.get('recommendation'):
            suggestions.append({
                'type': 'recommendation',
                'value': action['recommendation'],
                'action': 'manual_review'
            })
        
        return suggestions
    
    def auto_apply(self, problem_type: str, facts: Dict[str, Any], 
                    apply_fn: callable, context: str = "") -> Dict[str, Any]:
        """
        Solve problem and automatically apply best suggestion.
        
        Args:
            problem_type: Type of problem
            facts: Problem facts
            apply_fn: Function to apply suggestion, takes (suggestion) returns success bool
            context: Human-readable context
        
        Returns:
            Dict with 'applied', 'suggestion', 'confidence'
        """
        result = self.solve(problem_type, facts, context)
        
        if result['status'] != 'success':
            return {'applied': False, 'reason': result.get('message', 'Failed')}
        
        # Try each suggestion in order of confidence
        for suggestion in result['suggestions']:
            try:
                if apply_fn(suggestion):
                    print(f"[REASONING-FALLBACK] ✓ Applied: {suggestion.get('value', suggestion)}")
                    return {
                        'applied': True,
                        'suggestion': suggestion,
                        'confidence': result['confidence']
                    }
            except Exception as e:
                print(f"[REASONING-FALLBACK] Failed to apply {suggestion}: {e}")
                continue
        
        return {
            'applied': False,
            'reason': 'No suggestions worked',
            'tried': len(result['suggestions'])
        }


# Global instance
_fallback = None

def get_reasoning_fallback() -> ReasoningFallback:
    """Get singleton reasoning fallback instance."""
    global _fallback
    if _fallback is None:
        _fallback = ReasoningFallback()
    return _fallback
