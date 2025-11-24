import os
import re
from pathlib import Path

print("\n" + "="*70)
print("  COMPREHENSIVE GUI COMPLETENESS ASSESSMENT")
print("="*70)

guis = [
    {
        'name': 'Brad GUI',
        'file': 'brad_gui_routes.py',
        'url': '/brad/',
        'purpose': 'Multi-client case management for advocates',
        'expected_features': [
            'Client CRUD operations',
            'Search/filter clients',
            'Client details view',
            'Document management per client',
            'Communication log',
            'Task/reminder system',
            'Export client data',
            'Reporting/analytics',
            'AI chat assistant',
            'Storage health check',
            'Multi-client dashboard',
            'Client status tracking'
        ]
    },
    {
        'name': 'Modern GUI',
        'file': 'modern_gui_routes.py',
        'url': '/app/',
        'purpose': 'Interactive forms with smart auto-fill',
        'expected_features': [
            'Smart auto-fill',
            'Form validation',
            'Save drafts',
            'Profile management',
            'Form templates',
            'Progress tracking',
            'Error handling',
            'Context-aware suggestions'
        ]
    },
    {
        'name': 'Main Dashboard',
        'file': 'main_dashboard_routes.py',
        'url': '/',
        'purpose': 'Homepage and navigation hub',
        'expected_features': [
            'Welcome page',
            'Navigation menu',
            'Quick actions',
            'Recent activity',
            'Status widgets',
            'Notifications',
            'Progress overview',
            'Feature cards'
        ]
    },
    {
        'name': 'Learning Dashboard',
        'file': 'learning_dashboard_routes.py',
        'url': '/api/learning',
        'purpose': 'Adaptive learning system',
        'expected_features': [
            'Learning modules',
            'Progress tracking',
            'Adaptive difficulty',
            'Curiosity engine',
            'Topic recommendations',
            'Quiz/assessments',
            'Achievements',
            'Learning path'
        ]
    },
    {
        'name': 'Calendar Vault UI',
        'file': 'calendar_vault_ui_routes.py',
        'url': '/timeline/assistant',
        'purpose': 'Timeline with document suggestions',
        'expected_features': [
            'Event timeline',
            'Document suggestions',
            'Priority sorting',
            'Event creation',
            'Document linking',
            'Deadline tracking',
            'Export timeline',
            'Calendar integration'
        ]
    }
]

results = []

for gui in guis:
    print(f"\n{'='*70}")
    print(f"  {gui['name'].upper()} - {gui['url']}")
    print(f"{'='*70}")
    print(f"Purpose: {gui['purpose']}\n")
    
    if not os.path.exists(gui['file']):
        print(f"❌ FILE NOT FOUND: {gui['file']}")
        results.append({
            'name': gui['name'],
            'found': 0,
            'missing': len(gui['expected_features']),
            'total': len(gui['expected_features']),
            'percent': 0
        })
        continue
    
    with open(gui['file'], 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    # Count routes
    routes = len(re.findall(r'@\w+\.route\(', content))
    print(f"📊 Routes defined: {routes}")
    
    # Check for templates
    has_templates = 'render_template' in content
    has_api = '/api/' in content or 'jsonify' in content
    has_forms = 'request.form' in content or 'request.json' in content
    
    print(f"🎨 Uses templates: {'✓' if has_templates else '✗'}")
    print(f"🔌 Has API endpoints: {'✓' if has_api else '✗'}")
    print(f"📝 Handles forms: {'✓' if has_forms else '✗'}")
    
    # Check features
    print(f"\n📋 Feature Completeness:")
    found = 0
    missing_features = []
    
    for feature in gui['expected_features']:
        # Create search patterns for each feature
        patterns = feature.lower().split()
        matched = all(pattern in content for pattern in patterns[:2])  # Check first 2 words
        
        if matched:
            print(f"  ✓ {feature}")
            found += 1
        else:
            print(f"  ✗ {feature}")
            missing_features.append(feature)
    
    percent = int((found / len(gui['expected_features'])) * 100)
    
    results.append({
        'name': gui['name'],
        'found': found,
        'missing': len(missing_features),
        'total': len(gui['expected_features']),
        'percent': percent,
        'missing_list': missing_features
    })
    
    print(f"\n📈 Completeness: {found}/{len(gui['expected_features'])} ({percent}%)")

# Summary
print(f"\n{'='*70}")
print("  SUMMARY - GUI COMPLETENESS SCORES")
print(f"{'='*70}\n")

for r in results:
    bar_length = 30
    filled = int((r['percent'] / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"{r['name']:20} [{bar}] {r['percent']:3}% ({r['found']}/{r['total']})")

print(f"\n{'='*70}")
print("  OVERALL SYSTEM GAPS")
print(f"{'='*70}\n")

all_missing = []
for r in results:
    if 'missing_list' in r:
        for feature in r['missing_list']:
            all_missing.append(f"{r['name']}: {feature}")

print(f"Total missing features across all GUIs: {sum(r['missing'] for r in results)}\n")

# Group by priority
print("🔴 HIGH PRIORITY (Core functionality):")
high_priority = [m for m in all_missing if any(x in m.lower() for x in ['crud', 'search', 'save', 'validation', 'navigation'])]
for item in high_priority[:10]:
    print(f"  • {item}")

print(f"\n�� MEDIUM PRIORITY (Enhanced features):")
medium_priority = [m for m in all_missing if any(x in m.lower() for x in ['export', 'report', 'notification', 'progress', 'tracking'])]
for item in medium_priority[:10]:
    print(f"  • {item}")

print(f"\n🟢 LOW PRIORITY (Nice to have):")
low_priority = [m for m in all_missing if m not in high_priority and m not in medium_priority]
for item in low_priority[:10]:
    print(f"  • {item}")

print(f"\n{'='*70}")
