# Integration Example: Housing Programs + Intensity + Complaints

## Real-World Scenario: Tenant with No Heat

### User Story
Maria lives in Minneapolis, MN with her 2 children (household of 3). She makes $28,000/year. It's January and she's had no heat for 10 days. She first reported it to her landlord 10 days ago. The landlord hasn't responded.

---

## System Response (Integrated)

### Step 1: Intensity Assessment

```python
from integrated_tenant_support import get_integrated_support

support = get_integrated_support()

solution = support.get_comprehensive_solution(
    issue_type="no_heat",
    location={
        "city": "Minneapolis",
        "county": "Hennepin",
        "state": "MN",
        "zip": "55401"
    },
    situation={
        "urgency": "urgent",
        "household_size": 3,
        "annual_income": 28000,
        "special_needs": [],
        "section_8": False,
        "intensity_preference": "normal"
    },
    landlord_responsiveness="poor",  # No response for 10 days
    days_since_reported=10
)
```

### Step 2: Intensity Determination

**Result: ESCALATED**

Why?
- Issue severity: SERIOUS (no heat in winter)
- Landlord responsiveness: POOR (10 days, no response)
- Days since reported: 10 (moderate escalation trigger)
- Intensity score: 3 → ESCALATED

---

## System Recommendations

### First Steps (Priority Order)

```python
solution["first_steps"] = [
    {
        "step": 1,
        "action": "Call 211 RIGHT NOW",
        "why": "Connect to ALL emergency resources immediately",
        "phone": "211",
        "priority": "IMMEDIATE"
    },
    {
        "step": 2,
        "action": "Contact legal aid emergency line",
        "why": "No heat in winter is a housing emergency - you need immediate legal help",
        "phone": "Find at lsc.gov/find-legal-aid"
    },
    {
        "step": 3,
        "action": "Apply to ALL emergency assistance programs simultaneously",
        "why": "Get help from every available source",
        "programs": [
            "LIHEAP Emergency Assistance (18-48 hour processing)",
            "Salvation Army Emergency Funds",
            "Catholic Charities Assistance",
            "Hennepin County Emergency Assistance"
        ]
    },
    {
        "step": 4,
        "action": "File with ALL 5 enforcement agencies",
        "why": "Multi-venue pressure forces landlord response",
        "venues": [
            "Minneapolis Code Enforcement (priority 1)",
            "Minneapolis Health Department (priority 1)",
            "HUD Fair Housing (priority 1)",
            "Minnesota Attorney General (priority 1)",
            "Legal Aid for court action (priority 1)"
        ]
    }
]
```

---

## Assistance Programs Discovered

### Federal Programs

#### LIHEAP Emergency Assistance
```json
{
  "name": "Low Income Home Energy Assistance Program (LIHEAP)",
  "category": "utility_assistance",
  "level": "federal",
  "urgency": "EMERGENCY - 18-48 hour processing",
  "eligibility": {
    "income": "150% poverty line = $38,730 for household of 3",
    "maria_qualifies": "YES - $28,000 < $38,730"
  },
  "benefit": "Emergency heating assistance, can pay for alternative heating",
  "how_to_apply": [
    "1. Call Minnesota LIHEAP: 651-296-3353 or 800-657-3789",
    "2. Say 'EMERGENCY - NO HEAT' immediately",
    "3. They will schedule phone intake within 24 hours",
    "4. Provide: Utility bills, income proof, heating emergency documentation",
    "5. Decision in 18-48 hours for emergencies"
  ],
  "contact": {
    "phone": "651-296-3353 (Twin Cities) or 800-657-3789 (MN)",
    "website": "https://mn.gov/dhs/people-we-serve/seniors/services/energy-assistance/"
  },
  "pro_tip": "Emphasize it's winter and you have children. Priority processing."
}
```

#### Legal Aid (LSC-Funded)
```json
{
  "name": "Legal Aid for Housing Emergencies",
  "category": "legal_aid",
  "level": "federal",
  "urgency": "IMMEDIATE",
  "eligibility": {
    "income": "125% poverty line = $32,275 for household of 3",
    "maria_qualifies": "YES - $28,000 < $32,275"
  },
  "services": [
    "Emergency court action for no heat",
    "Rent escrow (withhold rent until fixed)",
    "Code enforcement representation",
    "Potential damages claim"
  ],
  "how_to_apply": [
    "1. Call Mid-Minnesota Legal Aid: 612-334-5970",
    "2. Say 'EMERGENCY - NO HEAT WITH CHILDREN'",
    "3. Intake within 24 hours for emergencies",
    "4. Lawyer assigned within 48 hours"
  ],
  "contact": {
    "name": "Mid-Minnesota Legal Aid",
    "phone": "612-334-5970 (Minneapolis)",
    "website": "https://mylegalaid.org",
    "hours": "Mon-Fri 9am-5pm, emergency hotline available"
  },
  "what_lawyer_will_do": [
    "File emergency motion for heat restoration",
    "Help you withhold rent legally (rent escrow)",
    "File code violations",
    "Represent you in court if needed",
    "Pursue damages (hotel costs, medical issues)"
  ]
}
```

#### HUD Housing Counseling
```json
{
  "name": "HUD Housing Counseling",
  "category": "housing_counseling",
  "level": "federal",
  "urgency": "High Priority",
  "services": [
    "Emergency housing counseling",
    "Rights education",
    "Connection to resources",
    "Financial planning during crisis"
  ],
  "contact": {
    "phone": "1-800-569-4287",
    "find_local": "hud.gov/findacounselor"
  },
  "benefit": "Free expert who can coordinate all resources and create action plan"
}
```

### State Programs

#### Minnesota Emergency Rental Assistance
```json
{
  "name": "Minnesota Emergency Rental Assistance",
  "level": "state",
  "status": "Check availability - may be exhausted",
  "how_to_check": "Call 211 or visit mn.gov/dhs",
  "if_available": {
    "benefit": "Up to 18 months rent/utilities",
    "eligibility": "80% area median income"
  }
}
```

### County Programs

#### Hennepin County Emergency Assistance
```json
{
  "name": "Hennepin County Emergency Assistance",
  "level": "county",
  "category": "emergency_funds",
  "how_to_apply": "Call 612-348-4111 (Adult Services)",
  "benefit": "Emergency funds for housing crisis",
  "processing": "Usually 3-5 days"
}
```

### City Programs

#### Minneapolis Code Enforcement (PRIORITY 1)
```json
{
  "name": "Minneapolis Code Enforcement",
  "level": "city",
  "category": "complaint_filing",
  "urgency": "FILE IMMEDIATELY",
  "what_they_do": "Inspect property, issue violations, can order immediate heat restoration",
  "contact": {
    "phone": "311 (Minneapolis residents)",
    "website": "minneapolismn.gov/government/departments/cped/housing/inspections/",
    "emergency": "After hours: 612-673-5777"
  },
  "how_to_file": [
    "1. Call 311 (or 612-673-3000 from mobile)",
    "2. Say 'Housing emergency - no heat with children'",
    "3. Inspector dispatched within 24 hours for emergencies",
    "4. Violation issued if confirmed",
    "5. Landlord given 24 hours to restore heat in winter"
  ],
  "effectiveness": "VERY HIGH (95%) - City has strong enforcement power"
}
```

### Nonprofit Resources

#### Salvation Army Twin Cities
```json
{
  "name": "Salvation Army - Twin Cities",
  "level": "nonprofit",
  "category": "emergency_funds",
  "services": [
    "Emergency financial assistance",
    "Utility help",
    "Sometimes space heaters if available"
  ],
  "contact": {
    "phone": "612-767-1500",
    "address": "900 N 4th St, Minneapolis, MN 55401"
  },
  "how_to_apply": "Walk-in or call for appointment, bring utility bills and proof of emergency"
}
```

#### Catholic Charities Twin Cities
```json
{
  "name": "Catholic Charities",
  "level": "nonprofit",
  "category": "emergency_funds",
  "services": [
    "Emergency assistance",
    "Food shelf",
    "Counseling"
  ],
  "contact": {
    "phone": "612-204-8500",
    "website": "cctwincities.org"
  }
}
```

---

## Complaint Filing Strategy (ESCALATED Intensity)

### Venues to File (Multi-Venue Pressure)

1. **Minneapolis Code Enforcement** (Priority 1, Local)
   - File: 311 or online
   - Timeline: Inspection within 24 hours
   - Why: Most effective, fastest response

2. **Minneapolis Health Department** (Priority 1, Local)
   - File: 612-673-2301
   - Timeline: 1-2 days
   - Why: Health hazard in winter

3. **HUD Fair Housing** (Priority 1, Federal)
   - File: hud.gov/fairhousing
   - Timeline: Weeks to months
   - Why: If discrimination involved, federal pressure

4. **Minnesota Attorney General** (Priority 1, State)
   - File: ag.state.mn.us
   - Timeline: 30-90 days
   - Why: Consumer protection, state enforcement

5. **Legal Aid Court Action** (Priority 1)
   - Via your lawyer
   - Timeline: Emergency motion within days
   - Why: Court order for heat restoration

---

## Timeline for Maria

### Immediate (Day 1 - TODAY)
- [ ] **Call 211** → Connect to emergency resources (30 minutes)
- [ ] **Call LIHEAP emergency line** → Start 18-48 hour process (30 minutes)
- [ ] **Call Mid-Minnesota Legal Aid** → Get lawyer assigned (30 minutes)
- [ ] **File Minneapolis 311** → Code enforcement inspection scheduled (15 minutes)
- [ ] **Call Salvation Army** → Emergency funds appointment (15 minutes)
- [ ] **Call Catholic Charities** → Additional emergency help (15 minutes)

### Day 1-2
- [ ] LIHEAP phone intake completed
- [ ] Legal aid lawyer assigned
- [ ] Code enforcement inspection completed
- [ ] Violation issued to landlord (24-hour deadline to restore heat)

### Day 2-3
- [ ] LIHEAP emergency assistance approved
- [ ] Space heater provided or hotel voucher while heat restored
- [ ] Lawyer files emergency court motion if landlord still non-responsive
- [ ] Salvation Army emergency funds received

### Day 3-5
- [ ] Code enforcement re-inspection
- [ ] If heat not restored: Court hearing for emergency order
- [ ] Health department inspection
- [ ] Attorney General complaint filed

### Resolution Expected
- **Best case**: Heat restored within 48 hours due to code enforcement pressure
- **Worst case**: Court order for heat + damages within 7 days
- **Financial help**: LIHEAP + emergency funds cover heating costs and alternative arrangements

---

## What Maria Sees in the UI

### Emergency Banner (Pulsing Red)
```
🚨 NEED HELP RIGHT NOW?
Call or Text: 211
United Way 211 connects you to emergency resources 24/7.
They can help with rent, utilities, food, shelter, and more.
```

### Results Header
```
✅ We Found 18 Programs For You!

Based on your situation (no heat, 10 days, non-responsive landlord),
we recommend an ESCALATED response:

• Apply for emergency assistance programs IMMEDIATELY
• Contact legal aid for emergency legal help
• File with ALL code enforcement agencies
• Multi-venue pressure will force landlord action

YOU QUALIFY for most programs based on your income ($28,000 is 72% of poverty line for household of 3).
```

### First Steps Card
```
📋 DO THESE THINGS RIGHT NOW (In Order):

1. ☎️ Call 211 IMMEDIATELY
   Why: Fastest connection to ALL emergency help in your area
   Phone: Just dial 211

2. ☎️ Call LIHEAP Emergency: 651-296-3353
   Why: Emergency heating help in 18-48 hours
   Say: "Emergency - no heat with children"

3. ☎️ Call Legal Aid: 612-334-5970
   Why: Free lawyer for emergency court action
   Say: "Housing emergency - no heat 10 days"

4. ☎️ Call 311 (Minneapolis Code Enforcement)
   Why: City inspector within 24 hours, violation issued
   Say: "No heat emergency with children"

5. 💰 Apply to emergency funds:
   • Salvation Army: 612-767-1500
   • Catholic Charities: 612-204-8500
   • Hennepin County: 612-348-4111
```

### Program Cards
Each program shows:
- ✅ YOU QUALIFY badge (based on income)
- Contact information
- Application steps
- Timeline
- "Why this helps" explanation
- Application guide button

---

## System Intelligence in Action

### Why ESCALATED vs MAXIMUM?

**ESCALATED chosen because:**
- Issue is serious (no heat in winter)
- Landlord is poor (10 days, no response)
- NOT retaliation or discrimination (yet)
- NOT immediate danger (family has alternative arrangements possible)

**If situation changes to MAXIMUM:**
- If retaliation detected
- If children get sick from cold
- If landlord threatens illegal eviction
- If 14+ days with no resolution

Then system would add:
- Media contacts (housing reporters)
- Elected officials (city council, mayor)
- Public pressure campaign
- All venues + media + officials simultaneously

---

## Outcomes Expected

### Likely Outcome (90%)
- Code enforcement forces heat restoration within 48 hours
- LIHEAP covers heating costs
- Legal aid secures rent reduction or damages
- Maria stays in home with heat restored

### If Landlord Retaliates
- System escalates to MAXIMUM intensity
- Retaliation protection via legal aid
- Additional complaints filed
- Potential for significant damages

### Long-Term
- Maria applies for Section 8 (gets on waitlist)
- Rates landlord poorly (bad landlord recognition)
- System learns this landlord is problematic
- Future tenants see poor rating

---

## System Learning

After resolution:
```python
# Track outcome
engine.track_application_outcome(
    program_id="LIHEAP",
    outcome="approved",
    timeline_days=2,
    notes="Emergency processing for no heat in winter"
)

engine.track_application_outcome(
    program_id="Minneapolis_Code_Enforcement",
    outcome="approved",
    timeline_days=1,
    notes="Inspection within 24 hours, heat restored within 48 hours"
)

# Rate landlord
intensity_engine.rate_landlord(
    landlord_id="maria_landlord_id",
    rating=1,  # 1 star - very poor
    category="responsiveness",
    comment="10 days no heat, no response until code enforcement"
)
```

**System now knows:**
- LIHEAP emergency processing works fast (2 days)
- Minneapolis code enforcement is very effective (95% success)
- This landlord has poor rating (future tenants warned)

---

## Key Takeaways

1. **Comprehensive**: System found 18+ resources across federal/state/county/city/nonprofit
2. **Intelligent**: ESCALATED intensity appropriate for situation
3. **Actionable**: Clear priority-ordered steps
4. **Effective**: Multi-venue pressure + legal aid + emergency assistance
5. **Fair**: If landlord had been responsive (GOOD rating), would have used COLLABORATIVE approach first

**The integration ensures Maria gets BOTH immediate help (programs) AND enforcement action (complaints) in appropriate balance for her situation's severity.**
