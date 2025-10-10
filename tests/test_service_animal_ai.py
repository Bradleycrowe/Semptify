import importlib
from bs4 import BeautifulSoup


def test_service_animal_form_shows_ai_helper_when_configured(monkeypatch):
    """Test that AI helper is shown on service animal form when AI_PROVIDER is configured"""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.setenv('AI_PROVIDER', 'ollama')
    monkeypatch.setenv('OLLAMA_HOST', 'http://localhost:11434')
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    r = client.get('/resources/service_animal')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    
    # Check that AI helper section is present
    assert 'AI Help' in html
    assert 'Provider: ollama' in html
    assert 'ai-generate-btn' in html
    assert 'Generate Explanation with AI' in html
    

def test_service_animal_form_without_ai(monkeypatch):
    """Test that service animal form shows tip when AI is not configured"""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.setenv('AI_PROVIDER', 'none')
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    r = client.get('/resources/service_animal')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    
    # Check that AI helper section is NOT present, but a tip is shown
    assert 'AI Help' not in html
    assert 'Configure AI_PROVIDER' in html
    assert 'ai-generate-btn' not in html


def test_service_animal_form_basic_elements(monkeypatch):
    """Test that basic form elements are present regardless of AI configuration"""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    r = client.get('/resources/service_animal')
    assert r.status_code == 200
    html = r.data.decode('utf-8')
    
    # Check that basic form elements exist
    assert 'tenant_name' in html
    assert 'landlord_name' in html
    assert 'property_address' in html
    assert 'animal_description' in html
    assert 'need_summary' in html
    assert 'sig_name' in html
    assert 'sig_consented' in html
    assert 'Preview' in html
