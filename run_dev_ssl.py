import os
from SemptifyGUI import app

if __name__ == '__main__':
    # Paths to local dev cert and key (PEM). Customize via env or defaults under security/
    cert_file = os.environ.get('DEV_SSL_CERT', os.path.join('security', 'dev-local.crt'))
    key_file = os.environ.get('DEV_SSL_KEY', os.path.join('security', 'dev-local.key'))

    # Enforce HTTPS in-app redirects/headers if desired
    os.environ.setdefault('FORCE_HTTPS', '1')

    # Flask's built-in SSL support is fine for local dev/testing (not production)
    # Use waitress/production TLS only behind a proper reverse proxy.
    port = int(os.environ.get('SEMPTIFY_PORT') or os.environ.get('PORT', '8443'))
    host = os.environ.get('SEMPTIFY_HOST', '0.0.0.0')
    print(f"Starting SemptifyGUI (dev SSL) on https://{host}:{port}")
    app.run(host=host, port=port, ssl_context=(cert_file, key_file), debug=False)
