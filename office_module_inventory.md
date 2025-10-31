# Office Module Function/Class Inventory

## backend_demo.py
- `list_rooms()`
- `create_room()`
- `room_token(room_id)`
- `list_documents()`
- `init_upload()`
- `upload_put(doc_id)`
- `complete_upload(doc_id)`
- `lock_document(doc_id)`
- `annotate(doc_id)`
- `office_page()`

## ai_orchestrator.py
- `async def home(request: Request)`
- `async def office_page(request: Request)`
- `async def preview_page(request: Request, slug: str)`
- `class AIRequestAI(BaseModel)`
- `class AIOrchestrateRequest(BaseModel)`
- `class AIJobStatus(BaseModel)`
- `def send_to_ai(ai_endpoint: str, payload: Dict[str, Any], api_key: str = None)`
- `def synthesize_results(results: List[Dict[str, Any]], strategy: str)`
- `def record_event(job_id: str, action: str, metadata: Dict[str, Any])`
- `async def orchestrate(request: AIOrchestrateRequest, background_tasks: BackgroundTasks)`
- `def _run_job(job_id: str)`
