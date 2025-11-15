#!/usr/bin/env bash
# run_tests.sh — simple test runner wrapper
set -euo pipefail
REPO_ROOT="$(pwd)"
# prefer a nested venv
if [ -f "plimver_scraper/.venv/bin/activate" ]; then
  source "plimver_scraper/.venv/bin/activate"
elif [ -f "venv/bin/activate" ]; then
  source "venv/bin/activate"
fi
python -m pytest -q
