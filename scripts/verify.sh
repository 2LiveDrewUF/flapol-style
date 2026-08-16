#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "${script_dir}/.." && pwd)"
cd "${project_root}"

echo "Running Python regression tests"
python3 -m unittest discover -s tests -p 'test_*.py'

echo "Checking Python syntax"
python3 -m compileall -q python

echo "Checking JSON registries"
jq empty python/flapol_style/data/*.json

echo "Checking coverage YAML"
ruby -e 'require "yaml"; Dir["coverage/*.yml"].sort.each { |path| YAML.safe_load(File.read(path), permitted_classes: [], aliases: false) }'

echo "Checking patch whitespace"
git diff --check

if [[ -n "${VALE_BIN:-}" ]]; then
  echo "Running Vale fixtures with VALE_BIN=${VALE_BIN}"
  VALE_BIN="${VALE_BIN}" ruby tools/test_rules.rb
elif command -v vale >/dev/null 2>&1; then
  echo "Running Vale fixtures with $(command -v vale)"
  VALE_BIN="$(command -v vale)" ruby tools/test_rules.rb
else
  echo "Vale is not installed locally; GitHub Actions must run the pinned Vale fixtures before release."
fi

echo "Local verification complete"
