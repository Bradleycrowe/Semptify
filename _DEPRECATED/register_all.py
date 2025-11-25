# Create comprehensive blueprint registration
registration_code = """
# ============================================================================
# BLUEPRINT REGISTRATION - Auto-discover and register available blueprints
# ============================================================================

# Core Features
blueprints_to_register = [
    ('calendar_api', 'calendar_api_bp'),
    ('calendar_hub_routes', 'calendar_hub_bp'),
    ('calendar_master', 'calendar_master_bp'),
    ('calendar_storage_routes', 'calendar_storage_bp'),
    ('calendar_timeline_routes', 'calendar_timeline_bp'),
    ('calendar_vault_api', 'calendar_vault_api'),
    ('calendar_vault_ui_routes', 'calendar_vault_ui_bp'),
    ('complaint_filing_routes', 'complaint_filing_bp'),
    ('data_flow_routes', 'data_flow_bp'),
    ('legal_routes', 'legal_bp'),
    ('ledger_routes', 'ledger_bp'),
    ('learning_routes', 'learning_bp'),
    ('learning_dashboard_routes', 'learning_dashboard_bp'),
    ('ollama_routes', 'ollama_bp'),
    ('brad_gui_routes', 'brad_bp'),
    ('help_hub_routes', 'help_hub_bp'),
    ('improvement_routes', 'improvement_bp'),
    ('journey_routes', 'journey_bp'),
    ('housing_programs_routes', 'housing_programs_bp'),
    ('attorney_finder_routes', 'attorney_finder_bp'),
    ('demo_routes', 'demo_bp'),
    ('library_routes', 'library_bp'),
    ('library_hub_routes', 'library_hub_bp'),
    ('main_dashboard_routes', 'main_dashboard_bp'),
    ('modern_gui_routes', 'modern_gui_bp'),
]

for module_name, bp_name in blueprints_to_register:
    try:
        module = __import__(module_name, fromlist=[bp_name])
        bp = getattr(module, bp_name)
        app.register_blueprint(bp)
        print(f'[OK] {bp_name} registered')
    except (ImportError, AttributeError) as e:
        print(f'[SKIP] {bp_name}: {e}')

"""

lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Find where vault_bp is registered and add after it
for i in range(len(lines)):
    if "from vault import vault_bp" in lines[i]:
        # Find the except block end
        j = i
        while j < len(lines) and 'except' not in lines[j]:
            j += 1
        while j < len(lines) and (lines[j].startswith('    ') or 'except' in lines[j] or 'print' in lines[j]):
            j += 1
        lines.insert(j, '\n' + registration_code)
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Added comprehensive blueprint registration")
