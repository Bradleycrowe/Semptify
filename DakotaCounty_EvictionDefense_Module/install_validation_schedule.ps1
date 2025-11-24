# Install Dakota County Eviction Defense Module Validation Schedule
# Registers Task Scheduler job for bi-weekly runs (Tuesday/Friday 9 AM)

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"
$taskName = "DakotaCountyEvictionValidation"
$taskPath = "\Semptify\"
$xmlPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "schedule_validation.xml"

Write-Host "Installing validation schedule for Dakota County Eviction Defense Module..." -ForegroundColor Cyan

# Check if XML exists
if (-not (Test-Path $xmlPath)) {
    Write-Host "ERROR: schedule_validation.xml not found at $xmlPath" -ForegroundColor Red
    exit 1
}

# Remove existing task if present
try {
    $existing = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Confirm:$false
    }
} catch {
    # Task doesn't exist, continue
}

# Register new task
try {
    Register-ScheduledTask -Xml (Get-Content $xmlPath | Out-String) -TaskName $taskName -TaskPath $taskPath -Force | Out-Null
    Write-Host "✓ Task registered: $taskPath$taskName" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to register task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Verify registration
$task = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Write-Host "  Name: $($task.TaskName)" -ForegroundColor Gray
    Write-Host "  Path: $($task.TaskPath)" -ForegroundColor Gray
    Write-Host "  State: $($task.State)" -ForegroundColor Gray
    
    $triggers = $task.Triggers
    Write-Host "  Schedule:" -ForegroundColor Gray
    foreach ($trigger in $triggers) {
        $days = $trigger.DaysOfWeek -join ', '
        Write-Host "    • $days at $($trigger.StartBoundary.TimeOfDay)" -ForegroundColor Gray
    }
    
    Write-Host "`n✓ Validation will run bi-weekly (Tuesday/Friday at 9:00 AM)" -ForegroundColor Green
    Write-Host "`nManual Test:" -ForegroundColor Cyan
    Write-Host "  Start-ScheduledTask -TaskName '$taskName' -TaskPath '$taskPath'" -ForegroundColor Gray
    Write-Host "`nView Results:" -ForegroundColor Cyan
    Write-Host "  Get-Content 'c:\Semptify\Semptify\DakotaCounty_EvictionDefense_Module\validation_log.json'" -ForegroundColor Gray
} else {
    Write-Host "ERROR: Task registration verification failed" -ForegroundColor Red
    exit 1
}
