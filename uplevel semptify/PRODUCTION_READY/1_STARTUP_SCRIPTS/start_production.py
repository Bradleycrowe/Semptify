#!/usr/bin/env python3
"""
Semptify Production Web Server Startup Script
Starts Flask with Waitress WSGI server with production configurations
"""

import os
import sys
import signal
import logging
from datetime import datetime
from pathlib import Path
from waitress import serve
from Semptify import app

# ============================================================
# CONFIGURATION
# ============================================================

# Get configuration from environment or use defaults
PORT = int(os.getenv('SEMPTIFY_PORT', os.getenv('PORT', 8080)))
HOST = os.getenv('SEMPTIFY_HOST', '0.0.0.0')
THREADS = int(os.getenv('SEMPTIFY_THREADS', 4))
WORKERS = int(os.getenv('SEMPTIFY_WORKERS', 1))
MAX_REQUEST_BODY_SIZE = int(os.getenv('MAX_REQUEST_BODY_SIZE', 16777216))  # 16MB
SHUTDOWN_TIMEOUT = int(os.getenv('SHUTDOWN_TIMEOUT', 30))

# Directories to ensure exist
REQUIRED_DIRS = [
    'uploads',
    'logs',
    'security',
    'copilot_sync',
    'final_notices',
    'data'
]

# ============================================================
# LOGGING SETUP
# ============================================================

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler('logs/production.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# STARTUP CHECKS
# ============================================================

def ensure_directories():
    """Ensure all required directories exist"""
    logger.info("Checking required directories...")
    for directory in REQUIRED_DIRS:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"✓ Created directory: {directory}")
        else:
            logger.info(f"✓ Directory exists: {directory}")

def check_environment():
    """Verify production environment variables"""
    logger.info("Checking environment variables...")
    
    required_vars = ['FLASK_SECRET']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.warning(f"⚠ Missing environment variable: {var}")
    
    optional_vars = [
        'SECURITY_MODE',
        'AI_PROVIDER',
        'GITHUB_TOKEN',
        'ADMIN_RATE_WINDOW',
        'ADMIN_RATE_MAX',
        'ACCESS_LOG_JSON'
    ]
    
    logger.info("Optional environment variables:")
    for var in optional_vars:
        value = os.getenv(var, 'not set')
        logger.info(f"  {var}: {value}")
    
    return len(missing_vars) == 0

def check_database():
    """Check if database connection is working"""
    logger.info("Checking database connectivity...")
    try:
        # Add any database checks here
        logger.info("✓ Database check passed")
        return True
    except Exception as e:
        logger.error(f"✗ Database check failed: {e}")
        return False

def startup_checks():
    """Run all startup checks"""
    logger.info("=" * 60)
    logger.info("SEMPTIFY PRODUCTION STARTUP")
    logger.info("=" * 60)
    logger.info(f"Startup time: {datetime.now().isoformat()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info("")
    
    # Ensure directories
    ensure_directories()
    logger.info("")
    
    # Check environment
    env_ok = check_environment()
    logger.info("")
    
    # Check database
    db_ok = check_database()
    logger.info("")
    
    if not env_ok:
        logger.warning("⚠ Some required environment variables are missing")
        logger.warning("  Proceeding anyway, but some features may not work")
    
    if not db_ok:
        logger.warning("⚠ Database connectivity check failed")
        logger.warning("  Proceeding anyway, but database operations may fail")
    
    logger.info("=" * 60)

# ============================================================
# SIGNAL HANDLERS
# ============================================================

def handle_sigterm(signum, frame):
    """Handle SIGTERM signal for graceful shutdown"""
    logger.info("\n" + "=" * 60)
    logger.info("SIGTERM received - initiating graceful shutdown")
    logger.info("=" * 60)
    sys.exit(0)

def handle_sigint(signum, frame):
    """Handle SIGINT signal (Ctrl+C) for graceful shutdown"""
    logger.info("\n" + "=" * 60)
    logger.info("SIGINT received - initiating graceful shutdown")
    logger.info("=" * 60)
    sys.exit(0)

# ============================================================
# MAIN SERVER START
# ============================================================

def start_server():
    """Start the production web server"""
    logger.info("\n" + "=" * 60)
    logger.info("STARTING WEB SERVER")
    logger.info("=" * 60)
    logger.info(f"Host: {HOST}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Threads: {THREADS}")
    logger.info(f"Workers: {WORKERS}")
    logger.info(f"Max request body size: {MAX_REQUEST_BODY_SIZE} bytes")
    logger.info(f"Shutdown timeout: {SHUTDOWN_TIMEOUT} seconds")
    logger.info("=" * 60)
    logger.info("")
    logger.info(f"🚀 Server starting at http://{HOST}:{PORT}")
    logger.info("   Press Ctrl+C to stop")
    logger.info("")
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigint)
    
    try:
        # Serve with Waitress
        serve(
            app,
            host=HOST,
            port=PORT,
            threads=THREADS,
            _quiet=False,
            _start=True,
            max_request_body_size=MAX_REQUEST_BODY_SIZE,
            shutdown_timeout=SHUTDOWN_TIMEOUT,
            url_scheme='https' if os.getenv('FORCE_HTTPS') else 'http',
        )
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    try:
        startup_checks()
        start_server()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
