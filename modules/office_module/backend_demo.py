"""
Flask blueprint demo for Office module minimal endpoints:
- /api/rooms
- /api/rooms/create
- /api/rooms/<id>/token
- /api/documents endpoints (list, upload/init, complete, lock, annotate)

This demo uses in-memory stores and is suitable for local testing only. To wire into SemptifyGUI.py,
register the blueprint: app.register_blueprint(office_bp)
"""
from flask import Blueprint, jsonify, request
import uuid
import time

office_bp = Blueprint('office', __name__)

ROOMS = {}
DOCUMENTS = {}

@office_bp.route('/api/rooms', methods=['GET'])
def list_rooms():
    return jsonify(list(ROOMS.values()))

@office_bp.route('/api/rooms/create', methods=['POST'])
def create_room():
    data = request.get_json() or {}
    room_id = str(uuid.uuid4())
    room = {
        'id': room_id,
        'type': data.get('type','open'),
        'host_id': None,
        'created_at': int(time.time()),
        'expires_at': int(time.time()) + int(data.get('expires_in',3600))
    }
    ROOMS[room_id] = room
    return jsonify(room)

@office_bp.route('/api/rooms/<room_id>/token', methods=['POST'])
def room_token(room_id):
    if room_id not in ROOMS:
        return jsonify({'error':'not found'}), 404
    token = str(uuid.uuid4())
    return jsonify({'token': token})

@office_bp.route('/api/documents', methods=['GET'])
def list_documents():
    return jsonify(list(DOCUMENTS.values()))

@office_bp.route('/api/documents/upload/init', methods=['POST'])
def init_upload():
    data = request.get_json() or {}
    doc_id = str(uuid.uuid4())
    # In a real setup you'd generate a pre-signed URL; for demo we return a local PUT target
    upload_url = f"/api/documents/upload/{doc_id}"
    DOCUMENTS[doc_id] = {
        'id': doc_id,
        'filename': data.get('filename'),
        'sha256': data.get('sha256'),
        'uploaded': False,
        'uploaded_at': None
    }
    return jsonify({'uploadUrl': upload_url, 'id': doc_id})

@office_bp.route('/api/documents/upload/<doc_id>', methods=['PUT'])
def upload_put(doc_id):
    if doc_id not in DOCUMENTS:
        return jsonify({'error':'not found'}), 404
    # store content in memory is not practical; we mark as uploaded
    DOCUMENTS[doc_id]['uploaded'] = True
    DOCUMENTS[doc_id]['uploaded_at'] = int(time.time())
    return '', 204

@office_bp.route('/api/documents/<doc_id>/complete', methods=['POST'])
def complete_upload(doc_id):
    if doc_id not in DOCUMENTS:
        return jsonify({'error':'not found'}), 404
    DOCUMENTS[doc_id]['complete'] = True
    return jsonify({'id': doc_id})

@office_bp.route('/api/documents/<doc_id>/lock', methods=['POST'])
def lock_document(doc_id):
    if doc_id not in DOCUMENTS:
        return jsonify({'error':'not found'}), 404
    DOCUMENTS[doc_id]['locked_at'] = int(time.time())
    return jsonify({'id': doc_id})

@office_bp.route('/api/documents/<doc_id>/annotate', methods=['POST'])
def annotate(doc_id):
    if doc_id not in DOCUMENTS:
        return jsonify({'error':'not found'}), 404
    data = request.get_json() or {}
    if 'annotations' not in DOCUMENTS[doc_id]:
        DOCUMENTS[doc_id]['annotations'] = []
    DOCUMENTS[doc_id]['annotations'].append({'text': data.get('text'),'timecode': data.get('timecode')})
    return jsonify({'ok': True})
