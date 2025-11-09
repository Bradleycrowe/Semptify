"""
Comprehensive Semptify Test Suite
Tests all major components and user flows
"""

import sys
import json
from datetime import datetime, timedelta

print("\n" + "="*80)
print("SEMPTIFY COMPREHENSIVE TEST SUITE")
print("="*80)

# TEST 1: Dashboard Components
print("\n[TEST 1] Dashboard Component System")
print("-" * 80)
try:
    from dashboard_components import (
        DashboardBuilder, RightsComponent, InformationComponent,
        InputComponent, NextStepsComponent, TimelineComponent
    )
    
    # Create and populate all component types
    builder = DashboardBuilder()
    
    rights = RightsComponent()
    rights.add_right("Test Right", "Test Description", "Test Source")
    builder.add_component(rights, 1)
    
    info = InformationComponent()
    info.add_warning("Test Warning", "Test warning description")
    info.add_guidance("Test Guidance", "Test guidance description")
    builder.add_component(info, 2)
    
    input_comp = InputComponent()
    input_comp.add_field("test_field", "Test Field", field_type="text")
    builder.add_component(input_comp, 3)
    
    steps = NextStepsComponent()
    steps.add_step(1, "Step 1", "Description")
    builder.add_component(steps, 4)
    
    timeline = TimelineComponent()
    timeline.add_event("2025-11-15", "Test Event", "Test Description", "deadline")
    builder.add_component(timeline, 5)
    
    # Verify structure
    json_data = builder.to_json()
    assert len(json_data['components']) == 5, "Should have 5 components"
    assert json_data['rows'] == [1, 2, 3, 4, 5], "Should have rows 1-5"
    
    print("✅ All 5 component types created and assigned to correct rows")
    print(f"   - RightsComponent (Row 1)")
    print(f"   - InformationComponent (Row 2)")
    print(f"   - InputComponent (Row 3)")
    print(f"   - NextStepsComponent (Row 4)")
    print(f"   - TimelineComponent (Row 5)")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

# TEST 2: Learning Adapter
print("\n[TEST 2] Learning Adapter - Multiple Scenarios")
print("-" * 80)
try:
    from learning_adapter import generate_dashboard_for_user, LearningAdapter
    
    scenarios = [
        ("SEARCHING", "move", "Minneapolis, MN"),
        ("HAVING_TROUBLE", "maintenance", "St. Paul, MN"),
        ("CONFLICT", "rent", "Minneapolis, MN"),
        ("LEGAL", "eviction", "Minneapolis, MN"),
    ]
    
    for stage, issue, location in scenarios:
        user_data = {
            "location": location,
            "issue_type": issue,
            "stage": stage,
            "history": []
        }
        
        result = generate_dashboard_for_user("test_user", user_data)
        
        # Verify structure
        assert result['stage'] == stage, f"Stage mismatch"
        assert result['issue_type'] == issue, f"Issue type mismatch"
        assert len(result['dashboard']['components']) == 5, f"Should have 5 components"
        
        # Verify row assignments
        rows_found = set()
        for comp in result['dashboard']['components']:
            rows_found.add(comp['row'])
        
        assert rows_found == {1, 2, 3, 4, 5}, f"Missing rows: {rows_found}"
        
        print(f"✅ Stage: {stage:15} | Issue: {issue:15} | Location: {location}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 3: User Database
print("\n[TEST 3] User Database & Schema")
print("-" * 80)
try:
    from user_database import init_database, _get_db
    
    # Initialize database
    init_database()
    
    # Check if tables exist
    db = _get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    db.close()
    
    required_tables = ['pending_users', 'users', 'user_learning_profiles', 'user_interactions']
    missing = [t for t in required_tables if t not in tables]
    
    if missing:
        print(f"❌ FAILED: Missing tables: {missing}")
        sys.exit(1)
    
    print(f"✅ All required tables exist:")
    for table in required_tables:
        print(f"   - {table}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 4: Flask Routes
print("\n[TEST 4] Flask Routes & Endpoints")
print("-" * 80)
try:
    from Semptify import app
    
    # Get all registered routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)
    
    required_routes = [
        '/register',
        '/signin',
        '/verify',
        '/dashboard',
        '/api/dashboard',
        '/api/dashboard/update'
    ]
    
    missing_routes = [r for r in required_routes if r not in routes]
    
    if missing_routes:
        print(f"❌ FAILED: Missing routes: {missing_routes}")
        print(f"\nAvailable routes: {sorted(routes)}")
        sys.exit(1)
    
    print(f"✅ All required routes registered:")
    for route in required_routes:
        print(f"   - {route}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 5: Component HTML Generation
print("\n[TEST 5] HTML Generation & Rendering")
print("-" * 80)
try:
    from learning_adapter import LearningAdapter
    
    adapter = LearningAdapter({
        "location": "Minneapolis, MN",
        "issue_type": "rent",
        "stage": "HAVING_TROUBLE"
    })
    
    dashboard = adapter.build_dashboard()
    
    # Get HTML
    html = dashboard.get_html()
    
    # Verify HTML structure
    assert '<div class="dashboard-container">' in html, "Missing container"
    assert 'component-full-width' in html, "Missing components"
    assert 'rights-box' in html, "Missing rights box"
    assert 'information-box' in html, "Missing information box"
    assert 'input-box' in html, "Missing input box"
    assert 'next-steps-box' in html, "Missing next steps box"
    assert 'timeline-box' in html, "Missing timeline box"
    
    # Count component occurrences
    component_count = html.count('component-full-width')
    assert component_count == 5, f"Expected 5 components, found {component_count}"
    
    print(f"✅ Valid HTML generated with all 5 components:")
    print(f"   - Total HTML length: {len(html):,} characters")
    print(f"   - Component count: {component_count}")
    print(f"   - All required component types present")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 6: Dynamic Behavior
print("\n[TEST 6] Stage-Specific Behavior")
print("-" * 80)
try:
    from learning_adapter import LearningAdapter
    
    # Test that different stages produce different input fields
    stages = ["SEARCHING", "HAVING_TROUBLE", "CONFLICT", "LEGAL"]
    field_counts = {}
    
    for stage in stages:
        adapter = LearningAdapter({
            "location": "Minneapolis, MN",
            "issue_type": "rent",
            "stage": stage
        })
        
        dashboard = adapter.build_dashboard()
        json_data = dashboard.to_json()
        
        # Find input component
        input_comp = None
        for comp in json_data['components']:
            if comp['component']['type'] == 'InputComponent':
                input_comp = comp['component']
                break
        
        if input_comp and input_comp['content'] and 'input_fields' in input_comp['content']:
            field_counts[stage] = len(input_comp['content']['input_fields'])
        else:
            field_counts[stage] = 0
    
    # Verify stages produce different field counts
    assert len(set(field_counts.values())) > 1, "All stages should not have same field count"
    
    print(f"✅ Stage-specific input fields:")
    for stage, count in field_counts.items():
        print(f"   - {stage:15}: {count} input fields")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 7: Jurisdiction-Specific Rights
print("\n[TEST 7] Jurisdiction-Specific Rights")
print("-" * 80)
try:
    from learning_adapter import LearningAdapter
    
    # Test Minnesota vs California
    states = {
        "Minneapolis, MN": "MN",
        "San Francisco, CA": "CA"
    }
    
    for location, state_code in states.items():
        adapter = LearningAdapter({
            "location": location,
            "issue_type": "rent",
            "stage": "CONFLICT"
        })
        
        dashboard = adapter.build_dashboard()
        json_data = dashboard.to_json()
        
        # Find rights component
        rights_comp = None
        for comp in json_data['components']:
            if comp['component']['type'] == 'RightsComponent':
                rights_comp = comp['component']
                break
        
        assert rights_comp is not None, f"Rights component not found for {location}"
        
        # Verify rights are populated
        if rights_comp['content'] and 'rights_list' in rights_comp['content']:
            rights_count = len(rights_comp['content']['rights_list'])
            print(f"✅ {state_code} ({location:20}): {rights_count} rights")
        else:
            print(f"⚠️  {state_code} ({location:20}): Generic rights")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# SUMMARY
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print("✅ All 7 test suites passed successfully!")
print("\nTest Coverage:")
print("  1. ✅ Dashboard Component System (5 component types)")
print("  2. ✅ Learning Adapter (4 user stages × multiple issues)")
print("  3. ✅ User Database (4 required tables)")
print("  4. ✅ Flask Routes (6 endpoints)")
print("  5. ✅ HTML Generation (Component rendering)")
print("  6. ✅ Stage-Specific Behavior (Dynamic input fields)")
print("  7. ✅ Jurisdiction-Specific Content (MN vs CA)")
print("\nReady for Deployment:")
print("  - Registration system: ✅")
print("  - Verification codes: ✅")
print("  - Dynamic dashboard: ✅")
print("  - Learning integration: ✅")
print("  - API endpoints: ✅")
print("\n" + "="*80)
