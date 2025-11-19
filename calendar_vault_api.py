'''
Calendar API with Vault Integration
Adds endpoints for cataloging events with documents
'''
from flask import Blueprint, request, jsonify
from calendar_vault_bridge import CalendarVaultBridge
from security import validate_user_token

calendar_vault_api = Blueprint('calendar_vault_api', __name__)
bridge = CalendarVaultBridge()

@calendar_vault_api.route('/api/calendar/catalog-event', methods=['POST'])
def catalog_event():
    '''
    Catalog an event with its associated documents
    
    POST /api/calendar/catalog-event
    Body: {
        user_token: str,
        event: {title, description, event_date, event_type},
        document_ids: [str]
    }
    '''
    data = request.get_json()
    
    # Validate user
    user_token = data.get('user_token')
    if not user_token or not validate_user_token(user_token):
        return jsonify({'error': 'Invalid user token'}), 401
    
    event_data = data.get('event', {})
    document_ids = data.get('document_ids', [])
    
    try:
        catalog_entry = bridge.catalog_event_with_documents(
            user_id=user_token,
            event_data=event_data,
            document_ids=document_ids
        )
        return jsonify({
            'ok': True,
            'catalog_entry': catalog_entry,
            'message': 'Event cataloged with documents'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@calendar_vault_api.route('/api/calendar/chronological', methods=['GET'])
def get_chronological():
    '''
    Get chronological view of events + documents
    
    GET /api/calendar/chronological?user_token=xxx&view=day|week|month|year
    '''
    user_token = request.args.get('user_token')
    if not user_token or not validate_user_token(user_token):
        return jsonify({'error': 'Invalid user token'}), 401
    
    view_type = request.args.get('view', 'day')
    
    try:
        chronological_data = bridge.get_chronological_view(user_token, view_type)
        return jsonify({
            'ok': True,
            'view_type': view_type,
            'data': chronological_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@calendar_vault_api.route('/api/calendar/event/<event_id>/documents', methods=['GET'])
def get_event_documents(event_id):
    '''Get all documents associated with an event'''
    user_token = request.args.get('user_token')
    if not user_token or not validate_user_token(user_token):
        return jsonify({'error': 'Invalid user token'}), 401
    
    # TODO: Implement event document lookup
    return jsonify({
        'ok': True,
        'event_id': event_id,
        'documents': []
    }), 200
