#!/usr/bin/env bash
set -euo pipefail

if [ -f package.json ]; then
  npm ci || npm install
  if [ -f tsconfig.json ]; then
    npx --yes tsc --noEmit
  else
    find . -path ./node_modules -prune -o -name '*.js' -print | xargs -r -n1 node --check
  fi
elif [ -f requirements.txt ] || ls *.py **/*.py >/dev/null 2>&1; then
  if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
  python -m compileall -q .
elif [ -f go.mod ]; then
  go build ./...
elif [ -f Cargo.toml ]; then
  cargo check
else
  echo "No recognized project manifest (package.json, requirements.txt, *.py, go.mod, Cargo.toml)."
  exit 1
fi
