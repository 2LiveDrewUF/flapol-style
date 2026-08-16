# FlaPol Style Project Charter

## Status

Active — public deterministic style kit released through `v0.1.0a3`; downstream adoption remains consumer-owned.

## Ownership and placement

- Owner: Drew
- Domain: Florida Politics editorial standards and deterministic rendering
- Canonical local location: `/Users/drew/DrewGPT/FlaPol Style`
- Public repository: `2LiveDrewUF/flapol-style`
- Default branch: `main`
- License: MIT for repository-owned source; third-party rights remain separate

This project began as work inside a Florida Politics assistant conversation and
became a maintained public package with its own rule lifecycle, tests, releases
and downstream consumers. It therefore has a distinct home and must not be
managed from the former synced-chat mirror.

## Mission

Maintain a public, product-neutral Florida Politics style system that turns
settled AP and house-style decisions into inspectable, deterministic and
reportable behavior without pretending that every editorial judgment can be
automated.

## Goals

- Record current Florida Politics rules and concise provenance.
- Apply later adopted guidance over superseded historical practice.
- Distinguish documentation, detection, automatic correction, findings and
  editor-only guidance.
- Keep automatic transformations deterministic, protected and idempotent.
- Preserve spoken substance while permitting explicitly speech-preserving
  written rendering inside balanced quotations.
- Expose stable rule IDs, authority, before/after forms and source locations.
- Publish immutable, tested releases that consumers can adopt deliberately.
- Reuse sound legacy logic without importing private product behavior or
  obsolete decisions wholesale.

## Non-goals

- Reproducing or redistributing the AP Stylebook.
- Replacing a human editor or authorizing generative quote editing.
- Owning Streamlet, Newsroom Tools, WordPress, newsletter assembly, name
  registries, deployment or downstream rule retirement.
- Treating every suggestion, Slack reminder or legacy regex as current law.
- Storing private Slack exports, article text, credentials, private registries
  or proprietary application code in this public repository.
- Creating hosted services or infrastructure merely to make the project look
  more important at cocktail parties.

## Inputs

- Current Florida Politics owner rulings and canonical guide decisions.
- A pinned AP baseline where Florida Politics has no later override.
- Public AP updates that supersede the pinned baseline.
- Existing Vale rules, fixtures and public package behavior.
- Read-only evidence from legacy newsroom implementations when authorized.
- Consumer bakeoffs and reproducible false-positive or false-negative cases.

## Outputs

- Public Vale rules and fixtures.
- An installable Python package with protected, context-aware APIs.
- Public rule registries and coverage records.
- Structured changes and contextual findings.
- Provenance, quote-policy and migration documentation.
- Immutable Git tags with verified branch and tag CI.
- Narrow downstream handoff contracts, not consumer-side implementation.

## Authority order

1. Drew's explicit current ruling.
2. Later adopted Florida Politics guidance.
3. The canonical Florida Politics guide and accepted project decisions.
4. Current AP guidance where Florida Politics has no override.
5. The pinned AP baseline.
6. Legacy implementation behavior as evidence only.
7. Inference, clearly labeled and never promoted to an automatic rule by itself.

## Primary risks

### Silent meaning changes

Automatic rules must be narrow, deterministic and tested. Contextual or
semantic questions become findings or editor-only guidance.

### Quote corruption

Ordinary and generative editing cannot enter quotations. A deterministic rule
may enter a balanced quotation only through explicit `speech_preserving`
classification and the read-aloud test. Uncertain quote structure fails closed.

### Copyright or private-source leakage

Record concise derived rules and provenance, not copied AP entries, e-books,
Slack history, private source code or unpublished newsroom text.

### Consumer regression

A public implementation does not prove safe adoption. Consumers compare a
released version against their real inputs, supply required context and own
their cutover and rollback.

### Release drift

Tags are immutable. A bad release is superseded by a new version; tags and
published history are never rewritten to disguise an error.

## Success criteria

The project is healthy when:

- a new maintainer can orient from `STARTUP.md` and `AGENTS.md`;
- every automatic rule has authority, stable identity, context and boundaries;
- quote access is explicit rather than inherited from a broad family;
- tests cover positive, negative, protected, malformed and idempotent cases;
- release tags point to green commits and install successfully;
- public documentation matches actual behavior;
- downstream consumers can identify exactly what a release replaces; and
- private product and source boundaries remain intact.
