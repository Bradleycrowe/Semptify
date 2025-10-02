# SemptifyGUI

![CI](https://github.com/Bradleycrowe/SemptifyGUI/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/Bradleycrowe/SemptifyGUI/actions/workflows/pages.yml/badge.svg)

Small Flask-based GUI for tenant-justice automation. This repository includes a development server, a production runner (`run_prod.py` using waitress), Docker support, tests, and CI workflows.

Quick Start (Automated Setup)

For a complete automated setup that creates the venv, installs dependencies, runs tests, and starts the service:

```powershell
Set-Location -LiteralPath 'd:\Semptify\SemptifyGUI'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\full_setup.ps1
```

This script will:
- Create a Python virtual environment (if needed)
- Install all dependencies
- Run tests
- Start the production service in the background
- If run as Administrator: Register a Scheduled Task for auto-start at logon

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

Service Management

After running the automated setup, you can manage the service using:

```powershell
# Check service status
.\scripts\status_service.ps1

# Stop the service
.\scripts\stop_service.ps1

# Restart the service
.\scripts\stop_service.ps1
.\scripts\start_service.ps1

# View service logs
Get-Content logs\out.log -Tail 20
Get-Content logs\err.log -Tail 20
```

CI and Releases

- GitHub Actions runs tests and builds images on push/PR.
- On tag pushes the workflow scans the image with Trivy, generates an SBOM with Syft, publishes images to GHCR (and optionally Docker Hub), and creates a GitHub Release with artifacts (image-info, SBOM, Trivy SARIF).

If you need me to add deploy manifests (Kubernetes/Helm) or automated tagging, tell me and I will add them.
