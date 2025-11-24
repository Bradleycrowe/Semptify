# Brad's GUI - Quick Reference Card

**Version:** 2.0.0 (Full Integration)  
**Last Updated:** 2025-11-21

---

## 🚀 Quick Start

```powershell
# Start Semptify
python .\Semptify.py

# Open Brad's Dashboard
http://localhost:8080/brad

# Open Workflow Wizard
http://localhost:8080/brad/workflow_wizard
```

---

## 🎯 Core Features at a Glance

| Feature | What It Does | How to Use |
|---------|--------------|------------|
| **Smart Tooltips** | Every element has rollover help + examples | Hover over any field, button, or badge |
| **Auto-Fill** | Suggests Dakota cities, formats case numbers | Start typing, press Tab to accept |
| **Context Flow** | Active client context flows to all modules | Select client once, all actions use that context |
| **Workflow Wizard** | Step-by-step case building guide | Click "Workflow Wizard" in dashboard |
| **AI Assistant** | Context-aware legal + coding help | Ask anything, AI knows your active client |
| **Quick Actions** | One-click access to vault/timeline/filing | Click buttons on client cards |

---

## 📋 Common Tasks

### Add New Client
```
1. Click "➕ Add Client"
2. Fill name (required) + contact (required)
3. Start typing address → Select from Dakota cities
4. Type case number → Auto-formats to 62-CV-YY-####
5. Add notes
6. Submit
```

**Tooltip Help:** Hover over any field for examples

---

### Upload Documents
```
Option 1: Quick Action
  • Click "📁 Vault" on client card
  • Upload file
  • Timeline event auto-created

Option 2: Integration Route
  • POST /brad/integrate/vault/upload
  • File saved to uploads/vault/<client_id>/
  • Certificate generated with client metadata
```

---

### Build Timeline
```
Option 1: Manual Entry
  • Navigate to client detail
  • Add timeline event
  • Auto-associated with client

Option 2: Automatic
  • Upload document → Timeline event created
  • Add client → "Case opened" event
  • Add case number → "Case filed" event
```

---

### Get Motion Suggestions
```
1. Access Dakota County Library
2. System analyzes client timeline
3. Suggests relevant motions:
   • Service defects → Motion to Dismiss
   • Habitability issues → Motion for Rent Escrow
   • Retaliation pattern → Counterclaim
```

**API:** `GET /brad/integrate/dakota/context`

---

### File Complaint
```
1. Click "📝 File" on client card
2. Redirects to complaint filing
3. All client data pre-filled:
   ✓ Name
   ✓ Contact
   ✓ Address
   ✓ Case number
4. Documents available for attachment
```

**URL:** `/complaint_filing?client_id=<id>&prefill=true`

---

## 💡 Tooltip Examples

### Form Field Tooltips
```
"Client Name" field:
┌─────────────────────────────────────┐
│ Enter tenant's full legal name     │
│ as it appears on lease documents.  │
│                                     │
│ Example: John Michael Doe          │
└─────────────────────────────────────┘
```

### Storage Badge Tooltips
```
"R2 Storage" badge:
┌─────────────────────────────────────┐
│ R2 (Cloudflare) - Primary storage  │
│ Fast, reliable cloud storage with   │
│ global CDN.                         │
│                                     │
│ Status meanings:                    │
│ • HEALTHY: All systems operational  │
│ • DEGRADED: Accessible but slow     │
│ • ERROR: Configuration issue        │
└─────────────────────────────────────┘
```

### AI Quick Prompt Tooltips
```
"💡 Suggest Next Action" prompt:
┌─────────────────────────────────────┐
│ Get AI recommendations for what to  │
│ do next based on current client     │
│ status and timeline analysis        │
└─────────────────────────────────────┘
```

---

## 🧠 Smart Auto-Fill

### Address Suggestions
```
User types: "123 Main"
System suggests:
  • 123 Main St, Eagan, MN 55123
  • 123 Main St, Apple Valley, MN 55124
  • 123 Main St, Burnsville, MN 55337

User presses Tab → Full address filled
```

**Cities included:** Eagan, Apple Valley, Burnsville, Lakeville, Rosemount, Farmington, Hastings

---

### Case Number Formatting
```
User types: "251234"
System auto-formats to: "62-CV-25-1234"

User types: "621234"
System auto-formats to: "62-CV-12-34"
```

**Format:** Dakota County = 62-CV-YY-####

---

### Phone Number Formatting
```
User types: "5551234567"
System auto-formats to: "555-123-4567"
```

---

## 🎓 Workflow Wizard Steps

### Step 1: Client Information
**Purpose:** Gather basic facts  
**Checklist:**
- ☐ Full legal name
- ☐ Contact info
- ☐ Property address
- ☐ Case number (if filed)

**Thought Process:** "Before we can help, we need to understand their situation..."

---

### Step 2: Gather Evidence
**Purpose:** Build case file  
**Priority Order:**
1. Eviction notice (📩)
2. Lease agreement (📄)
3. Payment records (💵)
4. Communications (💬)
5. Photos/videos (📸)
6. Inspection reports (🔍)

**Thought Process:** "In court, facts matter more than feelings. Documents are proof..."

---

### Step 3: Build Timeline
**Purpose:** Create narrative  
**Key Events:**
- When problems started
- When you reported problems
- When eviction notice served
- When court hearing scheduled

**Thought Process:** "Courts understand stories. Timeline shows cause and effect..."

---

### Step 4: Analyze Case
**Purpose:** Identify defenses  
**AI Looks For:**
- Service defects (§504B.321)
- Retaliation (§504B.285)
- Habitability (§504B.161)
- Procedural errors

**Thought Process:** "Not all defenses apply. Analyze facts to find strongest arguments..."

---

### Step 5: Take Action
**Purpose:** Execute strategy  
**Action Options:**
- 📝 File motion
- ⚔️ File counterclaim
- 🤝 Negotiate settlement
- 📋 Prepare for hearing

**Thought Process:** "Analysis is worthless without action..."

---

## 🔗 Integration Routes

### Vault Upload
```http
POST /brad/integrate/vault/upload
Content-Type: multipart/form-data

file=<file>
document_type=evidence
description=Optional description
```

**Auto-creates:**
- Timeline event: "Uploaded: filename"
- Notary certificate
- Client-tagged metadata

---

### Timeline Add
```http
POST /brad/integrate/timeline/add
Content-Type: application/json

{
  "title": "Event title",
  "event_type": "general",
  "description": "Details",
  "event_date": "2025-11-21"
}
```

**Auto-associates:** with active client (user_id = client_id)

---

### Dakota Context
```http
GET /brad/integrate/dakota/context
```

**Returns:**
```json
{
  "client": {"id": "...", "name": "..."},
  "suggestions": [
    {
      "motion_type": "escrow",
      "title": "Motion for Rent Escrow",
      "reason": "Habitability issues in timeline",
      "url": "/dakota_eviction_library/motion/escrow"
    }
  ]
}
```

---

### AI with Context
```http
POST /brad/integrate/ai/context
Content-Type: application/json

{
  "message": "What should I do next?"
}
```

**Context Injected:**
- Active client name + case number
- Recent timeline (5 events)
- Document count
- Case-specific guidance

---

## 🎯 Next-Step Hints

### Red Badges on Client Cards
```
"Add Case #" → Missing case number (high priority)
"Upload Evidence" → No documents uploaded
"Create Timeline" → No timeline events
```

### Workflow Hints in Header
```
"💡 Next Step: Upload evidence documents to vault"
"💡 Next Step: Add case number for filing features"
"💡 Next Step: Review Dakota County motion templates"
```

---

## 📊 Context Flow Example

```
User adds John Doe as client
  ↓
Client ID: client_001
Active client: client_001
Timeline event: "Case opened"
  ↓
User clicks "📁 Vault" on John's card
  ↓
Redirects to /brad/client/client_001#vault
Context: John Doe, case 62-CV-25-1234
  ↓
User uploads eviction_notice.pdf
  ↓
Saved to: uploads/vault/client_001/eviction_notice.pdf
Timeline event: "Uploaded: eviction_notice.pdf"
Certificate generated with client metadata
  ↓
User asks AI: "What should I do next?"
  ↓
AI receives:
  - Active client: John Doe
  - Case: 62-CV-25-1234
  - Timeline: "Uploaded eviction notice" (just now)
  - Documents: 1
  ↓
AI suggests: "Review notice for service defects..."
```

---

## 🧪 Quick Testing

### Test Auto-Fill
```
1. Click "Add Client"
2. Name field: Start typing → No suggestions (names are unique)
3. Address field: Type "123 Main" → Dakota cities appear
4. Case number: Type "251234" → Auto-formats to 62-CV-25-1234
5. Contact: Type "5551234567" → Auto-formats to 555-123-4567
```

### Test Tooltips
```
1. Hover over "Add Client" button → Tooltip appears
2. Hover over "Client Name" field → Tooltip with example
3. Hover over storage badges → Status explanations
4. Hover over AI quick prompts → Expected outcomes
```

### Test Context Flow
```
1. Add client → Becomes active (green border)
2. Click "📁 Vault" → Opens client-specific vault
3. Upload file → Timeline event created
4. Ask AI question → Response mentions client by name
5. Click "Dakota Library" → Motion suggestions based on timeline
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **Tooltips not showing** | Hover longer (0.3s delay) |
| **Auto-fill not working** | Type at least 2 characters |
| **Client not active** | Click client card to activate |
| **Upload failed** | Check client is selected first |
| **AI not responding** | Verify OPENAI_API_KEY set |
| **Motion suggestions empty** | Add timeline events first |

---

## �� Quick Links

- **Dashboard:** `/brad`
- **Workflow Wizard:** `/brad/workflow_wizard`
- **Settings:** `/brad/settings`
- **Client Detail:** `/brad/client/<id>`
- **Integration Health:** `/brad/integrate/health`

---

## 💾 File Locations

```
c:\Semptify\Semptify\
├── brad_gui_routes.py
├── brad_integration_routes.py
├── templates\brad_gui\
│   ├── dashboard_enhanced.html
│   ├── workflow_wizard.html
│   ├── settings.html
│   └── client_detail.html
├── data\brad_clients\
│   └── clients.json
├── uploads\vault\
│   └── <client_id>\
│       └── [documents]
└── BRAD_GUI_WIRING_COMPLETE.md
```

---

## 🎓 Learning Resources

- **Full Integration Guide:** `BRAD_GUI_WIRING_COMPLETE.md`
- **Installation Guide:** `BRAD_GUI_INSTALLATION.md`
- **Usage Guide:** `BRAD_GUI_README.md`
- **Session Summary:** `SESSION_SUMMARY_2025-11-21.md`

---

**Pro Tip:** Hover over EVERYTHING. Tooltips are everywhere with helpful examples!

---

**Version:** 2.0.0  
**Last Updated:** 2025-11-21  
**Status:** ✅ Production Ready
