# Remove duplicate /vault route from Semptify.py
lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Find and remove @app.route('/vault') and the function
new_lines = []
skip_next = 0
for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    if "@app.route('/vault')" in line:
        # Skip this line and next 2 (def vault(): and return)
        skip_next = 2
        continue
    new_lines.append(line)

open("Semptify.py", "w", encoding="utf-8").writelines(new_lines)
print("✓ Removed duplicate /vault route")
