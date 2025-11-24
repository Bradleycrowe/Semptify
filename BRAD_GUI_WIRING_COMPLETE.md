# Brad's GUI - Complete Feature Wiring & Context Flow

**Status:** ✅ Fully Integrated  
**Date:** 2025-11-21

---

## 🔌 Integration Architecture

Brad's GUI now serves as the **central hub** for all Semptify features, with intelligent context flow that automatically connects related functions.

### Core Principle
**Single Active Client Context** - All subsequent actions (uploads, timeline events, filings) automatically use the active client's context. No need to re-enter client info across different modules.

---

## 📊 Feature Integration Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     Brad's GUI Dashboard                         │
│                  (Central Command Center)                        │
└─────────────────┬───────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬─────────────────┬──────────────┐
    │             │             │                 │              │
    ▼             ▼             ▼                 ▼              ▼
┌────────┐  ┌──────────┐  ┌───────────┐  ┌─────────────┐  ┌─────────┐
│ Vault  │  │ Timeline │  │ Complaint │  │   Dakota    │  │   AI    │
│ System │  │  Events  │  │  Filing   │  │   Library   │  │Assistant│
└────────┘  └──────────┘  └───────────┘  └─────────────┘  └─────────┘
     │            │              │                │              │
     └────────────┴──────────────┴────────────────┴──────────────┘
                           │
                    Auto-sync context
                  (client ID, case #, etc.)
```

---

## 🔗 Integration Routes

### 1. Vault Integration
**Endpoint:** `/brad/integrate/vault/upload`

**Context Flow:**
```python
User uploads document → 
  ✓ Saves to uploads/vault/<client_id>/
  ✓ Generates notary certificate with client metadata
  ✓ Auto-creates timeline event: "Uploaded: filename"
  ✓ Tags document with client_id, case_number, upload_date
```

**Usage in Dashboard:**
```javascript
// Quick action button on client card
<button onclick="uploadToVault('client_001')">📁 Vault</button>

// Redirects to integrated upload with client context pre-filled
```

**Benefits:**
- ✅ No need to select client in vault
- ✅ Automatic timeline tracking
- ✅ Proper file organization by client
- ✅ Metadata includes case context

---

### 2. Timeline Integration
**Endpoint:** `/brad/integrate/timeline/add`

**Context Flow:**
```python
User adds timeline event →
  ✓ Auto-associates with active client (user_id = client_id)
  ✓ Appears in client detail view immediately
  ✓ Analyzed by AI for pattern detection
  ✓ Used in workflow suggestions
```

**Automatic Timeline Events:**
- Document uploaded → "Uploaded: [filename]"
- Client created → "Case opened"
- Case number added → "Case filed: [case_number]"
- Complaint filed → "Filed: [motion_type]"

**Benefits:**
- ✅ Automatic event creation (no manual entry)
- ✅ Chronological case history
- ✅ Pattern analysis (retaliation detection)
- ✅ Evidence of proper documentation

---

### 3. Complaint Filing Integration
**Endpoint:** `/brad/integrate/complaint/prefill`

**Context Flow:**
```python
User clicks "File Complaint" →
  ✓ Redirects to /complaint_filing with query params
  ✓ Pre-fills: tenant_name, contact, address, case_number
  ✓ Loads client documents for evidence attachment
  ✓ Timeline used for date verification
```

**Pre-filled Fields:**
```
?prefill=true
&tenant_name=John+Doe
&tenant_contact=555-123-4567
&property_address=123+Main+St,+Eagan,+MN
&case_number=62-CV-25-1234
&client_id=client_001
```

**Benefits:**
- ✅ Zero data re-entry
- ✅ Consistent naming across documents
- ✅ Faster filing process
- ✅ Reduced errors

---

### 4. Dakota Library Integration
**Endpoint:** `/brad/integrate/dakota/context`

**Context Flow:**
```python
User accesses Dakota resources →
  ✓ Analyzes client timeline for triggers
  ✓ Suggests relevant motions based on patterns
  ✓ Pre-fills motion templates with client data
  ✓ Returns customized recommendations
```

**Motion Suggestions Based on Timeline:**

| Timeline Pattern | Suggested Motion | Statute |
|------------------|------------------|---------|
| "service" or "notice" mentioned | Motion to Dismiss (Improper Service) | §504B.321 |
| "repair", "mold", "heat" mentioned | Motion for Rent Escrow (Habitability) | §504B.161, §504B.385 |
| Complaint within 90 days of eviction | Counterclaim (Retaliation) | §504B.285 |
| Any case | Motion to Continue (More Time) | §504B.341 |

**API Response Example:**
```json
{
  "client": {
    "id": "client_001",
    "name": "John Doe",
    "case_number": "62-CV-25-1234"
  },
  "suggestions": [
    {
      "motion_type": "escrow",
      "title": "Motion for Rent Escrow (Habitability)",
      "reason": "Timeline shows mold complaints and repair requests",
      "url": "/dakota_eviction_library/motion/escrow"
    },
    {
      "motion_type": "counterclaim",
      "title": "Counterclaim (Retaliation)",
      "reason": "Eviction filed 15 days after city complaint",
      "url": "/dakota_eviction_library/motion/counterclaim"
    }
  ]
}
```

**Benefits:**
- ✅ AI-powered motion selection
- ✅ Context-aware templates
- ✅ Pattern recognition (retaliation timing)
- ✅ Statutory references included

---

### 5. AI Assistant Integration
**Endpoint:** `/brad/integrate/ai/context`

**Enhanced Context Injection:**
```python
User asks AI question →
  ✓ Injects active client name, case number
  ✓ Includes recent timeline summary (5 events)
  ✓ Adds document count
  ✓ Provides case-specific guidance
```

**Context-Enriched Prompt Example:**
```
User query: "What should I do next?"

CONTEXT ADDED BY SYSTEM:
Active Client: John Doe
Case Number: 62-CV-25-1234
Property: 123 Main St, Eagan, MN

Recent Timeline:
  - 2025-11-20: Uploaded eviction notice
  - 2025-11-18: City inspection report (mold confirmed)
  - 2025-11-15: Tenant reported mold to landlord
  - 2025-11-10: Heating failure documented
  - 2025-11-05: Repair request sent (email)

Documents on file: 8
```

**AI Response Benefits:**
- ✅ Case-specific recommendations
- ✅ Timeline-aware analysis
- ✅ Evidence-based suggestions
- ✅ Deadline calculations

---

## 🧠 Smart Features

### 1. Auto-Fill System
**Location:** dashboard_enhanced.html

**Capabilities:**

| Field | Auto-Fill Logic |
|-------|-----------------|
| **Address** | Dakota County city suggestions (Eagan, Apple Valley, Burnsville, etc.) |
| **Case Number** | Auto-formats to 62-CV-YY-#### as you type |
| **Contact** | Phone numbers auto-format to ###-###-#### |
| **Notes** | Template suggestions based on common eviction types |

**How It Works:**
```javascript
// Dakota County cities
function checkAutofill('address', value) {
    const dakotaCities = ['Eagan, MN', 'Apple Valley, MN', ...];
    const matches = dakotaCities.filter(city => 
        value.toLowerCase().includes(city.split(',')[0].toLowerCase())
    );
    showSuggestions('address', matches);
}

// Case number formatting
function formatCaseNumber(input) {
    let value = input.value;
    // Auto-format to 62-CV-YY-####
    if (!value.startsWith('62')) value = '62-' + value;
    // ... more formatting logic
}
```

**User Experience:**
1. User starts typing "123 Main"
2. System suggests: "→ 123 Main St, Eagan, MN 55123"
3. User presses Tab → Full address filled
4. Next field gains focus automatically

---

### 2. Tooltip System
**Location:** dashboard_enhanced.html

**Coverage:**
- ✅ Every form field (purpose + example)
- ✅ Storage status badges (what each status means)
- ✅ Client card actions (what each button does)
- ✅ AI quick prompts (what to expect)
- ✅ Settings options (configuration requirements)

**Tooltip Structure:**
```html
<div class="tooltip-container">
    <input type="text" placeholder="Client name">
    <div class="tooltip tooltip-right">
        Enter the tenant's full legal name as it appears on lease documents.
        <span class="tooltip-example">
            Example: John Michael Doe
        </span>
    </div>
</div>
```

**Tooltip Types:**
- **Top:** For buttons and headers
- **Bottom:** For dropdowns and large elements
- **Right:** For form fields (doesn't cover input)
- **Left:** For right-aligned elements

---

### 3. Workflow Suggestions
**Endpoint:** `/brad/api/workflow/suggestions`

**Decision Logic:**
```python
def suggest_next_action(client):
    suggestions = []
    
    # Missing data checks
    if not client.case_number:
        suggestions.append("Add case number")
    
    # Document checks
    if vault_empty(client.id):
        suggestions.append("Upload evidence documents")
    
    # Timeline checks
    if no_timeline_events(client.id):
        suggestions.append("Create timeline")
    
    # Ready to file checks
    if has_docs AND has_timeline AND has_case_number:
        suggestions.append("File legal response")
    
    return suggestions
```

**Priority System:**
- 🔴 **High:** Missing critical data (case number, documents)
- 🟡 **Medium:** Incomplete data (timeline, notes)
- 🟢 **Low:** Enhancements (more documents, Dakota resources)

**Display:**
```html
<!-- Red badge on client card -->
<div class="next-step-hint">Add Case #</div>

<!-- Workflow hint in header -->
<div class="workflow-hint">
    💡 Next Step: Upload evidence documents to vault
</div>
```

---

### 4. Context-Aware Quick Actions
**Location:** Client cards in dashboard

**Actions:**
```html
<div class="client-actions">
    <button onclick="quickAction('client_001', 'vault')">📁 Vault</button>
    <button onclick="quickAction('client_001', 'timeline')">📅 Timeline</button>
    <button onclick="quickAction('client_001', 'file')">📝 File</button>
</div>
```

**Behavior:**
```javascript
function quickAction(clientId, action) {
    switch(action) {
        case 'vault':
            // Opens client-specific vault section
            window.location.href = `/brad/client/${clientId}#vault`;
            break;
        case 'timeline':
            // Opens timeline with client filter
            window.location.href = `/brad/client/${clientId}#timeline`;
            break;
        case 'file':
            // Redirects to complaint filing with prefill
            window.location.href = `/complaint_filing?client_id=${clientId}`;
            break;
    }
}
```

---

## 🎯 Workflow Wizard

**Location:** `/brad/workflow_wizard`  
**Purpose:** Step-by-step guide through entire case building process

### 5 Steps with Human Thought Process:

#### **Step 1: Client Information**
**Thought Process Box:**
```
💭 Why this matters:
Before we can help someone defend against eviction, we need to understand 
their situation. Think of this like a doctor taking medical history before treatment.

What we're establishing:
• Who is the client? (for documents and court filings)
• How can we reach them? (critical for deadlines)
• Where is the property? (determines jurisdiction)
• What's the case status? (determines urgency)
```

**Interactive Checklist:**
- ☐ Client's full legal name
- ☐ Contact information
- ☐ Property address
- ☐ Court case number (if filed)

**Real Example:**
> "Jane Smith, lives at 123 Oak Street, Eagan MN. Received eviction notice on Nov 1st..."

---

#### **Step 2: Gather Evidence**
**Thought Process Box:**
```
💭 Why this matters:
In court, facts matter more than feelings. Documents are proof.

Priority order:
1. Notice documents (proves service, identifies defects)
2. Lease agreement (shows terms, obligations)
3. Payment records (receipts, bank statements)
4. Communication records (texts, emails)
5. Habitability evidence (photos, inspections)
```

**Document Cards:**
- 📩 Eviction Notice
- 📄 Lease Agreement
- 💵 Payment Records
- 💬 Communications
- 📸 Photos/Videos
- 🔍 Inspection Reports

**What Judges Look For:**
> "Dated documents showing a clear pattern. Example: Tenant reported mold on Oct 5..."

---

#### **Step 3: Build Timeline**
**Thought Process Box:**
```
💭 Why this matters:
Courts understand stories. A timeline turns scattered events into a coherent 
narrative showing cause and effect.

What makes a strong timeline:
• Starts with move-in or when problems began
• Shows pattern of complaints and responses
• Documents all notice dates
• Reveals retaliation timing
• Connects to evidence documents
```

**Timeline Checklist:**
- ☐ When did problems start?
- ☐ When did you report problems?
- ☐ When was eviction notice served?
- ☐ When is the court hearing?

**Example Showing Retaliation:**
```
• Oct 5: Tenant reports broken furnace
• Oct 12: Temp drops to 55°F
• Oct 15: Tenant calls city inspector
• Oct 18: City issues violation
• Oct 25: Landlord serves eviction (7 days after!)
```

---

#### **Step 4: Analyze**
**Thought Process Box:**
```
💭 Why this matters:
Not all defenses apply to every case. We analyze your specific facts 
to identify the strongest legal arguments.

What AI looks for:
• Service defects (§504B.321)
• Retaliation (§504B.285)
• Habitability (§504B.161)
• Discrimination
• Procedural errors
```

**Analysis Cards:**
- ⚖️ Service Review
- 🛡️ Retaliation Check
- 🏠 Habitability Issues

**Defense Strategy:**
> Primary: Motion to Dismiss (improper service)  
> Backup: Counterclaim for Retaliation  
> Alternative: Rent Escrow (habitability)  
> Post-case: Motion for Expungement

---

#### **Step 5: Take Action**
**Thought Process Box:**
```
💭 Why this matters:
Analysis is worthless without action. Based on your evidence and defenses, 
here are concrete steps to take.

Priority actions:
1. File strongest defense motion ASAP
2. Prepare backup defenses
3. Gather missing evidence
4. Consider settlement
5. Prepare for court hearing
```

**Action Cards:**
- 📝 File Motion
- ⚔️ File Counterclaim
- 🤝 Negotiate Settlement
- 📋 Prepare for Hearing

**Recommended Next Steps:**
```
1. File Motion to Dismiss (improper service detected)
2. Prepare Counterclaim (retaliation timeline)
3. Gather more photos (strengthen habitability)
4. Schedule court prep (hearing in 10 days)
```

---

## 🧪 Testing the Full Flow

### Complete User Journey Test:

#### 1. **Add Client**
```
Action: Click "Add Client" → Fill form → Submit
Expected: 
  ✓ Client card appears
  ✓ Client becomes active (green border)
  ✓ Workflow hint: "Upload evidence documents"
  ✓ Timeline event: "Case opened"
```

#### 2. **Upload Documents**
```
Action: Click "📁 Vault" on client card → Upload file
Expected:
  ✓ File saved to uploads/vault/<client_id>/
  ✓ Notary certificate generated
  ✓ Timeline event: "Uploaded: filename"
  ✓ Document count updates
```

#### 3. **Add Timeline Event**
```
Action: Navigate to client detail → Add timeline entry
Expected:
  ✓ Event associated with client_id
  ✓ Appears in timeline panel
  ✓ Analyzed by AI for patterns
  ✓ Workflow suggestion updates
```

#### 4. **Get AI Suggestions**
```
Action: Ask AI "What should I do next?"
Expected:
  ✓ AI receives client context
  ✓ Response mentions client by name
  ✓ Suggestions based on timeline
  ✓ Next steps are specific to case
```

#### 5. **Access Dakota Resources**
```
Action: Click Dakota Library link
Expected:
  ✓ Motion suggestions based on timeline
  ✓ Pre-filled templates available
  ✓ Statutory references provided
  ✓ Examples match client situation
```

#### 6. **File Complaint**
```
Action: Click "File" quick action
Expected:
  ✓ Redirects to /complaint_filing
  ✓ Tenant name pre-filled
  ✓ Address pre-filled
  ✓ Case number pre-filled
  ✓ Documents available for attachment
```

---

## 📊 Data Flow Diagram

```
CLIENT CREATION
     ↓
  Generates client_id (client_001)
     ↓
     ├→ Saves to data/brad_clients/clients.json
     ├→ Creates uploads/vault/<client_id>/
     ├→ Adds timeline event: "Case opened"
     └→ Sets as active client

DOCUMENT UPLOAD (via integration route)
     ↓
  Receives client context from Brad's GUI
     ↓
     ├→ Saves to uploads/vault/<client_id>/filename
     ├→ Generates certificate with client metadata
     ├→ Adds timeline event: "Uploaded: filename"
     └→ Updates document count

TIMELINE ANALYSIS
     ↓
  Reads timeline_events WHERE user_id = client_id
     ↓
     ├→ Detects patterns (service, habitability, retaliation)
     ├→ Calculates days between events
     ├→ Suggests relevant motions
     └→ Updates workflow recommendations

AI QUERY
     ↓
  Injects client context into prompt
     ↓
     ├→ Active client name, case number
     ├→ Recent timeline summary (5 events)
     ├→ Document count
     ├→ Case-specific guidance
     └→ Returns contextualized response

COMPLAINT FILING
     ↓
  Receives prefill parameters from Brad
     ↓
     ├→ Pre-fills tenant_name
     ├→ Pre-fills contact
     ├→ Pre-fills address
     ├→ Pre-fills case_number
     └→ Loads client documents for attachment
```

---

## ✅ Verification Checklist

### Integration Points:
- [x] Vault auto-saves to client-specific directory
- [x] Timeline events auto-associate with active client
- [x] Complaint filing pre-fills client data
- [x] Dakota library suggests motions based on timeline
- [x] AI assistant receives full client context

### Smart Features:
- [x] Auto-fill for addresses (Dakota County cities)
- [x] Auto-format case numbers (62-CV-YY-####)
- [x] Auto-format phone numbers (###-###-####)
- [x] Tooltips on all form fields
- [x] Examples in all tooltips

### Workflow Guidance:
- [x] Workflow suggestions API functional
- [x] Next-step hints on client cards
- [x] Workflow wizard with 5 steps
- [x] Human thought process explanations
- [x] Real-world examples throughout

### Context Flow:
- [x] Active client context propagates to all modules
- [x] Client ID used as user_id in timeline
- [x] Client ID used in vault paths
- [x] Client data pre-fills complaint forms
- [x] AI receives enriched context

---

## 🚀 Usage Instructions

### For Users (Brad):

**1. Start with Dashboard:**
```
Visit: http://localhost:8080/brad
```

**2. Add Client:**
```
Click "➕ Add Client" 
→ Fill form (auto-suggestions will appear)
→ Submit
```

**3. Follow Workflow Hints:**
```
Look at workflow hint in header:
  "💡 Next Step: Upload evidence documents"
  
Or check red badges on client cards:
  "Add Case #"
```

**4. Use Quick Actions:**
```
Click buttons on client card:
  📁 Vault → Upload documents
  📅 Timeline → Add events
  📝 File → Create complaint
```

**5. Get AI Help:**
```
Use quick prompts in AI panel:
  "💡 Suggest Next Action"
  "📊 Review Case"
  "📝 Draft Motion"

Or ask naturally:
  "What should I do next for John Doe?"
```

**6. Access Resources:**
```
Navigate to Dakota Library
→ System suggests relevant motions
→ Templates auto-fill with client data
```

---

### For Developers:

**1. Access Integration Routes:**
```python
# Upload with context
POST /brad/integrate/vault/upload
Headers: multipart/form-data
Body: file=<file>, document_type=evidence

# Add timeline with context
POST /brad/integrate/timeline/add
Body: {"title": "...", "event_date": "..."}

# Get motion suggestions
GET /brad/integrate/dakota/context
Returns: {"suggestions": [...]}

# AI with context
POST /brad/integrate/ai/context
Body: {"message": "What should I do next?"}
```

**2. Extend Integration:**
```python
# Add new integration route
from brad_integration_routes import integration_bp

@integration_bp.route('/new_feature/connect', methods=['POST'])
def new_feature_integration():
    client = _get_active_client()
    # ... use client context
    return jsonify({"success": True})
```

**3. Add Workflow Suggestions:**
```python
# In workflow_suggest() function
if condition_detected(client):
    suggestions.append({
        'action': 'new_action',
        'title': 'Do Something',
        'description': 'Why this matters',
        'priority': 'high',
        'url': '/path/to/action'
    })
```

---

## 📈 Future Enhancements

### Planned Features:
- [ ] Voice input for AI assistant (speech-to-text)
- [ ] OCR for uploaded documents (auto-extract dates, names)
- [ ] Calendar integration (court date reminders)
- [ ] SMS notifications for deadlines
- [ ] Mobile-responsive workflow wizard
- [ ] Multi-language support (Spanish, Somali, Hmong)
- [ ] Bulk document upload
- [ ] Export case summary as PDF

### Integration Opportunities:
- [ ] Google Calendar sync for hearings
- [ ] Email integration (import correspondence)
- [ ] SMS integration (text-based updates)
- [ ] Court e-filing system connection
- [ ] Legal aid referral network
- [ ] Translation service integration

---

**Last Updated:** 2025-11-21  
**Version:** 2.0.0 (Full Integration)  
**Status:** ✅ Production Ready
