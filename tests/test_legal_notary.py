import os
import io
import json
import importlib

def test_legal_notary_record(tmp_path, monkeypatch):
    monkeypatch.setenv('SECURITY_MODE', 'open')
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    monkeypatch.chdir(tmp_path)

    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    token_plain = 'u1token'
    users_path.write_text(json.dumps([{ 'id':'u1','name':'User One','hash': sempt._hash_token(token_plain),'enabled':True }]), encoding='utf-8')

    # Seed a source file
    udir = tmp_path / 'uploads' / 'vault' / 'u1'
    os.makedirs(udir, exist_ok=True)
    (udir / 'doc.txt').write_text('hello', encoding='utf-8')

    # GET form requires auth
    r0 = client.get('/legal_notary')
    assert r0.status_code == 401

    # GET with token should render
    r1 = client.get('/legal_notary?user_token=' + token_plain)
    assert r1.status_code == 200
    assert b'Legal Notary' in r1.data

    # POST a record with upload
    data = {
        'user_token': token_plain,
        'notary_name': 'Jane Notary',
        'commission_number': 'ABC123',
        'state': 'CA',
        'jurisdiction': 'SF',
        'notarization_date': '2024-01-01',
        'method': 'ron',
        'provider': 'Notarize',
        'source_file': 'doc.txt',
        'notes': 'test case'
    }
    file_data = (io.BytesIO(b'PDFDATA'), 'scan.pdf')
    r2 = client.post('/legal_notary', data={**data, 'notarized_file': file_data}, content_type='multipart/form-data', follow_redirects=False)
    assert r2.status_code in (302, 303)

    # Verify certificate exists
    certs = list(udir.glob('legalnotary_*.json'))
    assert len(certs) == 1
    payload = json.loads(certs[0].read_text(encoding='utf-8'))
    assert payload.get('type') == 'legal_notary_record'
    assert payload.get('state') == 'CA'
    assert payload.get('notary_name') == 'Jane Notary'
