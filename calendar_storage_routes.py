"""
Calendar Routes - Enhanced with Vault Storage
Users add events through calendar → automatically stored in vault
"""
from flask import Blueprint, render_template, request, jsonify
from calendar_vault_bridge import CalendarVaultBridge
from security import validate_user_token
import json

calendar_storage_bp = Blueprint('calendar_storage', __name__)
bridge = CalendarVaultBridge()

@calendar_storage_bp.route('/calendar', methods=['GET'])
def calendar_view():
    '''Calendar interface for adding events + documents'''
    return render_template('calendar_vault/calendar_input.html')

@calendar_storage_bp.route('/api/calendar/add-event', methods=['POST'])
def add_event_with_storage():
    '''
    Add event to calendar AND store in vault
    
    POST /api/calendar/add-event
    Body: {
        user_token: str,
        title: str,
        description: str,
        event_date: str (ISO format),
        event_type: str,
        files: [] (optional file uploads)
    }
    '''
    user_token = request.form.get('user_token') or request.json.get('user_token')
    
    if not user_token or not validate_user_token(user_token):
        return jsonify({'error': 'Invalid user token'}), 401
    
    # Get event data
    event_data = {
        'title': request.form.get('title') or request.json.get('title'),
        'description': request.form.get('description') or request.json.get('description'),
        'event_date': request.form.get('event_date') or request.json.get('event_date'),
        'event_type': request.form.get('event_type', 'general') or request.json.get('event_type', 'general')
    }
    
    # Handle file uploads (store in vault)
    document_ids = []
    if 'files' in request.files:
        from vault import _file_path, _cert_path, _sha256_of_file
        import os
        from datetime import datetime
        
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename:
                # Save to vault
                user_dir = os.path.join('uploads', 'vault', user_token)
                os.makedirs(user_dir, exist_ok=True)
                
                # Generate document ID
                timestamp = datetime.utcnow().isoformat().replace(':', '').replace('-', '').replace('.', '')
                doc_id = f"doc_{timestamp}_{file.filename}"
                
                # Save file
                file_path = os.path.join(user_dir, doc_id)
                file.save(file_path)
                
                # Create certificate
                cert = {
                    'doc_id': doc_id,
                    'filename': file.filename,
                    'sha256': _sha256_of_file(file_path),
                    'timestamp': datetime.utcnow().isoformat(),
                    'uploaded_via': 'calendar',
                    'event_title': event_data['title']
                }
                
                cert_file = os.path.join(user_dir, f'{doc_id}.cert.json')
                with open(cert_file, 'w', encoding='utf-8') as f:
                    json.dump(cert, f, indent=2)
                
                document_ids.append(doc_id)
    
    # Catalog event with documents
    try:
        catalog_entry = bridge.catalog_event_with_documents(
            user_id=user_token,
            event_data=event_data,
            document_ids=document_ids
        )
        
        # Trigger curiosity: What should user do next?
        try:
            question = on_calendar_event_added(user_token, event_data)
            if question:
                print(f'[CURIOSITY] {question}')
        except Exception as e:
            print(f'[WARN] Curiosity hook failed: {e}')
                return jsonify({
            'ok': True,
            'message': f'Event stored with {len(document_ids)} document(s)',
            'event_id': catalog_entry['event_id'],
            'documents': document_ids
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@calendar_storage_bp.route('/timeline', methods=['GET'])
def timeline_viewer():
    '''Lightweight viewer for vault contents'''
    user_token = request.args.get('user_token')
    view = request.args.get('view', 'month')
    
    return render_template('calendar_vault/timeline_viewer.html', 
                         user_token=user_token,
                         view=view)
