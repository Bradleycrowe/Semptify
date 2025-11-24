lines = open("Semptify.py", "r", encoding="utf-8").readlines()
lines[87:93] = [
    "@app.route('/admin')\n",
    "def admin():\n",
    "    if not _require_admin_or_401():\n",
    '        return jsonify({"error": "Unauthorized"}), 401\n',
    "    return render_template('admin.html')\n",
    "\n"
]
open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("Fixed")
