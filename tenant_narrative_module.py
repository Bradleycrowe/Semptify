from flask import Blueprint, request

tenant_narrative_bp = Blueprint('tenant_narrative', __name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
  <title>UVTA Tenant Narrative Form</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; }
    h2 { color: #b30000; }
    label { font-weight: bold; }
    textarea, input, select { width: 100%; margin-bottom: 15px; padding: 8px; }
    button { background-color: #b30000; color: white; padding: 10px 20px; border: none; cursor: pointer; }
  </style>
</head>
<body>
  <h2>🗣 Tenant Narrative Form</h2>
  <form method="POST" action="/tenant_narrative/submit_narrative">
    <label>Name (optional):</label>
    <input type="text" name="name">

    <label>Unit/Apt #:</label>
    <input type="text" name="unit">

    <label>Property Address:</label>
    <input type="text" name="address">

    <label>Date of Incident(s):</label>
    <input type="text" name="date">

    <label>Landlord or Property Manager Name(s):</label>
    <input type="text" name="landlord">

    <label>Your Story:</label>
    <textarea name="story" rows="6" placeholder="Describe what happened in your own words..."></textarea>

    <label>Impact:</label>
    <textarea name="impact" rows="4" placeholder="How did this affect you or your household?"></textarea>

    <label>Do you have documentation?</label>
    <select name="evidence">
      <option value="yes">Yes</option>
      <option value="no">No</option>
    </select>

    <label>Consent to use your story:</label>
    <select name="consent">
      <option value="public">Yes, publicly</option>
      <option value="anonymous">Yes, anonymously</option>
      <option value="internal">No, internal use only</option>
    </select>

    <label>Anything else you'd like to share?</label>
    <textarea name="extra" rows="3"></textarea>

    <button type="submit">Submit Narrative</button>
  </form>
</body>
</html>
"""

@tenant_narrative_bp.route('/')
def form():
    return HTML_FORM

@tenant_narrative_bp.route('/submit_narrative', methods=['POST'])
def submit_narrative():
    data = {
        "name": request.form.get("name"),
        "unit": request.form.get("unit"),
        "address": request.form.get("address"),
        "date": request.form.get("date"),
        "landlord": request.form.get("landlord"),
        "story": request.form.get("story"),
        "impact": request.form.get("impact"),
        "evidence": request.form.get("evidence"),
        "consent": request.form.get("consent"),
        "extra": request.form.get("extra")
    }
    print("Narrative received:", data)
    return "<h3>✅ Thank you for sharing your story. UVTA stands with you.</h3>"
