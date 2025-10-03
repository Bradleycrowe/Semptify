# Set your actual repo path
$repoPath = "D:\Semptify\SemptifyGUI"

# Navigate to repo
Set-Location $repoPath

# === Embed cleanup route and logic into SemptifyGUI.py ===
$cleanupCode = @"
@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    if request.method == 'POST':
        result = run_cleanup()
        return render_template('cleanup_result.html', result=result)
    return render_template('cleanup.html')

def run_cleanup():
    logs = []
    try:
        os.remove('temp/transcript_WR-JD.txt')
        logs.append("Transcript deleted.")
    except FileNotFoundError:
        logs.append("Transcript not found.")
    except Exception as e:
        logs.append(f"Error deleting transcript: {str(e)}")

    try:
        with open('cases/WR-JD/status.txt', 'w') as f:
            f.write('reset')
        logs.append("Case WR-JD reset.")
    except Exception as e:
        logs.append(f"Error resetting case: {str(e)}")

    return logs
"@
Add-Content "$repoPath\SemptifyGUI.py" $cleanupCode

# === Create templates folder if missing ===
$templatePath = "$repoPath\templates"
if (-not (Test-Path $templatePath)) {
    New-Item -ItemType Directory -Path $templatePath
}

# === Create cleanup.html ===
$cleanupHtml = @"
<h2>🧹 Run Cleanup</h2>
<form method="post">
    <button type="submit">Run Cleanup</button>
</form>
"@
Set-Content "$templatePath\cleanup.html" $cleanupHtml

# === Create cleanup_result.html ===
$resultHtml = @"
<h2>✅ Cleanup Results</h2>
<ul>
  {% for item in result %}
    <li>{{ item }}</li>
  {% endfor %}
</ul>
<a href="/cleanup">Run Again</a>
"@
Set-Content "$templatePath\cleanup_result.html" $resultHtml

# === Add sidebar link if sidebar.html exists ===
$sidebarPath = "$templatePath\sidebar.html"
$link = '<a href="/cleanup">🧹 Run Cleanup</a>'
if (Test-Path $sidebarPath) {
    Add-Content $sidebarPath $link
} else {
    Write-Host "Sidebar file not found. Skipping navigation update."
}

# === Fix Git lock if needed ===
$lockFile = "$repoPath\.git\index.lock"
if (Test-Path $lockFile) {
    Remove-Item $lockFile
    Write-Host "Removed stale Git lock file."
}

# === Git commit and push ===
git add .
git commit -m "Embed cleanup module into SemptifyGUI"
git push origin main

Write-Host "`n✅ Cleanup module embedded, committed, and pushed. Render will auto-deploy shortly."
