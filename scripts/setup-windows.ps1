# ReclaimKit — Windows setup helper
# Run this in PowerShell (PS C:\Users\...>). Do NOT run the Linux commands yourself.
#
# Usage:
#   irm https://raw.githubusercontent.com/tgollogly/ReclaimKit/main/scripts/setup-windows.ps1 | iex
# Or save this file and run:  .\setup-windows.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " ReclaimKit — Windows setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Clean up bad PowerShell clone if present
$badClone = Join-Path $env:USERPROFILE "~\stop-assholes"
if (Test-Path $badClone) {
    Write-Host "[..] Removing wrong PowerShell clone at $badClone" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $badClone -ErrorAction SilentlyContinue
}

Write-Host "[1/3] Checking WSL..." -ForegroundColor Green
if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: WSL not installed." -ForegroundColor Red
    Write-Host "  Open PowerShell as Admin and run:  wsl --install" -ForegroundColor Red
    Write-Host "  Restart PC, then run this script again." -ForegroundColor Red
    exit 1
}

$distro = "Ubuntu"
$distros = wsl -l -q 2>$null
if ($distros -notmatch "Ubuntu") {
    Write-Host "WARNING: Ubuntu not found in WSL. Using default distro." -ForegroundColor Yellow
    Write-Host "  Install Ubuntu:  wsl --install -d Ubuntu" -ForegroundColor Yellow
    $distro = $null
}

Write-Host "[2/3] Checking Docker Desktop..." -ForegroundColor Green
Write-Host "  Make sure Docker Desktop is open and says 'Running'." -ForegroundColor Gray
Start-Sleep -Seconds 2

$bashCmd = @'
sudo apt update && sudo apt install -y git && rm -rf ~/stop-assholes && git clone https://github.com/tgollogly/stop-assholes.git ~/stop-assholes && cd ~/stop-assholes && chmod +x scripts/wsl-setup-and-test.sh && ./scripts/wsl-setup-and-test.sh
'@

Write-Host "[3/3] Running setup inside Linux (this takes a few minutes)..." -ForegroundColor Green
Write-Host ""

if ($distro) {
    wsl -d $distro bash -c $bashCmd
} else {
    wsl bash -c $bashCmd
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "SETUP FAILED. Common fixes:" -ForegroundColor Red
    Write-Host "  1. Start Docker Desktop and wait until it says Running" -ForegroundColor Red
    Write-Host "  2. Install Ubuntu:  wsl --install -d Ubuntu  (then restart)" -ForegroundColor Red
    Write-Host "  3. Open Ubuntu from Start menu and run the bash commands in README" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " NEXT STEPS" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  1. Open Ubuntu (Start menu) and run:  nano ~/stop-assholes/config.yaml"
Write-Host "  2. Add screenshots to:  ~/stop-assholes/evidence/screenshots/"
Write-Host "  3. Email Meta using the letter in ~/stop-assholes/output/campaign-package-.../"
Write-Host ""
Write-Host "Full guide: https://github.com/tgollogly/ReclaimKit/blob/main/README.md"
Write-Host ""
