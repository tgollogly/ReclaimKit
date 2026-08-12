# ReclaimKit — Windows setup helper
# Run this in PowerShell (PS C:\Users\...>). Do NOT run the Linux commands yourself.
#
# Usage (repo must be public, or git auth configured first):
#   .\setup-windows.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " ReclaimKit — Windows setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Clean up bad PowerShell clone if present
$badClone = Join-Path $env:USERPROFILE "~\reclaimkit"
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
sudo apt update && sudo apt install -y git && if [ -d ~/reclaimkit/.git ]; then cd ~/reclaimkit && git pull && ./scripts/wsl-setup-and-test.sh; else git clone https://github.com/tgollogly/ReclaimKit.git ~/reclaimkit && cd ~/reclaimkit && chmod +x scripts/wsl-setup-and-test.sh scripts/wsl-reset-repo.sh && ./scripts/wsl-setup-and-test.sh; fi
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
    Write-Host "  3. Repo is private — make it public or use a GitHub token for git clone" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " NEXT STEPS" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  1. Edit config (do NOT run nano in PowerShell — use one of these):"
Write-Host "       wsl -d Ubuntu nano ~/reclaimkit/config.yaml"
Write-Host "     Or open Ubuntu from Start menu and run:  nano ~/reclaimkit/config.yaml"
Write-Host "  2. Add screenshots to:  ~/reclaimkit/evidence/screenshots/"
Write-Host "  3. Email Meta using the letter in ~/reclaimkit/output/campaign-package-.../"
Write-Host ""
Write-Host "Fresh reinstall (stops Docker, removes old files):"
Write-Host "  wsl -d Ubuntu bash -c 'cd ~/reclaimkit && ./scripts/wsl-reset-repo.sh && ./scripts/wsl-setup-and-test.sh'"
Write-Host ""
Write-Host "Full guide: https://github.com/tgollogly/ReclaimKit/blob/main/README.md"
Write-Host ""
