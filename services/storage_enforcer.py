"""
Storage Requirement Enforcer - Block app startup without persistent storage
Patched: R2 recognition, override support, corrected status logic, non-strict warning.
"""
import os
import sys

R2_CORE_VARS = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME']
R2_ENDPOINT_VARS = ['R2_ENDPOINT_URL', 'R2_ENDPOINT']
GCS_VARS = ['GOOGLE_APPLICATION_CREDENTIALS', 'GCS_BUCKET_NAME']


def _r2_configured() -> tuple[bool, list]:
    missing = [v for v in R2_CORE_VARS if not os.getenv(v)]
    if missing:
        return False, missing
    endpoint = next((os.getenv(v) for v in R2_ENDPOINT_VARS if os.getenv(v)), None)
    if not endpoint and os.getenv('R2_ACCOUNT_ID'):
        inferred = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
        os.environ['R2_ENDPOINT_URL'] = inferred
    return True, []


def _gcs_configured() -> tuple[bool, list]:
    missing = [v for v in GCS_VARS if not os.getenv(v)]
    return (len(missing) == 0), missing


def _render_disk_configured() -> tuple[bool, list]:
    disk = os.getenv('PERSISTENT_DISK_PATH')
    if disk and os.path.exists(disk):
        return True, []
    return False, ['PERSISTENT_DISK_PATH'] if disk else []


def check_storage_configured() -> tuple[bool, str, list]:
    override = os.getenv('PERSISTENCE_OVERRIDE')
    if override and override.lower() in ('1', 'true', 'yes'):
        return True, 'Override (DEV)', []

    r2_ok, r2_missing = _r2_configured()
    if r2_ok:
        return True, 'Cloudflare R2', []

    gcs_ok, gcs_missing = _gcs_configured()
    if gcs_ok:
        return True, 'Google Cloud Storage', []

    render_ok, render_missing = _render_disk_configured()
    if render_ok:
        return True, 'Render Persistent Disk', []

    return False, 'None', r2_missing or gcs_missing or render_missing


def enforce_storage_requirement(strict: bool = None):
    """Enforce persistent storage requirement. Returns True if configured, False if running ephemeral (non-strict)."""
    if strict is None:
        is_render = bool(os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER_SERVICE_ID'))
        is_production = os.getenv('PRODUCTION') == 'true'
        strict = is_render or is_production

    configured, provider, missing = check_storage_configured()

    if configured:
        print(f"\n{'='*70}\nOK PERSISTENT STORAGE CONFIGURED: {provider}\n{'='*70}\n")
        return True

    if not strict:
        print("\n" + "="*70)
        print("WARNING  EPHEMERAL STORAGE MODE")
        if missing:
            print("Missing vars: " + ", ".join(missing))
        print("Data will be lost on restart!")
        print("Set production vars or PERSISTENCE_OVERRIDE=1 to silence this.")
        print("="*70 + "\n")
        return False

    print("\n" + "="*70)
    print(" CRITICAL ERROR: PERSISTENT STORAGE NOT CONFIGURED")
    print("="*70)
    print("\nMissing variables: " + (', '.join(missing) if missing else 'Unknown'))
    print("Refer to PERSISTENCE_SETUP_GUIDE.md for configuration details.\n")
    sys.exit(1)


def get_storage_status() -> dict:
    configured, provider, missing = check_storage_configured()
    return {
        'configured': configured,
        'provider': provider,
        'missing_vars': missing,
        'status': 'ready' if configured else 'ephemeral',
        'override': bool(os.getenv('PERSISTENCE_OVERRIDE')),
    }


