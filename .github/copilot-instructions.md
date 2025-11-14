# Copilot Instructions for Semptify

Concise, actionable guide for AI coding agents working on this Flask tenant rights protection platform. Focus on discoverable patterns from the codebase.

## Architecture Overview

**Single monolithic Flask app** (`Semptify.py`, ~2000+ lines) with blueprint-based modularity:
- Main app: `Semptify.py` coordinates startup, middleware, and blueprint registration
- Blueprints: `admin/`, `blueprints/`, route modules (`*_routes.py`, `*_engine.py`)
- Templates: `templates/` (Jinja2), static assets: `static/`
- Runtime dirs: `uploads/`, `logs/`, `security/`, `data/`, `copilot_sync/`, `final_notices/`
- Database: SQLite via `user_database.py` (user auth, remember tokens, timeline events)

**Key architectural pattern**: Routes (`*_routes.py`) handle HTTP, engines (`*_engine.py`) contain business logic, standalone modules provide utilities. Blueprints register via dynamic imports with try/except fallback logging.

## Security Architecture (Project-Specific)

**Dual-mode security** (`SECURITY_MODE=open|enforced`):
- `open`: Admin routes accessible without tokens (still logged/rate-limited) - used in dev/testing
- `enforced`: Admin requires token validation, CSRF on state-changing POSTs

**Admin tokens**: Multi-token support in `security/admin_tokens.json` (SHA-256 hashed, format: `[{id, hash, breakglass?}]` or `{id: {hash, ...}}`). Legacy `ADMIN_TOKEN` env var fallback. Break-glass: create `security/breakglass.flag` + use token with `"breakglass": true` (one-time).

**User tokens**: Anonymous digits-only tokens (12 chars) in `security/users.json`, SHA-256 hashed. Validated via `validate_user_token()` from `security.py`.

**CSRF**: Only enforced in `enforced` mode on POST routes. Use `_get_or_create_csrf_token()` in handlers, include `<input type="hidden" name="csrf_token" value="{{ csrf_token }}">` in forms. Tests rely on `open` mode bypassing CSRF.

**Rate limiting**: Sliding window via `check_rate_limit(key)` in `security.py`. Returns 429 with `Retry-After` header. Admin/registration endpoints use `ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX` env vars. Logs `rate_limited` events.

## Developer Workflows (Windows PowerShell)

**Setup & run**:
```powershell
Set-Location 'c:\Semptify\Semptify'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\Semptify.py  # Dev mode, port 5000
```

**Production**: `python .\run_prod.py` (waitress, uses `PORT` or `SEMPTIFY_PORT` env). HTTPS dev: `python .\run_dev_ssl.py` (requires `security/dev-local.crt|key`, set `FORCE_HTTPS=1`).

**Testing**: `python -m pytest -q` or run task `pytest` from VS Code. Tests in `tests/` cover enforced/open modes, CSRF, rate limits, vault, copilot, registration. Use monkeypatching for external APIs (GitHub, AI providers).

**Database init**: 
```powershell
.\.venv\Scripts\python.exe -c "from user_database import init_database, init_remember_tokens_table; init_database(); init_remember_tokens_table(); print('√ Database initialized')"
```

**Blueprint registration pattern** (in `Semptify.py`):
```python
try:
    from dashboard_api_routes import dashboard_api_bp
    app.register_blueprint(dashboard_api_bp)
    print("[OK] Dashboard API registered")
except ImportError as e:
    print(f"[WARN] Dashboard API not available: {e}")
```

## Key Integration Points

**AI Providers** (Copilot feature): Set `AI_PROVIDER=openai|azure|ollama` + provider-specific keys (`OPENAI_API_KEY`, `AZURE_*`, `OLLAMA_BASE_URL`). Route: POST `/api/copilot` accepts JSON, returns provider output. See `ollama_routes.py` for local LLM integration.

**GitHub API** (`/release_now`): Creates tags via API. In testing without `GITHUB_TOKEN`, simulates tag and logs to `logs/release-log.json`. Monkeypatch `requests.get/post` in tests.

**Database**: SQLite at `users.db`. Key tables: `users` (id, email, password_hash, created_at), `remember_tokens` (token_hash, user_id, expires_at), `timeline_events` (event_type, title, description, event_date, user_id). Use `get_user_db()` from `user_database.py`.

**Document Vault**: User uploads to `uploads/vault/<user_id>/`. Each upload generates a JSON certificate (`notary_<timestamp>_<type>.json`) with `sha256`, `ts`, `request_id`, evidence context. Auth via `?user_token=...`, `X-User-Token` header, or form field `user_token`.

## Registration & Vault Flow

1. **Register**: `GET /register` renders form with CSRF token. `POST /register` creates user with anonymous 12-digit token (hash stored in `security/users.json`).
2. **Rate limiting**: IP-based using `ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX`. Returns configured status (`ADMIN_RATE_STATUS`, default 429) with `Retry-After` header.
3. **Success**: `register_success.html` displays one-time token and link to `/vault?user_token=<token>`. Tests assert phrase "one-time token".
4. **Vault access**: Token required via query param, header, or form. Authenticate with `_require_user_or_401()`. Upload/download/attest operations logged to `logs/events.log`.

## Observability

**Metrics** (`/metrics`): Prometheus format (text/plain) or JSON. Counters: `requests_total`, `admin_requests_total`, `admin_actions_total`, `errors_total`, `releases_total`, `rate_limited_total`, `breakglass_used_total`, `token_rotations_total`. Gauge: `uptime_seconds`. Latency: `p50_ms`, `p95_ms`, `p99_ms`, `mean_ms`, `max_ms`.

**Readiness** (`/readyz`): Checks runtime dirs writable, `security/users.json` and `security/admin_tokens.json` loadable, database connectivity. Returns `{ status: ready|degraded, details: {...} }`.

**Logs**: `logs/init.log` (startup), `logs/events.log` (JSON events with rotation). Optional JSON access logs: set `ACCESS_LOG_JSON=1` (includes `request_id`, latency, IP). `X-Request-Id` header propagated.

## Contribution Conventions

**Startup side effects**: Preserve runtime dir creation (`uploads`, `logs`, `security`, `data`, `copilot_sync`, `final_notices`) and init logging to `logs/init.log`.

**File operations**: Use `secure_filename()` from werkzeug. Save user files under `uploads/vault/<user_id>/`. Generate JSON certificates with `sha256`, `ts`, `request_id`, evidence context (see `witness_save`, `packet_save` patterns).

**Admin UIs**: Include CSRF hidden field, require explicit confirm fields (e.g., `confirm_release=yes`). Authenticate via `_require_admin_or_401()`, rate-limit via `_rate_or_unauth_response()`.

**Blueprint creation**: Export as `<name>_bp = Blueprint(...)`. Register in `Semptify.py` with try/except and print statements. Routes can be standalone files or in `blueprints/` dir.

**Testing**: Write pytest tests in `tests/`. Use `SECURITY_MODE=open` for bypassing auth in tests. Monkeypatch external APIs. Test both enforced and open modes where applicable.

**Do not commit**: Anything under `security/` (tokens, flags, breakglass), large binaries in `uploads/`, `logs/`, `*.db` files.

## Deployment & Environment

**Render.com**: Uses `render.yaml` (not tracked in repo root). Env vars: `PORT`, `FLASK_SECRET_KEY`, `SECURITY_MODE`, `ADMIN_TOKEN` (legacy), `DATABASE_URL` (Postgres), GitHub tokens, AI provider keys.

**Docker**: `Dockerfile` and `docker-compose.yml` present. Ollama integration via separate service (`Dockerfile.ollama-service.bak` for reference).

**Environment template**: `config.env.template` shows required vars. Never commit actual `.env` with secrets.

## Project-Specific Patterns

**Atomic writes**: Use `_atomic_write_json(path, data)` for critical files (admin tokens, learning patterns). Writes to temp, then renames.

**Timeline feature**: Vault uploads auto-populate timeline. API: `GET /api/timeline/events` returns merged events from DB + vault certificates.

**Learning engine**: Adaptive system in `data/learning_patterns.json`. Admin routes: `/admin/learning` (UI), POST `/admin/prime_learning` (seed), POST `/admin/learning/reset`. Uses `_metadata` key for versioning.

**Complaint filing**: Multi-step wizard (`complaint_filing_engine.py`, `complaint_filing_routes.py`). Generates court packets as PDFs via reportlab.

**Ledger system**: Rent payment tracking (`ledger_*` modules). Calendar integration via `icalendar` lib.

**Curiosity engine**: Self-learning system (`curiosity_engine.py`) that adapts to user patterns and suggests next steps.

## Module Naming Conventions

- `*_routes.py`: Blueprint route definitions
- `*_engine.py`: Business logic, no Flask dependencies
- `*_api.py`: External API integrations
- `*_model.py`: Data models (if using ORM patterns)
- `user_database.py`: Database utilities and queries
- `security.py`: Auth, tokens, rate limiting, metrics

## Common Pitfalls

1. **Blueprint registration**: Always use try/except. If blueprint import fails, app should still start (log warning).
2. **Token validation**: Use `validate_user_token()` or `validate_admin_token()` from `security.py`, never roll your own.
3. **CSRF**: Remember `open` mode bypasses CSRF (tests need this). In `enforced` mode, all state-changing POSTs need token.
4. **Rate limiting**: Apply AFTER auth, not before. Use consistent rate keys (`admin:<ip>:<path>`).
5. **File paths**: Runtime dirs may not exist on first run. Startup ensures they exist, but if adding new dirs, update startup logic.
6. **Database**: Use `get_user_db()` for connection, not raw `sqlite3.connect()`. Ensures proper threading.

## Quick Reference: Key Files

- `Semptify.py`: Main app, blueprint registration, startup
- `security.py`: Auth, tokens, rate limiting, metrics, CSRF
- `vault.py`: Document storage (may also be in `blueprints/vault_bp.py`)
- `user_database.py`: SQLite utilities, user/token management
- `requirements.txt`: Dependencies (Flask, waitress, pytest, reportlab, etc.)
- `tests/`: Pytest suite (test_*.py files)
- `.github/copilot-instructions.md`: This file

## When Unclear

If architecture decisions, security patterns, or testing approaches are unclear, check:
1. Existing tests in `tests/` for usage examples
2. `Semptify.py` blueprint registration for integration patterns
3. `security.py` for auth/rate-limit implementations
4. BLUEPRINT.md or other `*_COMPLETE.md` docs for feature deep-dives

Ask for expansion on: Database migrations, Render deploy specifics, PWA assets, token rotation workflows, or Kubernetes manifests if needed.
