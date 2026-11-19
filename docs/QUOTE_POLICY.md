# Direct-quotation rendering policy

Florida Politics preserves what a speaker said, not necessarily the exact
characters selected by a transcription engine.

Direct quotations remain unavailable to generative, semantic and ordinary
copy-editing rules. The formatter must not paraphrase, repair grammar, remove
repetitions or hedges, change emphasis or tone, alter factual content, or make
a contextual editorial judgment inside quoted speech.

The a14 protection fix recognizes standalone straight single quotes and curly
single quotation marks as well as the existing double-quote forms. Single
quotations are hard-protected, including from rules with existing
`speech_preserving=True` grants: recognizing a delimiter does not grant a rule
new in-quote rendering authority. Ordinary word-internal apostrophes,
unquoted s-possessives and bounded leading elisions are not delimiters.
An ambiguous s-apostrophe inside open single-quoted speech keeps the speech
protected through a later close or the remainder. This can conservatively
withhold findings in ambiguous narration rather than expose possibly quoted
words. Mismatched and unbalanced quotation marks fail closed. Delimiters in
hard-protected literals do not open a single quotation in surrounding prose.

This corrects an implementation gap; the earlier contract did not document a
double-quotes-only limitation. See `SINGLE_QUOTE_DEFECT_2026-11-19.md`.

A deterministic rule may operate inside a balanced direct quotation only when
the rule is explicitly classified as `speech_preserving`. That classification
means both of the following are true:

1. The before and after forms represent the same spoken utterance under the
   read-aloud test.
2. The transformation is an explicit AP or Florida Politics rendering rule,
   not an inference by a language model.

The read-aloud test is necessary but not sufficient. Quote access is assigned
rule by rule and is false by default. A rule does not become speech-preserving
merely because it lives in a word-preference, capitalization, title, number or
date registry.

Permitted examples include written forms such as lowercase `advisor` to `adviser`
(title-cased `Advisor` is preserved as possible formal-name text),
`long-time` to `longtime`, `US` to `U.S.`, `8 percent` or `eight percent` to
`8%`, `4 PM` or `four PM` to `4 p.m.`, and `Governor Ron DeSantis` to
`Gov. Ron DeSantis`. A lowercase month in proven date context may be
capitalized, such as `september 30` to `September 30`. The `Agriculture
Commissioner` title is capitalized inside
quotations, but quoted `Commissioner of Agriculture` ordering is preserved.

The body sentence-opening exception for word-form percentages applies to
narration. In balanced double quotations, the existing speech-preserving
transcript rendering can still convert those percentages.

Prohibited examples include changing `I don't support the bill` to `I oppose
the bill`, removing `kind of`, or changing `We ain't doing that` to `We aren't
doing that`.

Florida Politics number-sign rules also remain outside quotations: quoted
`#1`, `#8isEnough` and other hash forms are preserved even when an unquoted
narrative form would be corrected or flagged.

Code fences, inline code, literal examples, URLs, email addresses and Markdown
link destinations remain hard-protected even when they appear inside a direct
quotation. Unbalanced or structurally uncertain quotation markup fails closed;
no rule, including a speech-preserving rule, may mutate the uncertain span.

The numbered-bill abbreviation finding likewise stays outside quotations.
House bill/Senate bill wording and the supplied Bill/bill case remain exactly
as quoted, without an HB/SB finding. The Nov. 19, 2026 ruling does not admit
quote capitalization changes; that question remains reserved for judgment.

Every permitted in-quote mutation uses the ordinary structured reporting path.
Its edit record includes the rule ID, before and after forms, original and
working locations, authority and `speech_preserving=True` classification.
