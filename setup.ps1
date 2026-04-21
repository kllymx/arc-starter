# ARC - Install automated knowledge capture (Windows PowerShell)
#
# What this does:
#   1. Installs uv (fast Python package manager) if not present
#   2. Installs project dependencies
#
# Run once after cloning, from the project root:
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
#
# If your execution policy blocks unsigned scripts, the line above temporarily
# bypasses it for this one invocation without changing system policy.

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Step 1: Install uv if not present
$uvExists = $null
try {
    $uvExists = Get-Command uv -ErrorAction SilentlyContinue
} catch {}

if (-not $uvExists) {
    Write-Host "Installing uv..."
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    } catch {
        Write-Host "ERROR: uv install failed. Install manually: https://docs.astral.sh/uv/" -ForegroundColor Red
        exit 1
    }

    # Make uv available in this session
    $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:Path"

    $uvExists = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uvExists) {
        Write-Host "ERROR: uv installed but not on PATH. Open a new PowerShell window and rerun setup.ps1." -ForegroundColor Red
        exit 1
    }
    Write-Host "uv installed successfully."
}

# Step 2: Install project dependencies
Write-Host "Installing dependencies..."
& uv sync --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: uv sync failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Automated knowledge capture is ready." -ForegroundColor Green
Write-Host ""
Write-Host "Next, verify Git Bash is on your PATH (required for Claude Code + arc-starter hooks):" -ForegroundColor Yellow
Write-Host "  bash --version"
Write-Host ""
Write-Host "If Git Bash is missing, install Git for Windows (includes Git Bash):"
Write-Host "  winget install Git.Git"
Write-Host ""
