"""
Multi-Tier Storage Architecture for Semptify
- R2 (Cloudflare): System & Admin only (persistent, distributed)
- OAuth Cloud: Dropbox & Google Drive for end users
- Local Storage: Manager, Advocate, Legal staff (fast access)
"""
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os
import json
from datetime import datetime

class StorageTier(Enum):
    """Storage tier classification"""
    R2_SYSTEM = "r2_system"  # Admin, system backups, audit logs
    OAUTH_USER = "oauth_user"  # End user documents (Dropbox, Google Drive)
    LOCAL_MANAGER = "local_manager"  # Manager documents (fast local)
    LOCAL_ADVOCATE = "local_advocate"  # Advocate case files (local)
    LOCAL_LEGAL = "local_legal"  # Legal team documents (local)

class CloudProvider(Enum):
    """OAuth cloud storage providers"""
    DROPBOX = "dropbox"
    GOOGLE_DRIVE = "google_drive"
    R2 = "r2"
    LOCAL = "local"

@dataclass
class StorageConfig:
    """Storage configuration per tier"""
    tier: StorageTier
    provider: CloudProvider
    base_path: str
    max_size_mb: int
    allowed_extensions: List[str]
    encryption_required: bool
    audit_logging: bool

class MultiTierStorage:
    """Multi-tier storage routing and management"""
    
    STORAGE_CONFIGS = {
        # R2 - System & Admin only (persistent, distributed)
        StorageTier.R2_SYSTEM: StorageConfig(
            tier=StorageTier.R2_SYSTEM,
            provider=CloudProvider.R2,
            base_path="r2://semptify-system",
            max_size_mb=500,
            allowed_extensions=[".pdf", ".json", ".zip", ".db", ".log"],
            encryption_required=True,
            audit_logging=True
        ),
        
        # OAuth - End users (Dropbox, Google Drive)
        StorageTier.OAUTH_USER: StorageConfig(
            tier=StorageTier.OAUTH_USER,
            provider=CloudProvider.DROPBOX,  # Default, user can choose
            base_path="oauth://user-documents",
            max_size_mb=100,
            allowed_extensions=[".pdf", ".jpg", ".png", ".docx", ".txt"],
            encryption_required=False,
            audit_logging=True
        ),
        
        # Local - Manager (fast access, local only)
        StorageTier.LOCAL_MANAGER: StorageConfig(
            tier=StorageTier.LOCAL_MANAGER,
            provider=CloudProvider.LOCAL,
            base_path="uploads/manager",
            max_size_mb=200,
            allowed_extensions=[".pdf", ".xlsx", ".docx", ".csv", ".json"],
            encryption_required=False,
            audit_logging=True
        ),
        
        # Local - Advocate (case files, local only)
        StorageTier.LOCAL_ADVOCATE: StorageConfig(
            tier=StorageTier.LOCAL_ADVOCATE,
            provider=CloudProvider.LOCAL,
            base_path="uploads/advocate",
            max_size_mb=150,
            allowed_extensions=[".pdf", ".jpg", ".png", ".docx", ".txt", ".json"],
            encryption_required=False,
            audit_logging=True
        ),
        
        # Local - Legal team (legal documents, local only)
        StorageTier.LOCAL_LEGAL: StorageConfig(
            tier=StorageTier.LOCAL_LEGAL,
            provider=CloudProvider.LOCAL,
            base_path="uploads/legal",
            max_size_mb=300,
            allowed_extensions=[".pdf", ".docx", ".txt", ".json"],
            encryption_required=True,
            audit_logging=True
        )
    }
    
    def __init__(self):
        self._ensure_directories()
        self._load_r2_config()
    
    def _ensure_directories(self):
        """Create local storage directories"""
        local_dirs = [
            "uploads/manager",
            "uploads/advocate",
            "uploads/legal",
            "uploads/oauth_cache",  # Temporary OAuth file cache
            "data/storage_audit"
        ]
        for dir_path in local_dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def _load_r2_config(self):
        """Load R2 configuration"""
        r2_config_path = "r2_config.json"
        if os.path.exists(r2_config_path):
            with open(r2_config_path, 'r') as f:
                self.r2_config = json.load(f)
        else:
            self.r2_config = {
                "account_id": os.getenv("R2_ACCOUNT_ID", ""),
                "access_key_id": os.getenv("R2_ACCESS_KEY_ID", ""),
                "secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY", ""),
                "bucket_name": os.getenv("R2_BUCKET_NAME", "semptify-system")
            }
    
    def route_storage(self, user_role: str) -> StorageConfig:
        """Route user to appropriate storage tier based on role"""
        role_mapping = {
            "admin": StorageTier.R2_SYSTEM,
            "system": StorageTier.R2_SYSTEM,
            "manager": StorageTier.LOCAL_MANAGER,
            "advocate": StorageTier.LOCAL_ADVOCATE,
            "legal": StorageTier.LOCAL_LEGAL,
            "user": StorageTier.OAUTH_USER,
            "tenant": StorageTier.OAUTH_USER
        }
        
        tier = role_mapping.get(user_role.lower(), StorageTier.OAUTH_USER)
        return self.STORAGE_CONFIGS[tier]
    
    def get_storage_path(self, user_role: str, filename: str) -> str:
        """Get full storage path for a file based on user role"""
        config = self.route_storage(user_role)
        
        if config.provider == CloudProvider.R2:
            return f"{config.base_path}/{filename}"
        elif config.provider in [CloudProvider.DROPBOX, CloudProvider.GOOGLE_DRIVE]:
            return f"{config.base_path}/{filename}"
        else:  # LOCAL
            return os.path.join(config.base_path, filename)
    
    def validate_upload(self, user_role: str, filename: str, size_mb: float) -> Dict[str, Any]:
        """Validate if upload is allowed for user role"""
        config = self.route_storage(user_role)
        
        # Check file extension
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in config.allowed_extensions:
            return {
                "allowed": False,
                "reason": f"File type {file_ext} not allowed. Allowed: {', '.join(config.allowed_extensions)}"
            }
        
        # Check file size
        if size_mb > config.max_size_mb:
            return {
                "allowed": False,
                "reason": f"File size {size_mb}MB exceeds limit of {config.max_size_mb}MB"
            }
        
        return {
            "allowed": True,
            "tier": config.tier.value,
            "provider": config.provider.value,
            "path": self.get_storage_path(user_role, filename),
            "encryption_required": config.encryption_required
        }
    
    def log_storage_event(self, event_type: str, user_role: str, filename: str, metadata: Dict = None):
        """Log storage events for audit"""
        audit_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_role": user_role,
            "filename": filename,
            "tier": self.route_storage(user_role).tier.value,
            "metadata": metadata or {}
        }
        
        # Write to audit log
        audit_path = "data/storage_audit/storage_events.jsonl"
        with open(audit_path, 'a') as f:
            f.write(json.dumps(audit_log) + '\n')

# Global instance
storage_router = MultiTierStorage()
