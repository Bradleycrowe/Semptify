"""Tests for evidence collection functionality."""
import os
import io
import json
import importlib
import shutil


def test_evidence_home_requires_auth(tmp_path, monkeypatch):
    """Test that evidence page requires authentication."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.chdir(tmp_path)
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    response = client.get('/evidence')
    assert response.status_code == 401


def test_evidence_home_with_auth(tmp_path, monkeypatch):
    """Test evidence page with valid authentication."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.chdir(tmp_path)
    
    # Prepare users.json
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    token_plain = 'test-token-123'
    user_entry = [{
        'id': 'test-user-123',
        'name': 'Test User',
        'hash': sempt._hash_token(token_plain),
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')
    
    response = client.get(f'/evidence?user_token={token_plain}')
    assert response.status_code == 200
    assert b'Evidence Collection' in response.data


def test_evidence_submit_basic(tmp_path, monkeypatch):
    """Test basic evidence submission with timestamp."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.chdir(tmp_path)
    
    # Prepare users.json
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    token_plain = 'test-token-123'
    user_entry = [{
        'id': 'test-user-123',
        'name': 'Test User',
        'hash': sempt._hash_token(token_plain),
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')
    
    # Submit evidence (CSRF disabled in open mode)
    response = client.post('/api/evidence/submit',
                          data={
                              'user_token': token_plain,
                              'title': 'Leak in Bathroom',
                              'description': 'Water leaking from ceiling since yesterday'
                          },
                          content_type='multipart/form-data')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'evidence_id' in data
    
    # Verify evidence file was created
    evidence_path = tmp_path / 'uploads' / 'evidence' / 'test-user-123' / 'evidence_metadata.json'
    assert evidence_path.exists()
    evidence_data = json.loads(evidence_path.read_text())
    assert len(evidence_data) == 1
    assert evidence_data[0]['title'] == 'Leak in Bathroom'
    assert 'timestamp' in evidence_data[0]


def test_evidence_submit_with_location(tmp_path, monkeypatch):
    """Test evidence submission with location data."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.chdir(tmp_path)
    
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    token_plain = 'test-token-456'
    user_entry = [{
        'id': 'test-user-456',
        'name': 'Test User 2',
        'hash': sempt._hash_token(token_plain),
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')
    
    response = client.post('/api/evidence/submit',
                          data={
                              'user_token': token_plain,
                              'title': 'Noise Complaint',
                              'description': 'Excessive noise from upstairs neighbor',
                              'location_lat': '40.7128',
                              'location_lng': '-74.0060',
                              'location_address': '123 Main St, New York, NY'
                          },
                          content_type='multipart/form-data')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify location was saved
    evidence_path = tmp_path / 'uploads' / 'evidence' / 'test-user-456' / 'evidence_metadata.json'
    evidence_data = json.loads(evidence_path.read_text())
    assert evidence_data[0]['location'] is not None
    assert evidence_data[0]['location']['lat'] == 40.7128
    assert evidence_data[0]['location']['lng'] == -74.006
    assert evidence_data[0]['location']['address'] == '123 Main St, New York, NY'


def test_evidence_submit_with_audio(tmp_path, monkeypatch):
    """Test evidence submission with audio file."""
    monkeypatch.setenv('SECURITY_MODE', 'open')
    monkeypatch.chdir(tmp_path)
    
    sec_dir = tmp_path / 'security'
    sec_dir.mkdir()
    users_path = sec_dir / 'users.json'
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    token_plain = 'test-token-789'
    user_entry = [{
        'id': 'test-user-789',
        'name': 'Test User 3',
        'hash': sempt._hash_token(token_plain),
        'enabled': True
    }]
    users_path.write_text(json.dumps(user_entry), encoding='utf-8')
    
    # Create a fake audio file
    audio_data = b'fake audio data for testing'
    
    response = client.post('/api/evidence/submit',
                          data={
                              'user_token': token_plain,
                              'title': 'Harassment Recording',
                              'description': 'Recording of landlord making threats',
                              'audio': (io.BytesIO(audio_data), 'recording.webm')
                          },
                          content_type='multipart/form-data')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify audio file was saved
    evidence_path = tmp_path / 'uploads' / 'evidence' / 'test-user-789' / 'evidence_metadata.json'
    evidence_data = json.loads(evidence_path.read_text())
    assert evidence_data[0]['audio_file'] is not None
    assert evidence_data[0]['audio_sha256'] is not None
    
    # Check that audio file exists
    audio_file = tmp_path / 'uploads' / 'evidence' / 'test-user-789' / evidence_data[0]['audio_file']
    assert audio_file.exists()


def test_evidence_metadata_functions(tmp_path, monkeypatch):
    """Test evidence metadata helper functions."""
    monkeypatch.chdir(tmp_path)
    
    import SemptifyGUI as sempt
    importlib.reload(sempt)
    
    # Test directory creation
    user_dir = sempt._evidence_user_dir('test-user-999')
    assert os.path.exists(user_dir)
    assert 'test-user-999' in user_dir
    
    # Test save and load
    test_items = [
        {
            'id': 'test-123',
            'title': 'Test Evidence',
            'description': 'Test description',
            'timestamp': '2025-10-10T12:00:00Z'
        }
    ]
    sempt._evidence_save('test-user-999', test_items)
    loaded_items = sempt._evidence_load('test-user-999')
    assert len(loaded_items) == 1
    assert loaded_items[0]['title'] == 'Test Evidence'

