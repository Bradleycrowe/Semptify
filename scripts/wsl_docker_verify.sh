#!/usr/bin/env bash
set -euo pipefail

# Lightweight Docker verification for WSL environment.
# Ensures docker CLI works, tests pulling hello-world, and (optional) builds local image.

echo "[INFO] Checking docker availability"
if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] docker not found. Re-run wsl_setup.sh with --with-docker or install manually." >&2
  exit 1
fi

echo "[INFO] Docker version: $(docker --version || true)"

echo "[INFO] Running 'docker info' (may require permissions if group not applied yet)"
if ! docker info >/dev/null 2>&1; then
  echo "[WARN] 'docker info' failed. If you just added your user to the docker group, restart WSL (wsl --shutdown)." >&2
else
  echo "[OK] docker info succeeded"
fi

echo "[INFO] Pulling hello-world"
docker pull hello-world:latest >/dev/null
docker run --rm hello-world:latest | head -n 3

if [[ -f Dockerfile ]]; then
  echo "[INFO] Building local Semptify image (quick validation)"
  docker build -t Semptify:local --progress=plain . >/dev/null
  echo "[OK] Image built: Semptify:local"
else
  echo "[SKIP] No Dockerfile in current directory"
fi

echo "[DONE] Docker verification completed."
