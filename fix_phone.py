# Fix phone_import_routes.py to include import_id in responses
import re

with open('phone_import_routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import_id generation at the top (after imports)
if 'import secrets' not in content:
    content = content.replace('import json', 'import json\nimport secrets')

# Fix call_logs response
content = content.replace(
    """return jsonify({
        'message': 'Call logs uploaded and notarized',
        'filename': filename,
        'notary_certificate': cert
    }), 201""",
    """return jsonify({
        'message': 'Call logs uploaded and notarized',
        'filename': filename,
        'import_id': secrets.token_hex(8),
        'notary_certificate': cert
    }), 201"""
)

# Fix voicemail response
content = content.replace(
    """return jsonify({
        'message': 'Voicemail uploaded and notarized',
        'filename': filename,
        'notary_certificate': cert
    }), 201""",
    """return jsonify({
        'message': 'Voicemail uploaded and notarized',
        'filename': filename,
        'import_id': secrets.token_hex(8),
        'notary_certificate': cert
    }), 201"""
)

# Fix texts response
content = content.replace(
    """return jsonify({
        'message': 'Text messages uploaded and notarized',
        'filename': filename,
        'notary_certificate': cert
    }), 201""",
    """return jsonify({
        'message': 'Text messages uploaded and notarized',
        'filename': filename,
        'import_id': secrets.token_hex(8),
        'notary_certificate': cert
    }), 201"""
)

with open('phone_import_routes.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed phone_import_routes.py')
