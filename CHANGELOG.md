# Changelog

This project follows semantic versioning. Release tags use a `v` prefix; the
Python distribution exposes the corresponding PEP 440 version without that
prefix.

## 0.1.0a1 — Unreleased

- Add an installable Python package with included JSON rule registries.
- Add protected date, word-form, title and capitalization transformations.
- Add protected COVID, percent and meridiem auto-fixes already represented by
  Vale rules.
- Add a reportable headline profile that converts imported title case to
  Florida Politics sentence case, accepts caller-supplied proper nouns and
  applies the Florida Politics `U.S.` form.
- Add stable rule IDs and structured `EditResult` reporting against original
  source coordinates.
- Separate automatic capitalization from contextual findings.
- Replace Boolean coverage markers with documentation, detection, correction,
  context and protected-region records.
- Record the Streamlet salvage and project-ownership boundaries.

No release or adoption by a consuming application is implied by this
unreleased entry.
