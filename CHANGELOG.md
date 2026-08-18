# Changelog

This project follows semantic versioning. Release tags use a `v` prefix; the
Python distribution exposes the corresponding PEP 440 version without that
prefix.

## 0.1.0a4 — 2026-08-18

- Add a Markdown presentation API for Florida Politics' closed bolding
  convention.
- Bold inline and reference-style hyperlink labels without changing link
  destinations.
- Move approved full and abbreviated office or corporate titles outside
  otherwise name-shaped bold spans.
- Remove bold from approved officeholder-group language including
  commissioners, governors, representatives, senators, state reps and state
  sens.
- Accept caller-supplied document person names for first-reference bolding and
  require an explicit completeness assertion before removing all remaining
  nonlink bold.
- Report unresolved nonlink bold as findings when person context is incomplete.
- Extend exact-span structured reporting for presentation adapters.

## 0.1.0a3 — 2026-08-16

- Replace blanket quotation immutability with explicit rule-level
  `speech_preserving` classification.
- Keep balanced quotations closed to ordinary and semantic editing while
  allowing approved written-style renderings of the same spoken utterance.
- Keep code, URLs, link destinations, email addresses and structurally
  uncertain quotations hard-protected from every rule.
- Apply approved adviser, word-form, capitalization, title, date-display,
  `U.S.`, percent and meridiem rendering inside balanced quotations.
- Add spoken-number transcript handling for percentages through 999 and spoken
  one-through-twelve meridiem hours.
- Include quote-safety metadata on every structured automatic edit.

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
