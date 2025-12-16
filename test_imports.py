try:
    from calendar_hub_routes import calendar_hub_bp
    print("✓ calendar_hub_bp")
except Exception as e:
    print(f"✗ calendar_hub_bp: {e}")

try:
    from journey_routes import journey_bp
    print("✓ journey_bp")
except Exception as e:
    print(f"✗ journey_bp: {e}")

try:
    from legal_routes import legal_bp
    print("✓ legal_bp")
except Exception as e:
    print(f"✗ legal_bp: {e}")

try:
    from rent_calculator_routes import rent_calculator_bp
    print("✓ rent_calculator_bp")
except Exception as e:
    print(f"✗ rent_calculator_bp: {e}")

try:
    from doc_explorer_routes import doc_explorer_bp
    print("✓ doc_explorer_bp")
except Exception as e:
    print(f"✗ doc_explorer_bp: {e}")

try:
    from av_routes import av_routes_bp
    print("✓ av_routes_bp")
except Exception as e:
    print(f"✗ av_routes_bp: {e}")

try:
    from ai_orchestrator_routes import orchestrator_bp
    print("✓ orchestrator_bp")
except Exception as e:
    print(f"✗ orchestrator_bp: {e}")

try:
    from timeline_api_routes import timeline_api_bp
    print("✓ timeline_api_bp")
except Exception as e:
    print(f"✗ timeline_api_bp: {e}")
