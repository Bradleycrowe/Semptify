# PowerShell script to preview p1shell.html in Flask
$venv = ".venv"
$flaskApp = "Semptify.py"
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $cwd

# Activate virtual environment
if (Test-Path "$venv\Scripts\Activate.ps1") {
    . "$venv\Scripts\Activate.ps1"
}

# Ensure Flask is installed
pip install flask

# Add preview route to Semptify.py if missing
$p1Route = "@app.route('/p1shell')`n    def p1shell():`n        return render_template('p1shell.html')"
$semptifyPath = Join-Path $cwd $flaskApp
$semptifyContent = Get-Content $semptifyPath -Raw
if ($semptifyContent -notmatch "@app.route\('/p1shell'\)") {
    $insertPoint = $semptifyContent.LastIndexOf("if __name__ == '__main__'")
    if ($insertPoint -gt 0) {
        $before = $semptifyContent.Substring(0, $insertPoint)
        $after = $semptifyContent.Substring($insertPoint)
        $newContent = $before + "`n$p1Route`n" + $after
        Set-Content -Path $semptifyPath -Value $newContent
        Write-Host "Added /p1shell route to $flaskApp."
    } else {
        Write-Host "Could not find insertion point. Please add the route manually."
    }
} else {
    Write-Host "/p1shell route already exists."
}

# Start Flask server
python $flaskApp
Write-Host "Visit http://localhost:5000/p1shell to preview p1shell.html."
