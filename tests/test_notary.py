import os
import io
import json
import importlib

def test_notary_upload_and_attest_existing(tmp_path, monkeypatch):
    # Open mode to bypass CSRF
    monkeypatch.setenv('SECURITY_MODE', 'open')

    # Prepare users.json
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'

    # Point CWD to tmp
    monkeypatch.chdir(tmp_path)

    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    token_plain = 'u1token'
    user_entry = [{
        'id': 'u1', 'name': 'User One', 'hash': sempt._hash_token(token_plain), 'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')

    # GET notary requires auth
    r0 = client.get('/notary')
    assert r0.status_code == 401

    r1 = client.get('/notary?user_token=' + token_plain)
    assert r1.status_code == 200
    assert b'Virtual Notary' in r1.data

    # Upload via notary
    data = {
        'user_token': token_plain,
        'file': (io.BytesIO(b'hello notarized'), 'noted.txt')
    }
    r2 = client.post('/notary/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert r2.status_code == 200
    # File exists
    dest = tmp_path / 'uploads' / 'vault' / 'u1' / 'noted.txt'
    assert dest.exists()
    # Certificate exists (one created recently)
    certs = list((tmp_path / 'uploads' / 'vault' / 'u1').glob('notary_*.json'))
    assert len(certs) >= 1

    # Attest existing
    r3 = client.post('/notary/attest_existing', data={ 'user_token': token_plain, 'filename': 'noted.txt' }, follow_redirects=True)
    assert r3.status_code == 200
    certs2 = list((tmp_path / 'uploads' / 'vault' / 'u1').glob('notary_*.json'))
    assert len(certs2) >= 2

