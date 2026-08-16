# Direct-quotation rendering policy

Florida Politics preserves what a speaker said, not necessarily the exact
characters selected by a transcription engine.

Direct quotations remain unavailable to generative, semantic and ordinary
copy-editing rules. The formatter must not paraphrase, repair grammar, remove
repetitions or hedges, change emphasis or tone, alter factual content, or make
a contextual editorial judgment inside quoted speech.

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

Permitted examples include written forms such as `advisor` to `adviser`,
`long-time` to `longtime`, `US` to `U.S.`, `8 percent` or `eight percent` to
`8%`, `4 PM` or `four PM` to `4 p.m.`, and `Governor Ron DeSantis` to
`Gov. Ron DeSantis`.

Prohibited examples include changing `I don't support the bill` to `I oppose
the bill`, removing `kind of`, or changing `We ain't doing that` to `We aren't
doing that`.

Code fences, inline code, literal examples, URLs, email addresses and Markdown
link destinations remain hard-protected even when they appear inside a direct
quotation. Unbalanced or structurally uncertain quotation markup fails closed;
no rule, including a speech-preserving rule, may mutate the uncertain span.

Every permitted in-quote mutation uses the ordinary structured reporting path.
Its edit record includes the rule ID, before and after forms, original and
working locations, authority and `speech_preserving=True` classification.
