"""Protected-region discovery for deterministic editing.

Protection is deliberately conservative. When a quotation or code fence is
unbalanced, the uncertain remainder is protected instead of being rewritten.
The processor may miss a correction in malformed input; it must not silently
alter text that could be verbatim or literal.
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
_URL_RE = re.compile(r"https?://[^\s<>\]\[\"']+", re.IGNORECASE)
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
        spans.append(ProtectedSpan(start, end, "direct_quotation"))
        if close < 0:
            break
        cursor = end

    straight = [m.start() for m in re.finditer(r'(?<!\\)"', text)]
    for index in range(0, len(straight), 2):
        start = straight[index]
        end = straight[index + 1] + 1 if index + 1 < len(straight) else len(text)
        spans.append(ProtectedSpan(start, end, "direct_quotation"))

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


def find_protected_spans(text: str) -> list[ProtectedSpan]:
    """Return merged spans that deterministic transformations must not edit."""
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
    spans.extend(_quote_spans(text))
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
