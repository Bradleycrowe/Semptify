Semptify Office module

This module provides a scaffold for a secure "Office" workspace with:
- Certified Rooms (video)
- Notary Station
- Document Center with SHA-256 hashing and timestamp/lock flow
- Live Review and annotations
- AI Orchestrator demo

Files:
- office_module.tsx - React frontend component (drop into your React app)
- backend_demo.py - Flask blueprint with minimal endpoints for testing
- ai_orchestrator.py - FastAPI demo service for multi-AI orchestration
- help/ - markdown help files for users, organizers, and admins

How to run demo backend locally (quick):

1) Register the blueprint in your main Flask app (SemptifyGUI.py):

    from modules.office_module.backend_demo import office_bp
    app.register_blueprint(office_bp)

2) Or run a standalone Flask app for testing:

    export FLASK_APP=modules/office_module/backend_demo.py
    flask run --port 9002

How to run the AI orchestrator demo:

    uvicorn modules.office_module.ai_orchestrator:app --reload --port 9001

Notes:
- These are demo scaffolds. Replace in-memory stores with persistent DB and secure AI endpoints before production.
- Use signed URLs for production uploads and store file hashes in the documents table.
