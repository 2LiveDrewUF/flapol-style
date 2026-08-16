# Contributing

Every contribution must preserve the distinction between an adopted rule, a
detectable condition and a safe automatic correction.

Project-wide operating instructions live in `AGENTS.md`. Use
`runbooks/add-or-reclassify-rule.md` for rule work and `runbooks/release.md` for
publication.

## Rule workflow

1. Identify the governing source and record concise provenance. Florida
   Politics main controls over AP; later adopted guidance controls over older
   guidance.
2. Assign a stable, namespaced rule ID. Do not recycle an ID for a different
   behavior.
3. Classify the action as `AUTO_FIX`, `FLAG`, `EDITOR_ONLY` or reference-only.
4. Add positive, negative and boundary examples.
5. For an automatic rule, add quotation, protected-region and idempotence
   tests.
6. Implement detection independently from automatic eligibility. A Vale alert
   does not by itself authorize a Python rewrite.
7. Update the appropriate coverage record: documentation, detection mode,
   automatic status, contexts, protected-region support and implementation
   paths.
8. Run the Vale fixtures, coverage validator, Python tests and installed-package
   smoke test.
9. Record a Florida Politics departure from AP without reproducing copyrighted
   Stylebook text.

## Scope boundaries

- Main rules must remain product-neutral.
- Headline, presentation and newsletter behavior must use explicit profiles.
- Input sanitation must remain separate from editorial transformations.
- Do not add private article text, Slack exports, credentials or application
  internals to fixtures.
- Streamlet and other Newsroom Tools applications decide when to adopt a
  released version; this repository does not perform their migration.

## Required checks

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
VALE_BIN=/path/to/vale ruby tools/test_rules.rb
python3 -m pip install .
```

After installation, verify the package from outside the repository so a source
directory cannot hide missing package data.
