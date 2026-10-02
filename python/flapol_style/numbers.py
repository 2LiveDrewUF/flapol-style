"""Florida Politics number-sign forms with conservative context boundaries."""

from __future__ import annotations

import re

from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec


_AUTHORITY = "Florida Politics owner ruling 2026-10-02"
_NUMBER = r"(?P<number>\d+)(?!\w)"

_RANKING_AFTER_CUE_RE = re.compile(
    rf"(?P<prefix>\b(?:(?:ranked|rated|seeded|finished|placed)\s+|"
    rf"(?:rose|fell|moved|climbed|dropped)\s+to\s+))#{_NUMBER}",
    re.IGNORECASE,
)
_RANKING_BEFORE_CUE_RE = re.compile(
    rf"(?<![\w#])#{_NUMBER}(?P<suffix>-(?:ranked|rated|seeded)\b|\s+seed\b)",
    re.IGNORECASE,
)
_EXECUTIVE_ORDER_RE = re.compile(
    rf"(?P<prefix>\bExecutive\s+Order\s+)#{_NUMBER}",
    re.IGNORECASE,
)
_ROOM_RE = re.compile(
    rf"(?P<prefix>\bRoom\s+)#{_NUMBER}",
    re.IGNORECASE,
)
_BALLOT_AMENDMENT_RE = re.compile(
    rf"(?P<prefix>\b(?:Florida(?:\s+ballot)?|ballot)\s+Amendment\s+)"
    rf"#{_NUMBER}",
    re.IGNORECASE,
)
_AMBIGUOUS_AMENDMENT_RE = re.compile(
    rf"(?P<prefix>\bAmendment\s+)#{_NUMBER}",
    re.IGNORECASE,
)
_NUMBER_SIGN_RE = re.compile(rf"(?<![\w#])#{_NUMBER}")

_RANKING_RULE = RuleSpec(
    "flapol.numbers.ranking-number-sign",
    _AUTHORITY,
)
_EXECUTIVE_ORDER_RULE = RuleSpec(
    "flapol.numbers.executive-order-number-sign",
    _AUTHORITY,
)
_ROOM_RULE = RuleSpec(
    "flapol.numbers.room-number-sign",
    _AUTHORITY,
)
_BALLOT_AMENDMENT_RULE = RuleSpec(
    "flapol.numbers.ballot-amendment-number-sign",
    _AUTHORITY,
)


def _to_number_form(match: re.Match[str], _text: str) -> str:
    return f"{match.group('prefix')}No. {match.group('number')}"


def apply_number_sign_rules_to_session(session: EditingSession) -> None:
    """Apply only number-sign corrections whose context proves the result."""
    session.replace_pattern(_RANKING_RULE, _RANKING_AFTER_CUE_RE, _to_number_form)
    session.replace_pattern(
        _RANKING_RULE,
        _RANKING_BEFORE_CUE_RE,
        lambda match, _text: (
            f"No. {match.group('number')}{match.group('suffix')}"
        ),
    )
    session.replace_pattern(
        _EXECUTIVE_ORDER_RULE,
        _EXECUTIVE_ORDER_RE,
        _to_number_form,
    )
    session.replace_pattern(_ROOM_RULE, _ROOM_RE, _to_number_form)
    session.replace_pattern(
        _BALLOT_AMENDMENT_RULE,
        _BALLOT_AMENDMENT_RE,
        lambda match, _text: (
            f"{match.group('prefix')}{match.group('number')}"
        ),
    )


def number_sign_flags_for_session(session: EditingSession) -> tuple[Finding, ...]:
    """Flag unprotected numeric hash forms that still require adjudication."""
    text = session.text
    protected = find_protected_spans(text)
    findings: list[Finding] = []
    occupied: list[tuple[int, int]] = []

    def is_protected(start: int, end: int) -> bool:
        return any(start < span.end and span.start < end for span in protected)

    for match in _AMBIGUOUS_AMENDMENT_RE.finditer(text):
        if is_protected(*match.span()):
            continue
        source_start, source_end = session.source_span(*match.span())
        findings.append(
            Finding(
                rule_id="flapol.numbers.amendment-number-sign-review",
                action="FLAG",
                found=match.group(0),
                suggestion=f"{match.group('prefix')}{match.group('number')}",
                source_start=source_start,
                source_end=source_end,
                severity="warning",
                authority=_AUTHORITY,
            )
        )
        occupied.append(match.span())

    for match in _NUMBER_SIGN_RE.finditer(text):
        if is_protected(*match.span()):
            continue
        if any(
            match.start() < end and start < match.end()
            for start, end in occupied
        ):
            continue
        source_start, source_end = session.source_span(*match.span())
        findings.append(
            Finding(
                rule_id="flapol.numbers.number-sign-review",
                action="FLAG",
                found=match.group(0),
                suggestion=f"No. {match.group('number')}",
                source_start=source_start,
                source_end=source_end,
                severity="warning",
                authority=_AUTHORITY,
            )
        )

    return tuple(
        sorted(findings, key=lambda item: (item.start, item.end, item.rule_id))
    )


def normalize_number_sign_forms(text: str) -> str:
    """Apply only context-proven number-sign forms outside quotations."""
    session = EditingSession(text)
    apply_number_sign_rules_to_session(session)
    return session.text


def find_number_sign_flags(text: str) -> tuple[Finding, ...]:
    """Apply proven forms, then report unresolved numeric hash forms."""
    session = EditingSession(text)
    apply_number_sign_rules_to_session(session)
    return number_sign_flags_for_session(session)
