# Title-use and named-entity safety audit — Nov. 12, 2026

## Outcome

D-021 replaces the unreleased military rule's name-shaped-only eligibility
with immediate uniformed-service context plus full-name and noun-phrase checks.
Unqualified rank-like matches are preserved with a review finding. Known
civilian occupations and supported nonperson phrases are not treated as ranks.

The shared noun-phrase guard also protects supported formal names across other
abbreviation families. Legislative rules preserve institutional references even
when the embedded human name is in the current officeholder roster, and those
references do not establish the document's legislative jurisdiction. Explicit
civilian representative roles are likewise excluded from title inference.

This is an applicability correction, not a change to the accepted abbreviation
when a military or legislative title actually identifies a person. No new
quotation access, caller parameters, identity registry or consumer changes are
introduced. The release remains a9; this work is local and unreleased.

## Research and reproduced failures

Ran 28 archive queries and retrieved 40 complete public bodies, totaling 471,857
characters. Queries span institutes, awards, medals, programs, museums,
academies, memorials, foundations, funds, committees, businesses, civilian
occupations and rank-word policy terms. The sample includes standalone stories
and newsletters. Results were deduplicated and read; keyword co-occurrence alone
was not treated as evidence of an institutional name.

The public source index is
`references/name-safety-sources-2026-11-12.json`. Raw bodies and executable
replay evidence remain under ignored `build/name-safety/`, outside Git. This is
a broad targeted sample, not an exhaustive institutional-name census or a claim
of zero possible future false positives.

| Published or supplied reference | Prior behavior | Current behavior |
| --- | --- | --- |
| Staff Sergeant Parker Gordon Fox Suicide Prevention Grant Program; supplied by Drew and confirmed in [Delegation for Oct. 6](https://floridapolitics.com/archives/823480-delegation-for-10-6-26-battleground-offshore-drilling-college-sports-ai-guardrails-pipelines/) | The title-cased published form was already preserved, but a lowercase program suffix or soft line wrap could cause Staff Sgt. inside the program name | Preserve the complete name and tested mixed-case/wrapped variants, including Drew's VA prefix |
| Admiral Farragut Academy in [Bowens endorsements](https://floridapolitics.com/archives/661671-donald-bowens-lands-all-star-endorsements-in-st-pete-city-council-bid/) and [school tuition comparison](https://floridapolitics.com/archives/613508-lutheran-church-of-the-cross-day-school-says-goodbye-to-holly-carlson/) | Two incorrect Adm. changes | Preserve the academy's name |
| Healthcare finance/financial specialist Tosha Chambers in [Broward election results](https://floridapolitics.com/archives/830023-from-coconut-creek-to-wilton-manors-heres-how-browards-municipal-elections-shook-out/) and [municipal election preview](https://floridapolitics.com/archives/823352-browards-municipal-elections-whos-running-and-whats-at-stake/) | Two incorrect Spc. changes to a civilian occupation | Preserve the occupation and name without a military finding |
| General Obligation Bonds Oversight Committee in [Miami-Dade election results](https://floridapolitics.com/archives/829621-from-aventura-to-virginia-gardens-here-are-miami-dades-municipal-election-results/) | Incorrect Gen. change | Preserve the committee name |
| Major Disaster Declaration in [Delegation for Nov. 10](https://floridapolitics.com/archives/831878-delegation-for-11-10-26-fresh-faces-no-days-off-fema-billions-space-race-star-power/) | Incorrect Maj. change | Preserve the non-rank phrase |
| FHP Colonel Gary Howze in [Takeaways — Canopy community](https://floridapolitics.com/archives/830061-takeaways-from-tallahassee-canopy-community/) | Col. | Retain this supported shortening: an immediate uniformed-service qualifier exists |
| Unqualified Commander reference in [South Florida commentary](https://floridapolitics.com/archives/832174-diego-hernandez-moreno-florida-democrats-must-stop-ignoring-south-florida/) | Automatically shortened | Preserve for review because this occurrence supplies no immediate service qualifier; the audit does not adjudicate the person's biography |

The replay compared the prior `698a4e2` implementation against the new one:
eight former rank edits became one supported automatic rank edit and one
context-review finding. Six incorrect edits across six articles were blocked;
one additional article changed because its unqualified title was deferred.
Protected regions, original coordinates and idempotence were checked.

## Generalized tests beyond the published examples

The full suite now contains 238 test methods, with positive and adversarial
subcases. The new cases cover:

- Invented names across academy, institute, award, medal, program, scholarship,
  foundation, fund, commission, museum and association frames, rather than an
  allowlist of the particular names found in the archive.
- Mixed case, plurals, initials, suffix punctuation, bold names, quoted
  nicknames, soft line wraps and long unresolved noun phrases.
- The same named person as an explicit service member versus an institutional
  namesake; the institutional frame takes priority over a nearby service cue.
- Immediate Army/Navy/FHP/police context versus a service elsewhere in the
  document, a separate paragraph or retirement without a named service.
- Actual people who speak about programs, so a later program mention does not
  automatically protect the preceding personal title.
- Synthetic institutions named after registered lawmakers, including a joint
  scholarship. These are invented regression scenarios, not claims that those
  institutions exist. They test title preservation, quote preservation and
  exclusion from state/federal document-mode inference.
- Known lawmaker names used as company, union, legal, campaign or applicant
  representatives, including qualified/bold and plural references.
- Source coordinates after earlier shortening, repeated application, straight
  and curly quotes, malformed quotes/fences, literals and link destinations.

## Limits and verification

This remains a conservative structural check, not an entity or identity
resolver. The noun-phrase guard is bounded and fails closed on an unresolved
overlong phrase. It can withhold a legitimate abbreviation. Unknown formal
names and unusual punctuation still need editorial judgment. An unqualified
rank finding does not instruct a writer to insert service wording simply to
make the checker pass; an editor may establish the role and apply the correct
form manually. No exhaustive institution-name registry is claimed.

Local checks include the complete Python regression suite, JSON/coverage
validation, syntax and whitespace checks, the 40-body replay and a built-package
installation smoke test. The required Bash verifier is run with an explicit
Python route. Its initial run stopped at missing jq, with Ruby and Vale also
absent. Later on Nov. 12, the checksum-pinned project-local Windows runner
resolved those prerequisites: the full Bash verifier passed, including all
238 tests, Ruby coverage checks and five Vale fixtures. See
`WINDOWS_VERIFICATION.md`. Branch/tag CI and minimum-supported Python
verification remain separate release requirements.
