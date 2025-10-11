# Copilot Instructions for SemptifyGUI

Concise, actionable guide for AI coding agents on this Flask app. Focus only on patterns discoverable from this repo.

## Architecture snapshot
- Single Flask app: `SemptifyGUI.py` (templates in `templates/`, assets in `static/`).
- Startup ensures runtime dirs exist: `uploads`, `logs`, `copilot_sync`, `final_notices`, `security`; logs initialization to `logs/init.log` and JSON events to `logs/events.log` (with rotation).
- Key endpoints: `/`, `/health`, `/healthz`, `/readyz`, `/metrics`, `/info`, admin (`/admin`, `/admin/status`, POST `/release_now`, POST `/trigger_workflow`, `/release_history`, `/sbom*`), user resources (witness/packet/service-animal/move checklist), Document Vault (`/vault`, upload/download), rent ledger, registration (`/register`), Copilot UI/API (`/copilot`, POST `/api/copilot`).

## Security & auth (project-specific)
- Modes: `SECURITY_MODE=open|enforced` (env). In open mode, admin routes allow access but still log; in enforced, admin requires token.
- Admin tokens: hashed entries in `security/admin_tokens.json` (multi-token). Legacy fallback env `ADMIN_TOKEN` supported. Break‑glass: create `security/breakglass.flag` and use a token with `"breakglass": true` once.
- CSRF: enforced for state‑changing POSTs only when in enforced mode. Use `_get_or_create_csrf_token()` and include `<input type="hidden" name="csrf_token" value="{{ csrf_token }}">` in forms.
- Rate limiting (admin and select APIs): sliding window via `ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX`, returns 429 with `Retry-After` and logs `rate_limited`.

## Observability & readiness
- `/metrics` exposes counters (Prometheus): `requests_total`, `admin_requests_total`, `admin_actions_total`, `errors_total`, `releases_total`, `rate_limited_total`, `breakglass_used_total`, `token_rotations_total`, plus `uptime_seconds` gauge.
- `/readyz` verifies runtime dirs are writable and tokens/users can load; returns `{ status: ready|degraded }` with details.
- Optional JSON access logs: set `ACCESS_LOG_JSON=1` (includes `request_id`, latency, IP). `X-Request-Id` is propagated.

## Runs, builds, tests (Windows PowerShell)
- Dev run:
  ```powershell
  Set-Location -LiteralPath 'd:\Semptify\SemptifyGUI'
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  python .\SemptifyGUI.py
  ```
- Prod run (waitress): `python .\run_prod.py` (uses `SEMPTIFY_PORT` or `PORT`). HTTPS dev: `python .\run_dev_ssl.py` with `security/dev-local.crt|key` and `FORCE_HTTPS=1`.
- Tests: `python -m pytest -q` (see `tests/` for enforced/open mode, CSRF, rate limit, copilot, vault).

## Integration points
- GitHub API: `/release_now` creates a tag on the repo; in TESTING without `GITHUB_TOKEN`, it simulates a tag and appends to `logs/release-log.json`.
- Copilot providers via env: `AI_PROVIDER=openai|azure|ollama` (+ provider‑specific keys). POST `/api/copilot` accepts JSON and returns provider output.

## User sign‑up flow (Document Vault)
- Registration: `GET /register` renders a form with a CSRF token; `POST /register` creates a user with an anonymous digits‑only token (hash stored in `security/users.json`).
- CSRF: In `open` mode, CSRF is bypassed (tests rely on this). In `enforced` mode, include the hidden `csrf_token` input.
- Rate limiting: Registration is IP‑limited using the same window/max envs (`ADMIN_RATE_WINDOW`, `ADMIN_RATE_MAX`, responds with configured status and `Retry-After`).
- Success: `register_success.html` shows a one‑time token and a link to `/vault?user_token=<token>`. Tests assert the phrase "one-time token" (`tests/test_registration.py`).
- Vault auth: user token can be supplied via `?user_token=...`, `X-User-Token` header, or form field `user_token`.

## Contribution conventions for agents
- Preserve startup side effects (runtime dirs + init log). When writing files for users, save under per-user vault `uploads/vault/<user_id>`; include a JSON certificate with `sha256`, `ts`, `request_id`, and evidence context (see `witness_save`, `packet_save`, etc.).
- For admin UIs, include CSRF hidden field and require explicit confirm fields (e.g., `confirm_release=yes`).
- Use `secure_filename` and serve files via `send_file`; authenticate with `_require_user_or_401()` or `_require_admin_or_401()` and reuse `_rate_or_unauth_response()`.
- Do not commit anything under `security/` (tokens, flags) or large binaries under `uploads/`.

If any section is unclear or missing important patterns you rely on, tell me what to expand (e.g., token rotation, Render deploy vars, or PWA assets) and I’ll update this file.
