import importlib

def test_register_flow_open_mode(monkeypatch):
    monkeypatch.setenv('SECURITY_MODE', 'open')
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    r_get = client.get('/register')
    assert r_get.status_code == 200

    # In open mode, CSRF is bypassed, so we can post without token in tests
    r_post = client.post('/register', data={'name': 'Test User'})
    assert r_post.status_code == 200
    assert b"one-time token" in r_post.data
