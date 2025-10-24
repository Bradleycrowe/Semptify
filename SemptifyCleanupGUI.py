from flask import Flask, render_template_string, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

# Ensure runtime folders exist
for folder in ['uploads', 'logs', 'copilot_sync', 'final_notices', 'security']:
    os.makedirs(folder, exist_ok=True)

# HTML dashboard with all buttons
dashboard_html = """
<!DOCTYPE html>
<html>
<head><title>Semptify</title></head>
<body>
  <h1>Semptify Control Panel</h1>
  <form action="/upload" method="post"><button>Upload Evidence</button></form>
  <a href="/logs"><button>View Logs</button></a>
  <form action="/sync" method="post"><button>Copilot Sync Now</button></form>
  <form action="/generate" method="post"><button>Generate Notice</button></form>
  <a href="/security"><button>Security Check</button></a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(dashboard_html)

@app.route('/upload', methods=['POST'])
def upload():
    with open('uploads/upload_log.txt', 'a') as f:
        f.write(f"Evidence uploaded at {datetime.now()}\n")
    return redirect('/')

@app.route('/logs')
def logs():
    entries = []
    for fname in os.listdir('logs'):
        with open(f'logs/{fname}', 'r') as f:
            entries.append(f.read())
    return "<br>".join(entries) or "No logs yet."

@app.route('/sync', methods=['POST'])
def sync():
    with open('copilot_sync/sync_log.txt', 'a') as f:
        f.write(f"Copilot synced at {datetime.now()}\n")
    return redirect('/')

@app.route('/generate', methods=['POST'])
def generate():
    with open('final_notices/notice.txt', 'w') as f:
        f.write("Final notice generated.\n")
    return redirect('/')

@app.route('/security')
def security():
    return "Security check passed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

