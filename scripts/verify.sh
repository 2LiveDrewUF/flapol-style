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
ruby <<'RUBY'
require "yaml"

allowed_detection_modes = %w[vale python both contextual].freeze

Dir["coverage/*.yml"].sort.each do |path|
  manifest = YAML.safe_load(
    File.read(path),
    permitted_classes: [],
    aliases: false
  )
  abort "#{path}: coverage manifest must be a nonempty mapping" unless manifest.is_a?(Hash) && !manifest.empty?

  manifest.each do |rule_id, record|
    abort "#{path}:#{rule_id}: coverage record must be a mapping" unless record.is_a?(Hash)

    if record["detected"]
      unless allowed_detection_modes.include?(record["detection_mode"])
        abort "#{path}:#{rule_id}: detected rules need a supported detection_mode"
      end
    elsif record.key?("detection_mode")
      abort "#{path}:#{rule_id}: undetected rules must omit detection_mode"
    end
  end
end
RUBY

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
