"""
Storage Requirement Enforcer - Block app startup without persistent storage
"""
import os
import sys


def check_storage_configured() -> tuple[bool, str, list]:
    """
    Check if ANY persistent storage is configured.
    Returns: (is_configured, provider_name, missing_vars)
    """
    # Check R2 (Cloudflare)
    r2_vars = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME']
    r2_configured = all(os.getenv(var) for var in r2_vars)
    
    if r2_configured:
        return True, "Cloudflare R2", []
    
    # Check GCS (Google Cloud)
    gcs_vars = ['GOOGLE_APPLICATION_CREDENTIALS', 'GCS_BUCKET_NAME']
    gcs_configured = all(os.getenv(var) for var in gcs_vars)
    
    if gcs_configured:
        return True, "Google Cloud Storage", []
    
    # Check Render Persistent Disk
    render_disk = os.getenv('PERSISTENT_DISK_PATH')
    if render_disk and os.path.exists(render_disk):
        return True, "Render Persistent Disk", []
    
    # Nothing configured - determine what's missing
    missing = []
    if not r2_configured:
        missing.extend([v for v in r2_vars if not os.getenv(v)])
    
    return False, "None", missing


def enforce_storage_requirement(strict: bool = None):
    """
    Enforce persistent storage requirement.
    Exits application with clear error if not configured.
    """
    # Check if dev mode (allow local storage)
    import os
    if strict is None:
        # Auto-detect: strict in production, lenient in dev
        # Auto-detect production: check for Render or explicit PRODUCTION flag
        is_render = bool(os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER_SERVICE_ID'))
        is_production = os.getenv('PRODUCTION') == 'true'
        strict = is_render or is_production
    
    # Allow bypass in development
    if not strict and os.getenv('DEV_MODE') == 'true':
        print("\n" + "="*70)
        print("⚠️  DEV MODE: Running with ephemeral local storage")
        print("   Data will be lost on restart!")
        print("="*70 + "\n")
        return True
    
    configured, provider, missing = check_storage_configured()
    
    if configured:
        print(f"\n{'='*70}")
        print(f"✓ PERSISTENT STORAGE CONFIGURED: {provider}")
        print(f"{'='*70}\n")
        return True
    
    # NOT CONFIGURED - Block startup with clear message
    print("\n" + "="*70)
    print("❌ CRITICAL ERROR: PERSISTENT STORAGE NOT CONFIGURED")
    print("="*70)
    print("\n⚠️  Semptify REQUIRES persistent storage to function.\n")
    print("WITHOUT STORAGE, YOU WILL LOSE:")
    print("  • All uploaded documents (vault)")
    print("  • User accounts and login credentials")
    print("  • Timeline history and events")
    print("  • Notary certificates and document hashes")
    print("  • Admin tokens and access")
    print("  • AI learning patterns\n")
    
    print("SOLUTION: Configure ONE of these storage providers:\n")
    
    print("1. CLOUDFLARE R2 (Recommended - $2-3/month)")
    print("   Set these environment variables:")
    print("     R2_ACCOUNT_ID")
    print("     R2_ACCESS_KEY_ID")
    print("     R2_SECRET_ACCESS_KEY")
    print("     R2_BUCKET_NAME")
    print("     R2_ENDPOINT_URL\n")
    
    print("2. GOOGLE CLOUD STORAGE (Free tier available)")
    print("   Set these environment variables:")
    print("     GOOGLE_APPLICATION_CREDENTIALS=/app/gcs-key.json")
    print("     GCS_BUCKET_NAME")
    print("   Upload service account key as secret file\n")
    
    print("3. RENDER PERSISTENT DISK ($10/month for 10GB)")
    print("   Set environment variable:")
    print("     PERSISTENT_DISK_PATH=/mnt/data\n")
    
    print("="*70)
    print("DOCUMENTATION: See PERSISTENCE_SETUP_GUIDE.md for detailed setup")
    print("="*70)
    print("\n🛑 Application startup blocked until storage is configured.\n")
    
    # In non-strict mode, warn but allow
    if not strict:
        print("⚠️  WARNING: Continuing with ephemeral storage (development only)")
        print("   Set PRODUCTION=true to enforce storage requirement\n")
        return False
    
    # Exit with error code in strict/production mode
    sys.exit(1)


def get_storage_status() -> dict:
    """Get detailed storage configuration status for health checks."""
    # Check if dev mode (allow local storage)
    import os
    if strict is None:
        # Auto-detect: strict in production, lenient in dev
        # Auto-detect production: check for Render or explicit PRODUCTION flag
        is_render = bool(os.getenv('RENDER_SERVICE_NAME') or os.getenv('RENDER_SERVICE_ID'))
        is_production = os.getenv('PRODUCTION') == 'true'
        strict = is_render or is_production
    
    # Allow bypass in development
    if not strict and os.getenv('DEV_MODE') == 'true':
        print("\n" + "="*70)
        print("⚠️  DEV MODE: Running with ephemeral local storage")
        print("   Data will be lost on restart!")
        print("="*70 + "\n")
        return True
    
    configured, provider, missing = check_storage_configured()
    
    return {
        "configured": configured,
        "provider": provider,
        "missing_vars": missing,
        "status": "ready" if configured else "blocked",
        "message": f"Using {provider}" if configured else "No persistent storage configured"
    }
