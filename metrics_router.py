"""
Metrics FastAPI Router - Observability metrics endpoint
Converted from Flask blueprint: metrics.py
"""
from fastapi import APIRouter
from typing import Dict, Any

from security import get_metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """
    Get all observability metrics
    
    Returns Prometheus-compatible metrics including:
    - Request counters (total, admin, errors, rate_limited)
    - Release counters
    - Token rotation counters
    - Latency percentiles (p50, p95, p99, mean, max)
    - Uptime gauge
    """
    return get_metrics()
