# STEP 3: Add latency_stats to metrics
lines = open("Semptify.py", "r", encoding="utf-8").readlines()

for i in range(len(lines)):
    if "return jsonify(get_metrics())" in lines[i]:
        # Replace with enhanced metrics including latency stats
        lines[i] = "    metrics = get_metrics()\n"
        lines.insert(i+1, "    from security import get_latency_stats\n")
        lines.insert(i+2, "    metrics['latency_stats'] = get_latency_stats()\n")
        lines.insert(i+3, "    return jsonify(metrics)\n")
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Step 3: Added latency_stats to metrics")
