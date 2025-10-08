import os, json, importlib, time

# We'll simulate enforced mode with a break-glass token

def setup_tokens(tmpdir):
    os.environ['SECURITY_MODE'] = 'enforced'
    os.environ['ADMIN_RATE_WINDOW'] = '2'
    os.environ['ADMIN_RATE_MAX'] = '3'
    # legacy token for fallback clarity
    os.environ['ADMIN_TOKEN'] = 'legacytok'
    sec_dir = os.path.join(tmpdir, 'security')
    os.makedirs(sec_dir, exist_ok=True)
    # create break-glass file
    open(os.path.join(sec_dir, 'breakglass.flag'), 'w').close()
    # create tokens file with breakglass token
    import hashlib
    bg_hash = 'sha256:' + hashlib.sha256(b'glass123').hexdigest()
    with open(os.path.join(sec_dir, 'admin_tokens.json'), 'w') as f:
        json.dump([{ 'id': 'bg', 'hash': bg_hash, 'enabled': True, 'breakglass': True }], f)
    os.chdir(tmpdir)
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    return sempt

def test_breakglass_one_shot_and_rate_limit(tmp_path):
    sempt = setup_tokens(str(tmp_path))
    client = sempt.app.test_client()
    # Use breakglass token first time (flag exists)
    r1 = client.get('/admin?token=glass123')
    assert r1.status_code == 200
    assert b'ENFORCED' in r1.data
    # Second time should still work (now normal multi-token since token is in file) but breakglass flag consumed
    r2 = client.get('/admin?token=glass123')
    assert r2.status_code == 200
    # Hit same admin path to trigger rate limiting (limit=3/window)
    client.get('/admin?token=glass123')
    client.get('/admin?token=glass123')
    rlim = client.get('/admin?token=glass123')
    # After exceeding, we expect 401 from _require_admin_or_401 returning False due to rate limit (current impl)
    assert rlim.status_code in (401, 429)
    metrics = client.get('/metrics').data.decode()
    assert 'rate_limited_total' in metrics
    assert 'breakglass_used_total' in metrics
