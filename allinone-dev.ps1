# All-in-one PowerShell script for Semptify development and PHP/MySQL test

# 1. Start Flask development server
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python Semptify.py"

# 2. Wait for server to start
Start-Sleep -Seconds 2

# 3. Open Semptify homepage in browser
Start-Process "http://localhost:5000"

# 4. Open shell.html for live editing
Start-Process "c:\Semptify\Semptify\templates\shell.html"


# 5. Full PHP and MySQL test
$phpTestFile = "$PSScriptRoot\php_mysql_test.php"
$phpTestContent = @'
<?php
$conn = new mysqli("localhost", "root", "", "test");
if ($conn->connect_error) {
    echo "MySQL connection failed: " . $conn->connect_error;
    exit(1);
}
echo "PHP and MySQL are working together!";
$conn->close();
?>
'@
Set-Content -Path $phpTestFile -Value $phpTestContent

if (Get-Command php -ErrorAction SilentlyContinue) {
    Write-Host "Testing PHP and MySQL integration..."
    php $phpTestFile
} else {
    Write-Host "PHP not found. Skipping PHP/MySQL test."
}

Remove-Item $phpTestFile -ErrorAction SilentlyContinue

Write-Host "All-in-one dev workflow started. Flask, browser, shell.html, PHP/MySQL integration test complete."
