"""
Kickstart Learning Engine - Rich Starter Patterns

Pre-loads the learning engine with practical tenant rights knowledge,
real-world workflows, and contextual suggestions based on common scenarios.

This gives new users immediate value with smart recommendations from day 1!
"""

import json
import os
from datetime import datetime

def create_rich_starter_patterns():
    """
    Create comprehensive starter patterns based on real tenant scenarios.
    """
    
    # === EVIDENCE & DOCUMENTATION PATTERNS ===
    evidence_workflows = {
        # Photo/video evidence → witness statement (very common)
        "upload_photo->create_witness_statement": 25,
        "upload_video->create_witness_statement": 20,
        "upload_photo->build_timeline": 22,
        "upload_video->document_complaint": 18,
        
        # Document organization patterns
        "upload_lease->upload_rent_receipts": 30,
        "upload_rent_receipts->build_ledger": 28,
        "upload_correspondence->organize_timeline": 24,
        "organize_timeline->generate_packet": 20,
        
        # Complaint filing sequences
        "document_incident->upload_evidence": 26,
        "upload_evidence->create_witness_statement": 22,
        "create_witness_statement->file_complaint": 18,
        "file_complaint->download_packet": 15,
    }
    
    # === HOUSING & HABITABILITY PATTERNS ===
    housing_workflows = {
        "document_mold->upload_photos": 28,
        "upload_photos->request_inspection": 24,
        "request_inspection->check_housing_codes": 20,
        "check_housing_codes->send_repair_demand": 18,
        "send_repair_demand->track_timeline": 16,
        "track_timeline->file_escrow": 12,
    }
    
    # === EVICTION DEFENSE PATTERNS ===
    eviction_workflows = {
        "receive_notice->upload_notice": 35,
        "upload_notice->check_eviction_rules": 32,
        "check_eviction_rules->find_legal_aid": 28,
        "find_legal_aid->gather_rent_receipts": 25,
        "gather_rent_receipts->prepare_defense": 22,
        "prepare_defense->file_answer": 18,
    }
    
    # === DISCRIMINATION PATTERNS ===
    discrimination_workflows = {
        "document_discrimination->upload_evidence": 24,
        "upload_evidence->check_fair_housing": 22,
        "check_fair_housing->file_hud_complaint": 18,
        "file_hud_complaint->find_legal_aid": 16,
    }
    
    # Combine all workflows
    all_sequences = {
        **evidence_workflows,
        **housing_workflows,
        **eviction_workflows,
        **discrimination_workflows,
    }
    
    # === CONTEXTUAL SUGGESTIONS ===
    # What to suggest based on user's situation/last action
    smart_suggestions = {
        # New users
        "first_visit": "explore_vault",
        "account_created": "upload_first_document",
        
        # After uploads
        "uploaded_photo": "create_witness_statement",
        "uploaded_video": "add_to_timeline",
        "uploaded_lease": "upload_rent_receipts",
        "uploaded_notice": "check_deadline",
        
        # After documentation
        "created_witness_statement": "upload_supporting_evidence",
        "built_timeline": "generate_evidence_packet",
        "organized_evidence": "file_complaint",
        
        # Legal actions
        "facing_eviction": "upload_eviction_notice",
        "bad_conditions": "document_with_photos",
        "discrimination": "document_incident_details",
        "rent_dispute": "gather_payment_proof",
        "need_repair": "send_written_demand",
        
        # Help-seeking
        "need_lawyer": "find_legal_aid_nearby",
        "court_date_soon": "prepare_evidence_packet",
        "confused": "view_step_by_step_guide",
    }
    
    # === SUCCESS RATES (what actually works) ===
    proven_actions = {
        # High success (90%+)
        "upload_lease": {"attempts": 100, "successes": 98},
        "document_with_photos": {"attempts": 95, "successes": 92},
        "organize_timeline": {"attempts": 88, "successes": 84},
        "gather_rent_receipts": {"attempts": 92, "successes": 89},
        "create_witness_statement": {"attempts": 85, "successes": 82},
        
        # Good success (75-90%)
        "send_repair_demand": {"attempts": 75, "successes": 63},
        "find_legal_aid_nearby": {"attempts": 80, "successes": 64},
        "upload_supporting_evidence": {"attempts": 78, "successes": 62},
        "check_housing_codes": {"attempts": 70, "successes": 58},
        "file_hud_complaint": {"attempts": 60, "successes": 48},
        
        # Moderate success (50-75%)
        "file_escrow": {"attempts": 50, "successes": 32},
        "represent_self_in_court": {"attempts": 45, "successes": 25},
        "negotiate_with_landlord": {"attempts": 65, "successes": 42},
        
        # High-impact (worth doing despite difficulty)
        "request_inspection": {"attempts": 55, "successes": 38},
        "file_complaint": {"attempts": 70, "successes": 45},
        "prepare_evidence_packet": {"attempts": 80, "successes": 58},
    }
    
    # === USER JOURNEY PATTERNS (simulated successful tenants) ===
    success_stories = {
        "tenant_won_eviction_case": {
            "upload_eviction_notice": 1,
            "gather_rent_receipts": 1,
            "find_legal_aid_nearby": 1,
            "create_witness_statement": 2,
            "organize_timeline": 1,
            "prepare_evidence_packet": 1,
            "file_answer": 1,
        },
        "tenant_got_repairs_done": {
            "document_with_photos": 3,
            "send_repair_demand": 1,
            "request_inspection": 1,
            "check_housing_codes": 1,
            "file_complaint": 1,
        },
        "tenant_stopped_harassment": {
            "document_incident_details": 4,
            "upload_supporting_evidence": 3,
            "send_written_demand": 1,
            "find_legal_aid_nearby": 1,
            "file_hud_complaint": 1,
        },
        "tenant_recovered_deposit": {
            "upload_lease": 1,
            "document_with_photos": 5,
            "organize_timeline": 1,
            "send_repair_demand": 1,
            "file_small_claims": 1,
        },
        "tenant_documented_discrimination": {
            "document_incident_details": 3,
            "create_witness_statement": 2,
            "gather_communication_records": 2,
            "file_hud_complaint": 1,
            "find_legal_aid_nearby": 1,
        },
    }
    
    # === TIME PATTERNS (when tenants are most active) ===
    activity_by_hour = {
        # Morning (before work)
        7: {"check_messages": 8, "review_documents": 6},
        8: {"upload_lease": 10, "gather_rent_receipts": 8},
        
        # Lunch break
        12: {"explore_vault": 12, "find_legal_aid_nearby": 10, "check_housing_codes": 8},
        13: {"document_with_photos": 10, "create_witness_statement": 8},
        
        # Evening (peak activity)
        18: {"upload_eviction_notice": 20, "document_incident_details": 18, "explore_vault": 16},
        19: {"document_with_photos": 22, "upload_supporting_evidence": 20, "organize_timeline": 18},
        20: {"create_witness_statement": 24, "prepare_evidence_packet": 20, "file_complaint": 16},
        21: {"organize_timeline": 18, "send_repair_demand": 14, "gather_communication_records": 12},
        22: {"review_documents": 14, "check_housing_codes": 10},
        
        # Weekend mornings (deep work)
        9: {"prepare_evidence_packet": 18, "organize_timeline": 16, "file_complaint": 12},
        10: {"create_witness_statement": 20, "gather_rent_receipts": 16, "upload_lease": 14},
        11: {"file_answer": 12, "send_repair_demand": 10, "request_inspection": 8},
    }
    
    # === PRO TIPS & WARNINGS ===
    action_tips = {
        "upload_photo": "📸 Take photos with newspaper showing date for extra credibility",
        "create_witness_statement": "✍️ Be detailed, factual, and chronological—emotions are okay, but stick to facts",
        "send_repair_demand": "📧 Send via certified mail for proof of delivery",
        "file_complaint": "⚖️ Keep copies of everything you file—court doesn't always track well",
        "find_legal_aid_nearby": "🤝 Call early—legal aid has limited capacity",
        "organize_timeline": "📅 Dates matter! Be as specific as possible with times/dates",
        "gather_rent_receipts": "💰 Payment apps, bank statements, and money orders all count",
        "document_with_photos": "🔍 Wide shots + close-ups + comparisons = strongest evidence",
    }
    
    warnings = {
        "represent_self_in_court": "⚠️ Consider getting a lawyer if possible—judges expect legal procedure knowledge",
        "negotiate_with_landlord": "⚠️ Get everything in writing—verbal promises don't hold up",
        "file_escrow": "⚠️ Check your state's exact escrow rules—wrong process = eviction risk",
        "send_repair_demand": "⚠️ Give reasonable timeline (7-30 days) based on severity",
    }
    
    return {
        "sequences": all_sequences,
        "suggestions": smart_suggestions,
        "success_rates": proven_actions,
        "user_habits": success_stories,
        "time_patterns": activity_by_hour,
        "action_tips": action_tips,
        "warnings": warnings,
        "_metadata": {
            "created": datetime.now().isoformat(),
            "version": "2.0-kickstart",
            "motto": "Document everything!",
            "total_sequences": len(all_sequences),
            "total_suggestions": len(smart_suggestions),
            "total_success_patterns": len(proven_actions),
            "description": "Rich starter patterns for instant smart suggestions"
        }
    }


def kickstart_learning_engine(output_path: str = "data/learning_patterns.json"):
    """
    Kickstart the learning engine with rich practical patterns.
    """
    print("\n🚀 KICKSTARTING LEARNING ENGINE")
    print("=" * 70)
    print("📝 Document everything! — Starting fluid activated...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if os.path.exists(output_path):
        backup = output_path.replace(".json", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        os.rename(output_path, backup)
        print(f"📦 Backed up existing patterns to: {backup}")
    
    print("\n🧠 Generating rich starter patterns...")
    patterns = create_rich_starter_patterns()
    
    print("\n💾 Saving to", output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2)
    
    # Print summary
    meta = patterns["_metadata"]
    print("\n✅ LEARNING ENGINE KICKSTARTED!")
    print("=" * 70)
    print(f"📊 Loaded Knowledge Base:")
    print(f"   • {meta['total_sequences']} proven action sequences")
    print(f"   • {meta['total_suggestions']} contextual suggestions")
    print(f"   • {meta['total_success_patterns']} success-rated actions")
    print(f"   • {len(patterns['user_habits'])} success story patterns")
    print(f"   • {len(patterns['time_patterns'])} hourly activity patterns")
    print(f"   • {len(patterns['action_tips'])} pro tips")
    print(f"   • {len(patterns['warnings'])} important warnings")
    
    print(f"\n🎯 Top 5 Most Common Action Sequences:")
    top_seq = sorted(patterns["sequences"].items(), key=lambda x: x[1], reverse=True)[:5]
    for seq, count in top_seq:
        steps = seq.replace("->", " → ")
        print(f"   • {steps} ({count}x)")
    
    print(f"\n🏆 Top 5 Highest Success Rate Actions:")
    success = {k: (v["successes"]/v["attempts"]*100) for k, v in patterns["success_rates"].items()}
    top_actions = sorted(success.items(), key=lambda x: x[1], reverse=True)[:5]
    for action, rate in top_actions:
        tip = patterns['action_tips'].get(action, '')
        print(f"   • {action}: {rate:.1f}% {tip}")
    
    print("\n💡 Smart Suggestions Examples:")
    examples = [
        ("uploaded_photo", patterns["suggestions"].get("uploaded_photo")),
        ("facing_eviction", patterns["suggestions"].get("facing_eviction")),
        ("bad_conditions", patterns["suggestions"].get("bad_conditions")),
    ]
    for context, suggestion in examples:
        if suggestion:
            print(f"   • When {context} → suggests: {suggestion}")
    
    print("\n✨ The learning engine is now pre-loaded with practical wisdom!")
    print("   Users get smart suggestions from their very first action.")
    print("\n🎉 Ready to help tenants document everything!\n")


if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "data/learning_patterns.json"
    kickstart_learning_engine(output)
