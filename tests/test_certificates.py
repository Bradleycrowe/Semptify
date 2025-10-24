import os
import json
import importlib

def test_certificates_list_and_view_and_export(tmp_path, monkeypatch):
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

    # Seed a couple of certificates and a related file
    udir = tmp_path / 'uploads' / 'vault' / 'u1'
    os.makedirs(udir, exist_ok=True)
    (udir / 'doc.txt').write_text('hello', encoding='utf-8')
    (udir / 'notary_1234_aaaa.json').write_text(json.dumps({ 'type':'notary_attestation','filename':'doc.txt' }), encoding='utf-8')
    (udir / 'certpost_1234_bbbb.json').write_text(json.dumps({ 'type':'certified_post','related_file':'doc.txt','tracking_number':'1' }), encoding='utf-8')

    # List
    r1 = client.get('/vault/certificates?user_token=' + token_plain)
    assert r1.status_code == 200
    body = r1.data.decode('utf-8')
    assert 'notary_1234_aaaa.json' in body
    assert 'certpost_1234_bbbb.json' in body

    # View a certificate
    r2 = client.get('/vault/certificates/notary_1234_aaaa.json?user_token=' + token_plain)
    assert r2.status_code == 200
    assert 'notary_1234_aaaa.json' in r2.data.decode('utf-8')

    # Export zip
    r3 = client.post('/vault/export_bundle', data={ 'user_token': token_plain }, follow_redirects=False)
    assert r3.status_code == 200
    assert r3.headers['Content-Type'].startswith('application/zip')

