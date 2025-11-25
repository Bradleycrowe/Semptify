import sys
sys.path.insert(0, '.')

try:
    from core.storage import (
        UnifiedStorageBackend,
        create_google_drive_backend,
        create_dropbox_backend,
        create_local_backend,
        StorageException
    )
    print('✅ core.storage imports successfully')
    
    from storage_setup_routes import storage_setup_bp
    print('✅ storage_setup_routes imports successfully')
    
    # Test token generation
    token = UnifiedStorageBackend.generate_token()
    print(f'✅ Generated token: {token[:4]}...{token[-4:]}')
    
    # Test token hashing
    token_hash = UnifiedStorageBackend.hash_token(token)
    print(f'✅ Hashed token: {token_hash[:16]}...')
    
    # Test validation
    from core.storage import UnifiedStorageBackend
    print('✅ UnifiedStorageBackend class accessible')
    
    print('\n🎉 ALL IMPORTS SUCCESSFUL!')
    
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
