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

```
ADMIN_RATE_WINDOW=60   # window seconds
ADMIN_RATE_MAX=60      # max requests per window
```

When exceeded the attempt is logged (`rate_limited`) and increments `rate_limited_total`.

### Extended Metrics

The `/metrics` endpoint (Prometheus plaintext) now exposes:

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
.\n+RenderSmokeTest.ps1 -BaseUrl https://semptifygui.onrender.com
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

The app ships a service worker + manifest. The `/offline` route serves a fallback message when the network is unavailable. Future iterations may add richer offline caching.

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
