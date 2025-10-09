<#!
.SYNOPSIS
  Windows PowerShell wrapper to bootstrap SemptifyGUI inside Ubuntu WSL.

.EXAMPLE
  ./scripts/wsl_setup.ps1

.EXAMPLE
  ./scripts/wsl_setup.ps1 -WithDocker -ForceVenv -Dir /mnt/d/Semptify/SemptifyGUI

.NOTES
  Pass-through flags map to the bash script: --with-docker, --force-venv, --dir=...
#>
param(
  [switch]$WithDocker,
  [switch]$ForceVenv,
  [string]$Dir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Require-Command($Name){
  if(-not (Get-Command $Name -ErrorAction SilentlyContinue)){
    Write-Error "Required command '$Name' not found. Install WSL components first."
  }
}

Require-Command wsl

# Detect a preferred Ubuntu distro (first matching name containing 'Ubuntu')
$distro = (wsl -l -q | Where-Object { $_ -match 'Ubuntu' } | Select-Object -First 1)
if(-not $distro){
  Write-Error "No Ubuntu WSL distribution found. Install via: wsl --install -d Ubuntu"; exit 1
}

Write-Host "[INFO] Using WSL distro: $distro" -ForegroundColor Cyan

$argsList = @()
if($WithDocker){ $argsList += '--with-docker' }
if($ForceVenv){ $argsList += '--force-venv' }
if($Dir){ $argsList += "--dir=$Dir" }

Write-Host "[INFO] Invoking bootstrap script inside WSL..." -ForegroundColor Cyan
wsl -d $distro -- bash -lc "cd $(wslpath -u (Get-Location)) && bash scripts/wsl_setup.sh $([string]::Join(' ', $argsList))"

Write-Host "[DONE] WSL setup complete." -ForegroundColor Green