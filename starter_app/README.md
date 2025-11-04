starter_app — minimal Flask starter scaffold

This folder contains a minimal Flask application and a tiny pytest to exercise the root endpoint.

Structure
- starter_app/: Python package with the Flask app
- tests/: pytest tests for the app
- requirements.txt: runtime and test deps

Quick start (PowerShell):

Set-Location -LiteralPath "$(Split-Path -LiteralPath $MyInvocation.MyCommand.Definition -Parent)"
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -m starter_app

Run tests (after installing deps):
pytest -q tests

Next steps
- Add CI to run tests and linting
- Add configuration and logging
- Consider adding a Dockerfile and health endpoints
