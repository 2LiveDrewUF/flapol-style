# Python API contract

The package exposes two main entry points:

```python
apply_main_style(text, publication_date=None) -> str
apply_main_style_with_report(text, publication_date=None) -> EditResult
```

Both execute the same automatic rules in the same order. The string API is a
convenience wrapper around the reported API.

Headline-only behavior uses separate entry points:

```python
apply_headline_style(text, preserve_phrases=()) -> str
apply_headline_style_with_report(text, preserve_phrases=()) -> EditResult
```

The headline API converts imported title case to sentence case, keeps that
broad casing pass out of quoted and literal regions, and applies separately
classified headline-only house rules. The optional
`preserve_phrases` iterable lets a consumer protect current people, entities or
specialized proper nouns without moving a changing registry into this package.
The headline API does not implicitly call the main-body pipeline.

Presentation-only Markdown behavior uses separate entry points:

```python
apply_presentation_style(
    text,
    person_names=(),
    *,
    person_context_complete=False,
) -> str
apply_presentation_style_with_report(
    text,
    person_names=(),
    *,
    person_context_complete=False,
) -> EditResult
```

`text` is the body-copy Markdown scope to be normalized. Headlines remain a
separate profile and must not be prepended merely to help person discovery. A
consumer may inspect a broader article packet to build its person list, then
apply this API to the body field where first-reference bolding is required.

The presentation API treats bold as a closed house convention. It bolds the
visible labels of inline and reference-style Markdown links without changing
their destinations. It also moves approved before-name titles outside an
existing bold span and removes approved officeholder-group bolding such as
`**Flagler County commissioners**` without requiring a person roster.

`person_names` supplies approved exact full-name strings for the current body.
The first eligible exact occurrence of each supplied name is bolded; a broader
existing bold span is narrowed to the supplied name. The package does not
discover or verify people.

`person_context_complete=True` is an explicit caller assertion that the
supplied names are complete for the document. It authorizes removal of every
remaining nonlink bold span. Without that assertion, unresolved nonlink bold
is returned as a `FLAG` finding rather than removed. An empty complete list is
valid and means that the caller asserts the document contains no person names
eligible for first-reference bolding.

This API emits Markdown. It does not claim direct WordPress integration. An
HTML consumer should preserve the same semantic result by wrapping visible
hyperlink text in `strong` without changing the destination.

## EditResult

`EditResult.text` is the final transformed text. `changes` is an ordered tuple
of automatic edits. `findings` is a tuple of contextual conditions that were
not automatically changed.

Each `Edit` contains:

- `sequence`: application order within the editing session.
- `rule_id`: stable namespaced rule identifier.
- `action`: currently `AUTO_FIX` for changes.
- `before` and `after`: text at the moment that rule ran.
- `source_start` and `source_end`: half-open offsets into the untouched input.
- `working_start` and `working_end`: half-open offsets into the intermediate
  text at the moment the rule ran.
- `severity` and `authority`: review and provenance metadata.
- `speech_preserving`: whether the governing rule was explicitly authorized
  to render the same utterance inside a balanced direct quotation.

Later edits may operate on text produced by an earlier edit. The tracker
preserves unchanged subranges so both edits still map to the original source.
The `before` value of a later edit therefore may differ from the untouched
source slice. Consumers should use `EditResult.text` for the final document and
the ordered changes for explanation, not attempt to replay changes against the
original input without observing sequence and working offsets.

Each `Finding` contains a stable rule ID, `FLAG` action, found and suggested
forms, original-source offsets, severity and authority. A finding is not an
authorization to rewrite the text.

## Protection and metadata

Ordinary automatic edits and contextual findings exclude direct quotations.
An automatic rule may enter a balanced quotation only when its `RuleSpec` is
explicitly marked `speech_preserving=True`. Markdown link destinations, URLs,
email addresses, inline code and fenced code remain hard-protected from all
rules. Malformed or structurally uncertain quotations and code fences fail
closed.

Publication-date-relative behavior runs only when the caller supplies an
explicit `datetime.date`. The package never substitutes the machine's current
date.

Presentation formatting is classified as speech-preserving because it does not
change the utterance. It may operate inside balanced quotations, while code,
link destinations and structurally uncertain quotation or code regions remain
hard-protected.

## Versioning

The current API version is alpha `0.1.0a4`. Consumers must pin a released tag
or commit. Floating `main` is not a production dependency.
