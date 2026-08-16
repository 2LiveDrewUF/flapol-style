# FlaPol Style

`FlaPol` is a Vale-compatible implementation of deterministic Florida Politics house-style rules.

The package does not attempt to replace an editor or reproduce the AP Stylebook. It implements narrow, tested rules whose violations can be identified without inventing facts, changing quotations or making an unreviewed editorial judgment.

## Status

This repository is an early implementation scaffold. A rule is not considered implemented merely because the human guide discusses it. See `coverage/` for the implementation ledger.

## Authority

Rules are derived from:

1. The current Florida Politics house-style guide.
2. A pinned AP Stylebook edition where Florida Politics has no override.
3. Product-specific profiles where expressly applicable.

Florida Politics house style controls when it differs from AP. Later adopted Florida Politics guidance controls over older guidance.

## Safety boundary

The package must not automatically alter:

- Direct quotations.
- URLs or Markdown link destinations.
- Code or literal text.
- Verified formal names and document titles.
- Language reserved for writer or editor judgment.

Vale alone cannot identify every protected inline quotation or resolve every document-level question. A Florida Politics document processor will supply those protections and the metadata needed by contextual rules.

## Repository structure

```text
FlaPol/       Vale rule files
fixtures/     isolated inputs for individual rules
coverage/     source-topic implementation status
docs/         public governing documentation
tools/        validation and packaging utilities
```

## Vale configuration

For local development:

```ini
StylesPath = .
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = FlaPol
```

Published releases will contain a `FlaPol.zip` package suitable for a version-pinned `Packages` URL and `vale sync`.

## Rule levels

| Vale level | Florida Politics meaning |
| --- | --- |
| `error` | A concrete violation with one intended deterministic form. |
| `warning` | The condition can be detected, but correction requires context. |
| `suggestion` | Editorial or craft concern; the text is not presumed wrong. |

Only tested `error` rules with a safe correction action may be eligible for automatic application by the Florida Politics document processor.

## Source-material boundary

The repository does not contain the AP Stylebook, extracted AP chapters, private Slack exports or local source-file paths. AP-derived rules are concise operational implementations, not reproduced Stylebook entries.

## Acknowledgment

The repository structure, fixture strategy and coverage-accounting approach were informed by the MIT-licensed `vale-cli/Microsoft` package. No Microsoft writing preferences are inherited by default.
