#!/usr/bin/env python3
"""
Quick template generator for Semptify UI stub pages
Creates all missing templates with proper structure
"""

import os
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Define all stub templates needed
STUB_TEMPLATES = {
    "resources.html": {
        "title": "Resources",
        "subtitle": "Learning center and support resources",
        "content": """
    <div class="cards-grid">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🎓 Educational Resources</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="/know-your-rights" class="btn btn-outline btn-sm btn-block">Know Your Rights</a></li>
            <li class="mb-2"><a href="/library" class="btn btn-outline btn-sm btn-block">Legal Library</a></li>
            <li class="mb-2"><a href="/faq" class="btn btn-outline btn-sm btn-block">FAQ</a></li>
            <li class="mb-2"><a href="/how-it-works" class="btn btn-outline btn-sm btn-block">How It Works</a></li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🛠️ Tools & Utilities</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="/tools/complaint-generator" class="btn btn-outline btn-sm btn-block">Complaint Generator</a></li>
            <li class="mb-2"><a href="/tools/statute-calculator" class="btn btn-outline btn-sm btn-block">Statute Calculator</a></li>
            <li class="mb-2"><a href="/tools/court-packet" class="btn btn-outline btn-sm btn-block">Court Packet Builder</a></li>
            <li class="mb-2"><a href="/tools/rights-explorer" class="btn btn-outline btn-sm btn-block">Rights Explorer</a></li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">📞 Support</h2>
        </div>
        <div class="card-body">
          <p>Need help? Contact our support team.</p>
          <div style="margin-top: var(--space-md);">
            <p><strong>Email:</strong> support@semptify.org</p>
            <p><strong>Hours:</strong> Mon-Fri 9am-5pm EST</p>
          </div>
        </div>
      </div>
    </div>
        """
    },
    
    "library.html": {
        "title": "Legal Library",
        "subtitle": "Templates, guides, and legal references",
        "content": """
    <div class="cards-grid">
      <div class="card">
        <div class="card-body">
          <h3 class="card-title">📋 Templates</h3>
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Complaint Letter Template</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Notice to Cure</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Demand Letter</a></li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-body">
          <h3 class="card-title">📚 Guides</h3>
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Tenant Rights Guide</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Evidence Collection</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Court Preparation</a></li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-body">
          <h3 class="card-title">⚖️ Legal References</h3>
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">State Laws</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Local Ordinances</a></li>
            <li class="mb-2"><a href="#" class="btn btn-outline btn-sm btn-block">Case Precedents</a></li>
          </ul>
        </div>
      </div>
    </div>
        """
    },
    
    "tools.html": {
        "title": "Tools & Utilities",
        "subtitle": "Specialized legal tools for your case",
        "content": """
    <div class="cards-grid">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">📝 Complaint Generator</h2>
        </div>
        <div class="card-body">
          <p>Generate formal complaints for landlord violations.</p>
          <a href="/tools/complaint-generator" class="btn btn-primary mt-3">Open Tool</a>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">⏱️ Statute Calculator</h2>
        </div>
        <div class="card-body">
          <p>Calculate statute of limitations deadlines by jurisdiction.</p>
          <a href="/tools/statute-calculator" class="btn btn-primary mt-3">Open Tool</a>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">⚖️ Court Packet Builder</h2>
        </div>
        <div class="card-body">
          <p>Assemble evidence into court-ready packets.</p>
          <a href="/tools/court-packet" class="btn btn-primary mt-3">Open Tool</a>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">📚 Rights Explorer</h2>
        </div>
        <div class="card-body">
          <p>Explore your legal rights by scenario.</p>
          <a href="/tools/rights-explorer" class="btn btn-primary mt-3">Open Tool</a>
        </div>
      </div>
    </div>
        """
    },
    
    "complaint_generator.html": {
        "title": "Complaint Generator",
        "subtitle": "Generate formal complaints for landlord violations",
        "content": """
    <div class="container container-lg">
      <div class="card">
        <div class="card-body">
          <form method="post">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            
            <div class="form-group">
              <label for="complaint-type">Type of Complaint</label>
              <select id="complaint-type" name="complaint_type">
                <option value="">-- Select --</option>
                <option value="maintenance">Maintenance Issues</option>
                <option value="harassment">Harassment</option>
                <option value="illegal-entry">Illegal Entry</option>
                <option value="utilities">Utilities Shut Off</option>
                <option value="eviction">Improper Eviction</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="description">Description</label>
              <textarea id="description" name="description" placeholder="Describe the issue in detail..."></textarea>
            </div>
            
            <div class="form-group">
              <label for="date">Date Issue Occurred</label>
              <input type="date" id="date" name="date">
            </div>
            
            <button type="submit" class="btn btn-primary">Generate Complaint</button>
          </form>
        </div>
      </div>
    </div>
        """
    },
    
    "statute_calculator.html": {
        "title": "Statute of Limitations Calculator",
        "subtitle": "Calculate important legal deadlines",
        "content": """
    <div class="container container-lg">
      <div class="card">
        <div class="card-body">
          <form method="post">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-lg);">
              <div class="form-group">
                <label for="action-type">Action Type</label>
                <select id="action-type" name="action_type">
                  <option value="">-- Select --</option>
                  <option value="eviction">Eviction Notice</option>
                  <option value="complaint">Complaint Filed</option>
                  <option value="service">Service of Process</option>
                  <option value="appeal">Appeal Deadline</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="jurisdiction">Jurisdiction</label>
                <select id="jurisdiction" name="jurisdiction">
                  <option value="">-- Select State --</option>
                  <option value="ca">California</option>
                  <option value="ny">New York</option>
                  <option value="tx">Texas</option>
                  <option value="fl">Florida</option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label for="start-date">Start Date</label>
              <input type="date" id="start-date" name="start_date">
            </div>
            
            <button type="submit" class="btn btn-primary">Calculate Deadline</button>
          </form>
          
          <div id="result" class="mt-4" style="display: none;">
            <div class="alert alert-info">
              <strong>Deadline:</strong> <span id="deadline-date"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
        """
    },
    
    "court_packet_builder.html": {
        "title": "Court Packet Builder",
        "subtitle": "Assemble evidence into court-ready documents",
        "content": """
    <div class="container">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-lg);">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Available Evidence</h2>
          </div>
          <div class="card-body">
            <div id="evidence-list" style="max-height: 400px; overflow-y: auto;">
              <p class="text-muted">No evidence available. <a href="/evidence/gallery">View your evidence gallery.</a></p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Court Packet</h2>
          </div>
          <div class="card-body">
            <div id="packet-preview" style="max-height: 400px; overflow-y: auto;">
              <p class="text-muted">Add evidence to begin building your packet.</p>
            </div>
            <div style="margin-top: var(--space-lg); display: flex; gap: var(--space-md);">
              <button class="btn btn-primary">Export as PDF</button>
              <button class="btn btn-outline">Clear All</button>
            </div>
          </div>
        </div>
      </div>
    </div>
        """
    },
    
    "rights_explorer.html": {
        "title": "Rights Explorer",
        "subtitle": "Learn about your legal rights",
        "content": """
    <div class="container container-lg">
      <div class="card">
        <div class="card-body">
          <form method="post">
            <div class="form-group">
              <label for="scenario">Select Your Situation</label>
              <select id="scenario" name="scenario">
                <option value="">-- Choose --</option>
                <option value="eviction">Landlord served eviction notice</option>
                <option value="maintenance">Landlord won't make repairs</option>
                <option value="harassment">Experiencing harassment</option>
                <option value="entry">Landlord entered without notice</option>
                <option value="rent-increase">Received rent increase notice</option>
              </select>
            </div>
            
            <button type="submit" class="btn btn-primary">Explore Rights</button>
          </form>
        </div>
      </div>
      
      <div id="rights-info" class="mt-4" style="display: none;">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Your Rights</h2>
          </div>
          <div class="card-body" id="rights-content">
            <!-- Rights content will appear here -->
          </div>
        </div>
      </div>
    </div>
        """
    },
    
    "know_your_rights.html": {
        "title": "Know Your Rights",
        "subtitle": "Understanding tenant and renter rights",
        "content": """
    <div class="cards-grid">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🏠 Housing Rights</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: disc; padding-left: var(--space-lg);">
            <li>Right to safe and habitable housing</li>
            <li>Right to quiet enjoyment of property</li>
            <li>Protection from unlawful entry</li>
            <li>Right to proper notice before eviction</li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">💰 Financial Rights</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: disc; padding-left: var(--space-lg);">
            <li>Protection from improper rent increases</li>
            <li>Right to receive written lease terms</li>
            <li>Right to security deposit return</li>
            <li>Limits on late fees and charges</li>
          </ul>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🛡️ Legal Protections</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: disc; padding-left: var(--space-lg);">
            <li>Protection from retaliation</li>
            <li>Disability accommodations (ADA)</li>
            <li>Fair housing protections</li>
            <li>Service animal protections</li>
          </ul>
        </div>
      </div>
    </div>
        """
    },
    
    "settings.html": {
        "title": "Settings",
        "subtitle": "Manage your account and preferences",
        "content": """
    <div class="container container-md">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Account Settings</h2>
        </div>
        <div class="card-body">
          <form method="post">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            
            <div class="form-group">
              <label for="email">Email Address</label>
              <input type="email" id="email" name="email" value="" required>
            </div>
            
            <div class="form-group">
              <label for="name">Full Name</label>
              <input type="text" id="name" name="name" value="">
            </div>
            
            <div class="form-group">
              <label for="language">Language</label>
              <select id="language" name="language">
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
              </select>
            </div>
            
            <div class="form-check">
              <input type="checkbox" id="notifications" name="notifications" checked>
              <label for="notifications">Enable email notifications</label>
            </div>
            
            <button type="submit" class="btn btn-primary mt-4">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
        """
    },
    
    "help.html": {
        "title": "Help & Support",
        "subtitle": "Get help using Semptify",
        "content": """
    <div class="cards-grid">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">❓ Frequently Asked Questions</h2>
        </div>
        <div class="card-body">
          <div class="mb-3">
            <strong>How do I upload evidence?</strong>
            <p class="text-muted">Go to the Vault or Evidence Gallery and click "Upload". All files are encrypted and verified.</p>
          </div>
          <div class="mb-3">
            <strong>How do I build a court packet?</strong>
            <p class="text-muted">Use the Court Packet Builder to select evidence and organize it chronologically.</p>
          </div>
          <div class="mb-3">
            <strong>Can I share my vault?</strong>
            <p class="text-muted">Yes! Create a read-only share link for trusted people like your attorney.</p>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">📞 Contact Us</h2>
        </div>
        <div class="card-body">
          <p><strong>Email Support:</strong><br>support@semptify.org</p>
          <p><strong>Phone Support:</strong><br>1-800-SEMPTIFY</p>
          <p><strong>Hours:</strong><br>Mon-Fri 9am-5pm EST</p>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🎓 Learning Resources</h2>
        </div>
        <div class="card-body">
          <ul style="list-style: none; padding: 0;">
            <li class="mb-2"><a href="/how-it-works" class="btn btn-outline btn-sm btn-block">How It Works</a></li>
            <li class="mb-2"><a href="/library" class="btn btn-outline btn-sm btn-block">Legal Library</a></li>
            <li class="mb-2"><a href="/know-your-rights" class="btn btn-outline btn-sm btn-block">Know Your Rights</a></li>
          </ul>
        </div>
      </div>
    </div>
        """
    },
}

# Base template structure
BASE_TEMPLATE = """{{%% extends "shell.html" %%}}

{{%% block title %%}}{title} • Semptify{{%% endblock %%}}

{{%% block content %%}}
<div class="page-header">
  <h1 class="page-title">{title}</h1>
  <p class="page-subtitle">{subtitle}</p>
</div>

{content}
{{%% endblock %%}}
"""

def create_stub_templates():
    """Create all stub templates."""
    created = []
    skipped = []
    
    for filename, config in STUB_TEMPLATES.items():
        filepath = TEMPLATES_DIR / filename
        
        if filepath.exists():
            skipped.append(filename)
            print(f"⊘ Skipped {filename} (already exists)")
            continue
        
        content = BASE_TEMPLATE.format(
            title=config["title"],
            subtitle=config["subtitle"],
            content=config.get("content", "")
        )
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        created.append(filename)
        print(f"✓ Created {filename}")
    
    return created, skipped

if __name__ == "__main__":
    print("🚀 Creating Semptify UI Stub Templates\n")
    print("=" * 60)
    
    created, skipped = create_stub_templates()
    
    print("\n" + "=" * 60)
    print(f"\n✅ Created: {len(created)} templates")
    if created:
        for f in created:
            print(f"   - {f}")
    
    print(f"\n⊘ Skipped: {len(skipped)} templates (already exist)")
    if skipped:
        for f in skipped:
            print(f"   - {f}")
    
    print("\n" + "=" * 60)
    print("✨ All templates ready!")
    print("\nNext steps:")
    print("  1. Update shell.html to include navigation")
    print("  2. Run: python -m flask run")
    print("  3. Visit: http://localhost:5000/dashboard")
