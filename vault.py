# vault.py - Document Vault with user token authentication
# Clean rewrite - no duplicate code, proper token validation

import os
import json
import hashlib
import secrets
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template_string

vault_bp = Blueprint('vault', __name__)

# Simple HTML template for vault page
VAULT_TEMPLATE = '''<!DOCTYPE html>
<html><head><title>Document Vault</title></head>
<body>
<h1>Document Vault</h1>
<p>Welcome, user {{ user_id }}</p>
<form action="/vault/upload" method="post" enctype="multipart/form-data">
    <input type="hidden" name="user_token" value="{{ token }}">
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
</form>
<h2>Your Documents</h2>
<ul>
{% for doc in documents %}
<li>{{ doc }}</li>
{% else %}
<li>No documents yet</li>
{% endfor %}
</ul>
</body></html>
'''


def _get_upload_root():
    """Get upload root based on current working directory."""
    return os.path.join(os.getcwd(), "uploads", "vault")


def _get_user_dir(user_id):
    """Get user's upload directory."""
    return os.path.join(_get_upload_root(), user_id)


def _validate_token(token):
    """Validate user token and return user_id or None."""
    if not token:
        return None
    
    # Import here to avoid circular imports and get fresh reference
    from security import validate_user_token
    result = validate_user_token(token)
    
    # Handle bool result (from open mode)
    if isinstance(result, bool):
        return None
    return result


def _get_token_from_request():
    """Extract token from request (query param, header, cookie, or form)."""
    # Check Authorization: Bearer header first (session tokens)
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    # Check session token header
    session_token = request.headers.get('X-Session-Token')
    if session_token:
        return session_token
    
    # Check cookie
    cookie_token = request.cookies.get('semptify_session')
    if cookie_token:
        return cookie_token
    
    # Fall back to query params and form (permanent tokens)
    return (
        request.args.get('user_token') or
        request.args.get('token') or
        request.headers.get('X-User-Token') or
        request.form.get('user_token')
    )


@vault_bp.route('/vault', methods=['GET', 'POST'])
def vault_index():
    """Main vault page - requires user token."""
    token = _get_token_from_request()
    user_id = _validate_token(token)
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    # List user's documents
    user_dir = _get_user_dir(user_id)
    documents = []
    if os.path.isdir(user_dir):
        documents = [f for f in os.listdir(user_dir) if not f.endswith('.cert.json')]
    
    return render_template_string(VAULT_TEMPLATE, 
                                   user_id=user_id, 
                                   token=token,
                                   documents=documents)


@vault_bp.route('/vault/upload', methods=['POST'])
def upload():
    """Upload a file to user's vault."""
    token = _get_token_from_request()
    user_id = _validate_token(token)
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "no file provided"}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "no filename"}), 400
    
    # Secure the filename
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    
    # Create user directory
    user_dir = _get_user_dir(user_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Save file
    filepath = os.path.join(user_dir, filename)
    file.save(filepath)
    
    # Create certificate
    with open(filepath, 'rb') as f:
        content = f.read()
    
    cert = {
        "filename": filename,
        "sha256": hashlib.sha256(content).hexdigest(),
        "ts": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "request_id": secrets.token_hex(8)
    }
    
    cert_path = filepath + ".cert.json"
    with open(cert_path, 'w') as f:
        json.dump(cert, f, indent=2)
    
    return jsonify({"status": "uploaded", "filename": filename, "cert": cert}), 200


@vault_bp.route('/vault/list', methods=['GET'])
def list_documents():
    """List all documents for user."""
    token = _get_token_from_request()
    user_id = _validate_token(token)
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    user_dir = _get_user_dir(user_id)
    documents = []
    
    if os.path.isdir(user_dir):
        for f in os.listdir(user_dir):
            if not f.endswith('.cert.json'):
                documents.append({"filename": f})
    
    return jsonify({"documents": documents}), 200


@vault_bp.route('/vault/download', methods=['GET'])
def download():
    """Download a file from vault."""
    token = _get_token_from_request()
    user_id = _validate_token(token)
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "filename required"}), 400
    
    from werkzeug.utils import secure_filename
    filename = secure_filename(filename)
    
    filepath = os.path.join(_get_user_dir(user_id), filename)
    if not os.path.isfile(filepath):
        return jsonify({"error": "not found"}), 404
    
    from flask import send_file
    return send_file(filepath, as_attachment=True)
