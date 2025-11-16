from reasoning_system import ReasoningSystem
from datetime import datetime, timedelta

print("\n" + "="*70)
print("TESTING REASONING SYSTEM WITH MULTIPLE SCENARIOS")
print("="*70)

# Scenario 1: CRISIS - Court date in 5 days
court_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
crisis_facts = {
    'lease_status': 'ended',
    'still_in_unit': True,
    'payment_current': False,
    'notices_received': 'eviction_summons',
    'court_date': court_date,
    'timeline': '30 days since notice'
}

reasoner = ReasoningSystem()
result1 = reasoner.analyze(crisis_facts, 'eviction')

print("\n1. CRISIS: Court date in 5 days")
print("-" * 70)
print(f"Urgency: {result1['summary']['urgency']}")
print(f"Risk Level: {result1['summary']['risk_level']}")
print(f"Recommendation: {result1['summary']['recommended_action']}")
print(f"Risks identified: {len(result1['steps'][3]['risks'])}")
if result1['steps'][3]['risks']:
    for risk in result1['steps'][3]['risks']:
        print(f"  - {risk}")

# Scenario 2: URGENT - Eviction notice received 3 days ago
notice_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
urgent_facts = {
    'lease_status': 'in_lease',
    'still_in_unit': True,
    'payment_current': False,
    'notices_received': 'eviction_notice',
    'eviction_notice_date': notice_date,
    'timeline': '3 days since notice'
}

result2 = reasoner.analyze(urgent_facts, 'in_lease')

print("\n2. URGENT: Eviction notice 3 days ago")
print("-" * 70)
print(f"Urgency: {result2['summary']['urgency']}")
print(f"Risk Level: {result2['summary']['risk_level']}")
print(f"Recommendation: {result2['summary']['recommended_action']}")
print(f"Risks identified: {len(result2['steps'][3]['risks'])}")
if result2['steps'][3]['risks']:
    for risk in result2['steps'][3]['risks']:
        print(f"  - {risk}")

# Scenario 3: NORMAL - Just exploring options
normal_facts = {
    'lease_status': 'in_lease',
    'still_in_unit': True,
    'payment_current': True,
    'notices_received': None,
    'timeline': '6 months into 12-month lease'
}

result3 = reasoner.analyze(normal_facts, 'in_lease')

print("\n3. NORMAL: Just exploring options")
print("-" * 70)
print(f"Urgency: {result3['summary']['urgency']}")
print(f"Risk Level: {result3['summary']['risk_level']}")
print(f"Recommendation: {result3['summary']['recommended_action']}")
print(f"Risks identified: {len(result3['steps'][3]['risks'])}")

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)
print(f"✓ Crisis urgency detected: {result1['summary']['urgency'] == 'critical'}")
print(f"✓ Urgent urgency detected: {result2['summary']['urgency'] == 'urgent'}")
print(f"✓ Normal urgency detected: {result3['summary']['urgency'] == 'normal'}")
print(f"✓ Crisis recommendation is urgent: {'URGENT' in result1['summary']['recommended_action']}")
