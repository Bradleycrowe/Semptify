#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uninstall unused VS Code extensions for Semptify project
.DESCRIPTION
    Removes 100+ unused extensions, keeping only essential ones for Python/Flask development
    Essential extensions kept: Python, Copilot, GitHub, Azure (core), Render, Flask, Git
#>

Write-Host "🧹 VS Code Extension Cleanup for Semptify" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will remove 100+ unused extensions." -ForegroundColor Yellow
Write-Host "Essential extensions will be kept: Python, Copilot, GitHub, Azure, Render, Flask, Git" -ForegroundColor Green
Write-Host ""

$response = Read-Host "Continue? (y/n)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "Cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Starting cleanup..." -ForegroundColor Green
Write-Host ""

$removed = 0
$failed = 0

# Java Extensions (6)
Write-Host "Removing Java extensions..." -ForegroundColor Yellow
$javaExtensions = @(
    "redhat.java",
    "vscjava.vscode-java-debug",
    "vscjava.vscode-java-dependency",
    "vscjava.vscode-java-pack",
    "vscjava.vscode-java-test",
    "vscjava.vscode-maven"
)
foreach ($ext in $javaExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# PHP Extensions (2)
Write-Host "Removing PHP extensions..." -ForegroundColor Yellow
$phpExtensions = @(
    "xdebug.php-debug",
    "xdebug.php-pack"
)
foreach ($ext in $phpExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Deno
Write-Host "Removing Deno..." -ForegroundColor Yellow
Write-Host "  - Uninstalling denoland.vscode-deno..." -NoNewline
$result = code --uninstall-extension denoland.vscode-deno 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅" -ForegroundColor Green
    $removed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}

# Docker Duplicate (keeping ms-azuretools.vscode-docker)
Write-Host "Removing duplicate Docker extension..." -ForegroundColor Yellow
Write-Host "  - Uninstalling ms-vscode-remote.remote-containers..." -NoNewline
$result = code --uninstall-extension ms-vscode-remote.remote-containers 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅" -ForegroundColor Green
    $removed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}

# TLA+ Tools
Write-Host "Removing TLA+ extensions..." -ForegroundColor Yellow
$tlaExtensions = @(
    "alygin.vscode-tlaplus",
    "chat-tools.tlaplus-spec-support"
)
foreach ($ext in $tlaExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Qt Tools
Write-Host "Removing Qt extension..." -ForegroundColor Yellow
Write-Host "  - Uninstalling tonka3000.qtvsctools..." -NoNewline
$result = code --uninstall-extension tonka3000.qtvsctools 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅" -ForegroundColor Green
    $removed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}

# IDL
Write-Host "Removing IDL extension..." -ForegroundColor Yellow
Write-Host "  - Uninstalling idl.idl..." -NoNewline
$result = code --uninstall-extension idl.idl 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅" -ForegroundColor Green
    $removed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}

# Kubernetes
Write-Host "Removing Kubernetes extension..." -ForegroundColor Yellow
Write-Host "  - Uninstalling ms-kubernetes-tools.vscode-kubernetes-tools..." -NoNewline
$result = code --uninstall-extension ms-kubernetes-tools.vscode-kubernetes-tools 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " ✅" -ForegroundColor Green
    $removed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}

# Test Adapters (unused)
Write-Host "Removing unused test adapters..." -ForegroundColor Yellow
$testExtensions = @(
    "hbenl.vscode-test-explorer",
    "ms-vscode.test-adapter-converter",
    "littlefoxteam.vscode-python-test-adapter"
)
foreach ($ext in $testExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Azure Unused (keeping core Azure, Functions, Resources, Account)
Write-Host "Removing unused Azure extensions..." -ForegroundColor Yellow
$azureUnused = @(
    "ms-azuretools.azure-dev",
    "ms-azuretools.vscode-apimanagement",
    "ms-azuretools.vscode-azureappservice",
    "ms-azuretools.vscode-azurecontainerapps",
    "ms-azuretools.vscode-azurefunctions",
    "ms-azuretools.vscode-azureresourcegroups",
    "ms-azuretools.vscode-azurestaticwebapps",
    "ms-azuretools.vscode-azurestorage",
    "ms-azuretools.vscode-azurevirtualmachines",
    "ms-azuretools.vscode-bicep",
    "ms-azuretools.vscode-cosmosdb",
    "ms-vscode.azure-repos",
    "msazurermtools.azurerm-vscode-tools"
)
foreach ($ext in $azureUnused) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Database Tools (unused)
Write-Host "Removing database tools..." -ForegroundColor Yellow
$dbExtensions = @(
    "ms-mssql.mssql",
    "ms-ossdata.vscode-postgresql",
    "mtxr.sqltools",
    "mtxr.sqltools-driver-pg",
    "mtxr.sqltools-driver-sqlite"
)
foreach ($ext in $dbExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Remote Development (unused)
Write-Host "Removing remote development extensions..." -ForegroundColor Yellow
$remoteExtensions = @(
    "ms-vscode-remote.remote-ssh",
    "ms-vscode-remote.remote-ssh-edit",
    "ms-vscode-remote.remote-wsl",
    "ms-vscode-remote.vscode-remote-extensionpack",
    "ms-vscode.remote-explorer",
    "ms-vscode.remote-server"
)
foreach ($ext in $remoteExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Language Support (unused)
Write-Host "Removing unused language support..." -ForegroundColor Yellow
$langExtensions = @(
    "golang.go",
    "ms-dotnettools.csdevkit",
    "ms-dotnettools.csharp",
    "ms-dotnettools.vscode-dotnet-runtime",
    "ms-dotnettools.vscodeintellicode-csharp",
    "rust-lang.rust-analyzer",
    "redhat.vscode-yaml",
    "redhat.vscode-xml",
    "tamasfe.even-better-toml"
)
foreach ($ext in $langExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Debuggers (unused)
Write-Host "Removing unused debuggers..." -ForegroundColor Yellow
$debugExtensions = @(
    "ms-vscode.cpptools",
    "ms-vscode.cpptools-extension-pack",
    "ms-vscode.cpptools-themes",
    "ms-vscode.cmake-tools",
    "twxs.cmake"
)
foreach ($ext in $debugExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Jupyter/Notebook (if not using notebooks)
Write-Host "Removing Jupyter extensions..." -ForegroundColor Yellow
$jupyterExtensions = @(
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-keymap",
    "ms-toolsai.jupyter-renderers",
    "ms-toolsai.vscode-jupyter-cell-tags",
    "ms-toolsai.vscode-jupyter-slideshow"
)
foreach ($ext in $jupyterExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

# Misc Unused
Write-Host "Removing miscellaneous unused extensions..." -ForegroundColor Yellow
$miscExtensions = @(
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-playwright.playwright",
    "visualstudioexptteam.vscodeintellicode",
    "streetsidesoftware.code-spell-checker",
    "editorconfig.editorconfig",
    "eamodio.gitlens",
    "donjayamanne.githistory",
    "mhutchie.git-graph",
    "gruntfuggly.todo-tree",
    "wayou.vscode-todo-highlight",
    "aaron-bond.better-comments",
    "oderwat.indent-rainbow",
    "mechatroner.rainbow-csv",
    "ms-vscode.powershell"
)
foreach ($ext in $miscExtensions) {
    Write-Host "  - Uninstalling $ext..." -NoNewline
    $result = code --uninstall-extension $ext 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $removed++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "  ✅ Removed: $removed extensions" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "  ❌ Failed:  $failed extensions" -ForegroundColor Red
}
Write-Host ""
Write-Host "Essential extensions still installed:" -ForegroundColor Cyan
Write-Host "  - Python (ms-python.python)" -ForegroundColor Green
Write-Host "  - Pylance (ms-python.vscode-pylance)" -ForegroundColor Green
Write-Host "  - GitHub Copilot (github.copilot)" -ForegroundColor Green
Write-Host "  - GitHub Copilot Chat (github.copilot-chat)" -ForegroundColor Green
Write-Host "  - Azure Account (ms-vscode.azure-account)" -ForegroundColor Green
Write-Host "  - Render (render.render)" -ForegroundColor Green
Write-Host "  - Git Extension Pack (donjayamanne.git-extension-pack)" -ForegroundColor Green
Write-Host ""
Write-Host "Restart VS Code to complete the cleanup." -ForegroundColor Yellow
