"""
Storage Auto-Unlock
Before-request detection: if user has Drive/Dropbox session, check for .semptify/auth_token.enc
If token provided, decrypt and authorize; else show unlock prompt
"""
from flask import Blueprint, request, session, redirect, render_template, g
from calendar_storage import EncryptedCalendarStorage
import os

storage_autologin_bp = Blueprint('storage_autologin', __name__)

def _get_storage_client():
    """Get Drive or Dropbox client from session"""
    if 'drive_credentials' in session:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload
        
        creds = Credentials(**session['drive_credentials'])
        service = build('drive', 'v3', credentials=creds)
        folder_id = session.get('drive_folder_id')
        
        class DriveClient:
            def __init__(self, svc, fid):
                self.service = svc
                self.folder_id = fid
            
            def upload(self, path, content):
                filename = path.split('/')[-1]
                media = MediaInMemoryUpload(content.encode() if isinstance(content, str) else content)
                query = f"name='{filename}' and '{self.folder_id}' in parents and trashed=false"
                results = self.service.files().list(q=query, fields='files(id)').execute()
                existing = results.get('files', [])
                if existing:
                    self.service.files().update(fileId=existing[0]['id'], media_body=media).execute()
                else:
                    file_metadata = {'name': filename, 'parents': [self.folder_id]}
                    self.service.files().create(body=file_metadata, media_body=media).execute()
            
            def download(self, path):
                filename = path.split('/')[-1]
                query = f"name='{filename}' and '{self.folder_id}' in parents and trashed=false"
                results = self.service.files().list(q=query, fields='files(id)').execute()
                files = results.get('files', [])
                if not files:
                    raise FileNotFoundError(f"{filename} not found")
                return self.service.files().get_media(fileId=files[0]['id']).execute()
        
        return DriveClient(service, folder_id), 'google_drive'
    
    elif 'dropbox_access_token' in session:
        import dropbox
        
        dbx = dropbox.Dropbox(session['dropbox_access_token'])
        
        class DropboxClient:
            def __init__(self, d):
                self.dbx = d
            
            def upload(self, path, content):
                data = content.encode() if isinstance(content, str) else content
                self.dbx.files_upload(data, f'/.semptify/{path.split("/")[-1]}', mode=dropbox.files.WriteMode.overwrite)
            
            def download(self, path):
                _, response = self.dbx.files_download(f'/.semptify/{path.split("/")[-1]}')
                return response.content
        
        return DropboxClient(dbx), 'dropbox'
    
    return None, None

@storage_autologin_bp.before_app_request
def check_storage_auth():
    """Auto-detect storage and authorize if token present"""
    # Skip for static, setup, OAuth, and unlock routes
    if request.path.startswith(('/static/', '/setup', '/oauth/', '/unlock')):
        return
    
    # Check if already authorized
    if hasattr(g, 'user_token') and g.user_token:
        return
    
    # Get user token from request
    user_token = request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')
    
    # Get storage client
    storage_client, storage_type = _get_storage_client()
    
    if not storage_client:
        # No storage connected, redirect to setup
        if request.path not in ('/', '/index', '/home'):
            return redirect('/setup')
        return
    
    # Storage is connected, check for auth_token.enc and auto-login
    try:
        encrypted_token_data = storage_client.download('auth_token.enc')
        
        # Auto-decrypt using token hash as key
        try:
            token_hash_data = storage_client.download('token_hash.txt')
            stored_hash = token_hash_data.decode().strip() if isinstance(token_hash_data, bytes) else token_hash_data.strip()
            
            # Use hash as decryption key to retrieve actual token
            storage = EncryptedCalendarStorage(storage_client, stored_hash)
            decrypted = storage.decrypt_data(encrypted_token_data.decode() if isinstance(encrypted_token_data, bytes) else encrypted_token_data)
            
            actual_token = decrypted.get('token')
            if actual_token:
                # Auto-authorized! Store in g and session
                g.user_token = actual_token
                g.storage_client = storage_client
                g.storage_type = storage_type
                session['auto_authorized'] = True
                return
        except:
            pass
        
        # If we have user_token in request, try that too
        if user_token:
            try:
                storage = EncryptedCalendarStorage(storage_client, user_token)
                decrypted = storage.decrypt_data(encrypted_token_data.decode() if isinstance(encrypted_token_data, bytes) else encrypted_token_data)
                if decrypted.get('token') == user_token:
                    g.user_token = user_token
                    g.storage_client = storage_client
                    g.storage_type = storage_type
                    return
            except:
                pass
        
        # Couldn't auto-login, redirect to setup
        if request.path not in ('/setup', '/welcome', '/vault'):
            return redirect('/setup')
    
    except FileNotFoundError:
        # No auth_token.enc, show unlock page
        if request.path not in ('/setup', '/welcome', '/unlock', '/', '/index'):
            return redirect(url_for('storage_autologin.unlock', next=request.path))

@storage_autologin_bp.route('/unlock', methods=['GET', 'POST'])
def unlock():
    """Unlock form to enter user token"""
    if request.method == 'POST':
        user_token = request.form.get('user_token', '').strip()
        next_url = request.form.get('next', '/') or '/'
        
        if user_token:
            # Verify and redirect with token
            return redirect(f'{next_url}?user_token={user_token}')
    
    next_url = request.args.get('next', '/')
    storage_client, storage_type = _get_storage_client()
    
    return render_template('unlock.html', next_url=next_url, storage_type=storage_type)

