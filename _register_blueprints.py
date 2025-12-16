import re

with open('Semptify.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for the location right after Dashboard API
insert_marker = "print('[OK] Dashboard API registered')"

new_blueprints = '''

# Law Library - Tenant rights law database with cross-referencing
try:
    from law_library_routes import law_library_bp
    app.register_blueprint(law_library_bp)
    print("[OK] Law Library registered (/api/law_library/*)")
except ImportError as e:
    print(f"[WARN] Law Library not available: {e}")

# Librarian - AI-powered legal research assistant
try:
    from librarian_routes import librarian_bp
    app.register_blueprint(librarian_bp)
    print("[OK] Librarian AI registered (/api/librarian/*)")
except ImportError as e:
    print(f"[WARN] Librarian AI not available: {e}")

# Document Center - Unified document management with Azure Doc Intelligence
try:
    from document_center_routes import document_center_bp
    app.register_blueprint(document_center_bp)
    print("[OK] Document Center registered (/api/documents/*)")
except ImportError as e:
    print(f"[WARN] Document Center not available: {e}")

# Phone Imports - Call logs, voicemail, text messages
try:
    from phone_import_routes import phone_import_bp
    app.register_blueprint(phone_import_bp)
    print("[OK] Phone Imports registered (/api/phone/*)")
except ImportError as e:
    print(f"[WARN] Phone Imports not available: {e}")

# Help System - Searchable help pages and FAQs
try:
    from help_routes import help_bp
    app.register_blueprint(help_bp)
    print("[OK] Help System registered (/help/*)")
except ImportError as e:
    print(f"[WARN] Help System not available: {e}")
'''

if 'Law Library registered' not in content:
    # Find location after Dashboard API exception handler
    pattern = r"(except NameError:\s+print\('\[WARN\] Dashboard API not available'\))"
    updated = re.sub(pattern, r"\1" + new_blueprints, content, count=1)
    
    with open('Semptify.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print('✓ Registered all new blueprints in Semptify.py')
else:
    print('ℹ️ Blueprints already registered in Semptify.py')
