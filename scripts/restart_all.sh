#!/usr/bin/env bash
set -euo pipefail
# Full clean restart helper for Semptify (Linux/WSL)
# Flags:
#   --force-venv      Recreate venv
#   --prod            Run run_prod.py after setup
#   --keep-logs       Keep existing logs directory contents
#   --gen-token       Generate random ADMIN_TOKEN for session
#   --enforced        Set SECURITY_MODE=enforced (default open)
#   --skip-tests      Skip pytest
#   --auto-start      Start server automatically
# Usage: ./scripts/restart_all.sh --force-venv --gen-token --enforced --auto-start --prod

force_venv=0
prod=0
keep_logs=0
gen_token=0
enforced=0
skip_tests=0
auto_start=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force-venv) force_venv=1 ; shift ;;
    --prod) prod=1 ; shift ;;
    --keep-logs) keep_logs=1 ; shift ;;
    --gen-token) gen_token=1 ; shift ;;
    --enforced) enforced=1 ; shift ;;
    --skip-tests) skip_tests=1 ; shift ;;
    --auto-start) auto_start=1 ; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

info(){ echo -e "\e[36m[*]\e[0m $*"; }
ok(){ echo -e "\e[32m[+]\e[0m $*"; }
warn(){ echo -e "\e[33m[!]\e[0m $*"; }
err(){ echo -e "\e[31m[x]\e[0m $*"; }

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"
info "Repo root: $repo_root"

if [[ $force_venv -eq 1 && -d .venv ]]; then
  info "Removing existing venv"
  rm -rf .venv
fi
if [[ ! -d .venv ]]; then
  info "Creating venv"
  python -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
info "Upgrading pip"
python -m pip install --upgrade pip >/dev/null
info "Installing requirements"
pip install -r requirements.txt

runtime_dirs=(uploads logs copilot_sync final_notices)
for d in "${runtime_dirs[@]}"; do
  mkdir -p "$d"
  if [[ $d == logs && $keep_logs -eq 1 ]]; then
    info "Keeping existing logs"
    continue
  fi
  info "Purging $d/*"
  find "$d" -mindepth 1 -maxdepth 1 -exec rm -rf {} + || true
done

mkdir -p security
if [[ $gen_token -eq 1 ]]; then
  export ADMIN_TOKEN="$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 48)"
  ok "Generated ADMIN_TOKEN (not persisted)"
fi
if [[ -z "${FLASK_SECRET:-}" ]]; then
  export FLASK_SECRET="$(python - <<'PY'
import secrets;print(secrets.token_hex(64))
PY
)"
  ok "Generated FLASK_SECRET"
fi
export SECURITY_MODE=$([[ $enforced -eq 1 ]] && echo enforced || echo open)
info "SECURITY_MODE=$SECURITY_MODE"

if [[ $skip_tests -ne 1 ]]; then
  info "Running tests"
  if python -m pytest -q; then
    ok "Tests passed"
  else
    err "Tests failed"; exit 3
  fi
else
  warn "Skipping tests"
fi

if [[ $auto_start -eq 1 ]]; then
  if [[ $prod -eq 1 ]]; then
    info "Starting production server (waitress)"
    exec python run_prod.py
  else
    info "Starting development server (Flask debug)"
    exec python Semptify.py
  fi
else
  ok "Restart sequence complete. Use --auto-start to run automatically."
  echo "Manual start (dev): source .venv/bin/activate; python Semptify.py"
  echo "Manual start (prod): source .venv/bin/activate; python run_prod.py"
fi

