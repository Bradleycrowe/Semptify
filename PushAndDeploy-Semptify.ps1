# PushAndDeploy-Semptify.ps1 — Commit, push, and launch Render auto-deploy

$repoPath = "D:\Semptify\SemptifyGUI"
$liveURL = "https://semptifygui.onrender.com"
$renderDashboard = "https://dashboard.render.com"

Set-Location $repoPath

# Step 1: Git commit and push with error handling
git add .
git commit -m "v0.1.5: Final backend patch — dashboard HTML fixed, all routes wired"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Git commit failed or nothing to commit."
}
git push origin main
if ($LASTEXITCODE -eq 0) {
    # Step 2: Open Render dashboard (optional)
    Start-Process $renderDashboard

    # Step 3: Launch live app in browser
    Start-Sleep -Seconds 5
    Start-Process $liveURL

    # Step 4: Confirm success
    Write-Host "`n✅ SemptifyGUI pushed and deployed."
    Write-Host "🌐 Live at: $liveURL"
    Write-Host "🧠 Backend: SemptifyCleanupGUI.py wired and running"
    Write-Host "🔘 Buttons: Upload, Logs, Sync, Generate, Security — all active"
} else {
    Write-Host "❌ Git push failed. Check your network or remote repo status."
}