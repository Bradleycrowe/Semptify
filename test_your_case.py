from reasoning_system import ReasoningSystem

# YOUR CASE: Lease ended 10/31/25 (15 days ago)
your_facts = {
    'lease_status': 'ended',
    'lease_end_date': '2025-10-31',
    'still_in_unit': True,
    'payment_current': True,
    'paying_rent': True,
    'notices_received': None,
    'landlord_communication': 'accepting rent',
    'deposit_returned': False,
    'timeline': '15 days since lease end'
}

reasoner = ReasoningSystem()
result = reasoner.analyze(your_facts, 'ended_lease')

print('\n' + '='*60)
print('YOUR ACTUAL CASE: Lease ended 10/31/25 (15 days ago)')
print('='*60 + '\n')

for step in result['steps']:
    step_name = step['step'].replace('_', ' ').upper()
    reasoning = step.get('reasoning', step.get('recommendation', ''))
    print(f'{step_name}:')
    print(f'  {reasoning}\n')

print('='*60)
print('SUMMARY')
print('='*60)
s = result['summary']
print(f'Primary Issue: {s["primary_issue"]}')
print(f'Risk Level: {s["risk_level"]}')
print(f'Urgency: {s["urgency"]}')
print(f'Confidence: {int(s["confidence"]*100)}%')
print(f'\nRecommendation: {s["recommended_action"]}')

print('\n' + '='*60)
print('YOUR 3 OPTIONS')
print('='*60)
options = result['steps'][4]['options']
for i, opt in enumerate(options, 1):
    print(f'\n{i}. {opt["option"]}')
    print(f'   Legal basis: {opt["basis"]}')
    print(f'   Requirements: {opt["requirements"]}')
    print(f'   Pros: {opt["pros"]}')
    print(f'   Cons: {opt["cons"]}')

print('\n' + '='*60)
print('NEXT STEPS')
print('='*60)
steps = result['steps'][5]['next_steps']
for i, step in enumerate(steps, 1):
    print(f'{i}. {step}')

print('\n' + '='*60)
print('LEGAL RESEARCH NEEDED')
print('='*60)
statutes = result['steps'][2]['statutes_needed']
for statute in statutes:
    print(f'MN {statute}: https://www.revisor.mn.gov/statutes/cite/{statute}')
