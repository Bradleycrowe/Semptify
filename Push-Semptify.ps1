# Push-Semptify.ps1 — Push all modules and prep for Render deployment

# Set canonical repo path
$repoPath = "D:\Semptify\SemptifyGUI"
$renderURL = "https://dashboard.render.com"
$liveURL = "https://semptifygui.onrender.com"

# Step 1: Navigate to repo
Set-Location $repoPath

# Step 2: Git push all changes
git add .
git commit -m "v0.1.1: All modules wired — full justice-grade GUI"
git push origin main

# Step 3: Launch Render dashboard for manual deploy
Start-Process $renderURL

# Step 4: Display Render setup instructions
Write-Host "`n✅ Git pushed. Now deploy manually on Render:"
Write-Host "🔧 Clear Build Cache"
Write-Host "🔧 Environment: Python 3.11+"
Write-Host "🔧 Build Command: pip install -r requirements.txt"
Write-Host "🔧 Start Command: python SemptifyCleanupGUI.py"
Write-Host "🔧 Port: 5000"
Write-Host "`n🌐 Live URL: $liveURL"

# Step 5: Open live app (if already deployed)
Start-Sleep -Seconds 5
Start-Process $liveURL
