"""
Storage Adapter for Semptify
Supports both local filesystem (ephemeral) and Cloudflare R2 (persistent)
"""
import os
import json
from pathlib import Path

# Try to import boto3 for R2 support
try:
    import boto3
    from botocore.client import Config
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


class StorageAdapter:
    """Abstract storage interface that works with local files or R2"""
    
    def __init__(self):
        self.use_r2 = self._should_use_r2()
        
        if self.use_r2:
            if not HAS_BOTO3:
                print("WARNING: R2 configured but boto3 not installed. Falling back to local storage.")
                self.use_r2 = False
            else:
                self._init_r2()
        
        print(f"Storage mode: {'R2' if self.use_r2 else 'Local (ephemeral)'}")
    
    def _should_use_r2(self):
        """Check if R2 is configured"""
        required = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME']
        return all(os.getenv(var) for var in required)
    
    def _init_r2(self):
        """Initialize R2 client"""
        account_id = os.getenv('R2_ACCOUNT_ID')
        endpoint = f'https://{account_id}.r2.cloudflarestorage.com'
        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            config=Config(signature_version='s3v4')
        )
        self.bucket = os.getenv('R2_BUCKET_NAME')
    
    def save_file(self, relative_path, content, metadata=None):
        """
        Save file with optional metadata
        relative_path: e.g., 'vault/user123/document.pdf'
        content: bytes or string
        metadata: dict of metadata to attach
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        if self.use_r2:
            return self._save_to_r2(relative_path, content, metadata)
        else:
            return self._save_to_local(relative_path, content, metadata)
    
    def _save_to_r2(self, relative_path, content, metadata):
        """Save to Cloudflare R2"""
        try:
            extra_args = {}
            if metadata:
                # R2 metadata keys must be strings
                extra_args['Metadata'] = {k: str(v) for k, v in metadata.items()}
            
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=relative_path,
                Body=content,
                **extra_args
            )
            return True
        except Exception as e:  # noqa: BLE001
            print(f"R2 save error for {relative_path}: {e}")
            return False
    
    def _save_to_local(self, relative_path, content, metadata):
        """Save to local filesystem"""
        try:
            full_path = Path('uploads') / relative_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(full_path, 'wb') as f:
                f.write(content)
            
            # Write metadata if provided
            if metadata:
                meta_path = full_path.with_suffix(full_path.suffix + '.meta.json')
                with open(meta_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
            
            return True
        except Exception as e:  # noqa: BLE001
            print(f"Local save error for {relative_path}: {e}")
            return False
    
    def read_file(self, relative_path):
        """Read file content (returns bytes)"""
        if self.use_r2:
            return self._read_from_r2(relative_path)
        else:
            return self._read_from_local(relative_path)
    
    def _read_from_r2(self, relative_path):
        """Read from R2"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=relative_path)
            return response['Body'].read()
        except Exception as e:  # noqa: BLE001
            print(f"R2 read error for {relative_path}: {e}")
            return None
    
    def _read_from_local(self, relative_path):
        """Read from local filesystem"""
        try:
            full_path = Path('uploads') / relative_path
            with open(full_path, 'rb') as f:
                return f.read()
        except Exception as e:  # noqa: BLE001
            print(f"Local read error for {relative_path}: {e}")
            return None
    
    def file_exists(self, relative_path):
        """Check if file exists"""
        if self.use_r2:
            try:
                self.s3_client.head_object(Bucket=self.bucket, Key=relative_path)
                return True
            except Exception:  # noqa: BLE001
                return False
        else:
            return (Path('uploads') / relative_path).exists()
    
    def list_files(self, prefix=''):
        """List files with optional prefix"""
        if self.use_r2:
            return self._list_r2_files(prefix)
        else:
            return self._list_local_files(prefix)
    
    def _list_r2_files(self, prefix):
        """List files in R2"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:  # noqa: BLE001
            print(f"R2 list error: {e}")
            return []
    
    def _list_local_files(self, prefix):
        """List local files"""
        try:
            base = Path('uploads') / prefix
            if not base.exists():
                return []
            
            files = []
            for path in base.rglob('*'):
                if path.is_file() and not path.name.endswith('.meta.json'):
                    rel = path.relative_to('uploads')
                    files.append(str(rel).replace('\\', '/'))
            return files
        except Exception as e:  # noqa: BLE001
            print(f"Local list error: {e}")
            return []
    
    def delete_file(self, relative_path):
        """Delete a file"""
        if self.use_r2:
            try:
                self.s3_client.delete_object(Bucket=self.bucket, Key=relative_path)
                return True
            except Exception as e:  # noqa: BLE001
                print(f"R2 delete error: {e}")
                return False
        else:
            try:
                full_path = Path('uploads') / relative_path
                if full_path.exists():
                    full_path.unlink()
                # Also delete metadata if exists
                meta_path = full_path.with_suffix(full_path.suffix + '.meta.json')
                if meta_path.exists():
                    meta_path.unlink()
                return True
            except Exception as e:  # noqa: BLE001
                print(f"Local delete error: {e}")
                return False


# Global instance
storage = StorageAdapter()
