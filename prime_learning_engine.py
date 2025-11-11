"""
Prime Learning Engine with Tenant Rights Knowledge

Pre-trains the learning engine with common tenant scenarios, successful patterns,
and recommended action sequences so it can provide intelligent suggestions from day 1.
"""

import json
import os
from datetime import datetime, timedelta
import random

def create_seed_data():
    """
    Create seed data representing successful tenant rights workflows.
    Based on real-world patterns that work for tenants.
    """
    
    # Successful action sequences (what tenants should do in order)
    successful_sequences = {
        # Eviction defense workflow
        "view_eviction_info->download_forms": 15,
        "download_forms->upload_lease": 12,
        "upload_lease->document_evidence": 10,
        "document_evidence->file_complaint": 8,
        "file_complaint->track_case": 8,
        
        # Rent withholding workflow
        "view_rent_withhold_info->upload_photos": 10,
        "upload_photos->send_notice_landlord": 9,
        "send_notice_landlord->file_escrow": 7,
        
        # Housing inspection workflow
        "view_housing_codes->request_inspection": 12,
        "request_inspection->upload_photos": 10,
        "upload_photos->track_complaint": 8,
        
        # Legal aid workflow
        "view_legal_resources->find_legal_aid": 15,
        "find_legal_aid->schedule_consultation": 10,
        "schedule_consultation->prepare_documents": 8,
        
        # Discrimination complaint workflow
        "view_discrimination_info->document_incident": 12,
        "document_incident->file_hud_complaint": 9,
        "file_hud_complaint->upload_evidence": 8,
        
        # Common preparation workflows
        "upload_lease->upload_receipts": 10,
        "upload_receipts->upload_correspondence": 8,
        "upload_correspondence->organize_timeline": 7,
        
        # Court filing workflows
        "view_court_procedures->download_forms": 14,
        "download_forms->fill_forms_online": 11,
        "fill_forms_online->file_electronically": 9,
        "file_electronically->pay_filing_fee": 8,
        "pay_filing_fee->schedule_hearing": 7,
        
        # Emergency workflows
        "view_emergency_resources->call_hotline": 10,
        "call_hotline->emergency_shelter": 5,
        "emergency_shelter->apply_assistance": 8,
    }
    
    # User habits (simulating successful tenants who got results)
    simulated_users = {
        "success_user_001": {
            "upload_lease": 3,
            "document_evidence": 5,
            "file_complaint": 2,
            "track_case": 4,
            "view_legal_resources": 3,
        },
        "success_user_002": {
            "view_housing_codes": 4,
            "request_inspection": 2,
            "upload_photos": 6,
            "file_hud_complaint": 1,
        },
        "success_user_003": {
            "view_eviction_info": 5,
            "download_forms": 4,
            "upload_lease": 2,
            "file_complaint": 2,
            "find_legal_aid": 3,
        },
        "success_user_004": {
            "view_rent_withhold_info": 3,
            "send_notice_landlord": 2,
            "file_escrow": 1,
            "upload_photos": 4,
        },
        "success_user_005": {
            "view_discrimination_info": 4,
            "document_incident": 5,
            "file_hud_complaint": 2,
            "find_legal_aid": 2,
        },
    }
    
    # Time patterns (when tenants typically take action)
    time_patterns = {
        # Evenings after work (most common)
        18: {"view_eviction_info": 20, "view_legal_resources": 15, "upload_lease": 12},
        19: {"document_evidence": 18, "upload_photos": 16, "fill_forms_online": 14},
        20: {"file_complaint": 12, "view_housing_codes": 10, "organize_timeline": 8},
        21: {"track_case": 10, "view_discrimination_info": 8, "prepare_documents": 6},
        
        # Lunch breaks
        12: {"view_eviction_info": 10, "find_legal_aid": 8, "call_hotline": 6},
        13: {"view_legal_resources": 8, "view_rent_withhold_info": 6},
        
        # Weekend mornings
        9: {"download_forms": 12, "upload_lease": 10, "schedule_consultation": 8},
        10: {"fill_forms_online": 14, "organize_timeline": 10, "document_evidence": 8},
        11: {"file_electronically": 10, "upload_correspondence": 8},
    }
    
    # Success rates (based on which actions typically lead to good outcomes)
    success_rates = {
        # High success actions (90%+)
        "upload_lease": {"attempts": 50, "successes": 48},
        "document_evidence": {"attempts": 45, "successes": 43},
        "view_legal_resources": {"attempts": 60, "successes": 58},
        "find_legal_aid": {"attempts": 40, "successes": 38},
        "upload_photos": {"attempts": 52, "successes": 50},
        
        # Good success actions (70-90%)
        "file_complaint": {"attempts": 30, "successes": 25},
        "request_inspection": {"attempts": 35, "successes": 28},
        "send_notice_landlord": {"attempts": 40, "successes": 32},
        "file_hud_complaint": {"attempts": 25, "successes": 20},
        "schedule_consultation": {"attempts": 38, "successes": 32},
        
        # Moderate success actions (50-70%)
        "file_escrow": {"attempts": 20, "successes": 12},
        "file_electronically": {"attempts": 28, "successes": 18},
        "apply_assistance": {"attempts": 45, "successes": 28},
        
        # Common but lower success (users need help)
        "fill_forms_online": {"attempts": 50, "successes": 30},  # 60% - needs guidance
        "navigate_court_system": {"attempts": 35, "successes": 18},  # 51% - difficult
        "represent_self_court": {"attempts": 25, "successes": 10},  # 40% - get lawyer!
    }
    
    # Suggestions by context (what to suggest based on user's situation)
    suggestions = {
        "facing_eviction": "view_eviction_info",
        "bad_conditions": "view_housing_codes",
        "discrimination": "view_discrimination_info",
        "need_lawyer": "find_legal_aid",
        "rent_dispute": "view_rent_withhold_info",
        "first_visit": "view_legal_resources",
        "uploaded_lease": "document_evidence",
        "has_evidence": "file_complaint",
        "filed_complaint": "track_case",
        "need_forms": "download_forms",
    }
    
    return {
        "user_habits": simulated_users,
        "sequences": successful_sequences,
        "time_patterns": time_patterns,
        "success_rates": success_rates,
        "suggestions": suggestions,
    }


def prime_learning_engine(data_dir: str = "data"):
    """
    Prime the learning engine with tenant rights knowledge.
    
    Args:
        data_dir: Directory where learning patterns are stored
    """
    
    print("🧠 Priming Learning Engine with Tenant Rights Knowledge...")
    print("=" * 60)
    
    # Create data directory if needed
    os.makedirs(data_dir, exist_ok=True)
    patterns_file = os.path.join(data_dir, "learning_patterns.json")
    
    # Check if already primed
    if os.path.exists(patterns_file):
        response = input(f"\n⚠️  {patterns_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled. Existing patterns preserved.")
            return
    
    # Generate seed data
    print("\n📊 Generating seed data from successful tenant workflows...")
    seed_data = create_seed_data()
    
    # Add metadata
    seed_data["_metadata"] = {
        "primed_at": datetime.now().isoformat(),
        "version": "1.0",
        "source": "tenant_rights_success_patterns",
        "description": "Pre-trained with successful tenant action patterns",
        "total_sequences": len(seed_data["sequences"]),
        "total_users": len(seed_data["user_habits"]),
        "total_success_data_points": sum(
            sr["attempts"] for sr in seed_data["success_rates"].values()
        ),
    }
    
    # Save to file
    print(f"\n💾 Writing primed patterns to {patterns_file}...")
    with open(patterns_file, 'w', encoding='utf-8') as f:
        json.dump(seed_data, f, indent=2)
    
    # Print summary
    print("\n✅ Learning Engine Primed Successfully!")
    print("=" * 60)
    print(f"📈 Statistics:")
    print(f"  • Successful sequences learned: {len(seed_data['sequences'])}")
    print(f"  • Simulated successful users: {len(seed_data['user_habits'])}")
    print(f"  • Time patterns (hourly): {len(seed_data['time_patterns'])}")
    print(f"  • Action success rates: {len(seed_data['success_rates'])}")
    print(f"  • Context suggestions: {len(seed_data['suggestions'])}")
    print(f"  • Total training data points: {seed_data['_metadata']['total_success_data_points']}")
    
    print(f"\n🎯 Most Successful Action Sequences:")
    top_sequences = sorted(
        seed_data["sequences"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    for seq, count in top_sequences:
        print(f"  • {seq} ({count} successes)")
    
    print(f"\n🏆 Highest Success Rate Actions:")
    success_rates = {
        action: (stats["successes"] / stats["attempts"] * 100)
        for action, stats in seed_data["success_rates"].items()
    }
    top_actions = sorted(success_rates.items(), key=lambda x: x[1], reverse=True)[:5]
    for action, rate in top_actions:
        print(f"  • {action}: {rate:.1f}%")
    
    print(f"\n💡 The learning engine will now provide intelligent suggestions")
    print(f"   based on these proven tenant success patterns!")
    print("\n✨ Ready to help tenants with data-driven recommendations.")


def verify_learning_engine():
    """
    Verify the learning engine can load and use the primed data.
    """
    print("\n🔍 Verifying Learning Engine...")
    
    try:
        from learning_engine import init_learning
        
        engine = init_learning()
        insights = engine.get_insights()
        
        print("✅ Learning engine loaded successfully!")
        print(f"  • Total actions tracked: {insights['total_actions_tracked']}")
        print(f"  • Most common sequences: {len(insights['most_common_sequences'])}")
        print(f"  • Actions with success data: {len(insights['success_rates'])}")
        
        # Test suggestion
        suggestion = engine.suggest_next_action("test_user", "upload_lease")
        if suggestion:
            print(f"\n💡 Example: After 'upload_lease', suggests: '{suggestion}'")
        
        print("\n✅ All systems operational!")
        
    except Exception as e:
        print(f"❌ Error verifying: {e}")
        print("   Make sure learning_engine.py exists and is working.")


if __name__ == "__main__":
    import sys
    
    # Allow specifying data directory
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    
    # Prime the engine
    prime_learning_engine(data_dir)
    
    # Verify it worked
    verify_learning_engine()
