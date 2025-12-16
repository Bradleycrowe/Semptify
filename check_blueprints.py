import sys
sys.path.insert(0, "C:\\Semptify\\Semptify")

blueprints_to_check = [
    ("complaint_filing_routes", "complaint_filing_bp"),
    ("legal_routes", "legal_bp"),
    ("rent_calculator_routes", "rent_calculator_bp"),
    ("doc_explorer_routes", "doc_explorer_bp"),
    ("calendar_hub_routes", "calendar_hub_bp"),
    ("av_routes", "av_routes_bp"),
    ("journey_routes", "journey_bp"),
    ("maintenance_routes", "maintenance_bp"),
    ("ai_orchestrator_routes", "orchestrator_bp"),
    ("timeline_api_routes", "timeline_api_bp"),
]

print("Checking blueprint imports:\n")
for module, bp_name in blueprints_to_check:
    try:
        mod = __import__(module, fromlist=[bp_name])
        bp = getattr(mod, bp_name)
        print(f"✓ {module}.{bp_name}")
        print(f"  URL Prefix: {bp.url_prefix if hasattr(bp, 'url_prefix') else 'None'}")
    except Exception as e:
        print(f"✗ {module}.{bp_name}: {str(e)[:80]}")
