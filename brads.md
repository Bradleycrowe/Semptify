# 📘 Semptify Integration Brief: Law Notes Modules

## 🧭 Purpose

This system introduces three modular, multilingual, GUI-driven components to help tenants understand and act on **legal responsibility** for property management misconduct. It empowers users to trace liability across:

- 🧑‍💼 Property Managers
- 🧑‍⚖️ Supervising Brokers
- 🏠 Property Owners

Each module includes push-button flows for filing complaints, generating demand letters, and attaching evidence—no legal or technical background required.

---

## 🧱 Modules to Implement

### # PowerShell script to preview p1shell.html in Flask
# Usage: Run this script from the project root (C:\Semptify\Semptify)

$venv = ".venv"
$flaskApp = "Semptify.py"
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $cwd

# Activate virtual environment
if (Test-Path "$venv\Scripts\Activate.ps1") {
    . "$venv\Scripts\Activate.ps1"
    Write-Host "Activated virtual environment."
} else {
    Write-Host "Virtual environment not found. Run 'python -m venv .venv' first."
    exit 1
}

# Ensure Flask is installed
pip install flask

# Add preview route to Semptify.py if missing
$p1Route = "@app.route('/p1shell')`r`n    def p1shell():`r`n        return render_template('p1shell.html')"
$semptifyPath = Join-Path $cwd $flaskApp
$semptifyContent = Get-Content $semptifyPath -Raw
if ($semptifyContent -notmatch "@app.route\('/p1shell'\)") {
    $insertPoint = $semptifyContent.LastIndexOf("if __name__ == '__main__'")
    if ($insertPoint -gt 0) {
        $before = $semptifyContent.Substring(0, $insertPoint)
        $after = $semptifyContent.Substring($insertPoint)
        $newContent = $before + "`r`n$p1Route`r`n" + $after
        Set-Content -Path $semptifyPath -Value $newContent
        Write-Host "Added /p1shell route to $flaskApp."
    } else {
        Write-Host "Could not find insertion point. Please add the route manually."
    }
} else {
    Write-Host "/p1shell route already exists."
}

# Start Flask server
Write-Host "Starting Flask server..."
python $flaskApp
Write-Host "Visit http://localhost:5000/p1shell to preview p1shell.html."
1. Broker Trail
- **Explains broker supervision duties** under MN Statutes §§ 82.73, 82.67, 82.70.
- **Buttons:**
  - Check Broker Supervision
  - File Broker Complaint
  - Generate Demand Letter

### 2. Owner Trail
- **Explains owner liability** under MN Statutes §§ 504B.001, 504B.181.
- **Buttons:**
  - Identify Property Owner
  - File Owner Complaint
  - Generate Demand Letter

### 3. Complaint Generator
- **Central hub** for filing complaints against manager, broker, or owner.
- **Buttons:**
  - Generate Demand Letter
  - File Broker Complaint
  - File Owner Complaint
  - Attach Evidence Packet
  - Multilingual Export (English, Español, Soomaali, Hmoob, Oromo, Vietnamese)

---

## 🧩 Integration Instructions

### 🔹 File Structure
Create three modular files:

