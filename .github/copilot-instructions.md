# Copilot Instructions for SemptifyGUI

Concise, actionable guide for AI coding agents working on SemptifyGUI — a small Flask-based GUI/web app for tenant-justice automation. Include only patterns and commands that are discoverable from the repository.

## Quick architecture snapshot
- Entry point: `SemptifyGUI.py` — a single-process Flask app (calls `app.run(debug=True)`).
- Runtime-created folders (the app ensures these exist at startup): `uploads`, `logs`, `copilot_sync`, `final_notices`, `security`.
- High-level flow: HTTP route → filesystem write/read (uploads, final notices) → append logs (`logs/init.log`) → return response.

## Concrete signals & examples (from `SemptifyGUI.py`)
- Folder creation is idempotent:

  ```py
  folders = ["uploads","logs","copilot_sync","final_notices","security"]
  for folder in folders:
      if not os.path.exists(folder):
          os.makedirs(folder)
  ```

- Initialization log append (follow this format for audit entries):

  ```py
  with open(os.path.join("logs","init.log"), "a") as f:
      f.write(f"[{timestamp}] SemptifyGUI initialized with folders: {', '.join(folders)}\n")
  ```

- The app imports `render_template` and `send_file` but currently returns inline HTML on `/` — add `templates/` and `static/` when you introduce pages or assets.

## How to run (Windows PowerShell, minimal)
Recommended: use a venv and install Flask. Run these from the repository root (`d:\Semptify\SemptifyGUI`).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Flask
python .\SemptifyGUI.py
```

Then verify index in another terminal:

```powershell
.\.venv\Scripts\Activate.ps1
Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing | Select-Object -ExpandProperty Content
```

Expected quick check: the response contains "SemptifyGUI is live. Buttons coming next." and `logs/init.log` has a timestamped entry.

## Project-specific conventions & notes
- Keep the runtime folder-creation and logging behavior when refactoring — other scripts and agents rely on these directories being present.
- `security/` is for keys and sensitive material; treat it as secrets: do not commit. Add it to `.gitignore` if not already ignored.
- When adding UI, put Jinja templates under `templates/` and static assets under `static/` (Flask conventions; `render_template` is already imported).
- File-serving or downloads should use `send_file` (already imported in `SemptifyGUI.py`). Serve only sanitized, access-controlled files (specially in `uploads/` and `final_notices/`).

## Integration points & dependencies
- External runtime dependency: Flask (no `requirements.txt` present). If you add dependencies, create a top-level `requirements.txt`.
- The app writes to disk — CI or runners must give the workspace write permissions.

## Contribution guidance for AI agents
- Preserve the core startup behavior: folder creation + `logs/init.log` append.
- When adding routes, mirror existing naming and folder layout. Example: new route that writes a notice should place generated files in `final_notices/` and append a log entry to `logs/init.log`.
- Avoid committing anything under `security/` or large binary files in `uploads/` and `copilot_sync/`.

## Safe quick tasks an AI agent can do now
- Add `requirements.txt` with `Flask`.
- Add `templates/index.html` and switch `index()` to `render_template("index.html")`.
- Add a tiny test using Flask's test client (under `tests/test_app.py`) that asserts `/` returns 200 and expected HTML.

If anything above is unclear or you want me to implement one of the safe quick tasks, tell me which and I'll proceed.
