# Storage Setup for Eviction Defense
Write-Host "`n=== STORAGE CONFIGURATION NEEDED ===" -ForegroundColor Cyan
Write-Host "For multi-user laptop use (you + roommate), you need cloud storage backup." -ForegroundColor Yellow

Write-Host "`n[OPTION 1] Cloudflare R2 (Recommended - FREE 10GB)" -ForegroundColor Green
Write-Host "1. Go to: https://dash.cloudflare.com/sign-up"
Write-Host "2. Create account (free tier)"
Write-Host "3. Go to R2 Object Storage > Create bucket > Name: semptify-vault"
Write-Host "4. Manage R2 API Tokens > Create API Token > Permissions: Object Read & Write"
Write-Host "5. Copy Access Key ID and Secret Access Key"
Write-Host ""
Write-Host "Then run:" -ForegroundColor Cyan
Write-Host '  [System.Environment]::SetEnvironmentVariable("R2_ACCESS_KEY_ID","YOUR_KEY_ID","User")'
Write-Host '  [System.Environment]::SetEnvironmentVariable("R2_SECRET_ACCESS_KEY","YOUR_SECRET","User")'
Write-Host '  [System.Environment]::SetEnvironmentVariable("R2_BUCKET_NAME","semptify-vault","User")'
Write-Host '  [System.Environment]::SetEnvironmentVariable("R2_ENDPOINT","https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com","User")'

Write-Host "`n[OPTION 2] Google Drive (Backup only, slower)" -ForegroundColor Yellow
Write-Host "Already configured for: 1semptify@gmail.com"
Write-Host "File: security/gdrive_credentials.json $(if(Test-Path security/gdrive_credentials.json){'EXISTS'}else{'MISSING - needs setup'})"

Write-Host "`n[CURRENT] Local Storage (Active)" -ForegroundColor Green
Write-Host "Documents stored in: uploads/vault/"
Write-Host "Status: WORKING - safe for single laptop use"
Write-Host "Limitation: No automatic cloud backup yet"

Write-Host "`n=== FOR YOUR EVICTION CASE ===" -ForegroundColor Red
Write-Host "CRITICAL: Upload these to vault ASAP:"
Write-Host "  • Eviction notice (Summons & Complaint)"
Write-Host "  • Lease agreement"
Write-Host "  • Rent payment receipts"
Write-Host "  • Correspondence with landlord (emails, texts)"
Write-Host "  • Photos of housing conditions (if relevant)"
Write-Host "  • Repair requests (if habitability defense)"
Write-Host ""
Write-Host "Once uploaded, system will:"
Write-Host "  ✓ Generate SHA-256 notary certificates"
Write-Host "  ✓ Create timeline events"
Write-Host "  ✓ Enable motion/answer filing"
