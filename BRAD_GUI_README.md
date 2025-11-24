# Brad's Single-User Multi-Client GUI

**Purpose:** Desktop-optimized interface for managing multiple tenant clients with R2 primary storage, Google Drive fallback, and Claude Sonnet 4.5 AI coding assistant.

**Target:** Single user (Brad) managing multiple client cases on laptop/desktop with optional external display or streaming output.

---

## 🎯 Features

### 1. Multi-Client Management
- **Client Cards:** Visual grid of all clients with quick-switch activation
- **Active Client:** Highlighted card shows currently selected client
- **Add/Edit:** Modal forms for client CRUD operations
- **Client Data:** Name, contact, address, case number, status, notes

### 2. Storage Architecture
- **R2 Storage (Primary):** Cloudflare R2 as main document store
- **Google Drive (Fallback):** 1semptify@gmail.com for redundancy
- **Local Storage:** Always-on failsafe
- **Health Monitoring:** Real-time status badges (Healthy/Degraded/Error)

### 3. AI Coding Assistant
- **Model:** Claude Sonnet 4.5 (via configured AI_PROVIDER)
- **Chat Interface:** Real-time coding assistance panel
- **Context Aware:** Knows Semptify architecture
- **Use Cases:**
  - Write Python Flask routes
  - Debug existing code
  - Create database queries
  - Design UI components

### 4. Desktop-Optimized Layout
- **Resolution:** 1920x1080+ recommended
- **3-Column Grid:**
  - Left: Storage status (350px)
  - Center: Client cards (flexible)
  - Right: AI assistant (400px)
- **Streaming Mode:** URL param `?streaming=1` shows LIVE indicator

---

## 🚀 Access

### URL
```
http://localhost:8080/brad
```

### Quick Launch
```powershell
# Start Semptify
.\Semptify_Launcher.ps1

# Open Brad's dashboard
Start-Process "http://localhost:8080/brad"
```

### Streaming Mode (OBS/Recording)
```
http://localhost:8080/brad?streaming=1
```
Adds red "LIVE" indicator in bottom-right corner.

---

## 📊 Dashboard Layout

```
┌────────────────────────────────────────────────────────────────┐
│  👨‍💻 Brad's Dashboard                      ⚙️ Settings ➕ Add Client  │
└────────────────────────────────────────────────────────────────┘

┌──────────────┬─────────────────────────────┬──────────────────┐
│              │                             │                  │
│  Storage     │  👥 Clients (3)             │  �� AI Assistant │
│  Status      │                             │                  │
│              │  ┌─────────┐ ┌─────────┐   │  Chat history... │
│  R2          │  │ Client1 │ │ Client2 │   │                  │
│  ✓ HEALTHY   │  │ Active  │ │         │   │                  │
│              │  └─────────┘ └─────────┘   │                  │
│  G Drive     │                             │                  │
│  ✓ HEALTHY   │  ┌─────────┐               │                  │
│              │  │ Client3 │               │                  │
│  Local       │  │         │               │  ┌─────────────┐ │
│  ✓ HEALTHY   │  └─────────┘               │  │ Ask me...   │ │
│              │                             │  └─────────────┘ │
└──────────────┴─────────────────────────────┴──────────────────┘
```

---

## 🔧 Setup Requirements

### 1. Storage Configuration

**R2 (Primary):**
```env
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=semptify-storage
```

**Google Drive (Fallback):**
1. Place `gdrive_credentials.json` in `security/`
2. OAuth token will be generated on first use
3. Account: 1semptify@gmail.com

**Verification:**
```powershell
# Test storage
.\.venv\Scripts\python.exe -c "from storage_manager import upload_file; print('Storage OK')"
```

### 2. AI Assistant Configuration

**OpenAI (Default):**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Azure OpenAI:**
```env
AI_PROVIDER=azure
AZURE_OPENAI_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
```

**Ollama (Local):**
```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

**Verification:**
Visit `/brad/settings` to check configuration status.

---

## 💼 Client Management Workflow

### Add New Client
1. Click "➕ Add Client" button
2. Fill in modal form:
   - Name (required)
   - Contact (required)
   - Address (optional)
   - Case Number (optional)
   - Notes (optional)
3. Click "Add Client"
4. Client appears in grid

### Switch Active Client
- Click any client card
- Card highlights with green border
- All subsequent actions (vault, timeline, etc.) use this client's context

### Edit Client
- (Future enhancement: right-click or edit button)
- For now: use API or database directly

### Archive Client
- (Future enhancement: status dropdown)
- Change `status` field to "archived" in `data/brad_clients/clients.json`

---

## �� AI Assistant Usage

### Coding Tasks
```
You: "Create a Flask route to export client data as JSON"

AI: [Provides complete code with comments]
```

### Debugging
```
You: "Why is my storage_manager import failing?"

AI: [Analyzes common issues and suggests fixes]
```

### UI Design
```
You: "Add a progress bar to the client card"

AI: [Provides HTML + CSS code]
```

### Context Commands
- "Show me the storage_manager code"
- "How do I add a new blueprint?"
- "Debug this error: [paste traceback]"

---

## 📁 Data Storage

### Client Data
```
data/brad_clients/
├── clients.json         # Client list + active client ID
└── (future: per-client subdirs)
```

### Client JSON Structure
```json
{
  "clients": [
    {
      "id": "client_001",
      "name": "John Doe",
      "contact": "555-123-4567",
      "address": "123 Main St, Eagan, MN",
      "case_number": "62-CV-25-1234",
      "status": "active",
      "notes": "Eviction defense case",
      "created_at": "2025-11-21T10:30:00",
      "updated_at": "2025-11-21T14:22:00"
    }
  ],
  "active_client_id": "client_001"
}
```

---

## �� Customization

### Change Color Scheme
Edit `dashboard.html`:
```css
body {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    /* Change to your preferred gradient */
}
```

### Adjust Layout Proportions
```css
.dashboard-grid {
    grid-template-columns: 350px 1fr 400px;
    /* Change column widths: left center right */
}
```

### Add Custom Client Fields
1. Update `add_client()` in `brad_gui_routes.py`
2. Add form fields in modal (dashboard.html)
3. Update client card display

---

## 🔗 Integration with Existing Modules

### Vault System
```python
# In vault routes, use active client context
from brad_gui_routes import _get_clients

data = _get_clients()
active_client = data["active_client_id"]

# Upload to client-specific path
upload_file(active_client, filename, data)
```

### Timeline
```python
# Tag timeline events with client ID
timeline_event = {
    "client_id": active_client,
    "event_type": "hearing",
    "date": "2025-12-01",
    ...
}
```

### Complaint Filing
```python
# Pre-fill forms with active client data
client = next(c for c in clients if c["id"] == active_client)
form_data = {
    "tenant_name": client["name"],
    "address": client["address"],
    ...
}
```

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/brad/` | GET | Main dashboard |
| `/brad/api/clients` | GET | List all clients |
| `/brad/api/clients` | POST | Add new client |
| `/brad/api/clients/<id>` | PUT | Update client |
| `/brad/api/clients/<id>/activate` | POST | Set active client |
| `/brad/api/storage/health` | GET | Check storage status |
| `/brad/api/ai/chat` | POST | Send message to AI |
| `/brad/settings` | GET | Settings page |
| `/brad/health` | GET | Blueprint health check |

### API Examples

**List Clients:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/brad/api/clients"
```

**Add Client:**
```powershell
$body = @{
    name = "Jane Smith"
    contact = "jane@example.com"
    address = "456 Oak Ave"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/brad/api/clients" -Method POST -Body $body -ContentType "application/json"
```

**Storage Health:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8080/brad/api/storage/health"
```

---

## 🚨 Troubleshooting

### Storage Status Shows "UNKNOWN"
**Cause:** `storage_manager.py` not loaded  
**Fix:** Verify imports in `brad_gui_routes.py`

### AI Assistant Not Responding
**Causes:**
1. `AI_PROVIDER` not set in `.env`
2. API key missing
3. Copilot routes not available

**Fix:**
1. Set environment variables
2. Check `/brad/settings` for config status
3. Test AI provider manually

### Clients Not Persisting
**Cause:** Write permissions on `data/brad_clients/`  
**Fix:**
```powershell
New-Item -ItemType Directory -Path "data/brad_clients" -Force
icacls "data\brad_clients" /grant Everyone:F
```

### Blueprint Not Registered
**Check:**
```powershell
.\.venv\Scripts\python.exe -c "from brad_gui_routes import brad_bp; print('Loaded:', brad_bp.name)"
```

**Fix:** Verify registration in `Semptify.py` (see installation section)

---

## 🎥 Streaming / Recording Tips

### OBS Studio Setup
1. Add Browser Source
2. URL: `http://localhost:8080/brad?streaming=1`
3. Resolution: 1920x1080
4. Custom CSS (optional): Hide scrollbars, adjust font sizes

### Display Capture
- External monitor recommended (1920x1080+)
- Zoom browser to 100% or 110%
- Enable "Hide mouse cursor" in OBS if needed

### LIVE Indicator
- Appears automatically with `?streaming=1` param
- Red badge bottom-right corner
- Pulsing animation

---

## 📈 Future Enhancements

- [ ] Per-client vault folders (auto-segregated uploads)
- [ ] Client search/filter in dashboard
- [ ] Bulk import clients from CSV
- [ ] Client timeline view (all events for one client)
- [ ] Export client report as PDF
- [ ] Voice input for AI assistant (speech-to-text)
- [ ] Dark/light theme toggle
- [ ] Mobile-responsive layout (currently desktop-only)
- [ ] Real-time collaboration (if multi-user mode added)

---

## 📞 Support

**Documentation:** This file + inline code comments  
**Issues:** Check logs in `logs/events.log`  
**Updates:** Re-run registration script if blueprint changes

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-21  
**Author:** Semptify Development Team
