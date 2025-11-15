"""
Template wrapper that adds status warnings to generated features.
"""
from flask import render_template as flask_render_template, Markup
from functools import wraps
from feature_registry import get_feature_registry, FeatureStatus

def feature_aware_render(template_name, **context):
    """Render template with automatic feature status banner."""
    # Determine if this is a generated feature template
    if any(pattern in template_name for pattern in ['attorney_finder', 'rent_calculator']):
        feature_name = template_name.replace('.html', '').replace('/', '_')
        registry = get_feature_registry()
        feature = registry.get_feature(feature_name)
        
        if feature:
            status = feature['status']
            completion = feature['completion_percent']
            
            # Generate warning banner HTML
            banner_html = _generate_status_banner(status, completion, feature_name)
            context['_feature_status_banner'] = Markup(banner_html)
            context['_feature_status'] = status
            context['_feature_completion'] = completion
    
    return flask_render_template(template_name, **context)

def _generate_status_banner(status, completion, feature_name):
    """Generate HTML banner based on feature status."""
    banners = {
        FeatureStatus.STUB.value: f'''
            <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; margin-bottom: 20px; border-radius: 4px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 24px;">⚠️</span>
                    <div>
                        <strong style="color: #92400e;">This feature is under development</strong>
                        <p style="margin: 4px 0 0; color: #78350f; font-size: 14px;">
                            Currently showing placeholder data. Functionality is limited ({completion}% complete).
                            Real implementation coming soon.
                        </p>
                    </div>
                </div>
            </div>
        ''',
        FeatureStatus.DEVELOPMENT.value: f'''
            <div style="background: #dbeafe; border-left: 4px solid #3b82f6; padding: 16px; margin-bottom: 20px; border-radius: 4px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 24px;">🚧</span>
                    <div>
                        <strong style="color: #1e40af;">Active Development</strong>
                        <p style="margin: 4px 0 0; color: #1e3a8a; font-size: 14px;">
                            This feature is being actively developed ({completion}% complete). 
                            Some functionality may be incomplete or change.
                        </p>
                    </div>
                </div>
            </div>
        ''',
        FeatureStatus.BETA.value: f'''
            <div style="background: #e0e7ff; border-left: 4px solid #6366f1; padding: 16px; margin-bottom: 20px; border-radius: 4px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 24px;">🧪</span>
                    <div>
                        <strong style="color: #4338ca;">Beta Feature</strong>
                        <p style="margin: 4px 0 0; color: #3730a3; font-size: 14px;">
                            This feature is in testing. Please report any issues you encounter.
                            <a href="/feedback?feature={feature_name}" style="color: #4f46e5;">Give feedback</a>
                        </p>
                    </div>
                </div>
            </div>
        ''',
        FeatureStatus.DEPRECATED.value: '''
            <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 16px; margin-bottom: 20px; border-radius: 4px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 24px;">⛔</span>
                    <div>
                        <strong style="color: #991b1b;">Deprecated Feature</strong>
                        <p style="margin: 4px 0 0; color: #7f1d1d; font-size: 14px;">
                            This feature will be removed in a future version. Please use the alternative feature.
                        </p>
                    </div>
                </div>
            </div>
        '''
    }
    
    return banners.get(status, '')

def add_feature_warnings(bp_name):
    """Decorator to automatically add status warnings to all routes in a blueprint."""
    def decorator(blueprint):
        # Store original render function
        original_render = flask_render_template
        
        # Wrap all view functions
        for endpoint, view_func in blueprint.view_functions.items():
            @wraps(view_func)
            def wrapped_view(*args, **kwargs):
                result = view_func(*args, **kwargs)
                # If result is string HTML, inject banner
                if isinstance(result, str) and '<html' in result.lower():
                    registry = get_feature_registry()
                    feature = registry.get_feature(bp_name)
                    if feature and feature['status'] != FeatureStatus.PRODUCTION.value:
                        banner = _generate_status_banner(
                            feature['status'],
                            feature['completion_percent'],
                            bp_name
                        )
                        # Inject after <body> tag
                        result = result.replace('<body>', f'<body>{banner}', 1)
                return result
            blueprint.view_functions[endpoint] = wrapped_view
        
        return blueprint
    return decorator
