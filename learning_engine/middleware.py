"""
Learning Middleware - Automatically observes all FastAPI interactions
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from learning_engine.core import get_learning_engine, InteractionType
from typing import Callable
import time
import json

class LearningMiddleware(BaseHTTPMiddleware):
    """Middleware that observes all requests for learning"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        learning_engine = get_learning_engine()
        
        # Capture request details
        start_time = time.time()
        path = request.url.path
        method = request.method
        
        # Get user identifier (from session, token, or IP)
        user_id = await self._get_user_id(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Observe route access
        learning_engine.observe_interaction(
            InteractionType.ROUTE_ACCESS,
            {
                "path": path,
                "method": method,
                "status_code": response.status_code,
                "process_time": process_time
            },
            user_id=user_id,
            metadata={
                "user_agent": request.headers.get("user-agent"),
                "referer": request.headers.get("referer")
            }
        )
        
        return response
    
    async def _get_user_id(self, request: Request) -> str:
        """Extract user identifier from request"""
        # Try session
        if hasattr(request.state, 'user_id'):
            return request.state.user_id
        
        # Try token from header
        if 'X-User-Token' in request.headers:
            return request.headers['X-User-Token']
        
        # Fall back to IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip_{client_ip}"

def observe_form_submission(form_data: dict, form_type: str, user_id: str = None):
    """Helper to observe form submissions"""
    learning_engine = get_learning_engine()
    learning_engine.observe_interaction(
        InteractionType.FORM_SUBMISSION,
        {
            "form_type": form_type,
            "fields": list(form_data.keys()),
            "data": form_data
        },
        user_id=user_id
    )

def observe_document_generation(doc_type: str, doc_data: dict, user_id: str = None):
    """Helper to observe document generation"""
    learning_engine = get_learning_engine()
    
    # Update document statistics
    documents = learning_engine._load_json(learning_engine.documents_db)
    documents['generated_count'] = documents.get('generated_count', 0) + 1
    
    if doc_type not in documents.get('popular_templates', {}):
        documents['popular_templates'][doc_type] = 0
    documents['popular_templates'][doc_type] += 1
    
    learning_engine._save_json(learning_engine.documents_db, documents)
    
    # Log interaction
    learning_engine.observe_interaction(
        InteractionType.DOCUMENT_GENERATION,
        {
            "document_type": doc_type,
            "data": doc_data
        },
        user_id=user_id
    )

def observe_defense_selection(defense_name: str, context: dict, user_id: str = None):
    """Helper to observe defense strategy selection"""
    learning_engine = get_learning_engine()
    learning_engine.observe_interaction(
        InteractionType.DEFENSE_SELECTED,
        {
            "defense_name": defense_name,
            "context": context
        },
        user_id=user_id
    )

def observe_motion_filed(motion_type: str, motion_data: dict, user_id: str = None):
    """Helper to observe motion filing"""
    learning_engine = get_learning_engine()
    learning_engine.observe_interaction(
        InteractionType.MOTION_FILED,
        {
            "motion_type": motion_type,
            "data": motion_data
        },
        user_id=user_id
    )

def record_case_outcome(outcome_data: dict):
    """Helper to record case outcome"""
    learning_engine = get_learning_engine()
    learning_engine.record_outcome(outcome_data)
