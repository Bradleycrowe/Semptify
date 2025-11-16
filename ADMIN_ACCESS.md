# Semptify Admin Access

## Local Development
**Admin Control Panel:** http://127.0.0.1:5000/admin/control-panel?token=gGYfIWpWYXzInpz4t2PljA

**Dev Admin Token:** gGYfIWpWYXzInpz4t2PljA
**Token Location:** security/admin_tokens.json (hashed)

## Production (Render)
**Admin Control Panel:** https://semptify.onrender.com/admin/control-panel?token=YOUR_PRODUCTION_TOKEN

**Environment Variables to Set in Render:**
- ADMIN_TOKEN=<secure-production-token>
- SECURITY_MODE=enforced
- AI_PROVIDER=openai (or azure/ollama)
- OPENAI_API_KEY=<your-key>

## Admin Routes
- /admin/control-panel - Main graphical dashboard
- /admin/users-panel - User management
- /admin/storage-db - Database and R2 storage
- /admin/security - Token and security settings
- /admin/email - Email provider config
- /admin/metrics - Prometheus metrics
- /admin/logs - Event logs

## Temporary Access API
- POST /admin/issue-temp-access - Issue time-limited tokens
- GET /admin/list-temp-access - List active temp tokens
- POST /admin/revoke-temp-access - Revoke token

**Allowed Scopes:** timeline, analytics, ai, admin_panels
**Excluded:** vault (owner-only access)

## System Modules Discovered (36 total)
### Engines (15)
- accuracy_engine.py
- adaptive_intensity_engine.py
- complaint_filing_engine.py
- curiosity_engine.py
- dashboard_engine.py
- data_flow_engine.py
- housing_programs_engine.py
- intelligence_engine.py
- jurisdiction_engine.py
- learning_engine.py
- librarian_engine.py
- perspective_engine.py
- prime_learning_engine.py
- reasoning_engine.py
- temp_access_engine.py

### Routes (17)
- av_routes.py
- calendar_timeline_routes.py
- complaint_filing_routes.py
- dashboard_api_routes.py
- data_flow_routes.py
- housing_programs_routes.py
- journey_routes.py
- learning_routes.py
- learning_dashboard_routes.py
- ledger_admin_routes.py
- ledger_calendar_routes.py
- ledger_tracking_routes.py
- ollama_routes.py
- onboarding_routes.py
- preliminary_learning_routes.py
- route_discovery_routes.py
- test_all_routes.py

### Blueprints (3)
- blueprints/ai_bp.py
- blueprints/auth_bp.py
- blueprints/vault_bp.py

### Admin (1)
- admin/routes.py

## Deployment Status
**Branch:** clean-deploy
**Commit:** 646e1179 - "Add state-of-the-art admin control panel with module discovery"
**Pushed:** 2025-11-14 02:09:52
**Status:** Auto-deploying to Render

## Security Notes
- Admin tokens stored SHA-256 hashed in security/admin_tokens.json
- Temporary access tokens expire automatically
- Vault access strictly owner-only (admin cannot override)
- CSRF protection active in enforced mode
- Rate limiting on admin endpoints
