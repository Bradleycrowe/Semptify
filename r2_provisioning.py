"""
Cloudflare R2 Auto-Provisioning
Creates per-user buckets and scoped access tokens automatically.
"""
import os
import requests
import secrets
from typing import Dict, Optional

CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID')
CF_API_TOKEN = os.getenv('CF_API_TOKEN')
CF_API_BASE = 'https://api.cloudflare.com/client/v4'

def provision_user_storage(user_id: str) -> Optional[Dict]:
    """
    Create R2 bucket + scoped token for user.
    Returns: {bucket_name, access_key_id, secret_access_key, endpoint_url} or None on error.
    """
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        return None  # Fallback to shared bucket or local

    bucket_name = f"semptify-user-{user_id}"
    headers = {'Authorization': f'Bearer {CF_API_TOKEN}', 'Content-Type': 'application/json'}

    # 1. Create bucket
    try:
        r = requests.post(
            f'{CF_API_BASE}/accounts/{CF_ACCOUNT_ID}/r2/buckets',
            headers=headers,
            json={'name': bucket_name},
            timeout=10
        )
        if r.status_code not in [200, 409]:  # 409 = already exists (ok)
            return None
    except Exception:
        return None

    # 2. Create API token scoped to this bucket
    try:
        token_payload = {
            'name': f'semptify-user-{user_id}-token',
            'policies': [{
                'effect': 'allow',
                'resources': {f'{CF_ACCOUNT_ID}/*/{bucket_name}': '*'},
                'permission_groups': [{'id': 'f267e341f3dd4697bd3b9f71dd96247f'}]  # R2 Read/Write
            }]
        }
        r = requests.post(
            f'{CF_API_BASE}/user/tokens',
            headers=headers,
            json=token_payload,
            timeout=10
        )
        if r.status_code != 200:
            return None
        token_data = r.json().get('result', {})
        access_key = token_data.get('id')
        secret_key = token_data.get('value')
        if not access_key or not secret_key:
            return None
    except Exception:
        return None

    return {
        'bucket_name': bucket_name,
        'access_key_id': access_key,
        'secret_access_key': secret_key,
        'endpoint_url': f'https://{CF_ACCOUNT_ID}.r2.cloudflarestorage.com',
        'account_id': CF_ACCOUNT_ID
    }

def provision_fallback(user_id: str) -> Dict:
    """
    Fallback: Use shared app bucket with namespaced prefix.
    """
    return {
        'bucket_name': os.getenv('R2_BUCKET_NAME', 'semptify-storage'),
        'access_key_id': os.getenv('R2_ACCESS_KEY_ID'),
        'secret_access_key': os.getenv('R2_SECRET_ACCESS_KEY'),
        'endpoint_url': f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        'account_id': os.getenv('R2_ACCOUNT_ID'),
        'prefix': f'users/{user_id}/',  # Namespace in shared bucket
        'shared': True
    }

# Google Cloud Storage Provisioning
from google.cloud import storage as gcs_client
from google.oauth2 import service_account
import json

GCS_PROJECT_ID = os.getenv('GCS_PROJECT_ID')
GCS_SERVICE_ACCOUNT_JSON = os.getenv('GCS_SERVICE_ACCOUNT_JSON')

def provision_user_storage_gcs(user_id: str) -> Optional[Dict]:
    """
    Create GCS bucket for user.
    Returns: {bucket_name, project_id, service_account} or None on error.
    """
    if not GCS_PROJECT_ID or not GCS_SERVICE_ACCOUNT_JSON:
        return None
    
    try:
        creds_dict = json.loads(GCS_SERVICE_ACCOUNT_JSON)
        credentials = service_account.Credentials.from_service_account_info(creds_dict)
        client = gcs_client.Client(project=GCS_PROJECT_ID, credentials=credentials)
        
        bucket_name = f"semptify-user-{user_id}"
        bucket = client.bucket(bucket_name)
        
        if not bucket.exists():
            bucket.location = "US"
            bucket.storage_class = "STANDARD"
            bucket = client.create_bucket(bucket)
        
        return {
            'bucket_name': bucket_name,
            'project_id': GCS_PROJECT_ID,
            'provider': 'google',
            'credentials': creds_dict
        }
    except Exception:
        return None

def auto_provision_storage(user_id: str) -> Optional[Dict]:
    """
    Auto-provision storage: try R2 first, then GCS.
    Returns storage config or None if both fail.
    NO FALLBACK - user must have real storage.
    """
    # Try R2 first
    config = provision_user_storage(user_id)
    if config:
        config['provider'] = 'r2'
        return config
    
    # Try GCS second
    config = provision_user_storage_gcs(user_id)
    if config:
        return config
    
    # Both failed - return None (no qualification)
    return None
