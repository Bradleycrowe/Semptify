lines = open("Semptify.py", "r", encoding="utf-8").readlines()

blueprint_code = """
try:
    from register import register_bp
    app.register_blueprint(register_bp)
    print('[OK] Registration blueprint registered')
except ImportError as e:
    print(f'[WARN] Registration blueprint not available: {e}')

try:
    from vault import vault_bp
    app.register_blueprint(vault_bp)
    print('[OK] Vault blueprint registered')
except ImportError as e:
    print(f'[WARN] Vault blueprint not available: {e}')

"""

# Insert after line 74 (index 73) - "Add more blueprint registrations here..."
lines.insert(74, blueprint_code)

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Added register_bp and vault_bp registrations")
