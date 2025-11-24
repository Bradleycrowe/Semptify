# Add /admin/status route
lines = open("Semptify.py", "r", encoding="utf-8").readlines()

route_code = '''
@app.route('/admin/status')
def admin_status():
    if not _require_admin_or_401():
        return jsonify({"error": "Unauthorized"}), 401
    from security import get_metrics
    return jsonify({"status": "ok", "metrics": get_metrics()})

'''

# Find admin route and add status after it
for i in range(len(lines)):
    if "def admin():" in lines[i]:
        # Find the end of this function
        j = i + 1
        while j < len(lines) and (lines[j].startswith("    ") or lines[j].strip() == ""):
            j += 1
        lines.insert(j, route_code)
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("Added /admin/status route")
