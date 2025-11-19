# Semptify Themed Dashboards

Three fully-integrated Flask themes that work with Semptify's existing card system and routing.

## Quick Access URLs

When the server is running:

- **Legal Portal**: http://127.0.0.1:5001/theme/legal
- **Helpdesk**: http://127.0.0.1:5001/theme/helpdesk  
- **Action Dashboard**: http://127.0.0.1:5001/theme/action

## Theme Switcher

Set your preferred theme (persists in session):

```
/theme/set/legal      → Legal Document Portal
/theme/set/helpdesk   → Tenant Helpdesk
/theme/set/action     → Rights Action Dashboard
/theme/set/default    → Original dashboard
```

## Integration

All themes:
- Extend `base.html` (inherit header/footer)
- Use existing `cards` from `dashboard_engine.get_all_cards()`
- Work with all current Semptify routes (`/vault`, `/timeline`, etc.)
- Fully responsive (mobile → desktop)
- Maintain user session state

## Registration

Add to `Semptify.py`:

```python
try:
    from themes_routes import themes_bp
    app.register_blueprint(themes_bp)
    print("[OK] Theme system registered (/theme/*)")
except ImportError as e:
    print(f"[WARN] Themes not available: {e}")
```

## Files

- `templates/dashboard_theme_legal.html` - Legal portal
- `templates/dashboard_theme_helpdesk.html` - Helpdesk
- `templates/dashboard_theme_action.html` - Action dashboard
- `themes_routes.py` - Flask blueprint with routes
