"""
Role Guards - Role-based access control for unified dashboard
Provides decorators and utilities for 5-tier access system
"""
from functools import wraps
from typing import Optional, List
from fastapi import HTTPException, Header, Query
from security import validate_user_token, validate_admin_token
import json
from pathlib import Path

# Role hierarchy (higher number = more access)
ROLE_HIERARCHY = {
    "user": 1,
    "attorney": 2,
    "advocate": 3,
    "manager": 4,
    "admin": 5
}

def get_user_role(user_token: str) -> Optional[str]:
    """Get role for a user token"""
    if validate_admin_token(user_token):
        return "admin"
    if validate_user_token(user_token):
        return "user"  # Default, will enhance with DB lookup
    return None

def has_role_access(user_role: str, required_role: str) -> bool:
    """Check if user_role has access to required_role features"""
    user_level = ROLE_HIERARCHY.get(user_role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 999)
    return user_level >= required_level

def get_accessible_features(role: str) -> List[str]:
    """Get list of feature IDs accessible to this role"""
    features = []
    user_level = ROLE_HIERARCHY.get(role, 0)
    
    if user_level >= 1:  # user
        features.extend(["vault", "rent_ledger", "timeline", "calendar", "complaint_filing", "housing_journey"])
    if user_level >= 2:  # attorney
        features.extend(["legal_review", "court_forms", "attestation", "case_strategy"])
    if user_level >= 3:  # advocate
        features.extend(["client_management", "doc_upload_assistance", "journey_guide"])
    if user_level >= 4:  # manager
        features.extend(["case_overview", "analytics", "vault_oversight", "team_activity"])
    if user_level >= 5:  # admin
        features.extend(["user_management", "system_config", "metrics", "token_management"])
    
    return features
