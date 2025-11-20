"""
Storage Setup Routes - User-Owned Storage Only
OAuth-based setup for Google Drive and Dropbox
Users store their own data; Semptify never stores user documents
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
import os
import secrets
import json
from datetime import datetime

storage_setup_bp = Blueprint('storage_setup', __name__)

# ============================================================================
# STORAGE SELECTION
# ============================================================================

@storage_setup_bp.route('/setup', methods=['GET'])
def choose_storage():
    """Storage provider selection - Google Drive or Dropbox only"""
    return render_template('storage_setup/choose_storage.html')

@storage_setup_bp.route('/setup/dropbox/guide', methods=['GET'])
def dropbox_storage_guide():
    """Dropbox OAuth wizard"""
    return render_template('storage_setup/dropbox_guide.html')

@storage_setup_bp.route('/setup/drive/guide', methods=['GET'])
def drive_storage_guide():
    """Google Drive OAuth wizard"""
    return render_template('storage_setup/drive_guide.html')

@storage_setup_bp.route('/welcome', methods=['GET'])
def welcome():
    '''Welcome page after successful storage setup'''
    user_token = request.args.get('user_token', 'your-secure-token')
    storage_provider = 'Google Drive' if 'drive_credentials' in session else 'Dropbox' if 'dropbox_access_token' in session else 'your storage'
    return render_template('storage_setup/welcome.html', user_token=user_token, storage_provider=storage_provider)

# ============================================================================
# GOOGLE DRIVE OAUTH
# ============================================================================

@storage_setup_bp.route('/oauth/google/start', methods=['GET'])
def google_oauth_start():
    '''Initiate Google OAuth flow'''
    try:
        from google_auth_oauthlib.flow import Flow
    except ImportError:
        return render_template('storage_setup/oauth_unavailable.html', provider='Google Drive'), 503

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

    if not client_id or not client_secret:
        return 'Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET env vars.', 500

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

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    session['oauth_state'] = state
    return redirect(authorization_url)

@storage_setup_bp.route('/oauth/google/callback', methods=['GET'])
def google_oauth_callback():
    """Handle Google OAuth callback (secure, with diagnostics and fallback)"""
    try:
        from google_auth_oauthlib.flow import Flow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload
    except ImportError:
        print('[OAUTH][Google] Libraries missing')
        return render_template('storage_setup/oauth_unavailable.html', provider='Google Drive'), 503

    if request.args.get('state') != session.get('oauth_state'):
        print('[OAUTH][Google][ERROR] State mismatch', request.args.get('state'), session.get('oauth_state'))
        return 'Invalid state parameter', 400

    code = request.args.get('code')
    if not code:
        print('[OAUTH][Google][ERROR] Missing code param')
        return 'Missing authorization code', 400

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    if not client_id or not client_secret:
        print('[OAUTH][Google][ERROR] Missing client credentials')
        return 'Google OAuth not configured', 500

    redirect_uri = _google_redirect_uri()
    # Force https scheme
    if redirect_uri.startswith('http://'):
        redirect_uri = 'https://' + redirect_uri[7:]

    flow = Flow.from_client_config({
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uris': [redirect_uri],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token'
        }
    }, scopes=['https://www.googleapis.com/auth/drive.file'])
    flow.redirect_uri = redirect_uri

    try:
        print(f'[OAUTH][Google] START token fetch: code={code[:15]}..., redirect_uri={redirect_uri}')
        print(f'[OAUTH][Google] token_uri={flow.client_config.get("token_uri")}')
        flow.fetch_token(code=code)
        print('[OAUTH][Google] Primary fetch SUCCESS')
    except Exception as e:
        import traceback
        print(f'[OAUTH][Google][ERROR] === PRIMARY TOKEN FETCH FAILED ===')
        print(f'[OAUTH][Google][ERROR] Type: {type(e).__name__}')
        print(f'[OAUTH][Google][ERROR] Message: {str(e)}')
        print(f'[OAUTH][Google][ERROR] Code (first 15 chars): {code[:15]}...')
        print(f'[OAUTH][Google][ERROR] Redirect URI used: {redirect_uri}')
        full_tb = traceback.format_exc()
        print(f'[OAUTH][Google][ERROR] Traceback:\n{full_tb}')
        auth_url = request.url
        if auth_url.startswith('http://'):
            auth_url = 'https://' + auth_url[7:]
        try:
            print(f'[OAUTH][Google] FALLBACK: authorization_response={auth_url}')
            flow.fetch_token(authorization_response=auth_url)
            print('[OAUTH][Google] Fallback fetch SUCCESS')
        except Exception as e2:
            print(f'[OAUTH][Google][ERROR] === FALLBACK ALSO FAILED ===')
            print(f'[OAUTH][Google][ERROR] Type: {type(e2).__name__}')
            print(f'[OAUTH][Google][ERROR] Message: {str(e2)}')
            full_tb2 = traceback.format_exc()
            print(f'[OAUTH][Google][ERROR] Fallback traceback:\n{full_tb2}')
            
            error_detail = f"{type(e2).__name__}: {str(e2)[:200]}"
            return render_template('storage_setup/oauth_error.html', 
                                 error_message=error_detail,
                                 provider='Google Drive'), 500

    credentials = flow.credentials

    drive_service = build('drive', 'v3', credentials=credentials)
    query = "name='.semptify' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id,name)').execute()
    files = results.get('files', [])
    if files:
        folder_id = files[0]['id']
    else:
        folder_metadata = {'name': '.semptify', 'mimeType': 'application/vnd.google-apps.folder'}
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder['id']

    session['drive_credentials'] = {
        'token': credentials.token,
        'refresh_token': getattr(credentials, 'refresh_token', None),
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    session['drive_folder_id'] = folder_id

    class DriveClient:
        def __init__(self, credentials):
            self.service = build('drive', 'v3', credentials=credentials)
            self.folder_id = session.get('drive_folder_id')
        def upload(self, path, content):
            filename = path.split('/')[-1]
            media = MediaInMemoryUpload(content.encode() if isinstance(content, str) else content)
            q = f"name='{filename}' and '{self.folder_id}' in parents and trashed=false"
            r = self.service.files().list(q=q, fields='files(id)').execute()
            existing = r.get('files', [])
            if existing:
                self.service.files().update(fileId=existing[0]['id'], media_body=media).execute()
            else:
                meta = {'name': filename, 'parents': [self.folder_id]}
                self.service.files().create(body=meta, media_body=media).execute()

    drive_client = DriveClient(credentials)
    user_token = ''.join(secrets.choice('0123456789') for _ in range(12))

    from calendar_storage import EncryptedCalendarStorage
    from security import _hash_token
    token_data = {'token': user_token, 'created_at': datetime.utcnow().isoformat(), 'storage_type': 'google_drive'}
    storage = EncryptedCalendarStorage(drive_client, user_token)
    encrypted_token = storage.encrypt_data(token_data)
    drive_client.upload('auth_token.enc', encrypted_token)

    token_hash_str = _hash_token(user_token)
    drive_client.upload('token_hash.txt', token_hash_str)

    token_hash = _hash_token(user_token)
    os.makedirs('security', exist_ok=True)
    users_file = 'security/users.json'
    users = {}
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    users[token_hash] = {'created_at': datetime.utcnow().isoformat(), 'storage': 'google_drive'}
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)

    print('[OAUTH][Google] Success folder_id=' + folder_id)
    return redirect('/welcome')

# ============================================================================
# DROPBOX OAUTH
# ============================================================================

@storage_setup_bp.route('/oauth/dropbox/start', methods=['GET'])
def dropbox_oauth_start():
    '''Initiate Dropbox OAuth flow'''
    from dropbox import DropboxOAuth2FlowNoRedirect

    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')

    if not app_key or not app_secret:
        return 'Dropbox OAuth not configured. Set DROPBOX_APP_KEY and DROPBOX_APP_SECRET env vars.', 500

    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = auth_flow.start()
    
    session['dropbox_auth_flow'] = {'app_key': app_key, 'app_secret': app_secret}
    return render_template('storage_setup/dropbox_auth.html', authorize_url=authorize_url)

@storage_setup_bp.route('/oauth/dropbox/callback', methods=['GET'])
def dropbox_oauth_callback():
    '''Handle Dropbox OAuth callback (automatic redirect)'''
    import dropbox
    from dropbox import DropboxOAuth2Flow

    # Validate state parameter
    state_param = request.args.get('state')
    expected_state = session.get('dropbox_oauth_state')
    if state_param != expected_state:
        print(f'[OAUTH][Dropbox][ERROR] State mismatch')
        return render_template('storage_setup/oauth_error.html', 
                             error_message='Invalid state parameter',
                             provider='Dropbox'), 400

    auth_code = request.args.get('code')
    if not auth_code:
        error = request.args.get('error_description', 'No authorization code provided')
        print(f'[OAUTH][Dropbox][ERROR] {error}')
        return render_template('storage_setup/oauth_error.html', 
                             error_message=error,
                             provider='Dropbox'), 400

    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')
    redirect_uri = session.get('dropbox_redirect_uri')

    auth_flow = DropboxOAuth2Flow(
        app_key, 
        app_secret,
        redirect_uri,
        session,
        'dropbox_auth_flow'
    )

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        return f'OAuth error: {str(e)}', 400

    # Create Dropbox client
    dbx = dropbox.Dropbox(oauth_result.access_token)

    # Create .semptify folder
    try:
        dbx.files_create_folder_v2('/.semptify')
    except dropbox.exceptions.ApiError:
        pass  # Folder already exists

    # Create DropboxClient helper
    class DropboxClient:
        def __init__(self, dbx):
            self.dbx = dbx

        def upload(self, path, content):
            data = content.encode() if isinstance(content, str) else content
            self.dbx.files_upload(data, f'/.semptify/{path.split("/")[-1]}', mode=dropbox.files.WriteMode.overwrite)

        def download(self, path):
            _, response = self.dbx.files_download(f'/.semptify/{path.split("/")[-1]}')
            return response.content

    dropbox_client = DropboxClient(dbx)

    # Generate user token
    user_token = ''.join(secrets.choice('0123456789') for _ in range(12))

    # Store encrypted token in user's Dropbox
    from calendar_storage import EncryptedCalendarStorage
    token_data = {'token': user_token, 'created_at': datetime.utcnow().isoformat(), 'storage_type': 'dropbox'}
    storage = EncryptedCalendarStorage(dropbox_client, user_token)
    encrypted_token = storage.encrypt_data(token_data)
    dropbox_client.upload('auth_token.enc', encrypted_token)
    
    # Write token hash for cross-device verification
    from security import _hash_token
    token_hash_str = _hash_token(user_token)
    dropbox_client.upload('token_hash.txt', token_hash_str)

    # Store user token hash in server security file
    from security import _hash_token
    token_hash = _hash_token(user_token)
    users_file = 'security/users.json'
    os.makedirs('security', exist_ok=True)
    users = {}
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    users[token_hash] = {'created_at': datetime.utcnow().isoformat(), 'storage': 'dropbox'}
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)

    session['dropbox_access_token'] = oauth_result.access_token

    return redirect('/welcome')

# ============================================================================
# HELPERS
# ============================================================================

def _google_redirect_uri():
    '''Build HTTPS-aware redirect URI for Google OAuth'''
    scheme = 'https' if (request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https' or os.getenv('FORCE_HTTPS') == '1') else 'http'
    return url_for('storage_setup.google_oauth_callback', _external=True, _scheme=scheme)






