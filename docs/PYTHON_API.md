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
apply_headline_style(text) -> str
apply_headline_style_with_report(text) -> EditResult
```

The headline API currently performs only explicitly implemented headline
rules and does not implicitly call the main-body pipeline.

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

Automatic edits and findings exclude direct quotations, Markdown link
destinations, URLs, email addresses, inline code and fenced code. Malformed
unclosed quotations and code fences fail closed.

Publication-date-relative behavior runs only when the caller supplies an
explicit `datetime.date`. The package never substitutes the machine's current
date.

## Versioning

The current API version is the unreleased alpha `0.1.0a1`. Consumers must pin a
released tag or commit. Floating `main` is not a production dependency.
