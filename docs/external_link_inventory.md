# Semptify External Link Inventory (Generated)

This file lists all external and internal links, endpoints, and placeholders found in the codebase and templates. Use this to track which are working, dead, or need to be linked up.

| Link/Endpoint/URL | Location | Status | Notes |
|-------------------|----------|--------|-------|
| https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css | templates/base.html | working | Bootstrap CDN |
| https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js | templates/base.html | working | Bootstrap JS CDN |
| https://www.hud.gov/topics/rental_assistance | templates/base.html | working | HUD Rental Assistance |
| https://www.justice.gov/crt/fair-housing | templates/base.html | working | DOJ Fair Housing |
| https://github.com/{owner}/{repo}/actions | Semptify.py | working | GitHub Actions (dynamic) |
| https://{owner}.github.io/{repo}/ | Semptify.py | working | GitHub Pages (dynamic) |
| https://github.com/{owner}/{repo}/releases/tag/{tag_name} | Semptify.py | working | GitHub Releases (dynamic) |
| https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main | Semptify.py | working | GitHub API (dynamic) |
| https://api.github.com/repos/{owner}/{repo}/git/refs | Semptify.py | working | GitHub API (dynamic) |
| https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches | Semptify.py | working | GitHub API (dynamic) |
| https://api.openai.com/v1/chat/completions | Semptify.py | working | OpenAI API (default) |
| https://api.bluenotary.example | ron_providers.py | placeholder | Replace with real BlueNotary API |
| https://<your-host>/webhooks/ron | Semptify.py | to be linked | RON webhook endpoint (dynamic) |
| https://tenantresourcehub.org/ | Semptify.py | working | Tenant Resource Hub |
| https://www.211.org/ | Semptify.py | working | 211 Community Services |
| https://nlihc.org/ | Semptify.py | working | National Low Income Housing Coalition |
| /api/copilot | Semptify.py | working | Internal API endpoint |
| /api/help_panel_settings | Semptify.py | working | Internal API endpoint |
| /health | Semptify.py | working | Health check |
| /readyz | Semptify.py | working | Readiness check |
| /metrics | Semptify.py | working | Prometheus metrics |
| /admin/status | Semptify.py | working | Admin status |
| /vault | templates/base.html | working | Internal link |
| /resources/* | templates/* | working | Internal resource links |
| /static/css/app.css | templates/* | working | Local static asset |
| /static/js/help-panel.js | templates/* | working | Local static asset |
| /static/icons/Semptfylogo.svg | templates/base.html | working | Local static asset |

# Legend
- working: confirmed in use and functional
- placeholder: needs to be replaced with a real endpoint or configured
- to be linked: dynamic or requires setup (e.g., webhook URLs)
- dead: known to be broken or deprecated (none found in scan)

# How to update
- Add new links/endpoints as you add features.
- Mark status as 'working', 'placeholder', 'to be linked', or 'dead'.
- For dynamic links, ensure the runtime config/env is set correctly.

