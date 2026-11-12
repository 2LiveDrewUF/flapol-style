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

## D-016 — Unqualified legislative-title abbreviations require identity

- Status: Accepted; implemented in 0.1.0a8
- Decision: Do not abbreviate unqualified `Representative`, `Representatives`,
  `Senator` or `Senators` merely because name-shaped text follows. Require the
  dated public officeholder book or a caller overlay to resolve the named
  person or people to the matching chamber. Explicit `U.S.` legislative titles
  remain eligible for the general title registry because their jurisdiction is
  stated in the text.
- Why: Organizational representatives, applicants, former local officials and
  institutional names can share the same surface pattern. Capitalization-shaped
  text is not identity proof.
- Consequence: Identity-proven abbreviation alone is speech-preserving inside
  balanced quotations, but the rule preserves every spoken jurisdiction word.
  Unknown or ambiguous title-name forms remain unchanged and are findings only
  when the text presents the term as a legislative title. The formal phrase
  `Commissioner of Agriculture and Consumer Services` is also protected from
  the shorter Agriculture Commissioner ordering rule.

## D-017 — Select the state roster by legislative term

- Status: Implemented, Nov. 5, 2026
- Decision: Preserve the 2024-2026 snapshot for dates through Nov. 3, 2026.
  Use the refreshed 2026-2028 House and Senate rosters from Nov. 4, 2026,
  through the House's listed term end on Nov. 7, 2028. Require adjudication
  starting Nov. 8, 2028, unless a subsequent snapshot covers that date.
- Decision: Omit middle initials from primary names in the refreshed state
  roster. Retain official source names and use source-derived aliases for
  formal, shortened and quoted-nickname forms. These are identity data for the
  existing legislative-title rules.
- Consequence: House District 33 is pending election and Senate District 39
  is vacant as of Nov. 5, 2026. The term boundary is a backstop. Recheck
  individual seats when official changes are reported.

## D-018 — Record incoming officeholders separately

- Status: Implemented, Nov. 5, 2026
- Decision: Keep sitting officeholders in `entries` and record incoming
  officeholders in the group's `incoming` section, with the evidence date
  and expected start. Mark the four U.S. House races Drew identified as
  unresolved as provisional. Reconcile results against certification.
- Consequence: Existing identity rules use sitting officeholders. The
  current congressional and executive snapshots require adjudication on
  Jan. 3 and Jan. 5, 2027, respectively. Confirm seating or assumption of
  office before activating the incoming entries, then preserve the prior
  sitting roster for historical dates.

## D-019 — Capitalize both Pro Tempore office titles

- Status: Accepted, Nov. 11, 2026. Implemented for the next release.
- Decision: In the main/body profile, capitalize the full office titles
  `Speaker Pro Tempore` and `President Pro Tempore`, with or without a
  connected name.
- Authority: Drew's Nov. 11, 2026, Florida Politics owner ruling.
- Classification: `AUTO_FIX` for either complete title in narration.
  `flapol.capitalization.speaker-pro-tempore-title` and
  `flapol.capitalization.president-pro-tempore-title` have
  `speech_preserving=False`. Quotation and literal protections apply.
- Evidence: The a9 body processor preserved correctly capitalized input.
  The admitted change normalizes lowercase and mixed-case full titles.

## D-020 — Admit bounded Nov. 11 style intake

- Status: Accepted and implemented for the next release, Nov. 11, 2026.
- Authority: Drew's Nov. 10 President ruling and Nov. 11 implementation
  instructions and clarification, informed by Peter's review corrections.
- Main/body automatic changes: President and explicit compound/plural forms;
  City Manager, City Attorney, Council Member and Board Member, including
  plural and singular -elect forms; named Police Department and narrowly
  supported definite references; approved military title forms before a full
  name; U.S. Ambassador to U.S. Amb. before a full name; numbered-address
  Avenue, Boulevard and Street; rescope inflections and preconstruction;
  no-party-affiliation voter/member to no-party voter/member; and the exact
  paired phrase third- and no-party voters.
- Preserve the stable President and Vice President IDs when promoting their
  narration behavior from findings to automatic changes. Previously permitted
  before-full-name quotation rendering retains its existing separate IDs and
  permission. All new and newly broadened automatic behavior has
  `speech_preserving=False`. No headline or presentation behavior is added.
- Council, unresolved Police Department, generic Commissioner/Deputy/Sergeant,
  Fiscal Year, internal City of, corporate suffixes, unsupported first-reference
  NPA voter/member/candidate uses, legal intervener and a narrow adverse-vote
  tally pattern remain findings. Their suggestions are not automatic fixes.
- NPA is second-reference style. The Pizzo first-reference example was an
  individual writer override, not a general rule. Do not automatically expand
  or insert NPA, invent third-party voters, or rewrite a quoted source's term.
- Corporate designators ordinarily disappear in narration, but legal-entity
  distinctions can require retention. This tranche flags rather than deletes.
- Title matching remains conservative name-shaped-text matching, not identity
  verification. Judicial titles, obvious nonperson names and named facilities,
  awards and programs receive explicit guards. Numeric warrant grades,
  unsupported Space Force specialist variants and surname-only military
  references remain unchanged pending stronger context or verified mappings.
- Archive usage is corroboration and a regression source, not independent
  authority. See `docs/STYLE_INTAKE_VALIDATION_2026-11-11.md` for the sample,
  observed false positives and validation limits.

## D-021 — Prove the title use, not merely the name shape

- Status: Accepted and implemented for the next release, Nov. 12, 2026.
- Authority: Drew's instruction to broaden institution/award/program research
  and avoid repeating the generic Representative failure; his supplied Staff
  Sergeant Parker Gordon Fox Suicide Prevention Grant Program example.
- Supersedes D-020's name-shaped-only eligibility for military abbreviations.
  A matched full name must have immediate, explicit service/rank context,
  such as Army, Navy, FHP or police. Retirement alone, capitalization and a
  service mentioned elsewhere do not establish the occurrence's role.
- Unqualified eligible rank words remain unchanged and produce
  `flapol.titles.military-context-required` findings. Known civilian occupations
  and supported nonperson noun phrases are preserved without being treated as
  military titles. No new people registry or inferred rank/service is added.
- A shared bounded noun-phrase guard protects supported institutional,
  award, program and other nonperson name frames across abbreviation families.
  It handles mixed case, soft line wraps, initials, suffixes and quoted
  nicknames; unresolved overlong noun phrases fail closed.
- A current lawmaker's name inside a named institution does not authorize
  title shortening, jurisdiction insertion or inference of the document's
  state/federal mode. Explicit company/union/legal/campaign representative
  roles likewise do not establish legislative title use merely because their
  names match a current lawmaker.
- All prior quotation and literal protections remain in force; this ruling
  grants no new quotation access. Main/body scope only; no release or consumer
  adoption is implied.
- See `docs/NAME_SAFETY_AUDIT_2026-11-12.md` and the public source index under
  `references/` for research, reproduced failures, tests and limitations.

## D-022 — Release the ready a10 subset; observe the remainder locally

- Status: Accepted, Nov. 12, 2026. Explicit owner release authorization.
- Authority: Drew directed publication of the additions assessed as ready,
  local testing of the others, and a two-week Newsroom Tools capture alongside
  natural Draft Room experience. Drew will seek Peter's guidance on the
  inconsistent artifact variations; absence of criticism admits no new rule.
- Decision: Release the exact D-019 titles and the ready D-020 body forms,
  named Police Department, address/spelling/no-party forms, supplied U.S. Amb.,
  NPA/corporate advisory findings and D-021 protections for existing title and
  legislative rules. See `docs/A10_SCOPE.md` for the enumerated contract.
- Activation boundary: D-020/D-021 military expansion and its rank-context
  finding, inferred police short references and the other new broad/contextual
  diagnostics are not in a10. Their existing IDs remain reserved. This later
  decision supersedes the earlier intended next-release activation, not the
  underlying preferred spellings or safety research.
- Additional local offices and Pro Tem forms remain reference-only. No new
  quote access or consumer adoption is authorized. The tested experimental
  source remains separately available locally; the release is assembled from
  the previous main baseline with the selected additions only.
- Evaluation: Newsroom Tools owns capture for Nov. 12-25, 2026 (America/New_York),
  ending Nov. 26 at midnight. Store raw copy privately; review occurrence
  context, before/after, findings, gaps and editor dispositions. Neither two
  weeks passing nor usage frequency admits a policy or proves safety.

## D-023 — Notify every current consumer on each numbered release

- Status: Accepted, Nov. 12, 2026.
- Authority: Drew explicitly required FlaPol Style project rules to inform
  consumers whenever a new numbered release is published.
- Decision: Make a refreshed consumer inventory and version-specific notice to
  every current consuming project's existing owning chat a mandatory release
  closeout step, including alpha, beta and release-candidate versions. Include
  the maintained inventory owner and separately deployed/wrapped services;
  the previous release's recipient list is not sufficient.
- Standing authority: These routine project release notices are authorized
  without asking Drew again on each release. This does not authorize a new
  communication channel, new chat, consumer source change, deployment,
  publication, credential or permission change.
- Required record: immutable tag/commit and verification, released scope and
  exclusions, caller requirements, owner adoption checks, and per-consumer
  delivery or explicit unresolved handoff. Distinguish notification,
  acknowledgment, adoption in progress and actual verified adoption.
- Consequence: A release closeout cannot silently omit a known consumer or
  equate a notice with a runtime upgrade. If tag checks are failed/unresolved,
  send an accurate status/hold notice and follow up when verified. Ordinary
  commits and local trial branches are not numbered-release triggers.
- Procedure: `runbooks/release.md`, `runbooks/downstream-handoff.md` and
  `docs/RELEASE_NOTIFICATIONS.md`.
