import pytest
import os

@pytest.fixture
def client():
    """Flask test client fixture"""
    import Semptify
    Semptify.app.config['TESTING'] = True
    return Semptify.app.test_client()
