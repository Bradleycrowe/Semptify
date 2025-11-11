"""
Simple Reasoning Engine Demo - Shows Cell A and Cell B concept
"""

def analyze_situation_simple(user_id: str, context: dict) -> dict:
    """
    Simple demonstration of how reasoning works for Cell A and Cell B.
    """

    issue_type = context.get("issue_type", "eviction")
    severity = context.get("severity", "medium")

    # CELL A: SITUATION - Facts & Statistics
    situation = {
        "facts": [
            f"You're dealing with: {issue_type.upper()}",
            f"Severity level: {severity}",
            "Minnesota law provides strong tenant protections",
            "Landlords must follow specific legal procedures",
            "You have the right to defend yourself in court"
        ],
        "statistics": {
            "success_rate": "65% of tenants win when they show up with evidence",
            "avg_resolution_time": "30-60 days with proper documentation"
        },
        "your_rights": [
            "Right to proper notice (14 days minimum)",
            "Right to repair and deduct",
            "Protection from retaliation",
            "Right to withhold rent for serious violations"
        ]
    }

    # CELL B: IMPACT & ACTION - Analysis and what to do
    if severity == "high":
        impact = "CRITICAL - Immediate action required to protect your rights"
        urgency = "immediate"
    elif severity == "medium-high":
        impact = "SERIOUS - Legal protections available, take action soon"
        urgency = "within 48 hours"
    else:
        impact = "MANAGEABLE - Stay informed and document everything"
        urgency = "within 1 week"

    analysis = {
        "impact_statement": impact,
        "severity": severity,
        "urgency": urgency,
        "recommended_approach": "legal" if severity == "high" else "positive_support"
    }

    actions = [
        {
            "priority": 1,
            "action": "Document Everything NOW",
            "why": "Evidence is your strongest protection",
            "how": "Take photos, save texts/emails, write down dates and times",
            "urgency": "immediate"
        },
        {
            "priority": 2,
            "action": "Check Your Deadlines",
            "why": "Missing deadlines can cost you your case",
            "how": "Look for any court dates or response deadlines in your notices",
            "urgency": urgency
        },
        {
            "priority": 3,
            "action": "Know Your Rights",
            "why": "Landlords count on tenants not knowing the law",
            "how": "Study Minnesota tenant laws for your specific situation",
            "urgency": "within 24 hours"
        },
        {
            "priority": 4,
            "action": "File Appropriate Forms" if severity == "high" else "Prepare Your Defense",
            "why": "Legal protection requires legal action",
            "how": "Answer any eviction notice, file complaints if needed",
            "urgency": urgency
        }
    ]

    return {
        "situation": situation,
        "analysis": analysis,
        "actions": actions
    }


# TEST IT
if __name__ == "__main__":
    print("\n" + "="*80)
    print("  REASONING ENGINE DEMO - Cell A & Cell B")
    print("="*80 + "\n")

    # Test scenario
    result = analyze_situation_simple(
        user_id="demo_user",
        context={
            "issue_type": "eviction",
            "severity": "high",
            "location": "Minneapolis, MN"
        }
    )

    # Display CELL A
    print("┌─ CELL A: YOUR SITUATION - Facts & Statistics ─────────────────────────")
    print("\n📊 KEY FACTS:")
    for fact in result['situation']['facts']:
        print(f"   • {fact}")

    print("\n📈 STATISTICS:")
    for key, value in result['situation']['statistics'].items():
        print(f"   • {key}: {value}")

    print("\n⚖️  YOUR RIGHTS:")
    for right in result['situation']['your_rights'][:3]:
        print(f"   • {right}")

    print("└" + "─"*79)

    # Display CELL B
    print("\n┌─ CELL B: IMPACT & WHAT TO DO ─────────────────────────────────────────")
    print(f"\n⚠️  IMPACT: {result['analysis']['impact_statement']}")
    print(f"🎯 URGENCY: {result['analysis']['urgency'].upper()}")
    print(f"📋 APPROACH: {result['analysis']['recommended_approach']}")

    print("\n🎯 PRIORITIZED ACTIONS:")
    for action in result['actions']:
        print(f"\n   {action['priority']}. {action['action'].upper()}")
        print(f"      WHY: {action['why']}")
        print(f"      HOW: {action['how']}")
        print(f"      ⏰ {action['urgency']}")

    print("\n└" + "─"*79)

    print("\n✅ This is how Cell A and Cell B work together!")
    print("   Cell A = Facts about your situation")
    print("   Cell B = Impact analysis + actionable steps\n")
