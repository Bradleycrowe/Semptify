import os
import json
import importlib

def test_ron_flow_simulated(tmp_path, monkeypatch):
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.setenv('RON_PROVIDER', 'bluenotary')
    monkeypatch.setenv('RON_WEBHOOK_SECRET', 'secret123')
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

    # Seed a source file
    udir = tmp_path / 'uploads' / 'vault' / 'u1'
    os.makedirs(udir, exist_ok=True)
    (udir / 'doc.txt').write_text('hello', encoding='utf-8')

    # Start RON
    r1 = client.post('/legal_notary/start', data={ 'user_token': token_plain, 'source_file': 'doc.txt' }, follow_redirects=False)
    assert r1.status_code in (302, 303)
    # Extract session id from redirect URL
    loc = r1.headers['Location']
    assert '/legal_notary/return' in loc
    session_id = loc.split('session_id=')[1].split('&')[0]

    # Return completes
    r2 = client.get(f'/legal_notary/return?session_id={session_id}&user_token={token_plain}', follow_redirects=False)
    assert r2.status_code in (302, 303)

    # Webhook update
    payload = { 'user_id': 'u1', 'session_id': session_id, 'status': 'completed', 'evidence_links': ['https://example.com/proof.pdf'] }
    r3 = client.post('/webhooks/ron', json=payload, headers={ 'X-RON-Signature': 'secret123' })
    assert r3.status_code == 200

    # Verify certificate exists and includes provider and status
    cert_path = udir / f'ron_{session_id}.json'
    assert cert_path.exists()
    data = json.loads(cert_path.read_text(encoding='utf-8'))
    assert data.get('type') == 'ron_session'
    assert data.get('provider') == 'bluenotary'
    assert data.get('status') == 'completed'
    assert data.get('evidence_links')

