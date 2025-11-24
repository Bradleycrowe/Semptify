# Find major feature modules
import os

features = {}
for root, dirs, files in os.walk('.'):
    # Skip backups and __pycache__
    if 'backup' in root or '__pycache__' in root or '.venv' in root:
        continue
    for file in files:
        if file.endswith('_routes.py') or file.endswith('_bp.py'):
            feature = file.replace('_routes.py', '').replace('_bp.py', '')
            path = os.path.join(root, file).replace('.\\', '')
            features[feature] = path

print(f"=== MAJOR FEATURES ({len(features)}) ===")
for name, path in sorted(features.items())[:40]:
    print(f"{name:35s} -> {path}")
