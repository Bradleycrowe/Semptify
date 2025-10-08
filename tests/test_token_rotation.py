import os, importlib, json, re, tempfile

def setup_enforced(tmpdir):
    os.environ['SECURITY_MODE'] = 'enforced'
    os.environ['ADMIN_TOKEN'] = 'rotsecret'
    security_dir = os.path.join(tmpdir, 'security')
    os.makedirs(security_dir, exist_ok=True)
    # Create tokens file with one entry
    token_hash = 'sha256:' + __import__('hashlib').sha256(b'rotsecret').hexdigest()
    with open(os.path.join(security_dir, 'admin_tokens.json'), 'w') as f:
        json.dump([{ 'id': 'primary', 'hash': token_hash, 'enabled': True }], f)
    # Point app to this custom security path by chdir
    os.chdir(tmpdir)
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    return sempt

def extract_csrf(html: str):
    m = re.search(r'name="csrf_token" value="([0-9a-f]+)"', html)
    assert m, 'csrf token missing'
    return m.group(1)

def test_token_rotation_flow(tmp_path):
    sempt = setup_enforced(str(tmp_path))
    client = sempt.app.test_client()
    admin_page = client.get('/admin?token=rotsecret')
    csrf = extract_csrf(admin_page.data.decode())
    resp = client.post('/rotate_token', data={
        'token': 'rotsecret',
        'csrf_token': csrf,
        'target_id': 'primary',
        'new_value': 'newrotsecret'
    }, follow_redirects=False)
    assert resp.status_code in (301,302)
    # Ensure metrics updated
    metrics = client.get('/metrics')
    assert b'token_rotations_total' in metrics.data
