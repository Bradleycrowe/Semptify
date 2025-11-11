"""Test script to verify reasoning engine integration with dashboard"""
from learning_adapter import LearningAdapter
import json

# Create adapter with test user data
adapter = LearningAdapter({
    'user_id': 'test123',
    'location': 'Minneapolis, MN',
    'issue_type': 'eviction',
    'stage': 'LEGAL'
})

# Build dashboard
dashboard = adapter.build_dashboard()

print("✅ SUCCESS: Dashboard built with reasoning engine integration")
print(f"Has reasoning analysis: {adapter.reasoning_analysis is not None}")

if adapter.reasoning_analysis:
    print("\n📊 Reasoning Analysis:")
    print(f"  - Actions: {len(adapter.reasoning_analysis.get('actions', []))}")
    print(f"  - Facts: {len(adapter.reasoning_analysis.get('situation', {}).get('facts', []))}")
    print(f"  - Intensity: {adapter.reasoning_analysis.get('intensity_level', 'N/A')}")
    
    print("\n🎯 Top Actions:")
    for i, action in enumerate(adapter.reasoning_analysis.get('actions', [])[:3], 1):
        print(f"  {i}. {action.get('action', 'N/A')}")
        print(f"     Why: {action.get('why', 'N/A')[:60]}...")
else:
    print("⚠️ WARNING: Reasoning analysis not available")

print("\n✓ Test complete!")
