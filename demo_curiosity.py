"""
Demonstration: How Curiosity Engine Works
Shows app learning through curiosity
"""

from engines.curiosity_engine import get_curiosity

def demo_prediction_failure():
    """Demo: App learns from being wrong"""

    print("=" * 70)
    print("CURIOSITY DEMO 1: Learning from Prediction Failure")
    print("=" * 70)

    curiosity = get_curiosity()

    # App made a prediction
    prediction = {
        "outcome": "tenant_wins",
        "confidence": 85,
        "factors": {
            "has_photos": True,
            "sent_notice": True,
            "waited_30_days": True
        }
    }

    # Actual outcome was different
    actual = {
        "outcome": "tenant_loses",
        "reason": "improper_service",
        "factors": {
            "has_photos": True,
            "sent_notice": True,
            "waited_30_days": True,
            "service_method": "certified_mail_unsigned"  # Missing factor!
        }
    }

    print("\n📊 APP'S PREDICTION:")
    print(f"   Outcome: {prediction['outcome']}")
    print(f"   Confidence: {prediction['confidence']}%")
    print(f"   Based on: {list(prediction['factors'].keys())}")

    print("\n❌ ACTUAL OUTCOME:")
    print(f"   Outcome: {actual['outcome']}")
    print(f"   Reason: {actual['reason']}")

    # Curiosity is triggered
    question = curiosity.detect_prediction_failure(prediction, actual)

    print("\n🤔 CURIOSITY TRIGGERED:")
    print(f"   Question: {question}")

    # Research the question
    question_obj = curiosity.questions["pending"][-1]
    print(f"\n🔬 RESEARCHING...")
    print(f"   Research paths:")
    for path in question_obj["research_paths"]:
        print(f"     • {path}")

    findings = curiosity.research_question(question_obj["id"])

    print(f"\n💡 FINDINGS:")
    print(f"   Root cause: {findings['root_cause']}")
    print(f"   Missing factors: {len(findings['missing_factors'])}")
    for mf in findings["missing_factors"]:
        print(f"     • {mf['factor']}: {mf['value']}")

    print(f"\n✅ APP IMPROVED:")
    print(f"   {findings['correction']['action']}")
    print(f"   Expected improvement: {findings['correction']['expected_improvement']}")


def demo_anomaly_detection():
    """Demo: App gets curious about unusual pattern"""

    print("\n\n" + "=" * 70)
    print("CURIOSITY DEMO 2: Learning from Anomalies")
    print("=" * 70)

    curiosity = get_curiosity()

    print("\n📊 OBSERVED PATTERN:")
    print("   ABC Management retaliates: 60% of cases")
    print("   XYZ Properties retaliates: 5% of cases")

    print("\n🤔 CURIOSITY TRIGGERED:")
    print("   Question: Why is XYZ Properties so different?")

    question = curiosity.detect_anomaly(
        pattern_name="landlord_retaliation",
        expected_behavior="60% retaliation rate",
        observed_behavior="5% retaliation rate",
        context={
            "landlord": "XYZ Properties",
            "cases": 20,
            "retaliation_count": 1
        }
    )

    question_obj = curiosity.questions["pending"][-1]

    print(f"\n🔬 RESEARCHING...")
    findings = curiosity.research_question(question_obj["id"])

    print(f"\n💡 FINDINGS:")
    print(f"   {findings['explanation']}")
    print(f"   Insight: {findings['actionable_insight']}")

    print(f"\n✅ NEW STRATEGY LEARNED:")
    print("   XYZ Properties responds well to complaints")
    print("   → Suggest filing complaints confidently (low retaliation risk)")
    print("   → Other landlords may have similar profiles (research more)")


def demo_knowledge_gap():
    """Demo: App realizes it needs more information"""

    print("\n\n" + "=" * 70)
    print("CURIOSITY DEMO 3: Filling Knowledge Gaps")
    print("=" * 70)

    curiosity = get_curiosity()

    print("\n📊 SITUATION:")
    print("   User asks: 'How much will mold remediation cost?'")
    print("   App knows: ❌ No data on repair costs")

    print("\n🤔 CURIOSITY TRIGGERED:")

    question = curiosity.detect_knowledge_gap(
        topic="average cost of mold remediation",
        why_needed="Users need cost estimates for legal claims"
    )

    print(f"   Question: {question}")

    question_obj = curiosity.questions["pending"][-1]

    print(f"\n🔬 RESEARCHING...")
    print("   Sources to check:")
    for path in question_obj["research_paths"]:
        print(f"     • {path}")

    findings = curiosity.research_question(question_obj["id"])

    print(f"\n💡 DATA COLLECTED:")
    print(f"   Topic: {findings['topic']}")
    print(f"   Sources used: {', '.join(findings['sources'])}")
    print(f"   Confidence: {findings['confidence']}")

    print(f"\n✅ NEW CAPABILITY:")
    print("   App can now estimate mold remediation costs")
    print("   → Helps users evaluate settlement offers")
    print("   → Warns if landlord claims 'too expensive'")


def demo_user_correction():
    """Demo: App learns from user who ignored suggestion"""

    print("\n\n" + "=" * 70)
    print("CURIOSITY DEMO 4: Learning from User Corrections")
    print("=" * 70)

    curiosity = get_curiosity()

    print("\n📊 SITUATION:")
    print("   App suggested: File with Rent Board (6 week timeline)")
    print("   User did: Filed with Health Dept instead")
    print("   Result: Resolved in 2 weeks (better!)")

    print("\n🤔 CURIOSITY TRIGGERED:")
    print("   Question: Why did user's choice work better?")

    question = curiosity.detect_user_correction(
        suggestion={"action": "file_rent_board", "timeline": "6 weeks"},
        user_action={"action": "file_health_dept", "timeline": "2 weeks"},
        result={"outcome": "resolved", "time_taken": "2 weeks"}
    )

    question_obj = curiosity.questions["pending"][-1]

    print(f"\n🔬 RESEARCHING...")
    findings = curiosity.research_question(question_obj["id"])

    print(f"\n💡 FINDINGS:")
    print(f"   Why user was right: {findings['why_user_was_right']}")
    print(f"   When to use: {findings['when_to_use_user_method']}")

    print(f"\n✅ RECOMMENDATION UPDATED:")
    print("   OLD: Always suggest Rent Board for all complaints")
    print("   NEW: Health hazards → Health Dept (faster)")
    print("        General issues → Rent Board")


def demo_self_evaluation():
    """Demo: App evaluates its own performance"""

    print("\n\n" + "=" * 70)
    print("CURIOSITY DEMO 5: Self-Evaluation & Improvement")
    print("=" * 70)

    curiosity = get_curiosity()

    # Simulate some predictions
    predictions = [
        {"prediction": {"outcome": "win"}, "actual": {"outcome": "win"}, "correct": True},
        {"prediction": {"outcome": "win"}, "actual": {"outcome": "win"}, "correct": True},
        {"prediction": {"outcome": "win"}, "actual": {"outcome": "lose"}, "correct": False},
        {"prediction": {"outcome": "lose"}, "actual": {"outcome": "win"}, "correct": False},
        {"prediction": {"outcome": "win"}, "actual": {"outcome": "win"}, "correct": True},
    ]

    print("\n📊 APP'S RECENT PREDICTIONS:")
    print(f"   Total: {len(predictions)}")
    print(f"   Correct: {sum(1 for p in predictions if p['correct'])}")
    print(f"   Incorrect: {sum(1 for p in predictions if not p['correct'])}")

    evaluation = curiosity.evaluate_performance(predictions)

    print(f"\n🎯 SELF-EVALUATION:")
    print(f"   Accuracy: {evaluation['accuracy']}")
    print(f"   Curiosity questions generated: {len(evaluation['curiosity_triggered'])}")

    print(f"\n🔬 RESEARCH AGENDA:")
    agenda = curiosity.generate_research_agenda()
    print(f"   Total questions pending: {agenda['total_questions']}")
    print(f"   High priority: {agenda['high_priority']}")

    print(f"\n✅ CONTINUOUS IMPROVEMENT:")
    print("   App notices when it's wrong")
    print("   → Gets curious about why")
    print("   → Researches the answer")
    print("   → Updates its model")
    print("   → Gets smarter over time")


if __name__ == "__main__":
    demo_prediction_failure()
    demo_anomaly_detection()
    demo_knowledge_gap()
    demo_user_correction()
    demo_self_evaluation()

    print("\n\n" + "=" * 70)
    print("KEY TAKEAWAY: CURIOSITY-DRIVEN LEARNING")
    print("=" * 70)
    print("✅ App notices when it doesn't know something")
    print("✅ App asks questions and researches answers")
    print("✅ App learns from users who do things differently")
    print("✅ App evaluates itself and improves continuously")
    print("✅ App becomes smarter through curiosity, not just data")
    print("=" * 70)
