"""
AI Orchestrator Routes - FastAPI with Learning
Multi-agent orchestration UI and API
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import json

from ai_orchestrator import Orchestrator, Agent, load_agents_from_file
from learning_engine import get_learning_engine, InteractionType

router = APIRouter(prefix="/ai", tags=["AI Orchestrator"])

AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'ai_agents.json')


class OrchestratorRunRequest(BaseModel):
    prompt: str
    agents: Optional[List[str]] = None


@router.post("/orchestrator/run")
async def orchestrator_run(
    request: OrchestratorRunRequest,
    learning = Depends(get_learning_engine)
):
    """Execute multi-agent orchestration round"""
    await learning.observe_interaction(
        InteractionType.FORM_SUBMISSION,
        {
            "route": "/ai/orchestrator/run",
            "prompt_length": len(request.prompt),
            "agent_count": len(request.agents) if request.agents else 0,
            "agents_selected": request.agents
        }
    )
    
    agents = load_agents_from_file(AGENTS_FILE)
    chosen = [a for a in agents if a.id in request.agents] if request.agents else agents
    
    if not chosen:
        raise HTTPException(status_code=400, detail="No agents selected or available")
    
    orchestrator = Orchestrator(chosen)
    result = orchestrator.run_round(request.prompt, context={})
    
    await learning.observe_interaction(
        InteractionType.DOCUMENT_GENERATED,
        {
            "route": "/ai/orchestrator/run",
            "agents_used": [a.id for a in chosen],
            "response_count": len(result.get('timeline', [])),
            "success": True
        }
    )
    
    return JSONResponse(content=result)


@router.get("/agents")
async def list_agents_api(learning = Depends(get_learning_engine)):
    """List all available agents"""
    await learning.observe_interaction(
        InteractionType.ROUTE_ACCESS,
        {"route": "/ai/agents"}
    )
    
    if os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(content={'agents': []})


@router.post("/agents/seed")
async def seed_agents_api(learning = Depends(get_learning_engine)):
    """Seed sample agents"""
    await learning.observe_interaction(
        InteractionType.FORM_SUBMISSION,
        {"route": "/ai/agents/seed"}
    )
    
    sample = {
        'agents': [
            {'id': 'legal', 'role': 'Legal Analyst', 'description': 'Summarize relevant eviction law and defenses', 'provider': 'local'},
            {'id': 'evidence', 'role': 'Evidence Collector', 'description': 'Give checklist for capturing photos, audio, and metadata', 'provider': 'local'},
            {'id': 'notary', 'role': 'Notary', 'description': 'Create a simple notary certificate JSON with SHA checks', 'provider': 'local'},
            {'id': 'packet', 'role': 'Packet Builder', 'description': 'Assemble court packet and required documents', 'provider': 'local'},
            {'id': 'summarizer', 'role': 'Summarizer', 'description': 'Condense the timeline and evidence into a one-page narrative', 'provider': 'local'}
        ]
    }
    
    os.makedirs(os.path.dirname(AGENTS_FILE), exist_ok=True)
    with open(AGENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2)
    
    return JSONResponse(content={'seeded': True, 'count': len(sample['agents'])})
