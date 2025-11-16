"""
Conversational Housing Journey Engine
Guides users through their housing situation with learning/growing at each step.
"""

class HousingJourneyEngine:
    """Conversational engine that learns from user responses and grows capabilities."""
    
    JOURNEY_STAGES = {
        'looking': {
            'label': 'Looking for Housing',
            'next_questions': [
                'What type of housing are you looking for? (apartment, house, room)',
                'What is your monthly housing budget?',
                'Do you have any rental history issues we should address?',
                'Do you need help with application fees or deposits?'
            ],
            'capabilities_needed': ['application_helper', 'budget_calculator', 'screening_prep']
        },
        'applying': {
            'label': 'Applying for Housing',
            'next_questions': [
                'Have you submitted applications yet?',
                'What documents do you have ready? (ID, pay stubs, references)',
                'Have you been denied? If so, do you know why?',
                'Do you need help understanding the application requirements?'
            ],
            'capabilities_needed': ['application_tracker', 'denial_response', 'document_checklist']
        },
        'signed_lease': {
            'label': 'Signed Lease - Moving In',
            'next_questions': [
                'When does your lease start?',
                'Have you done a move-in inspection?',
                'Do you understand your lease terms? (rent amount, due date, rules)',
                'Do you have move-in photos documented?'
            ],
            'capabilities_needed': ['lease_analyzer', 'inspection_guide', 'photo_documentation']
        },
        'in_lease': {
            'label': 'Currently in Lease',
            'next_questions': [
                'Are you having any issues with your rental?',
                'Maintenance problems? Pest issues? Neighbor conflicts?',
                'Is your rent being paid on time?',
                'Has landlord violated any lease terms?'
            ],
            'capabilities_needed': ['maintenance_tracker', 'rent_payment_log', 'lease_violation_detector']
        },
        'ending_lease': {
            'label': 'Lease Ending Soon',
            'next_questions': [
                'When does your lease end?',
                'Are you planning to renew or move out?',
                'Has landlord given you a rent increase notice?',
                'Do you need help with move-out procedures?'
            ],
            'capabilities_needed': ['renewal_analyzer', 'move_out_checklist', 'deposit_recovery']
        },
        'ended_lease': {
            'label': 'Lease Ended - Holdover or Moving',
            'next_questions': [
                'Have you moved out yet?',
                'Did you get your security deposit back?',
                'Are you still in the unit after lease end? (holdover)',
                'Has landlord threatened eviction?'
            ],
            'capabilities_needed': ['holdover_rights', 'deposit_dispute', 'eviction_defense']
        },
        'eviction': {
            'label': 'Facing Eviction',
            'next_questions': [
                'What type of notice did you receive? (3-day, 14-day, court summons)',
                'When did you receive the notice?',
                'What is the reason given? (non-payment, lease violation, holdover)',
                'Have you been to court yet?'
            ],
            'capabilities_needed': ['eviction_analyzer', 'court_response_generator', 'legal_aid_connector']
        }
    }
    
    def __init__(self):
        self.conversation_state = {}
        self.learned_facts = []
    
    def start_conversation(self) -> dict:
        """Begin the housing journey conversation."""
        return {
            'question': 'What is your current housing situation?',
            'options': [
                {'value': 'looking', 'label': '🔍 Looking for housing'},
                {'value': 'applying', 'label': '📝 Applying for housing'},
                {'value': 'signed_lease', 'label': '✍️ Just signed lease / moving in'},
                {'value': 'in_lease', 'label': '🏠 Currently renting (in my lease)'},
                {'value': 'ending_lease', 'label': '📅 My lease is ending soon'},
                {'value': 'ended_lease', 'label': '⏰ My lease ended (holdover/moving)'},
                {'value': 'eviction', 'label': '⚠️ Facing eviction or legal action'}
            ],
            'type': 'stage_selection'
        }
    
    def process_response(self, stage: str, user_answer: str, question_index: int = 0) -> dict:
        """
        Process user's response and determine next question or capability to grow.
        
        Returns:
            - next_question: str (if more questions needed)
            - capabilities_to_grow: list (engines to generate)
            - learned_facts: list (extracted information)
            - analysis: dict (insights from responses)
        """
        stage_info = self.JOURNEY_STAGES.get(stage, {})
        
        # Learn from the response
        fact = {
            'stage': stage,
            'question_index': question_index,
            'answer': user_answer,
            'timestamp': 'now'
        }
        self.learned_facts.append(fact)
        
        # Analyze what capabilities are needed
        capabilities_to_grow = []
        next_steps = []
        
        # Extract keywords to determine which engines to generate
        answer_lower = user_answer.lower()
        
        # Stage-specific capability detection
        if stage == 'looking':
            if 'budget' in answer_lower or '$' in user_answer:
                capabilities_to_grow.append('budget_calculator')
            if 'denied' in answer_lower or 'reject' in answer_lower:
                capabilities_to_grow.append('screening_prep')
        
        elif stage == 'applying':
            if 'denied' in answer_lower or 'rejected' in answer_lower:
                capabilities_to_grow.append('denial_response')
            if 'document' in answer_lower or 'paper' in answer_lower:
                capabilities_to_grow.append('document_checklist')
        
        elif stage == 'signed_lease':
            if 'inspection' in answer_lower or 'condition' in answer_lower:
                capabilities_to_grow.append('inspection_guide')
            if 'understand' in answer_lower or 'confus' in answer_lower:
                capabilities_to_grow.append('lease_analyzer')
        
        elif stage == 'in_lease':
            if any(word in answer_lower for word in ['repair', 'broken', 'leak', 'heat', 'maintenance']):
                capabilities_to_grow.append('maintenance_tracker')
            if 'rent' in answer_lower and ('late' in answer_lower or 'behind' in answer_lower):
                capabilities_to_grow.append('rent_payment_plan')
        
        elif stage == 'ending_lease':
            if 'increase' in answer_lower or 'raise' in answer_lower:
                capabilities_to_grow.append('rent_increase_analyzer')
            if 'deposit' in answer_lower:
                capabilities_to_grow.append('deposit_recovery')
        
        elif stage == 'ended_lease':
            if 'holdover' in answer_lower or 'still in' in answer_lower:
                capabilities_to_grow.append('holdover_rights')
            if 'deposit' in answer_lower and ('keep' in answer_lower or 'return' in answer_lower):
                capabilities_to_grow.append('deposit_dispute')
        
        elif stage == 'eviction':
            if 'notice' in answer_lower or 'day' in answer_lower:
                capabilities_to_grow.append('eviction_analyzer')
            if 'court' in answer_lower or 'summons' in answer_lower:
                capabilities_to_grow.append('court_response_generator')
        
        # Get next question in sequence
        questions = stage_info.get('next_questions', [])
        next_question = None
        if question_index + 1 < len(questions):
            next_question = questions[question_index + 1]
        
        return {
            'stage': stage,
            'stage_label': stage_info.get('label', stage),
            'learned_fact': fact,
            'capabilities_to_grow': capabilities_to_grow,
            'next_question': next_question,
            'progress': f"{question_index + 1}/{len(questions)}",
            'all_facts_learned': len(self.learned_facts),
            'recommendation': self._get_stage_recommendation(stage, self.learned_facts)
        }
    
    def _get_stage_recommendation(self, stage: str, facts: list) -> str:
        """Generate recommendation based on stage and learned facts."""
        recommendations = {
            'looking': 'Document everything during your search. Keep records of all applications and communications.',
            'applying': 'Get copies of everything you submit. If denied, ask for written explanation.',
            'signed_lease': 'Take photos/video of unit condition BEFORE moving in. Save this evidence.',
            'in_lease': 'Keep a log of all maintenance requests and landlord communications.',
            'ending_lease': 'Give proper notice in writing. Document unit condition for deposit return.',
            'ended_lease': 'Know your holdover rights. Keep paying rent if staying. Get agreements in writing.',
            'eviction': 'DO NOT IGNORE court papers. Respond immediately. Seek legal aid.'
        }
        return recommendations.get(stage, 'Document everything and know your rights.')

if __name__ == "__main__":
    # Test the engine
    engine = HousingJourneyEngine()
    
    # Start
    start = engine.start_conversation()
    print("QUESTION:", start['question'])
    print("\nOPTIONS:")
    for opt in start['options']:
        print(f"  {opt['label']}")
    
    # Simulate user selecting "ended_lease" (your situation)
    print("\n--- User selects: Lease ended (holdover) ---")
    result = engine.process_response('ended_lease', 'Yes, I am still in the unit after my lease ended', 0)
    
    print(f"\nStage: {result['stage_label']}")
    print(f"Progress: {result['progress']}")
    print(f"Capabilities to grow: {result['capabilities_to_grow']}")
    print(f"Next question: {result['next_question']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nTotal facts learned: {result['all_facts_learned']}")
