"""
Court AI Training Routes - Flask Blueprint for court training APIs

Provides endpoints for:
- Document validation
- Evidence assessment
- Case strength prediction
- AI training prompt generation
- Training data management
"""

from flask import Blueprint, request, jsonify, render_template
from court_ai_trainer import (
    CourtAITrainer,
    CourtDocument,
    CourtEvidence,
    EvictionCase,
    AITrainingPromptGenerator,
)
import json
from datetime import datetime

# Create Blueprint
court_training_bp = Blueprint('court_training', __name__, url_prefix='/api/court-training')

# Initialize trainer
trainer = CourtAITrainer(state="MN")


# ============================================================================
# Document Validation Endpoint
# ============================================================================

@court_training_bp.route('/validate-document', methods=['POST'])
def validate_document():
    """
    Validate a court document for compliance.
    
    Request JSON:
    {
        "doc_type": "complaint",
        "case_type": "eviction",
        "filed_date": "2025-11-05",
        "signature_present": true,
        "notarized": true,
        "filing_fee_paid": true,
        "service_documented": true,
        "has_table_of_contents": false
    }
    """
    try:
        data = request.json
        
        doc = CourtDocument(
            doc_type=data.get("doc_type"),
            case_type=data.get("case_type"),
            filed_date=data.get("filed_date"),
            response_due_date=data.get("response_due_date"),
            signature_present=data.get("signature_present", False),
            notarized=data.get("notarized", False),
            filing_fee_paid=data.get("filing_fee_paid", False),
            service_documented=data.get("service_documented", False),
            has_table_of_contents=data.get("has_table_of_contents", False),
        )
        
        validation = trainer.validator.validate_document(doc)
        
        return jsonify({
            "status": "success",
            "validation": validation,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


# ============================================================================
# Evidence Assessment Endpoint
# ============================================================================

@court_training_bp.route('/assess-evidence', methods=['POST'])
def assess_evidence():
    """
    Assess evidence for admissibility.
    
    Request JSON:
    {
        "evidence_type": "photo",
        "description": "Mold damage",
        "collection_date": "2025-11-04",
        "collected_by": "tenant",
        "gps_coordinates": "44.9537,-93.0900",
        "timestamp_visible": true,
        "authenticated": true,
        "chain_of_custody_documented": true,
        "is_original": true,
        "quality_score": 0.95
    }
    """
    try:
        data = request.json
        
        evidence = CourtEvidence(
            evidence_type=data.get("evidence_type"),
            description=data.get("description"),
            collection_date=data.get("collection_date"),
            collected_by=data.get("collected_by"),
            gps_coordinates=data.get("gps_coordinates"),
            timestamp_visible=data.get("timestamp_visible", False),
            authenticated=data.get("authenticated", False),
            chain_of_custody_documented=data.get("chain_of_custody_documented", False),
            is_original=data.get("is_original", False),
            quality_score=data.get("quality_score", 0.5),
        )
        
        assessment = trainer.assessor.assess_evidence(evidence)
        
        return jsonify({
            "status": "success",
            "assessment": assessment,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


# ============================================================================
# Case Strength Prediction Endpoint
# ============================================================================

@court_training_bp.route('/predict-case-strength', methods=['POST'])
def predict_case_strength():
    """
    Predict eviction case strength and outcome.
    
    Request JSON:
    {
        "case_id": "CASE-2025-0001",
        "case_type": "non-payment",
        "landlord_defects": ["no_proper_service", "formatting_errors"],
        "tenant_defenses": ["habitability_violation"],
        "evidence_strength": 0.75
    }
    """
    try:
        data = request.json
        
        case = EvictionCase(
            case_id=data.get("case_id"),
            case_type=data.get("case_type"),
            landlord_defects=data.get("landlord_defects", []),
            tenant_defenses=data.get("tenant_defenses", []),
            evidence_strength=data.get("evidence_strength", 0.5),
        )
        
        prediction = trainer.predictor.predict_eviction_case(case)
        
        return jsonify({
            "status": "success",
            "prediction": prediction,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


# ============================================================================
# AI Training Prompt Generation Endpoints
# ============================================================================

@court_training_bp.route('/generate-clerk-prompt', methods=['GET'])
def generate_clerk_prompt():
    """
    Generate system prompt for training AI as court clerk.
    
    Query params:
    - state: State code (default: MN)
    """
    try:
        state = request.args.get('state', 'MN')
        prompt = AITrainingPromptGenerator.generate_court_clerk_system_prompt(state=state)
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "state": state,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


@court_training_bp.route('/generate-evidence-prompt', methods=['POST'])
def generate_evidence_prompt():
    """
    Generate validation prompt for specific evidence.
    
    Request JSON:
    {
        "evidence_type": "photo",
        "description": "Mold damage in bathroom",
        "collection_date": "2025-11-04",
        "collected_by": "tenant"
    }
    """
    try:
        data = request.json
        
        evidence = CourtEvidence(
            evidence_type=data.get("evidence_type"),
            description=data.get("description"),
            collection_date=data.get("collection_date"),
            collected_by=data.get("collected_by"),
        )
        
        prompt = AITrainingPromptGenerator.generate_evidence_validation_prompt(evidence)
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


@court_training_bp.route('/generate-case-prompt', methods=['POST'])
def generate_case_prompt():
    """
    Generate analysis prompt for case.
    
    Request JSON:
    {
        "case_id": "CASE-2025-0001",
        "case_type": "eviction",
        "landlord_defects": ["no_proper_service"],
        "tenant_defenses": ["habitability_violation"],
        "evidence_strength": 0.75
    }
    """
    try:
        data = request.json
        
        case = EvictionCase(
            case_id=data.get("case_id"),
            case_type=data.get("case_type"),
            landlord_defects=data.get("landlord_defects", []),
            tenant_defenses=data.get("tenant_defenses", []),
            evidence_strength=data.get("evidence_strength", 0.5),
        )
        
        prompt = AITrainingPromptGenerator.generate_case_analysis_prompt(case)
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


# ============================================================================
# Comprehensive Submission Analysis Endpoint
# ============================================================================

@court_training_bp.route('/analyze-submission', methods=['POST'])
def analyze_submission():
    """
    Comprehensive analysis of entire court submission.
    
    Request JSON:
    {
        "document": {
            "doc_type": "answer",
            "case_type": "eviction",
            "filed_date": "2025-11-05",
            "signature_present": true,
            "notarized": true,
            "filing_fee_paid": true,
            "service_documented": true
        },
        "evidence": [
            {
                "evidence_type": "photo",
                "description": "Mold damage",
                "collection_date": "2025-11-04",
                "collected_by": "tenant",
                "timestamp_visible": true,
                "authenticated": true,
                "chain_of_custody_documented": true,
                "quality_score": 0.95
            }
        ]
    }
    """
    try:
        data = request.json
        
        # Parse document
        doc_data = data.get("document", {})
        doc = CourtDocument(
            doc_type=doc_data.get("doc_type"),
            case_type=doc_data.get("case_type"),
            filed_date=doc_data.get("filed_date"),
            signature_present=doc_data.get("signature_present", False),
            notarized=doc_data.get("notarized", False),
            filing_fee_paid=doc_data.get("filing_fee_paid", False),
            service_documented=doc_data.get("service_documented", False),
            has_table_of_contents=doc_data.get("has_table_of_contents", False),
        )
        
        # Parse evidence list
        evidence_list = []
        for ev_data in data.get("evidence", []):
            evidence = CourtEvidence(
                evidence_type=ev_data.get("evidence_type"),
                description=ev_data.get("description"),
                collection_date=ev_data.get("collection_date"),
                collected_by=ev_data.get("collected_by"),
                timestamp_visible=ev_data.get("timestamp_visible", False),
                authenticated=ev_data.get("authenticated", False),
                chain_of_custody_documented=ev_data.get("chain_of_custody_documented", False),
                is_original=ev_data.get("is_original", False),
                quality_score=ev_data.get("quality_score", 0.5),
            )
            evidence_list.append(evidence)
        
        # Analyze
        analysis = trainer.analyze_submission(doc, evidence_list)
        
        return jsonify({
            "status": "success",
            "analysis": analysis,
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


# ============================================================================
# Health Check
# ============================================================================

@court_training_bp.route('/health', methods=['GET'])
def health():
    """Health check for court training API."""
    return jsonify({
        "status": "healthy",
        "service": "court-training-api",
        "timestamp": datetime.now().isoformat(),
    }), 200


# ============================================================================
# Documentation Endpoint
# ============================================================================

@court_training_bp.route('/docs', methods=['GET'])
def documentation():
    """Return API documentation."""
    docs = {
        "service": "Court AI Training API",
        "endpoints": {
            "POST /validate-document": "Validate court document for compliance",
            "POST /assess-evidence": "Assess evidence for admissibility",
            "POST /predict-case-strength": "Predict eviction case outcome",
            "GET /generate-clerk-prompt": "Generate AI court clerk training prompt",
            "POST /generate-evidence-prompt": "Generate evidence validation prompt",
            "POST /generate-case-prompt": "Generate case analysis prompt",
            "POST /analyze-submission": "Comprehensive submission analysis",
            "GET /health": "API health check",
            "GET /docs": "This documentation",
        },
        "description": "Train and use AI for courtroom procedures, clerk duties, and legal protocols",
    }
    return jsonify(docs), 200
