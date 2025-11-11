# Artifacts Folder

This directory contains large binaries, installers, and other build/runtime artifacts that are too big to commit to git but needed for local development or testing.

## Contents

- **ollama.zip** - Ollama distribution archive for local AI model serving
- **OllamaSetup.exe** - Ollama Windows installer
- **\*.vsix** - VS Code extension packages (optional test installs)
- **\*.exe** - Other binary installers or utilities

## Why This Folder Exists

- Keeps large files (>10MB) out of the main repository root for better organization
- All contents are ignored by `.gitignore` (wildcards: `*.zip`, `*.exe`, `*.vsix`)
- Prevents accidental commits of multi-GB files

## Regenerating Artifacts

If you need to re-download or rebuild these files:

### Ollama
```powershell
# Download latest release from https://ollama.com/download
Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "artifacts/OllamaSetup.exe"
```

### VS Code Extensions (VSIX)
```powershell
# Download from VS Code marketplace if needed
# Example: code --install-extension <publisher>.<extension>
```

## Cleanup

To remove all artifacts and free disk space:
```powershell
Remove-Item -Recurse -Force artifacts/*
```

Artifacts are safe to delete—they can be re-downloaded or regenerated as needed.
