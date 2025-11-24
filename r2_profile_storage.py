"""
R2 Profile Storage - Store profile data in Cloudflare R2
Integrates profile_manager with persistent R2 storage
"""
import json
import os
import boto3
from pathlib import Path
from profile_manager import (
    get_all_profiles, get_active_profile, 
    PROFILES_DIR, PROFILES_FILE, ACTIVE_PROFILE_FILE
)

# R2 Configuration
R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "Semptify")

def get_r2_client():
    """Get boto3 client for R2"""
    if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
        return None
    
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name="auto"
    )

def sync_profiles_to_r2():
    """Upload profiles to R2"""
    client = get_r2_client()
    if not client:
        print("[WARN] R2 not configured, using local storage only")
        return False
    
    try:
        # Upload profiles.json
        if PROFILES_FILE.exists():
            client.upload_file(
                str(PROFILES_FILE),
                R2_BUCKET,
                "data/profiles/profiles.json"
            )
        
        # Upload active_profile.json
        if ACTIVE_PROFILE_FILE.exists():
            client.upload_file(
                str(ACTIVE_PROFILE_FILE),
                R2_BUCKET,
                "data/profiles/active_profile.json"
            )
        
        print("[OK] Synced profiles to R2")
        return True
    except Exception as e:
        print(f"[ERROR] R2 sync failed: {e}")
        return False

def restore_profiles_from_r2():
    """Download profiles from R2"""
    client = get_r2_client()
    if not client:
        return False
    
    try:
        # Ensure local dir exists
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Download profiles.json
        try:
            client.download_file(
                R2_BUCKET,
                "data/profiles/profiles.json",
                str(PROFILES_FILE)
            )
        except client.exceptions.NoSuchKey:
            print("[INFO] No profiles in R2, using local defaults")
        
        # Download active_profile.json
        try:
            client.download_file(
                R2_BUCKET,
                "data/profiles/active_profile.json",
                str(ACTIVE_PROFILE_FILE)
            )
        except client.exceptions.NoSuchKey:
            pass
        
        print("[OK] Restored profiles from R2")
        return True
    except Exception as e:
        print(f"[ERROR] R2 restore failed: {e}")
        return False

def upload_profile_data(profile_id, file_path, r2_key):
    """Upload profile-specific file to R2"""
    client = get_r2_client()
    if not client:
        return False
    
    try:
        r2_path = f"data/profiles/{profile_id}/{r2_key}"
        client.upload_file(str(file_path), R2_BUCKET, r2_path)
        return True
    except Exception as e:
        print(f"[ERROR] Upload failed for {r2_key}: {e}")
        return False

def download_profile_data(profile_id, r2_key, local_path):
    """Download profile-specific file from R2"""
    client = get_r2_client()
    if not client:
        return False
    
    try:
        r2_path = f"data/profiles/{profile_id}/{r2_key}"
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        client.download_file(R2_BUCKET, r2_path, str(local_path))
        return True
    except Exception as e:
        print(f"[ERROR] Download failed for {r2_key}: {e}")
        return False

def list_profile_files(profile_id):
    """List all files for a profile in R2"""
    client = get_r2_client()
    if not client:
        return []
    
    try:
        prefix = f"data/profiles/{profile_id}/"
        response = client.list_objects_v2(Bucket=R2_BUCKET, Prefix=prefix)
        
        if "Contents" not in response:
            return []
        
        return [obj["Key"].replace(prefix, "") for obj in response["Contents"]]
    except Exception as e:
        print(f"[ERROR] List failed: {e}")
        return []

# Auto-sync on import if R2 configured
if get_r2_client():
    restore_profiles_from_r2()
