#!/usr/bin/env ruby

require "open3"

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
  File.readlines(path).each_with_index do |line, index|
    if line.start_with?("# ")
      line.scan(/([A-Za-z][A-Za-z0-9]+\.yml)/).flatten.each do |rule|
        rule_path = File.join(ROOT, "FlaPol", rule)
        failures << "#{path}:#{index + 1}: missing #{rule}" unless File.file?(rule_path)
      end
    end

    content = line.sub(/#.*/, "").strip
    next if content.empty?

    key, value = content.split(":", 2).map(&:strip)
    unless key && %w[true false].include?(value)
      failures << "#{path}:#{index + 1}: coverage values must be true or false"
    end
  end
end

if failures.empty?
  puts "#{fixtures.length} rule fixtures passed; #{coverage_files.length} coverage manifests validated."
  exit 0
end

warn failures.join("\n\n")
exit 1
