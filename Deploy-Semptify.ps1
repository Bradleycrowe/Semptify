# Deploy-Semptify.ps1 — Justice-grade deployment from D:\Semptify\SemptifyGUI

# Set canonical repo path
$repoPath = "D:\Semptify\SemptifyGUI"
$renderURL = "https://dashboard.render.com"
$liveURL = "https://semptify.onrender.com"

# Step 1: Navigate to repo
Set-Location $repoPath

# Step 2: Git push
git add .
git commit -m "v0.1-stable: ready for Render"
git push origin main

# Step 3: Launch Render dashboard
Start-Process $renderURL

# Step 4: Display Render setup instructions
Write-Host "`n✅ Git pushed. Now configure Render:"
Write-Host "🔧 Environment: Python 3.11+"
Write-Host "🔧 Build Command: pip install -r requirements.txt"
Write-Host "🔧 Start Command: python SemptifyCleanupGUI.py"
Write-Host "🔧 Port: 5000"
Write-Host "`n🌐 Suggested live URL: $liveURL"

# Step 5: Open live app (if already deployed)
Start-Sleep -Seconds 5
Start-Process $liveURL
