"""Storage Qualification System
Users prove storage access = they get qualified.
No user accounts in Semptify - storage provider handles identity.
"""
from flask import Blueprint, request, jsonify, session
import boto3
from google.cloud import storage as gcs
import os
import secrets
from datetime import datetime

storage_qual_bp = Blueprint('storage_qual', __name__, url_prefix='/storage')

@storage_qual_bp.route('/qualify', methods=['POST'])
def qualify_storage():
    """Test user's storage credentials and qualify them if valid."""
    data = request.get_json()
    provider = data.get('provider')  # 'r2' or 'google'
    
    if provider == 'r2':
        return _qualify_r2(data)
    elif provider == 'google':
        return _qualify_google(data)
    else:
        return jsonify({'error': 'Invalid provider'}), 400

def _qualify_r2(data):
    """Test R2 credentials by writing/reading a test file."""
    try:
        account_id = data.get('account_id')
        access_key = data.get('access_key')
        secret_key = data.get('secret_key')
        bucket_name = data.get('bucket_name', 'semptify-user-data')
        
        # Create R2 client
        s3 = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )
        
        # Test: write a qualification file
        test_key = f'_semptify_qual_test_{secrets.token_hex(8)}.txt'
        test_content = f'Semptify qualification test at {datetime.utcnow().isoformat()}'
        s3.put_object(Bucket=bucket_name, Key=test_key, Body=test_content.encode())
        
        # Test: read it back
        obj = s3.get_object(Bucket=bucket_name, Key=test_key)
        retrieved = obj['Body'].read().decode()
        
        # Clean up test file
        s3.delete_object(Bucket=bucket_name, Key=test_key)
        
        # Success! Generate session token
        session_token = secrets.token_urlsafe(32)
        session['qualified'] = True
        session['storage_provider'] = 'r2'
        session['bucket_name'] = bucket_name
        session['session_token'] = session_token
        
        # Store credentials in session (encrypted by Flask)
        session['storage_creds'] = {
            'account_id': account_id,
            'access_key': access_key,
            'secret_key': secret_key
        }
        
        return jsonify({
            'qualified': True,
            'provider': 'r2',
            'bucket': bucket_name,
            'session_token': session_token,
            'message': 'Storage verified - you are qualified!'
        })
        
    except Exception as e:
        return jsonify({
            'qualified': False,
            'error': str(e),
            'message': 'Could not verify R2 storage access'
        }), 400

def _qualify_google(data):
    """Test Google Cloud Storage credentials."""
    try:
        credentials_json = data.get('credentials_json')
        bucket_name = data.get('bucket_name', 'semptify-user-data')
        
        # Create GCS client
        client = gcs.Client.from_service_account_info(credentials_json)
        bucket = client.bucket(bucket_name)
        
        # Test: write a qualification file
        test_blob_name = f'_semptify_qual_test_{secrets.token_hex(8)}.txt'
        test_content = f'Semptify qualification test at {datetime.utcnow().isoformat()}'
        blob = bucket.blob(test_blob_name)
        blob.upload_from_string(test_content)
        
        # Test: read it back
        retrieved = blob.download_as_text()
        
        # Clean up
        blob.delete()
        
        # Success!
        session_token = secrets.token_urlsafe(32)
        session['qualified'] = True
        session['storage_provider'] = 'google'
        session['bucket_name'] = bucket_name
        session['session_token'] = session_token
        session['storage_creds'] = credentials_json
        
        return jsonify({
            'qualified': True,
            'provider': 'google',
            'bucket': bucket_name,
            'session_token': session_token,
            'message': 'Storage verified - you are qualified!'
        })
        
    except Exception as e:
        return jsonify({
            'qualified': False,
            'error': str(e),
            'message': 'Could not verify Google Cloud Storage access'
        }), 400

@storage_qual_bp.route('/status', methods=['GET'])
def check_qualification():
    """Check if current session is qualified."""
    qualified = session.get('qualified', False)
    if qualified:
        return jsonify({
            'qualified': True,
            'provider': session.get('storage_provider'),
            'bucket': session.get('bucket_name')
        })
    else:
        return jsonify({'qualified': False}), 401

@storage_qual_bp.route('/logout', methods=['POST'])
def logout():
    """Clear qualification session."""
    session.clear()
    return jsonify({'message': 'Session cleared'})

# Helper: require qualification for protected routes
def require_storage_qualification(f):
    """Decorator to protect routes - user must be storage-qualified."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('qualified'):
            return jsonify({'error': 'Storage qualification required'}), 401
        return f(*args, **kwargs)
    return decorated
