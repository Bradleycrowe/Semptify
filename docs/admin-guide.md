# SemptifyGUI Admin Guide

This guide is the single source of truth for running, securing, operating, and troubleshooting SemptifyGUI. It assumes Windows + PowerShell and the repository at `d:\\Semptify\\SemptifyGUI`.

## Quick links
- Live service: `RENDER_BASE_URL` (see security/render.env)
- Admin page: `${RENDER_BASE_URL}/admin?token=${ADMIN_TOKEN}`
- Repo scripts: `scripts/`
- Runtime logs (in-container): `logs/`

## 1) Secrets management (do this once)
- Local key ring lives in `security/render.env` (not committed). Use the helper to generate strong secrets:

```powershell
# Generate/rotate FLASK_SECRET and ADMIN_TOKEN; prints token hash for optional multi-token setup
.\scripts\bootstrap_secrets.ps1 -ShowHash
```

- Required secrets in Render Dashboard for the service:
  - FLASK_SECRET (long random, from render.env)
  - ADMIN_TOKEN (long random, from render.env)
  - SECURITY_MODE = enforced
  - FORCE_HTTPS = 1, HSTS_MAX_AGE = 31536000, HSTS_PRELOAD = 1
  - ACCESS_LOG_JSON = 1

Tip: Use the automated sync to push these to Render:

```powershell
.\scripts\sync_render_secrets.ps1
```

## 2) Deploy and verify
- One-and-done deploy (syncs secrets, deploys, and opens the site):

```powershell
.\scripts\deploy_oneclick.ps1
```

- Health smoke checks:

```powershell
(Invoke-WebRequest $env:RENDER_BASE_URL + '/health' -UseBasicParsing).StatusCode
(Invoke-WebRequest $env:RENDER_BASE_URL + '/readyz' -UseBasicParsing).StatusCode
(Invoke-WebRequest $env:RENDER_BASE_URL + '/info' -UseBasicParsing).Content
```

## 3) Admin access
- Open admin (token auto-injected from security/render.env):

```powershell
.\scripts\open_admin.ps1
```

- Manual URL if needed:

```
https://<your-service>.onrender.com/admin?token=<ADMIN_TOKEN>
```

## 4) Token rotation and multi-token
- Rotate a token via the Admin page (Rotate Token form). CSRF is handled automatically.
- Optional multi-token file (`security/admin_tokens.json`), entries like:

```
[
  { "id": "primary", "hash": "sha256:<hex>", "enabled": true },
  { "id": "ops-breakglass", "hash": "sha256:<hex>", "enabled": true, "breakglass": true }
]
```

- Generate a hash for a plain token:

```powershell
# Python helper
D:\Semptify\SemptifyGUI\.venv\Scripts\python.exe .\scripts\hash_token.py PlainTokenValue
```

Note: The production container deletes any committed `security/admin_tokens.json` and bootstraps from `ADMIN_TOKEN` to avoid stale credentials. If you want to use a multi-token file in production, provide it securely at runtime.

## 5) Break-glass (one-shot)
- For emergencies only. Create `security/breakglass.flag` and use a token with `breakglass: true`. The first successful use consumes the flag and is logged.

## 6) Health, logs, and metrics
- Health endpoints:
  - `/health` → 200
  - `/healthz` and `/readyz` → JSON snapshot; `readyz` verifies writable dirs and token load
  - `/info` → version + readiness + security mode
  - `/metrics` → Prometheus text (requests_total, errors_total, uptime_seconds, etc.)

- Logs (app filesystem):
  - `logs/init.log` → human-readable startup and events
  - `logs/events.log` → structured JSON (access, admin actions, errors) when `ACCESS_LOG_JSON=1`

## 7) Security posture
- Enforced admin mode (`SECURITY_MODE=enforced`)
- HTTPS redirect enforced (`FORCE_HTTPS=1`) with HSTS (preload optional)
- CSRF required for state-changing admin POSTs (Release Now, Trigger CI, Rotate Token)
- Rate limiting on admin routes (window/max/status configurable via env)

## 8) Troubleshooting
- 401 on admin: Check `?token=<ADMIN_TOKEN>` or ensure `FLASK_SECRET` and `ADMIN_TOKEN` are set in Render
- CSRF failures: Ensure you used the form on `/admin` (it injects CSRF) and your browser allows cookies for the site
- Deploy stuck/build_failed: Redeploy via one-click; if persistent, check Render build logs (Docker runtime is used)
- “invalid JSON” on deploy API: The deploy script auto-retries with safe fallbacks
- No logs: Confirm `ACCESS_LOG_JSON=1` and check file permissions on `logs/`

## 9) Operational runbook
- Rotate ADMIN_TOKEN quarterly (or on personnel change):
  1) `.\scripts\bootstrap_secrets.ps1 -Force -ShowHash`
  2) `.\scripts\sync_render_secrets.ps1`
  3) `.\scripts\deploy_oneclick.ps1`
  4) Verify `/admin` loads with the new token.

- After-hours emergency (break-glass):
  1) Place `security/breakglass.flag`
  2) Use break-glass token once
  3) Remove flag if not auto-removed; review `logs/events.log`

- Rolling back a deploy: Trigger a new deploy from main, or tag and redeploy a previous image via Render UI.

---

Last updated: 2025-10-09
