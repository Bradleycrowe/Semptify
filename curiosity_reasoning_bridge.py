"""
Curiosity-Reasoning Integration
Connects curiosity_engine (pattern detection) with reasoning_system (legal analysis)
"""
from typing import Dict, List, Any
from curiosity_engine import CuriosityEngine
from reasoning_system import ReasoningSystem
from datetime import datetime
import json

class CuriosityReasoningBridge:
    """
    Bridges curiosity (what questions to ask) with reasoning (how to answer).
    Curiosity detects patterns → Reasoning analyzes → Curiosity learns from outcomes.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.curiosity = CuriosityEngine(data_dir=data_dir)
        self.reasoner = ReasoningSystem()
        self.interaction_history = []
        
    def analyze_with_context(self, facts: Dict, stage: str, user_input: str = None) -> Dict:
        """
        Enhanced reasoning that learns from curiosity patterns.
        
        Flow:
        1. Curiosity analyzes user input for patterns (urgency, concerns, priorities)
        2. Reasoning analyzes situation with curiosity context
        3. Track outcome for curiosity learning
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'curiosity_insights': None,
            'reasoning': None,
            'learning_updates': []
        }
        
        # Step 1: Curiosity pattern detection
        if user_input:
            curiosity_context = self._detect_user_patterns(user_input, facts)
            result['curiosity_insights'] = curiosity_context
            
            # Enhance facts with curiosity insights
            enhanced_facts = {**facts}
            if curiosity_context.get('urgency_detected'):
                enhanced_facts['urgency_signals'] = curiosity_context['urgency_signals']
            if curiosity_context.get('concerns'):
                enhanced_facts['user_concerns'] = curiosity_context['concerns']
        else:
            enhanced_facts = facts
        
        # Step 2: Reasoning with enhanced context
        reasoning_result = self.reasoner.analyze(enhanced_facts, stage)
        result['reasoning'] = reasoning_result
        
        # Step 3: Track interaction for learning
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'facts': facts,
            'stage': stage,
            'reasoning_summary': reasoning_result['summary'],
            'curiosity_patterns': result.get('curiosity_insights', {})
        }
        self.interaction_history.append(interaction)
        
        # Step 4: Update curiosity knowledge based on reasoning
        learning = self._update_curiosity_from_reasoning(reasoning_result, facts, stage)
        result['learning_updates'] = learning
        
        return result
    
    def _detect_user_patterns(self, user_input: str, facts: Dict) -> Dict:
        """
        Use curiosity engine to detect patterns in user input.
        Returns context for reasoning enhancement.
        """
        patterns = {
            'urgency_detected': False,
            'urgency_signals': [],
            'concerns': [],
            'question_type': 'exploration',
            'emotional_state': 'neutral'
        }
        
        user_lower = user_input.lower()
        
        # Urgency detection
        urgency_keywords = ['urgent', 'asap', 'immediately', 'emergency', 'deadline', 
                           'court date', 'eviction', 'lockout', 'shutoff']
        for keyword in urgency_keywords:
            if keyword in user_lower:
                patterns['urgency_detected'] = True
                patterns['urgency_signals'].append(keyword)
        
        # Concern detection
        concern_keywords = {
            'money': ['afford', 'cost', 'money', 'pay', 'deposit', 'rent'],
            'safety': ['safe', 'threat', 'violence', 'dangerous', 'scared'],
            'procedure': ['how', 'what do i', 'where do i', 'when', 'steps'],
            'evidence': ['proof', 'document', 'evidence', 'receipt', 'photo'],
            'rights': ['right', 'legal', 'can they', 'allowed to', 'law']
        }
        
        for concern_type, keywords in concern_keywords.items():
            if any(kw in user_lower for kw in keywords):
                patterns['concerns'].append(concern_type)
        
        # Question type
        if '?' in user_input or any(q in user_lower for q in ['what', 'how', 'why', 'when', 'where']):
            patterns['question_type'] = 'seeking_information'
        elif any(w in user_lower for w in ['help', 'problem', 'issue', 'need']):
            patterns['question_type'] = 'seeking_help'
        
        # Emotional state
        if any(w in user_lower for w in ['worried', 'scared', 'afraid', 'stressed', 'panic']):
            patterns['emotional_state'] = 'distressed'
        elif any(w in user_lower for w in ['confused', 'unsure', 'dont know']):
            patterns['emotional_state'] = 'uncertain'
        
        return patterns
    
    def _update_curiosity_from_reasoning(self, reasoning_result: Dict, facts: Dict, stage: str) -> List[str]:
        """
        Update curiosity engine based on reasoning outcomes.
        Learn which reasoning paths work well.
        """
        updates = []
        summary = reasoning_result['summary']
        
        # Detect if reasoning identified knowledge gaps
        fact_step = reasoning_result['steps'][0]  # fact_gathering step
        if fact_step.get('fact_gaps'):
            for gap in fact_step['fact_gaps']:
                # Create curiosity question about missing fact
                question = {
                    'id': f"gap_{gap}_{datetime.now().timestamp()}",
                    'type': 'knowledge_gap',
                    'subject': gap,
                    'context': f"Stage: {stage}",
                    'created_at': datetime.now().isoformat(),
                    'importance': 'high' if summary['urgency'] in ['critical', 'urgent'] else 'medium'
                }
                self.curiosity._save_questions()
                updates.append(f"Detected knowledge gap: {gap}")
        
        # Learn from confidence levels
        confidence = summary['confidence']
        if confidence < 0.7:
            updates.append(f"Low confidence ({int(confidence*100)}%) - need better fact gathering")
        elif confidence > 0.9:
            updates.append(f"High confidence ({int(confidence*100)}%) - reasoning pattern successful")
        
        # Learn from urgency patterns
        if summary['urgency'] == 'critical' and len(fact_step.get('fact_gaps', [])) > 0:
            updates.append("Critical situation with missing facts - prioritize fact gathering")
        
        return updates
    
    def get_learning_summary(self) -> Dict:
        """
        Summarize what the system has learned from interactions.
        """
        if not self.interaction_history:
            return {'message': 'No interactions yet'}
        
        # Analyze patterns
        urgency_distribution = {}
        confidence_scores = []
        common_concerns = []
        
        for interaction in self.interaction_history:
            urgency = interaction['reasoning_summary']['urgency']
            urgency_distribution[urgency] = urgency_distribution.get(urgency, 0) + 1
            confidence_scores.append(interaction['reasoning_summary']['confidence'])
            
            if 'curiosity_patterns' in interaction and interaction['curiosity_patterns']:
                common_concerns.extend(interaction['curiosity_patterns'].get('concerns', []))
        
        return {
            'total_interactions': len(self.interaction_history),
            'urgency_distribution': urgency_distribution,
            'average_confidence': sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
            'most_common_concerns': list(set(common_concerns)),
            'learning_insights': [
                f"Processed {len(self.interaction_history)} interactions",
                f"Average confidence: {int(sum(confidence_scores)/len(confidence_scores)*100)}%" if confidence_scores else "No data",
                f"Most common urgency: {max(urgency_distribution, key=urgency_distribution.get)}" if urgency_distribution else "No data"
            ]
        }
    
    def suggest_next_question(self, facts: Dict, stage: str) -> str:
        """
        Based on curiosity + reasoning, suggest best next question to ask user.
        """
        # Get fact gaps from reasoning
        reasoning = self.reasoner.analyze(facts, stage)
        fact_gaps = reasoning['steps'][0].get('fact_gaps', [])
        
        if not fact_gaps:
            return "Tell me more about your situation"
        
        # Prioritize based on urgency
        urgency = reasoning['summary']['urgency']
        
        # Map facts to user-friendly questions
        questions = {
            'notices_received': "Have you received any notices from your landlord (eviction notice, termination letter)?",
            'court_date': "Do you have a court date scheduled?",
            'payment_current': "Are you current on rent payments?",
            'landlord_communication': "How would you describe your landlord's recent communication?",
            'timeline': "When did this situation start?"
        }
        
        # Return most critical missing fact
        for gap in fact_gaps:
            if gap in questions:
                prefix = "URGENT: " if urgency == 'critical' else ""
                return f"{prefix}{questions[gap]}"
        
        return "What's your main concern right now?"


# Test if run directly
if __name__ == '__main__':
    print("\n=== CURIOSITY-REASONING INTEGRATION TEST ===\n")
    
    bridge = CuriosityReasoningBridge()
    
    # Test 1: User expresses urgency
    print("Test 1: Urgency detection")
    print("-" * 50)
    facts1 = {
        'lease_status': 'ended',
        'still_in_unit': True,
        'payment_current': True
    }
    result1 = bridge.analyze_with_context(
        facts1, 
        'ended_lease', 
        "I got an eviction notice yesterday and I''m scared about losing my home"
    )
    print(f"Urgency detected: {result1['curiosity_insights']['urgency_detected']}")
    print(f"Concerns: {result1['curiosity_insights']['concerns']}")
    print(f"Emotional state: {result1['curiosity_insights']['emotional_state']}")
    print(f"Reasoning urgency: {result1['reasoning']['summary']['urgency']}")
    print(f"Learning updates: {len(result1['learning_updates'])}")
    
    # Test 2: User asks procedural question
    print("\n\nTest 2: Procedural question")
    print("-" * 50)
    facts2 = {
        'lease_status': 'ended',
        'still_in_unit': True,
        'payment_current': True,
        'notices_received': None
    }
    result2 = bridge.analyze_with_context(
        facts2,
        'ended_lease',
        "What steps do I need to take to get my security deposit back?"
    )
    print(f"Question type: {result2['curiosity_insights']['question_type']}")
    print(f"Concerns: {result2['curiosity_insights']['concerns']}")
    print(f"Primary issue: {result2['reasoning']['summary']['primary_issue']}")
    
    # Test 3: Suggest next question
    print("\n\nTest 3: Next question suggestion")
    print("-" * 50)
    facts3 = {
        'lease_status': 'ended',
        'still_in_unit': True
    }
    next_q = bridge.suggest_next_question(facts3, 'ended_lease')
    print(f"Suggested question: {next_q}")
    
    # Learning summary
    print("\n\nLearning Summary")
    print("=" * 50)
    summary = bridge.get_learning_summary()
    for insight in summary.get('learning_insights', []):
        print(f"  • {insight}")
