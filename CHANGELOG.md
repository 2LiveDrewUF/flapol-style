# Changelog

This project follows semantic versioning. Release tags use a `v` prefix; the
Python distribution exposes the corresponding PEP 440 version without that
prefix.

## Unreleased

- Add bounded body-copy President and local-office capitalization, named
  Police Department references, approved military ranks and U.S. Amb. before
  full names, numbered street-address abbreviations, rescope/preconstruction
  forms and the clarified no-party voter/member wording.
- Add review findings for ambiguous local bodies and titles, corporate
  designators, first-reference NPA voter/member/candidate forms, legal
  intervener, internal City of and adverse vote-tally order. New rules preserve
  quotations and literals; no headline or presentation behavior is added.
- Capitalize `Speaker Pro Tempore` and `President Pro Tempore` in body
  narration, including standalone titles, under the Nov. 11 owner ruling.

## 0.1.0a9 — 2026-11-05

- Refresh the state officeholder roster for the 2026-2028 term, including
  House District 33 as pending election and Senate District 39 as vacant.
  Keep the previous snapshot available for dates through Nov. 3, 2026.
- Use primary names without middle initials in the refreshed state roster
  and resolve sourced initials and quoted nicknames for legislative titles.
- Record the incoming U.S. House slate and Florida executive transition
  separately from the sitting officeholders. Mark four congressional
  leaders provisional pending certification.

## 0.1.0a8 — 2026-10-07

- Require dated officeholder or caller-overlay identity before abbreviating
  unqualified `Representative`, `Representatives`, `Senator` or `Senators`,
  preventing organizational, applicant, local-office and institutional false
  positives while retaining identity-proven quotation rendering.
- Preserve the full formal phrase `Commissioner of Agriculture and Consumer
  Services` instead of applying the shorter Agriculture Commissioner ordering
  rule.

## 0.1.0a7 — 2026-10-02

- Normalize lowercase or mis-cased month names when a following day or year
  proves date context, including in headlines and balanced quotations.

## 0.1.0a6 — 2026-10-02

- Preserve title-cased `Advisor` as possible formal-name text while retaining
  automatic correction of lowercase `advisor` and all-capital `ADVISOR`.
- Normalize context-proven numeric number signs in body copy and headlines,
  flag unresolved forms, preserve hashtag-like tokens such as `#8isEnough`,
  and keep every hash form inside quotations untouched.

## 0.1.0a5 — 2026-10-02

- Add a narrow, official-source Florida officeholder book covering the
  Governor, Lieutenant Governor, Cabinet, congressional delegation and state
  lawmakers, while preserving vacancies and caller-owned overlays.
- Make the 2024-2026 state-legislator book valid through Nov. 3, 2026, and
  refuse to load it beginning Nov. 4 until it is adjudicated and refreshed.
- Scope the registry-backed state-only, federal-only and mixed-document
  legislator title convention and implement it through explicit dated identity
  context, caller overlays, protected automatic fixes and structured findings.
- Remove redundant `Florida` from `Florida Governor` or `Florida Gov.` directly
  before a full name, then apply the existing `Gov.` title abbreviation.
- Capitalize `Governor` with or without a connected name and flag, rather than
  automatically changing, `Florida Governor` without a full name.
- Use the capitalized `Agriculture Commissioner` house title in body copy and
  headlines; capitalize the title in quotations without changing the speaker's
  ordering.
- Add a public issue form for repeatable style gaps and regressions.
- Clarify that issues and consumer handoffs are evidence, not authority to
  admit a rule or change the package.

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
