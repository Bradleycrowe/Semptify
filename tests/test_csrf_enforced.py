import os, importlib, re

def setup_enforced():
    os.environ['SECURITY_MODE'] = 'enforced'
    os.environ['ADMIN_TOKEN'] = 'csrfsecret'
    import Semptify as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    return sempt

def extract_csrf(html: str):
    m = re.search(r'name="csrf_token" value="([0-9a-f]+)"', html)
    assert m, 'csrf token not found in admin page html'
    return m.group(1)

def test_missing_csrf_rejected():
    sempt = setup_enforced()
    client = sempt.app.test_client()
    # Prime session & get page
    client.get('/admin?token=csrfsecret')
    # Attempt POST without csrf
    resp = client.post('/release_now', data={'token': 'csrfsecret', 'confirm_release': 'yes'})
    assert resp.status_code == 400

def test_valid_csrf_allows_release_tag(monkeypatch):
    sempt = setup_enforced()
    client = sempt.app.test_client()
    page = client.get('/admin?token=csrfsecret')
    csrf = extract_csrf(page.data.decode())

    # Monkeypatch GitHub API calls used in release_now
    class DummyResp:
        def __init__(self, status_code, json_data=None, text=''):
            self.status_code = status_code
            self._json = json_data or {}
            self.text = text
        def json(self):
            return self._json
    def fake_get(url, headers=None):
        return DummyResp(200, {'object': {'sha': 'abc123'}})
    def fake_post(url, headers=None, json=None):
        return DummyResp(201, {})
    monkeypatch.setattr('requests.get', fake_get)
    monkeypatch.setattr('requests.post', fake_post)

    resp = client.post('/release_now', data={
        'token': 'csrfsecret',
        'csrf_token': csrf,
        'confirm_release': 'yes'
    }, follow_redirects=False)
    # Should redirect to github releases (302)
    assert resp.status_code in (301,302)

