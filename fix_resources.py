# Fix resource_download in Semptify.py
with open('Semptify.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def resource_download(filename):
    \'\'\'Download resource templates\'\'\'
    return jsonify({"error": "not found"}), 404'''

new = '''def resource_download(filename):
    \'\'\'Download resource templates\'\'\'
    from werkzeug.utils import secure_filename
    safe_name = secure_filename(filename)
    resource_path = os.path.join(os.path.dirname(__file__), 'resources', safe_name)
    if os.path.exists(resource_path):
        return send_file(resource_path, mimetype='text/plain', as_attachment=False)
    return jsonify({"error": "not found"}), 404'''

content = content.replace(old, new)

with open('Semptify.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed resource_download')
