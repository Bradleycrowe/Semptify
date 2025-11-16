"""
Enhanced Admin Control service - discovers registered modules.
"""
import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENGINES_DIR = PROJECT_ROOT / 'engines'
BLUEPRINTS_DIR = PROJECT_ROOT / 'blueprints'
ADMIN_DIR = PROJECT_ROOT / 'admin'
SERVICES_DIR = PROJECT_ROOT / 'services'


def _humanize_name(stem: str) -> str:
    return stem.replace('_', ' ').replace('  ', ' ').strip().title()


def _list_files(folder: Path, pattern: str):
    if not folder.exists():
        return []
    return sorted(folder.glob(pattern))


def discover_all_modules():
    """Auto-discover engines, routes, blueprints, admin modules, and services."""
    engines = []
    for engine_file in _list_files(ENGINES_DIR, '*_engine.py'):
        engines.append({
            'name': _humanize_name(engine_file.stem.replace('_engine', '')),
            'file': f'engines/{engine_file.name}',
            'category': 'engine',
            'icon': '⚙️'
        })

    routes = []
    for route_file in _list_files(PROJECT_ROOT, '*_routes.py'):
        routes.append({
            'name': _humanize_name(route_file.stem.replace('_routes', '')),
            'file': route_file.name,
            'category': 'routes',
            'icon': '🛣️'
        })

    blueprints = []
    for bp_file in _list_files(BLUEPRINTS_DIR, '*_bp.py'):
        blueprints.append({
            'name': _humanize_name(bp_file.stem.replace('_bp', '')),
            'file': f'blueprints/{bp_file.name}',
            'category': 'blueprint',
            'icon': '📦'
        })

    admin_modules = []
    for admin_file in _list_files(ADMIN_DIR, '*.py'):
        if admin_file.name == '__init__.py':
            continue
        admin_modules.append({
            'name': _humanize_name(admin_file.stem),
            'file': f'admin/{admin_file.name}',
            'category': 'admin',
            'icon': '🔐'
        })

    services = []
    for svc_file in _list_files(SERVICES_DIR, '*_service.py'):
        services.append({
            'name': _humanize_name(svc_file.stem.replace('_service', '')),
            'file': f'services/{svc_file.name}',
            'category': 'service',
            'icon': '🧩'
        })

    return {
        'engines': engines,
        'routes': routes,
        'blueprints': blueprints,
        'admin': admin_modules,
        'services': services,
        'total_count': len(engines) + len(routes) + len(blueprints) + len(admin_modules) + len(services)
    }


def get_admin_panels():
    """Return enhanced admin panel configurations."""
    return [
        {
            'name': 'System Modules',
            'icon': '🧩',
            'path': '/admin/modules',
            'description': 'All engines, routes, blueprints, and services',
            'manual': 'View all discovered engines, services, routes, blueprints, and admin modules.'
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

    admin_tokens = 0
    try:
        with open('security/admin_tokens.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'tokens' in data:
                admin_tokens = len(data['tokens'])
    except Exception:
        pass

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
        with open('logs/events.log', 'r', encoding='utf-8') as f:
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
