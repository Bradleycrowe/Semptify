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
