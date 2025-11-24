# Dakota County Eviction Defense Module – Validation System

**Purpose:** Automated bi-weekly validation to ensure module content remains current, accurate, and legally sound.

**Schedule:** Twice weekly (Tuesday/Friday at 9:00 AM)

---

## 🔍 What Gets Validated

### 1. External Link Checks
- MN Judicial Branch Housing Forms: https://www.mncourts.gov/getforms/housing-landlord-tenant
- LawHelp MN Eviction Resources: https://www.lawhelpmn.org/
- MN Statutes Chapter 504B: https://www.revisor.mn.gov/statutes/cite/504B
- MN Statute § 484.014 (Expungement): https://www.revisor.mn.gov/statutes/cite/484.014

**Checks:**
- URL accessibility (HTTP 200 status)
- Response time (<10 seconds)
- Basic content validation

### 2. File Freshness
- `process_flow.md` — Eviction timeline
- `motions_actions.md` — Motion templates
- `proactive_tactics.md` — Defense checklists
- `statutes_forms.md` — Statutory reference

**Threshold:** Warns if files >90 days old (suggests review for accuracy)

### 3. Statute Amendment Detection
- § 504B.321 (Service requirements)
- § 504B.285 (Retaliation defense)
- § 504B.161 (Habitability covenant)

**Method:** Web scraping MN Legislature site for "Last Amended" dates or recent year references

### 4. Template Integrity
- Verifies motion templates contain required placeholders:
  - `{{CASE_NO}}`
  - `{{TENANT_NAME}}`
  - `{{HEARING_DATE}}`
  - `{{SERVICE_DATE}}`

---

## 🚀 Installation

### Step 1: Run Installer (Requires Admin)

```powershell
# From PowerShell as Administrator
Set-Location 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module'
.\install_validation_schedule.ps1
```

**Output:**
```
✓ Task registered: \Semptify\DakotaCountyEvictionValidation
Task Details:
  Name: DakotaCountyEvictionValidation
  Path: \Semptify\
  State: Ready
  Schedule:
    • Tuesday at 09:00:00
    • Friday at 09:00:00

✓ Validation will run bi-weekly (Tuesday/Friday at 9:00 AM)
```

### Step 2: Verify Installation

```powershell
Get-ScheduledTask -TaskName "DakotaCountyEvictionValidation" -TaskPath "\Semptify\"
```

---

## 🧪 Manual Testing

### Run Validation Now

```powershell
# Option 1: Direct script execution
Set-Location 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module'
.\validate_module.ps1

# Option 2: Trigger scheduled task
Start-ScheduledTask -TaskName "DakotaCountyEvictionValidation" -TaskPath "\Semptify\"
```

### View Results

```powershell
# JSON log (programmatic access)
Get-Content 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module\validation_log.json' | ConvertFrom-Json

# Pretty-print
$log = Get-Content 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module\validation_log.json' | ConvertFrom-Json
Write-Host "Status: $($log.status)" -ForegroundColor $(if ($log.status -eq 'healthy') {'Green'} else {'Yellow'})
Write-Host "Timestamp: $($log.timestamp)"
Write-Host "Errors: $($log.errors.Count)"
Write-Host "Warnings: $($log.warnings.Count)"
```

---

## 📊 Validation Statuses

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `healthy` | All checks passed | None |
| `warning` | Non-critical issues (stale files, non-200 status) | Review warnings, consider updates |
| `failed` | Critical errors (broken links, missing files) | Immediate review required |

---

## 📧 Email Notifications (Optional)

Enable email alerts on validation failures:

```powershell
.\validate_module.ps1 -SendEmail -EmailTo "admin@example.com"
```

**Requirements:**
- Configure SMTP settings in script (line ~200)
- Uncomment `Send-MailMessage` call
- Provide valid SMTP server and credentials

**Email Content:**
- Validation status (HEALTHY/WARNING/FAILED)
- Summary (total checks, passed, failed)
- Errors and warnings list
- Recommendations for action

---

## 🔧 Customization

### Change Schedule

Edit `schedule_validation.xml`:

```xml
<!-- Example: Monday/Thursday at 2:00 PM -->
<CalendarTrigger>
  <StartBoundary>2025-11-24T14:00:00</StartBoundary>
  <ScheduleByWeek>
    <DaysOfWeek>
      <Monday />
      <Thursday />
    </DaysOfWeek>
  </ScheduleByWeek>
</CalendarTrigger>
```

Re-run `install_validation_schedule.ps1` to apply changes.

### Adjust Freshness Threshold

Edit `validate_module.ps1`:

```powershell
# Change from 90 to 60 days
$result = Test-FileFreshness -FilePath $filePath -MaxDaysOld 60
```

### Add Additional URLs

Edit `validate_module.ps1`, add to `$linkChecks` array:

```powershell
@{
    url = "https://www.example.com/resource"
    description = "Additional Resource"
}
```

---

## 📂 Output Files

| File | Purpose |
|------|---------|
| `validation_log.json` | Latest validation results (JSON) |
| Task Scheduler History | Windows Event Viewer → Task Scheduler |

### Sample `validation_log.json`

```json
{
  "timestamp": "2025-11-21 09:00:15",
  "status": "healthy",
  "checks": [
    {
      "passed": true,
      "url": "https://www.mncourts.gov/getforms/housing-landlord-tenant",
      "description": "MN Judicial Branch Housing Forms",
      "status": 200
    },
    {
      "passed": true,
      "file": "process_flow.md",
      "age_days": 5
    }
  ],
  "warnings": [],
  "errors": [],
  "recommendations": []
}
```

---

## 🚨 Troubleshooting

### Task Not Running

**Check Task State:**
```powershell
Get-ScheduledTask -TaskName "DakotaCountyEvictionValidation" | Select-Object State, LastRunTime, NextRunTime
```

**View Task History:**
1. Open Task Scheduler (`taskschd.msc`)
2. Navigate to `\Semptify\DakotaCountyEvictionValidation`
3. Click "History" tab
4. Look for execution errors

**Common Issues:**
- **Network unavailable:** Task requires internet (set `RunOnlyIfNetworkAvailable=true`)
- **Execution policy:** Script blocked (run: `Set-ExecutionPolicy RemoteSigned`)
- **Permissions:** Task runs as current user (ensure file access)

### Validation Log Not Created

**Verify script executes:**
```powershell
# Run manually with verbose output
.\validate_module.ps1 -Verbose
```

**Check write permissions:**
```powershell
Test-Path 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module\validation_log.json' -PathType Leaf
```

### External Links Fail

**Possible causes:**
- Internet connectivity issue
- Website temporary downtime
- Firewall blocking requests
- URL changed (update in script)

**Verify manually:**
```powershell
Invoke-WebRequest -Uri "https://www.mncourts.gov/getforms/housing-landlord-tenant" -Method Head
```

---

## 📅 Maintenance Schedule

### Weekly
- Review validation logs (automated via task)
- Investigate any warnings or errors

### Monthly
- Check for MN statute amendments manually
- Review file freshness warnings
- Update content if needed

### Quarterly
- Full module audit (legal accuracy)
- Test all motion templates with real cases
- Update multilingual strings if needed

### Annually
- Major version update
- Comprehensive legal review
- Check for legislative changes (session laws)

---

## 🔗 Integration with Semptify

### Option 1: Dashboard Widget

Display latest validation status in admin dashboard:

```python
# In dashboard_api_routes.py
@dashboard_api_bp.route("/eviction_module_health")
def eviction_module_health():
    log_path = "DakotaCounty_EvictionDefense_Module/validation_log.json"
    if os.path.exists(log_path):
        with open(log_path) as f:
            data = json.load(f)
        return jsonify({
            "status": data["status"],
            "last_check": data["timestamp"],
            "errors": len(data["errors"]),
            "warnings": len(data["warnings"])
        })
    return jsonify({"status": "unknown", "message": "No validation log found"})
```

### Option 2: Alert on Startup

Check validation status on Semptify startup:

```python
# In Semptify.py
def check_module_health():
    log_path = "DakotaCounty_EvictionDefense_Module/validation_log.json"
    if os.path.exists(log_path):
        with open(log_path) as f:
            data = json.load(f)
        if data["status"] != "healthy":
            print(f"[WARN] Dakota Eviction Module: {data['status'].upper()}")
            print(f"[WARN] Errors: {len(data['errors'])}, Warnings: {len(data['warnings'])}")

# Call on startup
check_module_health()
```

---

## 📖 References

- Minnesota Statutes: https://www.revisor.mn.gov/statutes/
- MN Judicial Branch: https://www.mncourts.gov/
- LawHelp MN: https://www.lawhelpmn.org/
- Task Scheduler Documentation: https://learn.microsoft.com/en-us/windows/win32/taskschd/

---

**Last Updated:** 2025-11-21  
**Module Version:** 1.0.0
