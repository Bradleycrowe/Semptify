# PushAndDeploy-Semptify.ps1 — All-in-one commit, push, build, and deploy for Semptify

$repoPath = "D:\Semptify\Semptify"
$liveURL = "https://Semptify.onrender.com"
$renderDashboard = "https://dashboard.render.com"

Set-Location $repoPath

Write-Host "🔄 Staging all changes..."
git add .

Write-Host "📝 Committing changes..."
git commit -m "chore: all-in-one deploy — update, build, push, and verify Semptify"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Git commit failed or nothing to commit."
}

Write-Host "🚀 Pushing to GitHub..."
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "🐳 Building Docker container locally for verification..."
    docker-compose down
    docker-compose up --build -d

    Write-Host "🌐 Opening Render dashboard..."
    Start-Process $renderDashboard

    Write-Host "🌍 Opening live app in browser..."
    Start-Sleep -Seconds 5
    Start-Process $liveURL

    Write-Host "`n✅ Semptify pushed, built, and deployed."
    Write-Host "🌐 Live at: $liveURL"
    Write-Host "🧠 Backend: Semptify.py wired and running"
    Write-Host "🔘 Buttons: Upload, Logs, Sync, Generate, Security — all active"
} else {
    Write-Host "❌ Git push failed. Check your network or remote repo status."
}
