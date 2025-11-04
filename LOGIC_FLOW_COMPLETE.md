# 🔄 Semptify Logic & Flow - Complete Pathways & Decision Trees

Comprehensive diagrams showing how actions flow through Semptify with decision points, reactions, and system responses.

---

## 🎯 Core Principle: Action → Ledger → Reactions → Calendar

```
┌──────────────────────────────────────────────────────────────────┐
│                      SEMPTIFY CORE FLOW                          │
└──────────────────────────────────────────────────────────────────┘

USER ACTION
    ↓
    ├─ Input: What is happening?
    ├─ Qualifiers: Who? What? When? Why? Context?
    └─ System checks rules
    
    ↓
    
LEDGER ENTRY
    ├─ Record: Timestamp, Actor, Type
    ├─ Hash: SHA256 for tamper-proof
    ├─ Certificate: JSON for audit trail
    └─ Store: Append-only to events.log
    
    ↓
    
SYSTEM RULES
    ├─ Check: What type of action?
    ├─ Check: What is the context?
    ├─ Decide: What reactions needed?
    └─ Execute: Suggestions, notifications, next steps
    
    ↓
    
CALENDAR EVENT
    ├─ Schedule: Next deadline/reminder
    ├─ Priority: Based on urgency
    ├─ Link: To ledger entry (related_entry_id)
    └─ Notify: User sees in calendar
    
    ↓
    
UI DISPLAY
    └─ Show: Suggestion, status, next steps
```

---

## 📊 Decision Tree: User Uploads Document

```
┌─────────────────────────────────────┐
│ USER UPLOADS DOCUMENT               │
│ Action: upload_document(file.pdf)   │
└────────────┬────────────────────────┘
             │
             ↓
    ┌────────────────────┐
    │ VALIDATE FILE      │
    ├────────────────────┤
    │ - File size OK?    │
    │ - Format OK?       │
    │ - Scan for malware?│
    └────────┬───────────┘
             │
        ┌────┴────┐
        │          │
       NO         YES
        │          │
        ↓          ↓
    ┌──────┐  ┌──────────────────┐
    │ERROR │  │ COMPUTE HASH     │
    │Return│  │ SHA256(file)     │
    └──────┘  └────────┬─────────┘
                       │
                       ↓
             ┌──────────────────────┐
             │ CREATE LEDGER ENTRY  │
             ├──────────────────────┤
             │ - Type: "document"   │
             │ - Timestamp: now()   │
             │ - SHA256: hash       │
             │ - Certificate: JSON  │
             │ - Actor: user_id     │
             └────────┬─────────────┘
                      │
                      ↓
          ┌───────────────────────┐
          │ ANALYZE DOCUMENT TYPE │
          └────────┬──────────────┘
                   │
         ┌─────────┼─────────┬──────────┬──────────┐
         │         │         │          │          │
         ↓         ↓         ↓          ↓          ↓
    ┌────────┐ ┌────────┐ ┌───────┐ ┌───────┐ ┌────────┐
    │RECEIPT?│ │NOTICE? │ │LEASE? │ │PHOTO? │ │ OTHER? │
    └───┬────┘ └───┬────┘ └───┬───┘ └───┬───┘ └───┬────┘
        │          │          │        │         │
        │          │          │        │         │
    YES│      YES│     YES│   YES│  │
        │          │          │        │         │
        ↓          ↓          ↓        ↓         ↓
    ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
    │UPDATE│  │CHECK │  │UPDATE│  │ADD TO│  │STORE │
    │LEDGER│  │DEAD- │  │LEASE │  │EVID- │  │VAULT │
    │PAYMENT
    │ STATUS│  │LINES │  │INFO  │  │ENCE  │  │      │
    └───┬──┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
        │        │         │        │         │
        │        │         │        │         │
        └─────┬──┴─────┬───┴──┬────┴────┬────┴───┐
              │        │      │         │        │
              ↓        ↓      ↓         ↓        ↓
        ┌──────────────────────────────────────────┐
        │ TRIGGER RULES                            │
        │ (Based on document type & context)       │
        └──────────────────────────────────────────┘
              │
              ↓
    ┌─────────────────────────────────────┐
    │ APPLY BUSINESS LOGIC                │
    ├─────────────────────────────────────┤
    │ IF document=receipt:                │
    │   - Check: Is payment on time?      │
    │   - Check: Is amount correct?       │
    │   - Check: Any late fees?           │
    │   - Suggest: Mark as evidence       │
    │                                     │
    │ IF document=notice:                 │
    │   - Check: Deadline to respond      │
    │   - Schedule: Follow-up calendar    │
    │   - Suggest: Next action            │
    │   - Priority: HIGH                  │
    │                                     │
    │ IF document=lease:                  │
    │   - Extract: Key dates              │
    │   - Schedule: Renewal reminder      │
    │   - Store: For reference            │
    │                                     │
    │ IF document=photo/evidence:         │
    │   - Add: To evidence packet         │
    │   - Group: With related photos      │
    │   - Export: For legal use           │
    └─────────────────────────────────────┘
              │
              ↓
    ┌─────────────────────────────────────┐
    │ CREATE CALENDAR EVENT (if needed)   │
    ├─────────────────────────────────────┤
    │ Title: Based on document type       │
    │ Date: Deadline or reminder          │
    │ Priority: Based on urgency          │
    │ Type: deadline/reminder/action      │
    │ Related: Links to ledger entry      │
    └────────────┬────────────────────────┘
                 │
                 ↓
    ┌──────────────────────────────┐
    │ DISPLAY SUGGESTION TO USER   │
    ├──────────────────────────────┤
    │ "Document uploaded!"         │
    │ Type: Receipt                │
    │ Status: Payment on time ✓    │
    │ Next: Consider uploading     │
    │        evidence photos       │
    └──────────────────────────────┘
```

---

## 💰 Decision Tree: Rent Payment Scenario

```
┌────────────────────────────────────────┐
│ SCENARIO: RENT PAYMENT                 │
│ User uploads rent receipt               │
└────────────┬─────────────────────────────┘
             │
             ↓
    ┌────────────────────┐
    │ EXTRACT FROM FILE  │
    ├────────────────────┤
    │ - Amount: $1,200   │
    │ - Date: Nov 1      │
    │ - Landlord: Bob's  │
    │ - Reference: CK123 │
    └────────┬───────────┘
             │
             ↓
    ┌──────────────────────────┐
    │ LEDGER: Record Payment   │
    ├──────────────────────────┤
    │ Type: payment            │
    │ Amount: $1,200           │
    │ Date: Nov 1, 2025        │
    │ Reference: Check #123    │
    │ Hash: SHA256(receipt)    │
    │ Actor: Tenant            │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ CHECK: Payment Status        │
    └────────┬─────────────────────┘
             │
    ┌────────┴────────┬──────────────┬──────────────┐
    │                 │              │              │
    ↓                 ↓              ↓              ↓
 ┌────────┐      ┌────────┐     ┌────────┐    ┌────────┐
 │ON TIME?│      │LATE?   │     │EARLY?  │    │MISSING?│
 │Due 11/1│      │Due 11/1│     │Due 11/1│    │Due 11/1│
 │Paid:11/1      │Paid:11/5     │Paid:10/28  │No record
 └────┬───┘      └────┬───┘     └────┬───┘   └────┬───┘
      │YES           │YES           │YES         │NO
      │              │              │            │
      ↓              ↓              ↓            ↓
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ MARK:    │  │ MARK:    │  │ MARK:    │  │ ALERT:   │
  │Compliant │  │ LATE     │  │Early/    │  │Missing   │
  │ ✓        │  │ ⚠️       │  │ Prompt   │  │ Payment  │
  │          │  │          │  │ ✓        │  │ ❌       │
  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │              │             │
       │             │              │             │
       └────┬────────┴──────────┬───┴────────┬────┘
            │                  │            │
            ↓                  ↓            ↓
       ┌──────────────────────────────────────────┐
       │ CALENDAR EVENTS                          │
       ├──────────────────────────────────────────┤
       │ ON TIME: No action needed                │
       │ - Optional: Remind for next month        │
       │ - Date: December 1, 2025                 │
       │ - Priority: LOW                          │
       │ - Type: reminder                         │
       │                                          │
       │ LATE: URGENT ACTION NEEDED               │
       │ - Event 1: "Pay late fee?"               │
       │   Date: NOW, Priority: HIGH, Type: action
       │                                          │
       │ - Event 2: "Contact landlord"            │
       │   Date: NOW, Priority: HIGH              │
       │   Type: action_needed                    │
       │                                          │
       │ - Event 3: "Document delay"              │
       │   Date: NOW+30 days                      │
       │   Priority: MEDIUM, Type: reminder       │
       │   (For future dispute)                   │
       │                                          │
       │ EARLY: No action needed                  │
       │ - Optional: Congratulation              │
       │ - Note: Marked as paid early             │
       │                                          │
       │ MISSING: URGENT ACTION NEEDED            │
       │ - Event 1: "Send payment ASAP"           │
       │   Date: NOW, Priority: HIGH              │
       │ - Event 2: "Risk: Eviction notice"       │
       │   Date: NOW+30 days                      │
       │   Priority: CRITICAL                     │
       └──────────────────────────────────────────┘
            │
            ↓
       ┌──────────────────────────────────┐
       │ SUGGESTIONS TO USER              │
       ├──────────────────────────────────┤
       │ ON TIME:                         │
       │ ✓ Payment recorded               │
       │ ✓ Ledger updated                 │
       │ Next: Upload next payment on 12/1
       │                                  │
       │ LATE:                            │
       │ ⚠️  Payment is 4 days late        │
       │ ⚠️  Late fees may apply           │
       │ → Action: Pay immediately        │
       │ → Suggested: Send notice         │
       │   "Payment received [date]"      │
       │                                  │
       │ MISSING:                         │
       │ ❌ No payment found              │
       │ ❌ Overdue by X days             │
       │ → Action: Pay immediately       │
       │ → Risk: Eviction notice possible │
       │ → Suggested: Contact landlord    │
       │             and arrange payment  │
       └──────────────────────────────────┘
            │
            ↓
       ┌──────────────────────────────────┐
       │ EVIDENCE TRACKING                │
       ├──────────────────────────────────┤
       │ All payments recorded in ledger: │
       │ Jan: ✓ $1,200 (on time)         │
       │ Feb: ✓ $1,200 (on time)         │
       │ Mar: ✓ $1,200 (on time)         │
       │ Apr: ⚠️ $1,200 (5 days late)    │
       │ May: ✓ $1,200 (on time)         │
       │ Jun: ❌ MISSING                  │
       │ Jul: ✓ $1,200 (on time)         │
       │                                  │
       │ Usable as EVIDENCE in disputes:  │
       │ - Shows payment pattern          │
       │ - Shows occasional delays        │
       │ - Shows good faith efforts       │
       │ - Protects tenant if landlord    │
       │   claims non-payment             │
       └──────────────────────────────────┘
```

---

## 📋 Decision Tree: Complaint Process

```
┌────────────────────────────────┐
│ USER FILES COMPLAINT           │
│ Example: Broken heater         │
└────────┬────────────────────────┘
         │
         ↓
    ┌─────────────────────────┐
    │ INPUT: Complaint Info   │
    ├─────────────────────────┤
    │ - Issue: Heating broken │
    │ - Date reported: Now    │
    │ - Severity: High        │
    │ - Impact: No heat       │
    │ - Duration: 3 days      │
    └────────┬────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │ LEDGER: Record Complaint │
    ├──────────────────────────┤
    │ Type: complaint          │
    │ Issue: heating           │
    │ Date: Nov 4, 2025        │
    │ Severity: high           │
    │ Actor: tenant            │
    │ Hash: SHA256(complaint)  │
    └────────┬─────────────────┘
             │
             ↓
    ┌───────────────────────────────┐
    │ CHECK: LOCAL RULES            │
    └────────┬──────────────────────┘
             │
    ┌────────┴──────────────┐
    │                       │
    ↓                       ↓
 ┌────────┐            ┌────────┐
 │Heating │            │Code    │
 │Required?│           │Says?   │
 │ YES    │            │70°F    │
 └───┬────┘            │min     │
     │                 └───┬────┘
     │                     │
     └─────────┬───────────┘
               │
               ↓
    ┌──────────────────────────────────┐
    │ DECIDE: What to do?              │
    ├──────────────────────────────────┤
    │ Heating broken = Habitability    │
    │ Issue = YES, urgent              │
    │ Legal right = YES                │
    │ Next step = NOTIFY LANDLORD      │
    └────────┬─────────────────────────┘
             │
             ↓
    ┌────────────────────────────────────┐
    │ SYSTEM SUGGESTS:                   │
    ├────────────────────────────────────┤
    │ Step 1: Send notice to landlord    │
    │         (48-72 hour deadline)      │
    │                                    │
    │ Step 2: If no response:            │
    │         File formal complaint      │
    │                                    │
    │ Step 3: If still no fix:           │
    │         Repair & deduct option     │
    │         OR file with housing board │
    │                                    │
    │ Step 4: Gather evidence:           │
    │         - Photos/videos           │
    │         - Temperature readings    │
    │         - Communication log       │
    │         - Repair receipts         │
    └────────┬─────────────────────────┘
             │
             ↓
    ┌──────────────────────────────────┐
    │ CREATE CALENDAR EVENTS           │
    ├──────────────────────────────────┤
    │ Event 1: SEND NOTICE             │
    │ - Title: "Send notice to landlord"
    │ - Due: TODAY                     │
    │ - Priority: 2 (HIGH)            │
    │ - Type: action_needed           │
    │                                  │
    │ Event 2: FOLLOW UP               │
    │ - Title: "Check if fixed"        │
    │ - Due: 3 days from now           │
    │ - Priority: 2 (HIGH)            │
    │ - Type: reminder                │
    │ - If not fixed → escalate        │
    │                                  │
    │ Event 3: DOCUMENT EVIDENCE       │
    │ - Title: "Take photos/video"     │
    │ - Due: TODAY                     │
    │ - Priority: 1 (MEDIUM)          │
    │ - Type: action_needed           │
    │                                  │
    │ Event 4: FILE FORMAL COMPLAINT   │
    │ - Title: "File complaint"        │
    │ - Due: 30 days from now          │
    │ - Priority: 2 (HIGH)            │
    │ - Type: deadline                │
    │ - Only if not fixed              │
    └────────┬─────────────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ GENERATE DOCUMENTS           │
    ├──────────────────────────────┤
    │ Document 1: NOTICE TEMPLATE  │
    │ - To: [landlord_name]        │
    │ - From: [tenant_name]        │
    │ - Issue: Heating broken      │
    │ - Demand: Fix within 48 hrs  │
    │ - Consequence: Will file     │
    │   complaint/seek relief      │
    │                              │
    │ Document 2: EVIDENCE SHEET   │
    │ - Date complained: Nov 4     │
    │ - Issue reported: Nov 1      │
    │ - Days without service: 3    │
    │ - Photos: (links)            │
    │ - Temperature log: (links)   │
    └────────┬─────────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ USER SEES DASHBOARD:         │
    ├──────────────────────────────┤
    │ Complaint Status: Active     │
    │ Issue: Heating               │
    │ Days unresolved: 3           │
    │ Actions: 4 pending           │
    │                              │
    │ URGENT: Send notice today    │
    │         ► Generate           │
    │         ► Print              │
    │         ► Send (certified)   │
    │                              │
    │ Then: Gather evidence        │
    │ Then: Monitor for 48 hours   │
    │ Then: Escalate if needed     │
    └──────────────────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ TIMELINE FOR EVIDENCE:       │
    ├──────────────────────────────┤
    │ Day 1 (Nov 1): Issue found   │
    │ ↓ Ledger entry #1           │
    │                              │
    │ Day 4 (Nov 4): Complaint filed
    │ ↓ Ledger entry #2           │
    │ ↓ Notice generated           │
    │ ↓ Calendar events created    │
    │                              │
    │ Day 4 (Nov 4): Notice sent   │
    │ ↓ Ledger entry #3           │
    │ ↓ Certified mail             │
    │                              │
    │ Day 5-6: Collect evidence    │
    │ ↓ Photos added to ledger     │
    │ ↓ Videos added to ledger     │
    │ ↓ Linked to complaint entry  │
    │                              │
    │ Day 7 (Nov 11): DEADLINE     │
    │ ↓ Landlord must respond      │
    │ ↓ If no response: Escalate   │
    │ ↓ Calendar event triggers    │
    │                              │
    │ Complete audit trail for:    │
    │ - Dispute resolution         │
    │ - Housing court              │
    │ - Small claims court         │
    │ - Settlement negotiations    │
    └──────────────────────────────┘
```

---

## 📸 Decision Tree: Evidence Collection

```
┌────────────────────────────────┐
│ USER UPLOADS EVIDENCE          │
│ Types: Photos, videos, docs    │
└────────┬────────────────────────┘
         │
         ↓
    ┌──────────────────────────┐
    │ PROCESS EACH FILE        │
    ├──────────────────────────┤
    │ - Validate format        │
    │ - Compute SHA256         │
    │ - Extract metadata       │
    │ - Create certificate     │
    │ - Store securely         │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────────┐
    │ ANALYZE: What is this?       │
    └────────┬─────────────────────┘
             │
    ┌────────┬────────┬────────┬──────────┐
    │        │        │        │          │
    ↓        ↓        ↓        ↓          ↓
 ┌──────┐┌──────┐┌──────┐┌────────┐┌────────┐
 │PHOTO ││VIDEO ││LEASE ││NOTICE  ││RECEIPT │
 │of    ││of    ││copy  ││signed  ││of      │
 │damage││damage││      ││by      ││payment │
 └──┬───┘└──┬───┘└──┬───┘└───┬────┘└───┬────┘
    │       │       │        │         │
    │       │       │        │         │
    └───────┼───────┼────────┼─────────┘
            │       │        │
            ↓       ↓        ↓
       ┌──────────────────────────┐
       │ GROUP BY CATEGORY        │
       ├──────────────────────────┤
       │ Photos: [5 files]        │
       │ Videos: [2 files]        │
       │ Documents: [8 files]     │
       └────────┬─────────────────┘
                │
                ↓
       ┌──────────────────────────┐
       │ LINK TO LEDGER ENTRIES   │
       ├──────────────────────────┤
       │ All files linked to:     │
       │ - Original complaint     │
       │ - Notice sent            │
       │ - Communication log      │
       └────────┬─────────────────┘
                │
                ↓
       ┌──────────────────────────┐
       │ CREATE EVIDENCE PACKET   │
       ├──────────────────────────┤
       │ Packet ID: EVP-001       │
       │ Type: Maintenance issue  │
       │ Status: Active           │
       │ Files: 15 items          │
       │ Total size: 250 MB       │
       │ Created: Nov 4, 2025     │
       │ All files hashed         │
       │ All files certified      │
       └────────┬─────────────────┘
                │
                ↓
       ┌──────────────────────────────────┐
       │ GENERATE EVIDENCE REPORT         │
       ├──────────────────────────────────┤
       │ MAINTENANCE ISSUE EVIDENCE       │
       │                                  │
       │ Issue: Broken heating system     │
       │ Date discovered: Nov 1, 2025     │
       │ Days unresolved: 3               │
       │                                  │
       │ EVIDENCE COLLECTED:              │
       │ ✓ Photo 1: Thermostat broken     │
       │ ✓ Photo 2: No heat visible       │
       │ ✓ Video: Temperature at 55°F     │
       │ ✓ Document: Lease (heat required)
       │ ✓ Document: Notice to landlord   │
       │ ✓ Document: Email correspondence │
       │                                  │
       │ COURT-ADMISSIBLE:                │
       │ ✓ All files hashed (SHA256)      │
       │ ✓ All files timestamped         │
       │ ✓ Chain of custody maintained   │
       │ ✓ Tamper-proof certificates     │
       │ ✓ Export ready for legal use    │
       └──────────────────────────────────┘
                │
                ↓
       ┌────────────────────────────────┐
       │ CALENDAR EVENT CREATED         │
       ├────────────────────────────────┤
       │ Title: Evidence collected      │
       │ Date: Nov 4, 2025              │
       │ Type: Completed ✓              │
       │ Note: Ready for dispute        │
       │                                │
       │ Next event: File complaint     │
       │ If landlord doesn't fix        │
       │ Date: Nov 11, 2025             │
       │ Priority: HIGH                 │
       │ Type: Deadline                 │
       └────────────────────────────────┘
```

---

## 🎯 Master Flow: Complete Tenant Action Sequence

```
┌──────────────────────────────────────────────────────────┐
│         COMPLETE TENANT DISPUTE TIMELINE                 │
└──────────────────────────────────────────────────────────┘

DAY 1: ISSUE DISCOVERED
┌──────────────────────────────────────┐
│ Action: Tenant discovers broken heat │
│ Input: "It's cold in here"           │
└──────────────────────────────────────┘
         ↓
    LEDGER ENTRY #1
    Type: Issue report
    Description: Heating not working
    Timestamp: Nov 1, 10:00 AM
         ↓
    CALENDAR EVENT #1
    Title: "Get temperature reading"
    Priority: MEDIUM
    Due: Today


DAY 2-3: DOCUMENT ISSUE
┌──────────────────────────────────────┐
│ Action: Take photos/videos           │
│ Input: Upload 5 photos + 1 video     │
└──────────────────────────────────────┘
         ↓
    LEDGER ENTRY #2-7
    Type: Evidence
    Files: photos + video (hashed)
    All linked to Entry #1
         ↓
    CALENDAR EVENT #2
    Title: "Send notice to landlord"
    Priority: HIGH
    Due: Tomorrow (Day 4)


DAY 4: SEND NOTICE
┌──────────────────────────────────────┐
│ Action: Send formal notice           │
│ System: Generated demand letter       │
└──────────────────────────────────────┘
         ↓
    LEDGER ENTRY #8
    Type: Notice
    Description: Certified notice sent
    Reference: "USPS Cert #ABC123"
         ↓
    CALENDAR EVENT #3
    Title: "Check if landlord responded"
    Priority: HIGH
    Due: 3 days (Day 7)
         ↓
    CALENDAR EVENT #4
    Title: "File formal complaint"
    Priority: HIGH
    Due: 30 days (Day 34) if not fixed


DAY 7: CHECK FOR RESPONSE
┌──────────────────────────────────────┐
│ Calendar reminds: "Have they fixed?" │
└──────────────────────────────────────┘
         ↓
    IF FIXED:
    └─ LEDGER ENTRY #9: "Issue resolved"
       CALENDAR EVENT: Mark complete ✓
       Status: Compliant
    
    IF NOT FIXED:
    └─ LEDGER ENTRY #9: "No response"
       CALENDAR EVENT #5: (escalate)
       Title: "Initiate formal complaint"
       Priority: CRITICAL
       Due: Immediately


DAY 7+: ESCALATE (IF NEEDED)
┌──────────────────────────────────────┐
│ Action: File formal complaint        │
│ System: Complaint form auto-filled   │
└──────────────────────────────────────┘
         ↓
    LEDGER ENTRY #10
    Type: Complaint
    Details: Formal complaint filed
    Date: Day 7+
         ↓
    ATTACH EVIDENCE PACKET:
    - All photos (hashes verified)
    - All videos (certificates)
    - All notices (timestamps)
    - Lease agreement
    - Email correspondence
    - Timeline of events
         ↓
    EVIDENCE PACKET STATUS:
    ✓ Complete audit trail
    ✓ All timestamps verified
    ✓ All files hashed (tamper-proof)
    ✓ Chain of custody maintained
    ✓ Court-ready export


FINAL RESULT: COMPLETE RECORD
┌────────────────────────────────────────────┐
│ LEDGER (Immutable Timeline):               │
│ 1. Issue discovered (Nov 1)                │
│ 2. Evidence collected (Nov 2-3)            │
│ 3. Notice sent (Nov 4)                     │
│ 4. No response (Nov 7)                     │
│ 5. Formal complaint (Nov 7+)               │
│                                            │
│ CALENDAR (Action Schedule):                │
│ - Document evidence: Nov 2-3               │
│ - Send notice: Nov 4 (COMPLETED)          │
│ - Follow up: Nov 7 (COMPLETED)            │
│ - File complaint: Nov 7+ (COMPLETED)      │
│ - Hearing: (scheduled after filing)       │
│                                            │
│ EVIDENCE PACKET (Court-Admissible):       │
│ - Photos: 5 files, all hashed             │
│ - Videos: 1 file, certified               │
│ - Documents: 8 files, timestamped         │
│ - Correspondence: Full email chain        │
│ - SHA256 hashes: All verified             │
│ - Certificates: All generated             │
│ - Ready for: Housing court, mediation     │
│                                            │
│ TENANT STATUS:                             │
│ ✓ Full documentation                      │
│ ✓ Proof of good faith effort              │
│ ✓ Evidence of landlord non-response       │
│ ✓ Proof of violation (habitability)       │
│ ✓ Ready for legal action                  │
└────────────────────────────────────────────┘
```

---

## 🔗 System Integration Flow

```
┌──────────────────────────────────────────────────────────┐
│          HOW MODULES FEED INTO LEDGER/CALENDAR           │
└──────────────────────────────────────────────────────────┘

OFFICE MODULE
├─ User creates room
├─ Logs: Ledger entry (new room)
├─ Schedule: Calendar event (setup reminder)
└─ Flow: room_created → log_action() → schedule_event()

LAW NOTES MODULE
├─ User generates complaint
├─ Logs: Ledger entry (complaint filed)
├─ Schedule: Calendar event (deadline to serve)
├─ Attach: Evidence packet (all linked)
└─ Flow: file_complaint() → log_action() + log_evidence() → schedule_event()

AI ORCHESTRATOR
├─ AI processes request
├─ Logs: Ledger entry (AI decision)
├─ Suggests: Next calendar event
├─ Output: Recommendation + calendar
└─ Flow: orchestrate() → record_event() → suggest_next_action()

VAULT MODULE (Evidence)
├─ User uploads file
├─ Logs: Ledger entry (file uploaded)
├─ Hashes: SHA256 of file
├─ Certificates: JSON audit trail
├─ Links: To related ledger entries
└─ Flow: upload_file() → create_cert() → link_to_entry()

GUI DESKTOP APP
├─ User performs action (create room, upload doc)
├─ Logs: Ledger entry (action recorded)
├─ Schedule: Calendar event (next step)
├─ Display: Suggestion UI
└─ Flow: user_action() → log_action() → display_suggestion()

ALL MODULES →  CENTRAL LEDGER → RULES ENGINE → CALENDAR
                  (immutable)    (logic)       (actions)
```

---

## 📋 Qualifier Checklist: Every Action

```
┌───────────────────────────────────────────────────────┐
│ BEFORE LOGGING ANY ACTION, CHECK THESE QUALIFIERS:   │
└───────────────────────────────────────────────────────┘

WHO?
┌─────────────────────────────────┐
│ - Tenant ID: u4a7c9d2b          │
│ - Landlord: (if applicable)     │
│ - Staff/Admin: (if applicable)  │
│ - System: (if auto-triggered)   │
└─────────────────────────────────┘

WHAT?
┌─────────────────────────────────┐
│ - Action type: payment/notice/  │
│   complaint/evidence/action     │
│ - Details: full description     │
│ - Context: what triggered it    │
└─────────────────────────────────┘

WHEN?
┌─────────────────────────────────┐
│ - Current timestamp: NOW()      │
│ - Event date: (if different)    │
│ - Deadline: (if applicable)     │
│ - Duration: start → end (time)  │
└─────────────────────────────────┘

WHY?
┌─────────────────────────────────┐
│ - Reason: legal/practical/other │
│ - Goal: what trying to achieve  │
│ - Legal basis: law/lease clause │
│ - Impact: what happens next     │
└─────────────────────────────────┘

CONTEXT?
┌─────────────────────────────────┐
│ - Room/Property: location       │
│ - Jurisdiction: state/local     │
│ - Legal status: in dispute?     │
│ - Priority: low/med/high        │
│ - Related entries: link IDs     │
└─────────────────────────────────┘

AFTER ANSWERING ALL:
Log entry → Check rules → Suggest reactions → Create calendar event
```

---

## 🎬 Reaction Rules Matrix

```
┌────────────────────────────────────────────────────────┐
│ ACTION TYPE → REACTIONS (What happens next?)          │
└────────────────────────────────────────────────────────┘

ACTION: Upload rent receipt
REACTIONS:
├─ Log: Ledger entry (payment recorded)
├─ Check: On time? Late? Early?
├─ If late: 
│  ├─ Flag: WARNING in UI
│  ├─ Schedule: "Pay late fees?" calendar event
│  └─ Suggest: Contact landlord
├─ If on time:
│  ├─ Mark: COMPLIANT ✓
│  ├─ Schedule: Next month reminder
│  └─ No action needed
└─ Export: For dispute evidence


ACTION: File complaint
REACTIONS:
├─ Log: Ledger entry (complaint filed)
├─ Generate: Demand letter (if not sent)
├─ Schedule: Deadline to respond (calendar)
├─ Schedule: Follow-up reminder (3 days)
├─ Attach: Evidence packet (link existing)
├─ Suggest: Next steps (file formal, etc.)
└─ Export: Complaint + evidence package


ACTION: Upload evidence photos
REACTIONS:
├─ Log: Ledger entry (evidence uploaded)
├─ Hash: SHA256 of each file
├─ Cert: JSON certificate for each
├─ Group: With related evidence
├─ Link: To related complaint/ledger entry
├─ Count: Update evidence packet totals
├─ Suggest: "Evidence complete? Ready to file?"
└─ Export: As evidence packet


ACTION: Generate legal letter
REACTIONS:
├─ Log: Ledger entry (letter generated)
├─ Store: Letter in vault (with cert)
├─ Suggest: "Print & send certified mail"
├─ Schedule: "Check if received" (calendar)
├─ Track: Mail tracking number (if provided)
├─ Link: To relevant complaint/entry
└─ Export: For court records


ACTION: Mark deadline as complete
REACTIONS:
├─ Log: Ledger entry (action completed)
├─ Update: Calendar event status
├─ Schedule: Next step (if applicable)
├─ Check: Related entries (cascade effects)
├─ Notify: User (action completed!)
└─ Suggest: "What's next?"
```

---

## ✨ Summary: Logic & Flow Blueprint

**Core Principle:**
```
User Action → Qualifiers Check → Ledger Entry → Rules Apply → Reactions → Calendar Event → UI Suggestion
```

**Every action flows through:**
1. **Input**: User does something
2. **Qualify**: Who? What? When? Why? Context?
3. **Log**: Immutable ledger entry with hash
4. **Analyze**: Check rules/business logic
5. **React**: Create calendar events, suggestions
6. **Display**: Show user what's next

**All connected:**
- Ledger = WHAT HAPPENED (timeline)
- Calendar = WHAT'S NEXT (actions)
- Evidence = PROOF (for disputes)
- Rules = LOGIC (if this, then that)
- UI = GUIDANCE (next steps for user)

