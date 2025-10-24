import os
import io
import json
import importlib

def test_certified_post_flow(tmp_path, monkeypatch):
    monkeypatch.setenv('SECURITY_MODE', 'open')
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    monkeypatch.chdir(tmp_path)

    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    token_plain = 'u1token'
    users_path.write_text(json.dumps([{ 'id':'u1','name':'User One','hash': sempt._hash_token(token_plain),'enabled':True }]), encoding='utf-8')

    # Create a vault file
    os.makedirs(tmp_path / 'uploads' / 'vault' / 'u1', exist_ok=True)
    (tmp_path / 'uploads' / 'vault' / 'u1' / 'doc.txt').write_text('hello', encoding='utf-8')

    # GET form requires auth
    r0 = client.get('/certified_post')
    assert r0.status_code == 401

    r1 = client.get('/certified_post?user_token=' + token_plain)
    assert r1.status_code == 200

    # Submit record
    data = {
        'user_token': token_plain,
        'service_type': 'postal_certified',
        'destination': 'Landlord, 123 Main St',
        'tracking_number': '94001118992239482374',
        'filename': 'doc.txt'
    }
    r2 = client.post('/certified_post', data=data, follow_redirects=True)
    assert r2.status_code == 200
    certs = list((tmp_path / 'uploads' / 'vault' / 'u1').glob('certpost_*.json'))
    assert len(certs) >= 1

