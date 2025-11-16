"""Seed Growth Simulation
Watch the seed grow engines based on user interactions.
"""
from seed_manager import SeedManager, UserBucketSimulator

def run_simulation():
    print("=" * 60)
    print("SEED GROWTH SIMULATION")
    print("=" * 60)
    
    # Create simulated bucket
    bucket = UserBucketSimulator("simulated_buckets/test_user_1")
    manager = SeedManager(bucket)
    
    # Plant or load seed
    print("\n[SEED] Step 1: Initialize Seed")
    print("-" * 60)
    manager.ensure_seed_exists({'name': 'Test User', 'state': 'CA'})
    
    # Simulation scenarios
    scenarios = [
        {
            'step': 2,
            'input': "I got a 3-day notice to quit, what should I do?",
            'expected_capability': 'eviction_defense'
        },
        {
            'step': 3,
            'input': "My landlord raised rent from $1500 to $1800, is that legal?",
            'expected_capability': 'rent_calculator'
        },
        {
            'step': 4,
            'input': "I need to file a motion for continuance",
            'expected_capability': 'motion_writer'
        },
        {
            'step': 5,
            'input': "I got another eviction notice, help!",
            'expected_capability': 'eviction_defense'  # Reuse existing
        }
    ]
    
    for scenario in scenarios:
        print(f"\n[STEP] Step {scenario['step']}: User Interaction")
        print("-" * 60)
        print(f"User says: '{scenario['input']}'")
        print()
        
        result = manager.process_user_input(scenario['input'])
        
        print(f"\n[RESULT] Result:")
        print(f"   Status: {result['status']}")
        print(f"   Capability: {result.get('capability', 'N/A')}")
        if result['status'] == 'success':
            print(f"   [OK] Successfully executed engine")
            if isinstance(result.get('result'), dict):
                for k, v in list(result['result'].items())[:3]:
                    print(f"     • {k}: {str(v)[:50]}")
        elif result['status'] == 'error':
            print(f"   [ERR] Error: {result.get('error')}")
    
    # Final seed state
    print("\n" + "=" * 60)
    print("FINAL SEED STATE")
    print("=" * 60)
    print(f"Seed ID: {manager.seed.seed_id}")
    print(f"Total Interactions: {manager.seed.interaction_count}")
    print(f"Capabilities Grown: {len(manager.seed.capabilities)}")
    print("\nCapabilities:")
    for cap in manager.seed.capabilities:
        print(f"  • {cap.name}")
        print(f"    Engine: {cap.engine_file}")
        print(f"    Usage: {cap.usage_count} times")
        print(f"    Success rate: {cap.success_rate * 100:.0f}%")
        print(f"    Created: {cap.created_at}")
    
    print(f"\nBucket Contents:")
    files = bucket.list_files()
    for f in files:
        print(f"  • {f}")
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    
    # Show one generated engine
    if bucket.file_exists("engines/eviction_defense.py"):
        print("\n[FILE] Sample Generated Engine (eviction_defense.py):")
        print("-" * 60)
        engine_code = bucket.read_file("engines/eviction_defense.py")
        print(engine_code[:500] + "..." if len(engine_code) > 500 else engine_code)

if __name__ == '__main__':
    run_simulation()

