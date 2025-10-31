import importlib, os, sys
# Ensure repo root is on sys.path so we can import Semptify
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
importlib.invalidate_caches()
app = importlib.import_module('Semptify').app
print('REGISTERED ENDPOINTS:')
for r in sorted(app.url_map.iter_rules(), key=lambda r: r.endpoint):
    print(f"{r.endpoint:40} -> {r}")
print('\nBLUEPRINTS:', list(app.blueprints.keys()))
