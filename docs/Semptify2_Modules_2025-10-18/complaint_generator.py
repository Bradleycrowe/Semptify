# complaint_generator.py

from datetime import datetime

def generate_complaint(tenant_name, landlord_name, issue_description, location, urgency_level):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    complaint = f"""
    SEMPTIFY COMPLAINT FORM
    ------------------------
    Tenant: {tenant_name}
    Landlord: {landlord_name}
    Location: {location}
    Timestamp: {timestamp}
    Urgency Level: {urgency_level}

    Issue Description:
    {issue_description}

    Requested Action:
    - Immediate investigation
    - Written response from landlord
    - Follow-up within 72 hours

    Signature: ______________________
    """
    return complaint.strip()
