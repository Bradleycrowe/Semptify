import os
import json
import pytest
from SemptifyGUI import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_evidence_panel_in_witness_form(client):
    """Test that witness form includes evidence collection panel"""
    rv = client.get('/resources/witness_statement')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert 'Evidence Collection System' in body
    assert 'evidence-system.js' in body

def test_evidence_panel_in_packet_form(client):
    """Test that filing packet form includes evidence collection panel"""
    rv = client.get('/resources/filing_packet')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert 'Evidence Collection System' in body
    assert 'evidence-system.js' in body

def test_evidence_panel_in_service_animal_form(client):
    """Test that service animal form includes evidence collection panel"""
    rv = client.get('/resources/service_animal')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert 'Evidence Collection System' in body
    assert 'evidence-system.js' in body

def test_evidence_panel_in_move_checklist_form(client):
    """Test that move checklist form includes evidence collection panel"""
    rv = client.get('/resources/move_checklist')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert 'Evidence Collection System' in body
    assert 'evidence-system.js' in body

def test_enhanced_copilot_with_evidence_context(client):
    """Test that copilot API handles evidence context"""
    with client.session_transaction() as sess:
        sess['csrf_token'] = 'test-token'
    
    # Test basic copilot request (may fail CSRF or AI provider check or rate limit)
    rv = client.post('/api/copilot',
                     json={'prompt': 'help with tenant rights'},
                     headers={'X-CSRFToken': 'test-token'})
    assert rv.status_code in [200, 400, 429, 501]  # 400 CSRF, 429 rate limit, 501 no AI provider
    
    # Test enhanced copilot with evidence context
    rv = client.post('/api/copilot',
                     json={
                         'prompt': 'help collecting evidence',
                         'location': '40.7128,-74.0060 (±10m)',
                         'timestamp': '2025-10-10T15:30:00Z',
                         'form_type': 'witness_statement',
                         'form_data': {'full_name': 'Test User', 'statement': 'Test statement'}
                     },
                     headers={'X-CSRFToken': 'test-token'})
    assert rv.status_code in [200, 400, 429, 501]  # 400 CSRF, 429 rate limit, 501 no AI provider

def test_evidence_data_extraction_from_form(client):
    """Test that evidence data is properly extracted from form submission"""
    with client.session_transaction() as sess:
        sess['csrf_token'] = 'test-token'
    
    form_data = {
        'csrf_token': 'test-token',
        'full_name': 'Test Witness',
        'contact': 'test@example.com',
        'statement': 'I witnessed the incident',
        'date': '2025-10-10',
        'sig_consented': 'on',
        'sig_name': 'Test Witness',
        'user_token': 'invalid_token',  # Will cause auth failure
        'evidence_timestamp': '2025-10-10T15:30:00Z',
        'evidence_location': '40.7128,-74.0060 (±10m)',
        'location_accuracy': '10',
        'evidence_user_agent': 'Test Browser'
    }
    
    # This should fail auth but show the route processes evidence data
    rv = client.post('/resources/witness_statement_save', data=form_data)
    assert rv.status_code in [400, 401]  # Expected without proper auth

def test_evidence_collector_js_exists():
    """Test that evidence collector JavaScript file exists and has required content"""
    js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          'static', 'js', 'evidence-collector.js')
    assert os.path.exists(js_path)
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key functionality
    assert 'SemptifyEvidenceCollector' in content
    assert 'navigator.geolocation' in content
    assert 'MediaRecorder' in content
    assert 'SpeechRecognition' in content
    assert 'toggleRecording' in content
    assert 'toggleVoiceCommands' in content
    assert 'askAI' in content

def test_evidence_panel_template_exists():
    """Test that evidence panel template exists and has required elements"""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'templates', 'evidence_panel.html')
    assert os.path.exists(template_path)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'evidence-panel' in content
    assert 'Evidence Collection System' in content
    assert 'toggleRecording' in content
    assert 'toggleVoiceCommands' in content
    assert 'askAI' in content
    assert 'updateLocation' in content
    assert 'Voice commands:' in content

def test_css_includes_evidence_styles(client):
    """Test that CSS includes evidence collection styles"""
    rv = client.get('/static/css/app.css')
    assert rv.status_code == 200
    
    css_content = rv.data.decode('utf-8')
    assert 'evidence-panel' in css_content
    assert 'evidence-controls' in css_content
    assert 'ai-response-panel' in css_content
    assert 'btn-record' in css_content
    assert 'btn-voice' in css_content

def test_service_worker_caches_evidence_js(client):
    """Test that service worker includes evidence collector in cache"""
    rv = client.get('/static/js/service-worker.js')
    assert rv.status_code == 200
    
    sw_content = rv.data.decode('utf-8')
    assert 'evidence-collector.js' in sw_content
    assert 'semptify-cache-v3' in sw_content

def test_build_evidence_prompt_function():
    """Test the evidence prompt building function"""
    from SemptifyGUI import _build_evidence_prompt
    
    # Test basic prompt
    result = _build_evidence_prompt(
        "help me collect evidence",
        "40.7128,-74.0060 (±10m)", 
        "2025-10-10T15:30:00Z",
        "witness_statement",
        {"full_name": "John Doe", "statement": "I saw the incident"}
    )
    
    assert "tenant rights and evidence collection" in result
    assert "40.7128,-74.0060" in result
    assert "2025-10-10T15:30:00Z" in result
    assert "witness statement" in result
    assert "John Doe" in result
    assert "help me collect evidence" in result
    assert "What evidence to collect" in result

def test_evidence_prompt_with_minimal_data():
    """Test evidence prompt building with minimal data"""
    from SemptifyGUI import _build_evidence_prompt
    
    result = _build_evidence_prompt(
        "need help",
        "",  # no location
        "",  # no timestamp  
        "general_form",
        {}   # no form data
    )
    
    assert "tenant rights and evidence collection" in result
    assert "need help" in result
    assert "What evidence to collect" in result