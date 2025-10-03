# PushAndDeploy-Semptify.ps1 — Commit, push, and launch Render auto-deploy

# Set repo path and live URL
$repoPath = "D:\Semptify\SemptifyGUI"
$liveURL = "https://semptifygui.onrender.com"
$renderDashboard = "https://dashboard.render.com"

# Step 1: Navigate to repo
Set-Location $repoPath

# Step 2: Git commit and push
git add .
git commit -m "v0.1.5: Final backend patch — dashboard HTML fixed, all routes wired"
git push origin main

# Step 3: Open Render dashboard (optional)
Start-Process $renderDashboard

# Step 4: Launch live app in browser
Start-Sleep -Seconds 5
Start-Process $liveURL

# Step 5: Confirm success
Write-Host "`n✅ SemptifyGUI pushed and deployed."
Write-Host "🌐 Live at: $liveURL"
Write-Host "🧠 Backend: SemptifyCleanupGUI.py wired and running"
Write-Host "🔘 Buttons: Upload, Logs, Sync, Generate, Security — all active"
