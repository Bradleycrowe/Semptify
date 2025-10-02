import os
from waitress import serve
from SemptifyGUI import app

if __name__ == '__main__':
    # Read host/port from environment with sane defaults
    host = os.environ.get('SEMPTIFY_HOST', '0.0.0.0')
    port = int(os.environ.get('SEMPTIFY_PORT', '8080'))

    # Required folders
    folders = ["uploads", "logs", "copilot_sync", "final_notices", "security", "sbom"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print(f"Starting SemptifyGUI (production) on {host}:{port}")
    serve(app, host=host, port=port)
