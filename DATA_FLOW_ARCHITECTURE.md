# Semptify Data Flow Architecture

## Calendar as Central Hub

The **Calendar** is the central processing hub for all module data. Every action, document, and decision routes through the calendar with:

### 1. **Timestamps** (WHEN)
- Exact timestamp for every event
- Enables deadline tracking
- Supports temporal queries (upcoming events, past actions)
- ISO format for system interoperability

### 2. **Registry** (WHO/WHAT/WHY)
- **Who**: Actor ID (tenant, landlord, admin, system)
- **What**: Action type (upload, payment, complaint, evidence, notice)
- **Why**: Reason/context/legal requirement
- **Context**: Property, room, jurisdiction, status

### 3. **Data Processing** (LOGICAL FLOW)
- **Input**: Document/action arrives
- **Processing**: Rules applied (conditionals)
- **Output**: Reactions triggered (suggestions, notices, evidence packets)
- **Routing**: Results flow back through calendar

### 4. **Document IDs** (REFERENCES)
- Every document has unique ID
- Linked to calendar entry
- Tracked through processing chain
- Enables complete audit trail

### 5. **Function References** (HOW)
- Records which function triggered the entry
- Tracks function processing history
- Enables debugging and replay
- Supports function registry

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 SEMPTIFY CALENDAR (HUB)                     │
│                                                             │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │Timestamp │ Registry │  Data    │ Document │ Function  │ │
│  │ (WHEN)   │(WHO/WHY) │Processing│   IDs    │References │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ▲
             ┌─────────────┼─────────────┐
             │             │             │
        ┌────┴────┐   ┌────┴────┐   ┌───┴────┐
        │ OFFICE  │   │ LAW     │   │   AI   │
        │ MODULE  │   │ NOTES   │   │ORCH.   │
        └────┬────┘   └────┬────┘   └───┬────┘
             │             │             │
        Uploads      Complaints    Analysis
        Documents    Evidence      Results
        Payments     Notices       Suggestions
```

---

## Data Flow Examples

### Example 1: Rent Payment Upload
```
1. INPUT
   - Tenant uploads receipt.pdf
   - Function: upload_payment()

2. CALENDAR ENTRY CREATED
   - ID: entry-uuid-1
   - Timestamp: 2025-01-15T10:30:00Z
   - Actor: tenant-123
   - Doc ID: doc-uuid-1
   - Function: "upload_payment"
   - Type: "payment"
   - Context: {amount: 1200, date: "2025-01-01"}

3. RULES PROCESSING
   - Rule 1: is_payment? → YES
     → Log to ledger, update payment status
   - Rule 2: is_late_payment? → NO
     → Skip late notice
   - Rule 3: is_dispute? → NO
     → Skip evidence packet

4. CALENDAR EVENTS CREATED
   - Event 1: "Payment Recorded" (completed)
   - Event 2: "Next Payment Due" (deadline, 2025-02-01)

5. OUTPUT
   - Ledger entry with hash/certificate
   - Updated payment ledger
   - Calendar reminders set
```

### Example 2: Maintenance Complaint
```
1. INPUT
   - Tenant files complaint about broken AC
   - Function: file_complaint()

2. CALENDAR ENTRY CREATED
   - ID: entry-uuid-2
   - Timestamp: 2025-01-15T14:00:00Z
   - Actor: tenant-123
   - Doc IDs: [doc-complaint, doc-photo1, doc-photo2]
   - Function: "file_complaint"
   - Type: "complaint"
   - Context: {issue: "AC broken", photos: 2, severity: "high"}

3. RULES PROCESSING
   - Rule 1: is_complaint? → YES
     → Prepare evidence packet
   - Rule 2: severity > "medium"? → YES
     → Set high priority
   - Rule 3: needs_deadline? → YES
     → Landlord response due in 14 days

4. CALENDAR EVENTS CREATED
   - Event 1: "Complaint Filed" (deadline, today + 3 days for confirmation)
   - Event 2: "Landlord Response Due" (deadline, today + 14 days)
   - Event 3: "Prepare Evidence Packet" (action_needed, high priority)

5. OUTPUT
   - Complaint logged with all attachments
   - Evidence packet prepared and linked
   - Timeline tracked in calendar
   - Notifications sent to landlord
```

### Example 3: Legal Notice Generation
```
1. INPUT
   - System triggers due to unpaid rent (7 days late)
   - Function: generate_notice()

2. CALENDAR ENTRY CREATED
   - ID: entry-uuid-3
   - Timestamp: 2025-01-20T09:00:00Z
   - Actor: "system"
   - Input Doc IDs: [payment-ledger-doc]
   - Function: "generate_notice"
   - Type: "notice"
   - Context: {notice_type: "pay-or-quit", days_late: 7}

3. RULES PROCESSING
   - Rule 1: days_late >= 7? → YES
     → Generate formal notice
   - Rule 2: jurisdiction == "MN"? → YES
     → Use Minnesota law template
   - Rule 3: has_prior_complaints? → YES
     → Add to evidence file

4. CALENDAR EVENTS CREATED
   - Event 1: "Notice Generated" (action_needed, sent)
   - Event 2: "Tenant Response Due" (deadline, today + 5 days)
   - Event 3: "File with Court" (deadline, today + 10 days, if no payment)

5. OUTPUT
   - Notice document created (doc-notice-uuid)
   - Linked to ledger and calendar
   - Evidence packet updated
   - Court filing deadline tracked
```

---

## Module Integration Points

### Office Module → Calendar
```python
# When document uploaded
@app.route('/upload')
def upload_document():
    flow.process_document(
        doc_type="document",
        file_path="/uploads/lease.pdf",
        owner_id="tenant-123",
        context={...},
        trigger_function="upload_document",
        reaction_rules=[...]
    )
    # Document ID, timestamp, and all reactions
    # automatically logged to calendar
```

### Law Notes → Calendar
```python
# When complaint filed
@app.route('/file-complaint')
def file_complaint():
    flow.process_document(
        doc_type="complaint",
        file_path="/uploads/complaint.pdf",
        owner_id="tenant-123",
        context={...},
        trigger_function="file_complaint",
        reaction_rules=[
            {"condition": "is_complaint", "reaction": "prepare_evidence"},
            {"condition": "severity_high", "reaction": "notify_landlord"}
        ]
    )
    # Complaint logged with reactions
    # Evidence packet prepared automatically
    # Calendar events created for deadlines
```

### AI Orchestrator → Calendar
```python
# When AI analysis completes
def record_ai_result(job_id, result):
    flow.process_document(
        doc_type="ai_analysis",
        file_path=f"/data/results/{job_id}.json",
        owner_id="system",
        context={"job_id": job_id, "result": result},
        trigger_function="orchestrate_ai",
        reaction_rules=[...]
    )
    # AI results timestamped and logged
    # Automatic suggestions triggered
```

---

## API Endpoints

### Calendar/Ledger API
```
GET    /api/ledger-calendar/ledger          → Get entries
GET    /api/ledger-calendar/calendar        → Get events
POST   /api/ledger-calendar/calendar/event  → Create event
POST   /api/ledger-calendar/action/log      → Log action
GET    /api/ledger-calendar/dashboard       → Summary view
```

### Data Flow API
```
POST   /api/data-flow/register-functions   → Register module functions
GET    /api/data-flow/functions            → List all functions
POST   /api/data-flow/process-document     → Process doc through flow
GET    /api/data-flow/document/<id>/flow   → Get document lineage
GET    /api/data-flow/actor/<id>/flow      → Get actor activity
GET    /api/data-flow/statistics           → Flow statistics
```

---

## Key Features

### ✅ Tamper-Proof
- SHA256 hash on every entry
- Append-only ledger
- Certificate for legal admissibility

### ✅ Traceable
- Complete audit trail
- Document lineage
- Function reference tracking

### ✅ Automated
- Rules-based reactions
- Smart suggestions
- Deadline tracking

### ✅ Queryable
- Filter by type, actor, time range
- Export for court review
- Analytics dashboard

### ✅ Connected
- All modules feed into calendar
- Timestamp synchronization
- Function registry

---

## Testing

```bash
# Run all tests (71 tests)
pytest -q

# Run specific test classes
pytest tests/test_ledger_calendar.py::TestLedger -v
pytest tests/test_ledger_calendar.py::TestCalendar -v

# Run data flow tests
pytest tests/test_ledger_calendar.py::TestIntegrationEndpoints -v
```

---

## Next Steps

1. **Connect Office Module** → Log document uploads to calendar
2. **Connect Law Notes Module** → Log complaints/notices to calendar
3. **Connect AI Module** → Log analysis results to calendar
4. **Build UI Dashboard** → Visualize calendar and flows
5. **Add Notifications** → Alert users to calendar events
6. **Export Reports** → Generate legal/audit documents
