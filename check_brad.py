from brad_gui_routes import brad_bp

print(f"Brad GUI Blueprint: {brad_bp.name}")
print(f"URL Prefix: {brad_bp.url_prefix}")
print(f"Routes: {len(brad_bp.deferred_functions)}")
print(f"\nRoute list:")
for func in brad_bp.deferred_functions:
    print(f"  - {func}")
