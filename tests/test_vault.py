import os
import io
import json
import importlib


def test_vault_auth_and_upload(tmp_path, monkeypatch):
    # Use open mode to avoid CSRF on POST
    monkeypatch.setenv('SECURITY_MODE', 'open')

    # Prepare users.json
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'

    # Point CWD to tmp to isolate writes
    monkeypatch.chdir(tmp_path)

    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    token_plain = 'u1token'
    user_entry = [{
        'id': 'u1',
        'name': 'User One',
        'hash': sempt._hash_token(token_plain),  # internal helper for tests
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')

    # 401 without token
    r1 = client.get('/vault')
    assert r1.status_code == 401

    # 200 with token
    r2 = client.get('/vault?user_token=' + token_plain)
    assert r2.status_code == 200
    assert b'Document Vault' in r2.data

    # Upload a small file
    data = {
        'user_token': token_plain,
        'file': (io.BytesIO(b'hello'), 'note.txt')
    }
    r3 = client.post('/vault/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert r3.status_code == 200
    # The file should exist under uploads/vault/u1/note.txt
    dest = tmp_path / 'uploads' / 'vault' / 'u1' / 'note.txt'
    assert dest.exists()
    assert dest.read_text(encoding='utf-8') == 'hello'

