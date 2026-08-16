# FlaPol Style — Agent Instructions

## Mission

Maintain the public, product-neutral Florida Politics style kit. Convert only
settled, sourced rules into deterministic behavior; expose uncertainty instead
of laundering it into confident automation.

## Startup

At the start of substantive work:

1. Read `PROJECT.md`, `STARTUP.md`, `OWNERSHIP.md` and relevant decisions.
2. Inspect `git status --short --branch` and current branch history.
3. Read the applicable runbook and rule-source documentation.
4. Resolve the exact requested scope before editing or publishing.

## Jurisdiction

This project owns:

- the public `flapol-style` repository;
- Vale rules and fixtures;
- the public Python package and registries;
- rule provenance, coverage and governing policy;
- tests, reports and release tags; and
- product-neutral integration contracts.

This project does not own:

- Newsroom Tools or Streamlet source, deployment or retirement work;
- WordPress, newsletter assembly or product-specific HTML cleanup;
- private people, officeholder or newsroom registries;
- generative language editing; or
- the AP Stylebook text or other third-party copyrighted sources.

Private implementations may be inspected read-only when explicitly authorized
and useful. Do not modify them from this project or copy private internals into
the public repository.

## Governing authority

Use this order:

1. The user's explicit current instruction.
2. Later adopted Florida Politics guidance.
3. Accepted project decisions and the canonical guide.
4. Current AP guidance where no house override exists.
5. The pinned AP baseline.
6. Legacy behavior as evidence, never authority by mere survival.

When chronology resolves a conflict, implement the current rule and do not
resurrect superseded disagreement as a live decision.

## Rule admission

Before adding or changing a rule, establish:

- the governing source and date;
- the stable rule ID;
- the applicable profile or context;
- `AUTO_FIX`, `FLAG`, `EDITOR_ONLY` or reference-only status;
- whether the text alone proves the correction;
- protected-region behavior;
- explicit quotation classification;
- positive, negative, boundary and idempotence examples; and
- coverage and documentation changes.

A rule's presence in Vale, a registry, Slack history or a legacy formatter does
not authorize automatic correction.

## Quotation boundary

Preserve what the speaker said, not necessarily a transcription engine's raw
orthography.

- Generative, semantic and ordinary copy editing cannot alter quotations.
- Deterministic rendering may enter a balanced quotation only when that exact
  rule has `speech_preserving=True`.
- Apply the read-aloud test, but do not treat it as sufficient authority.
- A registry or rule family cannot grant quote access implicitly.
- Code, literal examples, URLs, email addresses and link destinations remain
  hard-protected.
- Unbalanced or structurally uncertain quotations fail closed.
- Every in-quote mutation must use the ordinary structured report.

Read `docs/QUOTE_POLICY.md` before changing quotation behavior.

## Implementation rules

- Keep main, headline, presentation and product-specific profiles explicit.
- Keep input sanitation separate from editorial transformations.
- Prefer public data registries for reviewable closed mappings.
- Use stable namespaced rule IDs and never recycle an ID for new behavior.
- Preserve original-source coordinates through every transformation.
- Make transformations idempotent.
- Treat findings as findings; never silently promote them to fixes.
- Fail conservatively when entity identity, dates, meaning or structure is
  uncertain.

## Validation

For behavior changes:

- add positive and negative tests;
- test straight and curly quotes where quote scope matters;
- test code, URL and literal protection;
- test malformed input and fail-closed behavior;
- test structured before/after values and source offsets;
- test idempotence; and
- run `scripts/verify.sh`.

GitHub branch and tag CI are authoritative for the pinned Vale binary,
minimum-supported Python installation and installed-package smoke test.

## Documentation and provenance

- Record concise derived rules, source names and dates.
- Do not commit the AP e-book, copied AP entries, private Slack exports,
  unpublished copy, credentials or private registries.
- Update `coverage/`, `docs/RULE_SOURCES.md`, `CHANGELOG.md` and decisions when
  the behavior or architecture materially changes.
- Record a durable architectural or editorial ruling in `DECISIONS.md`.

## Git and releases

- Do not publish, tag, delete or rewrite remote history without user authority.
- Preserve unrelated worktree changes.
- Release only from a verified `main` commit using `runbooks/release.md`.
- Use annotated immutable tags with a `v` prefix.
- Verify branch CI before tagging and tag CI after pushing the tag.
- Never move or delete a published tag to conceal a mistake; supersede it.
- A release makes capability available. It does not imply consumer adoption.

## Communication

Lead with the outcome. Separate implemented behavior, findings, open decisions
and consumer-owned work. Do not call a rule “covered” when it is merely
documented or detected.
