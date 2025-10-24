# Add Python scripts directory to PATH for current session
$pythonScripts = "C:\Users\bradc\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
if ($env:Path -notlike "*${pythonScripts}*") {
    $env:Path += ";$pythonScripts"
    Write-Host "Added Python scripts directory to PATH for this session."
} else {
    Write-Host "Python scripts directory is already in PATH."
}

# Example: Set a custom environment variable (uncomment to use)
# $env:MY_VAR = "your_value"
# Write-Host "Set MY_VAR environment variable."

Write-Host "Current PATH: $env:Path"
