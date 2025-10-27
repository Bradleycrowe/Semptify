<#
.SYNOPSIS
  Generates a ready-to-commit bundle for the Semptify Delivery Module:
  - OpenAPI spec (YAML)
  - PowerShell integration script (library + example)
  - TypeScript definitions (.d.ts)
  - README with curl examples and integration notes

USAGE
  1. Save this file as Generate-SemptifyDeliveryBundle.ps1
  2. Run from your repo root:  .\Generate-SemptifyDeliveryBundle.ps1
  3. Files will be written to ./api/specs, ./scripts, ./types, ./docs
  4. Inspect, commit, and wire secrets per README.

NOTES
  - This script writes files relative to the current directory.
  - It will create directories if missing and will overwrite existing files with the same names.
  - After generation you can use the produced Semptify-Delivery.ps1 as a library by dot-sourcing it.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Destination layout
$base = (Get-Location).Path
$apiDir = Join-Path $base "api\specs"
$scriptsDir = Join-Path $base "scripts"
$typesDir = Join-Path $base "types"
$docsDir = Join-Path $base "docs"

New-Item -ItemType Directory -Path $apiDir -Force | Out-Null
New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
New-Item -ItemType Directory -Path $typesDir -Force | Out-Null
New-Item -ItemType Directory -Path $docsDir -Force | Out-Null

# File contents
$openApiYaml = @'
openapi: 3.0.3
info:
  title: Semptify Delivery Module API
  version: 1.0.0
  description: Delivery job creation, attempts, confirmation, file uploads, and webhook events for Semptify.
servers:
  - url: https://api.semptify.example
security:
  - bearerAuth: []
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    DeliveryStatus:
      type: string
      enum: [CREATED, PENDING, PARTIAL_COMPLETED, COMPLETED, FAILED, CANCELLED]
    MethodType:
      type: string
      enum: [USPS, EMAIL, CERTIFIED_PRINT, TEXT, HAND_DELIVERED, SERVICE_IN_PERSON, FEDEX, COURT_SERVER, OTHER]
    MethodStatus:
      type: string
      enum: [PENDING, ATTEMPTED, CONFIRMED, FAILED]
    RecipientContact:
      type: object
      properties:
        email:
          type: string
          format: email
        phone:
          type: string
        address:
          type: string
      additionalProperties: false
    DeliveryMethod:
      type: object
      required: [id, type, status]
      properties:
        id:
          type: string
        type:
          $ref: '#/components/schemas/MethodType'
        recipientName:
          type: string
        recipientContact:
          $ref: '#/components/schemas/RecipientContact'
        scheduledAt:
          type: string
          format: date-time
        serviceProvider:
          type: string
        trackingNumber:
          type: string
        certifiedNumber:
          type: string
        proofFiles:
          type: array
          items:
            type: string
        instructions:
          type: string
        costEstimate:
          type: number
          format: double
        currency:
          type: string
          example: USD
        requiredFields:
          type: array
          items:
            type: string
        status:
          $ref: '#/components/schemas/MethodStatus'
    DeliveryHistory:
      type: object
      required: [id, deliveryMethodId, event, actor, timestamp]
      properties:
        id:
          type: string
        deliveryMethodId:
          type: string
        event:
          type: string
        actor:
          type: string
        timestamp:
          type: string
          format: date-time
        metadata:
          type: object
          additionalProperties: true
    DeliveryJob:
      type: object
      required: [id, caseId, createdBy, createdAt, methods, priorityOrder, status]
      properties:
        id:
          type: string
        caseId:
          type: string
        createdBy:
          type: string
        createdAt:
          type: string
          format: date-time
        methods:
          type: array
          items:
            $ref: '#/components/schemas/DeliveryMethod'
        priorityOrder:
          type: array
          items:
            type: string
        status:
          $ref: '#/components/schemas/DeliveryStatus'
        history:
          type: array
          items:
            $ref: '#/components/schemas/DeliveryHistory'
        notes:
          type: string
    AttemptPayload:
      type: object
      required: [actor, attemptAt]
      properties:
        actor:
          type: string
        attemptAt:
          type: string
          format: date-time
        providerResponse:
          type: string
        trackingNumber:
          type: string
        proofFileIds:
          type: array
          items:
            type: string
    ConfirmPayload:
      type: object
      required: [actor, confirmedAt]
      properties:
        actor:
          type: string
        confirmedAt:
          type: string
          format: date-time
        proofFileIds:
          type: array
          items:
            type: string
    CreateDeliveryRequest:
      type: object
      required: [caseId, createdBy, createdAt, methods, priorityOrder, status]
      properties:
        caseId:
          type: string
        createdBy:
          type: string
        createdAt:
          type: string
          format: date-time
        methods:
          type: array
          items:
            $ref: '#/components/schemas/DeliveryMethod'
        priorityOrder:
          type: array
          items:
            type: string
        status:
          $ref: '#/components/schemas/DeliveryStatus'
        notes:
          type: string
  responses:
    BadRequest:
      description: Invalid input
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: string
              message:
                type: string
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: string
              message:
                type: string
paths:
  /api/deliveries:
    post:
      summary: Create delivery job
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateDeliveryRequest'
      responses:
        '201':
          description: Delivery job created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeliveryJob'
        '400':
          $ref: '#/components/responses/BadRequest'
  /api/deliveries/{deliveryId}:
    get:
      summary: Get delivery job by id
      security:
        - bearerAuth: []
      parameters:
        - name: deliveryId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Delivery job
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeliveryJob'
        '404':
          $ref: '#/components/responses/NotFound'
  /api/deliveries/{deliveryId}/methods/{methodId}/attempt:
    post:
      summary: Record a delivery attempt for a method
      security:
        - bearerAuth: []
      parameters:
        - name: deliveryId
          in: path
          required: true
          schema:
            type: string
        - name: methodId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AttemptPayload'
      responses:
        '200':
          description: Attempt recorded, returns updated DeliveryMethod and history
          content:
            application/json:
              schema:
                type: object
                properties:
                  method:
                    $ref: '#/components/schemas/DeliveryMethod'
                  historyEntry:
                    $ref: '#/components/schemas/DeliveryHistory'
        '400':
          $ref: '#/components/responses/BadRequest'
  /api/deliveries/{deliveryId}/methods/{methodId}/confirm:
    post:
      summary: Confirm a delivery method with proofs
      security:
        - bearerAuth: []
      parameters:
        - name: deliveryId
          in: path
          required: true
          schema:
            type: string
        - name: methodId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConfirmPayload'
      responses:
        '200':
          description: Method confirmed
          content:
            application/json:
              schema:
                type: object
                properties:
                  method:
                    $ref: '#/components/schemas/DeliveryMethod'
                  historyEntry:
                    $ref: '#/components/schemas/DeliveryHistory'
        '400':
          $ref: '#/components/responses/BadRequest'
  /api/cases/{caseId}/deliveries:
    get:
      summary: List deliveries for a case
      security:
        - bearerAuth: []
      parameters:
        - name: caseId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Delivery job summaries
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DeliveryJob'
  /api/files:
    post:
      summary: Upload file and return fileId
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        '201':
          description: File uploaded
          content:
            application/json:
              schema:
                type: object
                properties:
                  fileId:
                    type: string
                  filename:
                    type: string
                  contentType:
                    type: string
        '400':
          $ref: '#/components/responses/BadRequest'
  /webhooks/delivery-events:
    post:
      summary: Webhook endpoint for delivery events consumers may implement
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                eventType:
                  type: string
                  enum: [DELIVERY_CREATED, DELIVERY_ATTEMPTED, DELIVERY_CONFIRMED, DELIVERY_FAILED]
                payload:
                  type: object
                  additionalProperties: true
      responses:
        '200':
          description: Webhook received
'@

$psLibrary = @'
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
'@

$tsDef = @'
// semptify-delivery.d.ts
export type DeliveryStatus = "CREATED" | "PENDING" | "PARTIAL_COMPLETED" | "COMPLETED" | "FAILED" | "CANCELLED";
export type MethodType = "USPS" | "EMAIL" | "CERTIFIED_PRINT" | "TEXT" | "HAND_DELIVERED" | "SERVICE_IN_PERSON" | "FEDEX" | "COURT_SERVER" | "OTHER";
export type MethodStatus = "PENDING" | "ATTEMPTED" | "CONFIRMED" | "FAILED";

export interface DeliveryJob {
  id: string;
  caseId: string;
  createdBy: string;
  createdAt: string; // ISO timestamp
  methods: DeliveryMethod[];
  priorityOrder: string[]; // method ids in order
  status: DeliveryStatus;
  history: DeliveryHistory[];
  notes?: string;
}

export interface DeliveryMethod {
  id: string;
  type: MethodType;
  recipientName?: string;
  recipientContact?: RecipientContact;
  scheduledAt?: string; // ISO timestamp
  serviceProvider?: string;
  trackingNumber?: string;
  certifiedNumber?: string;
  proofFiles?: string[]; // file ids
  instructions?: string;
  costEstimate?: number;
  currency?: string;
  requiredFields?: string[]; // e.g. ["recipientContact.email"]
  status: MethodStatus;
}

export interface RecipientContact {
  email?: string;
  phone?: string;
  address?: string; // single-line or structured address string
}

export interface DeliveryHistory {
  id: string;
  deliveryMethodId: string;
  event: string;
  actor: string; // userId or system
  timestamp: string; // ISO
  metadata?: Record<string, unknown>;
}

export interface AttemptPayload {
  actor: string;
  attemptAt: string; // ISO
  providerResponse?: string;
  trackingNumber?: string;
  proofFileIds?: string[];
}

export interface ConfirmPayload {
  actor: string;
  confirmedAt: string; // ISO
  proofFileIds?: string[];
}
'@

$readmeMd = @'
# Semptify Delivery Module — Quick Start

## Files generated
- ./api/specs/semptify-delivery-openapi.yaml
- ./scripts/Semptify-Delivery.ps1
- ./types/semptify-delivery.d.ts
- ./docs/README_DELIVERY.md

## Configure
1. Edit ./scripts/Semptify-Delivery.ps1 and set ApiBase and ApiKey to your environment, or modify script to read secrets from a secure store.
2. Import the OpenAPI YAML into your gateway, tooling, or generate server stubs.
3. Commit generated files to your repo.

## Example curl commands
Create delivery job:
curl -X POST "https://api.semptify.example/api/deliveries" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "caseId":"CASE_123",
  "createdBy":"user_7",
  "createdAt":"2025-10-27T06:04:00Z",
  "methods":[
    {
      "id":"m1",
      "type":"EMAIL",
      "recipientName":"Tenant Example",
      "recipientContact":{"email":"tenant@example.com"},
      "instructions":"Attach complaint PDF",
      "status":"PENDING",
      "requiredFields":["recipientContact.email"]
    },
    {
      "id":"m2",
      "type":"USPS",
      "recipientName":"Owner Example",
      "recipientContact":{"address":"123 Main St, City, ST, 00000"},
      "instructions":"First class, keep tracking",
      "status":"PENDING",
      "requiredFields":["recipientContact.address"]
    }
  ],
  "priorityOrder":["m1","m2"],
  "status":"CREATED"
}
JSON

Upload proof file:
curl -X POST "https://api.semptify.example/api/files" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@/path/to/complaint.pdf;type=application/pdf"

Add delivery attempt:
curl -X POST "https://api.semptify.example/api/deliveries/DELIVERY_ID/methods/m1/attempt" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "actor":"user_7",
    "attemptAt":"2025-10-27T08:00:00Z",
    "providerResponse":"SMTP 250 OK",
    "trackingNumber":"",
    "proofFileIds":["FILE_ID_123"]
  }'

Confirm delivery:
curl -X POST "https://api.semptify.example/api/deliveries/DELIVERY_ID/methods/m1/confirm" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "actor":"user_7",
    "confirmedAt":"2025-10-27T08:05:00Z",
    "proofFileIds":["FILE_ID_123"]
  }'

## Integration notes
- Server must enforce method.requiredFields before accepting attempts.
- History entries must be append-only for auditability.
- Publish events: DELIVERY_CREATED, DELIVERY_ATTEMPTED, DELIVERY_CONFIRMED, DELIVERY_FAILED.
- File upload API must return stable fileId for attachments.
- Use secure secret storage and rotate tokens regularly.
- Test by importing OpenAPI into Swagger UI or Postman and running contract tests.

'@

# Write files
$openApiPath = Join-Path $apiDir "semptify-delivery-openapi.yaml"
$psPath = Join-Path $scriptsDir "Semptify-Delivery.ps1"
$typesPath = Join-Path $typesDir "semptify-delivery.d.ts"
$readmePath = Join-Path $docsDir "README_DELIVERY.md"

$openApiYaml | Out-File -FilePath $openApiPath -Encoding utf8
$psLibrary | Out-File -FilePath $psPath -Encoding utf8
$tsDef | Out-File -FilePath $typesPath -Encoding utf8
$readmeMd | Out-File -FilePath $readmePath -Encoding utf8

Write-Host "Generated files:" -ForegroundColor Green
Write-Host " - $openApiPath"
Write-Host " - $psPath"
Write-Host " - $typesPath"
Write-Host " - $readmePath"

# Quick validation - ensure files exist and report sizes
$files = @($openApiPath, $psPath, $typesPath, $readmePath)
foreach ($f in $files) {
    if (Test-Path $f) {
        $fi = Get-Item $f
        Write-Host ("  {0} ({1} bytes)" -f $fi.FullName, $fi.Length)
    } else {
        Write-Error "Failed to create $f"
    }
}

Write-Host "Bundle generation complete. Edit scripts/Semptify-Delivery.ps1 to wire secrets before running integration flows." -ForegroundColor Cyan
