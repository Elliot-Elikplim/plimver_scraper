# create_github_repo.ps1 — Create and push to GitHub
# Usage (PowerShell): .\scripts\create_github_repo.ps1 -Name "repo-name" -Private:$false
param(
    [string]$Name = $(Split-Path -Leaf (Get-Location)),
    [string]$Visibility = 'public', # 'public' or 'private'
    [string]$RemoteName = 'origin',
    [switch]$CreateReadme = $true
)

# Ensure repo has git initialized
if (-not (Test-Path .git)) {
    git init
    Write-Host "Initialized git repository"
}

# Create default branch 'main' if needed
if (-not (git rev-parse --abbrev-ref HEAD 2>$null)) {
    git checkout -b main
}

# Add a useful first commit
git add -A
if (-not (git commit -m "Initial commit" 2>$null)) {
    Write-Host "No changes to commit (already committed)"
}

# If gh (GitHub CLI) is present, use it to create the repo
if (Get-Command gh -ErrorAction SilentlyContinue) {
    $visibilityOpt = if ($Visibility -eq 'private') { '--private' } else { '' }

    $createArgs = "repo create $Name $visibilityOpt --source=. --remote=$RemoteName --push"
    if ($CreateReadme) { $createArgs += ' --description "Plimver scraper — Scrapy & Zyte examples"' }

    Write-Host "Running: gh $createArgs"
    gh repo create $Name $visibilityOpt --source=. --remote=$RemoteName --push --description "Plimver scraper — Scrapy & Zyte examples"
    Write-Host "Repository created and pushed via GitHub CLI."
} else {
    Write-Host "GitHub CLI 'gh' not found.\nTo create the repository manually, run these commands:"
    Write-Host "git remote add $RemoteName https://github.com/<your-org>/$Name.git"
    Write-Host "git push -u $RemoteName main"
}
