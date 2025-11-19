"""
R2 to User Storage Migration Tool
Migrates existing user files from R2 to their Google Drive or Dropbox
"""
import os
import boto3
from typing import Dict, List
from security import validate_user_token

class R2Migrator:
    def __init__(self):
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket = os.getenv('R2_BUCKET_NAME')
        
        if not all([self.account_id, self.access_key, self.secret_key, self.bucket]):
            raise ValueError("R2 credentials not configured")
        
        endpoint_url = f'https://{self.account_id}.r2.cloudflarestorage.com'
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='auto'
        )
    
    def list_user_files(self, user_token: str) -> List[str]:
        '''List all files for a user in R2'''
        # R2 structure: .semptify/<user_token_hash>/filename
        token_hash = validate_user_token(user_token)
        if not token_hash:
            return []
        
        prefix = f'.semptify/{token_hash}/'
        response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        
        if 'Contents' not in response:
            return []
        
        return [obj['Key'] for obj in response['Contents']]
    
    def migrate_user_to_drive(self, user_token: str, drive_client) -> Dict:
        '''Migrate user's R2 files to their Google Drive'''
        files = self.list_user_files(user_token)
        migrated = []
        errors = []
        
        for key in files:
            try:
                # Download from R2
                response = self.s3.get_object(Bucket=self.bucket, Key=key)
                content = response['Body'].read()
                
                # Extract filename
                filename = key.split('/')[-1]
                
                # Upload to Drive
                drive_client.upload(filename, content)
                migrated.append(filename)
                
            except Exception as e:
                errors.append({'file': key, 'error': str(e)})
        
        return {
            'migrated': migrated,
            'errors': errors,
            'total': len(files),
            'success': len(migrated)
        }
    
    def migrate_user_to_dropbox(self, user_token: str, dropbox_client) -> Dict:
        '''Migrate user's R2 files to their Dropbox'''
        files = self.list_user_files(user_token)
        migrated = []
        errors = []
        
        for key in files:
            try:
                # Download from R2
                response = self.s3.get_object(Bucket=self.bucket, Key=key)
                content = response['Body'].read()
                
                # Extract filename
                filename = key.split('/')[-1]
                
                # Upload to Dropbox
                dropbox_client.upload(filename, content)
                migrated.append(filename)
                
            except Exception as e:
                errors.append({'file': key, 'error': str(e)})
        
        return {
            'migrated': migrated,
            'errors': errors,
            'total': len(files),
            'success': len(migrated)
        }
    
    def get_migration_stats(self) -> Dict:
        '''Get stats on how many users need migration'''
        # List all .semptify/* folders in R2
        response = self.s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix='.semptify/',
            Delimiter='/'
        )
        
        users_with_data = 0
        if 'CommonPrefixes' in response:
            users_with_data = len(response['CommonPrefixes'])
        
        return {
            'users_with_r2_data': users_with_data,
            'bucket': self.bucket
        }
