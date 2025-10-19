"""
Minimal AI Orchestrator (FastAPI) for Semptify - demo scaffold
Run with: uvicorn ai_orchestrator:app --reload --port 9001

This is a minimal in-memory demo. Replace in-memory stores with a real DB and secure AI endpoints
for production. Use environment variables for DEFAULT_AI_ENDPOINT and AI_API_KEYS mapping.
"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import time
import requests
import os

app = FastAPI(title="Semptify AI Orchestrator")

# Simple in-memory store for demo. Replace with persistent DB.
AI_JOBS = {}

class AIRequestAI(BaseModel):
    name: str
    role: str
    endpoint: str = None

class AIOrchestrateRequest(BaseModel):
    requester: str
    input_refs: List[str]
    ais: List[AIRequestAI]
    strategy: str = "synthesize"
    approval_required: bool = True

class AIJobStatus(BaseModel):
    job_id: str
    status: str
    outputs: Dict[str, Any] = {}


def send_to_ai(ai_endpoint: str, payload: Dict[str, Any], api_key: str = None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    # simple POST to AI endpoint
    resp = requests.post(ai_endpoint, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def synthesize_results(results: List[Dict[str, Any]], strategy: str):
    # naive synthesizer: concatenate with labels
    out = {"content": "\n\n".join([f"--- {r.get('ai','unknown')} ---\n{r.get('content','')}" for r in results])}
    return out


def record_event(job_id: str, action: str, metadata: Dict[str, Any]):
    # replace with DB or events service
    AI_JOBS[job_id]["events"].append({"ts": int(time.time()), "action": action, "metadata": metadata})


@app.post("/api/ai/orchestrate")
async def orchestrate(request: AIOrchestrateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    AI_JOBS[job_id] = {"status": "queued", "request": request.dict(), "events": [], "outputs": {}}
    record_event(job_id, "job_created", {"requester": request.requester})

    def _run_job(job_id: str):
        AI_JOBS[job_id]["status"] = "running"
        record_event(job_id, "job_running", {})
        results = []
        for ai in request.ais:
            ai_entry = {"ai": ai.name, "role": ai.role}
            record_event(job_id, "ai_send", {"ai": ai.name})
            try:
                # build role-specific prompt
                prompt = {
                    "role": ai.role,
                    "context_refs": request.input_refs,
                    "instructions": f"You are {ai.role}. Produce a JSON with keys content and notes."
                }
                endpoint = ai.endpoint or os.getenv("DEFAULT_AI_ENDPOINT")
                if not endpoint:
                    raise ValueError("No AI endpoint configured for " + ai.name)
                resp = send_to_ai(endpoint, {"prompt": prompt})
                ai_entry["result"] = resp
                results.append({"ai": ai.name, "content": resp.get("content", str(resp))})
                record_event(job_id, "ai_success", {"ai": ai.name})
            except Exception as e:
                record_event(job_id, "ai_error", {"ai": ai.name, "error": str(e)})
                ai_entry["error"] = str(e)
                results.append({"ai": ai.name, "content": ""})
        composite = synthesize_results(results, request.strategy)
        AI_JOBS[job_id]["outputs"] = composite
        AI_JOBS[job_id]["status"] = "waiting_approval" if request.approval_required else "complete"
        record_event(job_id, "job_complete", {"status": AI_JOBS[job_id]["status"]})

    background_tasks.add_task(_run_job, job_id)
    return {"job_id": job_id}


@app.get("/api/ai/job/{job_id}", response_model=AIJobStatus)
async def get_job(job_id: str):
    job = AI_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": job["status"], "outputs": job["outputs"]}


@app.post("/api/ai/job/{job_id}/approve")
async def approve_job(job_id: str):
    job = AI_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "waiting_approval":
        raise HTTPException(status_code=400, detail="Job not waiting for approval")
    # persist composite output to documents service
    composite = job["outputs"]
    # call documents service to persist composite (signed manifest)
    # placeholder: simulate saving
    doc_id = str(uuid.uuid4())
    job["status"] = "complete"
    record_event(job_id, "job_approved", {"doc_id": doc_id})
    return {"job_id": job_id, "status": "complete", "document_id": doc_id}
