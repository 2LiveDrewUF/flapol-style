#!/usr/bin/env ruby

require "open3"
require "yaml"

ROOT = File.expand_path("..", __dir__)
VALE = ENV.fetch("VALE_BIN", "vale")

def normalized(text)
  text.gsub("\r\n", "\n").strip
end

failures = []
fixtures = Dir[File.join(ROOT, "fixtures", "*", "expected.txt")].sort

abort "No fixtures found." if fixtures.empty?

fixtures.each do |expected_path|
  directory = File.dirname(expected_path)
  name = File.basename(directory)
  expected = normalized(File.read(expected_path))

  stdout, stderr, status = Open3.capture3(
    VALE,
    "--output=line",
    "--sort",
    "--normalize",
    "--relative",
    "--no-global",
    "--no-exit",
    ".",
    chdir: directory
  )

  unless status.success?
    failures << "#{name}: Vale failed\n#{stderr}"
    next
  end

  actual = normalized(stdout)
  next if actual == expected

  failures << <<~REPORT
    #{name}: output differed
    EXPECTED:
    #{expected}

    ACTUAL:
    #{actual}
  REPORT
end

coverage_files = Dir[File.join(ROOT, "coverage", "*.yml")].sort

coverage_files.each do |path|
  begin
    manifest = YAML.safe_load(File.read(path), permitted_classes: [], aliases: false)
  rescue Psych::SyntaxError => error
    failures << "#{path}: invalid YAML: #{error.message}"
    next
  end

  unless manifest.is_a?(Hash) && !manifest.empty?
    failures << "#{path}: coverage manifest must be a nonempty mapping"
    next
  end

  manifest.each do |rule_id, record|
    unless record.is_a?(Hash)
      failures << "#{path}:#{rule_id}: coverage record must be a mapping"
      next
    end

    required = %w[documented detected auto_fix contexts protected_regions]
    missing = required.reject { |field| record.key?(field) }
    failures << "#{path}:#{rule_id}: missing #{missing.join(', ')}" unless missing.empty?

    %w[documented detected auto_fix].each do |field|
      next if [true, false].include?(record[field])
      failures << "#{path}:#{rule_id}: #{field} must be true or false"
    end

    contexts = record["contexts"]
    unless contexts.is_a?(Array) && !contexts.empty? && contexts.all? { |value| value.is_a?(String) }
      failures << "#{path}:#{rule_id}: contexts must be a nonempty string list"
    end

    unless %w[required partial not_applicable].include?(record["protected_regions"])
      failures << "#{path}:#{rule_id}: invalid protected_regions status"
    end

    if record["detected"]
      unless %w[vale python both contextual].include?(record["detection_mode"])
        failures << "#{path}:#{rule_id}: detected rules need a detection_mode"
      end
    elsif record.key?("detection_mode")
      failures << "#{path}:#{rule_id}: undetected rules must omit detection_mode"
    end

    if record["auto_fix"] && !record["detected"]
      failures << "#{path}:#{rule_id}: auto_fix requires detection"
    end

    implementations = record.fetch("implementations", [])
    unless implementations.is_a?(Array) && implementations.all? { |value| value.is_a?(String) }
      failures << "#{path}:#{rule_id}: implementations must be a string list"
      next
    end
    implementations.each do |relative_path|
      implementation_path = File.join(ROOT, relative_path)
      failures << "#{path}:#{rule_id}: missing #{relative_path}" unless File.file?(implementation_path)
    end
  end
end

if failures.empty?
  puts "#{fixtures.length} rule fixtures passed; #{coverage_files.length} coverage manifests validated."
  exit 0
end

warn failures.join("\n\n")
exit 1
