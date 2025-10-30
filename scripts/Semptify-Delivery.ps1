<#
.SYNOPSIS
  Semptify Delivery PowerShell library and CLI helper.
USAGE
  Dot-source the file to use functions in your session:
    . .\Semptify-Delivery.ps1
  Or run directly for the example block to execute a sample create job flow.
NOTES
  Edit $ApiBase and $ApiKey in the configuration section, or update to read from a secure store.
#>

# --- Configuration (update securely in your CI or local environment) ---
$Script:ApiBase = "https://api.semptify.example"    # replace with real host
$Script:ApiKey = "REPLACE_WITH_REAL_API_KEY"        # replace; prefer secure retrieval
$Script:TimeoutSeconds = 30

function Invoke-SemptifyApi {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][ValidateSet('GET','POST','PUT','DELETE','PATCH')][string]$Method,
        [Parameter(Mandatory=$true)][string]$Path,
        [object]$Body = $null,
        [hashtable]$Headers = @{}
    )
    $uri = "$($Script:ApiBase)$Path"
    $defaultHeaders = @{
        "Authorization" = "Bearer $($Script:ApiKey)"
        "Accept" = "application/json"
    }
    $allHeaders = $defaultHeaders + $Headers
    $json = $null
    if ($Body -ne $null) { $json = $Body | ConvertTo-Json -Depth 10 }

    try {
        Write-Host "HTTP $Method $uri"
        if ($json) { Write-Host "Payload: $json" -ForegroundColor DarkGray }
        $resp = Invoke-RestMethod -Method $Method -Uri $uri -Headers $allHeaders -Body $json -ContentType "application/json" -TimeoutSec $Script:TimeoutSeconds
        return $resp
    } catch {
        $err = $_.Exception
        Write-Error "API call failed: $($err.Message)"
        if ($err.Response -and $err.Response.GetResponseStream()) {
            try {
                $reader = New-Object System.IO.StreamReader($err.Response.GetResponseStream())
                $body = $reader.ReadToEnd()
                Write-Error "Response body: $body"
            } catch {}
        }
        throw
    }
}

function New-DeliveryJob {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$CaseId,
        [Parameter(Mandatory=$true)][string]$CreatedBy,
        [Parameter(Mandatory=$true)][array]$Methods,
        [string[]]$PriorityOrder = @()
    )
    $body = @{
        caseId = $CaseId
        createdBy = $CreatedBy
        createdAt = (Get-Date).ToString("o")
        methods = $Methods
        priorityOrder = $PriorityOrder
        status = "CREATED"
    }
    $resp = Invoke-SemptifyApi -Method "POST" -Path "/api/deliveries" -Body $body
    Write-Host "Delivery job created with id $($resp.id)" -ForegroundColor Green
    return $resp
}

function Get-DeliveryJob {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][string]$DeliveryId)
    $resp = Invoke-SemptifyApi -Method "GET" -Path "/api/deliveries/$DeliveryId"
    return $resp
}

function Add-DeliveryAttempt {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$DeliveryId,
        [Parameter(Mandatory=$true)][string]$MethodId,
        [Parameter(Mandatory=$true)][string]$Actor,
        [string]$ProviderResponse = "",
        [string]$TrackingNumber = "",
        [string[]]$ProofFileIds = @(),
        [datetime]$AttemptAt = (Get-Date)
    )
    $body = @{
        actor = $Actor
        attemptAt = $AttemptAt.ToString("o")
        providerResponse = $ProviderResponse
        trackingNumber = $TrackingNumber
        proofFileIds = $ProofFileIds
    }
    $resp = Invoke-SemptifyApi -Method "POST" -Path "/api/deliveries/$DeliveryId/methods/$MethodId/attempt" -Body $body
    Write-Host "Attempt recorded for method $MethodId on delivery $DeliveryId" -ForegroundColor Yellow
    return $resp
}

function Confirm-DeliveryMethod {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$DeliveryId,
        [Parameter(Mandatory=$true)][string]$MethodId,
        [Parameter(Mandatory=$true)][string]$Actor,
        [string[]]$ProofFileIds = @(),
        [datetime]$ConfirmedAt = (Get-Date)
    )
    $body = @{
        actor = $Actor
        confirmedAt = $ConfirmedAt.ToString("o")
        proofFileIds = $ProofFileIds
    }
    $resp = Invoke-SemptifyApi -Method "POST" -Path "/api/deliveries/$DeliveryId/methods/$MethodId/confirm" -Body $body
    Write-Host "Method $MethodId confirmed for delivery $DeliveryId" -ForegroundColor Green
    return $resp
}

function Upload-ProofFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$FilePath,
        [string]$ContentType = "application/pdf"
    )
    if (-not (Test-Path $FilePath)) {
        throw "File not found $FilePath"
    }
    $uri = "$($Script:ApiBase)/api/files"
    $headers = @{
        "Authorization" = "Bearer $($Script:ApiKey)"
    }
    try {
        Write-Host "Uploading proof file $FilePath"
        $resp = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -InFile $FilePath -ContentType $ContentType -TimeoutSec $Script:TimeoutSeconds
        $json = $resp.Content | ConvertFrom-Json
        Write-Host "Uploaded file id $($json.fileId)" -ForegroundColor Cyan
        return $json
    } catch {
        throw "File upload failed: $($_.Exception.Message)"
    }
}

function List-DeliveriesForCase {
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)][string]$CaseId)
    $resp = Invoke-SemptifyApi -Method "GET" -Path "/api/cases/$CaseId/deliveries"
    return $resp
}

# Example CLI block when run directly
if ($MyInvocation.InvocationName -eq $MyInvocation.MyCommand.Name) {
    Write-Host "Running example flow from Semptify-Delivery.ps1 (edit config at top to use real API)..." -ForegroundColor Magenta
    $exampleCase = "CASE_123"
    $exampleUser = "user_7"
    $methods = @(
        @{
            id = "m1"
            type = "EMAIL"
            recipientName = "Tenant Example"
            recipientContact = @{ email = "tenant@example.com" }
            instructions = "Attach complaint PDF"
            status = "PENDING"
            requiredFields = @("recipientContact.email")
        },
        @{
            id = "m2"
            type = "USPS"
            recipientName = "Owner Example"
            recipientContact = @{ address = "123 Main St, City, ST, 00000" }
            instructions = "First class, keep tracking"
            status = "PENDING"
            requiredFields = @("recipientContact.address")
        }
    )
    try {
        $job = New-DeliveryJob -CaseId $exampleCase -CreatedBy $exampleUser -Methods $methods -PriorityOrder @("m1","m2")
        Write-Host "Created job id: $($job.id)" -ForegroundColor Green
    } catch {
        Write-Error $_
    }
}
