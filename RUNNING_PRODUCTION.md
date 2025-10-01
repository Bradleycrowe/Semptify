# Production runner and deployment notes

This project is a small Flask app. The development server (`app.run(debug=True)`) is suitable for development only. Use the included `run_prod.py` with a production WSGI server.

Quick start (venv active):

```powershell
pip install -r requirements.txt
# Run on port 8080 (binds all interfaces)
$env:SEMPTIFY_PORT=8080
python .\run_prod.py
```

Environment variables

- `SEMPTIFY_HOST` — host to bind (default: `0.0.0.0`)
- `SEMPTIFY_PORT` — port to listen on (default: `8080`)

Notes

- `security/` may contain keys or secrets. Mount secrets at runtime; do not commit them to git.
- The app writes to disk; configure persistent storage for `uploads/`, `final_notices/`, and `logs/` in production.
- Consider placing the app behind a reverse proxy (nginx, IIS) for TLS, rate limiting, and static asset serving.

## Docker (recommended for small deployments)

Build the image locally:

```powershell
Set-Location -LiteralPath 'd:\Semptify\SemptifyGUI'
docker build -t semptifygui:latest .
```

Run with Docker (bind port 8080):

```powershell
docker run --rm -p 8080:8080 \
  -v ${PWD}:/app \
  -v ${PWD}\\uploads:/app/uploads \
  -v ${PWD}\\logs:/app/logs \
  semptifygui:latest
```

Or use docker-compose:

```powershell
docker-compose up --build
```

Notes:

- `.dockerignore` excludes runtime and secret folders from the build context.
- Volumes in `docker-compose.yml` map runtime folders to host for persistence and inspection.
