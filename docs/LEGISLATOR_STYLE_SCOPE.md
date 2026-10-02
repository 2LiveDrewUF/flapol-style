# Registry-backed legislator style scope

## Status

Implemented for the `main` profile in `flapol-style` 0.1.0a5. The public
officeholder book supplies identity evidence to the document-level convention
below when a caller provides an explicit officeholder as-of date.

The governing source is Drew's Florida Politics ruling of Sept. 29-Oct. 2,
2026. Existing title-abbreviation rules remain independently active.

## Stable rule families

- `legislator-jurisdiction-before-name`
- `legislator-jurisdiction-plural`
- `legislator-jurisdiction-attribution`

These rules apply to the `main` profile. Headline treatment is outside this
scope until separately settled.

## Identity and document context

Use the dated public officeholder book plus caller-supplied overlays. Determine
the document mode from lawmakers whose identities resolve in the copy:

- **State-only:** one or more Florida state lawmakers and no members of
  Congress.
- **Federal-only:** one or more members of Florida's congressional delegation
  and no Florida state lawmakers.
- **Mixed:** at least one lawmaker from each level.
- **Unresolved:** no lawmaker identity resolves, or a relevant title-name form
  has ambiguous identity.

Institutional mentions such as `Florida Senate`, `U.S. Senate` or `House` do
not establish a person's identity. Detection may inspect protected speech for
the limited purpose of establishing who the document invokes, but it must not
mutate protected text except under the quotation rules below.

If a required roster is stale for the supplied as-of date, stop the
identity-dependent rule family and require adjudication. Do not guess from the
title text or silently continue with stale identities.

## Settled rendering

### State-only documents

- `Rep. NAME` and `Sen. NAME`
- `Reps. NAME1, NAME2 and NAME3` and
  `Sens. NAME1, NAME2 and NAME3`
- `"Quoted text," the Representative said` and
  `"Quoted text," the Senator said`

### Federal-only documents

- `U.S. Rep. NAME` and `U.S. Sen. NAME`
- `U.S. Reps. NAME1, NAME2 and NAME3` and
  `U.S. Sens. NAME1, NAME2 and NAME3`
- `"Quoted text," the U.S. Representative said` and
  `"Quoted text," the U.S. Senator said`

### Mixed documents

- Use `U.S. Rep.` or `U.S. Sen.` before a federal lawmaker's name.
- Use `state Rep.` or `state Sen.` before a Florida state lawmaker's name.
- Never use `Florida Rep.` or `Florida Sen.` as edited narration.

The long title immediately before a full name is abbreviated in every mode,
including inside balanced direct quotations. That written rendering is already
classified as speech-preserving by the existing title rules.

## Action classes

### `AUTO_FIX`

Outside quotations, a title immediately before a resolved current lawmaker's
full name may be normalized to the form required by the document mode. This
includes removing `Florida`, adding `U.S.` or lowercase `state`, and applying
the established `Rep.` or `Sen.` abbreviation.

The written plural title is abbreviated before a name, including inside a
balanced quotation. Outside quotations, its jurisdiction may be normalized
only when a syntactically closed coordinated list resolves every named person
to the same legislative level and chamber.

In a state-only or federal-only document, a standalone attribution title may be
normalized to the corresponding settled form when the attribution structure is
unambiguous.

### `FLAG`

Preserve and report instead of guessing when:

- a title-name identity is unknown or ambiguous;
- a coordinated list mixes chambers or legislative levels;
- a mixed document uses a standalone `Representative` or `Senator`
  attribution whose speaker cannot be bound deterministically;
- the copy concerns a former, historical or other-state lawmaker not resolved
  by the dated base book or a caller overlay; or
- quotation or document structure is malformed.

## Quotation and literal boundaries

Inside a balanced direct quotation, preserve spoken jurisdiction words. Thus a
speaker's `Florida Representative NAME` may receive the already authorized
`Representative` to `Rep.` rendering, but this rule family must not add, remove
or replace `Florida`, `state` or `U.S.` inside the quotation.

Unbalanced quotations fail closed. Code, literal examples, URLs, email
addresses and link destinations remain hard-protected.

## Implementation proof

The implementation uses the shared editing session and produces
original-source coordinates and structured before/after values. Tests cover:

- all three resolved document modes and the unresolved mode;
- singular and plural House and Senate forms;
- state-only and federal-only attributions plus mixed-document ambiguity;
- exact official names, aliases supplied by a caller and ambiguous names;
- straight quotes, curly quotes and unbalanced quotes;
- former, historical and other-state negative cases;
- code, URL, email and link-destination protection;
- roster staleness; and
- idempotence.

Coverage records detection and automatic correction separately. The
officeholder book remains identity evidence rather than authority for any
other textual rule.
