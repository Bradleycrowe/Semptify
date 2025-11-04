"""
Flask Blueprint: Data Flow API endpoints

Provides REST API for:
- Registering module functions
- Processing documents through flow
- Tracking document lineage
- Viewing actor activity
"""

from flask import Blueprint, request, jsonify
from data_flow_engine import get_data_flow

data_flow_bp = Blueprint("data_flow", __name__, url_prefix="/api/data-flow")


@data_flow_bp.route("/register-functions", methods=["POST"])
def register_module_functions():
    """Register functions from a module.

    Body:
    {
        "module_name": "office_module",
        "functions": [
            {
                "name": "upload_document",
                "input_type": "document",
                "output_type": "document",
                "description": "Upload and process a document",
                "handler": null
            }
        ]
    }
    """
    data = request.get_json() or {}
    module_name = data.get("module_name")
    functions = data.get("functions", [])

    if not module_name or not functions:
        return jsonify({"error": "module_name and functions required"}), 400

    flow = get_data_flow()
    flow.register_module_functions(module_name, functions)

    return jsonify(
        {
            "status": "registered",
            "module": module_name,
            "functions_count": len(functions),
        }
    )


@data_flow_bp.route("/functions", methods=["GET"])
def list_functions():
    """List all registered functions with optional filters.

    Query params:
    - module: filter by module name
    - input_type: filter by input type
    """
    module = request.args.get("module")
    input_type = request.args.get("input_type")

    flow = get_data_flow()
    functions = flow.registry.list_functions(module=module, input_type=input_type)

    return jsonify(
        {
            "total": len(functions),
            "functions": [
                {
                    k: v for k, v in f.items() if k != "handler"  # Don't serialize handler
                }
                for f in functions
            ],
        }
    )


@data_flow_bp.route("/process-document", methods=["POST"])
def process_document():
    """Process a document through the data flow with reaction rules.

    Body:
    {
        "doc_type": "receipt",  # lease, receipt, notice, complaint, evidence
        "file_path": "/path/to/file.pdf",
        "owner_id": "tenant-123",
        "context": {
            "amount": 1200,
            "date": "2025-01-01",
            "property": "123 Main St",
            "is_late": false
        },
        "trigger_function": "upload_payment",
        "reaction_rules": [
            {
                "condition": "is_payment",
                "reaction": "update_ledger"
            },
            {
                "condition": "is_late_payment",
                "reaction": "suggest_notice"
            }
        ]
    }
    """
    data = request.get_json() or {}

    doc_type = data.get("doc_type")
    file_path = data.get("file_path")
    owner_id = data.get("owner_id")
    context = data.get("context", {})
    trigger_function = data.get("trigger_function")
    reaction_rules = data.get("reaction_rules", [])

    if not all([doc_type, file_path, owner_id, trigger_function]):
        return jsonify(
            {"error": "doc_type, file_path, owner_id, trigger_function required"}
        ), 400

    flow = get_data_flow()
    doc_ref, flow_events = flow.process_document(
        doc_type=doc_type,
        file_path=file_path,
        owner_id=owner_id,
        context=context,
        trigger_function=trigger_function,
        reaction_rules=reaction_rules,
    )

    return jsonify(
        {
            "document": doc_ref.to_dict(),
            "flow_events": [e.to_dict() for e in flow_events],
            "total_events": len(flow_events),
        }
    ), 201


@data_flow_bp.route("/document/<doc_id>/flow", methods=["GET"])
def get_document_flow(doc_id):
    """Get complete flow history for a document (lineage tracking)."""
    flow = get_data_flow()
    result = flow.get_document_flow(doc_id)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@data_flow_bp.route("/actor/<actor_id>/flow", methods=["GET"])
def get_actor_flow(actor_id):
    """Get all data flow activity for an actor (user)."""
    flow = get_data_flow()
    result = flow.get_actor_flow(actor_id)

    return jsonify(result)


@data_flow_bp.route("/registry", methods=["GET"])
def get_registry():
    """Get data flow registry status."""
    flow = get_data_flow()

    functions = flow.registry.list_functions()
    modules = set(f["module"] for f in functions)

    return jsonify(
        {
            "total_functions": len(functions),
            "modules": list(modules),
            "functions": [
                {k: v for k, v in f.items() if k != "handler"} for f in functions
            ],
        }
    )


@data_flow_bp.route("/statistics", methods=["GET"])
def get_statistics():
    """Get data flow statistics."""
    flow = get_data_flow()

    total_docs = len(flow.documents)
    total_events = len(flow.flow_events)
    doc_types = {}
    for doc in flow.documents.values():
        doc_types[doc.doc_type] = doc_types.get(doc.doc_type, 0) + 1

    reaction_types = {}
    for event in flow.flow_events:
        reaction_types[event.reaction_type] = (
            reaction_types.get(event.reaction_type, 0) + 1
        )

    return jsonify(
        {
            "total_documents": total_docs,
            "total_events": total_events,
            "documents_by_type": doc_types,
            "reactions_by_type": reaction_types,
        }
    )
