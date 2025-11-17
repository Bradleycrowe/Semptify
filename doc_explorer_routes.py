# doc_explorer_routes.py
from flask import Blueprint, render_template, jsonify, request, send_file
from doc_explorer_engine import SemptifyDocExplorer, generate_documentation
from pathlib import Path

doc_explorer_bp = Blueprint('doc_explorer', __name__, url_prefix='/docs')
explorer = SemptifyDocExplorer()

@doc_explorer_bp.route('/')
def docs_home():
    return render_template('doc_explorer/index.html')

@doc_explorer_bp.route('/overview')
def docs_overview():
    features = explorer.get_feature_map()
    navigation = explorer.get_navigation_structure()
    return render_template('doc_explorer/overview.html', features=features, navigation=navigation)

@doc_explorer_bp.route('/features')
def docs_features():
    features = explorer.get_feature_map()
    return render_template('doc_explorer/features.html', features=features)

@doc_explorer_bp.route('/features/<feature_name>')
def docs_feature_detail(feature_name):
    features = explorer.get_feature_map()
    feature = features.get(feature_name)
    if not feature:
        return "Feature not found", 404
    return render_template('doc_explorer/feature_detail.html', feature_name=feature_name, feature=feature)

@doc_explorer_bp.route('/search')
def docs_search():
    query = request.args.get('q', '').lower()
    if not query:
        return render_template('doc_explorer/search.html', results=[], query='')
    
    doc = explorer.scan_application()
    features = explorer.get_feature_map()
    results = []
    
    for feature_name, feature_data in features.items():
        if query in feature_name.lower() or query in feature_data['description'].lower():
            results.append({
                "type": "Feature",
                "name": feature_name,
                "description": feature_data['description'],
                "link": f"/docs/features/{feature_name}",
                "icon": feature_data['icon']
            })
    
    for component_type in ['blueprints', 'routes', 'apis']:
        for component in doc.get(component_type, []):
            component_name = component.get('name', '')
            docstring = component.get('docstring', '') or ''
            if query in component_name.lower() or query in docstring.lower():
                results.append({
                    "type": component_type.capitalize(),
                    "name": component_name,
                    "description": docstring[:200] if docstring else "No description",
                    "link": f"/docs/component/{component_name}",
                    "icon": "📦"
                })
    
    return render_template('doc_explorer/search.html', results=results, query=query)

@doc_explorer_bp.route('/api/generate')
def api_generate_docs():
    try:
        result = generate_documentation()
        return jsonify({"status": "success", "message": "Documentation generated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@doc_explorer_bp.route('/api/export')
def api_export_docs():
    try:
        doc_file = Path(__file__).parent / "data" / "documentation.json"
        if not doc_file.exists():
            generate_documentation()
        return send_file(doc_file, as_attachment=True, download_name="semptify_documentation.json")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@doc_explorer_bp.route('/journey')
def docs_journey():
    """Interactive tenant journey guide"""
    try:
        from tenant_journey import TenantJourney
        journey_sys = TenantJourney()
        stages = journey_sys.JOURNEY_STAGES
    except:
        stages = ["searching", "applying", "screening", "approved", "signing", 
                 "moving_in", "living", "issue", "resolving", "moving_out", "dispute", "closed"]
    
    journey_info = {
        "searching": {"title": "🔍 Searching for Housing", "desc": "Find apartments, research landlords", "features": ["Housing Programs", "Attorney Finder"]},
        "applying": {"title": "📝 Applying", "desc": "Submit applications, track responses", "features": ["Document Vault", "Timeline"]},
        "screening": {"title": "🔎 Screening", "desc": "Background checks, credit reports", "features": ["Document Vault", "User Management"]},
        "approved": {"title": "✅ Approved", "desc": "Application accepted", "features": ["Timeline", "Calendar"]},
        "signing": {"title": "✍️ Signing Lease", "desc": "Review and sign lease agreement", "features": ["Document Vault", "AI Assistant"]},
        "moving_in": {"title": "📦 Moving In", "desc": "Move-in inspection, security deposit", "features": ["Document Vault", "Rent & Ledger"]},
        "living": {"title": "🏠 Living", "desc": "Day-to-day tenancy, paying rent", "features": ["Rent & Ledger", "Document Vault", "Communication"]},
        "issue": {"title": "⚠️ Issue Arises", "desc": "Problems with unit or landlord", "features": ["Document Vault", "AI Assistant", "Learning System"]},
        "resolving": {"title": "🔧 Resolving", "desc": "Working on resolution", "features": ["Communication", "Attorney Finder", "AI Assistant"]},
        "moving_out": {"title": "📤 Moving Out", "desc": "End of tenancy, final inspection", "features": ["Document Vault", "Rent & Ledger"]},
        "dispute": {"title": "⚖️ Dispute", "desc": "Post-move-out disputes", "features": ["Legal Complaint Filing", "Attorney Finder", "Document Vault"]},
        "closed": {"title": "🎉 Journey Complete", "desc": "Case resolved", "features": ["Timeline"]}
    }
    return render_template('doc_explorer/journey.html', stages=stages, journey_info=journey_info)
