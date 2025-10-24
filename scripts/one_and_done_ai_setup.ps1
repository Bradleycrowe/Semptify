# One-and-done AI setup script for Semptify
# Usage: Run in PowerShell on your server or dev machine
# This script will install Ollama (local AI), pull a model, and configure Semptify for local-only AI Copilot

# Step 1: Install Ollama (Windows)
Write-Host "Installing Ollama..."
Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "$env:TEMP\OllamaSetup.exe"
Start-Process "$env:TEMP\OllamaSetup.exe" -Wait

# Step 2: Start Ollama service
Write-Host "Starting Ollama service..."
Start-Process "C:\Program Files\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 5

# Step 3: Pull Llama3 model
Write-Host "Pulling Llama3 model..."
Invoke-Expression "ollama pull llama3"

# Step 4: Configure Semptify for local AI
$envPath = "d:\Semptify\Semptify\security\render.env"
$envContent = Get-Content $envPath
$envContent = $envContent | Where-Object { $_ -notmatch '^AI_PROVIDER=' -and $_ -notmatch '^OLLAMA_HOST=' -and $_ -notmatch '^OLLAMA_MODEL=' }
$envContent += "AI_PROVIDER=ollama"
$envContent += "OLLAMA_HOST=http://localhost:11434"
$envContent += "OLLAMA_MODEL=llama3"
$envContent | Set-Content $envPath

Write-Host "Semptify is now configured for local-only AI Copilot using Ollama and Llama3. Restart the app to apply changes."

