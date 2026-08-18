# Rule sources

This file records the governing source behind automatic rules added while
salvaging product-neutral behavior from the legacy Streamlet formatter. The
legacy implementation is evidence that a rule was useful; it is not the
authority that makes the rule correct.

## Word forms

| Registry rule | Governing source |
| --- | --- |
| `advisor` to `adviser` | AP baseline and Florida Politics quote-boundary clarification, Aug. 16, 2026. |
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

## Title abbreviations

The before-name mappings implement the Florida Politics main-guide title rule
confirmed during the Aug. 16, 2026 canonical-guide review. Public titles are
abbreviated only directly before a full name. Familiar C-suite initialisms may
be used on first reference. State Attorney remains spelled out.

These rules do not implement headline choice, title capitalization away from a
name or the `Gov. DeSantis` versus `Ron DeSantis` distinction. Those questions
require document role or story meaning and are not word-level replacements.

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
