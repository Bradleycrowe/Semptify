#!/usr/bin/env bash
set -euo pipefail

# SemptifyGUI WSL bootstrap script
# Idempotent helper to provision dependencies, virtualenv, and run a smoke test
# Usage:
#   bash scripts/wsl_setup.sh                # basic python environment
#   bash scripts/wsl_setup.sh --with-docker  # additionally install docker engine (WSL2 Ubuntu)
#   bash scripts/wsl_setup.sh --force-venv   # recreate virtualenv even if it exists
#
# Safe to re-run; will skip steps that are already satisfied.

REPO_GIT="https://github.com/Bradleycrowe/SemptifyGUI.git"
PROJECT_NAME="SemptifyGUI"
DEFAULT_WIN_PATH="/mnt/d/Semptify/${PROJECT_NAME}"  # Adjust if your code is elsewhere
TARGET_DIR=""
WITH_DOCKER=0
FORCE_VENV=0

for arg in "$@"; do
	case "$arg" in
		--with-docker) WITH_DOCKER=1 ; shift ;;
		--force-venv) FORCE_VENV=1 ; shift ;;
		--dir=*) TARGET_DIR="${arg#*=}" ; shift ;;
		-h|--help)
			grep '^#' "$0" | sed 's/^# \{0,1\}//'
			exit 0 ;;
	esac
done

echo "[INFO] Starting WSL setup for ${PROJECT_NAME}"

# -------- Detect WSL / distro --------
if ! grep -qi 'microsoft' /proc/version; then
	echo "[WARN] This does not look like WSL. Continuing anyway." >&2
fi

if ! command -v apt >/dev/null 2>&1; then
	echo "[ERROR] This script expects an apt-based distro (Ubuntu/Debian)." >&2
	exit 1
fi

# -------- Choose target directory --------
if [[ -z "$TARGET_DIR" ]]; then
	if [[ -d "$DEFAULT_WIN_PATH/.git" ]]; then
		TARGET_DIR="$DEFAULT_WIN_PATH"
	else
		TARGET_DIR="$HOME/${PROJECT_NAME}"
	fi
fi
echo "[INFO] Target directory: $TARGET_DIR"

# -------- Packages --------
echo "[INFO] Updating apt metadata (sudo required)"
sudo apt update -y
echo "[INFO] Installing base packages"
sudo apt install -y --no-install-recommends \
	python3 python3-venv python3-pip git ca-certificates curl build-essential

if [[ $WITH_DOCKER -eq 1 ]]; then
	echo "[INFO] Installing Docker (engine + CLI)"
	if ! command -v docker >/dev/null 2>&1; then
		# Reference: https://docs.docker.com/engine/install/ubuntu/
		sudo apt install -y apt-transport-https gnupg lsb-release
		curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker.gpg
		echo \
			"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
			$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
		sudo apt update -y
		sudo apt install -y docker-ce docker-ce-cli containerd.io
		sudo usermod -aG docker "$USER" || true
		echo "[INFO] Docker installed. You may need to log out/in for group changes to apply."
	else
		echo "[INFO] Docker already present; skipping."
	fi
fi

# -------- Clone or reuse repo --------
if [[ -d "$TARGET_DIR/.git" ]]; then
	echo "[INFO] Existing git repo detected. Pulling latest main."
	(cd "$TARGET_DIR" && git fetch --all --prune && git checkout main && git pull --ff-only) || echo "[WARN] Git pull failed; continuing."
else
	echo "[INFO] Cloning repository into $TARGET_DIR"
	mkdir -p "$(dirname "$TARGET_DIR")"
	git clone "$REPO_GIT" "$TARGET_DIR"
fi

cd "$TARGET_DIR"

# -------- Python virtual environment --------
if [[ -d .venv ]] && [[ $FORCE_VENV -eq 1 ]]; then
	echo "[INFO] --force-venv specified; removing existing .venv"
	rm -rf .venv
fi

if [[ ! -d .venv ]]; then
	echo "[INFO] Creating virtualenv (.venv)"
	python3 -m venv .venv
fi

echo "[INFO] Upgrading pip & installing requirements"
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# -------- Smoke tests --------
if command -v pytest >/dev/null 2>&1; then
	echo "[INFO] Running quick test subset (index + health)"
	pytest -q tests/test_app.py::test_index tests/test_admin_open_mode.py::test_admin_open_mode_access || echo "[WARN] Some tests failed (non-blocking)."
else
	echo "[INFO] pytest not available; skipping tests"
fi

# -------- Run guidance --------
cat <<'EOF'

[DONE] SemptifyGUI environment prepared.

To run the development server inside WSL now:
	source .venv/bin/activate
	python SemptifyGUI.py

Then visit: http://127.0.0.1:5000

Production-style (waitress):
	source .venv/bin/activate
	python run_prod.py

Environment variables (examples):
	export SECURITY_MODE=open
	export ADMIN_TOKEN=changeme
	export FLASK_SECRET=$(python - <<PY
import secrets; print(secrets.token_hex(32))
PY
	)

If you enabled Docker and just added your user to the docker group, restart your WSL session for group membership to refresh.
EOF

echo "[INFO] Script complete"
