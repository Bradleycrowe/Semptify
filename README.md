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
