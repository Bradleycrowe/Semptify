import importlib


def test_root_returns_200():
    # Import the Flask app from the project
    app = importlib.import_module('Semptify').app
    app.testing = True
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.data[:200]}"
