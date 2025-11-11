import importlib

def test_register_flow_open_mode(monkeypatch):
    monkeypatch.setenv('SECURITY_MODE', 'open')
    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    r_get = client.get('/register')
    assert r_get.status_code == 200

    # In open mode, CSRF is bypassed, so we can post without token in tests
    # Test with complete registration data
    r_post = client.post('/register', data={
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'test.{sempt.secrets.token_hex(4)}@example.com',  # Unique email
        'phone': '555-0123',
        'address': '123 Test St',
        'city': 'Test City',
        'county': 'Test County',
        'state': 'CA',
        'zip': '12345',
        'verify_method': 'email'
    }, follow_redirects=False)
    
    # Should redirect to /verify after successful registration
    assert r_post.status_code == 302
    assert '/verify' in r_post.location

