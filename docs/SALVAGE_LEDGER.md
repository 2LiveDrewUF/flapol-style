# Streamlet salvage ledger

This ledger records which existing Streamlet formatter assets may become part
of the canonical Florida Politics style suite. Streamlet is implementation
evidence, not governing authority. The current Florida Politics guide and its
chronology rule control when legacy behavior differs.

## Responsibility boundary

This repository is responsible only for the public `flapol-style` kit.
Inspection of the private Newsroom Tools repository is read-only research used
to avoid rebuilding proven, Drew-owned logic from scratch.

This project does not:

- Modify Streamlet or any other Newsroom Tools product.
- Add a Streamlet dependency on `flapol-style`.
- Retire or disable Streamlet formatter behavior.
- Decide when a Newsroom Tools deployment adopts this package.
- Record a migration as complete merely because equivalent behavior exists
  here.

Newsroom Tools owns its future integration, transition, deployment and legacy
retirement work. Other products may integrate the public kit independently.
Until a consumer explicitly adopts a released version, the presence of a rule
in this repository says nothing about that consumer's active behavior.

## Port now

| Streamlet asset | Reusable value | Canonical treatment |
| --- | --- | --- |
| Date display normalization | AP month forms, ordinal removal and month-year punctuation | Port as isolated, protected-region-aware rules. |
| Publication-date-relative dates | Weekday validation, seven-day window and current-year removal | Require an explicit publication date; never default to the machine date. |
| Quote-span concept | Separate spoken substance from written rendering | Replace the limited 600-character regex with fail-closed structural detection. Only explicitly speech-preserving deterministic rules may enter balanced quotations. |
| Diff renderer | Human-readable before/after review | Retain as a later UI component after the rule engine emits structured changes. |
| First-reference registry parser | Canonical names, variants, nicknames and federal/state metadata | Separate registry construction from product-specific bolding behavior. |
| Bold-marker technique | Preserve intended tags through escaping | Retain where an HTML output adapter needs it; do not make it the core document representation. |
| Hyperlink bolding | Enforce the house link-format rule | Port into an HTML/Markdown adapter without changing destinations. |

## Review before porting

| Streamlet asset | Reason for review |
| --- | --- |
| Capitalization table | Contains useful house terms but broad case-insensitive replacement can change generic uses and quotations. Keep as flags until the term can be recognized in its Florida governmental or title sense. |
| Remaining headline proper-noun table | A small stable public seed and a caller-supplied preservation seam are implemented. The remainder of the 475-entry legacy list still needs duplicate, ambiguity, currency and provenance review. |
| Person registries | Thousands of public-name entries can save work, but currentness, aliases and public-release suitability must be checked. |
| Legacy headline title stripping and surname expansion | Kept separate because both change editorial meaning or naming; neither is part of sentence-case normalization. |
| Party/location tag stripping | Potentially useful for imported wire copy; it deletes text and depends on entity/context recognition. |
| State/federal legislator scoping | Valuable and appropriately registry-driven; requires a maintained, dated officeholder registry. |
| Remaining word-preference entries | Each substitution needs comparison with the current guide and AP baseline. Do not inherit the table wholesale. |

## Exclude from canonical main behavior

| Legacy behavior | Controlling reason |
| --- | --- |
| Infer quote safety from a registry or broad rule family | Quote access must be granted rule by rule under the speech-preserving policy. |
| Treat unbalanced quotation marks as ordinary unquoted text | The deterministic system must fail closed. |
| Default relative-date calculations to the day the software happens to run | Publication date is required context. |
| Compress a body name to a surname because it appeared in a headline | Sunburn-specific production behavior, not newsroom-wide first-reference style. |
| Strip every governmental title from headlines | Conflicts with the `Gov. DeSantis` official-action rule and is not a universal main-guide rule. |
| Normalize aliases merely because a dictionary recognizes a variant | Preferred-name changes require authoritative identity data and editorially approved mappings. |

## First salvaged implementation

The initial port lives in `python/flapol_style/` and contains:

- Fail-closed structural handling for direct quotations plus hard protection
  for Markdown link destinations, URLs, email addresses, inline code and
  fenced code.
- Fixed AP date-display normalization.
- Contextual weekday-window and current-year normalization requiring an
  explicit publication date.
- Regression tests derived from both the legacy behavior and current policy.

## Second salvaged implementation

The next product-neutral tranche adds public, data-backed registries for:

- `longtime`, `re-election`, `front-runner`, `healthcare` and `news conference`.
- Gov., Lt. Gov., Rep., Sen., U.S. Rep. and U.S. Sen. directly before a full
  name.
- CEO, CFO, COO and CMO directly before a full name.

Every replacement runs through the protected-region engine and has regression
coverage. Titles used alone or after a name are not abbreviated. State Attorney
is deliberately absent from the abbreviation registry.

The reconciliation decisions behind this tranche are explicit:

- `healthcare` is accepted as a later AP change announced April 27, 2026; it
  supersedes the supplied 56th-edition `health care` entry. The public source
  links are recorded in `RULE_SOURCES.md`.
- `news conference` is retained instead of `press conference`.
- The legacy `preempt` to `pre-empt` replacement is rejected. Current AP
  guidance generally omits the hyphen after common prefixes, and Florida
  Politics has adopted no contrary house rule. The official AP source is
  recorded in `RULE_SOURCES.md`.
- `child care` remains unchanged.

At the end of the second tranche, broad capitalization remained deferred
pending a split between context-proven fixes and contextual findings. The
third tranche below implements that split.

## Third salvaged implementation

The legacy capitalization table has been reconciled entry by entry. Its old
universal, case-insensitive replacement behavior remains rejected. The public
processor now:

- Automatically capitalizes named election stages, including `Midterms`.
- Automatically normalizes Florida Legislature, C-suite initialisms, titles
  directly before full names and governmental bodies with an explicit
  jurisdiction.
- Reports structured findings for standalone titles, seasons, shortened
  governmental bodies and ambiguous organization or house-term strings.
- Includes `Second Lady` under the title rule by owner ruling.
- Allows context-proven capitalization rendering inside balanced quotations;
  contextual findings and literal regions remain excluded.

The legacy table's 26 entries now have no unresolved policy items. The broader
main guide still contains capitalization rules that were not present in that
table; their coverage remains recorded separately rather than being inferred.

## Package and reporting foundation

Before additional Streamlet rule families are salvaged, the Python processor
is packaged as an alpha distribution and exposes structured
edit reporting. The reported and string-only APIs share one editing session.
Each automatic change carries a stable rule ID, action, working text,
before/after value, authority and offsets into the untouched source. Contextual
capitalization findings use the same source-coordinate contract.

Coverage records now distinguish documentation, detection mode, automatic
correction, applicable profiles and protected-region support. This prevents a
Vale alert or a prose rule from being mistaken for a protected automatic fix.

This foundation does not adopt the package in Streamlet. Release pinning,
shadow comparison, rule-family cutover and legacy retirement remain Newsroom
Tools responsibilities.

With reporting in place, the approved `COVID`, body-copy `U.S.`, gender-neutral
`Chair`, numeral-plus-percent-sign and meridiem forms run through the protected
main processor. The separate headline entry point converts imported title case
to sentence case and applies the headline `U.S.` form. It preserves stable
public proper nouns and accepts caller-supplied names without importing legacy
title removal, surname expansion or product-specific cleanup.

No private Streamlet source, production path, credential or private repository
metadata is reproduced in this public ledger.

## Presentation bolding tranche

The public Markdown presentation API now implements the closed Florida Politics
bolding convention adopted Aug. 18, 2026. Hyperlink labels are always bolded;
approved titles are moved outside name-shaped bold spans; and approved
officeholder-group terms lose erroneous bolding. The package accepts an ad hoc,
document-specific list of approved person names for additive first-reference
bolding. An explicit completeness assertion is required before the formatter
removes all other nonlink bold.

This tranche creates an integration seam but does not implement a Newsroom
Tools crawler, identity resolver, Markdown-to-HTML conversion, WordPress write
or consumer pin. Those remain consumer-owned work.
