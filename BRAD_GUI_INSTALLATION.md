# Brad's GUI - Installation & Testing Guide

**Status:** ✅ **COMPLETE** - Ready for testing

---

## ✅ Completed Components

### 1. Core Files
- ✅ `brad_gui_routes.py` - Flask blueprint with 11 routes
- ✅ `templates/brad_gui/dashboard.html` - Main 3-column interface
- ✅ `templates/brad_gui/settings.html` - Configuration page
- ✅ `templates/brad_gui/client_detail.html` - Individual client view

### 2. Blueprint Registration
- ✅ Registered in `Semptify.py` at line 413
- ✅ Import: `from brad_gui_routes import brad_bp`
- ✅ Registration: `app.register_blueprint(brad_bp)`
- ✅ URL prefix: `/brad`

### 3. Dependencies
- ✅ Flask (installed)
- ✅ storage_manager.py (available, Local storage enabled)
- ⚠️ Google Drive credentials (unavailable - expected)
- ⚠️ R2 storage (not configured - expected)
- ⚠️ copilot_routes (status unknown - will fall back to OpenAI API if needed)

### 4. Documentation
- ✅ `BRAD_GUI_README.md` - Comprehensive usage guide
- ✅ `BRAD_GUI_INSTALLATION.md` - This file

---

## 🚀 Quick Start

### 1. Start Semptify
```powershell
Set-Location 'c:\Semptify\Semptify'
.\.venv\Scripts\Activate.ps1
python .\Semptify.py
```

**Expected output:**
```
[OK] Brad's GUI registered at /brad
```

### 2. Open Brad's Dashboard
```powershell
Start-Process "http://localhost:8080/brad"
```

**Expected result:**
- 3-column layout loads
- Storage panel shows: R2 (DEGRADED), Google Drive (DEGRADED), Local (HEALTHY)
- Empty state: "No Clients Yet" with Add Client button
- AI Assistant panel with welcome message

### 3. Add First Client
1. Click "➕ Add Client" button
2. Fill form:
   - Name: `John Doe` (required)
   - Contact: `555-123-4567` (required)
   - Address: `123 Main St, Eagan, MN` (optional)
   - Case Number: `62-CV-25-1234` (optional)
   - Notes: `Eviction defense case` (optional)
3. Click "Add Client"
4. Client card appears in center panel

### 4. Test Client Switching
1. Add 2-3 clients
2. Click different client cards
3. Verify green border moves to active client

### 5. Test Client Detail View
1. Click a client card (navigates to `/brad/client/<id>`)
2. Verify:
   - Client information panel loads
   - Quick actions buttons present
   - Timeline section (empty if no events)
   - Documents section (empty if no uploads)

---

## 🔧 Configuration (Optional)

### R2 Storage (Primary)
```env
# Add to .env or set as environment variables
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=semptify-storage
```

**Verification:**
```powershell
.\.venv\Scripts\python.exe -c "from storage_manager import _init_r2; print('R2 OK' if _init_r2() else 'R2 Failed')"
```

### Google Drive (Fallback)
1. Place `gdrive_credentials.json` in `security/` directory
2. First OAuth flow will generate token automatically
3. Account: 1semptify@gmail.com

**Verification:**
```powershell
Test-Path 'security\gdrive_credentials.json'
```

### AI Assistant
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
Visit `/brad/settings` to see configuration status.

---

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Dashboard loads at `/brad`
- [ ] Storage status panel shows 3 backends
- [ ] AI provider displays in storage panel
- [ ] Add Client modal opens/closes
- [ ] Client form validation works (name + contact required)
- [ ] Client card appears after creation
- [ ] Active client highlighting works (green border)
- [ ] Client count updates in header

### Client Management
- [ ] Add 3 clients successfully
- [ ] Switch active client by clicking cards
- [ ] Navigate to client detail view
- [ ] Client information displays correctly
- [ ] Quick action buttons are present
- [ ] Back to dashboard button works

### API Endpoints
```powershell
# List clients
Invoke-RestMethod -Uri "http://localhost:8080/brad/api/clients"

# Add client
$body = @{name="Test User"; contact="555-9999"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/brad/api/clients" -Method POST -Body $body -ContentType "application/json"

# Storage health
Invoke-RestMethod -Uri "http://localhost:8080/brad/api/storage/health"

# Blueprint health
Invoke-RestMethod -Uri "http://localhost:8080/brad/health"
```

### Settings Page
- [ ] Navigate to `/brad/settings`
- [ ] Storage configuration section displays
- [ ] AI configuration section displays
- [ ] Storage health section displays
- [ ] Back button returns to dashboard

### AI Assistant (Requires API Key)
- [ ] Send message in chat panel
- [ ] Response appears in chat history
- [ ] User/assistant bubbles styled differently
- [ ] Enter key submits message
- [ ] Long messages scroll properly

### Streaming Mode
- [ ] Add `?streaming=1` to URL
- [ ] Red "LIVE" indicator appears bottom-right
- [ ] Pulse animation works

---

## 🐛 Troubleshooting

### Problem: Dashboard shows blank page
**Causes:**
- Blueprint not registered
- Template not found
- JavaScript error

**Fix:**
```powershell
# Check blueprint registration
Select-String -Path 'Semptify.py' -Pattern 'brad_gui_routes'

# Check templates exist
Get-ChildItem 'templates\brad_gui\'

# Check browser console for JS errors
# (F12 in browser)
```

### Problem: "No module named 'brad_gui_routes'"
**Cause:** Python can't find the module

**Fix:**
```powershell
# Verify file exists
Test-Path 'c:\Semptify\Semptify\brad_gui_routes.py'

# Check working directory when starting Semptify
Set-Location 'c:\Semptify\Semptify'
python .\Semptify.py
```

### Problem: Storage always shows "UNKNOWN"
**Cause:** `storage_manager.py` import failed

**Fix:**
```powershell
# Test import
.\.venv\Scripts\python.exe -c "from storage_manager import get_storage_health; print(get_storage_health())"
```

### Problem: AI Assistant not responding
**Causes:**
1. No API key configured
2. copilot_routes not available
3. Network error

**Fix:**
```powershell
# Check AI configuration
.\.venv\Scripts\python.exe -c "import os; print('OpenAI Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"

# Check copilot availability
.\.venv\Scripts\python.exe -c "try: from copilot_routes import generate_response; print('Copilot OK') except: print('Copilot unavailable')"
```

### Problem: Clients not persisting
**Cause:** Write permissions on data directory

**Fix:**
```powershell
# Create directory with permissions
New-Item -ItemType Directory -Path 'data\brad_clients' -Force
icacls 'data\brad_clients' /grant Everyone:F

# Test write access
Set-Content -Path 'data\brad_clients\test.txt' -Value 'test'
Remove-Item 'data\brad_clients\test.txt'
```

### Problem: Client detail view 404
**Cause:** Template not found or route error

**Fix:**
```powershell
# Verify template exists
Test-Path 'templates\brad_gui\client_detail.html'

# Check route registration
.\.venv\Scripts\python.exe -c "from brad_gui_routes import brad_bp; print([r.rule for r in brad_bp.deferred_functions])"
```

---

## 📊 Verification Commands

### Complete System Check
```powershell
# All-in-one verification
.\.venv\Scripts\python.exe -c "
from brad_gui_routes import brad_bp
from pathlib import Path

print('Blueprint:', brad_bp.name)
print('URL Prefix:', brad_bp.url_prefix)
print('Templates:', len(list(Path('templates/brad_gui').glob('*.html'))))
print('Data Dir:', Path('data/brad_clients').exists())

from storage_manager import get_storage_health
health = get_storage_health()
print('Storage - R2:', health['r2'])
print('Storage - GDrive:', health['google_drive'])
print('Storage - Local:', health['local'])

print('\n✅ Brad GUI is operational')
"
```

### Blueprint Routes List
```powershell
# Show all registered routes
.\.venv\Scripts\python.exe -c "
from brad_gui_routes import brad_bp

routes = []
for rule in brad_bp.deferred_functions:
    if hasattr(rule, '__name__'):
        routes.append(rule.__name__)

print('Routes:', ', '.join(routes))
"
```

---

## 📁 File Structure

```
c:\Semptify\Semptify\
├── brad_gui_routes.py                  # Main blueprint (250+ lines)
├── templates/
│   └── brad_gui/
│       ├── dashboard.html              # Main interface (500+ lines)
│       ├── settings.html               # Config page (150 lines)
│       └── client_detail.html          # Client view (300+ lines)
├── data/
│   └── brad_clients/
│       └── clients.json                # Client database (created on first use)
├── BRAD_GUI_README.md                  # Usage documentation
└── BRAD_GUI_INSTALLATION.md            # This file
```

---

## 🎯 Next Steps

### Immediate
1. **Test basic flow:** Start Semptify → Add client → Switch clients → View detail
2. **Verify API:** Use Invoke-RestMethod commands above
3. **Check logs:** Look for "[OK] Brad's GUI registered at /brad" on startup

### Short-term
1. **Configure storage:** Add R2 credentials for full storage health
2. **Configure AI:** Add OPENAI_API_KEY for assistant functionality
3. **Add test clients:** Create 3-5 realistic client profiles

### Long-term
1. **Integration testing:** Connect to vault, timeline, complaint filing
2. **Client edit feature:** Add update form in client detail view
3. **Client archive:** Add status dropdown and archive workflow
4. **Export reports:** Add PDF export for client case summary

---

## ✅ Success Criteria

**Brad's GUI is working correctly when:**
- ✅ Dashboard loads with 3-column layout
- ✅ Can add new clients via modal form
- ✅ Client cards display with correct information
- ✅ Active client highlighting works (green border)
- ✅ Client detail view loads with information panels
- ✅ Storage status panel shows backend health
- ✅ Settings page displays configuration
- ✅ API endpoints return valid JSON
- ✅ No errors in server logs or browser console

**Known limitations (expected):**
- ⚠️ R2/Google Drive show "DEGRADED" without credentials (correct behavior)
- ⚠️ AI assistant won't respond without API key (correct behavior)
- ⚠️ Timeline/documents empty for new clients (correct until data added)
- ⚠️ Client edit requires manual JSON editing (future enhancement)

---

## 📞 Support

**Logs:** Check `logs/events.log` for runtime errors  
**Blueprint Status:** Look for "[OK] Brad's GUI registered" on Semptify startup  
**Template Errors:** Check browser console (F12) for client-side errors  
**API Testing:** Use PowerShell `Invoke-RestMethod` commands above  

**Last Updated:** 2025-11-21  
**Version:** 1.0.0
