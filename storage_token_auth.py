"""
Storage-based token authentication system.
Token stored IN user's bucket proves they control storage.
"""
import hashlib
import secrets
import json
import boto3
from datetime import datetime
from typing import Optional, Dict, Any

def generate_token(prefix: str = "SMPT") -> str:
    """Generate human-friendly token: SMPT-XXXX-XXXX-XXXX"""
    parts = [prefix]
    for _ in range(3):
        # 4 chars per segment, uppercase alphanumeric (no confusing chars)
        chars = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(4))
        parts.append(chars)
    return '-'.join(parts)

def _get_s3_client(storage_config: Dict[str, Any]):
    """Create boto3 client for R2 or GCS-compatible S3 API"""
    if storage_config.get('provider') == 'google':
        # GCS with S3 compatibility (requires HMAC keys)
        return boto3.client(
            's3',
            aws_access_key_id=storage_config.get('access_key_id'),
            aws_secret_access_key=storage_config.get('secret_access_key'),
            endpoint_url='https://storage.googleapis.com'
        )
    else:
        # Cloudflare R2
        return boto3.client(
            's3',
            aws_access_key_id=storage_config['access_key_id'],
            aws_secret_access_key=storage_config['secret_access_key'],
            endpoint_url=storage_config['endpoint_url']
        )

def write_token_to_bucket(storage_config: Dict[str, Any], token: str, user_id: str) -> bool:
    """
    Write authentication token to /.semptify/auth_token.json in user's bucket.
    Returns True on success, False on failure.
    """
    try:
        s3_client = _get_s3_client(storage_config)
        bucket_name = storage_config['bucket_name']
        
        # Create auth data with integrity hash
        auth_data = {
            'token': token,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'sha256': hashlib.sha256(token.encode('utf-8')).hexdigest()
        }
        
        # Write to bucket
        s3_client.put_object(
            Bucket=bucket_name,
            Key='.semptify/auth_token.json',
            Body=json.dumps(auth_data, indent=2).encode('utf-8'),
            ContentType='application/json'
        )
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write token to bucket: {e}")
        return False

def verify_token_from_bucket(storage_config: Dict[str, Any], provided_token: str) -> Optional[Dict[str, Any]]:
    """
    Read auth token from user's bucket and verify it matches provided token.
    Returns auth_data dict on success, None on failure.
    """
    try:
        s3_client = _get_s3_client(storage_config)
        bucket_name = storage_config['bucket_name']
        
        # Read token file from bucket
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key='.semptify/auth_token.json'
        )
        auth_data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Verify token matches
        if auth_data.get('token') != provided_token:
            print(f"[WARN] Token mismatch for user_id={auth_data.get('user_id')}")
            return None
        
        # Verify integrity hash
        expected_hash = hashlib.sha256(provided_token.encode('utf-8')).hexdigest()
        if auth_data.get('sha256') != expected_hash:
            print(f"[WARN] Token integrity check failed for user_id={auth_data.get('user_id')}")
            return None
        
        return auth_data
        
    except Exception as e:
        print(f"[ERROR] Failed to verify token from bucket: {e}")
        return None

def hash_token_for_index(token: str) -> str:
    """Hash token for secure local indexing (user_id lookup)"""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()
