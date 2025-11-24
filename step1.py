# STEP 1: Register all remaining blueprints
registration_code = """
    # Additional Feature Blueprints
    ('learning_dashboard_routes', 'learning_dashboard_bp'),
    ('ledger_tracking_routes', 'ledger_tracking_bp'),
    ('ledger_admin_routes', 'ledger_admin_bp'),
    ('ledger_calendar_routes', 'ledger_calendar_bp'),
    ('av_routes', 'av_routes_bp'),
    ('ollama_routes', 'ollama_bp'),
    ('brad_integration_routes', 'integration_bp'),
    ('ai_orchestrator_routes', 'orchestrator_bp'),
    ('maintenance_routes', 'maintenance_bp'),
    ('migration_routes', 'migration_bp'),
    ('feature_admin_routes', 'feature_admin_bp'),
    ('doc_explorer_routes', 'doc_explorer_bp'),
    ('route_discovery_routes', 'route_discovery_bp'),
"""

lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Find the blueprints_to_register list and expand it
for i in range(len(lines)):
    if "blueprints_to_register = [" in lines[i]:
        # Find the closing bracket
        j = i + 1
        while j < len(lines) and ']' not in lines[j]:
            j += 1
        # Insert before the closing bracket
        lines.insert(j, registration_code)
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Step 1: Added 13 more blueprints to registration")
