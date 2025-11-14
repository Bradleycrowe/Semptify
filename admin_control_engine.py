"""
Enhanced Admin Control Engine - Discovers all modules and engines
"""
import os
import json
from pathlib import Path
from datetime import datetime

def discover_all_modules():
    """Auto-discover all engines, routes, and blueprints in the system."""
    base_path = Path(__file__).parent
    
    # Engines
    engines = []
    for engine_file in base_path.glob('*_engine.py'):
        if engine_file.name == 'admin_control_engine.py':
            continue
        engines.append({
            'name': engine_file.stem.replace('_', ' ').title(),
            'file': engine_file.name,
            'category': 'engine',
            'icon': '⚙️'
        })
    
    # Route modules
    routes = []
    for route_file in base_path.glob('*_routes.py'):
        routes.append({
            'name': route_file.stem.replace('_routes', '').replace('_', ' ').title(),
            'file': route_file.name,
            'category': 'routes',
            'icon': '🛣️'
        })
    
    # Blueprints
    blueprints = []
    bp_path = base_path / 'blueprints'
    if bp_path.exists():
        for bp_file in bp_path.glob('*_bp.py'):
            blueprints.append({
                'name': bp_file.stem.replace('_bp', '').replace('_', ' ').title(),
                'file': f'blueprints/{bp_file.name}',
                'category': 'blueprint',
                'icon': '📦'
            })
    
    # Admin modules
    admin_path = base_path / 'admin'
    admin_modules = []
    if admin_path.exists():
        for admin_file in admin_path.glob('*.py'):
            if admin_file.name != '__init__.py':
                admin_modules.append({
                    'name': admin_file.stem.replace('_', ' ').title(),
                    'file': f'admin/{admin_file.name}',
                    'category': 'admin',
                    'icon': '🔐'
                })
    
    return {
        'engines': sorted(engines, key=lambda x: x['name']),
        'routes': sorted(routes, key=lambda x: x['name']),
        'blueprints': sorted(blueprints, key=lambda x: x['name']),
        'admin': sorted(admin_modules, key=lambda x: x['name']),
        'total_count': len(engines) + len(routes) + len(blueprints) + len(admin_modules)
    }

def get_admin_panels():
    """Return enhanced admin panel configurations."""
    return [
        {
            'name': 'System Modules',
            'icon': '🧩',
            'path': '/admin/modules',
            'description': 'All engines, routes, and blueprints',
            'manual': 'View all discovered system modules including engines, routes, blueprints, and admin modules.'
        },
        {
            'name': 'Observability',
            'icon': '📊',
            'path': '/admin/metrics',
            'description': 'Metrics, logs, and system health',
            'manual': 'Monitor system performance via /admin/metrics (Prometheus), /admin/logs (events), and /readyz (health).'
        },
        {
            'name': 'Users & Auth',
            'icon': '👥',
            'path': '/admin/users-panel',
            'description': 'User management and authentication',
            'manual': 'View users, export lists, manage sessions. User tokens are 12-digit anonymous codes stored hashed.'
        },
        {
            'name': 'Storage & Database',
            'icon': '💾',
            'path': '/admin/storage-db',
            'description': 'SQLite and R2 storage management',
            'manual': 'Manage users.db, sync to R2, download backups, view schemas.'
        },
        {
            'name': 'AI & Copilot',
            'icon': '🤖',
            'path': '/admin/ai',
            'description': 'AI provider configuration',
            'manual': 'Configure AI_PROVIDER (OpenAI/Azure/Ollama), manage API keys, check Copilot status.'
        },
        {
            'name': 'Security',
            'icon': '🔒',
            'path': '/admin/security',
            'description': 'Tokens, rate limits, breakglass',
            'manual': 'Manage SECURITY_MODE, rotate admin tokens, configure rate limits, handle breakglass access.'
        },
        {
            'name': 'Temporary Access',
            'icon': '⏰',
            'path': '/admin/temp-access',
            'description': 'Issue time-limited tokens',
            'manual': 'Issue scoped tokens (timeline/analytics/ai/admin_panels) with auto-expiry. Vault excluded.'
        },
        {
            'name': 'Email & Delivery',
            'icon': '📧',
            'path': '/admin/email',
            'description': 'Email provider and testing',
            'manual': 'Configure email provider (SendGrid), test delivery, view logs.'
        },
        {
            'name': 'Releases',
            'icon': '🚀',
            'path': '/admin/',
            'description': 'GitHub release management',
            'manual': 'Create GitHub releases with auto-versioning. Requires GITHUB_TOKEN.'
        }
    ]

def get_system_overview():
    """Enhanced system overview with module counts."""
    modules = discover_all_modules()
    
    # Admin tokens
    admin_tokens = 0
    try:
        with open('security/admin_tokens.json', 'r') as f:
            data = json.load(f)
            if 'tokens' in data:
                admin_tokens = len(data['tokens'])
    except Exception:
        pass
    
    # Users
    total_users = 0
    try:
        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
    
    # Timeline events
    timeline_events = 0
    try:
        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM timeline_events')
        timeline_events = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
    
    return {
        'security_mode': os.environ.get('SECURITY_MODE', 'open'),
        'ai_provider': os.environ.get('AI_PROVIDER', 'openai'),
        'admin_tokens': admin_tokens,
        'total_users': total_users,
        'timeline_events': timeline_events,
        'modules': modules
    }

def get_recent_events(limit=6):
    """Get recent log events."""
    events = []
    try:
        with open('logs/events.log', 'r') as f:
            lines = f.readlines()[-limit:]
            for line in lines:
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except Exception:
                    pass
    except Exception:
        pass
    return events

def build_admin_context():
    """Build complete admin control panel context."""
    return {
        'overview': get_system_overview(),
        'panels': get_admin_panels(),
        'recent_events': get_recent_events()
    }
