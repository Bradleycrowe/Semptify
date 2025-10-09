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

echo "[lint] Done"