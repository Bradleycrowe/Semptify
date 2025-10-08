import os, importlib, json

def setup_enforced():
    os.environ['SECURITY_MODE'] = 'enforced'
    os.environ['ADMIN_TOKEN'] = 'statustoken'
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    return sempt

def test_admin_status_json():
    sempt = setup_enforced()
    client = sempt.app.test_client()
    # unauthorized first
    r1 = client.get('/admin/status')
    assert r1.status_code == 401
    # authorized
    r2 = client.get('/admin/status?token=statustoken')
    assert r2.status_code == 200
    data = r2.get_json()
    assert 'security_mode' in data and data['security_mode'] == 'enforced'
    assert 'metrics' in data and isinstance(data['metrics'], dict)
    assert 'tokens' in data
