# ✅ ADAPTIVE INTENSITY SYSTEM - COMPLETE

## WHAT WE BUILT

A **fair, balanced system** that scales response intensity based on situation - from **positive recognition for good landlords** to **maximum pressure for bad ones**.

---

## KEY PRINCIPLE

**Not all situations require full legal intensity!**

- Good landlords maintain properties → Get **recognition certificates**
- Minor issues with responsive landlords → Start with **friendly communication**
- Serious issues with unresponsive landlords → **Multi-venue filing**
- Critical/illegal with hostile landlords → **Maximum pressure everywhere**

---

## 5 INTENSITY LEVELS

### ✨ POSITIVE
Everything good → Recognition, no filing needed

### 🤝 COLLABORATIVE  
Minor issues, responsive landlord → Friendly communication first

### 📝 ASSERTIVE
Issue persists, slow landlord → Formal documentation, 1-2 venues

### ⚠️ ESCALATED
Serious issues, unresponsive → Multi-venue filing (3-5 venues)

### 🚨 MAXIMUM
Critical/illegal, hostile → ALL venues + media + legal aid

---

## GOOD LANDLORD RECOGNITION

### Rating System
- **5 stars**: Excellent - exceeds expectations
- **4 stars**: Good - meets expectations reliably  
- **3 stars**: Fair - meets basic standards
- **2 stars**: Poor - frequent issues
- **1 star**: Problem - persistent violations

### Recognition Levels
- **🌟 EXCELLENT (4.5+ avg)**: "Community Asset" - Gets certificate
- **✅ GOOD (4.0+ avg)**: "Reliable Landlord" - Gets certificate
- **⚠️ FAIR (3.0+ avg)**: "Meets Basic Standards"
- **❌ POOR (2.0+ avg)**: "Frequent Issues"
- **🚫 PROBLEM (<2.0 avg)**: "Persistent Violations"

### Certificate for Good Landlords
```
🏆 GOOD LANDLORD RECOGNITION 🏆

Rating: 4.7/5.0 stars (12 reviews)
Recognition: EXCELLENT - Community Asset

Category Ratings:
  • Responsiveness: ⭐⭐⭐⭐⭐ (4.8/5.0)
  • Maintenance: ⭐⭐⭐⭐⭐ (4.9/5.0)

Being a landlord is an investment in community, the future, 
and fair monetary gain. Thank you for maintaining your property 
well and treating tenants with respect.
```

---

## HOW INTENSITY IS CALCULATED

```
Factors:
1. Issue Severity (good → minor → moderate → serious → critical)
2. Landlord Responsiveness (excellent → good → fair → poor → hostile)
3. Time Elapsed (< 7 days → 7-14 days → 14-30 days → 30+ days)
4. Landlord History (4.5+ stars = lower intensity, <2 stars = higher)
5. User Preference ("gentle" → "normal" → "aggressive")

Algorithm:
Base score from severity + responsiveness
+ Time adjustment (escalate if issue not resolved)
+ History adjustment (good landlords get benefit of doubt)
+ User preference adjustment

Final Score → Intensity Level:
0 = POSITIVE ✨
1 = COLLABORATIVE 🤝
2 = ASSERTIVE 📝
3 = ESCALATED ⚠️
4 = MAXIMUM 🚨
```

---

## REAL EXAMPLES

### Example 1: Good Landlord, No Issues
**Input**: Everything fine, landlord has 4.8 star rating
**Intensity**: POSITIVE ✨
**Response**: "Your landlord is doing a great job! Leave a positive review to recognize good property management."

### Example 2: Minor Leak, Responsive Landlord  
**Input**: Kitchen dripping, landlord usually good (4.2 stars), 2 days elapsed
**Intensity**: COLLABORATIVE 🤝
**Response**: "Start with friendly text: 'Hi, sink is dripping. Could you take a look? Thanks!'"

### Example 3: No Heat 15 Days, Slow Landlord
**Input**: No heat in winter, landlord fair (3.2 stars), 15 days elapsed
**Intensity**: ASSERTIVE 📝 (moving to ESCALATED)
**Response**: "Send formal written notice with 24-hour deadline. Mention legal obligations. If not resolved, escalate to ESCALATED level and file with code enforcement."

### Example 4: Mold 30+ Days, Ignoring Landlord
**Input**: Black mold, landlord poor (2.1 stars), 30+ days elapsed
**Intensity**: ESCALATED ⚠️
**Response**: "File with code enforcement + health dept + state housing + legal aid. Multi-venue approach needed."

### Example 5: No Heat + Retaliation Threats
**Input**: No heat, landlord hostile (1.8 stars), threatening eviction
**Intensity**: MAXIMUM 🚨  
**Response**: "EMERGENCY: File everywhere immediately (code, health, HUD, AG, legal aid). Consider media. Retaliation is ILLEGAL."

---

## FILES CREATED

### 1. `adaptive_intensity_engine.py` (550+ lines)
Core engine that determines intensity and manages landlord ratings.

**Classes**:
- `IntensityLevel` - Enum of 5 intensity levels
- `SituationSeverity` - Enum of issue severity
- `LandlordResponsiveness` - Enum of landlord behavior
- `AdaptiveIntensityEngine` - Main engine

**Key Methods**:
- `determine_intensity()` - Calculate appropriate intensity level
- `rate_landlord()` - Rate landlord in specific category
- `get_landlord_profile()` - Get ratings and recognition
- `generate_landlord_recognition_certificate()` - Certificate for good landlords
- `report_tenant_issue()` - Placeholder for fairness (bad tenants exist too)

### 2. `complaint_filing_engine.py` (UPDATED)
Now uses adaptive intensity in `generate_filing_strategy()`.

**New Parameters**:
- `landlord_responsiveness` - "excellent", "good", "fair", "poor", "hostile"
- `landlord_id` - For history lookup
- `days_since_reported` - For time-based escalation

**New Behavior**:
- **POSITIVE intensity**: Returns recognition, no filing
- **COLLABORATIVE**: Returns communication template, no filing yet
- **ASSERTIVE**: Files with 1-2 most effective venues
- **ESCALATED**: Files with 3-5 venues (multi-venue)
- **MAXIMUM**: Files with ALL venues + media option

### 3. `ADAPTIVE_INTENSITY_SYSTEM.md`
Complete documentation with philosophy, examples, API usage.

---

## INTEGRATION

### Before (Old System)
```python
strategy = engine.generate_filing_strategy(
    issue_type="no_heat",
    location={...},
    user_situation={...},
    urgency="urgent"
)
# Always returned multi-venue filing strategy
```

### After (Adaptive System)
```python
strategy = engine.generate_filing_strategy(
    issue_type="no_heat",
    location={...},
    user_situation={
        "intensity_preference": "normal"  # "gentle", "normal", "aggressive"
    },
    urgency="urgent",
    landlord_responsiveness="poor",  # NEW: Key factor
    landlord_id="landlord_123",  # NEW: Use history
    days_since_reported=15  # NEW: Time-based escalation
)

# Returns appropriate strategy:
# - POSITIVE: No filing, just recognition
# - COLLABORATIVE: Communication template
# - ASSERTIVE: 1-2 venues
# - ESCALATED: Multi-venue (3-5)
# - MAXIMUM: All venues + media
```

---

## FAIRNESS PHILOSOPHY

### System Recognizes BOTH Sides

**Good Landlords**:
- ✅ Get recognition certificates
- ✅ Lower intensity recommendations  
- ✅ Benefit of doubt for minor issues
- ✅ Acknowledged as community assets

**Bad Landlords**:
- ❌ Higher intensity recommendations
- ❌ Escalate faster
- ❌ More venues filed with
- ❌ Public accountability

**Investment Perspective**:
- Landlords provide essential service (housing)
- Property maintenance costs money
- Fair rent = fair return on investment
- Good landlords invest in community future

**Bad Tenants**:
- System acknowledges bad tenants exist too
- Placeholder for tenant issue reporting
- Future: Landlords can report tenant problems
- **Balance**: Not all tenants are angels, not all landlords are bad

---

## DATA STORAGE

- `data/landlord_ratings.json` - Landlord ratings and recognition levels
- `data/intensity_history.json` - Intensity escalation history per situation

---

## KEY BENEFITS

### For Tenants
✅ **No unnecessary complaints** - collaborative for minor issues
✅ **Appropriate escalation** - serious issues get serious response
✅ **Clear guidance** - exactly what to do at each level
✅ **Builds good relationships** - positive recognition for good landlords

### For Landlords  
✅ **Recognition for good work** - certificates for excellent landlords
✅ **Fair treatment** - not immediately hostile for minor issues
✅ **Clear expectations** - know what triggers escalation
✅ **Community asset acknowledgment** - investing in community recognized

### For Community
✅ **Balanced system** - fair to both sides
✅ **Incentivizes good behavior** - recognition for good landlords
✅ **Protects tenants** - escalates appropriately for serious issues
✅ **Builds trust** - not automatically adversarial

---

## SUMMARY

✅ **5 intensity levels** - from positive recognition to maximum pressure
✅ **Good landlord recognition** - certificates for 4.0+ avg rating
✅ **Adaptive escalation** - scales based on severity + responsiveness + time + history
✅ **Fair to both sides** - acknowledges good landlords AND bad tenants
✅ **Community investment** - recognizes landlords contribute to community
✅ **No unnecessary filing** - collaborative for minor issues with responsive landlords
✅ **Maximum pressure when needed** - all venues + media for critical/hostile situations

**Result**: System is **SMART, FAIR, and EFFECTIVE** - not hostile to good landlords, but tough on bad ones. Scales intensity appropriately based on actual situation, not one-size-fits-all approach.

**Philosophy**: Being a landlord is an investment in community, the future, and fair monetary gain. Good landlords deserve recognition. Bad landlords deserve accountability. System recognizes both.
