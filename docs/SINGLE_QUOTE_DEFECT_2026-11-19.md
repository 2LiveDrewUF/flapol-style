# Single-quotation protection defect — Nov. 19, 2026

## Classification and released reproduction

Consumer acceptance found a contract defect in immutable v0.1.0a13 at
737c3acb6e7c081c0ca752bba045492a6a06be27. Its published documentation promises
quotation protection without a double-only syntax restriction. Its parser
recognizes straight and curly double quotes, but not standalone single quotes.
The consumer's single-quoted-speech fixture is valid and must not be weakened.

Isolated installed a13 reproduces the exact synthetic case:

    She said, 'House Bill 123 and Senate bill 24.'

The output text is unchanged, but two error-severity bill findings suggest
HB 123 at original offsets [11, 25) and SB 24 at [30, 44). The double-quoted
equivalent produces neither finding. A second case, single-quoted press
conference, is automatically changed to news conference by an older ordinary
word rule. The protection-layer gap predates the new numbered-bill finding.
This report does not claim that unpublished copy was altered or that any
consumer deployed a13; the reporting consumer held deployment on a12.

## Protective fix and conservative bounds

The main-based a14 candidate adds standalone ASCII and curly single-quotation
recognition to protected-region discovery. Those spans remain hard-protected
in body, headline and presentation profiles, including when a rule has
speech_preserving=True. The new internal span kind is deliberately distinct
from the existing balanced-double-quotation rendering scope. No rule gains
quotation access, no quoted words or case are changed, and no new bill fix is
introduced. A13 and its fixtures remain immutable.

Word-internal apostrophes in contractions/names and unquoted s-possessives are
not delimiters. A bounded set of common leading elisions and abbreviated
years remains narration. Inside open single-quoted speech, an s-apostrophe
before more words can be a possessive or a quote close; the parser keeps the
span protected rather than guess. It can therefore withhold findings from
ambiguous narration. Unclosed/mismatched marks protect the uncertain remainder;
an orphan closing mark protects the uncertain prefix. This is conservative
protection, not a claim to solve every linguistic interpretation of a single
apostrophe. Delimiters inside code, URLs, email and link destinations do not
open single quotations in surrounding narration.

## Required verification and release gate

Retain the exact consumer reproduction and add independent regression cases
for curly/straight singles, contractions/possessives/elisions, nested quotes,
unbalanced/mismatched structure, literals, source offsets after prior edits,
repeat stability and profile boundaries. Run the full project verifier and
an isolated installed successor package before release consideration.

The prior explicit publication approval named a13. Publication of a14 is a
separate approval gate under runbooks/release.md; this candidate does not
authorize a tag or consumer deployment. The rollout hold remains in place.

## Completed local verification

Full scripts/verify.sh validation passed on the isolated a13-based candidate:
266 Python tests (254 released baseline plus 12 single-quote regressions),
all five pinned Vale 3.17.1 fixtures, four coverage manifests, JSON registries,
Python syntax and patch whitespace. The original a13 bill tests are unchanged.
An isolated installed a14 wheel passed 26 synthetic cases, including the
exact reported failure, older semantic word edits, allowed narration edits,
source offsets, quote/literal boundaries and profile separation.
