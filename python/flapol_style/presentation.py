"""Markdown presentation rules for Florida Politics bold treatment."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Iterable

from .protected import find_protected_spans
from .reporting import EditingSession, EditResult, Finding, RuleSpec
from .titles import FULL_NAME_PATTERN


_DATA_PATH = Path(__file__).with_name("data") / "bolding.json"
_AUTHORITY = "Florida Politics owner ruling, 2026-08-18"
_STRONG_RE = re.compile(r"\*\*(?P<inner>[^*\n]+?)\*\*")
_INLINE_LINK_RE = re.compile(
    r"(?<!!)\[(?P<label>[^\]\n]+)\]"
    r"(?P<target>\((?:[^()\\\n]|\\.|\([^()\n]*\))*\)|\[[^\]\n]+\])"
)


def load_bolding_rules() -> dict[str, tuple[str, ...]]:
    """Load the public title and nonperson-term presentation registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        data = json.load(source)
    return {key: tuple(value) for key, value in data.items()}


_BOLDING_RULES = load_bolding_rules()
_TITLE_PREFIXES = tuple(
    sorted(_BOLDING_RULES["title_prefixes"], key=len, reverse=True)
)
_TITLE_PREFIX_RE = re.compile(
    r"\*\*(?P<title>"
    + "|".join(re.escape(value) for value in _TITLE_PREFIXES)
    + rf")(?P<space>\s+)(?P<name>{FULL_NAME_PATTERN})\*\*",
    re.IGNORECASE,
)
_TITLE_BEFORE_STRONG_RE = re.compile(
    r"(?:"
    + "|".join(re.escape(value) for value in _TITLE_PREFIXES)
    + r")\s+$",
    re.IGNORECASE,
)
_NONPERSON_TERM_RE = re.compile(
    r"(?<![\w])(?:"
    + "|".join(
        re.escape(value)
        + (
            r"\.?"
            if value.split()[-1] in {"rep", "reps", "sen", "sens"}
            else ""
        )
        for value in sorted(
            _BOLDING_RULES["nonperson_office_terms"], key=len, reverse=True
        )
    )
    + r")(?![\w])",
    re.IGNORECASE,
)

_LINK_RULE = RuleSpec(
    rule_id="flapol.presentation.bold-hyperlink-text",
    authority=_AUTHORITY,
    speech_preserving=True,
)
_TITLE_RULE = RuleSpec(
    rule_id="flapol.presentation.title-outside-person-bold",
    authority=_AUTHORITY,
    speech_preserving=True,
)
_OFFICE_RULE = RuleSpec(
    rule_id="flapol.presentation.remove-office-group-bold",
    authority=_AUTHORITY,
    speech_preserving=True,
)
_PERSON_RULE = RuleSpec(
    rule_id="flapol.presentation.bold-person-first-reference",
    authority=_AUTHORITY,
    speech_preserving=True,
)
_PERSON_NARROW_RULE = RuleSpec(
    rule_id="flapol.presentation.narrow-person-bold-span",
    authority=_AUTHORITY,
    speech_preserving=True,
)
_CLEANUP_RULE = RuleSpec(
    rule_id="flapol.presentation.remove-unauthorized-bold",
    authority=_AUTHORITY,
    speech_preserving=True,
)


def _overlaps(start: int, end: int, spans: Iterable[tuple[int, int]]) -> bool:
    return any(start < span_end and span_start < end for span_start, span_end in spans)


def _hard_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        (span.start, span.end)
        for span in find_protected_spans(text, allow_balanced_quotations=True)
    )


def _link_label_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        (match.start("label"), match.end("label"))
        for match in _INLINE_LINK_RE.finditer(text)
    )


def _inside_link_label(start: int, end: int, text: str) -> bool:
    return any(
        label_start <= start and end <= label_end
        for label_start, label_end in _link_label_spans(text)
    )


def _normalize_person_names(person_names: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    for supplied in person_names:
        name = supplied.strip()
        if not name:
            raise ValueError("person names must not be empty")
        if any(marker in name for marker in ("\n", "[", "]", "*", "`")):
            raise ValueError("person names must be plain single-line text")
        if name not in normalized:
            normalized.append(name)
    return tuple(sorted(normalized, key=len, reverse=True))


def _bold_hyperlinks(session: EditingSession) -> None:
    cursor = 0
    while True:
        match = _INLINE_LINK_RE.search(session.text, cursor)
        if not match:
            return
        label = match.group("label")
        full_end = match.end()
        outer_bold = (
            match.start() >= 2
            and session.text[match.start() - 2:match.start()] == "**"
            and session.text[full_end:full_end + 2] == "**"
        )
        if outer_bold or (label.startswith("**") and label.endswith("**")):
            cursor = full_end
            continue
        if session.replace_span(
            _LINK_RULE,
            match.start("label"),
            match.end("label"),
            f"**{label}**",
        ):
            cursor = match.end("label") + 4
        else:
            cursor = full_end


def _narrow_known_title_prefixes(session: EditingSession) -> None:
    def replacement(match: re.Match[str], text: str) -> str | None:
        if _inside_link_label(match.start(), match.end(), text):
            return None
        return f"{match.group('title')}{match.group('space')}**{match.group('name')}**"

    session.replace_pattern(_TITLE_RULE, _TITLE_PREFIX_RE, replacement)


def _remove_office_group_bold(session: EditingSession) -> None:
    def replacement(match: re.Match[str], text: str) -> str | None:
        if _inside_link_label(match.start(), match.end(), text):
            return None
        inner = match.group("inner")
        if _NONPERSON_TERM_RE.search(inner):
            return inner
        return None

    session.replace_pattern(_OFFICE_RULE, _STRONG_RE, replacement)


def _name_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w]){re.escape(name)}(?![\w])")


def _first_name_span(text: str, name: str) -> tuple[int, int] | None:
    hard_spans = _hard_spans(text)
    for match in _name_pattern(name).finditer(text):
        if not _overlaps(match.start(), match.end(), hard_spans):
            return match.start(), match.end()
    return None


def _enclosing_strong_span(
    text: str, start: int, end: int
) -> re.Match[str] | None:
    for match in _STRONG_RE.finditer(text):
        if match.start("inner") <= start and end <= match.end("inner"):
            return match
    return None


def _normalize_supplied_people(
    session: EditingSession, person_names: tuple[str, ...]
) -> None:
    for name in person_names:
        span = _first_name_span(session.text, name)
        if span is None:
            continue
        start, end = span
        if _inside_link_label(start, end, session.text):
            continue

        strong = _enclosing_strong_span(session.text, start, end)
        if strong is not None:
            if strong.group("inner") == name:
                continue
            relative_start = start - strong.start("inner")
            relative_end = end - strong.start("inner")
            inner = strong.group("inner")
            replacement = (
                inner[:relative_start]
                + f"**{inner[relative_start:relative_end]}**"
                + inner[relative_end:]
            )
            session.replace_span(
                _PERSON_NARROW_RULE,
                strong.start(),
                strong.end(),
                replacement,
            )
            continue

        session.replace_span(_PERSON_RULE, start, end, f"**{name}**")


def _allowed_person_strong_spans(
    text: str, person_names: tuple[str, ...]
) -> set[tuple[int, int]]:
    allowed: set[tuple[int, int]] = set()
    for name in person_names:
        span = _first_name_span(text, name)
        if span is None:
            continue
        strong = _enclosing_strong_span(text, *span)
        if strong is not None and strong.group("inner") == name:
            allowed.add((strong.start(), strong.end()))
    return allowed


def _follows_known_title(text: str, match: re.Match[str]) -> bool:
    """Return whether a name-shaped strong span follows an approved title."""
    if re.fullmatch(FULL_NAME_PATTERN, match.group("inner")) is None:
        return False
    prefix = text[max(0, match.start() - 80):match.start()]
    return _TITLE_BEFORE_STRONG_RE.search(prefix) is not None


def _remove_remaining_bold(
    session: EditingSession, person_names: tuple[str, ...]
) -> None:
    while True:
        allowed = _allowed_person_strong_spans(session.text, person_names)
        link_labels = _link_label_spans(session.text)
        hard_spans = _hard_spans(session.text)
        candidate: re.Match[str] | None = None
        for match in _STRONG_RE.finditer(session.text):
            if (match.start(), match.end()) in allowed:
                continue
            if _overlaps(match.start(), match.end(), link_labels):
                continue
            if _overlaps(match.start(), match.end(), hard_spans):
                continue
            candidate = match
            break
        if candidate is None:
            return
        session.replace_span(
            _CLEANUP_RULE,
            candidate.start(),
            candidate.end(),
            candidate.group("inner"),
        )


def _unverified_bold_findings(
    session: EditingSession, person_names: tuple[str, ...]
) -> tuple[Finding, ...]:
    allowed = _allowed_person_strong_spans(session.text, person_names)
    link_labels = _link_label_spans(session.text)
    hard_spans = _hard_spans(session.text)
    findings: list[Finding] = []
    for match in _STRONG_RE.finditer(session.text):
        if (match.start(), match.end()) in allowed:
            continue
        if _follows_known_title(session.text, match):
            continue
        if _overlaps(match.start(), match.end(), link_labels):
            continue
        if _overlaps(match.start(), match.end(), hard_spans):
            continue
        source_start, source_end = session.source_span(match.start(), match.end())
        findings.append(
            Finding(
                rule_id="flapol.presentation.unverified-nonlink-bold",
                action="FLAG",
                found=match.group(0),
                suggestion=match.group("inner"),
                source_start=source_start,
                source_end=source_end,
                severity="warning",
                authority=_AUTHORITY,
            )
        )
    return tuple(findings)


def apply_presentation_style_with_report(
    text: str,
    person_names: Iterable[str] = (),
    *,
    person_context_complete: bool = False,
) -> EditResult:
    """Normalize Markdown bolding under explicit person-name context.

    Supplied names authorize first-reference name bolding. Declaring the
    context complete additionally authorizes removal of every remaining
    nonlink bold span. Without that declaration, uncertain nonlink bold is
    reported rather than removed.
    """
    names = _normalize_person_names(person_names)
    session = EditingSession(text)
    _bold_hyperlinks(session)
    _narrow_known_title_prefixes(session)
    _remove_office_group_bold(session)
    _normalize_supplied_people(session, names)
    if person_context_complete:
        _remove_remaining_bold(session, names)
        findings: tuple[Finding, ...] = ()
    else:
        findings = _unverified_bold_findings(session, names)
    return session.result(findings)


def apply_presentation_style(
    text: str,
    person_names: Iterable[str] = (),
    *,
    person_context_complete: bool = False,
) -> str:
    """Return Markdown with implemented Florida Politics bold conventions."""
    return apply_presentation_style_with_report(
        text,
        person_names,
        person_context_complete=person_context_complete,
    ).text
