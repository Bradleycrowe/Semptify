# Semptify Function/Class Inventory

## modules/office_module/backend_demo.py
- list_rooms()
- create_room()
- room_token(room_id)
- list_documents()
- init_upload()
- upload_put(doc_id)
- complete_upload(doc_id)
- lock_document(doc_id)
- annotate(doc_id)
- office_page()

## modules/office_module/ai_orchestrator.py
- async def home(request: Request)
- async def office_page(request: Request)
- async def preview_page(request: Request, slug: str)
- class AIRequestAI(BaseModel)
- class AIOrchestrateRequest(BaseModel)
- class AIJobStatus(BaseModel)
- def send_to_ai(ai_endpoint: str, payload: Dict[str, Any], api_key: str = None)
- def synthesize_results(results: List[Dict[str, Any]], strategy: str)
- def record_event(job_id: str, action: str, metadata: Dict[str, Any])
- async def orchestrate(request: AIOrchestrateRequest, background_tasks: BackgroundTasks)
- def _run_job(job_id: str)

## modules/law_notes/mn_jurisdiction_checklist.py
- mn_checklist()

## modules/law_notes/law_notes_actions.py
- check_broker()
- file_broker_complaint()
- generate_demand_letter()
- identify_owner()
- file_owner_complaint()
- attach_evidence_packet()
- upload_evidence()
- group_evidence()
- export_evidence_packet()
- export_multilingual()

## modules/law_notes/evidence_packet_builder.py
- show_evidence_packet_builder()

## modules/law_notes/evidence_metadata.py
- evidence_metadata()

## modules/law_notes/complaint_templates.py
- complaint_template()

## modules/law_notes/attorney_trail.py
- attorney_trail_view()

## modules/public_exposure_module.py
- index()

## SemptifyAppGUI.py
- class SemptifyAppGUI(QMainWindow)
- __init__()
- initUI()
- setup_top_bar()
- reload_gui()
- setup_core_pages()
- make_page(title_text)
- make_office_page()
- make_tools_page()
- make_temp_todo_page()
- make_concierge_box()
- make_vault_page()
- make_admin_page()
- setup_office_buttons()
- open_office_page()
- create_room()
- list_rooms()
- upload_document()
- open_rights_explorer()
- get_selected_scenario()
- generate_complaint(scenario)
