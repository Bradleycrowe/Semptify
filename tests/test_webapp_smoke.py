def test_webapp_index():
    """Smoke test: ensure the minimal webapp.app module responds on '/' without requiring the full test matrix.

    This test is intentionally narrow so it can run quickly in the local dev environment
    without installing all repo test dependencies.
    """
    # Import the Flask application object from the module
    from webapp.app import app as semptify_webapp

    client = semptify_webapp.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Semptify webapp placeholder' in resp.data
