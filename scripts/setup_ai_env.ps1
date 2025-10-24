# PowerShell script to set up AI provider environment variables for Semptify
# Usage: Run in your repo root. Edit values as needed.

$envFile = "..\.env"

# Main Copilot AI (Allo)
$mainProvider = Read-Host "Main Copilot AI Provider (openai, azure, ollama)"
Set-Content -Path $envFile -Value "AI_PROVIDER=$mainProvider" -Force

if ($mainProvider -eq "openai") {
    $openaiKey = Read-Host "OpenAI API Key"
    $openaiModel = Read-Host "OpenAI Model (e.g. gpt-4o-mini)"
    Add-Content -Path $envFile -Value "OPENAI_API_KEY=$openaiKey"
    Add-Content -Path $envFile -Value "OPENAI_MODEL=$openaiModel"
}
elseif ($mainProvider -eq "azure") {
    $azureEndpoint = Read-Host "Azure OpenAI Endpoint URL"
    $azureKey = Read-Host "Azure OpenAI API Key"
    $azureDeployment = Read-Host "Azure Deployment Name"
    $azureVersion = Read-Host "Azure API Version (default: 2024-02-15-preview)"
    if (-not $azureVersion) { $azureVersion = "2024-02-15-preview" }
    Add-Content -Path $envFile -Value "AZURE_OPENAI_ENDPOINT=$azureEndpoint"
    Add-Content -Path $envFile -Value "AZURE_OPENAI_API_KEY=$azureKey"
    Add-Content -Path $envFile -Value "AZURE_OPENAI_DEPLOYMENT=$azureDeployment"
    Add-Content -Path $envFile -Value "AZURE_OPENAI_API_VERSION=$azureVersion"
}
elseif ($mainProvider -eq "ollama") {
    $ollamaHost = Read-Host "Ollama Host URL (default: http://localhost:11434)"
    if (-not $ollamaHost) { $ollamaHost = "http://localhost:11434" }
    $ollamaModel = Read-Host "Ollama Model (e.g. llama3.1)"
    Add-Content -Path $envFile -Value "OLLAMA_HOST=$ollamaHost"
    Add-Content -Path $envFile -Value "OLLAMA_MODEL=$ollamaModel"
}

# Vault AI (Groc, local only)
$vaultProvider = Read-Host "Vault AI Provider (ollama recommended for local)"
Set-Content -Path $envFile -Value "VAULT_AI_PROVIDER=$vaultProvider" -Force
if ($vaultProvider -eq "ollama") {
    $vaultOllamaHost = Read-Host "Vault Ollama Host URL (default: http://localhost:11434)"
    if (-not $vaultOllamaHost) { $vaultOllamaHost = "http://localhost:11434" }
    $vaultOllamaModel = Read-Host "Vault Ollama Model (e.g. llama3.1)"
    Add-Content -Path $envFile -Value "VAULT_OLLAMA_HOST=$vaultOllamaHost"
    Add-Content -Path $envFile -Value "VAULT_OLLAMA_MODEL=$vaultOllamaModel"
}

Write-Host "AI environment variables configured in $envFile. Edit as needed for Render deployment."

