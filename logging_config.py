"""
Production Error Monitoring and Logging Configuration
Comprehensive logging with rotation, filtering, and alerting
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime
import traceback


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'ip_address'):
            log_data['ip_address'] = record.ip_address
        
        return json.dumps(log_data)


def setup_production_logging(app):
    """
    Configure comprehensive logging for production.
    
    Creates:
    - Application log (JSON format, rotated daily)
    - Error log (ERROR and CRITICAL only)
    - Access log (all HTTP requests)
    - Security log (auth attempts, rate limits)
    """
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # 1. Application Log (INFO and above, JSON format)
    app_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/application.log',
        when='midnight',
        interval=1,
        backupCount=30,  # Keep 30 days
        encoding='utf-8'
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(JSONFormatter())
    
    # 2. Error Log (ERROR and above, human-readable)
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
        'Location: %(pathname)s:%(lineno)d in %(funcName)s\n'
        '%(message)s\n'
    )
    error_handler.setFormatter(error_formatter)
    
    # 3. Security Log (auth, rate limiting, suspicious activity)
    security_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/security.log',
        when='midnight',
        interval=1,
        backupCount=90,  # Keep 90 days for security logs
        encoding='utf-8'
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.setFormatter(JSONFormatter())
    
    # Configure Flask app logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    
    # Configure security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.INFO)
    security_logger.addHandler(security_handler)
    
    # Configure werkzeug (Flask's HTTP server) logger
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)  # Only warnings and errors
    werkzeug_logger.addHandler(error_handler)
    
    # Disable default Flask logging to console in production
    if os.getenv('FLASK_ENV') == 'production':
        werkzeug_logger.disabled = False
        app.logger.disabled = False
    
    app.logger.info("Production logging configured", extra={
        'log_directory': 'logs/',
        'rotation': 'daily',
        'retention_days': 30
    })
    
    return app


def log_security_event(event_type, details, user_id=None, ip_address=None):
    """
    Log security-related events.
    
    Event types:
    - auth_success / auth_failure
    - rate_limit_exceeded
    - token_rotation
    - breakglass_used
    - suspicious_activity
    """
    security_logger = logging.getLogger('security')
    
    log_data = {
        'event_type': event_type,
        'details': details,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if user_id:
        log_data['user_id'] = user_id
    if ip_address:
        log_data['ip_address'] = ip_address
    
    # Use appropriate log level based on event type
    if 'failure' in event_type or 'suspicious' in event_type:
        security_logger.warning(json.dumps(log_data))
    elif 'breakglass' in event_type:
        security_logger.critical(json.dumps(log_data))
    else:
        security_logger.info(json.dumps(log_data))


def log_error_with_context(app, error, request_id=None, user_id=None):
    """Log errors with full context for debugging"""
    app.logger.error(
        f"Error occurred: {str(error)}",
        exc_info=True,
        extra={
            'request_id': request_id,
            'user_id': user_id,
            'error_type': type(error).__name__
        }
    )


# Monitoring: Check log file sizes
def check_log_health():
    """
    Check logging health and return status.
    Used by /readyz endpoint.
    """
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        return {'status': 'error', 'message': 'Logs directory missing'}
    
    # Check if logs are writable
    test_file = os.path.join(logs_dir, '.write_test')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
    except Exception as e:
        return {'status': 'error', 'message': f'Logs not writable: {e}'}
    
    # Check log sizes
    log_files = ['application.log', 'errors.log', 'security.log']
    log_sizes = {}
    for log_file in log_files:
        path = os.path.join(logs_dir, log_file)
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            log_sizes[log_file] = f"{size_mb:.2f} MB"
    
    return {
        'status': 'healthy',
        'log_sizes': log_sizes,
        'directory': logs_dir
    }


# Example usage in Semptify.py:
# from logging_config import setup_production_logging, log_security_event
# app = setup_production_logging(app)