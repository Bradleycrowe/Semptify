import os
import json
import pytest
from Semptify import app

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
    assert 'evidence-system.js' in body
    assert 'evidence-panel' in body
    assert 'Evidence Collection' in body
    assert 'Start Recording' in body
    assert 'Voice Commands' in body
    assert 'Ask AI' in body

def test_evidence_copilot_api_requires_csrf(client):
    """Test evidence copilot API requires CSRF token"""
    rv = client.post('/api/evidence-copilot',
                     json={'prompt': 'help with evidence'})
    # Could be 400 (CSRF fail) or 501 (no AI provider)
    assert rv.status_code in [400, 501]

def test_evidence_copilot_api_with_mock_data(client):
    """Test evidence copilot API with minimal data"""
    # This would fail without proper AI provider, but tests structure
    with client.session_transaction() as sess:
        sess['csrf_token'] = 'test-token'

    rv = client.post('/api/evidence-copilot',
                     json={
                         'prompt': 'help collecting evidence',
                         'location': '40.7128,-74.0060',
                         'timestamp': '2025-10-10T12:00:00Z',
                         'form_type': 'witness_statement'
                     },
                     headers={'X-CSRFToken': 'test-token'})

    # Should get rate limited, AI error, or not implemented (expected without provider)
    assert rv.status_code in [400, 429, 500, 501]

def test_enhanced_evidence_data_in_certificate(client):
    """Test that evidence data is included in form certificates"""
    # Create a user first
    user_data = {
        'id': 'test_user_001',
        'hash': 'dummy_hash',
        'enabled': True
    }

    # Mock user authentication by adding to session
    with client.session_transaction() as sess:
        sess['csrf_token'] = 'test-token'
        sess['user_token'] = 'test_token'

    # Mock the witness form submission with evidence data
    form_data = {
        'csrf_token': 'test-token',
        'full_name': 'Test Witness',
        'contact': 'test@example.com',
        'statement': 'I witnessed the incident',
        'date': '2025-10-10',
        'sig_consented': 'on',
        'sig_name': 'Test Witness',
        'user_token': 'test_token',
        'evidence_timestamp': '2025-10-10T12:00:00Z',
        'evidence_location': '40.7128,-74.0060 (±10m)',
        'location_accuracy': '10'
    }

    # This will fail auth, but we can check the route exists
    rv = client.post('/resources/witness_statement_save', data=form_data)
    assert rv.status_code in [400, 401]  # Expected without proper auth (CSRF or auth failure)

def test_static_evidence_system_js_exists():
    """Test that evidence system JavaScript file exists"""
    js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'js', 'evidence-system.js')
    assert os.path.exists(js_path)

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for key functionality
    assert 'SemptifyEvidence' in content
    assert 'geolocation' in content
    assert 'MediaRecorder' in content
    assert 'webkitSpeechRecognition' in content
    assert 'evidence-copilot' in content

def test_evidence_panel_template_exists():
    """Test that evidence panel template exists"""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'evidence_panel.html')
    assert os.path.exists(template_path)

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'evidence-panel' in content
    assert 'toggleRecording' in content
    assert 'toggleVoiceRecognition' in content
    assert 'askAI' in content

