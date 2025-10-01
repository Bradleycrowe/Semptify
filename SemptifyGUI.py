from flask import Flask, render_template, request, redirect, send_file
import os
from datetime import datetime

app = Flask(__name__)

# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Log initialization
log_path = os.path.join("logs", "init.log")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_path, "a") as log_file:
    log_file.write(f"[{timestamp}] SemptifyGUI initialized with folders: {', '.join(folders)}\n")

@app.route("/")
def index():
    # Use a Jinja2 template so UI can be extended without changing the route.
    message = "SemptifyGUI is live. Buttons coming next."
    return render_template("index.html", message=message, folders=folders)


@app.route("/health")
def health():
    # Simple health endpoint for readiness checks
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
