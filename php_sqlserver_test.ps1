# PowerShell script to test PHP and SQL Server installation, update, and functionality

# 1. Check PHP installation
if (Get-Command php -ErrorAction SilentlyContinue) {
    Write-Host "PHP is installed. Version:"
    php -v
} else {
    Write-Host "PHP is NOT installed."
}

# 2. Check SQL Server installation
if (Get-Command sqlcmd -ErrorAction SilentlyContinue) {
    Write-Host "SQL Server command-line tools are installed. Version:"
    sqlcmd -? | Select-String -Pattern "Version"
} else {
    Write-Host "SQL Server command-line tools are NOT installed."
}

# 3. Test PHP connection to SQL Server
$phpTestFile = "$PSScriptRoot\php_sqlserver_test.php"
$phpTestContent = @'
<?php
$serverName = "localhost";
$connectionOptions = array(
    "Database" => "master",
    "Uid" => "sa",
    "PWD" => "yourStrong(!)Password"
);
$conn = sqlsrv_connect($serverName, $connectionOptions);
if ($conn === false) {
    echo "SQL Server connection failed: ";
    print_r(sqlsrv_errors());
    exit(1);
}
echo "PHP and SQL Server are working together!";
sqlsrv_close($conn);
?>
'@
Set-Content -Path $phpTestFile -Value $phpTestContent

if (Get-Command php -ErrorAction SilentlyContinue) {
    Write-Host "Testing PHP and SQL Server integration..."
    php $phpTestFile
} else {
    Write-Host "PHP not found. Skipping PHP/SQL Server test."
}

Remove-Item $phpTestFile -ErrorAction SilentlyContinue

Write-Host "PHP and SQL Server installation, update, and functionality test complete."
