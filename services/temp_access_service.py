"""Temporary access engine for Semptify admin workflows."""
from __future__ import annotations

import json
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "temp_access_tokens.json"
ALLOWED_SCOPES = [
    "timeline",
    "analytics",
    "ai",
    "admin_panels",
]


def _load_state() -> Dict[str, Any]:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"tokens": []}


def _save_state(state: Dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def list_temp_tokens() -> List[Dict[str, Any]]:
    state = _load_state()
    tokens = state.get("tokens", [])
    now = datetime.utcnow()
    cleaned = []
    for token in tokens:
        expires_at = datetime.fromisoformat(token["expires_at"])
        if expires_at < now:
            continue
        cleaned.append(token)
    state["tokens"] = cleaned
    _save_state(state)
    return cleaned


def issue_temp_token(*, scope: str, issued_to: str, minutes: int, issued_by: str) -> Dict[str, Any]:
    if scope not in ALLOWED_SCOPES:
        raise ValueError("Scope not allowed for temporary access")

    token_value = secrets.token_urlsafe(24)
    payload = {
        "token": token_value,
        "scope": scope,
        "issued_to": issued_to or "anonymous",
        "issued_by": issued_by,
        "issued_at": datetime.utcnow().isoformat() + "Z",
        "expires_at": (datetime.utcnow() + timedelta(minutes=minutes)).isoformat(),
    }
    state = _load_state()
    state.setdefault("tokens", []).append(payload)
    _save_state(state)
    return payload


def revoke_temp_token(token: str) -> bool:
    state = _load_state()
    tokens = state.get("tokens", [])
    filtered = [t for t in tokens if t.get("token") != token]
    state["tokens"] = filtered
    _save_state(state)
    return len(filtered) != len(tokens)


def validate_temp_token(token: str, scope: str) -> bool:
    for entry in list_temp_tokens():
        if entry["token"] == token and entry["scope"] == scope:
            return True
    return False
