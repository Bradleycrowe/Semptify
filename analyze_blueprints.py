# Analyze blueprints: defined vs registered
import os, re

# Find all blueprint definitions
blueprints_defined = {}
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(r'(\w+)\s*=\s*Blueprint\([\'"](\w+)[\'"]', content)
                    for var_name, bp_name in matches:
                        blueprints_defined[var_name] = (path, bp_name)
            except:
                pass

# Find what's registered in Semptify.py
registered = []
try:
    with open('Semptify.py', 'r', encoding='utf-8') as f:
        content = f.read()
        registered = re.findall(r'app\.register_blueprint\((\w+)\)', content)
except:
    pass

print(f"=== BLUEPRINTS DEFINED: {len(blueprints_defined)} ===")
for bp, (path, name) in sorted(blueprints_defined.items())[:30]:
    reg = "✓ REGISTERED" if bp in registered else "✗ NOT REGISTERED"
    print(f"{reg}: {bp:30s} in {path}")

print(f"\n=== REGISTERED IN SEMPTIFY.PY: {len(set(registered))} ===")
for bp in sorted(set(registered)):
    if bp not in blueprints_defined:
        print(f"⚠️  {bp} (not found in scan)")
    else:
        print(f"✓  {bp}")
