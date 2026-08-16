# Changelog

This project follows semantic versioning. Release tags use a `v` prefix; the
Python distribution exposes the corresponding PEP 440 version without that
prefix.

## 0.1.0a2 — 2026-08-16

- Convert imported title case to Florida Politics sentence case through the
  explicit headline API.
- Preserve stable proper nouns and accept caller-supplied names during
  headline normalization.
- Normalize bare `US` to `U.S.` in protected body copy.
- Normalize `Chairman` and `Chairwoman` to the house `Chair` form outside
  protected regions.
- Update the package, coverage and migration documentation for the first
  Newsroom Tools cutover tranche.

## 0.1.0a1 — 2026-08-16

- Add an installable Python package with included JSON rule registries.
- Add protected date, word-form, title and capitalization transformations.
- Add protected COVID, percent and meridiem auto-fixes already represented by
  Vale rules.
- Add the initial narrow headline `U.S.` rule.
- Add stable rule IDs and structured `EditResult` reporting against original
  source coordinates.
- Separate automatic capitalization from contextual findings.
- Replace Boolean coverage markers with documentation, detection, correction,
  context and protected-region records.
- Record the Streamlet salvage and project-ownership boundaries.

No adoption by a consuming application is implied by a package release.
