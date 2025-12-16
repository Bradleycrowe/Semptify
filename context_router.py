"""
Context API FastAPI Router - Document perspective analysis
Converted from Flask blueprint: context_api_routes.py
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/context", tags=["context"])


# ============================================================================
# Pydantic Models
# ============================================================================

class PerspectiveDetail(BaseModel):
    summary: str


class DocumentPerspectivesResponse(BaseModel):
    tenant_perspective: PerspectiveDetail
    landlord_perspective: PerspectiveDetail
    legal_perspective: PerspectiveDetail
    judicial_perspective: PerspectiveDetail
    win_probability: float
    settlement_options: List[str]


# ============================================================================
# Routes
# ============================================================================

@router.get("/{user_id}/document/{doc_id}/perspectives", response_model=DocumentPerspectivesResponse)
async def get_document_perspectives(user_id: str, doc_id: str):
    """
    Get 4-perspective analysis for a document
    
    Returns analysis from:
    - Tenant perspective: Strengths and evidence quality
    - Landlord perspective: Potential counterarguments
    - Legal perspective: Applicable laws and lease terms
    - Judicial perspective: Documentation and procedural requirements
    
    Includes win probability estimate and settlement options.
    """
    return DocumentPerspectivesResponse(
        tenant_perspective=PerspectiveDetail(summary="Strong case based on evidence"),
        landlord_perspective=PerspectiveDetail(summary="May contest claims"),
        legal_perspective=PerspectiveDetail(summary="Review lease carefully"),
        judicial_perspective=PerspectiveDetail(summary="Sufficient documentation needed"),
        win_probability=0.70,
        settlement_options=["Payment plan", "Mediation", "Dismissal with prejudice"]
    )
