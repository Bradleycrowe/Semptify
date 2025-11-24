"""
Profile Manager - Single-user mode with multiple client/case profiles
Replaces multi-user system with case-based organization
"""
import json
import os
from datetime import datetime
from pathlib import Path

PROFILES_DIR = Path("data/profiles")
PROFILES_FILE = PROFILES_DIR / "profiles.json"
ACTIVE_PROFILE_FILE = PROFILES_DIR / "active_profile.json"

def init_profiles():
    """Initialize profiles directory and default profile"""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    
    if not PROFILES_FILE.exists():
        default = {
            "profiles": {
                "default": {
                    "id": "default",
                    "name": "My Case",
                    "description": "Default case profile",
                    "created_at": datetime.now().isoformat(),
                    "color": "#4A90E2"
                }
            }
        }
        PROFILES_FILE.write_text(json.dumps(default, indent=2))
    
    if not ACTIVE_PROFILE_FILE.exists():
        ACTIVE_PROFILE_FILE.write_text(json.dumps({"active": "default"}, indent=2))

def get_all_profiles():
    """Get all client/case profiles"""
    init_profiles()
    data = json.loads(PROFILES_FILE.read_text())
    return data.get("profiles", {})

def get_active_profile():
    """Get currently active profile"""
    init_profiles()
    active_data = json.loads(ACTIVE_PROFILE_FILE.read_text())
    profile_id = active_data.get("active", "default")
    
    profiles = get_all_profiles()
    return profiles.get(profile_id, profiles.get("default"))

def set_active_profile(profile_id):
    """Switch to different profile"""
    profiles = get_all_profiles()
    if profile_id not in profiles:
        return False
    
    ACTIVE_PROFILE_FILE.write_text(json.dumps({"active": profile_id}, indent=2))
    return True

def create_profile(name, description="", color="#4A90E2"):
    """Create new client/case profile"""
    profiles = get_all_profiles()
    
    # Generate ID from name
    profile_id = name.lower().replace(" ", "_").replace("/", "_")
    counter = 1
    original_id = profile_id
    while profile_id in profiles:
        profile_id = f"{original_id}_{counter}"
        counter += 1
    
    profiles[profile_id] = {
        "id": profile_id,
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "color": color
    }
    
    PROFILES_FILE.write_text(json.dumps({"profiles": profiles}, indent=2))
    return profile_id

def update_profile(profile_id, **kwargs):
    """Update profile metadata"""
    profiles = get_all_profiles()
    if profile_id not in profiles:
        return False
    
    for key in ["name", "description", "color"]:
        if key in kwargs:
            profiles[profile_id][key] = kwargs[key]
    
    profiles[profile_id]["updated_at"] = datetime.now().isoformat()
    PROFILES_FILE.write_text(json.dumps({"profiles": profiles}, indent=2))
    return True

def delete_profile(profile_id):
    """Delete a profile (cannot delete default)"""
    if profile_id == "default":
        return False
    
    profiles = get_all_profiles()
    if profile_id not in profiles:
        return False
    
    del profiles[profile_id]
    PROFILES_FILE.write_text(json.dumps({"profiles": profiles}, indent=2))
    
    # If this was active, switch to default
    active_data = json.loads(ACTIVE_PROFILE_FILE.read_text())
    if active_data.get("active") == profile_id:
        set_active_profile("default")
    
    return True

def get_profile_data_path(profile_id=None):
    """Get data directory for specific profile"""
    if profile_id is None:
        profile = get_active_profile()
        profile_id = profile["id"]
    
    path = PROFILES_DIR / profile_id
    path.mkdir(parents=True, exist_ok=True)
    return path
