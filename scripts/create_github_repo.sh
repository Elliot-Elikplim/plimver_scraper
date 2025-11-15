#!/usr/bin/env bash
# create_github_repo.sh — create and push to GitHub using gh (GitHub CLI) if available
# Usage: ./scripts/create_github_repo.sh <repo-name> [public|private]
set -euo pipefail
NAME=${1:-$(basename "$(pwd)")}
VIS=${2:-public}
REMOTE_NAME=${3:-origin}

# init git if needed
if [ ! -d .git ]; then
  git init
  echo "Initialized git repo"
fi

# ensure main exists
if ! git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
  git checkout -b main
fi

# add commit
git add -A || true
if ! git commit -m "Initial commit" >/dev/null 2>&1; then
  echo "No new changes to commit"
fi

if command -v gh >/dev/null 2>&1; then
  if [ "$VIS" = "private" ]; then
    gh repo create "$NAME" --private --source=. --remote="$REMOTE_NAME" --push --description "Plimver scraper — Scrapy & Zyte examples"
  else
    gh repo create "$NAME" --public --source=. --remote="$REMOTE_NAME" --push --description "Plimver scraper — Scrapy & Zyte examples"
  fi
else
  echo "gh not found — you can add a remote and push manually:"
  echo "git remote add $REMOTE_NAME https://github.com/<owner>/$NAME.git"
  echo "git push -u $REMOTE_NAME main"
fi
