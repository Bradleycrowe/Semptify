# Background Check - What User Sees vs What System Does

## 🎯 Philosophy: Simplified User Experience

**User sees:** Simple form → Submit → Result (Approved/Denied/Review)
**System does:** Complex verification, scoring, learning, compliance (all hidden)

---

## ✅ What User MUST Provide (Input Form)

### Basic Information
- **Full Legal Name** (as it appears on ID)
- **Date of Birth** (MM/DD/YYYY)
- **Social Security Number** (for identity verification)
  - _Note: "We use this only to verify your identity and check rental history. It's encrypted and never shared."_
- **Current Address**
- **Previous Addresses** (last 2 years)
  - Address line
  - Dates lived there (from - to)

### Consent
- **☐ Checkbox:** "I authorize [Property/Landlord] to obtain a background check including credit, criminal, and eviction records. I understand this is required to process my application."
- **Signature or Click to Agree**

### Optional (if applicable)
- **Driver's License or State ID Number** (for faster verification)
- **Income Information** (if not provided separately)
  - Monthly income amount
  - Employer name (optional)

---

## 📊 What User SEES After Submission

### Simple Status Screen

#### Example 1: Approved ✅
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Application Status: APPROVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your application has been approved!

Next Steps:
→ Sign your lease within 5 days
→ Schedule move-in inspection
→ Pay security deposit ($1,500)

Questions? Call us at 555-1234
```

#### Example 2: Needs Review ⚠️
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Application Status: UNDER REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We need to review your application.

What this means:
• We found information that requires manual review
• This is normal and does not mean denial
• A staff member will contact you within 2 business days

You may be asked to:
• Provide additional documentation
• Explain certain items on your record
• Consider a co-signer

We'll contact you at: your_email@example.com
```

#### Example 3: Conditional Approval 🟡
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Application Status: CONDITIONAL APPROVAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You're approved with conditions:

Required:
☐ Provide a qualified co-signer
☐ Increased security deposit: $2,500 (instead of $1,500)

If you complete these within 7 days, you're approved!

Questions? Call us at 555-1234
```

#### Example 4: Denied ❌
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Application Status: NOT APPROVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Unfortunately, we cannot approve your application at this time.

Reason:
Your application did not meet our rental criteria.

Your Rights:
• You will receive a detailed letter within 7 days explaining the decision
• You have the right to dispute any inaccurate information
• You can request a copy of your background report

Resources:
→ Tenant Rights Hotline: 866-866-3546
→ Dispute Process: [Link]
→ Find a Co-Signer Program: [Link]

This is not a reflection of your character. Keep looking!
```

---

## 🚫 What User NEVER Sees (Backend Only)

### Things Hidden from User View:
- ❌ Raw credit scores (640, 720, etc.)
- ❌ Vendor names (SafeScreen, Experian, etc.)
- ❌ Automated risk scores (0.42, 0.78, etc.)
- ❌ Processing steps ("Querying vendor...", "Hashing SSN...", "Computing score...")
- ❌ Internal decision reasons ("eviction 2021; insufficient income")
- ❌ Compliance logging details
- ❌ Which databases were searched
- ❌ Raw criminal/eviction record details
- ❌ Comparison to other applicants

### System Does (Silently):
1. Encrypts SSN immediately
2. Hashes identifiers
3. Queries multiple vendors (credit, criminal, eviction)
4. Computes automated risk score
5. Applies landlord criteria rules
6. Logs everything for compliance
7. Stores de-identified data for learning
8. Triggers pre-adverse notice workflow (if required by law)
9. Updates location intelligence statistics
10. Learns patterns for future predictions

---

## 📝 Example: Complete User Flow

### Step 1: User Fills Form
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Background Check Authorization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To process your application, we need to verify your rental history.

Full Name: [John Doe                    ]
Date of Birth: [MM] [DD] [YYYY]
SSN: [***-**-1234]

Current Address:
[123 Main St, Eagan, MN 55121        ]

Previous Address (if less than 2 years):
[456 Oak Ave, Minneapolis, MN 55401  ]
Lived here from: [01/2022] to [10/2024]

☑ I authorize this background check
☑ I certify this information is accurate

[Submit Application]
```

### Step 2: User Sees Loading (Brief)
```
Processing your application...
This usually takes 30-60 seconds.
```

### Step 3: User Gets Result (One of Above Examples)
```
Status: APPROVED ✅
Next Steps: Sign lease, pay deposit
```

---

## 🔐 Privacy Notice (Shown to User)

**What we check:**
- Identity verification
- Rental history (evictions)
- Credit history
- Criminal records (where legally permitted)

**How we protect your data:**
- All information is encrypted
- Only authorized staff can access reports
- We comply with Fair Credit Reporting Act (FCRA)
- Your SSN is never stored in plain text
- Reports are deleted according to our retention policy

**Your rights:**
- You can request a copy of your report
- You can dispute inaccurate information
- You will be notified if you're denied based on the report
- You can opt out of marketing uses

[View Full Privacy Policy]

---

## 💾 What System Stores (User Doesn't See)

### Backend Record (From Previous Analysis)
```json
{
  "record_id": "bg_12345",
  "application_id": "app_2025_000123",
  "user_id": "u123",
  "created_at": "2025-11-07T15:10:00Z",
  "consent_given": true,

  "identity": {
    "name_hash": "sha256$abc123...",
    "ssn_hash": "sha256$def456...",
    "dob_year": 1994
  },

  "screening": {
    "criminal_search": {"found": false},
    "eviction_search": {"found": false},
    "credit_report": {"score_bucket": "fair"},
    "identity_verification": {"verified": true}
  },

  "decision": {
    "status": "approved",
    "automated_score": 0.85,
    "risk_category": "low"
  }
}
```

**User sees:** "APPROVED ✅"
**User does NOT see:** The JSON above

---

## 🎨 UI Implementation Notes

### Input Form
```html
<!-- Simple, clean form -->
<form id="background-check-form">
  <h2>Background Check Authorization</h2>

  <input type="text" placeholder="Full Legal Name" required>
  <input type="date" placeholder="Date of Birth" required>
  <input type="text" placeholder="SSN" required pattern="\d{3}-\d{2}-\d{4}">

  <input type="text" placeholder="Current Address" required>

  <label>
    <input type="checkbox" required>
    I authorize this background check
  </label>

  <button type="submit">Submit Application</button>
</form>
```

### Result Display
```html
<!-- Simple status card -->
<div class="status-card approved">
  <h1>✅ Application Approved</h1>
  <p>Your application has been approved!</p>

  <h3>Next Steps:</h3>
  <ul>
    <li>Sign your lease within 5 days</li>
    <li>Pay security deposit ($1,500)</li>
  </ul>

  <button>Continue to Lease Signing</button>
</div>
```

---

## 📊 What Gets Learned (Behind the Scenes)

### From This Application, System Learns:
- Eagan, MN approval rate updates
- Income-to-rent ratio patterns
- Typical security deposit amounts
- Common approval conditions
- Time-to-decision metrics

### User Doesn't Know:
- Their data helped improve the system
- Statistics were aggregated (anonymously)
- Future applicants will benefit

---

## ✅ Summary: User Interface Philosophy

| What User Provides | What User Sees | What System Does (Hidden) |
|-------------------|----------------|---------------------------|
| Name, DOB, SSN | "Processing..." | Encrypt, hash, query vendors |
| Consent checkbox | Simple status | Complex scoring, compliance logging |
| Address history | Next steps | Learn patterns, update statistics |
| - | Resources (if denied) | Suggest procedures from learned data |

**Goal:** User has simple, clear experience. System does all complex work invisibly.

---

## 🚀 Implementation Checklist

- [ ] Create simple input form (name, DOB, SSN, addresses, consent)
- [ ] Add "Processing..." spinner (hide all backend steps)
- [ ] Show ONLY final status: Approved/Denied/Review/Conditional
- [ ] Provide clear next steps for each status
- [ ] Never show raw scores, vendor names, or processing details
- [ ] Store everything needed in backend (from previous schema)
- [ ] Emit learning events (de-identified) silently
- [ ] Handle legal notices (pre-adverse) automatically
- [ ] Provide simple "Dispute" link if needed

**User Experience:** "It just works" ✨
