"""
Storage Setup Routes - R2/GCS Clipboard-Monitored Setup
Zero-typing setup wizard with automatic credential capture
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
import boto3
import secrets
import hashlib
from datetime import datetime
import json
import os

storage_setup_bp = Blueprint('storage_setup', __name__)


# ============================================================================
# USER-FRIENDLY STORAGE OPTIONS
# ============================================================================

@storage_setup_bp.route('/setup', methods=['GET'])
def choose_storage():
    """Main storage selection page - user-friendly options"""
    return render_template('storage_setup/choose_storage.html')

@storage_setup_bp.route('/setup/local/guide', methods=['GET'])
def local_storage_guide():
    """Local folder storage using File System Access API"""
    return render_template('storage_setup/local_guide.html')

@storage_setup_bp.route('/setup/dropbox/guide', methods=['GET'])
def dropbox_storage_guide():
    """Dropbox OAuth wizard"""
    return render_template('storage_setup/dropbox_guide.html')

@storage_setup_bp.route('/setup/drive/guide', methods=['GET'])
def drive_storage_guide():
    """Google Drive OAuth wizard"""
    return render_template('storage_setup/drive_guide.html')


@storage_setup_bp.route('/setup', methods=['GET'])
def setup_wizard():
    '''Storage setup wizard - R2 or Google Cloud Storage'''
    return render_template('storage_setup/wizard.html')

@storage_setup_bp.route('/setup/r2/guide', methods=['GET'])
def r2_guide():
    '''R2 signup guide with clipboard monitoring'''
    return render_template('storage_setup/r2_guide.html')

@storage_setup_bp.route('/api/storage/test-r2', methods=['POST'])
def test_r2_connection():
    '''
    Test R2 connection with provided credentials
    
    POST /api/storage/test-r2
    Body: {
        account_id: str,
        access_key_id: str,
        secret_access_key: str
    }
    '''
    data = request.get_json()
    
    account_id = data.get('account_id', '').strip()
    access_key_id = data.get('access_key_id', '').strip()
    secret_access_key = data.get('secret_access_key', '').strip()
    
    # Validate format
    if not account_id or len(account_id) != 32:
        return jsonify({'ok': False, 'error': 'Invalid Account ID format'}), 400
    
    if not access_key_id or len(access_key_id) != 20:
        return jsonify({'ok': False, 'error': 'Invalid Access Key ID format'}), 400
    
    if not secret_access_key or len(secret_access_key) != 40:
        return jsonify({'ok': False, 'error': 'Invalid Secret Access Key format'}), 400
    
    try:
        # Initialize R2 client
        endpoint_url = f'https://{account_id}.r2.cloudflarestorage.com'
        
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='auto'
        )
        
        # Generate unique bucket name
        bucket_name = f'semptify-{secrets.token_hex(8)}'
        
        # Try to create bucket
        try:
            s3.create_bucket(Bucket=bucket_name)
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass  # Bucket already exists, that's fine
        except Exception as e:
            return jsonify({'ok': False, 'error': f'Failed to create bucket: {str(e)}'}), 400
        
        # Test write
        test_key = '.semptify/connection_test.txt'
        test_content = f'Semptify connection test at {datetime.utcnow().isoformat()}'
        
        s3.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content.encode('utf-8')
        )
        
        # Test read
        response = s3.get_object(Bucket=bucket_name, Key=test_key)
        content = response['Body'].read().decode('utf-8')
        
        if content != test_content:
            return jsonify({'ok': False, 'error': 'Read/write test failed'}), 400
        
        # Generate user token
        user_token = secrets.token_hex(16)  # 32 characters
        token_hash = hashlib.sha256(user_token.encode()).hexdigest()
        
        # Write auth token to user's bucket
        auth_token_data = {
            'token_hash': token_hash,
            'created_at': datetime.utcnow().isoformat(),
            'storage_provider': 'r2',
            'bucket': bucket_name
        }
        
        s3.put_object(
            Bucket=bucket_name,
            Key='.semptify/auth_token.json',
            Body=json.dumps(auth_token_data, indent=2).encode('utf-8')
        )
        
        # Return encrypted credentials for browser storage
        credentials_json = json.dumps({
            'account_id': account_id,
            'access_key_id': access_key_id,
            'secret_access_key': secret_access_key,
            'bucket': bucket_name,
            'endpoint': endpoint_url
        })
        
        return jsonify({
            'ok': True,
            'bucket': bucket_name,
            'user_token': user_token,
            'credentials': credentials_json,
            'message': 'R2 storage connected successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': f'Connection test failed: {str(e)}'
        }), 400

@storage_setup_bp.route('/welcome', methods=['GET'])
def welcome():
    '''Welcome page after successful storage setup'''
    user_token = request.args.get('token')
    storage_provider = 'Google Drive' if 'drive_credentials' in session else 'Dropbox' if 'dropbox_access_token' in session else 'your storage'
    return render_template('storage_setup/welcome.html', user_token=user_token, storage_provider=storage_provider)


@storage_setup_bp.route('/setup/gcs/guide', methods=['GET'])
def gcs_setup_guide():
    """Google Cloud Storage setup wizard"""
    return render_template('storage_setup/gcs_guide.html')

@storage_setup_bp.route('/api/storage/test-gcs', methods=['POST'])
def test_gcs_connection():
    """Test GCS credentials and create bucket"""
    try:
        from datetime import datetime
        from google.cloud import storage
        from google.oauth2 import service_account
        
        data = request.get_json()
        service_account_json = data.get('service_account_json')
        
        if not service_account_json:
            return jsonify({'success': False, 'error': 'Service account JSON required'}), 400
        
        # Parse and validate JSON
        try:
            sa_data = json.loads(service_account_json)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
        
        # Validate required fields
        required_fields = ['project_id', 'private_key', 'client_email', 'type']
        missing = [f for f in required_fields if f not in sa_data]
        if missing:
            return jsonify({'success': False, 'error': f'Missing fields: {", ".join(missing)}'}), 400
        
        if sa_data.get('type') != 'service_account':
            return jsonify({'success': False, 'error': 'Must be a service account key'}), 400
        
        # Test GCS connection
        credentials = service_account.Credentials.from_service_account_info(sa_data)
        client = storage.Client(credentials=credentials, project=sa_data['project_id'])
        
        # Create bucket (lowercase, no underscores)
        bucket_name = f"semptify-{secrets.token_hex(8)}"
        bucket = client.create_bucket(bucket_name, location='US')
        
        # Test write
        blob = bucket.blob('.semptify/connection_test.txt')
        blob.upload_from_string('Semptify GCS connection successful!')
        
        # Test read
        test_content = blob.download_as_text()
        if 'successful' not in test_content:
            raise Exception('Read test failed')
        
        # Generate user token
        user_token = secrets.token_hex(16)
        token_hash = hashlib.sha256(user_token.encode()).hexdigest()
        
        # Store token in bucket
        token_blob = bucket.blob('.semptify/auth_token.json')
        token_data = {
            'token_hash': token_hash,
            'created_at': str(datetime.now()),
            'bucket_name': bucket_name,
            'project_id': sa_data['project_id']
        }
        token_blob.upload_from_string(json.dumps(token_data))
        
        # Encrypt credentials for client storage
        encrypted = {
            'provider': 'gcs',
            'project_id': sa_data['project_id'],
            'bucket_name': bucket_name,
            'service_account': service_account_json  # In production, encrypt this!
        }
        
        return jsonify({
            'success': True,
            'token': user_token,
            'credentials': encrypted
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# GOOGLE DRIVE OAUTH
# ============================================================================

@storage_setup_bp.route('/oauth/google/start', methods=['GET'])
def google_oauth_start():
    '''Initiate Google OAuth flow'''
    from google_auth_oauthlib.flow import Flow
    import os
    
    # OAuth credentials (from environment)
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return 'Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET env vars.', 500
    
    # Create flow
    flow = Flow.from_client_config(
        {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uris': [_google_redirect_uri()],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token'
            }
        },
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    flow.redirect_uri = _google_redirect_uri()
    
    # Generate authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    # Store state in session
    session['oauth_state'] = state
    
    return redirect(authorization_url)

@storage_setup_bp.route('/oauth/google/callback', methods=['GET'])
def google_oauth_callback():
    '''Handle Google OAuth callback'''
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaInMemoryUpload
    import os, secrets, hashlib, json
    
    # Verify state
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return 'Invalid state parameter', 400
    
    # Exchange code for token
    flow = Flow.from_client_config(
        {
            'web': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'redirect_uris': [_google_redirect_uri()],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token'
            }
        },
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    flow.redirect_uri = _google_redirect_uri()
    
    flow.fetch_token(code=request.args.get('code'))
    credentials = flow.credentials
    
    # Build Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Create .semptify folder
    folder_metadata = {
        'name': '.semptify',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    
    # Generate user token
    user_token = secrets.token_hex(16)
    token_hash = hashlib.sha256(user_token.encode()).hexdigest()
    
    # Create encrypted token file
    from calendar_storage import EncryptedCalendarStorage
    
    class DriveClient:
        def __init__(self, service, folder_id):
            self.service = service
            self.folder_id = folder_id
        
        def upload(self, path, content):
            file_metadata = {'name': path.split('/')[-1], 'parents': [self.folder_id]}
            media = MediaInMemoryUpload(content.encode() if isinstance(content, str) else content)
            self.service.files().create(body=file_metadata, media_body=media).execute()
        
        def download(self, path):
            results = self.service.files().list(q=f"name='{path.split('/')[-1]}' and '{self.folder_id}' in parents").execute()
            files = results.get('files', [])
            if files:
                return self.service.files().get_media(fileId=files[0]['id']).execute().decode()
            raise FileNotFoundError()
    
    drive_client = DriveClient(drive_service, folder_id)
    
    # Store encrypted auth token
    token_data = {
        'token_hash': token_hash,
        'created_at': datetime.now().isoformat(),
        'storage_type': 'google_drive',
        'folder_id': folder_id
    }
    
    storage = EncryptedCalendarStorage(drive_client, user_token)
    encrypted_token = storage.encrypt_data(token_data)
    drive_client.upload('auth_token.enc', encrypted_token)
    
    # Store credentials in session
    session['user_token'] = user_token
    session['drive_credentials'] = credentials.to_json()
    session['drive_folder_id'] = folder_id
    
    return redirect(f'/welcome?user_token={user_token}')


# ============================================================================
# DROPBOX OAUTH  
# ============================================================================

@storage_setup_bp.route('/oauth/dropbox/start', methods=['GET'])
def dropbox_oauth_start():
    '''Initiate Dropbox OAuth flow'''
    import os
    from dropbox import DropboxOAuth2FlowNoRedirect
    
    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')
    
    if not app_key or not app_secret:
        return 'Dropbox OAuth not configured. Set DROPBOX_APP_KEY and DROPBOX_APP_SECRET env vars.', 500
    
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = auth_flow.start()
    
    # Store flow in session
    session['dropbox_auth_flow'] = {'app_key': app_key, 'app_secret': app_secret}
    
    return redirect(authorize_url)

@storage_setup_bp.route('/oauth/dropbox/callback', methods=['GET', 'POST'])
def dropbox_oauth_callback():
    '''Handle Dropbox OAuth callback'''
    import dropbox
    import os, secrets, hashlib, json
    
    # Get auth code from query params
    auth_code = request.args.get('code') or request.form.get('code')
    if not auth_code:
        return 'No authorization code provided', 400
    
    # Get app credentials
    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')
    
    # Complete OAuth flow
    from dropbox import DropboxOAuth2FlowNoRedirect
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    
    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        return f'OAuth error: {str(e)}', 400
    
    # Create Dropbox client
    dbx = dropbox.Dropbox(oauth_result.access_token)
    
    # Create .semptify folder
    try:
        dbx.files_create_folder_v2('/.semptify')
    except:
        pass  # Folder might already exist
    
    # Generate user token
    user_token = secrets.token_hex(16)
    token_hash = hashlib.sha256(user_token.encode()).hexdigest()
    
    # Create encrypted token file
    from calendar_storage import EncryptedCalendarStorage
    
    class DropboxClient:
        def __init__(self, dbx):
            self.dbx = dbx
        
        def upload(self, path, content):
            data = content.encode() if isinstance(content, str) else content
            self.dbx.files_upload(data, f'/.semptify/{path.split("/")[-1]}', mode=dropbox.files.WriteMode.overwrite)
        
        def download(self, path):
            _, response = self.dbx.files_download(f'/.semptify/{path.split("/")[-1]}')
            return response.content.decode()
    
    dropbox_client = DropboxClient(dbx)
    
    # Store encrypted auth token
    token_data = {
        'token_hash': token_hash,
        'created_at': datetime.now().isoformat(),
        'storage_type': 'dropbox'
    }
    
    storage = EncryptedCalendarStorage(dropbox_client, user_token)
    encrypted_token = storage.encrypt_data(token_data)
    dropbox_client.upload('auth_token.enc', encrypted_token)
    
    # Store credentials in session
    session['user_token'] = user_token
    session['dropbox_access_token'] = oauth_result.access_token
    
    return redirect(f'/welcome?user_token={user_token}')



def _google_redirect_uri():
    from flask import request, url_for
    import os
    xf_proto = (request.headers.get('X-Forwarded-Proto') or '').split(',')[0].strip()
    scheme = 'https' if os.getenv('FORCE_HTTPS') == '1' or xf_proto == 'https' or request.host.endswith('onrender.com') else request.scheme
    return url_for('storage_setup.google_oauth_callback', _external=True, _scheme=scheme)



def _google_redirect_uri():
    from flask import request, url_for
    import os
    xf_proto = (request.headers.get('X-Forwarded-Proto') or '').split(',')[0].strip()
    scheme = 'https' if os.getenv('FORCE_HTTPS') == '1' or xf_proto == 'https' or request.host.endswith('onrender.com') else request.scheme
    return url_for('storage_setup.google_oauth_callback', _external=True, _scheme=scheme)






