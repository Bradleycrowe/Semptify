lines = open("Semptify.py", "r", encoding="utf-8").readlines()
seen = set()
new_lines = []
for line in lines:
    if "learning_dashboard_routes" in line and "learning_dashboard_routes" in seen:
        continue  # Skip duplicate
    if "learning_dashboard_routes" in line:
        seen.add("learning_dashboard_routes")
    new_lines.append(line)
open("Semptify.py", "w", encoding="utf-8").writelines(new_lines)
print("Removed duplicate learning_dashboard")
