import os
import importlib

def test_admin_enforced_requires_token():
    os.environ['SECURITY_MODE'] = 'enforced'
    os.environ['ADMIN_TOKEN'] = 'secret123'
    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    # Missing token -> 401
    resp1 = client.get('/admin')
    assert resp1.status_code == 401
    # With token -> 200
    resp2 = client.get('/admin?token=secret123')
    assert resp2.status_code == 200
    assert b'SECURITY MODE: ENFORCED' in resp2.data
