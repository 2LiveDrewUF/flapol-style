# FlaPol Style

`FlaPol` is a Vale-compatible implementation of deterministic Florida Politics house-style rules.

The package does not attempt to replace an editor or reproduce the AP Stylebook. It implements narrow, tested rules whose violations can be identified without inventing facts, changing quotations or making an unreviewed editorial judgment.

## Project boundary

This repository owns the public, product-neutral Florida Politics style kit.
It may use behavior observed in Drew-owned newsroom applications as
implementation evidence, but it does not own those applications or their
migration work.

In particular, Streamlet does not currently depend on this package. Any future
Streamlet integration, replacement of its internal formatter or retirement of
legacy behavior belongs to the separately managed Newsroom Tools project and
must be recorded there. This repository supplies a versioned dependency that
Newsroom Tools and other consumers may choose to integrate.

## Status

This repository is an early implementation scaffold. A rule is not considered implemented merely because the human guide discusses it. See `coverage/` for the implementation ledger.

The Python distribution is currently versioned `0.1.0a2`. A release tag makes
a version available to consumers; it does not imply that any application has
adopted it.

See `docs/RULE_SOURCES.md` for the provenance of automatic rules salvaged from
the legacy formatter and `docs/SALVAGE_LEDGER.md` for accepted, deferred and
rejected legacy behavior.

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
python/       protected, context-aware editing primitives
tests/        processor regression tests
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

## Context-aware processor

The Python package under `python/flapol_style/` contains transformations that
cannot safely be expressed as isolated Vale rules. It normalizes dates,
approved word forms and before-name title abbreviations while protecting
quotations, Markdown link destinations, URLs, email addresses and code.
Relative-date rules require an explicit publication date; the processor does
not infer one from the machine clock. Its word and title registries are public
data files so every automatic replacement can be reviewed without reading
application code.

Consumers can call `apply_main_style()` for the stable product-neutral
pipeline or use the narrower date, word-form and title functions separately.
The combined entry point includes automatic fixes only; it does not silently
turn flags or editor-only guidance into changes.

Consumers that need explainability can call
`apply_main_style_with_report()`. It returns an `EditResult` containing the
final text, ordered automatic changes and contextual findings. Every change
includes a stable rule ID, action, before/after text, authority and offsets into
the original source. The simple and reported APIs execute the same rule path.

Capitalization is deliberately split between automatic fixes and structured
findings. Named election stages, C-suite initialisms, Florida Legislature,
titles directly before full names and governmental bodies with an explicit
jurisdiction can be normalized automatically. Ambiguous seasons, standalone
titles, shortened governmental bodies and organization names are reported for
contextual review instead of being blindly uppercased.

The main pipeline also provides protected automatic forms for `COVID`, `U.S.`,
the gender-neutral `Chair`, numeral plus `%`, and lowercase punctuated
`a.m.`/`p.m.`. The separate
`apply_headline_style()` and `apply_headline_style_with_report()` entry points
convert imported title case to Florida Politics sentence case and apply the
headline-specific `US` to `U.S.` rule. Already sentence-cased headlines are
left alone. Quotes, acronyms, internal capitals, money expressions, stable
built-in proper nouns and caller-supplied preservation phrases are protected.
Headline rules do not silently inherit the body pipeline.

Run its tests with:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

Install the development package with:

```sh
python3 -m pip install .
```

JSON rule registries are included as package data. A consumer should pin a
published tag or commit; it should never treat floating `main` as a production
dependency.

See `CONTRIBUTING.md` for the rule-authoring and validation contract and
`CHANGELOG.md` for release notes. The structured result and coordinate
semantics are documented in `docs/PYTHON_API.md`.

## Source-material boundary

The repository does not contain the AP Stylebook, extracted AP chapters, private Slack exports or local source-file paths. AP-derived rules are concise operational implementations, not reproduced Stylebook entries.

## Acknowledgment

The repository structure, fixture strategy and coverage-accounting approach were informed by the MIT-licensed `vale-cli/Microsoft` package. No Microsoft writing preferences are inherited by default.
