import hashlib
import json
import os
import time
from typing import Dict, Optional


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_certificate(kind: str, sha256: str, meta: Optional[Dict] = None, out_dir: str = "logs") -> str:
    ts = int(time.time())
    _ensure_dir(out_dir)
    payload = {
        "ts": ts,
        "sha256": sha256,
        "kind": kind,
        "meta": meta or {},
    }
    fname = f"notary_{ts}_{kind}.json"
    fpath = os.path.join(out_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return fpath
