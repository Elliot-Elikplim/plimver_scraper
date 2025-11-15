# run_tests.ps1 — convenience wrapper to run tests locally
# Usage: .\scripts\run_tests.ps1

$RepoRoot = (Get-Location).Path
# try to activate a venv inside the package directory, fallback to repo venv
$venvPath1 = Join-Path $RepoRoot "plimver_scraper\.venv\Scripts\Activate.ps1"
$venvPath2 = Join-Path $RepoRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvPath1) {
    . $venvPath1
} elseif (Test-Path $venvPath2) {
    . $venvPath2
}

Write-Host "Running pytest..."
python -m pytest -q
