import importlib
from bs4 import BeautifulSoup


def test_copilot_page_and_api_open_mode(monkeypatch):
    # Open mode disables CSRF enforcement for simplicity in tests
    monkeypatch.setenv('SECURITY_MODE', 'open')

    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()

    # Page loads
    r = client.get('/copilot')
    assert r.status_code == 200
    assert b'Semptify Copilot' in r.data

    # API requires prompt
    r2 = client.post('/api/copilot', json={})
    assert r2.status_code == 400
    assert r2.is_json
    assert r2.get_json().get('error') == 'missing_prompt'