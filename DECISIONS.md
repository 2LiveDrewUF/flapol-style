# Durable Decisions

Accepted decisions govern until a later accepted decision explicitly
supersedes them. New entries append; do not rewrite history to make chronology
look tidier than it was.

## D-001 — FlaPol Style is a public product-neutral kit

- Status: Accepted
- Decision: Maintain deterministic Florida Politics rules in a public package
  separate from every consuming application.
- Why: The rules are reusable, reviewable and nonproprietary, while consumers
  have different product, data and deployment lifecycles.
- Consequence: This repository publishes capability; consumers own adoption.

## D-002 — Later adopted guidance supersedes older practice

- Status: Accepted
- Decision: Apply the most recent adopted Florida Politics guidance. Historical
  disagreement is provenance, not a live conflict after practice is settled.
- Why: A canonical guide cannot behave like six years of unmerged local commits.
- Consequence: Surface only decisions that remain unresolved under current
  practice.

## D-003 — Implementation status has separate dimensions

- Status: Accepted
- Decision: Track documentation, detection, action class, automatic correction,
  context and protected-region support separately.
- Why: A prose rule or Vale alert does not prove safe automatic correction.
- Consequence: Coverage records cannot collapse implementation into one Boolean.

## D-004 — Automatic behavior must be deterministic and reportable

- Status: Accepted
- Decision: Automatic rules use stable IDs, explicit authority, exact before and
  after forms, original-source coordinates and idempotent transformations.
- Why: Consumers need to explain, compare and audit every mutation.
- Consequence: Semantic or context-dependent work remains a finding or editor call.

## D-005 — Quoted speech preserves utterance, not transcript orthography

- Status: Accepted; supersedes blanket quote immutability for the deterministic renderer
- Decision: Ordinary and generative editing cannot enter quotations. A specific
  deterministic rule may render inside a balanced quotation only when explicitly
  classified `speech_preserving` and authorized by AP or Florida Politics style.
- Why: Speech does not encode `advisor` versus `adviser`, words versus numerals,
  or `PM` versus `p.m.`, but it does encode grammar, word choice and meaning.
- Consequence: Quote safety is false by default, assigned rule by rule and
  reported on every edit. Uncertain quote structure and literal regions fail closed.

## D-006 — Protected literals are a separate hard boundary

- Status: Accepted
- Decision: Code, literal examples, URLs, email addresses and link destinations
  remain protected even inside balanced quotations.
- Why: These strings are character-sensitive rather than ordinary prose.
- Consequence: `speech_preserving` never overrides literal protection.

## D-007 — Releases use immutable annotated tags

- Status: Accepted
- Decision: Release from a green `main` commit, then create and push an annotated
  `v`-prefixed tag and verify the independent tag workflow.
- Why: Consumers need a stable auditable dependency rather than floating `main`.
- Consequence: A bad release is superseded; published tags are not moved or deleted.

## D-008 — The canonical local home is the DrewGPT project

- Status: Accepted
- Decision: `/Users/drew/DrewGPT/FlaPol Style` is the canonical local checkout.
  The former synced ChatGPT-project checkout is no longer the operating home.
- Why: The work now manages a real repository and requires durable local project
  governance beyond a conversation mirror.
- Consequence: Future work begins here and reconciles with the public remote.

## D-009 — No fictional services or infrastructure

- Status: Accepted
- Decision: Record that the project currently operates no hosted service and
  manages no production host. GitHub is the remote and CI provider, not a server
  administered by this project.
- Why: Empty ceremonial infrastructure records create false confidence.
- Consequence: Add a service or system record only when a real managed target exists.
