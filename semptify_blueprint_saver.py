import os
from datetime import datetime

# === CONFIGURATION ===
MODULE_NAME = "legal_enforcement_suite"
BASE_DIR = os.path.expanduser("~/SemptifyBlueprints")  # Change to your preferred path
CLOUD_SYNC_DIR = os.path.expanduser("~/OneDrive/SemptifyBlueprints")  # Optional cloud sync

# === CONTENT ===
README = """\
# Legal Enforcement Suite

This module wires federal, state, and local housing codes into Semptify's GUI and backend.
Includes GUI buttons, backend complaint hooks, and citations for enforcement.

## Buttons
- Fair Housing Violation -> 42 U.S.C. § 3601
- ADA Accessibility -> 42 U.S.C. § 12131–12189
- Lead Paint Disclosure -> 24 CFR § 35.92
- HUD Funding Misuse -> 24 CFR Part 964
- IRS Rental Fraud -> IRS Pub. 527, 26 U.S.C. § 42
- EPA Pesticide Use -> 7 U.S.C. § 136
- MN Habitability -> MN Statutes Ch. 504B
- Eagan Sidewalk Code -> Eagan Code § 7.08
- P-Trap Plumbing Code -> UPC § 1001.2
"""

HTML = """\
<!-- legal_enforcement_suite.html -->
<div class="module">
  <h2>Legal Enforcement Suite</h2>
  <button onclick="triggerComplaint('Fair Housing Act')">Fair Housing Violation</button>
  <button onclick="triggerComplaint('ADA Accessibility')">Disability Access Violation</button>
  <button onclick="triggerComplaint('Lead Paint Disclosure')">Lead Paint Exposure</button>
  <button onclick="triggerComplaint('HUD Funding Misuse')">Public Housing Misuse</button>
  <button onclick="triggerComplaint('IRS Rental Fraud')">Tax Fraud Trigger</button>
  <button onclick="triggerComplaint('EPA Pesticide Use')">Unsafe Pesticide Alert</button>
  <button onclick="triggerComplaint('MN Habitability')">Minnesota Habitability Violation</button>
  <button onclick="triggerComplaint('Eagan Sidewalk Code')">Sidewalk/Grass Violation</button>
  <button onclick="triggerComplaint('P-Trap Plumbing Code')">Plumbing Trap Violation</button>
</div>
"""

PYTHON = """\
# complaint_generator.py (hook extension)
def triggerComplaint(domain):
    citations = {
        "Fair Housing Act": "42 U.S.C. § 3601",
        "ADA Accessibility": "42 U.S.C. § 12131–12189",
        "Lead Paint Disclosure": "24 CFR § 35.92",
        "HUD Funding Misuse": "24 CFR Part 964",
        "IRS Rental Fraud": "IRS Pub. 527, 26 U.S.C. § 42",
        "EPA Pesticide Use": "7 U.S.C. § 136",
        "MN Habitability": "MN Statutes Ch. 504B",
        "Eagan Sidewalk Code": "Eagan Code § 7.08",
        "P-Trap Plumbing Code": "UPC § 1001.2"
    }
    complaint = generate_complaint(domain, citations[domain])
    return complaint
"""

# === SAVE FUNCTION ===
def save_blueprint():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    folder_name = f"{MODULE_NAME}_{timestamp}"
    full_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(full_path, exist_ok=True)

    # Replace unsupported characters in README
    readme_fixed = README.replace("→", "->")

    with open(os.path.join(full_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_fixed)
    with open(os.path.join(full_path, "legal_enforcement_suite.html"), "w") as f:
        f.write(HTML)
    with open(os.path.join(full_path, "complaint_generator.py"), "w") as f:
        f.write(PYTHON)

    print(f"✅ Saved locally to: {full_path}")

    # Optional cloud sync
    if os.path.exists(CLOUD_SYNC_DIR):
        cloud_path = os.path.join(CLOUD_SYNC_DIR, folder_name)
        os.system(f'cp -r "{full_path}" "{cloud_path}"')
        print(f"☁️ Synced to cloud at: {cloud_path}")

if __name__ == "__main__":
    save_blueprint()
