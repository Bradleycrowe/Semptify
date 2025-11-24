import os
import re

pattern = re.compile(r'''Blueprint\s*\(\s*["']ollama["']''', re.IGNORECASE)
ollama_files = []

for root, dirs, files in os.walk("."):
    if ".venv" in root or "__pycache__" in root or ".git" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if pattern.search(content):
                        ollama_files.append(path)
            except:
                pass

print(f"Found 'ollama' blueprints in {len(ollama_files)} files:")
for f in ollama_files:
    print(f"  - {f}")
