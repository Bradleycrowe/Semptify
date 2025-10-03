from flask import Flask, render_template, request, redirect, send_file, session
import os
from datetime import datetime, timezone
import json
import requests
import time
from flask_wtf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'please-change-me')

# Session cookie security (set FLASK_COOKIE_SECURE=true in production to enable)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_COOKIE_SECURE', 'False').lower() == 'true'

# Initialize CSRF and Flask-Login
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id: str = 'admin'):
        self.id = id


@login_manager.user_loader
def load_user(user_id: str):
    # Only a single admin user is supported by this simple app and only if ADMIN_PASSWORD is set
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_password and user_id == 'admin':
        return User('admin')
    return None

# Required folders
folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Log initialization
log_path = os.path.join("logs", "init.log")
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
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
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {line}\n")


def _is_admin_authenticated() -> bool:
    """Return True if the current request is authenticated as admin.

    Checks (in order):
    - Flask-Login current_user.is_authenticated
    - legacy session flag 'admin_logged_in'
    - ADMIN_TOKEN provided via query/header/form
    """
    try:
        if current_user and getattr(current_user, 'is_authenticated', False):
            return True
    except Exception:
        pass
    if session.get('admin_logged_in'):
        return True
    # token fallback
    token = request.args.get('token') or request.form.get('token') or request.headers.get('X-Admin-Token')
    admin_token = app.config.get('ADMIN_TOKEN') or os.environ.get('ADMIN_TOKEN')
    if admin_token and token == admin_token:
        return True
    return False


@app.route('/admin', methods=['GET'])
def admin():
    # Allow Flask-Login session OR legacy session flag OR token for scripts
    if not _is_admin_authenticated():
        return "Unauthorized", 401

    owner = os.environ.get('GITHUB_OWNER', 'Bradleycrowe')
    repo = os.environ.get('GITHUB_REPO', 'SemptifyGUI')
    ci_url = f"https://github.com/{owner}/{repo}/actions"
    pages_url = f"https://{owner}.github.io/{repo}/"
    return render_template('admin.html', ci_url=ci_url, pages_url=pages_url, folders=folders)


@app.route('/release_now', methods=['POST'])
@csrf.exempt
def release_now():
    if not _is_admin_authenticated():
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

    # Create a timestamped tag (use timezone-aware UTC)
    tag_name = f'v{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")}'
    create_ref_url = f'https://api.github.com/repos/{owner}/{repo}/git/refs'
    payload = { 'ref': f'refs/tags/{tag_name}', 'sha': sha }
    r = requests.post(create_ref_url, headers=headers, json=payload)
    if r.status_code in (201, 200):
        _append_log(f'Created tag {tag_name} via API')
        # record release in release-log.json
        log_path = os.path.join('logs', 'release-log.json')
        entry = { 'tag': tag_name, 'sha': sha, 'timestamp': datetime.now(timezone.utc).isoformat() }
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
@csrf.exempt
def trigger_workflow():
    if not _is_admin_authenticated():
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
    if not _is_admin_authenticated():
        return "Unauthorized", 401
    log_path = os.path.join('logs', 'release-log.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
    else:
        data = []
    return render_template('release_history.html', data=data)


@app.route('/release_log_raw')
def release_log_raw():
    """Return the raw release-log.json contents (protected by admin auth)."""
    if not _is_admin_authenticated():
        return "Unauthorized", 401
    log_path = os.path.join('logs', 'release-log.json')
    if os.path.exists(log_path):
        return send_file(log_path, as_attachment=True)
    return "Not found", 404


@app.route('/sbom')
def sbom_list():
    if not _is_admin_authenticated():
        return "Unauthorized", 401
    sbom_dir = os.path.join('.', 'sbom')
    files = []
    if os.path.exists(sbom_dir):
        files = sorted(os.listdir(sbom_dir), reverse=True)
    return render_template('sbom_list.html', files=files)


@app.route('/sbom/<path:filename>')
def sbom_get(filename):
    if not _is_admin_authenticated():
        return "Unauthorized", 401
    sbom_dir = os.path.join('.', 'sbom')
    # Prevent path traversal
    requested_path = os.path.abspath(os.path.join(sbom_dir, filename))
    if not requested_path.startswith(os.path.abspath(sbom_dir) + os.sep) and os.path.abspath(sbom_dir) != requested_path:
        return "Invalid path", 400
    if os.path.exists(requested_path) and os.path.isfile(requested_path):
        return send_file(requested_path, as_attachment=True)
    return "Not found", 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_password and password == admin_password:
            # Login via Flask-Login
            user = User('admin')
            login_user(user)
            # preserve legacy flag for compatibility
            session['admin_logged_in'] = True
            return redirect('/admin')
        return "Invalid credentials", 403
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    try:
        logout_user()
    except Exception:
        pass
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/cleanup', methods=['GET', 'POST'])
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
