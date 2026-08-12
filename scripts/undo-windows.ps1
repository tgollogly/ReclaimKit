# ReclaimKit — undo local install (Windows PowerShell)
# Removes cloned repo + packages installed for this project, then verifies.
#
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File C:\Users\User\reclaimkit\scripts\undo-windows.ps1
#
# Or after repo is deleted, download this file once and run with -RepoPath:
#   powershell -ExecutionPolicy Bypass -File undo-windows.ps1 -RepoPath C:\Users\User\reclaimkit

param(
    [string]$RepoPath = "$env:USERPROFILE\reclaimkit"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "ReclaimKit UNDO — remove folder and project packages" -ForegroundColor Cyan
Write-Host "Repo path: $RepoPath"
Write-Host ""

# Packages newly installed by: pip install -r requirements.txt
# (Skips pyyaml/Pillow/requests/etc. if you use them for other projects)
$PackagesToRemove = @(
    "duckduckgo-search",
    "pytest",
    "pluggy",
    "iniconfig",
    "primp"
)

function Test-Command($Name) {
    $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

# --- Step 1: Remove repo folder ---
Write-Host "[1/3] Removing repo folder..." -ForegroundColor Yellow
if (Test-Path $RepoPath) {
    Set-Location $env:USERPROFILE
    Remove-Item -LiteralPath $RepoPath -Recurse -Force
    Write-Host "      Deleted: $RepoPath" -ForegroundColor Green
} else {
    Write-Host "      Not found (already gone): $RepoPath" -ForegroundColor DarkGray
}

# --- Step 2: Uninstall pip packages ---
Write-Host "[2/3] Uninstalling ReclaimKit pip packages..." -ForegroundColor Yellow
$pip = $null
if (Test-Command "pip") { $pip = "pip" }
elseif (Test-Command "py") { $pip = "py -m pip" }

if (-not $pip) {
    Write-Host "      WARN: pip not found — skip package uninstall" -ForegroundColor DarkYellow
} else {
    foreach ($pkg in $PackagesToRemove) {
        Invoke-Expression "$pip uninstall $pkg -y 2>`$null" | Out-Null
        Write-Host "      Uninstalled (if present): $pkg"
    }
}

# --- Step 3: Verify ---
Write-Host "[3/3] Verification..." -ForegroundColor Yellow
$ok = $true

if (Test-Path $RepoPath) {
    Write-Host "      FAIL: Folder still exists: $RepoPath" -ForegroundColor Red
    $ok = $false
} else {
    Write-Host "      OK: Folder removed" -ForegroundColor Green
}

if ($pip) {
    foreach ($pkg in $PackagesToRemove) {
        $check = Invoke-Expression "$pip show $pkg 2>`$null"
        if ($LASTEXITCODE -eq 0 -and $check) {
            Write-Host "      FAIL: Package still installed: $pkg" -ForegroundColor Red
            $ok = $false
        } else {
            Write-Host "      OK: $pkg not installed" -ForegroundColor Green
        }
    }
}

Write-Host ""
if ($ok) {
    Write-Host "UNDO COMPLETE — ReclaimKit removed from this PC." -ForegroundColor Green
    exit 0
} else {
    Write-Host "UNDO INCOMPLETE — see FAIL lines above." -ForegroundColor Red
    exit 1
}
