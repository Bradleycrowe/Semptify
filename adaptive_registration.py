"""
Adaptive User Registration for Semptify
Automatically learns from user location information.
"""

from location_intelligence import get_location_intelligence
from engines.jurisdiction_engine import get_jurisdiction_engine
from engines.learning_engine import get_learning
from typing import Dict, Any


def register_user_adaptive(
    user_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Register user and automatically learn from their location.

    User provides:
        - address (or city, state, zip)
        - email/phone

    System automatically:
        - Detects location
        - Discovers resources
        - Learns laws
        - Prepares guidance
    """

    # Get intelligence systems
    location_intel = get_location_intelligence()
    jurisdiction = get_jurisdiction_engine()
    learning = get_learning()

    # 1. DETECT LOCATION
    if "address" in user_data:
        location = location_intel.detect_location_from_address(user_data["address"])
    else:
        location = location_intel.detect_location_from_user(user_data)

    print(f"📍 Detected location: {location['city']}, {location['state']} {location['zip']}")

    # 2. DISCOVER RESOURCES (if new location)
    location_data = location_intel.discover_resources(location)

    # 3. PREPARE USER PROFILE
    user_profile = {
        "user_id": user_data.get("user_id"),
        "location": location,
        "location_key": location_data["location_key"],
        "discovered_resources": location_data["resources"],
        "applicable_laws": jurisdiction.determine_applicable_laws(
            issue_category="all",
            user_location=location
        ),
        "local_statistics": location_data["statistics"],
        "guidance_ready": True
    }

    # 4. LEARN FROM REGISTRATION DATA
    # If user provided rent amount, fees, etc., learn from it
    if "rent_amount" in user_data:
        location_intel.learn_from_user_data(
            location_data["location_key"],
            "rent_amount",
            {
                "bedrooms": user_data.get("bedrooms", "1br"),
                "amount": user_data["rent_amount"]
            }
        )

    if "application_fee" in user_data:
        location_intel.learn_from_user_data(
            location_data["location_key"],
            "application_fee",
            {"amount": user_data["application_fee"]}
        )

    return user_profile


def report_issue_adaptive(
    user_id: str,
    location_key: str,
    issue_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    User reports an issue - system learns from it.

    User provides:
        - issue_type (no_heat, mold, leak, etc.)
        - description

    System automatically:
        - Updates issue statistics for location
        - Provides applicable laws
        - Suggests procedures
        - Learns what works
    """

    location_intel = get_location_intelligence()
    jurisdiction = get_jurisdiction_engine()

    # Get location data
    location_data = location_intel.locations.get(location_key)
    if not location_data:
        return {"error": "Location not found"}

    # Learn from issue
    location_intel.learn_from_user_data(
        location_key,
        "issue",
        {
            "issue_type": issue_data["issue_type"],
            "severity": issue_data.get("severity", "normal")
        }
    )

    # Extract location components
    location = {
        "city": location_data["city"],
        "state": location_data["state"],
        "zip": location_data["zip"]
    }

    # Get applicable laws
    laws = jurisdiction.determine_applicable_laws(
        issue_category=issue_data["issue_type"],
        user_location=location
    )

    # Get procedures (learned from previous cases)
    procedures = location_data.get("procedures", {})

    return {
        "issue_id": f"issue_{user_id}_{issue_data['issue_type']}",
        "applicable_laws": [
            {
                "statute": law.statute,
                "requirement": law.requirement,
                "deadline": law.deadline
            }
            for law in laws
        ],
        "procedures": procedures.get(issue_data["issue_type"], {
            "learning_status": "Gathering data from similar cases..."
        }),
        "resources": location_data.get("resources", {}),
        "local_context": {
            "common_in_area": issue_data["issue_type"] in [
                i["type"] for i in location_data["statistics"]["common_issues"]["top_issues"]
            ],
            "typical_timeline": "Learning from user experiences..."
        }
    }


def report_outcome_adaptive(
    location_key: str,
    outcome_data: Dict[str, Any]
):
    """
    User reports outcome - system learns procedures.

    User provides:
        - what they did
        - where they filed
        - how long it took
        - what happened

    System learns:
        - Actual procedures that work
        - Real timelines
        - Resources that helped
    """

    location_intel = get_location_intelligence()

    # Learn from outcome
    location_intel.learn_from_user_data(
        location_key,
        "outcome",
        outcome_data
    )

    print(f"✅ Learned from outcome - will help future users in this area!")


def contribute_resource_adaptive(
    location_key: str,
    resource_data: Dict[str, Any]
):
    """
    User contributes a resource - system adds and verifies.

    User provides:
        - resource name
        - contact info
        - type (hotline, legal_aid, etc.)

    System:
        - Adds to location data
        - Makes available to other users
        - Verifies over time
    """

    location_intel = get_location_intelligence()

    location_intel.learn_from_user_data(
        location_key,
        "resource",
        resource_data
    )

    print(f"✅ Resource added - helping others in {location_key}!")


# Example usage documentation
"""
ADAPTIVE REGISTRATION FLOW:

1. User signs up with address:

   user_profile = register_user_adaptive({
       "user_id": "user123",
       "address": "123 Main St, Eagan, MN 55121",
       "email": "tenant@example.com"
   })

   → System automatically:
     - Detects: Eagan, MN, Dakota County
     - Discovers: HOME Line, legal aid, housing court
     - Learns: Minnesota Statutes §504B.xxx
     - Prepares: Rent ranges, common issues, procedures

2. User reports rent amount:

   register_user_adaptive({
       "user_id": "user123",
       "address": "123 Main St, Eagan, MN 55121",
       "rent_amount": 1350,
       "bedrooms": "1br"
   })

   → System learns: 1BR in Eagan typically $1,350

3. User reports issue:

   issue_response = report_issue_adaptive(
       "user123",
       "eagan_mn_55121",
       {
           "issue_type": "no_heat",
           "severity": "emergency"
       }
   )

   → System provides:
     - MN Statute §504B.161 (habitability)
     - 24-hour emergency timeline
     - HOME Line hotline
     - Common in area? Stats
     - Procedures learned from others

4. User resolves issue:

   report_outcome_adaptive(
       "eagan_mn_55121",
       {
           "issue_type": "no_heat",
           "filed_with": "Eagan Code Enforcement",
           "timeline": "2 days",
           "successful": True,
           "method": "Called 651-675-5500"
       }
   )

   → Next user with no_heat gets:
     "Call Eagan Code Enforcement at 651-675-5500
      Typically resolved in 2 days"

5. User shares resource:

   contribute_resource_adaptive(
       "eagan_mn_55121",
       {
           "type": "legal_aid",
           "name": "Southern MN Regional Legal Services",
           "phone": "952-888-9615",
           "helped_with": "security_deposit_dispute"
       }
   )

   → Resource now shown to all Eagan users
"""
