#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semptify - Dakota County Eviction Defense (FastAPI)
Includes:
- Interactive modal (multilingual)
- State/federal/funding/online/trial panels
- Courtroom procedures, offensive & defensive motions, arguments
- Negotiation playbook
- Counter-suit tools + official forms catalog
- Court Companion (live hearing helper)
- Answer + Counterclaim + Evidence Index generation
- Checkpoint zip

Run:
  pip install fastapi uvicorn
  python semptify_dakota_full_counterclaims.py
Open:
  http://127.0.0.1:8000/
"""

import os
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ======= Config =======
TODAY = datetime.now().strftime("%Y-%m-%d")
BASE = Path.cwd() / "Semptify"
MODULES = BASE / "modules"
MODULE_NAME = "DakotaCounty_EvictionDefense"
ROOT = MODULES / MODULE_NAME

PATHS = {
    "Root": ROOT,
    "Public": ROOT / "public",
    "Assets": ROOT / "assets",
    "Graphics": ROOT / "assets" / "graphics",
    "Data": ROOT / "data",
    "Flows": ROOT / "flows",
    "Templates": ROOT / "templates",
    "Help": ROOT / "help",
    "Readme": ROOT / "README",
    "Checkpoints": ROOT / "checkpoints",
    "Court": ROOT / "court_helper",
    "Forms": ROOT / "forms"
}

BUNDLE_NAME = f"{MODULE_NAME}_{TODAY}.zip"
CHECKPOINT_ZIP = PATHS["Checkpoints"] / BUNDLE_NAME

def ensure_dirs():
    (BASE).mkdir(exist_ok=True)
    (MODULES).mkdir(exist_ok=True)
    for p in PATHS.values():
        p.mkdir(parents=True, exist_ok=True)

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ======= Scaffolding =======
def scaffold_files():
    # Multilingual help
    help_json = {
        "version": "1.0",
        "languages": ["en", "es", "so"],
        "strings": {
            "en": {
                "cta_counterclaim": "Do you want to raise a counterclaim?",
                "what_is_counterclaim": "A counterclaim is your claim against the landlord, filed in the same eviction case.",
                "when_to_file": "Include counterclaims in your Answer before or at the first hearing.",
                "evidence_tip": "Upload photos, notices, receipts. Add dates and short descriptions.",
                "timeline_tip": "Track deadlines: summons date, answer preparation, first hearing."
            },
            "es": {
                "cta_counterclaim": "¿Desea presentar una contrademanda?",
                "what_is_counterclaim": "Una contrademanda es su reclamación contra el propietario, presentada en el mismo caso de desalojo.",
                "when_to_file": "Incluya las contrademandas en su Respuesta antes o en la primera audiencia.",
                "evidence_tip": "Suba fotos, avisos y recibos. Agregue fechas y descripciones breves.",
                "timeline_tip": "Controle los plazos: fecha de citación, preparación de la respuesta y primera audiencia."
            },
            "so": {
                "cta_counterclaim": "Ma rabtaa inaad keento dacwad ka hortag ah?",
                "what_is_counterclaim": "Dacwadda ka hortagga waa sheegashadaada ka dhanka ah mulkiilaha, oo lagu gudbiyo isla kiiska ka saarista.",
                "when_to_file": "Ku dar dacwooyinka ka hortagga Jawaabtaada ka hor ama kulanka maxkamadda ee ugu horreeya.",
                "evidence_tip": "Ku soo rar sawirro, ogeysiisyo, iyo rasiidhyo. Ku dar taariikho iyo sharaxaad gaaban.",
                "timeline_tip": "La soco waqtiyada: taariikhda wacitaanka, diyaargarowga jawaabta, kulanka koowaad."
            }
        }
    }
    write_file(PATHS["Help"] / "multilingual_help.json", json.dumps(help_json, ensure_ascii=False, indent=2))

    # Statute navigator (state + federal)
    statutes_json = {
        "version": "1.0",
        "jurisdiction": "Minnesota + Federal",
        "statutes": [
            {"cite": "Minn. Stat. § 504B.285", "topic": "Eviction grounds and procedure", "use": "Answer defenses and case framing"},
            {"cite": "Minn. Stat. § 504B.161", "topic": "Habitability covenants", "use": "Counterclaims and Tenant Remedies"},
            {"cite": "Minn. Stat. § 504B.225", "topic": "Retaliation prohibited", "use": "Defenses and counterclaims"},
            {"cite": "Minn. Stat. § 504B.231", "topic": "Lockouts/utility shutoffs illegal", "use": "Emergency relief and damages"},
            {"cite": "Minn. Stat. § 504B.371", "topic": "Tenant Remedies Action", "use": "Motions for repairs and abatement"},
            {"cite": "Fair Housing Act, 42 U.S.C. § 3601 et seq.", "topic": "Anti-discrimination", "use": "Defenses to discriminatory eviction"},
            {"cite": "VAWA, 34 U.S.C. § 12491", "topic": "Survivor protections in federal housing", "use": "Defense against eviction based on abuse"},
            {"cite": "U.S. Const. Amend. XIV", "topic": "Due process", "use": "Notice and fair hearing requirements"}
        ]
    }
    write_file(PATHS["Data"] / "statute_navigator.json", json.dumps(statutes_json, ensure_ascii=False, indent=2))

    # Funding resources
    funding_json = {
        "version": "1.0",
        "programs": [
            {"name": "RentHelpMN (status varies)", "type": "State ERA", "use": "Back rent and utilities where available"},
            {"name": "Housing Benefits 101", "type": "Guidance", "use": "Cash assistance, utility shutoff help, eviction prevention"},
            {"name": "Continuum of Care (CoC)", "type": "Federal HUD", "use": "Prevention, rapid rehousing, case management"},
            {"name": "Emergency Solutions Grants (ESG)", "type": "Federal HUD", "use": "Eviction prevention, shelter diversion"},
            {"name": "Minnesota Housing Trust Fund", "type": "State/local", "use": "Rental assistance for at-risk households"}
        ],
        "tips": [
            "Ask the landlord to accept pending assistance and pause judgment.",
            "Bring proof of application or award to court (emails, portal screenshots).",
            "Request continuance to finalize funding disbursement."
        ]
    }
    write_file(PATHS["Data"] / "funding_resources.json", json.dumps(funding_json, ensure_ascii=False, indent=2))

    # Forms catalog (official references)
    forms_json = {
        "version": "1.0",
        "official_sources": [
            {
                "name": "Minnesota Judicial Branch – Housing/Landlord-Tenant Forms",
                "url": "https://www.mncourts.gov/getforms/housing-landlord-tenant",
                "use": "Eviction Answer, Counterclaim, Rent Escrow, Expungement, Appeals"
            },
            {
                "name": "Minnesota Judicial Branch – Tenant Resources (Forms section)",
                "url": "https://www.mncourts.gov/help-topics/tenants/forms",
                "use": "Statewide/district forms for tenant actions"
            },
            {
                "name": "Rent Escrow statute (Minn. Stat. § 504B.385)",
                "url": "https://www.revisor.mn.gov/statutes/cite/504B.385",
                "use": "Deposit rent with court and seek repairs/abatement"
            },
            {
                "name": "Counterclaim for Possession of Premises (court form)",
                "url": "https://www.uslegalforms.com/forms/mn-hou402/counterclaim-for-possession-of-premises-and-notice",
                "use": "Counter-sue within housing case (official court form distribution)"
            },
            {
                "name": "Minnesota AG – Landlords & Tenants Handbook",
                "url": "https://www.ag.state.mn.us/Consumer/Handbooks/LT/default.asp",
                "use": "Plain-language guide to rights and duties"
            }
        ]
    }
    write_file(PATHS["Forms"] / "forms_catalog.json", json.dumps(forms_json, ensure_ascii=False, indent=2))

    # Templates: Answer, Counterclaim, Motions (including offensive/defensive)
    answer_md = """# Eviction answer template (Dakota County)

**Case caption:** District Court, Dakota County, Housing
**Defendant/Tenant:** [Your Name]
**Plaintiff/Landlord:** [Landlord Name]
**File No.:** [If known]

**Admissions/Denials:**
- **General denial:** Tenant denies allegations not specifically admitted.

**Defenses (select and add facts):**
- **Improper notice/service:** [Facts]
- **Habitability violations (§ 504B.161):** [Facts]
- **Retaliation (§ 504B.225):** [Facts]
- **Illegal lockout/utility shutoff (§ 504B.231):** [Facts]
- **Discrimination (FHA):** [Facts]
- **VAWA survivor protection:** [Facts]

**Relief requested:**
- **Dismissal or continuance**
- **Repairs order / rent abatement**
- **Costs and fees**
"""
    write_file(PATHS["Templates"] / "answer_form.md", answer_md)

    counterclaim_md = """# Counterclaim template (Dakota County)

**Parties:** Tenant counterclaims against Landlord in this eviction case.

**Grounds:**
- **Habitability covenants (§ 504B.161):**
  - Facts: [Heat out, leaks, infestations, etc.]
  - Notice to landlord: [Dates/methods]
- **Retaliation (§ 504B.225):**
  - Facts: [Protected activity + adverse action]
- **Illegal lockout/utility shutoff (§ 504B.231):**
  - Facts: [Dates, actions, impacts]
- **Breach of lease:**
  - Facts: [Terms breached]
- **Discrimination (FHA) / VAWA protections:**
  - Facts: [Protected class/survivor status + adverse action]

**Evidence:** Photos, notices, receipts, communications.

**Relief requested:** Repairs with deadline, rent abatement, statutory remedies, costs/fees, other equitable relief.
"""
    write_file(PATHS["Templates"] / "counterclaim.md", counterclaim_md)

    motions_md = """# Motion library (Dakota County)

## Defensive motions
- **Motion to dismiss (defective notice/service)** — Due process concerns.
- **Motion for continuance** — Time to obtain counsel and organize evidence.

## Offensive motions
- **Tenant Remedies Motion (§ 504B.371)** — Repairs, inspection, rent abatement.
- **Motion to stay writ based on funding** — Pause enforcement pending disbursement.
- **Motion to consolidate related claims** — Efficiency and fairness.

## Funding leverage
- **Stipulate to dismissal upon payment** — Present ERA/CoC/ESG proofs.
- **Request short continuance** — Finalize assistance and avoid judgment.

## Negotiation scripts
- “Landlord agrees to accept rental assistance and dismiss case upon payment.”
- “Parties agree to repair list with deadlines; rent abated until completion.”
"""
    write_file(PATHS["Templates"] / "motions_bundle.md", motions_md)

    # Evidence index & manifest
    evidence_index_md = """# Evidence index

**Case:** [File No.]
**Tenant:** [Your Name]

**Items:**
- **Photo:** [YYYY-MM-DD] — [Issue + location]
- **Notice:** [YYYY-MM-DD] — [Type + summary]
- **Receipt:** [YYYY-MM-DD] — [Amount + purpose]
- **Message:** [YYYY-MM-DD] — [Medium + summary]
"""
    write_file(PATHS["Public"] / "evidence_index.md", evidence_index_md)

    manifest_json = {
        "version": "1.0",
        "files": [
            {"type": "photo", "path": "public/photos", "index": "public/evidence_index.md"},
            {"type": "notice", "path": "public/notices", "index": "public/evidence_index.md"},
            {"type": "receipt", "path": "public/receipts", "index": "public/evidence_index.md"},
            {"type": "message", "path": "public/messages", "index": "public/evidence_index.md"},
        ]
    }
    write_file(PATHS["Public"] / "evidence_manifest.json", json.dumps(manifest_json, ensure_ascii=False, indent=2))

    # Evidence subfolders
    for sub in ["photos", "notices", "receipts", "messages"]:
        (PATHS["Public"] / sub).mkdir(parents=True, exist_ok=True)

    # Resources & referral
    resources_md = """# Resource connector (Dakota County)

**Housing Resource Line:** 651-554-5751
**Legal Aid (MN):** Contact local office for intake.
**Tenant unions:** Connect for accompaniment and organizing.

Use this section to log referrals and outcomes.
"""
    write_file(PATHS["Public"] / "resources.md", resources_md)

    referral_md = """[Date]

Subject: Urgent eviction defense referral — [Tenant Name], [Property Address], Dakota County

To whom it may concern:
Tenant seeks assistance for an eviction case with potential counterclaims (habitability, retaliation, illegal lockout). Hearing is scheduled on [Hearing Date]. Evidence is being compiled and indexed.

Requested support:
- Brief advice or representation
- Inspection or documentation support
- Emergency relief if lockout/shutoff occurred

Sincerely,
[Tenant/Advocate Name]
"""
    write_file(PATHS["Public"] / "referral_letter_template.md", referral_md)

    # Graphics
    rights_svg = """<svg xmlns='http://www.w3.org/2000/svg' width='820' height='560'>
  <rect x='0' y='0' width='820' height='560' fill='#F7FAFC'/>
  <text x='24' y='48' font-size='28' font-family='Arial' fill='#1A202C'>Your rights in court</text>
  <text x='24' y='100' font-size='18' font-family='Arial' fill='#2D3748'>• Raise defenses and counterclaims at the first hearing.</text>
  <text x='24' y='140' font-size='18' font-family='Arial' fill='#2D3748'>• Bring evidence: photos, notices, receipts.</text>
  <text x='24' y='180' font-size='18' font-family='Arial' fill='#2D3748'>• Ask for a continuance if you need more time.</text>
</svg>
"""
    write_file(PATHS["Graphics"] / "rights_infographic.svg", rights_svg)

    steps_svg = """<svg xmlns='http://www.w3.org/2000/svg' width='820' height='560'>
  <rect x='0' y='0' width='820' height='560' fill='#FFFFFF'/>
  <text x='24' y='48' font-size='28' font-family='Arial' fill='#1A202C'>Steps to counterclaim</text>
  <text x='24' y='100' font-size='18' font-family='Arial' fill='#2D3748'>1. Identify grounds (habitability, retaliation, lockout, breach).</text>
  <text x='24' y='140' font-size='18' font-family='Arial' fill='#2D3748'>2. Collect evidence and index it.</text>
  <text x='24' y='180' font-size='18' font-family='Arial' fill='#2D3748'>3. Draft Answer and Counterclaim together.</text>
  <text x='24' y='220' font-size='18' font-family='Arial' fill='#2D3748'>4. File before or at the first hearing.</text>
</svg>
"""
    write_file(PATHS["Graphics"] / "counterclaim_steps.svg", steps_svg)

    # Flows (timeline + simulator)
    timeline_html = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><title>Eviction timeline</title>
<style>
  body { font-family: system-ui, Arial; margin: 24px; }
  .step { border-left: 4px solid #005f99; padding-left: 12px; margin: 16px 0; }
  .date { color: #005f99; font-weight: bold; }
</style></head><body>
  <h2>Eviction timeline</h2>
  <div class="step"><div class="date">Summons served</div><p>Record the service date; this starts your defense clock.</p></div>
  <div class="step"><div class="date">Answer preparation</div><p>Draft Answer + Counterclaim before the first hearing.</p></div>
  <div class="step"><div class="date">First hearing</div><p>Bring evidence, raise defenses and counterclaims.</p></div>
</body></html>
"""
    write_file(PATHS["Flows"] / "deadline_flow.html", timeline_html)

    simulator_html = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><title>Outcome simulator</title>
<style>
  body { font-family: system-ui, Arial; margin: 24px; }
  .node { border: 1px dashed #888; padding: 10px; margin: 8px; border-radius: 6px; }
</style></head><body>
  <h2>Outcome simulator</h2>
  <div class="node">If notice or service is defective → Motion to dismiss may be granted.</div>
  <div class="node">If habitability violations proven → Rent abatement or repairs order.</div>
  <div class="node">If retaliation proven → Eviction barred; potential damages.</div>
  <div class="node">If illegal lockout/shutoff proven → Emergency relief and statutory remedies.</div>
</body></html>
"""
    write_file(PATHS["Flows"] \
               / "outcome_simulator.html", simulator_html)

    # README + Court scripts/checklist
    readme_md = """# Dakota County Eviction Defense (Semptify, FastAPI)

Purpose: Push-button tools to generate Answer + Counterclaim, organize evidence, track deadlines, and click through state law, federal protections, funding, online court procedures, and trial scenarios. Includes Court Companion for live hearings and official forms catalog.

Panels:
- State law: Minnesota eviction statutes, defenses, timelines.
- Federal law: FHA, VAWA, constitutional due process.
- Funding: ERA tips, CoC/ESG programs, trust fund.
- Online court: Zoom etiquette, exhibits, requests.
- Trial scenarios: Motions, evidence, appeals.
- Court Companion: Objections, motions, chat snippets, statute navigator, Zoom helper.
- Forms: Official Minnesota tenant/eviction forms and rent escrow references.

Use:
1. Open http://127.0.0.1:8000 and select language.
2. Draft filings (grounds, facts, relief, evidence).
3. Click panels for guidance; open tools and official forms.
4. Court Companion for live support during hearing.
5. Generate → files saved; checkpoint zip created.
"""
    write_file(PATHS["Readme"] / "README_eviction_defense.md", readme_md)

    court_scripts_md = """# Court Companion scripts (copy-ready)

## Quick objections
- **Hearsay:** “Objection, hearsay.”
- **Foundation:** “Objection, lack of foundation.”
- **Speculation:** “Objection, calls for speculation.”
- **Relevance:** “Objection, relevance.”

## Motions (oral)
- **Continuance:** “Tenant requests a brief continuance to obtain counsel and complete exhibits.”
- **Dismissal (service/notice):** “Tenant moves to dismiss for defective service/notice.”
- **Tenant Remedies:** “Tenant requests repairs order, inspection, and rent abatement under § 504B.371.”
- **Stay of writ for funding:** “Tenant requests stay of writ pending disbursement of approved assistance.”

## Zoom chat snippets
- “Tenant objects to improper service under Minn. Stat. § 504B.285.”
- “Tenant asserts habitability violations under § 504B.161 and requests remedies under § 504B.371.”
- “Tenant requests interpreter.”
- “Tenant requests breakout to confer privately.”

## Exhibit checklist
- Label each item (Photo/Notice/Receipt/Message) with date and short description.
- Be ready to explain relevance and authenticity.
"""
    write_file(PATHS["Court"] / "court_scripts.md", court_scripts_md)

    court_checklist_md = """# Court Companion checklist (Zoom + in-person)

- Join early; rename: “First Last — Tenant”.
- Test audio/video; have exhibits ready to share.
- Mute unless speaking; no recording.
- Ask for interpreter if needed.
- If confused or rushed, request a brief continuance.
- Bring proof of funding applications or awards.
"""
    write_file(PATHS["Court"] / "court_checklist.md", court_checklist_md)

def create_checkpoint_zip():
    if CHECKPOINT_ZIP.exists():
        CHECKPOINT_ZIP.unlink()
    with zipfile.ZipFile(CHECKPOINT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(ROOT):
            for f in files:
                fp = Path(folder) / f
                arc = fp.relative_to(ROOT)
                z.write(fp, arcname=str(arc))

# ======= App =======
ensure_dirs()
scaffold_files()
create_checkpoint_zip()

app = FastAPI(title="Semptify - Dakota County Eviction Defense (All Add-Ons + Court Companion)", version="1.3")
app.mount("/static", StaticFiles(directory=str(ROOT)), name="static")

# ======= UI: Main modal =======
INDEX_HTML = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/>
<title>Dakota County Eviction Defense</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  body { font-family: system-ui, Arial; margin: 24px; max-width: 1000px; }
  .card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 16px 0; }
  .grid2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
  label { display:block; margin-top: 8px; }
  input, textarea, select { width: 100%; padding: 8px; }
  .badge { background: #005f99; color: #fff; padding: 4px 8px; border-radius: 6px; margin-right: 8px; }
  .small { font-size: 12px; color: #555; }
  .panel-btn { margin: 6px 6px 0 0; }
  .companion { background: #f7fbff; border: 1px solid #cfe8ff; }
</style>
</head><body>
  <h1>Dakota County Eviction Defense — Interactive Modal</h1>

  <div class="card">
    <h3>Language</h3>
    <button onclick="loadHelp('en')">English</button>
    <button onclick="loadHelp('es')">Español</button>
    <button onclick="loadHelp('so')">Somali</button>
    <div id="help-box" class="small" style="margin-top:8px;">Select a language to view help text.</div>
  </div>

  <div class="card">
    <div>
      <span class="badge">Counterclaim</span>
      <span class="badge">Answer</span>
      <span class="badge">Evidence</span>
    </div>
    <h3>Draft Answer + Counterclaim</h3>
    <div class="grid2">
      <div><label>Tenant name</label><input id="tenant_name" placeholder="Your name"/></div>
      <div><label>Landlord name</label><input id="landlord_name" placeholder="Landlord"/></div>
      <div><label>File number</label><input id="file_no" placeholder="Case file #"/></div>
      <div><label>Hearing date</label><input id="hearing_date" placeholder="YYYY-MM-DD"/></div>
    </div>
    <label>Grounds (Ctrl/Cmd to select multiple)</label>
    <select id="grounds" multiple>
      <option>Habitability violations (§ 504B.161)</option>
      <option>Retaliation (§ 504B.225)</option>
      <option>Illegal lockout or utility shutoff (§ 504B.231)</option>
      <option>Breach of lease</option>
      <option>Improper notice/service</option>
      <option>Discrimination (FHA)</option>
      <option>VAWA survivor protection</option>
    </select>
    <label>Short facts</label>
    <textarea id="facts" rows="5" placeholder="Example: Heat out since Oct 10; notified landlord Oct 12 and Oct 20; no repairs."></textarea>
    <label>Requested relief</label>
    <textarea id="relief" rows="3" placeholder="Repairs by deadline; rent abatement; fees; case dismissed."></textarea>
    <label>Evidence items (one per line; e.g., 2025-10-12 Photo - living room leak)</label>
    <textarea id="evidence" rows="4" placeholder="YYYY-MM-DD Type - summary"></textarea>
    <div style="margin-top:12px;">
      <button onclick="generate()">Generate Answer + Counterclaim + Index</button>
      <span id="status" class="small"></span>
    </div>
  </div>

  <div class="card">
    <h3>Panels</h3>
    <button class="panel-btn" onclick="openPanel('/panel/state')">State law</button>
    <button class="panel-btn" onclick="openPanel('/panel/federal')">Federal protections</button>
    <button class="panel-btn" onclick="openPanel('/panel/funding')">Funding & assistance</button>
    <button class="panel-btn" onclick="openPanel('/panel/online')">Online court (Zoom)</button>
    <button class="panel-btn" onclick="openPanel('/panel/trial')">Trial scenarios (motions, evidence, appeals)</button>
    <button class="panel-btn" onclick="openPanel('/panel/procedures')">Courtroom procedures</button>
    <button class="panel-btn" onclick="openPanel('/panel/forms')">Official forms & rent escrow</button>
    <button class="panel-btn" onclick="openPanel('/panel/negotiation')">Negotiation playbook</button>
    <button class="panel-btn" onclick="openPanel('/panel/precedents')">Precedents overview</button>
  </div>

  <div class="card companion">
    <h3>Court Companion (live hearing helper)</h3>
    <div class="grid2">
      <div>
        <label>Quick objections</label>
        <select id="obj">
          <option>Objection, hearsay.</option>
          <option>Objection, lack of foundation.</option>
          <option>Objection, calls for speculation.</option>
          <option>Objection, relevance.</option>
        </select>
        <button onclick="copyText('obj')">Copy to clipboard</button>
      </div>
      <div>
        <label>Quick motions</label>
        <select id="mot">
          <option>Tenant requests a brief continuance to obtain counsel and complete exhibits.</option>
          <option>Tenant moves to dismiss for defective service/notice.</option>
          <option>Tenant requests repairs order, inspection, and rent abatement under § 504B.371.</option>
          <option>Tenant requests stay of writ pending disbursement of approved assistance.</option>
        </select>
        <button onclick="copyText('mot')">Copy to clipboard</button>
      </div>
      <div>
        <label>Zoom chat snippets</label>
        <select id="chat">
          <option>Tenant objects to improper service under Minn. Stat. § 504B.285.</option>
          <option>Tenant asserts habitability violations under § 504B.161 and requests remedies under § 504B.371.</option>
          <option>Tenant requests interpreter.</option>
          <option>Tenant requests breakout to confer privately.</option>
        </select>
        <button onclick="copyText('chat')">Copy to clipboard</button>
      </div>
      <div>
        <label>Statute navigator</label>
        <button onclick="window.open('/static/data/statute_navigator.json','_blank')">Open</button>
      </div>
    </div>
    <label>Live notes (save locally)</label>
    <textarea id="live_notes" rows="4" placeholder="Type notes during hearing..."></textarea>
    <div style="margin-top:8px;">
      <button onclick="saveNotes()">Save notes to file</button>
      <span id="note_status" class="small"></span>
    </div>
    <div style="margin-top:8px;">
      <button onclick="window.open('/static/court_helper/court_scripts.md','_blank')">Court scripts</button>
      <button onclick="window.open('/static/court_helper/court_checklist.md','_blank')">Court checklist</button>
    </div>
  </div>

  <div class="card">
    <h3>Tools</h3>
    <button onclick="window.open('/static/flows/deadline_flow.html','_blank')">Timeline</button>
    <button onclick="window.open('/static/flows/outcome_simulator.html','_blank')">Outcome simulator</button>
    <button onclick="window.open('/static/templates/motions_bundle.md','_blank')">Motion library</button>
    <button onclick="window.open('/static/assets/graphics/rights_infographic.svg','_blank')">Rights infographic</button>
    <button onclick="window.open('/static/assets/graphics/counterclaim_steps.svg','_blank')">Counterclaim steps</button>
    <button onclick="window.open('/static/README/README_eviction_defense.md','_blank')">README</button>
    <button onclick="window.open('/static/data/statute_navigator.json','_blank')">Statute navigator</button>
    <button onclick="window.open('/static/data/funding_resources.json','_blank')">Funding resources</button>
    <button onclick="window.open('/static/forms/forms_catalog.json','_blank')">Forms catalog</button>
  </div>

<script>
async function loadHelp(lang) {
  const res = await fetch('/help?lang=' + lang);
  if (!res.ok) return;
  const data = await res.json();
  const s = data.strings;
  document.getElementById('help-box').innerHTML = `
    <strong>${s.cta_counterclaim}</strong><br/>
    ${s.what_is_counterclaim}<br/>
    ${s.when_to_file}<br/>
    <em>${s.evidence_tip}</em><br/>
    <em>${s.timeline_tip}</em>`;
}

function openPanel(url) { window.open(url, '_blank'); }

async function generate() {
  const tenant_name = document.getElementById('tenant_name').value;
  const landlord_name = document.getElementById('landlord_name').value;
  const file_no = document.getElementById('file_no').value;
  const hearing_date = document.getElementById('hearing_date').value;
  const facts = document.getElementById('facts').value;
  const relief = document.getElementById('relief').value;
  const groundsSelect = document.getElementById('grounds');
  const grounds = Array.from(groundsSelect.selectedOptions).map(o => o.value);
  const evidence = document.getElementById('evidence').value.split('\\n').filter(x => x.trim().length > 0);

  const res = await fetch('/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ tenant_name, landlord_name, file_no, hearing_date, facts, relief, grounds, evidence })
  });
  const data = await res.json();
  document.getElementById('status').innerText = data.message || 'Generated';
}

function copyText(selectId) {
  const val = document.getElementById(selectId).value;
  navigator.clipboard.writeText(val);
}

async function saveNotes() {
  const notes = document.getElementById('live_notes').value;
  const res = await fetch('/notes', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ notes })
  });
  const data = await res.json();
  document.getElementById('note_status').innerText = data.message || 'Saved';
}
</script>
</body></html>
"""

# ======= Routes =======
@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML

@app.get("/help")
def help(lang: str = "en"):
    with open(PATHS["Help"] / "multilingual_help.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    strings = data["strings"].get(lang, data["strings"]["en"])
    return JSONResponse({"strings": strings})

@app.post("/generate")
def generate(payload: dict = Body(...)):
    tenant_name = payload.get("tenant_name", "").strip() or "[Your Name]"
    landlord_name = payload.get("landlord_name", "").strip() or "[Landlord Name]"
    file_no = payload.get("file_no", "").strip() or "[File No.]"
    hearing_date = payload.get("hearing_date", "").strip() or "[Hearing Date]"
    facts = payload.get("facts", "").strip() or "[Facts]"
    relief = payload.get("relief", "").strip() or "[Relief]"
    grounds: List[str] = payload.get("grounds", []) or []
    evidence: List[str] = payload.get("evidence", []) or []

    answer_out = f"""# Eviction answer (Dakota County)

**Case caption:** District Court, Dakota County, Housing
**Defendant/Tenant:** {tenant_name}
**Plaintiff/Landlord:** {landlord_name}
**File No.:** {file_no}
**Hearing Date:** {hearing_date}

**Admissions/Denials:**
- **General denial:** Tenant denies allegations not specifically admitted.

**Defenses selected:**
""" + "".join([f"- **{g}:** {facts}\n" for g in grounds]) + f"""

**Relief requested:**
- {relief}
"""

    cc_out = f"""# Counterclaim (Dakota County)

**Parties:** Tenant counterclaims against Landlord in this eviction case.

**Grounds selected:**
""" + "".join([f"- {g}\n" for g in grounds]) + f"""
**Facts:** {facts}

**Evidence:** See evidence_index_{TODAY}.md

**Relief requested:** {relief}
"""

    evidence_lines = "\n".join([f"- **Item:** {line}" for line in evidence]) or "- **Item:** [List items]"
    ev_out = f"""# Evidence index

**Case:** {file_no}
**Tenant:** {tenant_name}

**Items:**
{evidence_lines}
"""

    write_file(PATHS["Templates"] / f"answer_generated_{TODAY}.md", answer_out)
    write_file(PATHS["Templates"] / f"counterclaim_generated_{TODAY}.md", cc_out)
    write_file(PATHS["Public"] / f"evidence_index_{TODAY}.md", ev_out)
    create_checkpoint_zip()
    return JSONResponse({"message": f"Generated. Files saved and checkpoint at {CHECKPOINT_ZIP.name}."})

@app.post("/notes")
def save_notes(payload: Dict = Body(...)):
    notes = payload.get("notes", "")
    write_file(PATHS["Court"] / f"live_notes_{TODAY}.md", notes or "[No notes]")
    create_checkpoint_zip()
    return JSONResponse({"message": "Notes saved and checkpoint updated."})

# ======= Panels =======
@app.get("/panel/state", response_class=HTMLResponse)
def panel_state():
    return """<!doctype html><html><head><meta charset="utf-8"><title>State law</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Minnesota state law (eviction)</h2>
<div class="item"><strong>Chapter 504B overview:</strong> Grounds, notice, complaint, summons, hearing, judgment.</div>
<div class="item"><strong>Key defenses:</strong> Improper notice/service; habitability (§ 504B.161); retaliation (§ 504B.225); illegal lockout/utility shutoff (§ 504B.231).</div>
<div class="item"><strong>Tenant Remedies (§ 504B.371):</strong> Repairs, inspections, rent abatement when covenants are violated.</div>
<div class="item"><strong>Timing:</strong> Summons typically sets hearing within 7–14 days; answer/counterclaims raised by first hearing.</div>
<a href="/static/data/statute_navigator.json" target="_blank">Open Statute Navigator</a>
</body></html>"""

@app.get("/panel/federal", response_class=HTMLResponse)
def panel_federal():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Federal protections</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Federal protections</h2>
<div class="item"><strong>Fair Housing Act:</strong> Bars discriminatory eviction (race, color, religion, sex, disability, familial status, national origin).</div>
<div class="item"><strong>VAWA:</strong> Protects survivors in federally subsidized housing from eviction due to abuse; enables emergency transfers.</div>
<div class="item"><strong>Constitutional due process:</strong> Notice and fair opportunity to be heard before deprivation of housing.</div>
<div class="item"><strong>Intersection:</strong> Use federal defenses alongside state claims (e.g., habitability + FHA).</div>
<a href="/static/data/statute_navigator.json" target="_blank">Open Statute Navigator</a>
</body></html>"""

@app.get("/panel/funding", response_class=HTMLResponse)
def panel_funding():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Funding & assistance</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Funding & assistance</h2>
<div class="item"><strong>Programs:</strong> ERA (RentHelpMN, as available), CoC, ESG, MN Housing Trust Fund.</div>
<div class="item"><strong>Proof for court:</strong> Applications, award letters, emails, portal screenshots.</div>
<div class="item"><strong>Motions:</strong> Request continuance or stay of writ based on pending/approved assistance.</div>
<div class="item"><strong>Negotiation:</strong> Ask landlord to accept funds and stipulate to dismissal upon payment.</div>
<a href="/static/data/funding_resources.json" target="_blank">Open Funding Resources</a>
</body></html>"""

@app.get("/panel/online", response_class=HTMLResponse)
def panel_online():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Online court (Zoom)</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Online court (Zoom) procedures</h2>
<div class="item"><strong>Join & identify:</strong> Log in early; rename to 'First Last — Tenant'; enable video if possible.</div>
<div class="item"><strong>Exhibits:</strong> Keep files ready; share screen when permitted; follow digital exhibit guidance.</div>
<div class="item"><strong>Etiquette:</strong> Mute when not speaking; wait to be recognized; no recording.</div>
<div class="item"><strong>Requests:</strong> Ask for breakout to confer, continuance to gather evidence, or interpreter if needed.</div>
<a href="/static/flows/deadline_flow.html" target="_blank">Open Timeline</a> •
<a href="/static/flows/outcome_simulator.html" target="_blank">Open Outcome Simulator</a>
</body></html>"""

@app.get("/panel/trial", response_class=HTMLResponse)
def panel_trial():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Trial scenarios</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px} .code{background:#f7f7f7;padding:8px;border-radius:6px}</style></head><body>
<h2>Trial scenarios: motions, evidence, appeals</h2>

<h3>Common motions</h3>
<div class="item"><strong>Continuance:</strong> “Tenant requests a brief continuance to obtain counsel and complete exhibits.”</div>
<div class="item"><strong>Dismissal (service/notice):</strong> “Tenant moves to dismiss for defective service/notice prejudicing due process.”</div>
<div class="item"><strong>Tenant Remedies:</strong> “Tenant requests repairs order, inspection, and rent abatement under § 504B.371.”</div>
<div class="item"><strong>Stay writ for funding:</strong> “Tenant requests stay of writ pending disbursement of approved assistance.”</div>

<h3>Evidence practice</h3>
<div class="item"><strong>Foundation:</strong> Identify, date, and describe each exhibit; explain relevance (heat outage, leaks, retaliation).</div>
<div class="item"><strong>Witnesses:</strong> Direct: who/what/when/how; Cross: inconsistencies, notice given, repairs delayed.</div>
<div class="item"><strong>Exhibit list:</strong> Keep an index and mark each item clearly; provide copies to the other side.</div>

<h3>Appeals & post-judgment</h3>
<div class="item"><strong>Appeal rights:</strong> Consider appeal if legal error or due process concerns; note deadlines and bond issues.</div>
<div class="item"><strong>Writ and enforcement:</strong> Only the court can issue a writ of recovery; self-help lockouts are prohibited.</div>

<div class="item code">Quick script (say aloud):<br/>
“Your Honor, Tenant asserts habitability violations under § 504B.161 and requests remedies under § 504B.371, including repairs and rent abatement. Tenant also moves to dismiss for defective notice and, alternatively, to continue to finalize funding.”</div>

<a href="/static/templates/motions_bundle.md" target="_blank">Open Motion Library</a> •
<a href="/static/public/evidence_index.md" target="_blank">Open Evidence Index Template</a>
</body></html>"""

@app.get("/panel/procedures", response_class=HTMLResponse)
def panel_procedures():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Courtroom procedures</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Courtroom procedures (Minnesota eviction)</h2>
<div class="item"><strong>Filing:</strong> Landlord files complaint; court issues summons with hearing date.</div>
<div class="item"><strong>Service:</strong> Summons must be properly served before hearing; defective service can be grounds to dismiss.</div>
<div class="item"><strong>Answer & counterclaims:</strong> Raise defenses and counterclaims in writing or at the first hearing.</div>
<div class="item"><strong>Hearing & trial:</strong> Present evidence; examine witnesses; make motions; seek remedies.</div>
<div class="item"><strong>Judgment & writ:</strong> If eviction granted, enforcement by writ; illegal lockouts are prohibited.</div>
</body></html>"""

@app.get("/panel/forms", response_class=HTMLResponse)
def panel_forms():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Official forms & rent escrow</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Official forms & rent escrow</h2>
<div class="item"><strong>Use Judicial Branch forms:</strong> Eviction Answer, Counterclaim, Rent Escrow, Expungement, Appeals.</div>
<div class="item"><strong>Rent Escrow (Minn. Stat. § 504B.385):</strong> Deposit rent with court to request repairs/abatement.</div>
<div class="item"><strong>Counterclaim form:</strong> Counterclaim for Possession of Premises & Notice of Hearing (housing cases).</div>
<div class="item"><strong>Catalog:</strong> Open the forms catalog JSON and click the official links.</div>
<a href="/static/forms/forms_catalog.json" target="_blank">Open Forms Catalog</a>
</body></html>"""

@app.get("/panel/negotiation", response_class=HTMLResponse)
def panel_negotiation():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Negotiation playbook</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px} .code{background:#f7f7f7;padding:8px;border-radius:6px}</style></head><body>
<h2>Negotiation playbook</h2>
<div class="item"><strong>Stipulations:</strong> Dismissal upon payment via assistance; repair lists with deadlines and abatements.</div>
<div class="item"><strong>Funding leverage:</strong> Provide proof of ERA/CoC/ESG; seek continuance or stay pending disbursement.</div>
<div class="item"><strong>Payment plans:</strong> Structured repayment monitored by court; add remedies for repairs.</div>
<div class="item code">Script:<br/>“We propose dismissal conditioned on assistance payment. Repairs completed by [date]; rent abated until completion.”</div>
</body></html>"""

@app.get("/panel/precedents", response_class=HTMLResponse)
def panel_precedents():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Precedents overview</title>
<style>body{font-family:system-ui,Arial;margin:24px;max-width:900px}.item{margin-bottom:12px}</style></head><body>
<h2>Precedents overview (guidance)</h2>
<div class="item"><strong>Habitability defenses:</strong> Minnesota courts recognize rent abatement and repairs where covenants are violated.</div>
<div class="item"><strong>Due process & service:</strong> Defective notice/service can bar eviction; tenants may seek dismissal.</div>
<div class="item"><strong>Anti-discrimination:</strong> FHA claims can be raised alongside state defenses; retaliation is prohibited.</div>
<div class="item"><strong>Practice tip:</strong> Cite statutes and attach exhibits; request specific remedies and timelines.</div>
</body></html>"""

# ======= Main =======
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

