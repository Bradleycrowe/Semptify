from reasoning_system import ReasoningSystem

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

print('Result keys:', result.keys())
print('\nFull result structure:')
import json
print(json.dumps(result, indent=2, default=str))
