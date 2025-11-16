"""
Database Persistence Service - Sync SQLite to cloud storage
Solves ephemeral container storage by backing up DB to R2/GCS
"""
import os
import shutil
import time
from datetime import datetime
from typing import Optional


class DatabasePersistenceService:
    """Sync SQLite database to/from cloud storage for persistence."""
    
    def __init__(self, db_path: str = "users.db", backup_key: str = "database/users.db"):
        self.db_path = db_path
        self.backup_key = backup_key
        self.storage = None
    
    def _get_storage(self):
        """Lazy load storage adapter."""
        if self.storage is None:
            from storage_adapter import StorageAdapter
            self.storage = StorageAdapter()
        return self.storage
    
    def restore_from_cloud(self) -> bool:
        """
        Restore database from cloud storage on startup.
        Returns True if restored, False if no backup exists.
        """
        print("[DB-PERSIST] Checking for cloud database backup...")
        
        storage = self._get_storage()
        
        # Check if backup exists
        if not storage.file_exists(self.backup_key):
            print("[DB-PERSIST] No cloud backup found, starting fresh")
            return False
        
        try:
            # Download database
            print(f"[DB-PERSIST] Restoring database from {self.backup_key}...")
            db_data = storage.read_file(self.backup_key)
            
            # Write to local file
            with open(self.db_path, 'wb') as f:
                f.write(db_data if isinstance(db_data, bytes) else db_data.encode())
            
            size_kb = len(db_data) / 1024
            print(f"[DB-PERSIST] ✓ Restored {size_kb:.2f} KB from cloud")
            return True
            
        except Exception as e:
            print(f"[DB-PERSIST] ✗ Restore failed: {e}")
            return False
    
    def backup_to_cloud(self, force: bool = False) -> bool:
        """
        Backup database to cloud storage.
        
        Args:
            force: Backup even if file hasn't changed
        
        Returns:
            True if backup successful
        """
        if not os.path.exists(self.db_path):
            print(f"[DB-PERSIST] Database not found: {self.db_path}")
            return False
        
        try:
            storage = self._get_storage()
            
            # Read database file
            with open(self.db_path, 'rb') as f:
                db_data = f.read()
            
            # Create metadata
            metadata = {
                "backup_time": datetime.now().isoformat(),
                "size_bytes": len(db_data),
                "db_path": self.db_path
            }
            
            # Upload to cloud
            result = storage.save_file(self.backup_key, db_data, metadata=metadata)
            
            if result:
                size_kb = len(db_data) / 1024
                print(f"[DB-PERSIST] ✓ Backed up {size_kb:.2f} KB to cloud")
            else:
                print(f"[DB-PERSIST] ✗ Backup failed")
            
            return result
            
        except Exception as e:
            print(f"[DB-PERSIST] ✗ Backup error: {e}")
            return False
    
    def auto_backup_loop(self, interval_seconds: int = 300):
        """
        Run periodic backups in background.
        
        Args:
            interval_seconds: Time between backups (default 5 minutes)
        """
        import threading
        
        def backup_worker():
            while True:
                time.sleep(interval_seconds)
                self.backup_to_cloud()
        
        thread = threading.Thread(target=backup_worker, daemon=True)
        thread.start()
        print(f"[DB-PERSIST] Auto-backup started (every {interval_seconds}s)")
    
    def backup_on_shutdown(self):
        """Register shutdown handler to backup on exit."""
        import atexit
        atexit.register(lambda: self.backup_to_cloud(force=True))
        print("[DB-PERSIST] Shutdown backup registered")


# Global instance
_persistence = None

def get_db_persistence(db_path: str = "users.db") -> DatabasePersistenceService:
    """Get singleton database persistence service."""
    global _persistence
    if _persistence is None:
        _persistence = DatabasePersistenceService(db_path)
    return _persistence


def init_database_persistence(enable_auto_backup: bool = True):
    """
    Initialize database persistence on app startup.
    Call this BEFORE any database operations.
    
    Args:
        enable_auto_backup: Start periodic backup thread
    """
    service = get_db_persistence()
    
    # Restore from cloud if available
    service.restore_from_cloud()
    
    # Register shutdown backup
    service.backup_on_shutdown()
    
    # Start auto-backup
    if enable_auto_backup:
        service.auto_backup_loop(interval_seconds=300)  # 5 minutes
    
    return service
