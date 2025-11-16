"""
Test jurisdiction engine - shows how legal hierarchy works
"""

from engines.jurisdiction_engine import get_jurisdiction

def test_mold_jurisdiction():
    """Test: Mold issue in Sacramento - which law applies?"""

    engine = get_jurisdiction()

    result = engine.get_procedural_requirements(
        issue_type="mold",
        location={
            "city": "sacramento_city",
            "county": "sacramento_county",
            "state": "california"
        }
    )

    print("=" * 60)
    print("JURISDICTION TEST: Mold in Sacramento")
    print("=" * 60)
    print(f"\nIssue: {result['issue_type']}")
    print(f"Category: {result['category']}")
    print(f"\n{'─' * 60}")
    print("APPLICABLE LAW:")
    print(f"{'─' * 60}")
    print(f"Statute: {result['applicable_law']['statute']}")
    print(f"Jurisdiction: {result['applicable_law']['jurisdiction']}")
    print(f"Requirement: {result['applicable_law']['requirement']}")
    print(f"Deadline: {result['applicable_law']['deadline']}")

    print(f"\n{'─' * 60}")
    print("CONFLICT RESOLUTION:")
    print(f"{'─' * 60}")
    print(result['conflict_resolution'])

    print(f"\n{'─' * 60}")
    print("PROCEDURAL STEPS:")
    print(f"{'─' * 60}")
    for step in result['procedural_steps']:
        print(f"\nSTEP {step['step']}: {step['action']}")
        print(f"  Required: {step['required']}")
        print(f"  Legal Basis: {step['legal_basis']}")
        print(f"  Deadline: {step['deadline']}")
        print(f"  Validation: {step['validation']}")


def test_security_deposit_conflict():
    """Test: Security deposit - state vs city law conflict"""

    engine = get_jurisdiction()

    # Sacramento City has stricter deposit limits than state
    laws = engine.determine_applicable_laws(
        issue_category="payment",
        city="sacramento_city",
        county="sacramento_county",
        state="california"
    )

    print("\n\n" + "=" * 60)
    print("JURISDICTION TEST: Security Deposit Limits")
    print("=" * 60)

    for law in laws:
        print(f"\n{law.level.upper()} LAW:")
        print(f"  Statute: {law.statute}")
        print(f"  Requirement: {law.requirement}")
        print(f"  Protective Level: {law.protective_level}/10")

    winner, explanation = engine.resolve_conflict(laws)

    print(f"\n{'─' * 60}")
    print("RESOLUTION:")
    print(f"{'─' * 60}")
    print(explanation)


def test_health_hazard_timeline():
    """Test: Health hazard repair timeline - city vs state"""

    engine = get_jurisdiction()

    laws = engine.determine_applicable_laws(
        issue_category="health_hazard",
        city="sacramento_city",
        county="sacramento_county",
        state="california"
    )

    print("\n\n" + "=" * 60)
    print("JURISDICTION TEST: Health Hazard Repair Timeline")
    print("=" * 60)

    print("\nQUESTION: How long does landlord have to fix mold?")
    print("\nAPPLICABLE LAWS:")

    for law in laws:
        print(f"\n  • {law.jurisdiction} ({law.statute})")
        print(f"    Deadline: {law.deadline}")
        print(f"    Protective Level: {law.protective_level}/10")

    winner, explanation = engine.resolve_conflict(laws)

    print(f"\n{'─' * 60}")
    print("ANSWER:")
    print(f"{'─' * 60}")
    print(f"✅ {winner.deadline} ({winner.statute})")
    print(f"\nReason: {winner.jurisdiction} has stricter timeline than state law")
    print("Local ordinances can be MORE protective than state (but not less)")


if __name__ == "__main__":
    test_mold_jurisdiction()
    test_security_deposit_conflict()
    test_health_hazard_timeline()

    print("\n\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("=" * 60)
    print("✅ Most PROTECTIVE law wins")
    print("✅ Local CAN be stricter than state")
    print("✅ State CANNOT be weaker than federal")
    print("✅ Lease CANNOT violate any law")
    print("=" * 60)
