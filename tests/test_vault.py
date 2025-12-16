import os
import io
import json
import pytest


def test_vault_auth_and_upload(tmp_path, monkeypatch):
    """Test vault authentication and file upload."""
    # Use enforced mode
    monkeypatch.setenv('SECURITY_MODE', 'enforced')
    
    # Create security directory in tmp_path
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    
    # Change to tmp_path so security module finds it
    monkeypatch.chdir(tmp_path)
    
    # Import fresh - monkeypatch.chdir is auto-restored by pytest
    import security
    import Semptify as sempt
    
    # Create user with hashed token
    token_plain = 'u1token'
    hash_val = security._hash_token(token_plain)
    user_entry = [{
        'id': 'u1',
        'name': 'User One',
        'hash': hash_val,
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')
    
    # Test token validation directly
    result = security.validate_user_token(token_plain)
    assert result == 'u1', f"Expected 'u1', got {result}"
    
    # Test via Flask client
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    # 401 without token
    r1 = client.get('/vault')
    assert r1.status_code == 401
    
    # 200 with token
    r2 = client.get('/vault?user_token=' + token_plain)
    assert r2.status_code == 200
    assert b'Document Vault' in r2.data
    
    # Upload file
    data = {
        'user_token': token_plain,
        'file': (io.BytesIO(b'hello'), 'note.txt')
    }
    r3 = client.post('/vault/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert r3.status_code == 200
    
    # Verify file exists
    dest = tmp_path / 'uploads' / 'vault' / 'u1' / 'note.txt'
    assert dest.exists()
    assert dest.read_text(encoding='utf-8') == 'hello'
