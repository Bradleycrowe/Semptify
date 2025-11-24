"""
Complaint Filing Context API Routes
Exposes Context-enhanced complaint filing via REST API.
"""

from flask import Blueprint, request, jsonify
from complaint_filing_context_integration import (
    auto_fill_complaint,
    suggest_evidence,
    generate_context_enhanced_packet
)

complaint_context_api_bp = Blueprint('complaint_context_api', __name__, url_prefix='/api/complaint')


@complaint_context_api_bp.route('/<user_id>/auto-fill', methods=['GET'])
def api_auto_fill(user_id):
    """
    GET /api/complaint/<user_id>/auto-fill
    
    Auto-fill complaint form using Context System.
    Returns all extracted information from user's documents.
    
    Query params:
        issue_type: eviction_defense (default), habitability, discrimination, etc.
    """
    issue_type = request.args.get('issue_type', 'eviction_defense')
    
    try:
        form_data = auto_fill_complaint(user_id, issue_type)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'issue_type': issue_type,
            'form_data': {
                'tenant': {
                    'name': form_data.tenant_name,
                    'phone': form_data.tenant_phone,
                    'email': form_data.tenant_email,
                    'address': form_data.tenant_address
                },
                'landlord': {
                    'name': form_data.landlord_name,
                    'company': form_data.landlord_company,
                    'phone': form_data.landlord_phone,
                    'address': form_data.landlord_address
                },
                'property': {
                    'rental_address': form_data.rental_address,
                    'city': form_data.city,
                    'state': form_data.state,
                    'zip_code': form_data.zip_code
                },
                'financial': {
                    'monthly_rent': form_data.monthly_rent,
                    'security_deposit': form_data.security_deposit,
                    'amount_owed': form_data.amount_owed
                },
                'timeline': {
                    'lease_start_date': form_data.lease_start_date,
                    'lease_end_date': form_data.lease_end_date,
                    'issue_start_date': form_data.issue_start_date,
                    'notice_date': form_data.notice_date
                },
                'issue_description': form_data.issue_description,
                'case_strength': form_data.case_strength,
                'win_probability': form_data.win_probability,
                'key_documents': form_data.key_documents,
                'timeline_events': form_data.timeline_events
            },
            'meta': {
                'data_confidence': form_data.data_confidence,
                'extraction_source': form_data.extraction_source,
                'fields_count': len([f for f in [
                    form_data.tenant_name,
                    form_data.landlord_name,
                    form_data.rental_address,
                    form_data.monthly_rent
                ] if f])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@complaint_context_api_bp.route('/<user_id>/evidence', methods=['GET'])
def api_suggest_evidence(user_id):
    """
    GET /api/complaint/<user_id>/evidence
    
    Get ranked evidence suggestions for complaint filing.
    Returns documents ordered by relevance with perspective scores.
    
    Query params:
        case_type: eviction_defense (default), habitability, etc.
        limit: max number of results (default 10)
    """
    case_type = request.args.get('case_type', 'eviction_defense')
    limit = int(request.args.get('limit', 10))
    
    try:
        evidence = suggest_evidence(user_id, case_type, limit)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'case_type': case_type,
            'total_evidence': len(evidence),
            'evidence': [
                {
                    'document_id': ev.document_id,
                    'filename': ev.filename,
                    'doc_type': ev.doc_type,
                    'relevance_score': ev.relevance_score,
                    'legal_significance': ev.legal_significance,
                    'reason': ev.reason,
                    'perspective_scores': ev.perspective_scores
                }
                for ev in evidence
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@complaint_context_api_bp.route('/<user_id>/packet', methods=['GET'])
def api_generate_packet(user_id):
    """
    GET /api/complaint/<user_id>/packet
    
    Generate complete court packet with Context intelligence.
    Returns comprehensive packet data ready for PDF generation.
    
    Query params:
        case_type: eviction_defense (default), habitability, etc.
    """
    case_type = request.args.get('case_type', 'eviction_defense')
    
    try:
        packet = generate_context_enhanced_packet(user_id, case_type)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'case_type': case_type,
            'packet': packet
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@complaint_context_api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'complaint_context_api',
        'features': [
            'auto_fill_complaint',
            'suggest_evidence',
            'generate_packet'
        ]
    }), 200