import os
import io
import json
import importlib

def test_court_clerk_flow(tmp_path, monkeypatch):
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
    (tmp_path / 'uploads' / 'vault' / 'u1' / 'complaint.txt').write_text('claim', encoding='utf-8')

    # GET form requires auth
    r0 = client.get('/court_clerk')
    assert r0.status_code == 401

    r1 = client.get('/court_clerk?user_token=' + token_plain)
    assert r1.status_code == 200

    # Submit record
    data = {
        'user_token': token_plain,
        'court_name': 'County Court',
        'case_number': '2025-CV-001',
        'filing_type': 'Complaint',
        'submission_method': 'in_person',
        'status': 'submitted',
        'filename': 'complaint.txt'
    }
    r2 = client.post('/court_clerk', data=data, follow_redirects=True)
    assert r2.status_code == 200
    certs = list((tmp_path / 'uploads' / 'vault' / 'u1').glob('courtclerk_*.json'))
    assert len(certs) >= 1

