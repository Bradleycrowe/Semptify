import importlib
import re

import pytest

def test_full_register_verify_dashboard(monkeypatch):
    """End-to-end: register -> verify -> dashboard using known verification code.
    We monkeypatch generate_verification_code to produce a deterministic code.
    SECURITY_MODE=open bypasses CSRF for test simplicity.
    """
    monkeypatch.setenv('SECURITY_MODE', 'open')

    # Force predictable code
    import user_database
    monkeypatch.setattr(user_database, 'generate_verification_code', lambda: '123456')

    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    unique_email = f'test.{sempt.secrets.token_hex(4)}@example.com'

    # Register
    r_post = client.post('/register', data={
        'first_name': 'Flow',
        'last_name': 'Tester',
        'email': unique_email,
        'phone': '555-0000',
        'address': '1 Test Way',
        'city': 'Testville',
        'county': 'Test',
        'state': 'MN',
        'zip': '55401',
        'verify_method': 'email'
    }, follow_redirects=False)
    assert r_post.status_code == 302
    assert '/verify' in r_post.location

    # Extract user_id from redirect query string
    match = re.search(r'user_id=([^&]+)', r_post.location)
    assert match, 'user_id not found in redirect location'
    user_id = match.group(1)

    # Verify with known code
    r_verify = client.post('/verify', data={
        'user_id': user_id,
        'full_code': '123456'
    }, follow_redirects=True)
    assert r_verify.status_code == 200
    assert b'dashboard' in r_verify.data.lower() or b'Document' in r_verify.data  # heuristic

    # Access dashboard directly
    r_dash = client.get('/dashboard')
    assert r_dash.status_code == 200


def test_login_flow_issue_code(monkeypatch):
    """Register + verify user, then login again to ensure code issuance for existing user works."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    import user_database
    # First registration uses code A, second login should issue code B
    codes = ['111111', '222222']
    def code_gen():
        return codes.pop(0)
    monkeypatch.setattr(user_database, 'generate_verification_code', code_gen)

    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    email = f'login.{sempt.secrets.token_hex(4)}@example.com'

    # Register
    r_post = client.post('/register', data={
        'first_name': 'Login',
        'last_name': 'User',
        'email': email,
        'phone': '555-0001',
        'address': '2 Test Way',
        'city': 'Testville',
        'county': 'Test',
        'state': 'MN',
        'zip': '55402',
        'verify_method': 'email'
    }, follow_redirects=False)
    assert r_post.status_code == 302
    user_id = re.search(r'user_id=([^&]+)', r_post.location).group(1)

    # Verify first code
    r_verify = client.post('/verify', data={'user_id': user_id, 'full_code': '111111'}, follow_redirects=True)
    assert r_verify.status_code == 200

    # Logout by clearing session (simulate new session)
    with client.session_transaction() as sess:
        sess.clear()

    # Initiate login, which should create a pending entry with second code
    r_login = client.post('/login', data={'email': email}, follow_redirects=False)
    assert r_login.status_code == 302 and '/verify' in r_login.location
    new_user_id = re.search(r'user_id=([^&]+)', r_login.location).group(1)
    assert new_user_id  # same or new user_id depending on implementation (create_login_pending_entry uses existing user_id)

    # Verify second code
    r_verify2 = client.post('/verify', data={'user_id': new_user_id, 'full_code': '222222'}, follow_redirects=True)
    assert r_verify2.status_code == 200

    # Dashboard should be accessible again
    r_dash = client.get('/dashboard')
    assert r_dash.status_code == 200
