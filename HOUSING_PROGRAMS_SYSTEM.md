# Housing Programs & Resources System

**Complete Documentation**

## 🎯 Overview

The Housing Programs & Resources system discovers ALL available assistance programs (federal, state, county, city, nonprofit) for any location, provides complete application details, and integrates with the adaptive intensity system for site-wide intelligent tenant support.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Program Categories](#program-categories)
3. [Federal Programs Database](#federal-programs-database)
4. [Intensity Integration](#intensity-integration)
5. [API Reference](#api-reference)
6. [User Interface](#user-interface)
7. [Data Storage](#data-storage)
8. [Site-Wide Usage](#site-wide-usage)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATED TENANT SUPPORT                     │
│  Combines: Intensity Assessment + Programs + Complaints         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┴────────────────────┐
         │                                          │
┌────────▼────────┐                   ┌────────────▼──────────┐
│  Adaptive       │                   │  Housing Programs      │
│  Intensity      │◄──────────────────│  Discovery Engine      │
│  Engine         │    Coordinates    │                        │
└────────┬────────┘                   └────────────┬───────────┘
         │                                         │
         │    ┌─────────────────────────────┐     │
         │    │  Complaint Filing Engine    │     │
         └───►│  (Files when appropriate)   │◄────┘
              └─────────────────────────────┘
```

### Core Components

1. **housing_programs_engine.py** (1000+ lines)
   - Discovers all programs for a location
   - Provides application guides
   - Calculates eligibility
   - Tracks effectiveness
   - Integrates with intensity system

2. **housing_programs_routes.py**
   - Flask API endpoints
   - Search, filter, track outcomes
   - Category browsing
   - Emergency quick help

3. **templates/housing_programs.html**
   - Beautiful 4-step wizard
   - Location → Categories → Situation → Results
   - Emergency mode with 211 banner

4. **integrated_tenant_support.py**
   - Coordinates all three systems
   - POSITIVE → programs (proactive)
   - COLLABORATIVE → programs + communication
   - ASSERTIVE → programs + selective filing
   - ESCALATED → ALL programs + multi-venue filing
   - MAXIMUM → crisis resources + all venues + media

---

## Program Categories

### For Tenants

| Category | Description | Examples |
|----------|-------------|----------|
| **Rent Assistance** | Help paying rent | Section 8, ERAP, local funds |
| **Utility Assistance** | Help with bills | LIHEAP (heating/cooling), water bill help |
| **Emergency Funds** | Quick cash for crises | Salvation Army, Catholic Charities |
| **Legal Aid** | Free legal help | LSC-funded legal aid, tenant rights orgs |
| **Housing Counseling** | Expert guidance | HUD counseling, tenant education |
| **Weatherization** | Energy efficiency | Free insulation, HVAC repair |
| **Disability & Accessibility** | ADA accommodations | Modifications, accessible housing |
| **Veteran Services** | Veterans-only programs | HUD-VASH, VA loans, homeless prevention |
| **Senior Services** | 65+ programs | Senior housing, Medicaid waivers |
| **Homeless Prevention** | Keep you housed | Rapid rehousing, emergency shelter |
| **Food Assistance** | Food banks, SNAP | Feeding America network, local pantries |
| **Healthcare** | Medical help | Medicaid, free clinics, prescriptions |
| **Mediation** | Dispute resolution | Free landlord-tenant mediation |

### For Landlords

| Category | Description | Examples |
|----------|-------------|----------|
| **Landlord Rehab Programs** | Property improvement | Loans/grants for repairs, code upgrades |
| **Landlord Tax Credits** | Tax incentives | Low-Income Housing Tax Credit (LIHTC) |

---

## Federal Programs Database

### Section 8 Housing Choice Voucher

**What it is**: Monthly rental assistance for low-income families, elderly, and disabled.

**Who qualifies**:
- Income: 50% of area median income
- Citizenship: US citizen or eligible immigrant
- Background check required
- Landlord must accept voucher

**How to apply**:
1. Find your local Public Housing Authority (PHA)
2. Check if waitlist is open
3. Submit application
4. Wait (often 2+ years)
5. Respond immediately when your name comes up

**Contact**:
- Website: https://www.hud.gov/topics/housing_choice_voucher_program_section_8
- Phone: 1-800-955-2232 (HUD)
- Local: Find PHA at hud.gov/program_offices/public_indian_housing/pha/contacts

**Tips**:
- Apply to MULTIPLE PHAs if you're willing to move
- Check for preferences (veteran, elderly, disabled)
- Keep contact info current with PHA
- Apply for other programs while waiting

**For landlords**:
- Guaranteed rent payment
- Must pass HUD inspection
- Higher income tenants preferred by HUD

---

### LIHEAP (Low Income Home Energy Assistance)

**What it is**: Help with heating/cooling bills and energy crises.

**Who qualifies**:
- Income: Typically 150% of poverty line (varies by state)
- Crisis assistance: Shutoff notice, out of fuel, extreme weather

**How to apply**:
1. Find your state LIHEAP office
2. Check application period (seasonal)
3. Gather documents (income proof, utility bills, shutoff notice)
4. Apply (online, phone, or in person depending on state)
5. Wait: Emergency 18-48 hours, Regular 2-4 weeks

**Contact**:
- Website: https://www.acf.hhs.gov/ocs/liheap
- Find state office: acf.hhs.gov/ocs/liheap-state-and-territory-contact-listing

**Emergency assistance**:
- If you have a shutoff notice, SAY SO IMMEDIATELY
- May get processing within 18-48 hours
- Can usually apply once per heating season and once per cooling season

---

### Legal Aid (LSC-funded)

**What it is**: Free legal help for housing issues.

**Who qualifies**:
- Income: 125% of poverty line (typically)
- Case types: Eviction, discrimination, unsafe housing, landlord-tenant disputes

**Services**:
- Eviction defense
- Housing discrimination cases
- Unsafe housing conditions
- Fair housing violations
- Landlord-tenant disputes

**Contact**:
- Website: https://www.lsc.gov/what-legal-aid/find-legal-aid
- Find local office: Use website tool

**When to contact**:
- ASAP if facing eviction
- For discrimination or retaliation
- For unsafe conditions landlord won't fix
- Before signing anything you don't understand

---

### HUD Housing Counseling

**What it is**: Free or low-cost housing counseling from HUD-approved agencies.

**Services**:
- Eviction prevention
- Rental housing counseling
- Budgeting and financial management
- Fair housing rights education
- Homebuyer education

**Contact**:
- Website: https://www.hud.gov/findacounselor
- Phone: 1-800-569-4287

**Why use it**:
- Expert guidance on all options
- Can help you create a plan
- Connects you to other resources
- Free and confidential

---

### VA Housing Assistance

**For veterans only**

**Programs**:
- VA Home Loans (0% down)
- HUD-VASH (housing vouchers for homeless veterans)
- Adaptive housing grants (disabled veterans)
- Homeless veteran programs

**Contact**:
- Website: https://www.va.gov/housing-assistance/
- Phone: 1-877-827-3702
- Local: Contact your local VA Medical Center

**Eligibility**:
- Veteran status required
- Honorable discharge for most programs
- Some programs for active duty families

---

### United Way 211

**THE STARTING POINT FOR EVERYTHING**

**What it is**: 24/7 referral service that connects you to ALL local resources.

**How to use**:
- Dial 211 (or text your ZIP to 898-211)
- Available 24/7 in most areas
- Free and confidential
- Available in multiple languages

**Why it's important**:
- Fastest way to get help
- Knows ALL local programs
- Can connect you immediately to emergency assistance
- One call does it all

---

## Intensity Integration

The housing programs system integrates with adaptive intensity to provide appropriate resources:

### POSITIVE Intensity
- **Programs recommended**: Proactive resources (HUD counseling, credit building, financial planning)
- **Approach**: "Keep things going well"
- **Complaint filing**: None (no issues)
- **First step**: Rate landlord positively, apply for Section 8 (get on waitlist)

### COLLABORATIVE Intensity
- **Programs recommended**: Assistance programs (rent help, utility help, mediation)
- **Approach**: "Resolve cooperatively"
- **Complaint filing**: Not yet (try communication first)
- **First step**: Apply for assistance, friendly communication, mediation

### ASSERTIVE Intensity
- **Programs recommended**: Legal aid + emergency assistance
- **Approach**: "Formal action appropriate"
- **Complaint filing**: Yes (1-2 most effective venues)
- **First step**: Legal aid + emergency funds + formal notice + selective filing

### ESCALATED Intensity
- **Programs recommended**: ALL emergency resources
- **Approach**: "Comprehensive action needed"
- **Complaint filing**: Yes (3-5 venues simultaneously)
- **First step**: Call 211 + legal aid emergency + all assistance programs + multi-venue filing

### MAXIMUM Intensity
- **Programs recommended**: Crisis resources + media contacts
- **Approach**: "EMERGENCY - all available resources"
- **Complaint filing**: Yes (ALL venues + media)
- **First step**: 211 IMMEDIATELY + emergency legal aid + all programs + all venues + media/officials

---

## API Reference

### POST /api/programs/search

Search for programs by location and criteria.

**Request**:
```json
{
  "location": {
    "city": "Minneapolis",
    "county": "Hennepin",
    "state": "MN",
    "zip": "55401"
  },
  "categories": ["rent_assistance", "utility_assistance"],
  "urgency": "urgent",
  "household_size": 3,
  "annual_income": 28000,
  "special_needs": ["veteran", "disability"],
  "for_landlord": false
}
```

**Response**:
```json
{
  "federal_programs": [...],
  "state_programs": [...],
  "county_programs": [...],
  "city_programs": [...],
  "nonprofit_resources": [...],
  "recommended_first_steps": [...],
  "emergency_contacts": [...],
  "eligibility_guidance": {...}
}
```

---

### GET /api/programs/guide/{program_id}

Get detailed application guide for a specific program.

**Query params**: city, county, state, zip, household_size, annual_income

**Response**:
```json
{
  "program": "Section 8 Housing Choice Voucher",
  "steps": [
    {
      "step": 1,
      "action": "Find your local PHA",
      "description": "...",
      "time": "10 minutes"
    }
  ],
  "required_documents": [...],
  "timeline": "Variable - often 2+ year waitlist",
  "tips": [...],
  "contact_info": {...}
}
```

---

### POST /api/programs/intensity-recommendations

Get program recommendations based on intensity level.

**Request**:
```json
{
  "intensity_level": "ESCALATED",
  "situation": {
    "issue": "no_heat",
    "days": 15,
    "location": {...}
  }
}
```

**Response**:
```json
{
  "intensity_level": "ESCALATED",
  "recommended_programs": [...],
  "recommended_actions": [...],
  "tone": "Urgent and comprehensive",
  "guidance": "..."
}
```

---

### GET /api/programs/quick-help

Get emergency contacts immediately.

**Response**:
```json
{
  "emergency_contacts": [
    {
      "name": "United Way 211",
      "phone": "211",
      "description": "24/7 connection to all resources",
      "why": "Fastest way to get help"
    }
  ],
  "immediate_steps": [...]
}
```

---

## User Interface

### 4-Step Wizard

1. **Location**
   - City, County, State (required), ZIP
   - Validates state is provided

2. **What You Need**
   - Category grid with icons
   - Select all that apply
   - Skippable (will show all programs)

3. **Your Situation**
   - Urgency selector: Routine | Soon | Urgent | Emergency
   - Household size & income (optional, for eligibility check)
   - Special needs: Veteran, Disability, Senior, Homeless
   - "I'm a landlord" checkbox

4. **Results**
   - Emergency contacts (if urgent/emergency)
   - First steps (priority-ordered)
   - Eligibility guidance (if income provided)
   - Program cards by level (federal, state, county, city, nonprofit)
   - Application guides
   - Print button

### Emergency Mode

- If urgency is "Emergency", shows pulsing red banner with 211
- Emergency contacts displayed prominently
- Fast-track program info
- Emphasizes immediate action

---

## Data Storage

### housing_programs_data/programs.json

Complete program database:
```json
{
  "federal": {
    "HUD_Section8": {
      "name": "Section 8 Housing Choice Voucher",
      "category": "rent_assistance",
      "eligibility": {...},
      "contact": {...},
      "for_landlords": {...}
    }
  },
  "state_template": {...},
  "county_template": {...},
  "nonprofit_template": {...}
}
```

### housing_programs_data/applications.json

User application tracking (anonymous):
```json
{
  "app_12345": {
    "program_id": "HUD_Section8",
    "applied_date": "2024-01-15",
    "status": "pending",
    "location": "MN"
  }
}
```

### housing_programs_data/outcomes.json

Effectiveness tracking:
```json
{
  "HUD_Section8": {
    "total_tracked": 100,
    "approved": 45,
    "denied": 30,
    "pending": 25,
    "avg_timeline_days": 730
  }
}
```

---

## Site-Wide Usage

### In Complaint Filing System

```python
from integrated_tenant_support import get_integrated_support

support = get_integrated_support()

solution = support.get_comprehensive_solution(
    issue_type="no_heat",
    location={"city": "Minneapolis", "state": "MN"},
    situation={"urgency": "urgent", "household_size": 3},
    landlord_responsiveness="poor",
    days_since_reported=10
)

# Returns:
# - Intensity level (ESCALATED)
# - Assistance programs (LIHEAP emergency, legal aid, etc.)
# - Complaint strategy (multi-venue filing)
# - First steps (211, apply for programs, file complaints)
```

### In Registration Flow

```python
# After user registers, show them available programs
programs = engine.discover_programs(
    location=user_location,
    categories=["rent_assistance", "legal_aid"],
    urgency="routine"
)

# Display in welcome email or dashboard
```

### In Adaptive Intensity System

```python
# When intensity is COLLABORATIVE, recommend programs first
if intensity_level == "COLLABORATIVE":
    recommendations = engine.get_intensity_based_recommendations(
        intensity_level="COLLABORATIVE",
        situation=situation
    )
    # Shows: mediation, assistance programs, communication templates
    # NO formal complaints yet
```

---

## Executive Branch Contacts (Escalation Path)

For all federal programs, if you're not getting help:

1. **Program level**: Local administrator (PHA director, LIHEAP coordinator)
2. **Regional level**: Regional HUD office, state agency director
3. **National level**: HUD Secretary, ACF Director, cabinet officials
4. **Congressional**: Contact your Representative and Senators

Example escalation:
- Issue with local PHA → Contact PHA director
- No response → Contact regional HUD office
- Still no response → Contact HUD Secretary via elected officials
- Final option → Congressional inquiry (very effective)

---

## Best Practices

### For Users

1. **Start with 211**: Always call 211 first for emergency needs
2. **Apply to multiple programs**: Don't put all eggs in one basket
3. **Keep copies**: Save everything you submit
4. **Follow up**: Squeaky wheel gets the grease
5. **Be patient but persistent**: Waitlists are long, but stay on them

### For Landlords

1. **Check available incentives**: Tax credits, rehab loans
2. **Partner with housing authorities**: Guaranteed rent
3. **Maintain good ratings**: Good landlords get recognition
4. **Communicate**: Most issues resolved with communication

### For Integration

1. **Use intensity-based routing**: Show programs appropriate to situation
2. **Prioritize assistance over complaints**: Programs first when appropriate
3. **Emergency fast-track**: 211 + emergency contacts for urgent situations
4. **Track outcomes**: Report back what worked to improve recommendations

---

## Future Enhancements

- [ ] Add state-specific program databases (beyond templates)
- [ ] Real-time waitlist status for Section 8
- [ ] Calendar integration for application deadlines
- [ ] Mobile app with location services
- [ ] Push notifications for new programs
- [ ] Landlord portal for incentive programs
- [ ] Success stories and testimonials
- [ ] Multi-language support
- [ ] Integration with 211 API (if available)

---

## Support

For questions or issues with the housing programs system:
- Check user guide: `/housing-programs` page
- Emergency help: Dial 211
- Technical support: [Your support contact]

---

**Remember**: This system is designed to be COMPREHENSIVE (find ALL available resources) and ADAPTIVE (scale response to situation). Good landlords get recognition, assistance comes before complaints when appropriate, and emergency situations get immediate crisis resources.
