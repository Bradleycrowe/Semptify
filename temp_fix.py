
with open('Semptify.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic line
content = content.replace('try:\\n    from route_discovery_routes import route_discovery_bp, init_route_discovery_api\\nexcept ImportError:\\n    route_discovery_bp = None\\n    init_route_discovery_api = None\\n\\napp.config[', 'try:\\n    from route_discovery_routes import route_discovery_bp, init_route_discovery_api\\nexcept ImportError:\\n    route_discovery_bp = None\\n    init_route_discovery_api = None\\n\\napp.config[')

with open('Semptify.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Replaced the quotes')
