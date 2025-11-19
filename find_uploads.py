import os
import re

print("=== SEARCHING FOR VAULT UPLOAD FUNCTIONS ===\n")

patterns = [
    (r'def\s+(notary_upload|vault_upload|witness_save|packet_save)\s*\(', 'Upload functions'),
    (r'\.save\(.*\)', 'File save operations'),
    (r'cert\.json|certificate', 'Certificate creation'),
    (r'@.*route.*upload', 'Upload routes')
]

for root, dirs, files in os.walk('.'):
    # Skip venv and __pycache__
    dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'node_modules']]
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                for pattern, desc in patterns:
                    for i, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            print(f"{file}:{i} [{desc}]")
                            print(f"  {line.strip()[:80]}")
                            
            except Exception as e:
                pass

print("\n=== DONE ===")
