"""Pytest fixtures for Semptify tests."""
import pytest
import sys
import os

# Add parent directory to path so we can import from Semptify
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client():
    """Provide a Flask test client for integration tests."""
    from Semptify import app

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
