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

## D-010 — Body-copy bold is a closed presentation convention

- Status: Accepted
- Decision: Permit bold only for the first eligible full-name reference to a
  real person and for the visible text of a hyperlink. Keep preceding titles,
  offices, honorifics, affiliations and descriptive language outside the
  person-name span.
- Why: Bold is production structure in Florida Politics copy, not discretionary
  emphasis. A closed convention can be normalized and audited deterministically.
- Consequence: Hyperlink labels are structurally fixable. Person additions use
  caller-supplied approved names. Complete removal of other bold requires an
  explicit assertion that the document-specific person context is complete.

## D-011 — Person discovery remains consumer-owned

- Status: Accepted
- Decision: Accept approved, document-specific person names through the public
  presentation API without embedding a private roster or inferring identity in
  FlaPol Style.
- Why: A consumer can crawl and resolve the full article using its own current
  data, while the public package remains product-neutral and deterministic.
- Consequence: A nonempty list does not imply completeness. The caller must
  explicitly declare complete person context before broad nonlink-bold cleanup.

## D-012 — Consumer handoffs and issues are proposals, not authority

- Status: Accepted
- Decision: Treat every reporter alike. Issues and consumer handoffs may identify
  recurring patterns or regressions, but they do not admit rules or authorize
  changes to FlaPol Style.
- Why: Consumers are valuable sources of real-world evidence, but letting each
  product decide package policy would create conflicting rules, leak private
  assumptions and bypass deterministic-safety review.
- Consequence: Every report is reproduced and classified here. Filing,
  assigning or wording an issue does not admit a rule, select an action class,
  grant quote access, authorize implementation or approve a release.

## D-013 — Keep a narrow, dated public officeholder base

- Status: Accepted
- Decision: Maintain a public base book limited to Florida's Governor,
  Lieutenant Governor, Attorney General, Chief Financial Officer, Agriculture
  Commissioner, congressional delegation and state lawmakers. Build it from
  official government sources and keep reporter-, region- and newsroom-specific
  names in caller-supplied overlays.
- Why: State-versus-federal legislative style requires identity context, and
  this small high-value roster is public and reviewable. Expanding it into a
  general people database would create unnecessary maintenance and privacy
  scope.
- Consequence: This decision is a narrow qualification to D-011, not a transfer
  of private roster ownership. The book supplies identity evidence but does not
  itself authorize a textual change. Vacancies remain vacancies. Each group
  records when it was verified. The 2024-2026 state-legislator group is valid
  through Nov. 3, 2026, and hard-stale beginning Nov. 4: the public loader must
  require adjudication and refresh rather than continue returning that group.

## D-014 — Legislative jurisdiction style is document-level and identity-backed

- Status: Accepted; implemented in 0.1.0a5
- Decision: Select state-only, federal-only or mixed legislative title forms
  from resolved lawmakers present in the document. Use the public officeholder
  base plus caller overlays as identity evidence. Outside quotations,
  identity-proven forms may be corrected to `Rep.` or `Sen.`, `U.S. Rep.` or
  `U.S. Sen.`, or lowercase `state Rep.` or `state Sen.` as the document mode
  requires. Edited narration never uses `Florida Rep.` or `Florida Sen.`.
- Why: The same short title has different Florida Politics meaning depending on
  whether a story invokes state lawmakers, members of Congress or both. Text
  alone cannot safely establish that distinction; the dated book now supplies
  the missing evidence.
- Consequence: Implement the three rule families and proof boundaries in
  `docs/LEGISLATOR_STYLE_SCOPE.md` before claiming coverage. Preserve spoken
  jurisdiction words inside quotations, flag unresolved identities and mixed
  standalone attributions, and stop rather than use a stale required roster.

## D-015 — Numeric number signs require proven prose context

- Status: Accepted
- Decision: Outside quotations, automatically replace a numeric number sign
  only when the surrounding text proves a ranking, Executive Order, room or
  explicitly identified ballot-amendment form. Use `No.` for rankings, orders
  and rooms; omit the sign for ballot amendments. Flag other standalone `#N`
  forms. Do not match when another word character follows the digits.
- Why: A number sign is rarely acceptable in Florida Politics narrative copy,
  but the correct replacement depends on context and numeric hashtags such as
  `#8isEnough` must survive unchanged.
- Consequence: This rule family has no quotation access. Balanced quotations,
  including quoted rankings and social posts, are untouched and unflagged;
  malformed quotations and literal regions fail closed.
