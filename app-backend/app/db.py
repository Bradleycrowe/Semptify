"""Lightweight DB helper with sqlite fallback.

This module exposes a SQLAlchemy engine created from DATABASE_URL env var
or falls back to a local sqlite file for local development.
"""
import os
import time
from sqlalchemy import create_engine, text

# Determine base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)


def get_database_url() -> str:
    # Prefer common env var DATABASE_URL
    env_url = os.environ.get('DATABASE_URL')
    if env_url:
        return env_url
    # Fallback to sqlite in data directory
    sqlite_path = os.path.join(DATA_DIR, 'semptify.db')
    return f'sqlite:///{sqlite_path.replace('\\', '/')}'


_engine = None


def get_engine():
    global _engine
    if _engine is not None:
        return _engine
    url = get_database_url()
    # If sqlite, ensure check_same_thread is disabled for SQLAlchemy usage pattern
    connect_args = {}
    if url.startswith('sqlite:'):
        connect_args = {'check_same_thread': False}
    _engine = create_engine(url, connect_args=connect_args)
    return _engine


def test_connection(timeout: float = 2.0) -> dict:
    """Test DB connectivity. Returns a dict with status and details.

    Always returns quickly for sqlite (file-backed). If remote DB is unreachable
    the exception text will be included.
    """
    engine = get_engine()
    start = time.time()
    try:
        with engine.connect() as conn:
            # lightweight query
            conn.execute(text('SELECT 1'))
        elapsed = time.time() - start
        return {'ok': True, 'latency_s': round(elapsed, 3), 'url': summarize_url(get_database_url())}
    except Exception as e:
        elapsed = time.time() - start
        return {'ok': False, 'error': str(e), 'latency_s': round(elapsed, 3), 'url': summarize_url(get_database_url())}


def summarize_url(url: str) -> str:
    # Return a safe summary (scheme and host/path only, hide credentials)
    try:
        if url.startswith('sqlite:'):
            return 'sqlite (local file)'
        # naive parsing for common DB URL forms
        # show scheme and host/path, strip user:pass@
        if '://' in url:
            scheme, rest = url.split('://', 1)
            if '@' in rest:
                rest = rest.split('@', 1)[1]
            return f"{scheme}://{rest}"
    except Exception:
        pass
    return 'unknown'
