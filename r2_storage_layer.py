"""
r2_storage_layer.py - Unified R2-only storage abstraction.
Ensures Semptify runs in single-user, multi-client (profiles) mode with ONLY Cloudflare R2.
"""
import os
import json
from pathlib import Path
import threading

try:
    import boto3  # noqa
except ImportError:
    boto3 = None

# Env vars expected (Render / .env):
# R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
# Optional: R2_ONLY=1 (enforce exclusive R2 mode)

R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "Semptify")
R2_ONLY = os.getenv("R2_ONLY", "0") == "1"

_local_root = Path("data/profiles")
_local_root.mkdir(parents=True, exist_ok=True)

_client_lock = threading.Lock()
_cached_client = None

def _other_provider_present():
    # Detect env hints for other storage providers
    other_env_keys = [
        "GOOGLE_DRIVE_TOKEN", "DROPBOX_ACCESS_TOKEN", "AWS_ACCESS_KEY_ID", "AZURE_STORAGE_KEY"
    ]
    for k in other_env_keys:
        if os.getenv(k):
            return k
    return None

def get_r2_client():
    global _cached_client
    if _cached_client:
        return _cached_client
    if not boto3:
        if R2_ONLY:
            raise RuntimeError("R2_ONLY enforced but boto3 not installed.")
        return None
    if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
        if R2_ONLY:
            raise RuntimeError("R2_ONLY enforced but R2 credentials incomplete.")
        return None

    other = _other_provider_present()
    if other and R2_ONLY:
        raise RuntimeError(f"R2_ONLY mode active; conflicting provider env detected: {other}")

    with _client_lock:
        if _cached_client is None:
            _cached_client = boto3.client(
                "s3",
                endpoint_url=R2_ENDPOINT,
                aws_access_key_id=R2_ACCESS_KEY,
                aws_secret_access_key=R2_SECRET_KEY,
                region_name="auto"
            )
    return _cached_client

def r2_available():
    c = get_r2_client()
    return c is not None

def ensure_r2_only():
    if R2_ONLY and not r2_available():
        raise RuntimeError("R2_ONLY=1 but R2 client unavailable.")

# Basic helpers

def r2_key_for_profile_file(profile_id: str, filename: str) -> str:
    return f"data/profiles/{profile_id}/{filename}" if filename else f"data/profiles/{profile_id}"

def upload_bytes(profile_id: str, filename: str, data: bytes) -> bool:
    client = get_r2_client()
    if not client:
        # Save locally as fallback (only if not enforced)
        if R2_ONLY:
            return False
        dest = _local_root / profile_id
        dest.mkdir(parents=True, exist_ok=True)
        (dest / filename).write_bytes(data)
        return True
    try:
        client.put_object(Bucket=R2_BUCKET, Key=r2_key_for_profile_file(profile_id, filename), Body=data)
        return True
    except Exception as e:
        print(f"[ERROR] R2 upload failed: {e}")
        return False

def download_bytes(profile_id: str, filename: str):
    client = get_r2_client()
    if not client:
        if R2_ONLY:
            return None
        path = _local_root / profile_id / filename
        return path.read_bytes() if path.exists() else None
    try:
        obj = client.get_object(Bucket=R2_BUCKET, Key=r2_key_for_profile_file(profile_id, filename))
        return obj['Body'].read()
    except client.exceptions.NoSuchKey:
        return None
    except Exception as e:
        print(f"[ERROR] R2 download failed: {e}")
        return None

def list_profile_files(profile_id: str):
    client = get_r2_client()
    prefix = f"data/profiles/{profile_id}/"
    if not client:
        if R2_ONLY:
            return []
        local_dir = _local_root / profile_id
        if not local_dir.exists():
            return []
        return [p.name for p in local_dir.iterdir() if p.is_file()]
    try:
        resp = client.list_objects_v2(Bucket=R2_BUCKET, Prefix=prefix)
        if "Contents" not in resp:
            return []
        return [o['Key'].replace(prefix, '') for o in resp['Contents'] if not o['Key'].endswith('/')]
    except Exception as e:
        print(f"[ERROR] R2 list failed: {e}")
        return []

def save_json(profile_id: str, filename: str, obj) -> bool:
    return upload_bytes(profile_id, filename, json.dumps(obj, indent=2).encode('utf-8'))

def load_json(profile_id: str, filename: str):
    raw = download_bytes(profile_id, filename)
    if raw is None:
        return None
    try:
        return json.loads(raw.decode('utf-8'))
    except Exception:
        return None

# Integrity check on import
try:
    ensure_r2_only()
except Exception as e:
    print(f"[FATAL] R2 storage configuration error: {e}")
