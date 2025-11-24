# Fix metrics endpoint
lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Find metrics route (around line 130)
for i in range(len(lines)):
    if lines[i].strip() == "@app.route('/metrics')":
        # Replace the next 2 lines (def and return)
        lines[i+1] = "def metrics():\n"
        lines[i+2] = '    from security import get_metrics\n'
        lines.insert(i+3, '    format_type = request.args.get("format", "json")\n')
        lines.insert(i+4, '    accept = request.headers.get("Accept", "")\n')
        lines.insert(i+5, '    if "text/plain" in accept or format_type == "prometheus":\n')
        lines.insert(i+6, '        # Return Prometheus format\n')
        lines.insert(i+7, '        metrics_data = get_metrics()\n')
        lines.insert(i+8, '        output = []\n')
        lines.insert(i+9, '        for key, value in metrics_data.items():\n')
        lines.insert(i+10, '            if isinstance(value, (int, float)):\n')
        lines.insert(i+11, '                output.append(f"{key} {value}")\n')
        lines.insert(i+12, '        return Response("\\n".join(output), mimetype="text/plain; charset=utf-8")\n')
        lines.insert(i+13, '    return jsonify(get_metrics())\n')
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Fixed metrics endpoint")
