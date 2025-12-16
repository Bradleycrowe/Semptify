# tests/test_new_features.py - Tests for law library, librarian, document center, phone imports, help
import pytest
import json
import os
from io import BytesIO

@pytest.fixture
def client():
    import Semptify
    Semptify.app.config['TESTING'] = True
    return Semptify.app.test_client()

def test_law_library_search(client):
    """Test law library search"""
    response = client.get('/api/law_library/search?q=eviction')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert 'count' in data

def test_law_library_get_law(client):
    """Test getting specific law"""
    response = client.get('/api/law_library/law/MN-STAT-504B')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 'MN-STAT-504B'
    assert 'title' in data

def test_law_library_cross_reference(client):
    """Test creating law-document cross-reference"""
    response = client.post('/api/law_library/cross_reference',
                          json={'law_id': 'MN-STAT-504B', 'document_id': 'DOC123'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['law_id'] == 'MN-STAT-504B'
    assert data['document_id'] == 'DOC123'

def test_librarian_ask(client):
    """Test librarian AI assistant (without actual AI)"""
    response = client.post('/api/librarian/ask',
                          json={'question': 'Can I withhold rent for repairs?'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data
    assert 'laws' in data

def test_librarian_suggest(client):
    """Test librarian law suggestions"""
    response = client.post('/api/librarian/suggest',
                          json={'situation': "My landlord won't fix the heat and it's winter"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'suggested_laws' in data

def test_document_center_upload(client):
    """Test document upload with notary certificate"""
    data = {
        'file': (BytesIO(b'test document content'), 'test.pdf')
    }
    response = client.post('/api/document_center/upload?user_token=123456789012',
                          data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert 'document_id' in result
    assert 'sha256' in result
    assert 'timestamp' in result

def test_document_center_verify(client):
    """Test document tamper detection"""
    response = client.post('/api/document_center/verify',
                          json={'document_id': 'DOC123', 'sha256': 'abc123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'verified' in data

def test_phone_imports_upload_texts(client):
    """Test text message import"""
    data = {
        'file': (BytesIO(b'timestamp,sender,message\n2024-01-01,landlord,test'), 'texts.csv')
    }
    response = client.post('/api/phone_imports/texts?user_token=123456789012',
                          data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert 'import_id' in result

def test_phone_imports_upload_voicemail(client):
    """Test voicemail import"""
    data = {
        'file': (BytesIO(b'fake audio data'), 'voicemail.mp3')
    }
    response = client.post('/api/phone_imports/voicemail?user_token=123456789012',
                          data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert 'import_id' in result

def test_phone_imports_call_logs(client):
    """Test call log import"""
    data = {
        'file': (BytesIO(b'timestamp,number,duration\n2024-01-01,555-1234,60'), 'calls.csv')
    }
    response = client.post('/api/phone_imports/call_logs?user_token=123456789012',
                          data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert 'import_id' in result

def test_azure_doc_intelligence_analyze(client):
    """Test Azure Document Intelligence OCR"""
    data = {
        'file': (BytesIO(b'fake pdf data'), 'doc.pdf')
    }
    response = client.post('/api/azure_doc_intelligence/analyze?user_token=123456789012',
                          data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'text' in result or 'error' in result

def test_help_pages_index(client):
    """Test help pages index"""
    response = client.get('/api/help')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'topics' in data

def test_help_pages_get_topic(client):
    """Test getting specific help topic"""
    response = client.get('/api/help/topic/vault')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'title' in data
    assert 'content' in data

def test_help_pages_search(client):
    """Test help search"""
    response = client.get('/api/help/search?q=upload')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
