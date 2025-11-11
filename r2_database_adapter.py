"""
R2-backed SQLite database adapter for persistent storage across Render deploys.

Instead of storing users.db locally (ephemeral on Render free tier), this adapter:
1. Downloads users.db from R2 on startup (if exists)
2. Uses local SQLite normally during runtime
3. Periodically syncs changes back to R2
4. Uploads on shutdown/deploy

This gives you persistent user data without needing Render Persistent Disk.
"""

import os
import sqlite3
import time
import atexit
from pathlib import Path

# Try to import boto3 for R2 support
try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

DB_PATH = "security/users.db"
R2_DB_KEY = "database/users.db"  # Path in R2 bucket


class R2DatabaseAdapter:
    """Manages SQLite database with R2 backup/restore."""
    
    def __init__(self):
        self.enabled = False
        self.s3_client = None
        self.bucket = os.getenv('R2_BUCKET_NAME', 'semptify-storage')
        self.last_sync = 0
        self.sync_interval = 300  # Sync every 5 minutes
        
        if self._init_r2():
            self.enabled = True
            self._restore_from_r2()
            atexit.register(self._backup_to_r2)
            print(f"✓ R2 database persistence enabled (bucket: {self.bucket})")
        else:
            print("⚠ R2 not configured - using local-only database (ephemeral)")
    
    def _init_r2(self):
        """Initialize R2 connection."""
        if not HAS_BOTO3:
            return False
        
        required = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY']
        if not all(os.getenv(var) for var in required):
            return False
        
        try:
            account_id = os.getenv('R2_ACCOUNT_ID')
            self.s3_client = boto3.client(
                's3',
                endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
                region_name='auto'
            )
            return True
        except Exception as e:
            print(f"⚠ R2 init failed: {e}")
            return False
    
    def _restore_from_r2(self):
        """Download database from R2 if exists."""
        if not self.enabled:
            return
        
        try:
            # Check if database exists in R2
            self.s3_client.head_object(Bucket=self.bucket, Key=R2_DB_KEY)
            
            # Download to local path
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            self.s3_client.download_file(self.bucket, R2_DB_KEY, DB_PATH)
            print(f"✓ Restored database from R2 ({R2_DB_KEY})")
            
        except self.s3_client.exceptions.NoSuchKey:
            print("ℹ No existing database in R2 - starting fresh")
        except Exception as e:
            print(f"⚠ Failed to restore from R2: {e}")
    
    def _backup_to_r2(self):
        """Upload current database to R2."""
        if not self.enabled or not os.path.exists(DB_PATH):
            return
        
        try:
            self.s3_client.upload_file(DB_PATH, self.bucket, R2_DB_KEY)
            self.last_sync = time.time()
            print(f"✓ Backed up database to R2 ({R2_DB_KEY})")
        except Exception as e:
            print(f"⚠ Failed to backup to R2: {e}")
    
    def sync_if_needed(self):
        """Periodic sync to R2 (call this in background task or after writes)."""
        if not self.enabled:
            return
        
        now = time.time()
        if now - self.last_sync >= self.sync_interval:
            self._backup_to_r2()


# Global instance
_r2_db_adapter = None


def get_r2_adapter():
    """Get or create R2 database adapter singleton."""
    global _r2_db_adapter
    if _r2_db_adapter is None:
        _r2_db_adapter = R2DatabaseAdapter()
    return _r2_db_adapter


def init_r2_database():
    """Initialize R2 database adapter (call on app startup)."""
    return get_r2_adapter()


def sync_database_to_r2():
    """Manually trigger database sync to R2."""
    adapter = get_r2_adapter()
    if adapter.enabled:
        adapter._backup_to_r2()


# Example usage in user_database.py:
# After any significant write operation:
#   from r2_database_adapter import sync_database_to_r2
#   sync_database_to_r2()
