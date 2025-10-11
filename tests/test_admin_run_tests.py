import os
import pytest
from SemptifyGUI import app


def test_admin_run_tests_open_mode():
    """Test that tests can be executed from admin dashboard in open mode"""
    os.environ['SECURITY_MODE'] = 'open'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # First get CSRF token
        rv = client.get('/admin')
        assert rv.status_code == 200
        
        # Extract CSRF token from response
        from flask import session as flask_session
        with client.session_transaction() as sess:
            csrf_token = sess.get('csrf_token', '')
        
        # Run tests via the endpoint
        rv = client.post('/admin/run_tests', data={
            'token': 'any-token-in-open-mode',
            'confirm_run_tests': 'yes',
            'csrf_token': csrf_token,
            'test_path': 'tests/test_app.py::test_index',
            'verbose': 'off'
        })
        
        assert rv.status_code == 200
        assert b'Test Results' in rv.data
        assert b'test_app.py::test_index' in rv.data or b'tests/test_app.py' in rv.data


def test_admin_run_tests_requires_confirmation():
    """Test that test execution requires confirmation field"""
    os.environ['SECURITY_MODE'] = 'open'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['csrf_token'] = 'test-token'
        
        # Try without confirmation
        rv = client.post('/admin/run_tests', data={
            'token': 'any-token',
            'csrf_token': 'test-token',
            'test_path': 'tests/'
        })
        
        assert rv.status_code == 400


def test_admin_run_tests_requires_csrf():
    """Test that test execution requires CSRF token in enforced mode"""
    os.environ['SECURITY_MODE'] = 'enforced'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # Try without CSRF token
        rv = client.post('/admin/run_tests', data={
            'token': 'any-token',
            'confirm_run_tests': 'yes',
            'test_path': 'tests/'
        })
        
        assert rv.status_code == 400
        assert b'CSRF validation failed' in rv.data
