# Rule sources

This file records the governing source behind automatic rules added while
salvaging product-neutral behavior from the legacy Streamlet formatter. The
legacy implementation is evidence that a rule was useful; it is not the
authority that makes the rule correct.

## Nov. 12, 2026 title-use safety refinement

Release boundary: Drew's later Nov. 12 instruction, D-022, selects the a10
subset in `A10_SCOPE.md`. The research below describes the full local candidate;
military mappings/context findings, inferred police short references and other
held diagnostics are not implemented in a10. Additional variations in the
16-example artifact remain questions in `PETER_STYLE_QUESTIONS_2026-11-12.md`.

Drew's Nov. 12 institution/award/program audit instruction supersedes the
name-shaped-only eligibility described in the Nov. 11 military intake below.
The supplied Fox grant-program name and broader archive research demonstrate
that even full human names and known officeholder identities can occur inside
institutional names. Healthcare finance specialist is also a civilian job,
not evidence of the Army rank Specialist.

The experimental military abbreviation requires immediate explicit uniformed-service
context, plus the existing full-name and protected-region checks; its unqualified
candidates receive local review findings. A bounded, mixed-case noun-phrase guard
protects supported institutional references across title families, and
legislative inference excludes those references and explicit nonlegislative
representative roles. No name list or capitalization heuristic grants a rank.
See D-021 and `NAME_SAFETY_AUDIT_2026-11-12.md`; the archive corroborates and
stress-tests the owner's direction rather than adopting new editorial rules.

## Nov. 11, 2026 intake

Drew's Nov. 10 President ruling and Nov. 11 implementation direction establish
the body-copy title inventory and conservative action split in D-020. Peter's
review corrections and the published examples in the validation report
corroborate the forms; they do not grant additional automatic behavior.

- President and explicit compound/plural forms, City Manager, City Attorney,
  Council Member and Board Member are automatic narration capitalization.
  Commissioner and Deputy require a supported before-full-name context;
  standalone forms, Council and Fiscal Year diagnostics remain local experiments.
- A named Police Department is automatic in a10. The experimental inference
  for later definite references and its unresolved-reference findings are held
  outside the release, even if a single earlier agency is named.
- Numbered-address Avenue, Boulevard and Street use Ave., Blvd. and St.
  This is the AP addresses rule, confirmed by Drew and corroborated by the
  [VA AP-style reference](https://digital.va.gov/oit-brand-system/ap-styles/).
  Road, Drive and other street types are not shortened. Directional-name
  interpretation, mailing-label rendering and postal validation are excluded.
- Approved military forms are public factual mappings, cross-checked against
  the [MHS May 1, 2026 rank tables](https://health.mil/Reference-Center/Publications/2026/05/01/MHS-Style-Guide)
  and the [Army AP rank reference](https://api.army.mil/e2/c/downloads/293960.pdf).
  Longest titles run first. The package does not inherit unrelated MHS house
  departures or inconsistent warrant-grade deletions, guess service/grade,
  or convert administrative abbreviations such as LTC. Numeric warrant
  grades and unsupported specialist variants remain unchanged.
- U.S. Ambassador before a full name becomes U.S. Amb. as a house form.
  The source must already identify the U.S.; no nationality is inferred.
- Peter's airport-story corrections, confirmed by the Nov. 11 implementation
  direction, establish rescope/rescoped/rescopes/rescoping and preconstruction.
  [Merriam-Webster](https://www.merriam-webster.com/dictionary/preconstruction)
  lists both preconstruction and pre-construction; the unhyphenated preference
  here is the adopted house choice, not a claim that the variant is nonexistent.
  Title-cased possible formal names are preserved.
- Drew's Nov. 11 clarification supersedes the earlier NPA intake inference:
  use no-party voter/member and ordinarily third- and no-party voters when
  both groups are discussed. NPA is second-reference style. The first-reference
  Pizzo case was a writer override. The processor never automatically inserts
  or expands NPA and does not invent an unmentioned third-party group.
- Corporate designators are ordinarily omitted, but their removal can erase a
  legal distinction. Only findings are implemented in a10. Legal intervener,
  internal City of and the narrow adverse vote-tally findings remain local.

Every new automatic rule above has `speech_preserving=False`; literals and
uncertain structures remain protected. The existing President/Vice President
before-full-name quotation rendering keeps its prior rule IDs and permission.
These additions affect only the main/body pipeline. See
`STYLE_INTAKE_VALIDATION_2026-11-11.md` for evidence, tests and limitations.

## Word forms

| Registry rule | Governing source |
| --- | --- |
| `advisor` to `adviser` | AP baseline and Florida Politics quote-boundary clarification, Aug. 16, 2026. Title-cased `Advisor` is preserved because it may be part of a formal name; lowercase and all-capital forms remain automatic. |
| `health care` or `health-care` to `healthcare` | AP announced `healthcare` as one word on April 27, 2026: [AP Stylebook update](https://www.apstylebook.com/blog_posts/26) and [58th-edition announcement](https://www.ap.org/media-center/press-releases/2026/new-ap-stylebook-features-expanded-artificial-intelligence-chapter/). This later ruling supersedes the pinned 56th-edition entry. |
| `press conference` to `news conference` | The pinned 56th-edition `press conference` entry prefers `news conference`; Florida Politics owner confirmation, Aug. 16, 2026. |
| `reelection` to `re-election` | Florida Politics main-guide house departure, retained by owner in the 2026 canonical-guide review. |
| `frontrunner` to `front-runner` | Florida Politics main-guide house form, retained by owner in the 2026 canonical-guide review. |
| `long-time` to `longtime` | Pinned 56th-edition AP baseline and repeated newsroom guidance. |

The processor leaves title-cased `Health Care` unchanged because it may be part
of a verified formal name. Resolving that case requires entity information;
lowercase `health care` and sentence-initial `Health care` remain automatic.

The legacy `preempt` to `pre-empt` replacement is intentionally excluded. AP's
2024 dictionary update says prefixes including `pre-` generally do not take a
hyphen: [AP primary-dictionary announcement](https://www.ap.org/the-definitive-source/products-and-services/a-new-primary-dictionary-for-the-ap-stylebook/).

## Number signs

Florida Politics owner guidance on Oct. 2, 2026, treats a number sign followed
by digits as unsuitable in ordinary narrative copy when the surrounding text
proves the intended form. Ranking cues, Executive Orders and room numbers use
`No.`; explicitly identified Florida or ballot amendments drop the number sign.
Other numeric hash forms produce findings rather than guessed corrections.

The numeric token must end before another word character. Consequently,
`#8isEnough`, `#8_is_Enough` and similar hashtags are neither changed nor
flagged, while punctuation, a ranking hyphen, whitespace or the end of the text
can end a numeric token. All number-sign changes and findings stay out of
balanced quotations so quoted rankings, slogans and social-media hashtags are
preserved. Literal regions and malformed quotations remain hard-protected.

## Title abbreviations

The before-name mappings implement the Florida Politics main-guide title rule
confirmed during the Aug. 16, 2026 canonical-guide review. Public titles are
abbreviated only directly before a full name. Familiar C-suite initialisms may
be used on first reference. State Attorney remains spelled out.

These rules do not implement headline choice, title capitalization away from a
name or the `Gov. DeSantis` versus `Ron DeSantis` distinction. Those questions
require document role or story meaning and are not word-level replacements.

Florida Politics owner guidance on Oct. 2, 2026, establishes Florida as the
assumed home jurisdiction. When `Florida Governor` or `Florida Gov.` appears
directly before a full name in body copy, the processor removes `Florida`; the
ordinary before-name title rule then renders a spelled-out `Governor` as
`Gov.`. Other states remain identified, so `California Governor Gavin Newsom`
becomes `California Gov. Gavin Newsom`. The home-state deletion does not enter
quotations. Without a full name, `Florida Governor` or `Florida Gov.` produces
a finding rather than an automatic deletion; the formal `Florida Governor's
Mansion` is excluded. The same owner guidance makes `Governor` a capitalized
house title with or without a connected name, including inside balanced
quotations.

Florida Politics owner guidance on Oct. 2, 2026, establishes `Agriculture
Commissioner` as the capitalized house title in body copy and headlines,
including when it stands alone. The automatic rule changes `Commissioner of
Agriculture` to `Agriculture Commissioner` and normalizes that title's
capitalization. Geographic modifiers remain unchanged pending a separate,
broader title rule. It does not alter `USDA Secretary`. Ordering is an editorial
choice and does not operate inside quotations. Capitalization is explicitly
speech-preserving: inside a balanced quotation, the formatter capitalizes the
title while retaining the speaker's `Commissioner of Agriculture` or
`Agriculture Commissioner` ordering.

## Capitalization

The capitalization registry implements the Florida Politics main-guide rules
without inheriting the legacy formatter's universal case-insensitive rewrite.
Owner rulings on Aug. 16, 2026, confirmed that `Midterms` is capitalized and
added `Second Lady` to the house title forms.

Automatic changes require textual proof: an unambiguous named election stage,
the exact Florida Legislature name, a title directly before a full name, a
C-suite initialism or an explicitly named governmental body. Seasons,
standalone titles, shortened governmental bodies, The Process, VISIT FLORIDA
and POLITICO remain findings when the string alone cannot prove the intended
sense. Context-proven capitalization is speech-preserving and may render
inside balanced quotations. Contextual findings remain excluded from
quotations, and literal regions remain excluded from both changes and findings.

Drew's Nov. 11, 2026, owner ruling establishes `Speaker Pro Tempore` and
`President Pro Tempore` in the main/body profile, including standalone
references. The complete title supplies enough context for automatic
capitalization. The two rules are explicitly classified
`speech_preserving=False` and use normal quotation and literal protection.
The a9 processor already preserved supplied capitals. This ruling adds
normalization of lowercase and mixed-case versions of the two full titles.

## Presentation bolding

Florida Politics owner rulings on Aug. 18, 2026, establish body-copy bolding as
a closed presentation convention. Bold is permitted only for the first
eligible full-name reference to a real person and for the visible text of a
hyperlink. A title, office, honorific, affiliation or descriptive phrase
immediately preceding a person's name remains outside the name's bold span.

The Markdown adapter automatically bolds inline and reference-style hyperlink
labels without changing destinations. This is a representation of the semantic
rule; it does not claim direct WordPress or WYSIWYG integration. A later HTML
adapter should render the visible link label with `strong`, such as
`<a href="..."><strong>Florida Politics</strong></a>`.

The public before-name presentation registry includes full and abbreviated
forms for Governor, Lieutenant Governor, Secretary of State, U.S., state and
unqualified Representative and Senator titles, Commissioner, President and
approved C-suite titles. When one of those forms begins an otherwise
name-shaped bold span, the title is moved outside the bold markers without a
person roster.

Bold officeholder-group language using `commissioners`, `governors`, full or
abbreviated Representative and Senator forms, and `state rep` or `state sen`
singular and plural forms is removed when it does not resolve as the approved
title-plus-name structure. This narrow negative rule does not attempt to infer
arbitrary people or descriptive phrases.

Positive first-reference person bolding uses caller-supplied, document-specific
approved names. A caller may explicitly declare that list complete for the
document; only then may the adapter remove every remaining nonlink bold span.
Without complete context, supplied people and structurally proven rules are
applied, while unresolved nonlink bold spans remain findings. Person discovery,
identity resolution, WordPress conversion and consumer adoption remain outside
the public package.

The presentation input is body-copy Markdown. A consumer may crawl a broader
article packet to discover people, but headlines and other separately governed
fields are not prepended to the body when determining its first eligible
reference.

## Public officeholder identity book

Florida Politics owner rulings on Oct. 2, 2026, establish a narrow public base
book containing only the Governor, Lieutenant Governor, Cabinet, Florida's
congressional delegation and Florida state lawmakers. This identity resource
does not itself change text or confer quotation access. Reporter- and
region-specific names remain caller-owned overlays.

The snapshot verified Oct. 2, 2026, uses these official government sources:

- [Executive Office of the Governor](https://www.flgov.com/eog/) and its
  [Lieutenant Governor profile](https://www.flgov.com/eog/leadership/people/jay-collins)
- [Florida Attorney General](https://www.myfloridalegal.com/ag-bio)
- [Florida Chief Financial Officer](https://myfloridacfo.com/about/meet-the-cfo)
- [Florida Agriculture Commissioner](https://www.fdacs.gov/About-Us/Meet-Commissioner-Simpson)
- [U.S. House directory](https://www.house.gov/representatives) and
  [U.S. Senate Florida page](https://www.senate.gov/states/FL/intro.htm)
- [Florida House roster](https://www.flhouse.gov/Representatives) and
  [Florida Senate roster](https://www.flsenate.gov/Senators)
- [Florida Division of Elections 2026 dates](https://dos.fl.gov/elections/for-voters/election-dates/)
  and [Florida Statutes §100.041](https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0100-0199/0100/Sections/0100.041.html)

Some Florida agencies use longstanding official `.com` domains. Source
admission is based on the government office controlling the site, not a
literal top-level-domain test.

The 2024-2026 legislative snapshot serves dates through Nov. 3, 2026. The
2026-2028 snapshot was checked Nov. 5, 2026, against the [Florida House
roster](https://www.flhouse.gov/Representatives) and the [2026-2028 Florida
Senate roster](https://www.flsenate.gov/Senators/2026-2028). It serves dates
from Nov. 4, 2026, through the House's listed term end, Nov. 7, 2028.
House District 33 was listed as pending election and Senate District 39
was listed as vacant in that initial snapshot. A Nov. 13 recheck of both
complete official rosters found 120 House members and 39 senators, with only
Senate District 39 vacant. The House now lists
[Daniel R. McDow for District 33](https://www.flhouse.gov/Sections/Representatives/details.aspx?LegislativeTermId=92&MemberId=5120),
with the same Nov. 4, 2026 term start. Drew's Nov. 13 instruction establishes
Dan McDow as the preferred name. Formal names and derived quoted-nickname
aliases remain identity evidence; they do not authorize rewriting the name
used in copy. The public `officeholder_name_preferences.json` record applies
only to the exact seat and official source name, so a future occupant cannot
inherit the preference merely by winning that district.
The Nov. 8, 2028, staleness gate is a backstop.
Special elections, resignations, deaths and other changes can require an
earlier refresh.

The Nov. 5, 2026, Florida Politics owner guidance omits middle initials from
primary names in the refreshed state roster. The roster preserves the
chambers' names for provenance and derives aliases with and without sourced
initials, as well as standalone and quoted forms of sourced nicknames.
These aliases supply identity evidence for the existing title rules.

The incoming U.S. House slate reflects the [Florida Division of Elections'
unofficial results](https://floridaelectionwatch.gov/FederalOffices/USRepresentative)
as checked Nov. 5, 2026. The state's [District 10 candidate
record](https://dos.elections.myflorida.com/candidates/CanDetail.asp?account=89909)
lists Maxwell Frost as unopposed. Districts 7, 9, 26 and 27 are marked
provisional for a certification check. The [current House
directory](https://www.house.gov/representatives) supplies the sitting
roster, including its District 20 vacancy. The [Twentieth
Amendment](https://constitution.congress.gov/static/files/Literal_Print_of_Constitution_MCT_1.9.26.pdf)
sets the new House term at noon Jan. 3, 2027. Representatives take the
oath when the [House organizes](https://history.house.gov/Institution/Origins-Development/Oath-of-Office/).

The incoming executive entries use the [Florida Division of Elections'
state offices results](https://floridaelectionwatch.gov/StateOffices/) checked
Nov. 5, 2026. Article IV, section 5 of the [Florida
Constitution](https://www.flsenate.gov/Laws/Constitution) sets the next
executive term start on Jan. 5, 2027.

## State and federal legislator titles

Florida Politics owner rulings from Sept. 29-Oct. 2, 2026, establish a
document-level convention backed by the dated officeholder book. A document
that invokes only Florida state lawmakers uses `Rep.`, `Sen.`, `Reps.` and
`Sens.`. A document that invokes only members of Congress adds `U.S.`. A mixed
document uses `U.S. Rep.` or `U.S. Sen.` for federal lawmakers and lowercase
`state Rep.` or `state Sen.` for state lawmakers. Edited narration does not use
`Florida Rep.` or `Florida Sen.`.

The implementation requires an explicit officeholder as-of date and resolves
identity from the public base plus caller overlays. Unknown identities,
mixed-level plural lists, former or historical offices and mixed-document
standalone attributions become findings instead of guesses. Unqualified
`Representative`, `Representatives`, `Senator` and `Senators` are no longer
abbreviated from name-shaped text alone. Inside balanced direct quotations,
spoken jurisdiction words remain unchanged; an identity-proven,
speech-preserving rule may abbreviate the long title only. Stale required
roster data stops the identity-dependent family.

The full formal phrase `Commissioner of Agriculture and Consumer Services` is
outside the shorter Agriculture Commissioner ordering rule. The package
preserves that phrase instead of producing the malformed hybrid `Agriculture
Commissioner and Consumer Services`.

## FP+ second review: reference-only observations

The Nov. 12, 2026, second review of all 16 examples in the FP+ Story Engine
developer artifact adds reference-only observations and a proposed title
inventory, recorded in `A10_READINESS_2026-11-12.md`. It does not admit new
capitalization rules from uncriticized text. Official local-government and
legislative sources support retaining a verified Pro Tem office form; any
additional house capitalization scope still requires adoption.

## Date capitalization

Florida Politics owner guidance on Oct. 2, 2026, makes lowercase or otherwise
mis-cased month names automatic when a following day or year proves date
context. The main profile then applies its existing AP date-display rules, so
`september 30th, 2026` becomes `Sept. 30, 2026`. The headline profile restores
the proper month capitalization after sentence-casing without importing the
rest of the main profile. Month homographs without date context, such as the
verbs in `workers may march`, remain untouched. This capitalization is
speech-preserving inside balanced quotations; literals and malformed quotation
structure remain protected.

## Existing Vale families promoted to protected auto-fix

| Rule | Governing source |
| --- | --- |
| `COVID-19` to `COVID` | Florida Politics main guide and the existing `FlaPol/Covid.yml` fixture. |
| Numeral plus `percent` or `per cent` to `%` | Pinned 56th-edition AP percent entry and the existing `FlaPol/PercentSymbol.yml` fixture. Percentage points remain a separate semantic rule. |
| Meridiem formatting | Pinned 56th-edition AP times entry and the existing `FlaPol/AMPM.yml` fixture. The automatic rule accepts valid 1–12-hour forms and does not legitimize invalid clock values. |
| Spoken number plus `percent` to numeral plus `%` | Florida Politics quote-boundary clarification, Aug. 16, 2026, applying the AP numeral-plus-percent form to deterministic transcript rendering. Supported word numbers are zero through 999. |
| Spoken one-through-twelve hour plus meridiem to numeral and punctuated meridiem | Florida Politics quote-boundary clarification, Aug. 16, 2026, applying the AP time form to deterministic transcript rendering. |
| Headline `US` to `U.S.` | Florida Politics headline departure recorded in main and the existing `FlaPol/USHeadline.yml` fixture. It runs only through the explicit headline API. |
| Headline sentence case | Florida Politics owner ruling, 2026-08-16. Imported title-case headlines are decapitalized through the explicit headline API, with protected text and proper nouns preserved. |
| Body-copy `US` to `U.S.` | AP baseline and Florida Politics main-guide usage, confirmed for the protected main processor on Aug. 16, 2026. |
| `Chairman` or `Chairwoman` to `Chair` | Florida Politics main-guide gender-neutral title form, confirmed for the protected main processor on Aug. 16, 2026. |
