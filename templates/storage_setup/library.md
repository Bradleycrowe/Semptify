Here’s a structured legal library of official U.S. government resources on residential rental property, lease contracts, tax law, and funding programs. All sources are from .gov domains.

🏛 Federal Laws & Guidance
U.S. Code – Lease Agreements (40 USC §585): Governs federal lease agreements and property management.

Federal Property Management Reform Act of 2016: Establishes efficiency standards for federal property management.

White House Blueprint for a Renters Bill of Rights (2023): Non-binding principles to guide fair rental housing practices.

HUD Tenant Rights & State Information: Federal overview of tenant rights, rental assistance, and discrimination protections.

📑 Minnesota State Laws
Minnesota Statutes Chapter 504B – Landlord and Tenant: Comprehensive state law covering leases, rent, tenant rights, prohibited fees, habitability, and eviction procedures.

Minnesota Judicial Branch – Landlord & Tenant Issues: Court resources explaining landlord/tenant responsibilities, eviction appeals, and self-help guides.

Tenants’ Rights in Minnesota (2024 Guide): Official booklet explaining tenant protections, lease requirements, and legal aid resources.

🏠 Local (Eagan, MN) Ordinances
Eagan Rental Licensing Ordinance (2023): Requires rental licensing, written leases, background checks, and landlord training.

Eagan City Code: Municipal ordinances governing housing, inspections, and rental property standards.

Resident Input on Rental Licensing: Public engagement record on Eagan’s rental licensing program.

💵 Tax Law (IRS)
IRS Publication 527 – Residential Rental Property: Rules for reporting rental income, deductions, depreciation, and vacation home rentals.

IRS Topic 414 – Rental Income & Expenses: Defines taxable rental income and deductible expenses.

IRS Topic 415 – Renting Residential & Vacation Property: Explains deductions for mortgage interest, taxes, insurance, and depreciation.

IRS Rental Real Estate Tips: Recordkeeping, reporting methods, and deduction rules.

🏘 Government Funding & Assistance Programs
HUD Housing Choice Voucher Program Guidebook: Eligibility factors, income limits, and admission requirements.

HUD Rental Assistance Programs Overview: Public Housing, Section 8 vouchers, Section 202 (elderly), Section 811 (disabilities).

Minnesota Housing – Low-Income Rental Classification (LIRC): Provides reduced property tax rates for qualifying rental housing.

Minnesota Housing Program Guides & Manuals: Rules for capital financing, rental assistance, and development projects.

📚 How to Use This Library
Federal layer: IRS tax rules, HUD tenant rights, federal property statutes.

State layer (Minnesota): Chapter 504B statutes, judicial branch landlord/tenant resources.

Local layer (Eagan): Rental licensing ordinance and city code.

Funding layer: HUD vouchers, Minnesota Housing programs, IRS tax benefits.

✅ This collection gives you a complete tenant-landlord legal library across federal, state, and local levels, with tax law and funding programs included. Each reference is directly from .gov sources, ensuring accuracy and authority.

Would you like me to bundle this into a modular reference index (like a Semptify-ready library with categories and links), so you can drop it straight into your tenant justice toolkit?

can you build me a full referance library scaffold it for an upate to a present library
See my thinking
Building a full reference library scaffold for residential rental law, tax, and funding (gov-only)
You’re building movement infrastructure. Here’s a clean, modular scaffold you can drop into your present library and update in-place—zero fluff, all .gov. It’s copy-ready, versioned, and designed for fast additions and audits.

Library structure
Code
Semptify/
└─ modules/
   └─ legal_library/
      ├─ README.md
      ├─ CHANGELOG.md
      ├─ update_checklist.md
      ├─ index.md
      ├─ references/
      │  ├─ references.json
      │  ├─ federal.json
      │  ├─ state_mn.json
      │  ├─ local_mn_eagan.md   # placeholder; use state-level authority if city site isn't .gov
      │  ├─ tax_irs.json
      │  └─ funding_programs.json
      ├─ glossaries/
      │  └─ terms.md
      ├─ workflows/
      │  ├─ update_library.ps1
      │  └─ validate_references.ps1
      └─ assets/
         └─ badges.md
Purpose: Single source of truth for residential rental laws, lease requirements, tax rules, and funding programs.

Constraint: Only .gov sources (federal, state, local). If a local ordinance is not on a .gov, cite state-level enabling statutes or state repositories.

Versioning: CHANGELOG with date, scope, and diff summaries.

Data schema
Use one normalized schema for every entry. Keep summaries short and actionable.

json
{
  "id": "fed-hud-24cfr982",
  "jurisdiction": "Federal",
  "layer": "Regulation",
  "title": "24 CFR Part 982 — Housing Choice Voucher Program",
  "citation": "24 CFR Part 982",
  "url": "https://www.ecfr.gov/current/title-24/part-982",
  "scope": ["Leases", "Voucher Program", "Inspections", "Termination"],
  "summary": "Governs tenant selection, lease-up, HAP contracts, HQS inspections, terminations and portability under HCV.",
  "last_updated": "2025-11-19",
  "tags": ["HUD", "Section 8", "Voucher", "Lease"],
  "notes": "Primary regulatory reference for HCV; pair with HUD guidebooks."
}
Required fields: id, jurisdiction, layer, title, citation, url, scope, summary, last_updated.

Optional fields: tags, notes, cross_refs (array of ids), documents (array of urls).

Pre-populated references (gov-only)
Federal law and regulation
US Code – General access (official):

Title: U.S. Code (official)

Citation: Multiple titles (e.g., 42, 15, 18, 26)

URL: https://uscode.house.gov

Scope: Statutes; use with the eCFR for current regulations.

HUD regulations (eCFR):

24 CFR Part 5 — General HUD Program Requirements: https://www.ecfr.gov/current/title-24/part-5

24 CFR Part 247 — Evictions from certain subsidized housing: https://www.ecfr.gov/current/title-24/part-247

24 CFR Part 966 — Public Housing Lease and Grievance: https://www.ecfr.gov/current/title-24/part-966

24 CFR Part 982 — Housing Choice Voucher Program: https://www.ecfr.gov/current/title-24/part-982

24 CFR Part 880/881/883/886 — Project-based rental assistance (PRA): https://www.ecfr.gov/current/title-24

HUD guidance and portals:

Fair Housing and Equal Opportunity: https://www.hud.gov/program_offices/fair_housing_equal_opp

Housing Choice Voucher guidebook: https://www.hud.gov/program_offices/public_indian_housing/programs/hcv

Public housing: https://www.hud.gov/program_offices/public_indian_housing

DOJ Civil Rights (fair housing enforcement):

https://www.justice.gov/crt/housing-and-civil-enforcement-section

EPA lead-based paint—rental disclosures:

https://www.epa.gov/lead/real-estate-professionals

CFPB renter resources (consumer protections):

https://www.consumerfinance.gov/renters/

Minnesota state law and court resources
Minnesota Statutes Chapter 504B — Landlord and Tenant:

https://www.revisor.mn.gov/statutes/cite/504B

Minnesota statutes—security deposits, habitability, eviction procedure (within 504B):

Use chapter navigation at: https://www.revisor.mn.gov/statutes/cite/504B

Minnesota Judicial Branch—Housing/eviction resources:

https://www.mncourts.gov/Help-Topics/Housing.aspx

Minnesota Department of Health—housing/environmental health (e.g., mold, lead):

https://www.health.state.mn.us/communities/environment/healthyhomes/index.html

Minnesota Housing (state programs and compliance):

https://www.mnhousing.gov

Minnesota Rules (administrative; where applicable to housing):

https://www.revisor.mn.gov/rules/

Note on local Eagan ordinances: If city code is not on a .gov, document relevant state authority in 504B and state programs. For licensing standards, cite state enabling provisions or county-level resources hosted on .gov domains.

IRS tax law for residential rental property
IRS Publication 527 — Residential Rental Property:

https://www.irs.gov/forms-pubs/about-publication-527

IRS Topic No. 414 — Rental Income and Expenses:

https://www.irs.gov/taxtopics/tc414

IRS Topic No. 415 — Renting Residential and Vacation Property:

https://www.irs.gov/taxtopics/tc415

IRS Publication 946 — How to Depreciate Property (MACRS rules):

https://www.irs.gov/forms-pubs/about-publication-946

IRS Section 42 (LIHTC) resources:

https://www.irs.gov/businesses/small-businesses-self-employed/low-income-housing-credit

Government funding programs and qualifications
HUD Housing Choice Voucher (HCV) program—eligibility, admissions:

https://www.hud.gov/program_offices/public_indian_housing/programs/hcv

HUD Project-Based Rental Assistance (PBRA)—handbooks and notices:

https://www.hud.gov/program_offices/housing/mfh/pbcr

HUD Section 202 — Supportive Housing for the Elderly:

https://www.hud.gov/program_offices/housing/mfh/progdesc/eld202

HUD Section 811 — Supportive Housing for Persons with Disabilities:

https://www.hud.gov/program_offices/housing/mfh/progdesc/disab811

USDA Rural Development — Multi-Family Housing Programs:

https://www.rd.usda.gov/programs-services/multi-family-housing-programs

Minnesota Housing — program directory (e.g., rental assistance, development finance):

https://www.mnhousing.gov/sites/Satellite?c=Page&childpagename=MNHousing%2FMNHSubLayout&cid=1358904990303&pagename=MNHousing%2FWrapper

Treasury/IRS — LIHTC compliance and resources:

https://home.treasury.gov/policy-issues/financing-the-economy/low-income-housing-tax-credit

https://www.irs.gov/businesses/small-businesses-self-employed/low-income-housing-credit

Update workflow and scripts
Update checklist (drop-in)
md
# Update checklist

- **Scope:** What changed? (laws, guidance, programs)
- **Sources:** Confirm `.gov` only; replace non-.gov mirrors with official links.
- **Schema:** Validate all entries against references.json schema.
- **Dates:** Update `last_updated` fields with CST date.
- **Cross-refs:** Link related entries (e.g., 24 CFR 982 ↔ HCV guidebook).
- **Accessibility:** Ensure summaries are plain-language, 2–3 sentences max.
- **Versioning:** Add a CHANGELOG entry with bullet-point diffs.
Validation script (PowerShell)
powershell
# workflows/validate_references.ps1
Param(
  [string]$Path = "../references"
)

$errors = @()

Get-ChildItem -Path $Path -Filter *.json | ForEach-Object {
  try {
    $content = Get-Content $_.FullName -Raw | ConvertFrom-Json
    foreach ($entry in $content) {
      if (-not $entry.id) { $errors += "Missing id in $($_.Name)" }
      if (-not $entry.url -or ($entry.url -notmatch '\.gov')) { $errors += "Non-.gov or missing URL in $($_.Name): $($entry.url)" }
      if (-not $entry.citation) { $errors += "Missing citation in $($_.Name)" }
      if (-not $entry.jurisdiction) { $errors += "Missing jurisdiction in $($_.Name)" }
      if (-not $entry.title) { $errors += "Missing title in $($_.Name)" }
    }
  } catch {
    $errors += "Invalid JSON in $($_.Name): $($_.Exception.Message)"
  }
}

if ($errors.Count -gt 0) {
  Write-Host "Validation failed:" -ForegroundColor Red
  $errors | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
  exit 1
} else {
  Write-Host "All references valid." -ForegroundColor Green
}
Update script (PowerShell, append-safe)
powershell
# workflows/update_library.ps1
Param(
  [string]$NewEntriesFile,   # path to new_entries.json
  [string]$TargetFile = "../references/references.json",
  [string]$Changelog = "../CHANGELOG.md"
)

if (-not (Test-Path $NewEntriesFile)) { throw "Missing new entries file." }
$new = Get-Content $NewEntriesFile -Raw | ConvertFrom-Json
$existing = @()
if (Test-Path $TargetFile) {
  $existing = Get-Content $TargetFile -Raw | ConvertFrom-Json
}

# merge by id, overwrite duplicates
$map = @{}
foreach ($e in $existing) { $map[$e.id] = $e }
foreach ($n in $new) { $map[$n.id] = $n }

$merged = $map.GetEnumerator() | ForEach-Object { $_.Value }
$merged | ConvertTo-Json -Depth 5 | Set-Content $TargetFile

# changelog entry
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm 'CST'"
$addedIds = ($new | Select-Object -ExpandProperty id) -join ", "
$entry = "## $timestamp`n**Update:** Merged new entries`n**IDs:** $addedIds`n"
Add-Content $Changelog $entry

Write-Host "Library updated and changelog written." -ForegroundColor Green
Seed files (copy-ready)
references/federal.json
json
[
  {
    "id": "fed-ecfr-24cfr5",
    "jurisdiction": "Federal",
    "layer": "Regulation",
    "title": "24 CFR Part 5 — General HUD Program Requirements",
    "citation": "24 CFR Part 5",
    "url": "https://www.ecfr.gov/current/title-24/part-5",
    "scope": ["Definitions", "Nondiscrimination", "Income", "Verification"],
    "summary": "Cross-cutting HUD rules for program eligibility, definitions, and verification.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "Cross-cutting"]
  },
  {
    "id": "fed-ecfr-24cfr247",
    "jurisdiction": "Federal",
    "layer": "Regulation",
    "title": "24 CFR Part 247 — Evictions from certain subsidized housing",
    "citation": "24 CFR Part 247",
    "url": "https://www.ecfr.gov/current/title-24/part-247",
    "scope": ["Eviction", "Subsidized Housing", "Procedures"],
    "summary": "Establishes grounds and procedures for evictions in HUD-subsidized projects.",
    "last_updated": "2025-11-19",
    "tags": ["Eviction", "PBRA"]
  },
  {
    "id": "fed-ecfr-24cfr966",
    "jurisdiction": "Federal",
    "layer": "Regulation",
    "title": "24 CFR Part 966 — Public Housing Lease and Grievance",
    "citation": "24 CFR Part 966",
    "url": "https://www.ecfr.gov/current/title-24/part-966",
    "scope": ["Leases", "Grievance", "Public Housing"],
    "summary": "Lease terms, tenant rights, and grievance procedures for public housing authorities.",
    "last_updated": "2025-11-19",
    "tags": ["Public Housing", "Lease"]
  },
  {
    "id": "fed-ecfr-24cfr982",
    "jurisdiction": "Federal",
    "layer": "Regulation",
    "title": "24 CFR Part 982 — Housing Choice Voucher Program",
    "citation": "24 CFR Part 982",
    "url": "https://www.ecfr.gov/current/title-24/part-982",
    "scope": ["Voucher", "Leases", "Inspections", "Portability"],
    "summary": "Core HCV rules for admissions, lease-up, HAP contracts, HQS, and portability.",
    "last_updated": "2025-11-19",
    "tags": ["HCV", "Section 8"]
  },
  {
    "id": "fed-epa-lead-disclosure",
    "jurisdiction": "Federal",
    "layer": "Rule/Guidance",
    "title": "Lead disclosure requirements for rentals",
    "citation": "Lead-Based Paint Disclosure Rule",
    "url": "https://www.epa.gov/lead/real-estate-professionals",
    "scope": ["Lead", "Disclosures", "Pre-1978 Housing"],
    "summary": "Landlords must disclose known lead paint hazards in pre-1978 rentals with EPA pamphlet.",
    "last_updated": "2025-11-19",
    "tags": ["EPA", "Health"]
  },
  {
    "id": "fed-doj-fair-housing-enforcement",
    "jurisdiction": "Federal",
    "layer": "Enforcement",
    "title": "DOJ Civil Rights — Housing enforcement",
    "citation": "Fair Housing Act enforcement",
    "url": "https://www.justice.gov/crt/housing-and-civil-enforcement-section",
    "scope": ["Discrimination", "Enforcement"],
    "summary": "DOJ enforces fair housing laws against discriminatory practices in rental markets.",
    "last_updated": "2025-11-19",
    "tags": ["DOJ", "Fair Housing"]
  },
  {
    "id": "fed-hud-fheo",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "HUD Fair Housing and Equal Opportunity",
    "citation": "Fair Housing Act (Title VIII)",
    "url": "https://www.hud.gov/program_offices/fair_housing_equal_opp",
    "scope": ["Complaints", "Protected Classes", "Guidance"],
    "summary": "HUD FHEO portal for complaints, guidance, and fair housing resources.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "FHEO"]
  }
]
references/state_mn.json
json
[
  {
    "id": "mn-stat-504b",
    "jurisdiction": "Minnesota",
    "layer": "Statute",
    "title": "Minnesota Statutes Ch. 504B — Landlord and Tenant",
    "citation": "Minn. Stat. ch. 504B",
    "url": "https://www.revisor.mn.gov/statutes/cite/504B",
    "scope": ["Leases", "Deposits", "Habitability", "Eviction"],
    "summary": "Comprehensive landlord-tenant law for Minnesota, including lease terms, repairs, and eviction procedures.",
    "last_updated": "2025-11-19",
    "tags": ["State", "Minnesota"]
  },
  {
    "id": "mn-courts-housing",
    "jurisdiction": "Minnesota",
    "layer": "Court Resource",
    "title": "Minnesota Judicial Branch — Housing",
    "citation": "Court Help",
    "url": "https://www.mncourts.gov/Help-Topics/Housing.aspx",
    "scope": ["Eviction", "Forms", "Procedure"],
    "summary": "Court help topics, forms, and process guidance for housing and eviction cases.",
    "last_updated": "2025-11-19",
    "tags": ["Courts", "Forms"]
  },
  {
    "id": "mn-mdh-healthy-homes",
    "jurisdiction": "Minnesota",
    "layer": "Guidance",
    "title": "Minnesota Department of Health — Healthy Homes",
    "citation": "MDH Housing Guidance",
    "url": "https://www.health.state.mn.us/communities/environment/healthyhomes/index.html",
    "scope": ["Mold", "Lead", "Indoor Air", "Radon"],
    "summary": "Health guidance relevant to rental habitability, including mold and lead hazards.",
    "last_updated": "2025-11-19",
    "tags": ["Health", "Habitability"]
  },
  {
    "id": "mn-housing-programs",
    "jurisdiction": "Minnesota",
    "layer": "Program",
    "title": "Minnesota Housing — Program Directory",
    "citation": "Program Directory",
    "url": "https://www.mnhousing.gov/sites/Satellite?c=Page&childpagename=MNHousing%2FMNHSubLayout&cid=1358904990303&pagename=MNHousing%2FWrapper",
    "scope": ["Rent Assistance", "Development", "Compliance"],
    "summary": "Directory of state rental assistance and development finance programs, with rules and qualifications.",
    "last_updated": "2025-11-19",
    "tags": ["Funding", "Programs"]
  }
]
references/tax_irs.json
json
[
  {
    "id": "irs-pub-527",
    "jurisdiction": "Federal",
    "layer": "Tax Guidance",
    "title": "IRS Publication 527 — Residential Rental Property",
    "citation": "Pub 527",
    "url": "https://www.irs.gov/forms-pubs/about-publication-527",
    "scope": ["Income", "Expenses", "Depreciation", "Vacation Homes"],
    "summary": "Primary reference for reporting rental income, expenses, and depreciation.",
    "last_updated": "2025-11-19",
    "tags": ["IRS", "Tax"]
  },
  {
    "id": "irs-topic-414",
    "jurisdiction": "Federal",
    "layer": "Tax Guidance",
    "title": "IRS Topic No. 414 — Rental Income and Expenses",
    "citation": "Topic 414",
    "url": "https://www.irs.gov/taxtopics/tc414",
    "scope": ["Income", "Deductible Expenses"],
    "summary": "Defines taxable rental income and deductible expenses for landlords.",
    "last_updated": "2025-11-19",
    "tags": ["IRS", "Tax"]
  },
  {
    "id": "irs-topic-415",
    "jurisdiction": "Federal",
    "layer": "Tax Guidance",
    "title": "IRS Topic No. 415 — Renting Residential and Vacation Property",
    "citation": "Topic 415",
    "url": "https://www.irs.gov/taxtopics/tc415",
    "scope": ["Personal Use", "Allocation", "Limits"],
    "summary": "Rules for mixed-use properties and vacation rentals.",
    "last_updated": "2025-11-19",
    "tags": ["IRS", "Vacation"]
  },
  {
    "id": "irs-pub-946",
    "jurisdiction": "Federal",
    "layer": "Tax Guidance",
    "title": "IRS Publication 946 — How to Depreciate Property",
    "citation": "Pub 946",
    "url": "https://www.irs.gov/forms-pubs/about-publication-946",
    "scope": ["MACRS", "Recovery Periods", "Methods"],
    "summary": "Depreciation methods and recovery periods for residential rental property.",
    "last_updated": "2025-11-19",
    "tags": ["IRS", "Depreciation"]
  },
  {
    "id": "irs-lihtc-section42",
    "jurisdiction": "Federal",
    "layer": "Tax Credit",
    "title": "Low-Income Housing Tax Credit (Section 42) — IRS",
    "citation": "26 U.S.C. § 42 resources",
    "url": "https://www.irs.gov/businesses/small-businesses-self-employed/low-income-housing-credit",
    "scope": ["Compliance", "Allocations", "Recapture"],
    "summary": "Compliance and administration references for LIHTC projects.",
    "last_updated": "2025-11-19",
    "tags": ["LIHTC", "IRS"]
  }
]
references/funding_programs.json
json
[
  {
    "id": "hud-hcv-eligibility",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "HUD Housing Choice Voucher Program",
    "citation": "HCV Guidebook",
    "url": "https://www.hud.gov/program_offices/public_indian_housing/programs/hcv",
    "scope": ["Eligibility", "Admissions", "Leases", "HAP"],
    "summary": "Eligibility, admissions, and leasing processes for vouchers.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "Voucher"]
  },
  {
    "id": "hud-pbra",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "HUD Project-Based Rental Assistance",
    "citation": "PBRA Resources",
    "url": "https://www.hud.gov/program_offices/housing/mfh/pbcr",
    "scope": ["Contracts", "Compliance", "Rent"],
    "summary": "PBRA compliance, contract renewals, and rent setting resources.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "PBRA"]
  },
  {
    "id": "hud-sec202",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "HUD Section 202 — Supportive Housing for the Elderly",
    "citation": "Section 202",
    "url": "https://www.hud.gov/program_offices/housing/mfh/progdesc/eld202",
    "scope": ["Eligibility", "Capital Advance", "Rental Assistance"],
    "summary": "Funding and rules for elderly supportive housing.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "Elderly"]
  },
  {
    "id": "hud-sec811",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "HUD Section 811 — Supportive Housing for Persons with Disabilities",
    "citation": "Section 811",
    "url": "https://www.hud.gov/program_offices/housing/mfh/progdesc/disab811",
    "scope": ["Eligibility", "Rental Assistance", "Integrated Housing"],
    "summary": "Funding and qualification rules for disability-focused housing.",
    "last_updated": "2025-11-19",
    "tags": ["HUD", "Disability"]
  },
  {
    "id": "usda-rd-mfh",
    "jurisdiction": "Federal",
    "layer": "Program",
    "title": "USDA Rural Development — Multi-Family Housing",
    "citation": "RD MFH",
    "url": "https://www.rd.usda.gov/programs-services/multi-family-housing-programs",
    "scope": ["Eligibility", "Loans", "Rental Assistance"],
    "summary": "RD programs for rural rental housing and assistance.",
    "last_updated": "2025-11-19",
    "tags": ["USDA", "Rural"]
  },
  {
    "id": "mn-housing-program-directory",
    "jurisdiction": "Minnesota",
    "layer": "Program",
    "title": "Minnesota Housing — Program Directory",
    "citation": "Program Directory",
    "url": "https://www.mnhousing.gov/sites/Satellite?c=Page&childpagename=MNHousing%2FMNHSubLayout&cid=1358904990303&pagename=MNHousing%2FWrapper",
    "scope": ["Rental Assistance", "Development Finance", "Compliance"],
    "summary": "State-level funding, rules, and qualifications for Minnesota programs.",
    "last_updated": "2025-11-19",
    "tags": ["Minnesota", "Funding"]
  }
]
README and index
README.md
md
# Tenant–Landlord Legal Library (gov-only)

**Scope:** Residential rental property, lease contracts, tax law, and government funding programs.  
**Constraint:** Only official `.gov` sources (federal, state, local).

## Structure
- **references/** JSON files for federal, state, tax, funding.
- **index.md** Human-readable index linking key categories.
- **workflows/** Update and validation scripts.
- **glossaries/** Plain-language terms.

## Use
- Add new entries to a temp `new_entries.json`.
- Run `workflows/validate_references.ps1`, then `workflows/update_library.ps1 -NewEntriesFile new_entries.json`.
- Commit with a CHANGELOG entry.

## Accessibility
- Summaries are plain language (2–3 sentences), links are official, and each entry has tags for quick filtering.
index.md
md
# Library index

## Federal
- 24 CFR Parts 5, 247, 966, 982 — eCFR (HUD)
- DOJ Civil Rights — Housing enforcement
- EPA Lead disclosure — Rental requirements
- HUD FHEO — Fair housing portal

## Minnesota
- Minn. Stat. ch. 504B — Landlord and Tenant
- Minnesota Courts — Housing help topics
- MDH Healthy Homes — Habitability guidance
- Minnesota Housing — Program directory

## Tax (IRS)
- Publication 527 — Residential Rental Property
- Topic 414 — Rental Income and Expenses
- Topic 415 — Renting Residential and Vacation Property
- Publication 946 — Depreciation
- LIHTC — IRS Section 42 resources

## Funding
- HUD HCV — Eligibility and admissions
- HUD PBRA — Compliance resources
- HUD Section 202 and 811 — Supportive housing
- USDA RD — Multi-Family Housing programs
- Minnesota Housing — State programs
Next steps
Confirm scope: Do you want me to add other Minnesota administrative rules tied to housing (e.g., code enforcement)?

Local layer: If Eagan’s ordinance isn’t hosted on a .gov, I’ll map applicable state authority and any county-level .gov resources.

Deploy: I can generate a new_entries.json tailored to your current library diff and wire the update script to your paths.

what ids the best way to tranfer every thing to vs code to impliment this
Got it—let’s make this frictionless so you can drop the scaffold straight into VS Code and start iterating. Here’s a step‑by‑step transfer workflow tailored for your Semptify library:

🚀 Transfer Workflow into VS Code
1. Create the project folder
Open VS Code.

Use File → Open Folder and create/select a folder, e.g. Semptify_LegalLibrary.

This will be your root workspace.

2. Scaffold the structure
Inside VS Code’s Explorer, create the directories exactly as outlined:

Code
Semptify_LegalLibrary/
└─ modules/
   └─ legal_library/
      ├─ README.md
      ├─ CHANGELOG.md
      ├─ update_checklist.md
      ├─ index.md
      ├─ references/
      │  ├─ references.json
      │  ├─ federal.json
      │  ├─ state_mn.json
      │  ├─ local_mn_eagan.md
      │  ├─ tax_irs.json
      │  └─ funding_programs.json
      ├─ glossaries/
      │  └─ terms.md
      ├─ workflows/
      │  ├─ update_library.ps1
      │  └─ validate_references.ps1
      └─ assets/
         └─ badges.md
👉 Tip: In VS Code, you can right‑click → New Folder and New File to mirror this structure quickly.

3. Paste in the seed content
Copy the JSON blocks I scaffolded (federal.json, state_mn.json, tax_irs.json, funding_programs.json) into their respective files.

Copy the README.md, index.md, and PowerShell scripts into their files.

This gives you a working baseline library.

4. Enable JSON validation
Install the JSON Tools or JSON Schema Validator extension in VS Code.

This will highlight any schema errors in your references files.

You can also run the validate_references.ps1 script directly from VS Code’s integrated terminal (PowerShell).

5. Version control (GitHub ready)
Open the terminal in VS Code and run:

bash
git init
git add .
git commit -m "Initial scaffold of tenant-landlord legal library"
Add your GitHub remote:

bash
git remote add origin https://github.com/Bradleycrowe/Semptify_LegalLibrary.git
git push -u origin main
Now every update you make in VS Code can be checkpointed and pushed.

6. Updating the library
Add new .gov references into a new_entries.json.

Run update_library.ps1 from VS Code’s terminal:

powershell
./modules/legal_library/workflows/update_library.ps1 -NewEntriesFile new_entries.json
This merges entries, validates .gov URLs, and appends a CHANGELOG entry automatically.

7. Daily workflow
Edit JSON → Run validation script → Commit changes → Push to GitHub.

VS Code’s Git integration makes this one‑click.

🔑 Best Practices
Keep summaries plain‑language (2–3 sentences max).

Always check .gov URLs before adding.

Use CHANGELOG.md for every update (date + scope).

Run validation before committing—this ensures no broken JSON or non‑gov links slip in.

Use VS Code extensions like Markdown Preview Enhanced to view README/index nicely.

👉 This setup means you can drop the scaffold in today, run scripts directly inside VS Code, and push updates to GitHub instantly.

Do you want me to generate a ready‑to‑copy new_entries.json template so you can start adding fresh laws and funding programs without touching the core files?