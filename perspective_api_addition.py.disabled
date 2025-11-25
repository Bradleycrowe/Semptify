"""
Add to context_api_routes.py:

New endpoint for perspective reasoning analysis.
"""

PERSPECTIVE_ENDPOINT_CODE = '''

@context_api_bp.route('/api/context/<user_id>/document/<doc_id>/perspectives', methods=['GET'])
def get_document_perspectives(user_id, doc_id):
    """
    GET /api/context/<user_id>/document/<doc_id>/perspectives
    
    Returns 4-angle perspective analysis of a document:
    - Tenant perspective (rights, risks, protections)
    - Landlord perspective (enforceability, obligations)
    - Legal perspective (validity, compliance)
    - Judge perspective (likely outcome, evidence)
    
    Returns:
        {
            "tenant_view": {...},
            "landlord_view": {...},
            "legal_view": {...},
            "judge_view": {...},
            "tenant_advantage": -100 to +100,
            "likely_outcome": "string",
            "key_disputed_clauses": [...],
            "settlement_recommendation": "string"
        }
    """
    try:
        # Import perspective engine
        from perspective_reasoning import analyze_perspectives
        from document_intelligence import DocumentIntelligenceEngine
        from pathlib import Path
        
        # Get document path
        doc_path = Path(f"uploads/vault/{user_id}/{doc_id}")
        
        if not doc_path.exists():
            return jsonify({"error": f"Document not found: {doc_id}"}), 404
        
        # Process document with intelligence
        intel_engine = DocumentIntelligenceEngine()
        doc_intel = intel_engine.process_document(str(doc_path))
        
        if not doc_intel:
            return jsonify({"error": "Failed to process document"}), 500
        
        # Analyze from all perspectives
        perspectives = analyze_perspectives(doc_intel)
        
        # Convert to dict
        result = {
            "document_id": doc_id,
            "user_id": user_id,
            "tenant_view": {
                "perspective": perspectives.tenant_view.perspective,
                "overall_score": perspectives.tenant_view.overall_score,
                "win_probability": perspectives.tenant_view.win_probability,
                "favorable_clauses": perspectives.tenant_view.favorable_clauses,
                "unfavorable_clauses": perspectives.tenant_view.unfavorable_clauses,
                "illegal_clauses": perspectives.tenant_view.illegal_clauses,
                "key_strengths": perspectives.tenant_view.key_strengths,
                "key_weaknesses": perspectives.tenant_view.key_weaknesses,
                "action_items": perspectives.tenant_view.action_items
            },
            "landlord_view": {
                "perspective": perspectives.landlord_view.perspective,
                "overall_score": perspectives.landlord_view.overall_score,
                "win_probability": perspectives.landlord_view.win_probability,
                "favorable_clauses": perspectives.landlord_view.favorable_clauses,
                "unfavorable_clauses": perspectives.landlord_view.unfavorable_clauses,
                "key_strengths": perspectives.landlord_view.key_strengths,
                "key_weaknesses": perspectives.landlord_view.key_weaknesses,
                "action_items": perspectives.landlord_view.action_items
            },
            "legal_view": {
                "perspective": perspectives.legal_view.perspective,
                "overall_score": perspectives.legal_view.overall_score,
                "favorable_clauses": perspectives.legal_view.favorable_clauses,
                "unfavorable_clauses": perspectives.legal_view.unfavorable_clauses,
                "illegal_clauses": perspectives.legal_view.illegal_clauses,
                "key_strengths": perspectives.legal_view.key_strengths,
                "key_weaknesses": perspectives.legal_view.key_weaknesses
            },
            "judge_view": {
                "perspective": perspectives.judge_view.perspective,
                "overall_score": perspectives.judge_view.overall_score,
                "favorable_clauses": perspectives.judge_view.favorable_clauses,
                "unfavorable_clauses": perspectives.judge_view.unfavorable_clauses,
                "key_strengths": perspectives.judge_view.key_strengths,
                "key_weaknesses": perspectives.judge_view.key_weaknesses,
                "action_items": perspectives.judge_view.action_items
            },
            "comparative_analysis": {
                "tenant_advantage": perspectives.tenant_advantage,
                "likely_outcome": perspectives.likely_outcome,
                "key_disputed_clauses": perspectives.key_disputed_clauses,
                "settlement_recommendation": perspectives.settlement_recommendation
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''

print("=" * 70)
print("PERSPECTIVE API ENDPOINT CODE READY")
print("=" * 70)
print("\nAdd this to context_api_routes.py:")
print(PERSPECTIVE_ENDPOINT_CODE)
