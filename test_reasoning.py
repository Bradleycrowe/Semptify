"""
Test & Simulate Reasoning Engine
Run different scenarios to see how the system reasons and generates recommendations.
"""

import json
from engines.reasoning_engine import get_reasoning_engine


def print_divider(title=""):
    """Print visual divider."""
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)
    print()


def print_cell_output(cell_name, title, content):
    """Format output as it would appear in a cell."""
    print(f"\n┌─ {cell_name}: {title} " + "─"*(75 - len(cell_name) - len(title)))
    if isinstance(content, list):
        for i, item in enumerate(content, 1):
            if isinstance(item, dict):
                print(f"\n  {i}. {item.get('action', item.get('title', 'Item'))}")
                if 'why' in item:
                    print(f"     WHY: {item['why']}")
                if 'how' in item:
                    print(f"     HOW: {item['how']}")
            else:
                print(f"  • {item}")
    elif isinstance(content, dict):
        for key, value in content.items():
            print(f"  {key}: {value}")
    else:
        print(f"  {content}")
    print("└" + "─"*79)


def simulate_scenario(scenario_name, user_id, context):
    """Run a simulation scenario."""
    print_divider(f"SCENARIO: {scenario_name}")

    print("📥 INPUT CONTEXT:")
    print(json.dumps(context, indent=2))

    # Get reasoning engine
    engine = get_reasoning_engine()

    # Analyze situation
    print("\n🧠 PROCESSING THROUGH 5 LEARNING ENGINES...")
    result = engine.analyze_situation(user_id, context)

    # Display Cell A: SITUATION
    print_cell_output(
        "CELL A",
        "Your Situation - Facts & Statistics",
        {
            "Facts Available": len(result['situation']['facts']),
            "Your Rights": len(result['situation']['your_rights']),
            "Journey Stage": result['situation']['journey_stage']
        }
    )

    if result['situation']['facts']:
        print("\n  📊 Key Facts:")
        for fact in result['situation']['facts'][:3]:
            print(f"     • {fact}")

    # Display Cell B: IMPACT & ACTION
    print_cell_output(
        "CELL B",
        "How This Affects You & What To Do",
        {
            "Impact": result['analysis']['impact_statement'],
            "Severity": result['analysis']['severity'],
            "Urgency": result['analysis']['urgency'],
            "Recommended Approach": result['analysis']['recommended_approach']
        }
    )

    print("\n  🎯 PRIORITIZED ACTIONS:")
    for action in result['actions'][:4]:  # Top 4 actions
        print(f"\n     Priority {action['priority']}: {action['action']}")
        print(f"     ├─ WHY: {action['why']}")
        print(f"     ├─ HOW: {action['how']}")
        print(f"     └─ URGENCY: {action['urgency']}")

    # Additional context
    print(f"\n  🔬 System Researching: {len(result['questions_researching'])} questions")
    print(f"  📍 Location Context: {bool(result['location_context'])}")
    print(f"  ⚡ Intensity Level: {result['intensity_level']}")


def run_all_tests():
    """Run all test scenarios."""

    print_divider("REASONING ENGINE TEST SUITE")
    print("Testing how the system analyzes different tenant situations")
    print("and generates smart recommendations...")

    # Scenario 1: New user, eviction notice
    simulate_scenario(
        "New User Gets Eviction Notice",
        user_id="test_user_001",
        context={
            "issue_type": "eviction",
            "severity": "high",
            "user_stress_level": "high",
            "location": "Minneapolis, MN",
            "situation_description": "Received 14-day eviction notice for alleged non-payment"
        }
    )

    # Scenario 2: Existing user, maintenance issue
    simulate_scenario(
        "Existing User - Landlord Ignoring Repairs",
        user_id="test_user_002",
        context={
            "issue_type": "maintenance",
            "severity": "medium",
            "user_stress_level": "medium",
            "location": "Minneapolis, MN",
            "situation_description": "Broken heating, landlord not responding for 3 weeks"
        }
    )

    # Scenario 3: Rent withholding question
    simulate_scenario(
        "User Considering Rent Withholding",
        user_id="test_user_003",
        context={
            "issue_type": "rent",
            "severity": "medium-high",
            "user_stress_level": "medium",
            "location": "Minneapolis, MN",
            "situation_description": "Multiple code violations, considering withholding rent"
        }
    )

    # Scenario 4: Retaliation concern
    simulate_scenario(
        "User Suspects Retaliation",
        user_id="test_user_004",
        context={
            "issue_type": "retaliation",
            "severity": "high",
            "user_stress_level": "high",
            "location": "Minneapolis, MN",
            "situation_description": "Landlord raised rent after tenant complained to inspector"
        }
    )

    # Scenario 5: Security deposit dispute
    simulate_scenario(
        "Security Deposit Not Returned",
        user_id="test_user_005",
        context={
            "issue_type": "security_deposit",
            "severity": "medium",
            "user_stress_level": "low",
            "location": "Minneapolis, MN",
            "situation_description": "Moved out 30 days ago, no deposit or itemized list"
        }
    )

    print_divider("TEST SUITE COMPLETE")
    print("✅ All scenarios processed successfully")
    print("\nThe reasoning engine is connecting all 5 learning modules to generate")
    print("intelligent, situation-specific recommendations for each user!")


if __name__ == "__main__":
    run_all_tests()
