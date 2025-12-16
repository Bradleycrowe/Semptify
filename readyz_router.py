"""
Readiness Check FastAPI Router - Health and readiness checks
Converted from Flask blueprint: readyz.py
"""
from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import Dict, Literal
import os

router = APIRouter(tags=["health"])


class ReadinessResponse(BaseModel):
    status: Literal["ready", "degraded"]
    details: Dict[str, str]


@router.get("/readyz", response_model=ReadinessResponse)
async def readyz(response: Response):
    """
    Check application readiness
    
    Validates that critical runtime directories are writable:
    - uploads: User document storage
    - logs: Event and access logs
    - copilot_sync: AI conversation persistence
    - final_notices: Generated court documents
    - security: Token and auth data
    
    Returns:
    - 200 with status="ready" if all checks pass
    - 503 with status="degraded" if any directory not writable
    """
    details = {}
    status = "ready"
    http_code = 200
    
    for d in ["uploads", "logs", "copilot_sync", "final_notices", "security"]:
        ok = os.access(d, os.W_OK)
        details[d] = "ok" if ok else "not writable"
        if not ok:
            status = "degraded"
            http_code = 503
    
    response.status_code = http_code
    return ReadinessResponse(status=status, details=details)
