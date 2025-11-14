"""
Test situation analyzer integration with learning modules.
Verifies alignment with Semptify principles.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from situation_analyzer import analyze_situation, generate_situation_cards
from learning_engine import init_learning
from human_perspective import humanize_object, READING_LEVELS, AUDIENCE_TIPS


def test_situation_analyzer_uses_learning_engine():
    """Verify situation analyzer integrates with learning engine."""
    # Initialize learning engine
    engine = init_learning(data_dir="data")
    
    # Simulate user situation
    user_data = {
        "issue_type": "eviction_notice",
        "urgency": "high",
        "location": "MN",
        "stage": "SEARCHING",
        "has_evidence": True,
        "notice_date": "2024-01-15"
    }
    
    # Analyze situation
    analysis = analyze_situation(user_data)
    
    # Check analysis has required fields
    assert "issue_type" in analysis
    assert "urgency" in analysis
    assert "success_rate" in analysis
    assert "learning_action" in analysis  # New field for tracking
    
    print("✓ Analysis includes learning action tracking")
    
    # Generate cards
    cards = generate_situation_cards(analysis, user_id="test_user_123")
    
    # Verify cards exist
    assert len(cards) >= 4, "Should generate at least 4 cards"
    
    # Verify "Document Everything" card exists
    doc_card = None
    for card in cards:
        if card["group_name"] == "Document Everything":
            doc_card = card
            break
    
    assert doc_card is not None, "Should have 'Document Everything' card"
    print("✓ 'Document Everything' card exists")
    
    # Verify plain language in cards
    for card in cards:
        # Check for "You" language (plain, direct)
        text = f"{card.get('description', '')} {card['what']} {card['why']} {card['when']}"
        has_you = "you" in text.lower() or "your" in text.lower()
        assert has_you, \
            f"Card '{card['title']}' should use 'you' language. Text: {text[:100]}"
        
        # Check for short descriptions (plain language principle)
        assert len(card["description"]) < 200, \
            f"Card '{card['title']}' description too long for plain language"
    
    print("✓ All cards use plain language")
    
    # Verify evidence emphasis
    evidence_mentions = sum(
        1 for card in cards 
        if "evidence" in str(card).lower() or 
           "document" in str(card).lower() or
           "photo" in str(card).lower()
    )
    assert evidence_mentions >= 3, "Cards should emphasize evidence collection"
    print("✓ Cards emphasize evidence collection")
    
    print(f"\n✅ Generated {len(cards)} cards with Semptify principles:")
    for card in cards:
        print(f"   - {card['icon']} {card['title']} ({card['group_name']})")


def test_humanize_object_integration():
    """Verify human_perspective integration."""
    test_card = {
        "title": "Test Card",
        "description": "Technical description with jargon and complexity",
        "what": "Complex legal procedure",
        "why": "Required by statute 123.456",
        "who": "Petitioner or counsel"
    }
    
    # Apply humanization
    humanized = humanize_object(test_card, context={
        "audience": "tenant",
        "reading_level": "plain"
    })
    
    # Check humanization result
    assert "next_steps" in humanized
    assert "audience" in humanized
    assert humanized["audience"] == "tenant"
    assert humanized["reading_level"] == "plain"
    
    # Verify next_steps emphasize documentation
    next_steps = humanized["next_steps"]
    doc_steps = [s for s in next_steps if "document" in s.lower() or 
                 "upload" in s.lower() or "save" in s.lower() or
                 "timeline" in s.lower() or "witness" in s.lower()]
    
    assert len(doc_steps) >= 3, "Humanized output should emphasize documentation"
    
    print("✓ humanize_object() emphasizes documentation")
    print(f"✅ Humanized output has {len(next_steps)} next steps")


def test_reading_levels_and_audience():
    """Verify READING_LEVELS and AUDIENCE_TIPS are defined correctly."""
    # Check reading levels
    assert "plain" in READING_LEVELS
    assert "simple" in READING_LEVELS
    assert "standard" in READING_LEVELS
    assert "professional" in READING_LEVELS
    
    # Verify plain language guidance
    plain_guidance = READING_LEVELS["plain"]
    assert "simple" in plain_guidance.lower() or "short" in plain_guidance.lower()
    
    print("✓ Reading levels defined correctly")
    
    # Check audiences
    assert "tenant" in AUDIENCE_TIPS
    assert "advocate" in AUDIENCE_TIPS
    assert "judge" in AUDIENCE_TIPS
    assert "landlord" in AUDIENCE_TIPS
    
    # Verify tenant guidance emphasizes evidence
    tenant_tips = AUDIENCE_TIPS["tenant"]
    assert "evidence" in tenant_tips.lower() or "save" in tenant_tips.lower()
    
    print("✓ Audience tips emphasize evidence for tenants")
    print("✅ All reading levels and audiences configured")


if __name__ == "__main__":
    print("Testing situation analyzer integration with Semptify principles...\n")
    
    try:
        test_situation_analyzer_uses_learning_engine()
        print()
        test_humanize_object_integration()
        print()
        test_reading_levels_and_audience()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - Situation analyzer aligns with:")
        print("   - LearningEngine for pattern tracking")
        print("   - human_perspective for plain language")
        print("   - 'Document everything!' core principle")
        print("   - Tenant-focused, evidence-first approach")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
