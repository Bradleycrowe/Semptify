# Remove duplicate ollama_bp registration
with open("Semptify.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

seen_ollama = False
new_lines = []

for i, line in enumerate(lines):
    # If this is an ollama line and we've already seen one, skip it
    if "ollama_routes" in line and "ollama_bp" in line:
        if seen_ollama:
            print(f"Skipping duplicate at line {i+1}: {line.strip()}")
            continue
        else:
            seen_ollama = True
    new_lines.append(line)

with open("Semptify.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✓ Removed duplicate ollama_bp registration")
