# Fix vault route to render HTML template
import re

with open('vault.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the vault() function's GET handler
old_get = '''    if request.method == 'GET':
        if not uid:
            return jsonify({"error": "unauthorized"}), 401
        return jsonify({"ok": True, "user": uid}), 200'''

new_get = '''    if request.method == 'GET':
        if not uid:
            return jsonify({"error": "unauthorized"}), 401
        documents = _get_user_documents(uid)
        return render_template('vault.html', user_id=uid, documents=documents)'''

if old_get in content:
    content = content.replace(old_get, new_get)
    
    # Make sure render_template is imported
    if 'render_template' not in content[:500]:
        content = content.replace('from flask import Blueprint,', 'from flask import Blueprint, render_template,', 1)
    
    with open('vault.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Fixed vault GET to render HTML template")
else:
    print("✗ Pattern not found - vault.py may have changed")
