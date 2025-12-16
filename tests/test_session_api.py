"""
Tests for Session API endpoints.
"""
import pytest
import json
import os

# Ensure security mode is open for testing
os.environ['SECURITY_MODE'] = 'open'


@pytest.fixture
def client():
    """Create test client."""
    from Semptify import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestSessionAPI:
    """Test session management API."""
    
    def test_create_session_missing_token(self, client):
        """POST /api/session/create without token returns 400."""
        resp = client.post('/api/session/create', json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'error' in data
    
    def test_create_session_invalid_token(self, client):
        """POST /api/session/create with invalid token returns 401."""
        resp = client.post('/api/session/create', json={'permanent_token': 'invalid123'})
        assert resp.status_code == 401
        data = resp.get_json()
        assert 'error' in data
    
    def test_validate_session_no_token(self, client):
        """GET /api/session/validate without token returns 401."""
        resp = client.get('/api/session/validate')
        assert resp.status_code == 401
        data = resp.get_json()
        assert data['valid'] is False
    
    def test_logout_always_succeeds(self, client):
        """POST /api/session/logout always succeeds."""
        resp = client.post('/api/session/logout')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['message'] == 'Logged out'
    
    def test_register_and_session_flow(self, client):
        """Full flow: register -> create session -> validate -> logout."""
        # Register new user
        resp = client.post('/api/session/register', json={'role': 'user'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'user_id' in data
        assert 'permanent_token' in data
        
        permanent_token = data['permanent_token']
        user_id = data['user_id']
        
        # Create session with permanent token
        resp = client.post('/api/session/create', json={'permanent_token': permanent_token})
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'session_token' in data
        assert 'expires_at' in data
        assert data['user_id'] == user_id
        
        session_token = data['session_token']
        
        # Validate session
        resp = client.get('/api/session/validate', headers={'Authorization': f'Bearer {session_token}'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['valid'] is True
        assert data['user_id'] == user_id
        
        # Get session info
        resp = client.get('/api/session/info', headers={'X-Session-Token': session_token})
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'user_id' in data
        
        # Get current user (protected route)
        resp = client.get('/api/session/me', headers={'Authorization': f'Bearer {session_token}'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['user_id'] == user_id
        
        # Logout
        resp = client.post('/api/session/logout', headers={'Authorization': f'Bearer {session_token}'})
        assert resp.status_code == 200
        
        # Session should be invalid after logout
        resp = client.get('/api/session/validate', headers={'Authorization': f'Bearer {session_token}'})
        assert resp.status_code == 401
    
    def test_refresh_session(self, client):
        """Test session refresh flow."""
        # Register
        resp = client.post('/api/session/register', json={})
        data = resp.get_json()
        permanent_token = data['permanent_token']
        
        # Create session
        resp = client.post('/api/session/create', json={'permanent_token': permanent_token})
        data = resp.get_json()
        old_token = data['session_token']
        
        # Refresh session
        resp = client.post('/api/session/refresh', headers={'Authorization': f'Bearer {old_token}'}, json={})
        assert resp.status_code == 200
        data = resp.get_json()
        new_token = data['session_token']
        
        # Old token should be invalid
        resp = client.get('/api/session/validate', headers={'Authorization': f'Bearer {old_token}'})
        assert resp.status_code == 401
        
        # New token should be valid
        resp = client.get('/api/session/validate', headers={'Authorization': f'Bearer {new_token}'})
        assert resp.status_code == 200


class TestVaultWithSession:
    """Test vault access using session tokens."""
    
    def test_vault_with_session_token(self, client):
        """Access vault using session token instead of user token."""
        # Register and create session
        resp = client.post('/api/session/register', json={})
        data = resp.get_json()
        permanent_token = data['permanent_token']
        user_id = data['user_id']
        
        # Create session
        resp = client.post('/api/session/create', json={'permanent_token': permanent_token})
        data = resp.get_json()
        session_token = data['session_token']
        
        # Access vault with session token via Bearer header
        resp = client.get('/vault', headers={'Authorization': f'Bearer {session_token}'})
        assert resp.status_code == 200
        
        # Access vault with session token via X-Session-Token header
        resp = client.get('/vault', headers={'X-Session-Token': session_token})
        assert resp.status_code == 200