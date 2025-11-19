"""
Document Vault - User Storage Only
All uploads/downloads go to user's Google Drive or Dropbox .semptify/ folder
No server-side storage of documents
"""
from flask import Blueprint, request, jsonify, g, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import os

vault_bp = Blueprint('vault', __name__)

USE_USER_STORAGE = os.getenv('USE_USER_STORAGE', '1') == '1'

def _require_storage():
    """Ensure user has storage connected and authorized"""
    if not hasattr(g, 'storage_client') or not g.storage_client:
        return {'error': 'Storage not connected. Please connect Google Drive or Dropbox.'}, 401
    if not hasattr(g, 'user_token') or not g.user_token:
        return {'error': 'Not authorized. Please provide your token.'}, 401
    return None

@vault_bp.route('/vault', methods=['GET'])
def vault_home():
    """Vault homepage"""
    err = _require_storage()
    if err:
        return render_template('vault_setup_required.html'), 401
    
    return render_template('vault.html', user_token=g.user_token, storage_type=g.storage_type)

@vault_bp.route('/vault/upload', methods=['POST'])
def upload_document():
    """Upload document to user's storage"""
    if not USE_USER_STORAGE:
        return jsonify({'error': 'User storage mode not enabled'}), 500
    
    err = _require_storage()
    if err:
        return jsonify(err[0]), err[1]
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    filename = secure_filename(file.filename)
    file_content = file.read()
    
    # Upload to user's storage under docs/
    doc_path = f'docs/{filename}'
    g.storage_client.upload(doc_path, file_content)
    
    # Create metadata entry
    metadata = {
        'filename': filename,
        'uploaded': datetime.utcnow().isoformat() + 'Z',
        'size': len(file_content),
        'content_type': file.content_type
    }
    
    # Load and update docs index
    try:
        index_data = g.storage_client.download('docs_index.json')
        docs_index = json.loads(index_data.decode() if isinstance(index_data, bytes) else index_data)
    except:
        docs_index = {'documents': []}
    
    docs_index['documents'].append(metadata)
    docs_index['last_modified'] = datetime.utcnow().isoformat() + 'Z'
    
    g.storage_client.upload('docs_index.json', json.dumps(docs_index, indent=2))
    
    return jsonify({'success': True, 'filename': filename, 'storage': g.storage_type})

@vault_bp.route('/vault/list', methods=['GET'])
def list_documents():
    """List documents in user's storage"""
    if not USE_USER_STORAGE:
        return jsonify({'error': 'User storage mode not enabled'}), 500
    
    err = _require_storage()
    if err:
        return jsonify(err[0]), err[1]
    
    try:
        index_data = g.storage_client.download('docs_index.json')
        docs_index = json.loads(index_data.decode() if isinstance(index_data, bytes) else index_data)
        return jsonify(docs_index)
    except FileNotFoundError:
        return jsonify({'documents': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vault_bp.route('/vault/download/<filename>', methods=['GET'])
def download_document(filename):
    """Download document from user's storage"""
    if not USE_USER_STORAGE:
        return jsonify({'error': 'User storage mode not enabled'}), 500
    
    err = _require_storage()
    if err:
        return jsonify(err[0]), err[1]
    
    try:
        filename = secure_filename(filename)
        doc_path = f'docs/{filename}'
        file_content = g.storage_client.download(doc_path)
        
        from flask import Response
        return Response(file_content, mimetype='application/octet-stream', headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        })
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
