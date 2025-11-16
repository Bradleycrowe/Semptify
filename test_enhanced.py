from reasoning_system import ReasoningSystem
import json

# YOUR CASE: Lease ended 10/31/25
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

print('\n' + '='*70)
print('YOUR CASE: Lease ended 10/31/25 (15 days ago) - ENHANCED')
print('='*70 + '\n')

# Show winter protections
step4 = result['steps'][3]
if step4.get('winter_protections'):
    print('❄️  WINTER PROTECTIONS ACTIVE (Oct 1 - Apr 30)')
    print('   Heat must be 68°F minimum')
    print('   Utilities cannot be shut off\n')

# Show all options with full details
print('YOUR OPTIONS WITH FULL DETAILS:')
print('='*70)
options = result['steps'][4]['options']
for i, opt in enumerate(options, 1):
    print(f'\n{i}. {opt["option"]}')
    print(f'   Legal basis: {opt["basis"]}')
    print(f'   Requirements: {opt["requirements"]}')
    
    if 'evidence_needed' in opt:
        print('\n   📋 Evidence you''ll need:')
        for ev in opt['evidence_needed']:
            print(f'      • {ev}')
    
    if 'action_steps' in opt:
        print('\n   📝 Action steps:')
        for j, step in enumerate(opt['action_steps'], 1):
            print(f'      {j}. {step}')
    
    if 'costs' in opt:
        print(f'\n   💰 Cost: {opt["costs"]}')
    
    if 'timeline' in opt:
        print(f'   ⏱️  Timeline: {opt["timeline"]}')
    
    print(f'\n   ✓ Pros: {", ".join(opt["pros"])}')
    print(f'   ✗ Cons: {", ".join(opt["cons"])}')

# Show recommendation with resources
print('\n' + '='*70)
print('RECOMMENDED ACTION')
print('='*70)
step6 = result['steps'][5]
print(f'\n{step6["recommendation"]}')
print(f'\nPriority: {step6["priority"]}')
print('\nNext steps:')
for i, step in enumerate(step6['next_steps'], 1):
    print(f'{i}. {step}')

print('\n📞 FREE LEGAL HELP:')
for resource in step6['resources']:
    print(f'   • {resource["name"]}: {resource["phone"]}')
    if 'hours' in resource:
        print(f'     Hours: {resource["hours"]}')
    if 'url' in resource:
        print(f'     Web: {resource["url"]}')

print('\n' + '='*70)
print(f'Confidence: {int(result["summary"]["confidence"]*100)}%')
print('='*70)
