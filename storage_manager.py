"""
storage_manager.py - Tiered storage: R2 primary + Google Drive fallback
Single user (YOU) managing multiple client profiles with redundant cloud storage.
"""
import os
import json
from pathlib import Path
from typing import Optional, List
import threading

# R2 imports
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

# Google Drive imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    import io
    GDRIVE_AVAILABLE = True
except ImportError:
    GDRIVE_AVAILABLE = False

# --- Configuration ---
R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "semptify")

GDRIVE_CREDENTIALS_FILE = os.getenv("GDRIVE_CREDENTIALS_FILE", "security/gdrive_credentials.json")
GDRIVE_TOKEN_FILE = os.getenv("GDRIVE_TOKEN_FILE", "security/gdrive_token.json")
GDRIVE_FOLDER_NAME = os.getenv("GDRIVE_FOLDER_NAME", "Semptify_Storage")
GDRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.file']

STORAGE_MODE = os.getenv("STORAGE_MODE", "auto")  # auto, r2_only, gdrive_only, both

_local_root = Path("data/profiles")
_local_root.mkdir(parents=True, exist_ok=True)

_r2_client = None
_gdrive_service = None
_gdrive_folder_id = None
_lock = threading.Lock()

# --- R2 Setup ---
def _init_r2():
    global _r2_client
    if not BOTO3_AVAILABLE:
        return None
    if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
        return None
    try:
        _r2_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            region_name="auto"
        )
        # Test connection
        _r2_client.list_buckets()
        print("[OK] R2 connected")
        return _r2_client
    except Exception as e:
        print(f"[WARN] R2 init failed: {e}")
        return None

def get_r2_client():
    global _r2_client
    if _r2_client is None:
        with _lock:
            if _r2_client is None:
                _r2_client = _init_r2()
    return _r2_client

# --- Google Drive Setup ---
def _init_gdrive():
    global _gdrive_service, _gdrive_folder_id
    if not GDRIVE_AVAILABLE:
        return None
    
    creds = None
    token_path = Path(GDRIVE_TOKEN_FILE)
    creds_path = Path(GDRIVE_CREDENTIALS_FILE)
    
    # Load existing token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), GDRIVE_SCOPES)
        except Exception as e:
            print(f"[WARN] Failed to load token: {e}")
    
    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[WARN] Token refresh failed: {e}")
                creds = None
        
        if not creds and creds_path.exists():
            try:
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), GDRIVE_SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"[WARN] OAuth flow failed: {e}")
                return None
        
        if creds:
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_text(creds.to_json())
    
    if not creds:
        print("[WARN] Google Drive credentials unavailable")
        return None
    
    try:
        service = build('drive', 'v3', credentials=creds)
        _gdrive_service = service
        
        # Find or create Semptify folder
        results = service.files().list(
            q=f"name='{GDRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = results.get('files', [])
        if folders:
            _gdrive_folder_id = folders[0]['id']
            print(f"[OK] Google Drive connected (folder: {_gdrive_folder_id})")
        else:
            # Create folder
            file_metadata = {
                'name': GDRIVE_FOLDER_NAME,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            _gdrive_folder_id = folder.get('id')
            print(f"[OK] Created Google Drive folder: {_gdrive_folder_id}")
        
        return service
    except Exception as e:
        print(f"[WARN] Google Drive init failed: {e}")
        return None

def get_gdrive_service():
    global _gdrive_service
    if _gdrive_service is None:
        with _lock:
            if _gdrive_service is None:
                _gdrive_service = _init_gdrive()
    return _gdrive_service

# --- Storage Operations ---
def storage_available() -> dict:
    """Check which storage backends are available"""
    return {
        "r2": get_r2_client() is not None,
        "gdrive": get_gdrive_service() is not None,
        "local": True
    }

def _r2_key(profile_id: str, filename: str) -> str:
    return f"data/profiles/{profile_id}/{filename}"

def _gdrive_path(profile_id: str, filename: str) -> str:
    return f"{profile_id}/{filename}"

def upload_file(profile_id: str, filename: str, data: bytes) -> dict:
    """Upload to R2 (primary) and Google Drive (secondary)"""
    results = {"r2": False, "gdrive": False, "local": False}
    
    # Try R2 first
    if STORAGE_MODE in ["auto", "r2_only", "both"]:
        r2 = get_r2_client()
        if r2:
            try:
                r2.put_object(Bucket=R2_BUCKET, Key=_r2_key(profile_id, filename), Body=data)
                results["r2"] = True
                print(f"[OK] Uploaded to R2: {filename}")
            except Exception as e:
                print(f"[ERROR] R2 upload failed: {e}")
    
    # Try Google Drive
    if STORAGE_MODE in ["auto", "gdrive_only", "both"]:
        gdrive = get_gdrive_service()
        if gdrive and _gdrive_folder_id:
            try:
                # Check if profile folder exists
                profile_folder_id = _get_or_create_gdrive_folder(profile_id, _gdrive_folder_id)
                
                # Upload file
                file_metadata = {'name': filename, 'parents': [profile_folder_id]}
                media = MediaFileUpload(io.BytesIO(data), resumable=True)
                gdrive.files().create(body=file_metadata, media_body=media, fields='id').execute()
                results["gdrive"] = True
                print(f"[OK] Uploaded to Google Drive: {filename}")
            except Exception as e:
                print(f"[ERROR] Google Drive upload failed: {e}")
    
    # Always save local copy as final fallback
    try:
        dest = _local_root / profile_id
        dest.mkdir(parents=True, exist_ok=True)
        (dest / filename).write_bytes(data)
        results["local"] = True
    except Exception as e:
        print(f"[ERROR] Local save failed: {e}")
    
    return results

def download_file(profile_id: str, filename: str) -> Optional[bytes]:
    """Download from R2 (primary) or Google Drive (secondary) or local"""
    
    # Try R2 first
    if STORAGE_MODE in ["auto", "r2_only", "both"]:
        r2 = get_r2_client()
        if r2:
            try:
                obj = r2.get_object(Bucket=R2_BUCKET, Key=_r2_key(profile_id, filename))
                data = obj['Body'].read()
                print(f"[OK] Downloaded from R2: {filename}")
                return data
            except r2.exceptions.NoSuchKey:
                pass
            except Exception as e:
                print(f"[WARN] R2 download failed: {e}")
    
    # Try Google Drive
    if STORAGE_MODE in ["auto", "gdrive_only", "both"]:
        gdrive = get_gdrive_service()
        if gdrive:
            try:
                file_id = _find_gdrive_file(profile_id, filename)
                if file_id:
                    request = gdrive.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    fh.seek(0)
                    data = fh.read()
                    print(f"[OK] Downloaded from Google Drive: {filename}")
                    return data
            except Exception as e:
                print(f"[WARN] Google Drive download failed: {e}")
    
    # Try local fallback
    local_path = _local_root / profile_id / filename
    if local_path.exists():
        print(f"[OK] Downloaded from local: {filename}")
        return local_path.read_bytes()
    
    return None

def list_files(profile_id: str) -> List[str]:
    """List files from all available sources"""
    files = set()
    
    # R2
    if STORAGE_MODE in ["auto", "r2_only", "both"]:
        r2 = get_r2_client()
        if r2:
            try:
                prefix = f"data/profiles/{profile_id}/"
                resp = r2.list_objects_v2(Bucket=R2_BUCKET, Prefix=prefix)
                if "Contents" in resp:
                    files.update([o['Key'].replace(prefix, '') for o in resp['Contents'] if not o['Key'].endswith('/')])
            except Exception as e:
                print(f"[WARN] R2 list failed: {e}")
    
    # Google Drive
    if STORAGE_MODE in ["auto", "gdrive_only", "both"]:
        gdrive = get_gdrive_service()
        if gdrive:
            try:
                profile_folder_id = _find_gdrive_folder(profile_id)
                if profile_folder_id:
                    results = gdrive.files().list(
                        q=f"'{profile_folder_id}' in parents and trashed=false",
                        fields='files(name)'
                    ).execute()
                    files.update([f['name'] for f in results.get('files', [])])
            except Exception as e:
                print(f"[WARN] Google Drive list failed: {e}")
    
    # Local
    local_dir = _local_root / profile_id
    if local_dir.exists():
        files.update([p.name for p in local_dir.iterdir() if p.is_file()])
    
    return sorted(list(files))

# --- Google Drive Helpers ---
def _find_gdrive_folder(profile_id: str) -> Optional[str]:
    gdrive = get_gdrive_service()
    if not gdrive or not _gdrive_folder_id:
        return None
    try:
        results = gdrive.files().list(
            q=f"name='{profile_id}' and '{_gdrive_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields='files(id)'
        ).execute()
        folders = results.get('files', [])
        return folders[0]['id'] if folders else None
    except Exception:
        return None

def _get_or_create_gdrive_folder(profile_id: str, parent_id: str) -> str:
    existing = _find_gdrive_folder(profile_id)
    if existing:
        return existing
    
    gdrive = get_gdrive_service()
    file_metadata = {
        'name': profile_id,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = gdrive.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def _find_gdrive_file(profile_id: str, filename: str) -> Optional[str]:
    profile_folder_id = _find_gdrive_folder(profile_id)
    if not profile_folder_id:
        return None
    
    gdrive = get_gdrive_service()
    try:
        results = gdrive.files().list(
            q=f"name='{filename}' and '{profile_folder_id}' in parents and trashed=false",
            fields='files(id)'
        ).execute()
        files = results.get('files', [])
        return files[0]['id'] if files else None
    except Exception:
        return None

# --- Convenience wrappers for JSON ---
def save_json(profile_id: str, filename: str, obj) -> dict:
    data = json.dumps(obj, indent=2).encode('utf-8')
    return upload_file(profile_id, filename, data)

def load_json(profile_id: str, filename: str):
    data = download_file(profile_id, filename)
    if data:
        try:
            return json.loads(data.decode('utf-8'))
        except Exception:
            return None
    return None

# --- Initialize on import ---
print("[INFO] Initializing storage backends...")
avail = storage_available()
print(f"[INFO] Storage: R2={avail['r2']}, GoogleDrive={avail['gdrive']}, Local={avail['local']}")

