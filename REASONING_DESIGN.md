REASONING IN AI SYSTEMS
========================

What is Reasoning?
-----------------
Reasoning = Breaking down complex problems into logical steps, considering multiple 
perspectives, weighing evidence, and arriving at well-supported conclusions.

Traditional AI: Give answer immediately
Reasoning AI: Think through the problem step-by-step before answering

Example Without Reasoning:
Q: "Can my landlord evict me?"
A: "Check your lease and local laws."

Example WITH Reasoning:
Q: "Can my landlord evict me?"
Internal reasoning:
1. Need to know: lease status, payment history, notices received
2. Need to check: MN eviction grounds (504B.285)
3. Consider: Is this holdover? nonpayment? lease violation?
4. Verify: What notices are required? (504B.321)
5. Context: Court timelines, tenant defenses available
6. Conclusion: Provide stage-specific guidance based on their situation

A: "It depends on several factors. Let me ask you some questions to understand 
    your situation better..." [then provides personalized guidance]


HOW SEMPTIFY CURRENTLY USES REASONING
======================================

1. Stage Detection Reasoning
---------------------------
housing_journey_engine.py → start_conversation()

Reasoning process:
- User at what stage? (looking, applying, in_lease, ending, ended, eviction)
- What questions reveal their context?
- What capabilities will they need based on stage?
- What legal issues are likely?

Code implements this as:
JOURNEY_STAGES = {
    'ended_lease': {
        'questions': [...],  # designed to reveal holdover situation
        'capabilities_needed': ['holdover_rights', 'security_deposit']
    }
}


2. Keyword Analysis Reasoning
-----------------------------
housing_journey_engine.py → process_response()

Reasoning process:
- Parse user answer for keywords
- "holdover" → implies lease ended, still in unit → need holdover_rights
- "eviction notice" → implies legal action → need eviction_defense
- "deposit" → implies move-out → need deposit_recovery

Code implements this as:
if any(kw in answer.lower() for kw in ['holdover', 'end of lease', 'lease expired']):
    capabilities_to_grow.append('holdover_rights')


3. Legal Conflict Reasoning
---------------------------
legal_conflict_resolver.py → analyze_preemption()

Reasoning process:
- Is there federal law on this topic?
- Is there state law on this topic?
- Do they conflict?
- If yes: Which type of preemption? (express, field, conflict, obstacle)
- What is the model? (floor vs ceiling)
- Which law controls?

Code implements this as:
if analysis.model == 'floor':
    result['applied_logic'].append(
        'Prefer more-protective state/local rules unless there is express preemption'
    )


4. Source Verification Reasoning
--------------------------------
official_sources.py → classify_source()

Reasoning process:
- Is this a legal fact claim or context/opinion?
- If legal fact: MUST be .gov source
- If context: Can be reputable non-gov
- What type of source is this URL?
- Can we use it for this purpose?

Code implements this as:
def classify_source(url):
    if is_official_source(url):
        return 'official'  # Use for legal facts
    elif is_reputable(url):
        return 'reputable'  # Use for context only
    else:
        return 'unknown'  # Don't use


WHERE SEMPTIFY NEEDS MORE REASONING
====================================

Current gaps where explicit reasoning would help:

1. Intent Detection
------------------
Currently: Keyword matching
Better with reasoning:
- Why are they asking this question?
- What outcome do they want?
- Are they proactive or reactive?
- Do they have resources to fight or need quick resolution?

Example reasoning chain:
User: "My lease ended 2 weeks ago"
→ Could be: intentional holdover, accidental, waiting for new lease, etc.
→ Ask: "Are you planning to stay or move?"
→ If stay: focus on month-to-month conversion
→ If move: focus on deposit recovery and proper notice


2. Risk Assessment
-----------------
Currently: Lists generic options
Better with reasoning:
- What are the realistic risks in THIS situation?
- Timeline analysis: How urgent is this?
- Probability: What is landlord likely to do?
- Consequences: Best/worst case scenarios

Example reasoning chain:
Facts: Holdover 14 days, rent paid, no notice from landlord
→ Reasoning:
  - MN 504B.141: Now month-to-month (lowest rent interval)
  - 504B.135: Either party needs notice to terminate
  - No notice = landlord hasn't begun eviction process
  - Risk level: LOW (landlord accepting rent = implicit consent)
  - Timeline: Secure if paying; vulnerable if stopping
→ Guidance: "Continue paying rent on time. Get any agreement in writing."


3. Next-Best-Action
------------------
Currently: General recommendations
Better with reasoning:
- Given their stage, resources, and goals
- What is the SINGLE most important thing to do next?
- What can wait? What is urgent?
- What has highest impact?

Example reasoning chain:
Situation: Eviction notice received, court date in 10 days
→ Reasoning:
  - Timeline critical: 10 days to respond
  - 504B.335: Must file answer before trial
  - Free legal aid available? (check local resources)
  - Defenses available? (retaliation, improper notice, payment tendered)
  - Priority 1: File answer (preserves rights)
  - Priority 2: Gather evidence (lease, payment receipts, photos)
  - Priority 3: Seek legal representation
→ Guidance: "URGENT: You must file an answer within 10 days..."


HOW TO ADD EXPLICIT REASONING TO SEMPTIFY
==========================================

Approach: Multi-step reasoning engine

Step 1: Create reasoning_engine.py
-----------------------------------
class ReasoningEngine:
    def analyze_situation(self, facts, stage, answers):
        """
        Multi-step reasoning process:
        1. Gather facts
        2. Identify issues
        3. Research applicable law
        4. Assess risks
        5. Determine options
        6. Recommend next action
        """
        reasoning_chain = []
        
        # Step 1: What do we know?
        reasoning_chain.append({
            'step': 'fact_gathering',
            'known': facts,
            'unknown': self._identify_gaps(facts, stage)
        })
        
        # Step 2: What are the legal issues?
        reasoning_chain.append({
            'step': 'issue_identification',
            'issues': self._identify_legal_issues(facts, stage)
        })
        
        # Step 3: What does the law say?
        reasoning_chain.append({
            'step': 'legal_research',
            'applicable_laws': self._fetch_applicable_laws(issues)
        })
        
        # Step 4: What are the risks?
        reasoning_chain.append({
            'step': 'risk_assessment',
            'risks': self._assess_risks(facts, laws),
            'timeline': self._assess_urgency(facts, laws)
        })
        
        # Step 5: What are the options?
        reasoning_chain.append({
            'step': 'option_generation',
            'options': self._generate_options(facts, laws, risks)
        })
        
        # Step 6: What should they do next?
        reasoning_chain.append({
            'step': 'recommendation',
            'next_action': self._determine_best_action(options, risks, resources)
        })
        
        return {
            'reasoning_chain': reasoning_chain,
            'confidence': self._assess_confidence(reasoning_chain),
            'show_to_user': self._format_for_display(reasoning_chain)
        }


Step 2: Integration Points
--------------------------
journey_routes.py → /api/journey/respond:
    1. Get user answer
    2. Update facts in engine
    3. Call ReasoningEngine.analyze_situation()
    4. Return reasoning + recommendations
    5. UI shows: "Here's how we arrived at this guidance..."


Step 3: UI Transparency
-----------------------
templates/housing_journey.html:
    - "Our Analysis" section showing reasoning steps
    - "What we considered:"
      • Your situation: [facts]
      • Applicable laws: [citations]
      • Timeline: [urgency]
      • Options: [numbered list]
    - "We recommend: [next action] because [reasoning]"


BENEFITS OF EXPLICIT REASONING
===============================

1. Transparency: User sees HOW system arrived at conclusion
2. Trust: Can verify each reasoning step against their situation
3. Correctness: Structured reasoning reduces errors
4. Explainability: Can show reasoning chain if questioned
5. Improvement: Can identify where reasoning breaks down


NEXT STEP
=========
Should I build the ReasoningEngine for Semptify?

It would:
- Take conversation facts + stage
- Run multi-step analysis
- Research applicable MN laws
- Assess risks and urgency
- Generate personalized options
- Recommend next best action
- Show reasoning chain to user

Want me to implement this?
