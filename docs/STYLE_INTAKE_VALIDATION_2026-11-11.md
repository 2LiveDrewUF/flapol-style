# Nov. 11 style intake: implementation and validation

This report records the implemented subset of the intake audit, under D-020.
The release version remains a9 until a separately verified release. These
changes are local, unreleased main/body behavior; consumer adoption is separate.

## Published-copy evidence

Searched the Florida Politics archive with 22 queries and retrieved 16 complete
article bodies. Queries covered the four explicit local offices, Police
Department, President/Vice President, military forms, U.S. Amb., voter wording,
corporate suffixes, intervenor, preconstruction, rescope, Fiscal Year, City of,
addresses and adverse vote-tally wording. This is a targeted sample, not a
frequency estimate or an exhaustive archive scan. Native keyword matches were
confirmed against bodies; some search hits were substring matches or quotes.

| Topic | Confirmed published example | Evidence and action |
| --- | --- | --- |
| Local titles and Police Department | [Doral recount, Nov. 9](https://floridapolitics.com/archives/831707-maureen-porras-secures-doral-council-re-election-after-razor-thin-recount/) | Uses Doral Police Department, City Manager, Council Member and School Board Member. Mixed Council member casing also demonstrates drift. Explicit office phrases and named agencies are automatic. |
| City Attorney; President after a name or role | [Fort Myers Estates, Nov. 4](https://floridapolitics.com/archives/829697-fort-myers-commits-1-9m-to-edison-and-ford-winter-estates-welcome-center/) | Uses City Attorney, City Manager, President and CEO, Council Member, yes/no vote marks and Council. Council alone remains a finding. |
| Military rank before a name | [St. Petersburg veterans ceremony](https://floridapolitics.com/archives/829944-st-petersburg-to-honor-2-vietnam-war-veterans-at-veterans-day-ceremony/) | Uses retired Army Lt. Col. before a full name. The new mapping uses the approved form, not an administrative initialism. |
| U.S. Amb. | [Lobbying compensation](https://floridapolitics.com/archives/767812-lobbying-compensation-top-15-firms-clear-1m-plus-in-q3/) | Uses U.S. Amb. Carlos Trujillo. Only a supplied U.S. qualifier is preserved and abbreviated. |
| Third- and no-party voters | [CD 27 recount, Nov. 10](https://floridapolitics.com/archives/831866-maria-elvira-salazar-wins-tight-cd-27-race-after-recount/) | The paired house form appears in narration. No automatic NPA insertion or expansion is implemented. |
| NPA and no-party-affiliation in speech | [MacManus turnout analysis](https://floridapolitics.com/archives/826875-susan-macmanus-sees-working-class-voters-continuing-to-change-floridas-landscape/) | The source uses both terms inside a quotation. That quoted speech is preserved; it is not evidence for automatically imposing either form throughout narration. |
| Board Member; numbered address; intervenor | [Miami preservation board, Nov. 4](https://floridapolitics.com/archives/829636-miami-preservation-board-shrinks-first-presbyterian-churchs-historic-boundary-over-icon-brickell-objections/) | Uses 609 Brickell Ave., Board Member and legal intervenor. Address rendering and explicit offices are automatic; legal spelling remains a contextual finding. |
| Rescope and preconstruction | [Pinellas airport, Nov. 4](https://floridapolitics.com/archives/829721-pinellas-county-oks-contracts-for-145m-airport-terminal-project-after-estimate-topped-220m/) | Uses rescoped, rescope and preconstruction in narration. New word-form changes preserve title-cased possible names and all protected quotations. |
| city of | [Sanibel housing award, Nov. 4](https://floridapolitics.com/archives/829645-lee-county-keeps-sanibel-affordable-housing-award-alive-delays-decision-30-days-for-talks-with-city/) | Repeated lowercase city of in narration supports the intended form. Possible formal-name uses of City of are flagged, not silently changed. |
| Fiscal Year | [Tampa road projects, Nov. 11](https://floridapolitics.com/archives/832265-amendment-3-puts-tampas-future-road-projects-and-spending-plans-in-question/) | Numbered Fiscal Year references coexist with generic lowercase fiscal year. This supports review rather than a universal replacement. |
| Corporate identity exception | [Miami Seaquarium, Nov. 10](https://floridapolitics.com/archives/832021-committee-deferral-leaves-miami-seaquarium-redevelopment-plan-treading-water-as-deal-deadline-nears/) | An LLC identifies the proposed lease affiliate. The suffix is retained with a review finding, never automatically deleted. |
| President and rank-like formal names | [Tampa General veterans, Nov. 11](https://floridapolitics.com/archives/832014-danny-burgess-tells-tampa-generals-veterans-to-stay-the-tip-of-the-spear/) and [Citrus veterans, Nov. 11](https://floridapolitics.com/archives/832023-jay-collins-helps-citrus-county-unveil-veterans-wall-of-fame/) | Confirm President usage while exposing named-program and unnamed-rank boundaries. |

The exact voted 1-4 search returned no results; this does not establish absence.
The adverse-vote finding derives from the supplied review correction, not that
empty search. Hyperlink word counts cannot be measured from the archive's
plain-text bodies; the soft length preference remains editorial guidance.
Alphabetical voter ordering and automatic quotation marks around vote words
also remain editorial, pending a separately bounded implementation.

## Validation and discovered limitations

- Full regression suite: 226 tests, including 17 new test methods with positive,
  negative and adversarial subcases. Cases cover straight/curly quotations,
  malformed quotes and fences, code, URLs, email, link destinations, plurals,
  possessives, -elect titles, accented/hyphenated names, source offsets,
  idempotence and main/headline separation.
- A real-copy replay compares the 16 complete bodies with the pre-intake
  `346616b` implementation. New edits are checked for source coordinates,
  quotation/literal exclusion and idempotence. Working source bodies and replay
  output remain in the ignored build directory; no article corpus is committed.
  The completed replay produced 13 new capitalization edits across five
  articles, plus four internal City of and one corporate-designator usage
  findings. Existing supported spellings and abbreviations remain unchanged.
- The replay exposed two unsafe initial military matches: General Magistrate
  in the Doral article and the named Major John Leroy Haynes program in the
  veterans article. Both are now guarded and represented by regression cases.
- Synthetic tests exposed doubled address periods, a false company match for
  An LLC, formal-name capitalization in Pre-Construction and overlapping
  paired-voter edits. All were corrected and retained as regression cases.
- Military matching still requires full name-shaped text. It is not an identity
  resolver, does not abbreviate surname-only references or standalone ranks,
  and conservatively withholds apparent facility/program names. Administrative
  initials, numeric warrant variants and unsupported Space Force specialist
  variants remain unchanged. The current MHS tables contain conflicting
  warrant-grade treatments; this package does not inherit those deletions.
- Address changes cover numbered, same-line, name-shaped street addresses and
  only Avenue/Boulevard/Street. They do not validate postal deliverability,
  interpret directional street names, rewrite Road/Drive, or guess incomplete
  address ranges. Original sentence-ending periods are not duplicated.
- Police Department references require one unquoted named agency earlier in
  the document and a supported definite-reference predicate. Generic uses,
  multiple agencies and uncertain references remain findings.
- NPA first-reference detection is intentionally limited to explicit NPA
  voter/member/candidate phrases lacking an earlier unquoted no-party
  voter/member antecedent. Other acronym meanings and bare statistical NPA
  labels are not automatically rewritten or universally resolved.
- Corporate findings recognize common name-shaped Inc./LLC/L.L.C. suffixes.
  They do not resolve legal identity or delete names. A finding's explanatory
  suggestion must never be applied as replacement text.

## Local verification boundary

The required Bash verifier was run. A temporary shell function routed python3
to the installed Python without changing system settings. Its regression and
syntax stages passed; it stopped at the missing jq executable. Ruby and Vale
are also absent locally. JSON and coverage-schema checks were run separately
with Python, followed by package build/installed-package smoke checks and
patch-whitespace checks. This does not constitute a full successful Bash/Vale
run or minimum-Python CI run. Branch/tag CI remains required before release.
