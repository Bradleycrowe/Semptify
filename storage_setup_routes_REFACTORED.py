"""
Storage Setup Routes - Refactored to use core/storage.py framework
Consolidated from ~450 lines to ~200 lines using UnifiedStorageBackend
"""

from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
import os
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import dropbox
from dropbox import DropboxOAuth2Flow

# Import unified storage framework
from core.storage import (
    create_google_drive_backend,
    create_dropbox_backend,
    create_local_backend,
    UnifiedStorageBackend,
    StorageException
)
from calendar_storage import EncryptedCalendarStorage

# Blueprint setup
storage_setup_bp = Blueprint('storage_setup', __name__)

# OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
DROPBOX_APP_KEY = os.getenv('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.getenv('DROPBOX_APP_SECRET')

SCOPES = ['https://www.googleapis.com/auth/drive.file']


@storage_setup_bp.route('/choose-storage')
def choose_storage():
    """Storage provider selection page"""
    return render_template('storage_choice.html')


@storage_setup_bp.route('/dropbox-guide')
def dropbox_storage_guide():
    """Dropbox setup guide"""
    return render_template('dropbox_storage_guide.html')


@storage_setup_bp.route('/drive-guide')
def drive_storage_guide():
    """Google Drive setup guide"""
    return render_template('drive_storage_guide.html')


@storage_setup_bp.route('/setup-storage')
def welcome():
    """Storage setup welcome page"""
    return render_template('setup_storage.html')


# =============================================================================
# GOOGLE DRIVE OAUTH
# =============================================================================

@storage_setup_bp.route('/google-oauth-start')
def google_oauth_start():
    """Initiate Google Drive OAuth flow"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=url_for('storage_setup.google_oauth_callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['google_oauth_state'] = state
    return redirect(authorization_url)


@storage_setup_bp.route('/google-oauth-callback')
def google_oauth_callback():
    """
    Google OAuth callback - REFACTORED to use UnifiedStorageBackend
    Reduced from ~150 lines to ~30 lines
    """
    try:
        # Complete OAuth flow
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=SCOPES,
            redirect_uri=url_for('storage_setup.google_oauth_callback', _external=True),
            state=session.get('google_oauth_state')
        )
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Use unified storage backend
        backend = create_google_drive_backend(credentials)
        token = UnifiedStorageBackend.generate_token()
        
        # Encrypt token for cloud storage
        encrypted_storage = EncryptedCalendarStorage(token)
        encrypted_data = encrypted_storage.encrypt_data({'token': token})
        
        # Complete setup using framework
        success, info = backend.setup_user_storage(token, encrypted_data)
        
        if success:
            session['user_token'] = token
            session['storage_provider'] = 'google_drive'
            return redirect(url_for('register_success', token=token))
        else:
            return f"Setup failed: {info.get('error')}", 500
            
    except Exception as e:
        current_app.logger.error(f"Google OAuth error: {e}")
        return f"OAuth error: {str(e)}", 500


# =============================================================================
# DROPBOX OAUTH
# =============================================================================

@storage_setup_bp.route('/dropbox-oauth-start')
def dropbox_oauth_start():
    """Initiate Dropbox OAuth flow"""
    redirect_uri = url_for('storage_setup.dropbox_oauth_callback', _external=True)
    flow = DropboxOAuth2Flow(
        DROPBOX_APP_KEY,
        DROPBOX_APP_SECRET,
        redirect_uri,
        session,
        'dropbox-auth-csrf-token'
    )
    auth_url = flow.start()
    return redirect(auth_url)


@storage_setup_bp.route('/dropbox-oauth-callback')
def dropbox_oauth_callback():
    """
    Dropbox OAuth callback - REFACTORED to use UnifiedStorageBackend
    Reduced from ~150 lines to ~30 lines
    """
    try:
        # Complete OAuth flow
        redirect_uri = url_for('storage_setup.dropbox_oauth_callback', _external=True)
        flow = DropboxOAuth2Flow(
            DROPBOX_APP_KEY,
            DROPBOX_APP_SECRET,
            redirect_uri,
            session,
            'dropbox-auth-csrf-token'
        )
        oauth_result = flow.finish(request.args)
        access_token = oauth_result.access_token
        
        # Use unified storage backend
        backend = create_dropbox_backend(access_token)
        token = UnifiedStorageBackend.generate_token()
        
        # Encrypt token for cloud storage
        encrypted_storage = EncryptedCalendarStorage(token)
        encrypted_data = encrypted_storage.encrypt_data({'token': token})
        
        # Complete setup using framework
        success, info = backend.setup_user_storage(token, encrypted_data)
        
        if success:
            session['user_token'] = token
            session['storage_provider'] = 'dropbox'
            return redirect(url_for('register_success', token=token))
        else:
            return f"Setup failed: {info.get('error')}", 500
            
    except Exception as e:
        current_app.logger.error(f"Dropbox OAuth error: {e}")
        return f"OAuth error: {str(e)}", 500


# =============================================================================
# LOCAL STORAGE (SKIP OAUTH)
# =============================================================================

@storage_setup_bp.route('/skip-setup', methods=['POST'])
def skip_setup():
    """
    Skip cloud storage, use local - REFACTORED to use UnifiedStorageBackend
    Reduced from ~100 lines to ~20 lines
    """
    try:
        # Use local backend
        backend = create_local_backend('uploads')
        token = UnifiedStorageBackend.generate_token()
        
        # Complete setup (no encryption needed for local)
        success, info = backend.setup_user_storage(token)
        
        if success:
            session['user_token'] = token
            session['storage_provider'] = 'local'
            return redirect(url_for('register_success', token=token))
        else:
            return f"Setup failed: {info.get('error')}", 500
            
    except Exception as e:
        current_app.logger.error(f"Local setup error: {e}")
        return f"Setup error: {str(e)}", 500


# =============================================================================
# HELPER ROUTES
# =============================================================================

@storage_setup_bp.route('/storage-status')
def storage_status():
    """Check storage connection status"""
    token = session.get('user_token')
    if not token:
        return {'status': 'no_token'}, 401
    
    if UnifiedStorageBackend.validate_token(token):
        return {
            'status': 'connected',
            'provider': session.get('storage_provider', 'unknown'),
            'token_valid': True
        }
    else:
        return {'status': 'invalid_token'}, 401
