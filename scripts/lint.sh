#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

echo "[lint] Python (ruff)"
if command -v ruff >/dev/null 2>&1; then
  ruff check .
else
  echo "[lint] Ruff not installed (skipping)"
fi

echo "[lint] Shell (shellcheck)"
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck scripts/*.sh
else
  echo "[lint] shellcheck not installed (skipping)"
fi

echo "[lint] Dockerfile (hadolint)"
if command -v hadolint >/dev/null 2>&1; then
  hadolint Dockerfile || exit 1
else
  echo "[lint] hadolint not installed (skipping)"
fi

echo "[lint] GitHub Workflows (actionlint)"
if command -v actionlint >/dev/null 2>&1; then
  actionlint || exit 1
else
  echo "[lint] actionlint not installed (skipping)"
fi

echo "[lint] Done"