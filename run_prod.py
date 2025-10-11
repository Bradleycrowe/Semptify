import os
from waitress import serve
from SemptifyGUI import app

if __name__ == '__main__':
    # Read host/port from environment with sane defaults
    # Accept both custom SEMPTIFY_PORT and platform-provided PORT (Render/Heroku style)
    host = os.environ.get('SEMPTIFY_HOST', '0.0.0.0')
    port = int(os.environ.get('SEMPTIFY_PORT') or os.environ.get('PORT', '8080'))

    # Ensure runtime folders exist (app already does this on import but keep-safe)
    folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    threads = int(os.environ.get('SEMPTIFY_THREADS', '8'))
    backlog = int(os.environ.get('SEMPTIFY_BACKLOG', '1024'))
    print(f"Starting SemptifyGUI (production) on {host}:{port} threads={threads} backlog={backlog} (PORT env fallback supported)")
    serve(app, host=host, port=port, threads=threads, backlog=backlog)
