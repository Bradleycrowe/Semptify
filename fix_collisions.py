# Fix blueprint name collisions by renaming duplicates
import os

fixes = [
    # learning_dashboard collision - rename the API one
    ('learning_dashboard_api.py', 'learning_dashboard', 'learning_dashboard_api'),
    # attorney_finder - use the one in routes/ folder
    ('attorney_finder_routes.py', 'attorney_finder', 'attorney_finder_main'),
    # register - use register.py, rename register_new.py
    ('register_new.py', 'register', 'register_new'),
    # rent_calculator - use the one in root
    ('routes\\rent_calculator_routes.py', 'rent_calculator', 'rent_calculator_alt'),
    # vault - use vault.py (vault_blueprint), rename blueprints/vault_bp.py
    ('blueprints\\vault_bp.py', 'vault', 'vault_bp_alt'),
]

for filepath, old_name, new_name in fixes:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace Blueprint("old_name" with Blueprint("new_name"
            content = content.replace(f'Blueprint("{old_name}"', f'Blueprint("{new_name}"')
            content = content.replace(f"Blueprint('{old_name}'", f"Blueprint('{new_name}'")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {filepath}: {old_name} -> {new_name}")
        except Exception as e:
            print(f"✗ Error fixing {filepath}: {e}")
    else:
        print(f"⚠ File not found: {filepath}")

print("\n✓ Blueprint collision fixes complete")
