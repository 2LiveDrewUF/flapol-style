# Style intake audit — Nov. 11, 2026

Status: historical intake snapshot, not the current implementation ledger.
See `STYLE_INTAKE_VALIDATION_2026-11-11.md` and D-020 for the subsequent owner
clarification, admitted rules and validation. In particular, the initial NPA
inference below was superseded: first-reference NPA in the Pizzo paragraph was
a writer override; the house form is no-party voter/member, with NPA on second
reference and third- and no-party voters when both groups are discussed.

## Scope and evidence

Reviewed 26 Draft Room conversations comprising 111 turns, covering Nov. 5–11,
2026, and all 16 story-review panels in the developer's compilation of Peter's
flagged stories. Nov. 5 was included in full to avoid losing guidance around
the release boundary; a9's release commit was made at 5:14 p.m. Eastern that day.

Compared the findings with release `v0.1.0a9` at `9160b08` and the current
working branch at `346616b`. The latter additionally implements Speaker Pro
Tempore and President Pro Tempore; those changes are not in a9. Read the
registries, Vale rules, coverage records and rule-source documentation, and
exercised the main Python API with synthetic examples.

Conversation directions are distinguished below from developer interpretations
of Peter's corrections. Neither a rewrite nor a developer's implementation
claim establishes a general house rule. This report contains derived findings
and invented examples, not private transcripts or article copy.

## Candidate inventory

The proposed treatment column is an intake recommendation, not an assigned
action class. Quotation access remains ungranted for any proposed new rule.

| Candidate | Evidence | Current implementation | Proposed treatment |
| --- | --- | --- | --- |
| Capitalize President in job-title uses even away from a name | Explicit Drew direction in the Nov. 10 personnel review, including corporate positions | Before-full-name capitalization is automatic; lowercase standalone and after-name uses produce findings but remain unchanged | Strongest new general ruling. Reclassify supported unquoted job-title cases; retain the stable rule ID. The observed package already flags the examples, so any failure to surface them also requires a separate consumer check. |
| City Manager and City Attorney | Peter's local-government review corrections as compiled by the developer | Neither detected nor corrected, including before a full name | Add bounded title coverage after establishing whether the rule extends to standalone, plural and headline uses. City Manager has an explicit capitalization note; do not infer identical scope for every other office. |
| Council Member, Board Member, Commissioners, Deputies and Sergeant | Several corrected local-government stories | These forms are absent from the implemented capitalization/title mappings | Reconcile a public title inventory. Named officeholders, generic occupations, plurals and military/police ranks need separate boundaries. |
| Short governmental-body references such as Council; Police Department | Peter's review corrections | Named City Council, County Commission and certain other bodies are automatically capitalized. Generic complete forms such as city council are flagged. The one-word council example was neither corrected nor flagged | Extend detection where textual context is adequate; do not claim all local-body capitalization is missing or universally safe to fix. |
| Lowercase city in city of a municipality | Peter's City of Sanibel corrections; similar Draft Room usage | A synthetic City of Naples example remained unchanged without a finding | Candidate house-form rule with formal-name, sentence-start and quotation boundaries. |
| Fiscal Year / Fiscal Years | Listed in the Jacksonville republish corrections | No implemented correction or finding | Establish exact scope before adding a house capitalization departure, including fiscal, school and calendar-year distinctions. |
| intervenor in the legal/procedural sense | Peter's Miami correction; the developer rewrite still uses intervener | No detection or correction | Source the legal-context preference. Do not globally replace intervener, which can have other uses. |
| rescope/rescoped and preconstruction | Airport-story spelling corrections | Synthetic re-scope and pre-construction examples remained unchanged without findings | Candidates for sourced word-form records; verify the preferred forms and protect formal names and quotations. |
| Avenue to Ave. in a numbered street address | Peter's Miami correction | Synthetic 123 Main Avenue remained unchanged | Candidate contextual address rule. Preserve an unnumbered Main Avenue and any verified formal names. |
| Lieutenant Colonel to Lt. Col. before a name | Drew's Nov. 11 Veterans Day edit | The implemented abbreviation registry does not include military ranks; Lieutenant Colonel Jane Doe remained unchanged | Candidate sourced military-title subset, not a blanket abbreviation of all title uses. |
| Omit Inc. and LLC in ordinary company narration | Explicit Drew edits to the Nov. 10 PBM company lists | Neither removed nor flagged | Useful candidate guidance, but the instruction applied to particular lists. Establish general scope and exceptions for legal identification, formal names and quotations before automatic deletion. |
| NPA reference order | The Nov. 6 Top Five edit was contextual; Drew clarified the rule Nov. 11 | a9 did not implement the no-party wording or reference-order check | Superseded intake inference: NPA is second reference. The Pizzo wording was a writer override. Use no-party voter/member, ordinarily third- and no-party voters when paired. |
| Winning side first in a vote tally | Peter's Riviera Beach correction | voted 1-4 against remained unchanged without a finding | A review flag is safer until syntax proves whether digits describe a motion, rejection, roll call or another count. Never infer or change the outcome. |
| Quotation marks around yes/no votes; alphabetical ordering of yes voters | Peter's Fort Myers republish corrections | No implemented rendering or ordering | Record as candidate vote-reporting guidance. Rendering quoted vote words is distinct from rewriting speech. Sort only a known list of voters, not arbitrary names or mover/seconder descriptions. |
| Short hyperlink labels, roughly five words as a soft ceiling | Explicit Drew direction in the Nov. 11 Diagnosis review | Presentation rules bold link labels; they do not shorten labels or flag their length | Editorial guidance or an optional advisory finding. Five words is not a hard failure threshold, and shortening requires meaning and accessibility judgment. |

## Existing coverage and its limits

- Named governmental bodies already have automatic coverage in supported
  contexts: Naples city council became Naples City Council. A standalone mayor
  produced a contextual finding. This does not cover every shortened body or
  local title in the artifact.
- Governor, Agriculture Commissioner, supported before-name public titles,
  C-suite forms and several other titles already have narrow implemented rules.
  Correctly identifying an official and supplying a missing title are separate
  reporting tasks; title formatting does not verify the underlying office.
- Speaker Pro Tempore and President Pro Tempore are implemented on the current
  branch, outside quotations, but await release. A locally verified Chair Pro
  Tem is a different office and cannot be substituted with Vice Chair or
  silently folded into the legislative-title rule.
- Publication-date-aware date display and weekday-window rules already exist.
  They require an explicit publication date and appropriate date text. They do
  not infer an event's freshness, insert a missing meeting day, or decide that
  an opening should be described as today or open now.
- Acronym first-reference guidance, including decisions such as introducing
  Federal Aviation Administration before FAA, is documented in coverage but
  has no detector or automatic correction. It is not implemented coverage.
- The presentation API can bold supplied person names. It does not resolve
  speakers, discover omitted names or supply verified first-reference titles.
- The personnel-announcement workflow already records the topper's education
  exclusion, quote priorities, minimum length and paragraphing. Those are
  product instructions, not universal transformations for every article.

## Editorial findings worth retaining

Recurring Draft Room directions support these editorial checks rather than
unconditional string replacements:

- Lead with the concrete conduct or new development; avoid bureaucratic
  categories and long setup. One rejected 39-word lead is evidence for concise
  writing, not adoption of a universal numerical word limit.
- For newly released data describing an older period, establish the release or
  update date early so readers do not mistake fresh information for stale news.
- Write relative time for the scheduled publication date. Do not mechanically
  inherit a release's yesterday, tomorrow or current officeholder description.
- Avoid restating a quote immediately before giving it, repeating the same
  fact, or appending a recap that adds no reporting. A specific successful
  kicker was explicitly retained; this is not a blanket ban on kickers.
- Distinguish elected chamber leadership appointments from staff appointments.
- Use full, verified names and appropriate titles; preserve exact quotation
  wording and attribution. A transcript's apparent name is not verification.
- Vote stories need the meeting day, correct outcome, reliable roll call,
  absences or abstentions where relevant, and enough procedural context.
  Those facts cannot be manufactured by a style checker.

Top Five paragraph layout and linked titles, Sunburn section placement,
personnel-topper packaging, and variety within a cocktail trio remain
consumer/workflow concerns. They should not become default main-profile fixes.

## Artifact cautions

- The Boca Raton feedback identifies Police Department capitalization while
  retaining lowercase headquarters. The developer rewrite uses Police
  Department Headquarters. That additional capital is not established by the
  cited correction.
- The artifact includes capitalization edits inside quotations. This is
  evidence to adjudicate exact rendering rules, not permission to enable an
  entire capitalization registry inside quotations.
- Corrections such as loath versus loathe in a quote, names, dollar amounts,
  legal outcome, award status, current titles and whether people are married
  require source verification. They are not automatic house-style fixes.
- The developer's workflow requirements, including source timing and
  transcription thresholds, describe that product. They are not independently
  adopted newsroom-wide or package-wide rules.

## Suggested order for later admission

1. Apply the explicit Nov. 10 President ruling to supported unquoted job-title
   uses, with tests distinguishing findings from automatic changes.
2. Reconcile the local-office and local-body capitalization inventory against
   Peter's actual corrections and the governing guide. Resolve standalone,
   plural, headline and quotation scope explicitly.
3. Establish provenance and boundaries for address forms, military ranks and
   the three spelling candidates.
4. Apply the subsequent NPA clarification and retain corporate-suffix review
   where identity matters. Keep vote reporting and hyperlink length advisory or editorial
   unless the text proves one safe result.

No behavior, registry, coverage declaration, release version or consumer pin
was changed by this audit.
