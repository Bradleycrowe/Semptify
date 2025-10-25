"""Minimal webapp entrypoint for Semptify.

This file is intentionally small: it provides a simple Flask
application so projects or tools that expect `webapp/app.py`
exist will find a runnable module.

Usage (PowerShell):
    python c:\Semptify\Semptify\webapp\app.py

The app is configured to look for templates/static in the repo
relative locations.
"""
from flask import Flask, render_template

app = Flask(__name__, static_folder='../static', template_folder='../templates')


@app.route('/')
def index():
    # Simple placeholder page useful for smoke testing or when tools
    # expect a webapp package with an `app.py` module.
    return 'Semptify webapp placeholder — app.py present'


if __name__ == '__main__':
    # Run on an alternate port to avoid colliding with main app if needed.
    app.run(debug=True, host='127.0.0.1', port=5001)
