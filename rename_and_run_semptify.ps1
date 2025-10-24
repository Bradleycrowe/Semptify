$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$ts = (Get-Date).ToString('yyyyMMddHHmmss')
$backup = Join-Path $root ("backups\before_rename_$ts")
New-Item -ItemType Directory -Force -Path $backup | Out-Null

Write-Host "Backing up project to $backup ..."
Get-ChildItem -Force -Recurse | ForEach-Object {
    $dest = Join-Path $backup ($_.FullName.Substring($root.Length) -replace '^[\\\/]','' -replace '[\\\/]','_')
    if ($_.PSIsContainer) { New-Item -ItemType Directory -Force -Path $dest | Out-Null } else { Copy-Item -Force $_.FullName $dest -ErrorAction SilentlyContinue }
}

Write-Host "Replacing all 'Semptify' with 'Semptify' in project files ..."
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\\.venv[\\\/]" -and $_.FullName -notmatch "\\backups\\" } |
    ForEach-Object {
        $f = $_.FullName
        try {
            $txt = Get-Content -Raw -ErrorAction Stop $f
            $new = $txt -replace 'Semptify','Semptify'
            if ($new -ne $txt) {
                $new | Set-Content -Encoding utf8 $f
                Write-Host "Replaced in: $f"
            }
        } catch { }
    }

if (Test-Path "Semptify.py") {
    Write-Host "Renaming Semptify.py -> Semptify.py"
    Rename-Item -Force "Semptify.py" "Semptify.py"
}

Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\\.venv[\\\/]" -and $_.FullName -notmatch "\\backups\\" } |
    ForEach-Object {
        try {
            $path = $_.FullName
            $c = Get-Content -Raw $path
            $c2 = $c -replace 'from\s+Semptify\s+import\s+app','from Semptify import app'
            if ($c2 -ne $c) { $c2 | Set-Content -Encoding utf8 $path; Write-Host "Fixed import in $path" }
        } catch { }
    }

Get-ChildItem -Recurse -Include __pycache__ -Directory -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue }

Write-Host "Activating venv and running Semptify.py ..."
if (Test-Path ".venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
} elseif (Test-Path ".venv-semp\Scripts\Activate.ps1") {
    .\.venv-semp\Scripts\Activate.ps1
} else {
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
}

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

Write-Host "Starting Semptify app ..."
python .\Semptify.py

