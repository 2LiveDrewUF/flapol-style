"""Protected-region discovery for deterministic editing.

Protection is deliberately conservative. Balanced direct quotations are a
separate policy boundary: ordinary rules cannot edit them, while explicitly
speech-preserving deterministic rules may. When a quotation or code fence is
unbalanced, the uncertain remainder remains hard-protected for every rule.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Callable, Iterable


@dataclass(frozen=True, order=True)
class ProtectedSpan:
    start: int
    end: int
    kind: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid protected span")


_INLINE_CODE_RE = re.compile(r"(`+)([^\n]*?)\1")
_LINK_DEST_RE = re.compile(r"\](\((?:[^()\\\n]|\\.|\([^()\n]*\))*\))")
_AUTOLINK_RE = re.compile(r"<(?:(?:https?|mailto):[^>\n]+)>", re.IGNORECASE)
_URL_RE = re.compile(r"https?://[^\s<>\]\[\"'“”‘’]+", re.IGNORECASE)
_EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",
    re.IGNORECASE,
)


def _fenced_code_spans(text: str) -> list[ProtectedSpan]:
    spans: list[ProtectedSpan] = []
    opener = re.compile(r"(?m)^[ \t]{0,3}(`{3,}|~{3,})[^\n]*(?:\n|$)")
    cursor = 0
    while True:
        match = opener.search(text, cursor)
        if not match:
            break
        marker = match.group(1)
        closer = re.compile(
            rf"(?m)^[ \t]{{0,3}}{re.escape(marker[0])}{{{len(marker)},}}[ \t]*(?:\n|$)"
        )
        close = closer.search(text, match.end())
        end = close.end() if close else len(text)
        spans.append(ProtectedSpan(match.start(), end, "fenced_code"))
        if not close:
            break
        cursor = end
    return spans


def _quote_spans(text: str) -> list[ProtectedSpan]:
    spans: list[ProtectedSpan] = []

    cursor = 0
    while True:
        start = text.find("“", cursor)
        if start < 0:
            break
        close = text.find("”", start + 1)
        end = close + 1 if close >= 0 else len(text)
        kind = "direct_quotation" if close >= 0 else "uncertain_quotation"
        spans.append(ProtectedSpan(start, end, kind))
        if close < 0:
            break
        cursor = end

    straight = [m.start() for m in re.finditer(r'(?<!\\)"', text)]
    for index in range(0, len(straight), 2):
        start = straight[index]
        balanced = index + 1 < len(straight)
        end = straight[index + 1] + 1 if balanced else len(text)
        kind = "direct_quotation" if balanced else "uncertain_quotation"
        spans.append(ProtectedSpan(start, end, kind))

    # A closing curly quote without a preceding opening mark makes the
    # preceding text structurally uncertain. Fail closed through that mark.
    covered_closers = {
        span.end - 1
        for span in spans
        if span.kind == "direct_quotation" and text[span.end - 1:span.end] == "”"
    }
    for close in (m.start() for m in re.finditer("”", text)):
        if close not in covered_closers:
            spans.append(ProtectedSpan(0, close + 1, "uncertain_quotation"))

    return spans


_LEADING_ELISION_RE = re.compile(
    r"['’](?:[0-9]{2}s?|n['’]?|cause|cos|em|round|til|tis|twas|twere|"
    r"bout|cept|scuse|tween)(?!\w)",
    re.IGNORECASE,
)


def _single_quote_spans(
    text: str, literal_spans: Iterable[ProtectedSpan]
) -> list[ProtectedSpan]:
    """Hard-protect single quotes without granting new rendering access.

    Apostrophes within words, unquoted s-possessives and bounded leading
    elisions are not quotation delimiters. An s-apostrophe within open speech
    is ambiguous: keep the quote open rather than expose possibly quoted words.
    """
    literals = tuple(literal_spans)
    spans: list[ProtectedSpan] = []
    stack: list[tuple[int, str]] = []
    elision_end = 0

    def word(character: str) -> bool:
        return character.isalnum() or character == "_"

    for match in re.finditer("['‘’]", text):
        index = match.start()
        if index < elision_end or (index and text[index - 1] == "\\"):
            continue
        if any(span.start <= index < span.end for span in literals):
            continue
        mark = match.group()
        before = text[index - 1] if index else ""
        after = text[index + 1] if index + 1 < len(text) else ""
        if word(before) and word(after):
            continue
        if not word(before):
            elision = _LEADING_ELISION_RE.match(text, index)
            if elision:
                elision_end = elision.end()
                continue
        if before in {"s", "S"} and not word(after):
            if not stack or (after.isspace() and text[index + 1:].lstrip()
                             and word(text[index + 1:].lstrip()[0])):
                continue

        opens = mark == "‘" or (mark == "'" and word(after) and not word(before))
        if opens:
            stack.append((index, "’" if mark == "‘" else "'"))
        elif stack:
            start, expected = stack[-1]
            if mark != expected:
                spans.append(ProtectedSpan(stack[0][0], len(text), "uncertain_quotation"))
                return spans
            stack.pop()
            # This kind is deliberately NOT direct_quotation: existing
            # speech-preserving grants must not acquire single-quote access.
            spans.append(ProtectedSpan(start, index + 1, "single_quotation"))
        elif word(after) and not word(before):
            spans.append(ProtectedSpan(index, len(text), "uncertain_quotation"))
            return spans
        else:
            spans.append(ProtectedSpan(0, index + 1, "uncertain_quotation"))

    if stack:
        spans.append(ProtectedSpan(stack[0][0], len(text), "uncertain_quotation"))
    return spans


def _regex_spans(
    text: str, pattern: re.Pattern[str], kind: str, group: int = 0
) -> list[ProtectedSpan]:
    return [ProtectedSpan(m.start(group), m.end(group), kind) for m in pattern.finditer(text)]


def _merge_spans(spans: Iterable[ProtectedSpan]) -> list[ProtectedSpan]:
    ordered = sorted(
        (span for span in spans if span.end > span.start),
        key=lambda span: (span.start, span.end),
    )
    if not ordered:
        return []

    merged: list[ProtectedSpan] = [ordered[0]]
    for span in ordered[1:]:
        previous = merged[-1]
        if span.start <= previous.end:
            kinds = sorted(set(previous.kind.split("+") + span.kind.split("+")))
            merged[-1] = ProtectedSpan(
                previous.start,
                max(previous.end, span.end),
                "+".join(kinds),
            )
        else:
            merged.append(span)
    return merged


def find_protected_spans(
    text: str,
    *,
    allow_balanced_quotations: bool = False,
) -> list[ProtectedSpan]:
    """Return spans protected from the requested transformation class.

    ``allow_balanced_quotations`` removes only balanced double quotations from
    the protected set. Single quotations, literal regions and structurally
    uncertain quotations remain protected; this adds no rendering authority.
    """
    if not text:
        return []

    spans: list[ProtectedSpan] = []
    spans.extend(_fenced_code_spans(text))
    spans.extend(_regex_spans(text, _INLINE_CODE_RE, "inline_code"))
    spans.extend(
        _regex_spans(text, _LINK_DEST_RE, "markdown_link_destination", group=1)
    )
    spans.extend(_regex_spans(text, _AUTOLINK_RE, "autolink"))
    spans.extend(_regex_spans(text, _URL_RE, "url"))
    spans.extend(_regex_spans(text, _EMAIL_RE, "email_address"))
    spans.extend(_single_quote_spans(text, spans))
    quote_spans = _quote_spans(text)
    if allow_balanced_quotations:
        quote_spans = [
            span for span in quote_spans if span.kind != "direct_quotation"
        ]
    spans.extend(quote_spans)
    return _merge_spans(spans)


def transform_unprotected(text: str, transform: Callable[[str], str]) -> str:
    """Apply ``transform`` only to unprotected slices of ``text``."""
    spans = find_protected_spans(text)
    if not spans:
        return transform(text)

    output: list[str] = []
    cursor = 0
    for span in spans:
        output.append(transform(text[cursor:span.start]))
        output.append(text[span.start:span.end])
        cursor = span.end
    output.append(transform(text[cursor:]))
    return "".join(output)
