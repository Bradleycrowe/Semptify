"""
System Map Builder - Generates interactive HTML map of all modules/functions
"""
import os
import re
from pathlib import Path

def scan_python_file(filepath):
    """Extract routes/functions from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        routes = []
        # FastAPI routes: @router.get("/path")
        fastapi_pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
        for match in re.finditer(fastapi_pattern, content):
            method, path = match.groups()
            routes.append({
                'method': method.upper(),
                'path': path,
                'type': 'fastapi'
            })
        
        # Flask routes: @bp.route("/path")
        flask_pattern = r'@\w+\.(route)\(["\']([^"\']+)["\']'
        for match in re.finditer(flask_pattern, content):
            _, path = match.groups()
            routes.append({
                'method': 'GET/POST',
                'path': path,
                'type': 'flask'
            })
        
        # Engine functions: def function_name(
        func_pattern = r'def\s+(\w+)\s*\('
        functions = re.findall(func_pattern, content)
        
        return {
            'routes': routes,
            'functions': [f for f in functions if not f.startswith('_')][:10]  # Top 10 public functions
        }
    except Exception as e:
        return {'routes': [], 'functions': [], 'error': str(e)}

def determine_role_access(filename, path=''):
    """Determine which roles can access this module"""
    filename_lower = filename.lower()
    path_lower = path.lower()
    
    # Admin only
    if 'admin' in filename_lower or 'admin' in path_lower or 'metrics' in filename_lower:
        return {'admin': True, 'manager': False, 'user': False}
    
    # Manager access
    if any(x in filename_lower for x in ['manager', 'analytics', 'oversight', 'team']):
        return {'admin': True, 'manager': True, 'user': False}
    
    # User accessible
    if any(x in filename_lower for x in ['vault', 'ledger', 'timeline', 'calendar', 'complaint', 'journey', 'profile']):
        return {'admin': True, 'manager': True, 'user': True}
    
    # Default: admin + manager
    return {'admin': True, 'manager': True, 'user': False}

def build_system_map():
    """Scan all Python files and build system map"""
    modules = []
    
    # Scan routers
    for router_file in Path('.').glob('*_router.py'):
        data = scan_python_file(router_file)
        access = determine_role_access(router_file.name)
        modules.append({
            'name': router_file.stem,
            'file': router_file.name,
            'type': 'FastAPI Router',
            'routes': data['routes'],
            'functions': data['functions'],
            **access
        })
    
    # Scan Flask routes
    for routes_file in Path('.').glob('*_routes.py'):
        data = scan_python_file(routes_file)
        access = determine_role_access(routes_file.name)
        modules.append({
            'name': routes_file.stem,
            'file': routes_file.name,
            'type': 'Flask Blueprint',
            'routes': data['routes'],
            'functions': data['functions'],
            **access
        })
    
    # Scan engines
    for engine_file in Path('engines').glob('*.py') if Path('engines').exists() else []:
        data = scan_python_file(engine_file)
        access = {'admin': True, 'manager': True, 'user': True}  # Engines are backend
        modules.append({
            'name': engine_file.stem,
            'file': f'engines/{engine_file.name}',
            'type': 'Engine',
            'routes': [],
            'functions': data['functions'],
            **access
        })
    
    return sorted(modules, key=lambda x: x['name'])

if __name__ == '__main__':
    import json
    system_map = build_system_map()
    with open('system_map.json', 'w') as f:
        json.dump(system_map, f, indent=2)
    print(f"Generated system map: {len(system_map)} modules")
