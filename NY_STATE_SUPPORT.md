# ✅ NEW YORK STATE CONFIGURATION ADDED

## Summary
Successfully added comprehensive **New York (NY)** state support to the Court AI Training module. The system now supports both Minnesota (MN) and New York (NY) court procedures.

---

## What Was Added

### 1. **New York Court Rules** (`court_ai_trainer.py`)
Added NY-specific court configuration to `COURT_RULES` dictionary:

```python
"NY": {
    "response_deadline_days": 30,      # 30 days to respond (CPLR § 213)
    "notice_requirement_days": 3,      # 3-day notice to cure
    "font_size_min": 11,
    "margin_min_inches": 1.0,
    "filing_fee_required": True,
    "notarization_required": False,    # NY doesn't require notarization
    "eviction_notice_days": 30,        # 30-day Notice to Quit minimum
    "pre_litigation_notice_days": 10,  # 10-day demand notice
    "answer_deadline_days": 5,         # STRICT 5-day answer deadline
    "court_type": "Civil Court or Supreme Court",
    "small_claims_limit": 5000,        # Small claims limit
    "marshal_fee_required": True,      # Marshal/sheriff fee for eviction
    "specials_allowed": True,          # Can claim special damages
    "habitability_threshold": "Substantial breach affecting health/safety",
}
```

**Key NY Features:**
- ✅ 30-day response deadline (vs. MN's 20 days)
- ✅ 5-day answer deadline (strict)
- ✅ 10-day demand notice required
- ✅ 30-day Notice to Quit minimum
- ✅ No notarization requirement for filings
- ✅ Marshal fee required for eviction

---

### 2. **New York Training Section** (`templates/court_training_module.html`)
Added comprehensive "🗽 New York Guide" section with:

#### **New York Court Structure**
- Civil Court (up to $25K claims)
- Supreme Court ($25K+ claims)
- Housing Court (NYC only - specialized housing court)

#### **NY Eviction Process** (9 Steps)
1. 10-Day Demand Notice
2. Notice to Quit (30+ days)
3. Petition Filing
4. Service on Tenant
5. Answer Due (5 days - STRICT)
6. Discovery
7. Hearing/Trial
8. Judgment
9. Warrant for Eviction (72-hour notice)

#### **NY Filing Requirements**
- ⚠️ Personal service required (not just certified mail)
- ⚠️ Predicate notice required (10-day demand + 30-day Notice to Quit)
- ⚠️ 5-day answer deadline is STRICT
- ⚠️ Affirmative defenses must be in answer or waived
- ⚠️ Housing Court for NYC (specific rules)
- ⚠️ Marshal fee ($300-500) on eviction

#### **Strong NY Tenant Defenses**
1. **Habitability Violations** (Most Powerful)
   - Mold, lead paint, heat/hot water, vermin, roof leaks
   - NY law implies warranty - cannot be waived

2. **Non-Payment Defense**
   - "Rent strike" if landlord breaches habitability
   - Rent goes into escrow account

3. **Retaliation** (Protected Class)
   - Illegal if eviction within 6 months of housing complaint/organizing

4. **Discrimination**
   - Illegal if based on race, religion, family status, disability, source of income

5. **Failure to Provide Predicate Notice**
   - If 10-day demand or 30-day Notice to Quit invalid = dismiss

6. **Improper Service**
   - Not personally served = dismiss

7. **Regulatory Violations**
   - Lease violates housing code

#### **NY Tenant Protections**
- ✅ Warranty of Habitability (landlord must maintain fit condition)
- ✅ Right to Repair/Deduct (repair and deduct from rent)
- ✅ Right to Organize/Complain (cannot be evicted for)
- ✅ No-Fault Eviction Protection (June 2019 - must have "just cause")
- ✅ Rent Control/Stabilization (highly protected)

#### **NY Resources & Agencies**
- Housing Court (NYC): 646-FIX-HOUSING
- HPD: 311 in NYC
- DHCR: Rent stabilization oversight
- Legal Aid Society: 212-577-3300
- Tenant Rights Hotline: 718-904-1180
- NY AG Consumer Bureau: 800-771-7755

#### **NY Evidence Rules**
- Photos/Videos: Must authenticate under oath
- Emails/Texts: Full headers required
- Prior Complaints: Very powerful evidence
- Repair Estimates: Supports damages claims
- Medical Evidence: Strengthens habitability defense
- Utility Records: Supports heat/water claims

#### **Winning Strategies**
- If Non-Payment: Assert habitability, document defects, file counterclaim
- If "Lease Violation": Challenge notice validity, show minor violation, offer to cure
- If Within 6 Months of Complaint: Assert retaliation (presumption favors tenant)

---

## API Integration

### Get NY Court Clerk Training Prompt
```bash
curl "http://localhost:5000/api/court-training/generate-clerk-prompt?state=NY"
```

**Response:**
```json
{
  "status": "success",
  "state": "NY",
  "prompt": "You are an expert AI Court Clerk Assistant for NY courts...",
}
```

### Create NY-Specific Trainer in Python
```python
from court_ai_trainer import CourtAITrainer

# Create NY trainer
trainer = CourtAITrainer(state="NY")

# NY trainer knows:
# - 30-day response deadline
# - 5-day answer deadline
# - 10-day demand + 30-day notice requirement
# - No notarization for filings
# - Marshal fee required
# - Warranty of habitability rules
```

---

## Accessing NY Guide

### Via Web
1. Go to http://localhost:5000/court-training
2. Click "🗽 New York Guide" in sidebar
3. Browse comprehensive NY tenant law information

### Via API
```bash
# Validate NY document
curl -X POST http://localhost:5000/api/court-training/validate-document \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type":"petition",
    "case_type":"eviction",
    "filed_date":"2025-11-05",
    "signature_present":true,
    "filing_fee_paid":true,
    "service_documented":true
  }'
```

---

## States Now Supported

✅ **Minnesota (MN)**
- 20-day response deadline
- 30-day Notice to Quit
- Notarization required for affidavits
- Statute of limitations tracking

✅ **New York (NY)**
- 30-day response deadline
- 5-day answer deadline (strict)
- 10-day demand + 30-day Notice to Quit
- No notarization for filings
- Marshal fee required
- Housing Court option (NYC)
- Habitability warranty (non-waivable)

---

## Future State Additions

To add more states, update `COURT_RULES` in `court_ai_trainer.py`:

```python
"CA": {  # California
    "response_deadline_days": 30,
    "notice_requirement_days": 3,
    # ... other CA-specific rules
}

"TX": {  # Texas
    "response_deadline_days": 20,
    "notice_requirement_days": 3,
    # ... other TX-specific rules
}
```

---

## Testing Results

✅ **Route Tests**
- GET /court-training → Status 200
- New York Guide section loads ✅
- Sidebar shows "🗽 New York Guide" ✅

✅ **API Tests**
- `GET /api/court-training/generate-clerk-prompt?state=NY` → Returns NY rules ✅
- NY response deadline: 30 days ✅
- NY answer deadline: 5 days ✅
- NY notice requirement: 3 days ✅

---

## Key NY Differences from MN

| Feature | MN | NY |
|---------|----|----|
| Response Deadline | 20 days | 30 days |
| Answer Deadline | N/A | 5 days (strict) |
| Notice to Quit | 30 days | 30 days |
| Demand Notice | N/A | 10 days required |
| Notarization Required | Yes | No |
| Habitability Waivable | No | No |
| Retaliation Window | Varies | 6 months |
| Court Type | District Court | Civil/Supreme/Housing |
| Marshal Fee | N/A | Required ($300-500) |

---

## Production Status

✅ **New York Support: PRODUCTION READY**

- Court rules configured
- Training section comprehensive
- API endpoints working
- AI prompts generated correctly
- Ready for tenant use

**Access:** http://localhost:5000/court-training

---

**Added:** November 5, 2025
**Status:** ✅ Fully Operational
**Next:** Can add additional states (CA, TX, IL, etc.) following same pattern
