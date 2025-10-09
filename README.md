# SemptifyGUI

![CI](https://github.com/Bradleycrowe/SemptifyGUI/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/Bradleycrowe/SemptifyGUI/actions/workflows/pages.yml/badge.svg)

Small Flask-based GUI for tenant-justice automation. This repository includes a development server, a production runner (`run_prod.py` using waitress), Docker support, tests, and CI workflows.

Getting started (development)

```powershell
Set-Location -LiteralPath 'd:\Semptify\SemptifyGUI'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\SemptifyGUI.py
```

Running in production (waitress)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\run_prod.py
```

Docker

```powershell
docker build -t semptifygui:latest .
docker run --rm -p 8080:8080 semptifygui:latest
```

Tests

```powershell
.\.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest -q
```

CI and Releases

- GitHub Actions runs tests and builds images on push/PR.
- On tag pushes the workflow scans the image with Trivy, generates an SBOM with Syft, publishes images to GHCR (and optionally Docker Hub), and creates a GitHub Release with artifacts (image-info, SBOM, Trivy SARIF).

If you need me to add deploy manifests (Kubernetes/Helm) or automated tagging, tell me and I will add them.

## Test Mode Release Simulation

In test mode (Flask `app.config['TESTING']=True`) when `GITHUB_TOKEN` is absent, `/release_now` creates a simulated tag (`vTEST-<timestamp>`) locally and records it in `logs/release-log.json` with `"simulated": true` instead of calling the GitHub API.

## Security Modes

`SECURITY_MODE` controls admin protection:

- `open` (default): Admin routes do not require the `ADMIN_TOKEN`, but each access is logged with an `OPEN_MODE` entry.
- `enforced`: Admin routes require the `ADMIN_TOKEN` (passed as `?token=...` or `X-Admin-Token` header).

Change mode by setting the environment variable before starting the app or updating the Render service env vars.

### Multi-Token & Break-Glass (Advanced)

Create `security/admin_tokens.json` (not committed) with entries:

```jsonc
[
  { "id": "primary", "hash": "sha256:<hash-of-token>", "enabled": true },
  { "id": "ops-breakglass", "hash": "sha256:<hash-of-token>", "enabled": true, "breakglass": true }
]
```

Generate a hash (PowerShell example):

```powershell
$raw = 'SuperSecretTokenValue'
$hash = (python - <<'PY'
import hashlib,os
print('sha256:' + hashlib.sha256(os.environ['RAW'].encode()).hexdigest())
PY
)
```

Or via Python directly in a REPL:

```python
import hashlib
print('sha256:' + hashlib.sha256(b'SuperSecretTokenValue').hexdigest())
```

Break-glass activation: create an empty file `security/breakglass.flag` on the server. The next request using a token marked `"breakglass": true` will authenticate and remove the flag (one-shot). All events append structured JSON lines in `logs/events.log`.

### CSRF Protection (Enforced Mode)

When `SECURITY_MODE=enforced`, all state-changing admin POST routes (`/release_now`, `/trigger_workflow`, `/rotate_token`) require a valid session CSRF token:

1. Browser (or test client) first performs a GET to `/admin` with a valid admin token to establish a session.
2. A hidden field `csrf_token` is included in the admin forms.
3. POST requests missing or with an invalid CSRF token return `400 CSRF validation failed`.

In `open` mode CSRF validation is skipped to keep friction low during early adoption / public demo.

### Rate Limiting

Admin routes apply a sliding-window rate limit (default 60 requests / 60 seconds / (IP, path) tuple). Configure via env vars:

yADMIN_RATE_STATUS=429  # HTTP status for limited requests (override if an upstream expects 503)
```
ADMIN_RATE_WINDOW=60    # window seconds
ADMIN_RATE_MAX=60       # max requests per window
ADMIN_RATE_STATUS=429   # HTTP status for limited requests (override if an upstream expects 503)
ADMIN_RATE_RETRY_AFTER=60 # (optional) seconds clients should wait before retry (defaults to ADMIN_RATE_WINDOW)
```

When exceeded the attempt is logged (`rate_limited`) and increments `rate_limited_total`. Responses now include:

```jsonc
{
  "error": "rate_limited",
  "retry_after": 60
}
```

And a `Retry-After` header with the same number of seconds. Unauthorized admin attempts return:

```json
{ "error": "unauthorized" }
```

HTML admin UI accesses still render templates; API/automation clients should inspect status codes (401 vs 429/ configured) and JSON body.

### Readiness Endpoint

`/readyz` performs writable checks for runtime directories and (if present) attempts to load the token file. Returns 200 with `{ "status": "ready" }` on success, or 503 with `{ "status": "degraded" }` if any directory is not writable or tokens fail to load.

### Extended Metrics

The `/metrics` endpoint (Prometheus plaintext) now exposes counters with HELP/TYPE preambles:

- `requests_total`
- `admin_requests_total`
- `admin_actions_total` (mutating operations)
- `errors_total`
- `releases_total`
- `rate_limited_total`
- `breakglass_used_total`
- `token_rotations_total`

### Admin Status Endpoint

`/admin/status` (GET) returns a JSON snapshot (requires auth in enforced mode):

```jsonc
{
  "security_mode": "enforced",
  "metrics": { "requests_total": 42, ... },
  "tokens": [ { "id": "primary", "breakglass": false } ],
  "time": "2025-10-08T12:34:56.789Z"
}
```

### Token Rotation

Rotate an existing entry in `security/admin_tokens.json` via the admin UI Rotate Token form. This updates the token hash atomically and increments `token_rotations_total`. (In enforced mode, CSRF + admin token are both required.)

## Render Deployment

The `render.yaml` describes the service. Key env vars:

- `SEMPTIFY_PORT`: internal port (default 8080)
- `ADMIN_TOKEN`: only required once you switch to enforced mode
- `SECURITY_MODE`: `open` or `enforced`

After a push to `main`, Render auto deploys (if configured). Health check: `/health`.

### Post-Deploy Smoke Test

Use the provided PowerShell script:

```powershell
./RenderSmokeTest.ps1 -BaseUrl https://semptifygui.onrender.com
```

If in enforced mode:

```powershell
RenderSmokeTest.ps1 -BaseUrl https://semptifygui.onrender.com -AdminToken YOUR_ADMIN_TOKEN
```

Outputs will confirm health, version metadata, and admin banner (OPEN or ENFORCED).

### Sample Admin Automation (CI / Status Polling)

Poll `/admin/status` for real-time dashboards:

```powershell
Invoke-RestMethod "https://<your-app>/admin/status?token=$env:ADMIN_TOKEN" | ConvertTo-Json -Depth 4
```

### Offline / PWA Support

The app ships a service worker + manifest, maskable icon, and dark/light theme toggle. The `/offline` route serves a fallback message when the network is unavailable. Future iterations may add richer offline caching (admin read-only panel).

---

## Roadmap (Open Doors → Fully Functional)

- [x] Multi-token & break-glass auth
- [x] CSRF protection (enforced mode)
- [x] Rate limiting + metrics
- [x] Structured event logging
- [x] PWA manifest + service worker offline fallback
- [ ] Rich offline admin panel subset (read-only)
- [ ] SBOM diff alerting
- [ ] Semantic version tagging automation
- [ ] Expanded test coverage for security edge cases

Contributions or feature requests: open an issue or describe the desired end-user workflow and the automation you want.

## Open Doors Checklist

Validate these before public production exposure:

1. **Secrets & Auth**
   - FLASK_SECRET strong random
   - Multi-token file present (if enforced) and stored securely
   - GITHUB_TOKEN configured (if using release UI)
2. **Security Mode**
   - SECURITY_MODE explicitly set (avoid implicit default)
3. **Rate Limiting**
   - ADMIN_RATE_WINDOW / ADMIN_RATE_MAX tuned
4. **Observability**
   - /metrics scraped; logs/events.log ingestion working
5. **Supply Chain**
   - Trivy scan passes (no unresolved CRITICAL/HIGH)
   - SBOM artifact attached; diff reviewed
6. **PWA / UX**
   - Icons + manifest valid; offline route reachable
7. **Admin Ops**
   - /admin/status returns healthy snapshot
   - Token rotation and (if needed) break-glass validated
8. **Health & Readiness**
   - /health, /healthz, /readyz 200 (simulate a failure to observe 503)
9. **Backups**
   - Secure copy of token file & essential logs (policy permitting)
10. **Automation**
    - Post-deploy smoke workflow green

## Environment Configuration

An `.env.example` file documents common variables. For local development:

```bash
cp .env.example .env
```

The app auto-loads `.env` at import time (without overriding already-set environment variables). Never commit real secrets.

## WSL Quick Setup

You can bootstrap a working SemptifyGUI environment inside Ubuntu on WSL2 with the helper script:

```bash
bash scripts/wsl_setup.sh            # basic Python env
bash scripts/wsl_setup.sh --force-venv  # recreate venv if needed
bash scripts/wsl_setup.sh --with-docker # also install Docker Engine (optional)
```

The script will:

1. Install required apt packages (python3, venv, build tools, git).
2. Clone or update this repository.
3. Create / reuse a `.venv` and install `requirements.txt`.
4. Run a light smoke test subset.
5. Print next‑step commands for dev (`python SemptifyGUI.py`) or prod (`python run_prod.py`).

Environment variables for security modes (examples):

```bash
export SECURITY_MODE=open
export ADMIN_TOKEN=changeme
export FLASK_SECRET=$(python - <<PY
import secrets; print(secrets.token_hex(32))
PY
)
```

If you pass `--with-docker`, the script installs Docker Engine under WSL; log out/in (or restart WSL) to activate group membership.

### Windows Wrapper

From PowerShell you can call a convenience wrapper instead of remembering bash flags:

```powershell
pwsh ./scripts/wsl_setup.ps1 -WithDocker -ForceVenv -Dir /mnt/d/Semptify/SemptifyGUI
```

### Docker Verification inside WSL

After enabling Docker (and restarting WSL session):

```bash
bash scripts/wsl_docker_verify.sh
```

It pulls `hello-world`, prints a short run excerpt, and (if the repo has a `Dockerfile`) builds a local image `semptifygui:local`.

### GitHub Codespaces / Dev Container

This repo includes a `.devcontainer/devcontainer.json` for a ready-to-code environment:

What happens on creation:
1. Base image: `mcr.microsoft.com/devcontainers/python:3.13`.
2. Installs requirements.
3. Runs pytest (non-fatal if failures) for quick feedback.
4. Provides Pylance + Python extensions.

To use locally with VS Code + Dev Containers extension:

1. Install the Dev Containers extension.
2. Command Palette: "Dev Containers: Reopen in Container".
3. On first build it seeds dependencies and runs the smoke tests.

Environment variables (e.g. `SECURITY_MODE`, `ADMIN_TOKEN`) can be added via a `.env` file or the devcontainer JSON `containerEnv` property if needed.

