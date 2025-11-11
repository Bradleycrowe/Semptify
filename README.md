$report = @()
$expectedDirs = @("modules", "templates", "static", "uploads", "logs", "security", "copilot_sync", "final_notices", "tests", ".github", "admin_tools")
$expectedFiles = @("Semptify.py", "run_prod.py", "requirements.txt", "README.md")

$report += "=== Directory Inventory ==="
Get-ChildItem -Directory | ForEach-Object {
    if ($expectedDirs -notcontains $_.Name) {
        $report += "⚠️  Unexpected directory: $($_.Name)"
    } else {
        $report += "✔ $($_.Name)"
    }
}

$report += "`n=== File Inventory ==="
Get-ChildItem -File | ForEach-Object {
    if ($expectedFiles -notcontains $_.Name) {
        $report += "⚠️  Unexpected file: $($_.Name)"
    } else {
        $report += "✔ $($_.Name)"
    }
}

$report += "`n=== Runtime Directory Check ==="
foreach ($dir in $expectedDirs) {
    if (!(Test-Path $dir)) {
        $report += "❌ Missing runtime dir: $dir"
    } else {
        $report += "✔ $dir exists"
    }
}

$report += "`n=== Module Inventory ==="
Get-ChildItem -Path "modules" -Recurse -Include *.py | ForEach-Object { $report += $_.FullName }

$report += "`n=== Template Inventory ==="
Get-ChildItem -Path "templates" -Recurse -Include *.html | ForEach-Object { $report += $_.FullName }

$report += "`n=== Static Asset Inventory ==="
Get-ChildItem -Path "static" -Recurse | ForEach-Object { $report += $_.FullName }

$report += "`n=== Notes, TODOs, and Instructions ==="
$searchPatterns = @("TODO", "NOTE", "INSTRUCTION", "FIXME")
foreach ($pattern in $searchPatterns) {
    $report += "`n--- $pattern ---"
    Get-ChildItem -Path . -Recurse -Include *.py,*.html,*.md | ForEach-Object {
        $matches = Select-String -Path $_.FullName -Pattern $pattern
        foreach ($m in $matches) {
            $report += "$($m.Path): $($m.Line)"
        }
    }
}

$reportPath = "admin_tools\full_inventory_report.txt"
$report | Set-Content $reportPath

Write-Host "`nFull inventory report saved to $reportPath"
Write-Host "Review this file for missing items, notes, TODOs, and instructions."# Semptify

![CI](https://github.com/Bradleycrowe/Semptify/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/Bradleycrowe/Semptify/actions/workflows/pages.yml/badge.svg)

Small Flask-based GUI for tenant-justice automation. This repository includes a development server, a production runner (`run_prod.py` using waitress), Docker support, tests, and CI workflows.

## 📁 Documentation Structure (Organized)

Related markdown files have been relocated under `docs/` for easier navigation:

- `docs/calendar/` – Calendar logic, components, delivery guides
- `docs/adaptive/` – Adaptive intensity, learning, system summaries
- `docs/deployment/` – Deployment checklists, CI/CD, environment setup
- `docs/render/` – Render-specific deployment and verification guides
- `docs/route-discovery/` – Route discovery architecture, manifests, summaries
- `docs/gui/` – GUI implementation strategy, device detection, verification
- `docs/security/` – Security policy and operational security references

If you had bookmarks to the previous root-level `CALENDAR_*.md`, `ADAPTIVE_*.md`, `DEPLOYMENT_*.md`, `RENDER_*.md`, `ROUTE_DISCOVERY_*.md`, `GUI_*.md`, or `SECURITY*.md` files, update them to point to the new folder paths.

Planned next steps:
- Consolidate architecture docs into `docs/architecture/`
- Introduce `docs/guides/` for quick start workflow guides
- Generate an index file (`docs/INDEX.md`) linking all major topic areas

Feel free to request additional categorization if a topic feels scattered.

Getting started (development)

```powershell
Set-Location -LiteralPath 'd:\Semptify\Semptify'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\Semptify.py
```

Running in production (waitress)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\run_prod.py
```

Docker

```powershell
docker build -t Semptify:latest .
docker run --rm -p 8080:8080 Semptify:latest
```

## Podman (Rootless)

The dev container now includes Podman. You can switch between Docker and Podman using the `Makefile`:

```bash
make build          # docker build
make build PODMAN=1 # podman build
make run            # run via docker
make run PODMAN=1   # run via podman
```

Direct Podman commands:

```bash
podman build -t Semptify:dev .
podman run --rm -p 8080:8080 Semptify:dev
```

If you prefer docker CLI semantics with podman under the hood:

```bash
alias docker=podman
```

Tests

```powershell
.\.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest -q
```

## Dev server (PowerShell)

Use the provided script to bootstrap a virtual environment, install dependencies, and run the app in open mode:

```powershell
pwsh -File .\scripts\dev_server.ps1
```

Options:

```powershell
# HTTPS self-signed (uses run_dev_ssl.py)
pwsh -File .\scripts\dev_server.ps1 -Https

# Persist runtime dirs under a specific data root
pwsh -File .\scripts\dev_server.ps1 -DataRoot 'D:\Semptify\data'

# Enable JSON access logging
pwsh -File .\scripts\dev_server.ps1 -AccessLog
```

## Run tests from Admin UI

On `/admin`, a Developer Utilities section provides a “Run Tests” button.

- In enforced mode, ensure you access `/admin` with a valid admin token to obtain a CSRF token.
- Clicking the button POSTs to `/admin/run_tests`, executes `pytest -q` with a short timeout, and shows the results inline.
- The HTTP status reflects the outcome (200 on pass, 500 on failure/timeout), making it CI/monitor friendly.

## Scaling and Storage

For horizontal scaling or container restarts, use a shared data root and tune the production server:

- `SEMPTIFY_DATA_ROOT`: Absolute path where runtime folders live
   (`uploads/`, `logs/`, `final_notices/`, `security/`). On startup the app
   changes directory to this path (`chdir`) if set.
- `SEMPTIFY_THREADS`: Number of waitress threads (default from waitress). Increase for more concurrent requests.
- `SEMPTIFY_BACKLOG`: Socket backlog size for pending connections.

Examples (PowerShell):

```powershell
$env:SEMPTIFY_DATA_ROOT = 'D:\Semptify\data'
$env:SEMPTIFY_THREADS = '8'
$env:SEMPTIFY_BACKLOG = '128'
python .\run_prod.py
```

When using Docker/Compose, mount a host directory at `/app` (or specific subfolders) to persist these paths.

## AI Copilot Providers

The Copilot UI `/copilot` can route to multiple providers controlled by environment variables:

- `AI_PROVIDER`: `openai`, `azure`, or `ollama`
- OpenAI: `OPENAI_API_KEY`
- Azure OpenAI: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, optional `AZURE_OPENAI_DEPLOYMENT`
- Ollama (local): `OLLAMA_HOST` (default `http://localhost:11434`), optional `OLLAMA_MODEL` (e.g., `llama3.1:8b`)

Quickstart examples (PowerShell):

OpenAI

```powershell
$env:AI_PROVIDER = 'openai'
$env:OPENAI_API_KEY = '<your-key>'
python .\Semptify.py
```

Azure OpenAI

```powershell
$env:AI_PROVIDER = 'azure'
$env:AZURE_OPENAI_ENDPOINT = 'https://<your-resource>.openai.azure.com/'
$env:AZURE_OPENAI_API_KEY = '<your-key>'
$env:AZURE_OPENAI_DEPLOYMENT = 'gpt-4o-mini'
python .\Semptify.py
```

Ollama (local, recommended for offline/free trials)

```powershell
$env:AI_PROVIDER = 'ollama'
$env:OLLAMA_HOST = 'http://localhost:11434'
$env:OLLAMA_MODEL = 'llama3.1:8b'
python .\Semptify.py
```

Tip: On first model pull, Ollama will download the model. Keep the terminal open until it finishes.

## Remote Online Notarization (RON) – BlueNotary adapter

Semptify includes a provider-agnostic RON flow wired to a BlueNotary adapter. In tests and when `BLUENOTARY_API_KEY` is absent, it runs in a safe mock/simulated mode with no external calls.

Environment:

- `RON_PROVIDER=bluenotary`
- `BLUENOTARY_API_KEY` (optional for live; omitted in tests to use mock)
- `BLUENOTARY_BASE_URL` (optional override)
- `RON_WEBHOOK_SECRET` shared secret used by `/webhooks/ron` for simple verification

User flow:

1. User goes to `/legal_notary` and picks a source file from their Vault.
2. POST `/legal_notary/start` creates a session via the adapter and writes `uploads/vault/<user_id>/ron_<session_id>.json` with status `started`.
3. The user is redirected to the app’s return route (mock) or provider page; on return, `/legal_notary/return` finalizes with status `completed`.
4. Provider webhook (or simulated call) POSTs to `/webhooks/ron` with `{ user_id, session_id, status, evidence_links }` and `X-RON-Signature: <RON_WEBHOOK_SECRET>`, updating the certificate JSON.

Certificates and the source file are included in the Vault export bundle.

Go‑live checklist (RON):

- Set `FORCE_HTTPS=1` in prod and serve behind TLS.
- Set `RON_PROVIDER=bluenotary` and a strong `RON_WEBHOOK_SECRET`.
- Configure the provider to call `https://<your-host>/webhooks/ron` with that secret.
- Validate a full session: start → return → webhook; verify `ron_*.json` contains provider, status, and any evidence links.

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
- `uptime_seconds` (gauge)

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

### Unified Info Endpoint

`/info` returns aggregated metadata (app, git SHA, build time), current security mode, and readiness snapshot in one call for dashboards.

### Structured Access Logging

Enable JSON access logs (one line per request) by setting `ACCESS_LOG_JSON=1`. Each entry includes method, path, status, IP, latency (ms), and `request_id`.

### Request Correlation

Each request receives an `X-Request-Id` header (preserved if a proxy already supplies one). Access log entries include this `request_id` for log correlation.

### Vulnerability Allowlist

Add an optional `security/vuln_allowlist.json` (example provided) to suppress known, time‑bounded CVEs in the vuln delta workflow. Suppressed counts appear in delta output (`new_effective`).

Rotate an existing entry in `security/admin_tokens.json` via the admin UI Rotate Token form. This updates the token hash atomically and increments `token_rotations_total`. (In enforced mode, CSRF + admin token are both required.)

## Render Deployment

The `render.yaml` describes the service. Key env vars:

- `SEMPTIFY_PORT`: internal port (default 8080)
- `ADMIN_TOKEN`: only required once you switch to enforced mode
- `SECURITY_MODE`: `open` or `enforced`

After a push to `main`, Render auto deploys (if configured). Health check: `/health`.

### Deployment checklist & automated config audit

We've added a deployment checklist and a small audit tool to help you verify environment readiness before pushing to Render or other hosts.

- See `docs/deployment_checklist.md` for a Render-focused pre-deploy and post-deploy checklist.
- An example env file is provided at `.env.example` — copy it to `.env` or use the entries to populate your Render service environment variables.
- To scan the repository for environment variable usage, external service hints, and runtime directory checks, run the audit script:

```powershell
.\.venv\Scripts\Activate.ps1
python .\scripts\config_audit.py
```

The script writes `logs/config_audit_report.json` and prints a short summary. Use this to find env vars that must be set in Render and to check writable runtime paths.


### Post-Deploy Smoke Test

Use the provided PowerShell script:

```powershell
./RenderSmokeTest.ps1 -BaseUrl https://Semptify.onrender.com
```

If in enforced mode:

```powershell
RenderSmokeTest.ps1 -BaseUrl https://Semptify.onrender.com -AdminToken YOUR_ADMIN_TOKEN
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

## Help Panel and Ledger

- A floating helper (R button) appears on most pages with Read/Instructions/Notes/To‑Do tabs. Admin can change defaults via `/admin` → Help Panel Settings.
- Notes/To‑Do are stored per page in `localStorage` and won’t be sent to the server.
- A simple rent ledger is available at `/resources/rent_ledger` for authenticated users (token via query/header/form). Entries are saved to `uploads/ledger/<user_id>/ledger.json` and totals are displayed.

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

You can bootstrap a working Semptify environment inside Ubuntu on WSL2 with the helper script:

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
5. Print next‑step commands for dev (`python Semptify.py`) or prod (`python run_prod.py`).

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
pwsh ./scripts/wsl_setup.ps1 -WithDocker -ForceVenv -Dir /mnt/d/Semptify/Semptify
```

### Docker Verification inside WSL

After enabling Docker (and restarting WSL session):

```bash
bash scripts/wsl_docker_verify.sh
```

It pulls `hello-world`, prints a short run excerpt, and (if the repo has a `Dockerfile`) builds a local image `Semptify:local`.

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


## Local HTTPS (dev/testing)

If you need local HTTP to be secured, you can run the app over HTTPS with a self-signed certificate.

1) Generate a dev cert and key (PowerShell with OpenSSL):

```powershell
New-Item -ItemType Directory -Force -Path security | Out-Null
$certBase = "security/dev-local"
openssl req -x509 -nodes -newkey rsa:2048 -keyout "$certBase.key" -out "$certBase.crt" -subj "/CN=localhost" -days 365
```

2) Start the app over HTTPS:

```powershell
.\.venv\Scripts\Activate.ps1
$env:SECURITY_MODE = 'open'
$env:FORCE_HTTPS = '1'
python .\run_dev_ssl.py
```

3) Visit <https://localhost:8443> and accept the self-signed cert. The `/info` endpoint will show `security_mode` and responses will include HSTS headers.

Notes:

- `FORCE_HTTPS=1` enforces HTTPS redirects and adds HSTS headers (also active when a request is already secure via a reverse proxy).
- For production, terminate TLS at your reverse proxy/load balancer and keep using `run_prod.py` behind it.


