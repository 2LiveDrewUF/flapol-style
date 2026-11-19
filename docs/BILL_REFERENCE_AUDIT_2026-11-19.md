# Numbered bill-reference audit — Nov. 19, 2026

## Scope and result

Drew asked whether established Florida Politics writers already use HB/SB on
first reference and preserve spoken House bill/Senate bill forms in quotations.
This is a bounded corroboration sample, not a random sample or a claim of
perfect newsroom compliance. Drew's Nov. 19 ruling, rather than publication
frequency, supplies the authority for the rule.

The archive returned complete public article bodies and printed bylines for
13 eligible articles from March 2024 through May 2025, by six established
writers. All 13 use HB/SB for the first numbered reference in the body.
Across those bodies, 46 numbered references use HB/SB in narration.
Three numbered expanded forms occur, all inside direct quotations; none occur
in narration. A 14th inspected article, fp:739652 by Jacob Ogles, contains no
matching numbered reference and is excluded from those counts.

No Fabrizio articles were selected. The audited bylines are Jesse Scheckner,
A.G. Gancarski, Christine Jordan Sexton, Janelle Irwin Taylor, Jacob Ogles and
Peter Schorsch. The sample does not include a Drew Wilson byline.

## Method and limits

Used the connected Florida Politics archive's search_archive and read_article
tools on Nov. 19, 2026. Searches included HB for March 1–15, 2025; SB for
March 1–8, 2024; and the phrases House Bill and Senate Bill for March–May
2025. Selected relevant straight-news articles, confirmed their printed
bylines, and inspected complete bodies rather than search snippets.

Counted case-sensitive HB/SB and House/Senate followed by Bill/bill and an
immediately following one- to four-digit number. Reviewed the expanded
occurrences in their quotation context. First reference means the first
numbered bill reference in the retrieved body, not headline or linked page.
These are observed examples, not an exhaustive error-rate estimate.
WordPress keyword search is not an author filter and exposes no authoritative
total, so search result totals are not used as compliance counts.

One additional legacy construction in fp:664214 says Senate Bill (SB 408).
That does not have digits immediately after Bill and is outside this narrow
rule. Its existence is a reason not to describe the sample as perfectly
consistent in every possible construction.

## Article inventory

| Article | Published | Printed byline | First numbered reference | HB/SB occurrences | Expanded numbered occurrences |
| --- | --- | --- | --- | ---: | ---: |
| [fp:726229](https://floridapolitics.com/archives/726229-mike-giallombardos-cra-killing-bill-advances-but-even-some-supporters-disagree-with-its-aim/) | 2025-03-13 | Jesse Scheckner | HB 991 | 15 | 0 |
| [fp:726144](https://floridapolitics.com/archives/726144-bill-easing-professional-licensing-of-ex-inmates-heads-to-house-floor/) | 2025-03-13 | Jesse Scheckner | HB 195 | 4 | 0 |
| [fp:726100](https://floridapolitics.com/archives/726100-porras-gulf/) | 2025-03-13 | A.G. Gancarski | HB 549 | 4 | 0 |
| [fp:726103](https://floridapolitics.com/archives/726103-andrades-presidential-library-bill/) | 2025-03-13 | A.G. Gancarski | HB 69 | 2 | 0 |
| [fp:664362](https://floridapolitics.com/archives/664362-eyeball-wars-likely-to-continue/) | 2024-03-08 | Christine Jordan Sexton | SB 1112 | 1 | 0 |
| [fp:664295](https://floridapolitics.com/archives/664295-legislature-again-snubs-ban-on-no-cash-businesses/) | 2024-03-08 | Jesse Scheckner | SB 106 | 3 | 0 |
| [fp:664259](https://floridapolitics.com/archives/664259-legislature-raises-minimum-age-for-strippers-to-21/) | 2024-03-08 | A.G. Gancarski | SB 796 | 2 | 0 |
| [fp:664214](https://floridapolitics.com/archives/664214-legislature-oks-new-veterans-history-program-expanded-benefits/) | 2024-03-08 | Janelle Irwin Taylor | HB 1329 | 2 | 0 |
| [fp:664134](https://floridapolitics.com/archives/664134-senate-passes-health-care-transparency-bill-as-end-of-2024-session-draws-near/) | 2024-03-07 | Christine Jordan Sexton | HB 7089 | 7 | 0 |
| [fp:739766](https://floridapolitics.com/archives/739766-animal-abuse-registry-now-up-to-ron-desantis/) | 2025-05-28 | A.G. Gancarski | HB 255 | 1 | 0 |
| [fp:738610](https://floridapolitics.com/archives/738610-bill-that-would-send-people-attacking-utility-workers-to-prison-heads-to-governor/) | 2025-05-23 | A.G. Gancarski | SB 1386 | 2 | 2 |
| [fp:735880](https://floridapolitics.com/archives/735880-zoning-bill-ready-for-governors-desk-after-impact-fee-haggling-between-senate-and-house/) | 2025-05-01 | Jacob Ogles | SB 1080 | 1 | 1 |
| [fp:739455](https://floridapolitics.com/archives/739455-lawmakers-failed-to-pass-a-legal-aid-funding-update-now-its-being-used-against-their-interests/) | 2025-05-27 | Peter Schorsch | HB 173 | 2 | 0 |

In fp:738610, the two expanded forms reproduce a utility association's quoted
statement after narration has already used SB/HB. In fp:735880, the expanded
form occurs in Darryl Rouson's quoted remarks after narration uses SB.
In fp:739455, generic House bill prose follows abbreviated numbered references;
it must remain available as ordinary narration.

## Accepted bounded implementation

- Stable ID: flapol.usage.numbered-bill-abbreviation.
- Profile: main/body. Headline and presentation behavior are not changed.
- Action: FLAG, severity error, suggesting HB N or SB N; no automatic edit.
- Match the exact chamber words House/Senate followed by Bill or bill,
  horizontal whitespace and a complete one- to four-digit ASCII number.
- Preserve generic House bill/Senate bill prose without a following number,
  existing HB/SB, plural labels and unsupported numeric constructions.
- Quotation classification: speech_preserving=False. No finding or mutation
  inside balanced direct quotations; preserve the supplied case of bill.
  Quoted-case policy remains unresolved. Malformed quotations and literals
  fail closed under the existing protection engine.
- Code, URLs, email addresses and link destinations remain hard-protected.
  Visible link labels remain reviewable.
- Findings retain found text, suggested form, authority and original offsets.
- The initial local implementation is now prepared for the focused a13
  release. Release and adoption status are recorded separately from this
  audit. Automatic shortening, quote capitalization and linking are excluded.

## Local validation

The six new tests cover both chambers, Bill/bill, one- through four-digit
numbers, generic prose, unsupported numeric forms, straight/curly and malformed
quotes, code, URLs, email, link labels/destinations, original-source coordinates
after earlier edits, repeated findings and body-only profile scope.

The complete scripts/verify.sh run through the project-local Windows runner
passed Nov. 19: 256 Python tests, syntax, JSON registries, four coverage
manifests, patch whitespace and all five pinned Vale 3.17.1 fixtures.
No Vale detector is added: this finding uses the shared Python quotation
protection rather than a surface match that would also alert inside quotes.
Branch/tag CI and installed minimum-Python package validation remain the
release workflow's responsibility. Nothing was published or deployed.

## Focused a13 release validation

The release candidate is based on main/a12 rather than the local trial branch.
It adds only the numbered-bill finding, its tests, provenance and a13 metadata.
Full local verification passed with 254 tests (248 baseline plus six new bill
tests), all five Vale 3.17.1 fixtures, four coverage manifests, JSON registries,
syntax and whitespace checks. The trial branch's 256-test count above includes
held work and is not the release test count.

An isolated installed a13 wheel also passed 31 synthetic checks covering
numbered references, generic/existing forms, quotations and malformed quotes,
literals, original offsets after earlier edits, and headline/presentation
separation. No consumer environment was changed by these checks.
