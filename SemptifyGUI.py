from flask import Flask, render_template, request, redirect, send_file
import os
from datetime import datetime
import json
import requests
import time

app = Flask(__name__)

# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security", "sbom"]

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


def _append_log(line: str):
    log_path = os.path.join("logs", "init.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {line}\n")


@app.route('/admin', methods=['GET'])
def admin():
    # Simple token check
    token = request.args.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401

    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    ci_url = f"https://github.com/{owner}/{repo}/actions"
    pages_url = f"https://{owner}.github.io/{repo}/"
    return render_template('admin.html', ci_url=ci_url, pages_url=pages_url, folders=folders, admin_token=admin_token)


@app.route('/release_now', methods=['POST'])
def release_now():
    token = request.form.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401

    github_token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    if not github_token:
        _append_log('release_now failed: missing GITHUB_TOKEN')
        return "GITHUB_TOKEN not configured on server", 500

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get latest commit SHA from default branch (main)
    ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main'
    r = requests.get(ref_url, headers=headers)
    if r.status_code != 200:
        _append_log(f'release_now failed: cannot read ref: {r.status_code}')
        return f'Failed to read ref: {r.status_code}', 500
    sha = r.json().get('object', {}).get('sha')

    # Create a timestamped tag
    tag_name = f'v{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    create_ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs'
    payload = { 'ref': f'refs/tags/{tag_name}', 'sha': sha }
    r = requests.post(create_ref_url, headers=headers, json=payload)
    if r.status_code in (201, 200):
        _append_log(f'Created tag {tag_name} via API')
        # record release in release-log.json
        log_path = os.path.join('logs', 'release-log.json')
        entry = { 'tag': tag_name, 'sha': sha, 'timestamp': datetime.utcnow().isoformat() }
        try:
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            data.insert(0, entry)
            with open(log_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            _append_log(f'Failed to write release-log.json: {e}')

        return redirect(f'https://github.com/{owner}/{repo}/releases/tag/{tag_name}')
    else:
        _append_log(f'Failed to create tag: {r.status_code} {r.text}')
        return f'Failed to create tag: {r.status_code}', 500


@app.route('/trigger_workflow', methods=['POST'])
def trigger_workflow():
    token = request.form.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401

    workflow = request.form.get('workflow', 'ci.yml')
    ref = request.form.get('ref', 'main')
    github_token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    if not github_token:
        return "GITHUB_TOKEN not configured", 500

    headers = { 'Authorization': f'token {github_token}', 'Accept': 'application/vnd.github.v3+json' }
    dispatch_url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches'
    payload = { 'ref': ref }
    r = requests.post(dispatch_url, headers=headers, json=payload)
    if r.status_code in (204, 201):
        _append_log(f'Triggered workflow {workflow} on {ref}')
        return redirect(f'https://github.com/{owner}/{repo}/actions')
    else:
        _append_log(f'Failed to trigger workflow {workflow}: {r.status_code} {r.text}')
        return f'Failed to trigger workflow: {r.status_code}', 500


@app.route('/release_history')
def release_history():
    token = request.args.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401
    log_path = os.path.join('logs', 'release-log.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
    else:
        data = []
    return render_template('release_history.html', data=data)


@app.route('/sbom')
def sbom_list():
    token = request.args.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401
    sbom_dir = os.path.join('.', 'sbom')
    files = []
    if os.path.exists(sbom_dir):
        files = sorted(os.listdir(sbom_dir), reverse=True)
    return render_template('sbom_list.html', files=files, admin_token=admin_token)


@app.route('/sbom/<path:filename>')
def sbom_get(filename):
    token = request.args.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN', 'devtoken')
    if token != admin_token:
        return "Unauthorized", 401
    sbom_dir = os.path.join('.', 'sbom')
    path = os.path.join(sbom_dir, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Not found", 404

if __name__ == "__main__":
    app.run(debug=True)
