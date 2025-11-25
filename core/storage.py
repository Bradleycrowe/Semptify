"""
Semptify Unified Storage Framework
===================================
Site-wide storage backend for authentication and document management.

Three-tier architecture:
1. R2 (Cloudflare) - Database persistence + admin storage
2. Local Storage - Token hashes (security/users.json)
3. User Storage - OAuth2 clouds (Dropbox, Google Drive) or local fallback

This framework is imported by ALL modules (vault, calendar, timeline, complaints).
"""

import os
import secrets
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod


class StorageException(Exception):
    """Base exception for storage operations"""
    pass


class StorageClient(ABC):
    """Abstract base class for storage providers"""
    
    @abstractmethod
    def create_semptify_folder(self) -> bool:
        """Create .semptify folder in user's storage"""
        pass
    
    @abstractmethod
    def upload_encrypted_token(self, token: str, encrypted_data: str) -> bool:
        """Upload encrypted token to user's storage"""
        pass
    
    @abstractmethod
    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage provider information"""
        pass


class GoogleDriveClient(StorageClient):
    """Google Drive OAuth2 storage client"""
    
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = None
        
    def create_semptify_folder(self) -> bool:
        """Create .semptify folder in Google Drive"""
        try:
            from googleapiclient.discovery import build
            self.service = build('drive', 'v3', credentials=self.credentials)
            
            # Search for existing folder
            results = self.service.files().list(
                q="name='.semptify' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            if results.get('files'):
                return True
            
            # Create folder
            folder_metadata = {
                'name': '.semptify',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            self.service.files().create(body=folder_metadata, fields='id').execute()
            return True
            
        except Exception as e:
            raise StorageException(f"Failed to create Drive folder: {e}")
    
    def upload_encrypted_token(self, token: str, encrypted_data: str) -> bool:
        """Upload encrypted token to Google Drive"""
        try:
            from googleapiclient.http import MediaInMemoryUpload
            
            # Find .semptify folder
            results = self.service.files().list(
                q="name='.semptify' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive',
                fields='files(id)'
            ).execute()
            
            if not results.get('files'):
                raise StorageException(".semptify folder not found")
            
            folder_id = results['files'][0]['id']
            
            # Upload encrypted token
            file_metadata = {
                'name': f'token_{token[:4]}.enc',
                'parents': [folder_id]
            }
            media = MediaInMemoryUpload(encrypted_data.encode(), mimetype='text/plain')
            self.service.files().create(body=file_metadata, media_body=media).execute()
            return True
            
        except Exception as e:
            raise StorageException(f"Failed to upload to Drive: {e}")
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get Google Drive storage information"""
        return {
            'provider': 'google_drive',
            'status': 'connected'
        }


class DropboxClient(StorageClient):
    """Dropbox OAuth2 storage client"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.dbx = None
        
    def create_semptify_folder(self) -> bool:
        """Create .semptify folder in Dropbox"""
        try:
            import dropbox
            self.dbx = dropbox.Dropbox(self.access_token)
            
            try:
                self.dbx.files_get_metadata('/.semptify')
                return True
            except:
                self.dbx.files_create_folder_v2('/.semptify')
                return True
                
        except Exception as e:
            raise StorageException(f"Failed to create Dropbox folder: {e}")
    
    def upload_encrypted_token(self, token: str, encrypted_data: str) -> bool:
        """Upload encrypted token to Dropbox"""
        try:
            path = f'/.semptify/token_{token[:4]}.enc'
            self.dbx.files_upload(
                encrypted_data.encode(),
                path,
                mode=dropbox.files.WriteMode.overwrite
            )
            return True
            
        except Exception as e:
            raise StorageException(f"Failed to upload to Dropbox: {e}")
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get Dropbox storage information"""
        return {
            'provider': 'dropbox',
            'status': 'connected'
        }


class LocalClient(StorageClient):
    """Local filesystem storage client (fallback)"""
    
    def __init__(self, base_path: str = 'uploads'):
        self.base_path = base_path
        
    def create_semptify_folder(self) -> bool:
        """Create .semptify folder locally"""
        try:
            folder = os.path.join(self.base_path, '.semptify')
            os.makedirs(folder, exist_ok=True)
            return True
        except Exception as e:
            raise StorageException(f"Failed to create local folder: {e}")
    
    def upload_encrypted_token(self, token: str, encrypted_data: str) -> bool:
        """Save encrypted token locally"""
        try:
            path = os.path.join(self.base_path, '.semptify', f'token_{token[:4]}.enc')
            with open(path, 'w') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            raise StorageException(f"Failed to save locally: {e}")
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get local storage information"""
        return {
            'provider': 'local',
            'status': 'connected',
            'path': self.base_path
        }


class UnifiedStorageBackend:
    """
    Unified storage backend for Semptify.
    
    Handles:
    - Token generation (12-digit anonymous tokens)
    - Token hashing (SHA-256)
    - Hash storage (security/users.json)
    - Encrypted token upload (user's cloud)
    - Provider abstraction (Google Drive, Dropbox, Local)
    """
    
    def __init__(self, client: StorageClient):
        self.client = client
        self.users_file = 'security/users.json'
        
    @staticmethod
    def generate_token(length: int = 12) -> str:
        """Generate anonymous numeric token"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    
    @staticmethod
    def hash_token(token: str) -> str:
        """Hash token with SHA-256"""
        return hashlib.sha256(token.encode()).hexdigest()
    
    def store_token_hash(self, token: str, metadata: Optional[Dict] = None) -> bool:
        """Store token hash in security/users.json"""
        try:
            os.makedirs('security', exist_ok=True)
            
            # Load existing users
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
            else:
                users = {}
            
            # Add new user
            token_hash = self.hash_token(token)
            users[token_hash] = {
                'created_at': datetime.now().isoformat(),
                'provider': self.client.get_storage_info()['provider'],
                **(metadata or {})
            }
            
            # Save atomically
            temp_file = f'{self.users_file}.tmp'
            with open(temp_file, 'w') as f:
                json.dump(users, f, indent=2)
            os.replace(temp_file, self.users_file)
            
            return True
            
        except Exception as e:
            raise StorageException(f"Failed to store token hash: {e}")
    
    def setup_user_storage(self, token: str, encrypted_data: Optional[str] = None) -> Tuple[bool, Dict]:
        """
        Complete user storage setup flow.
        
        Steps:
        1. Create .semptify folder in user's storage
        2. Upload encrypted token (if provided)
        3. Store token hash in security/users.json
        
        Returns: (success, info_dict)
        """
        try:
            # Create folder
            self.client.create_semptify_folder()
            
            # Upload encrypted token if provided
            if encrypted_data:
                self.client.upload_encrypted_token(token, encrypted_data)
            
            # Store hash
            self.store_token_hash(token)
            
            return True, {
                'token': token,
                'storage_info': self.client.get_storage_info(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate token against security/users.json"""
        try:
            users_file = 'security/users.json'
            if not os.path.exists(users_file):
                return False
            
            with open(users_file, 'r') as f:
                users = json.load(f)
            
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            return token_hash in users
            
        except Exception:
            return False


# Convenience factory functions
def create_google_drive_backend(credentials) -> UnifiedStorageBackend:
    """Create backend with Google Drive client"""
    return UnifiedStorageBackend(GoogleDriveClient(credentials))


def create_dropbox_backend(access_token: str) -> UnifiedStorageBackend:
    """Create backend with Dropbox client"""
    return UnifiedStorageBackend(DropboxClient(access_token))


def create_local_backend(base_path: str = 'uploads') -> UnifiedStorageBackend:
    """Create backend with local filesystem client"""
    return UnifiedStorageBackend(LocalClient(base_path))
