# Find all blueprint name collisions
import re
from collections import defaultdict

blueprints = defaultdict(list)

# Scan all Python files for Blueprint definitions
import os
for root, dirs, files in os.walk('.'):
    if '.venv' in root or 'backup' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find Blueprint("name", ...)
                    matches = re.findall(r'Blueprint\([\'"](\w+)[\'"]', content)
                    for bp_name in matches:
                        blueprints[bp_name].append(path)
            except:
                pass

print("=== BLUEPRINT NAME COLLISIONS ===")
for name, paths in sorted(blueprints.items()):
    if len(paths) > 1:
        print(f"\n'{name}' defined in {len(paths)} files:")
        for p in paths:
            print(f"  - {p}")
