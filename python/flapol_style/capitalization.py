"""Conservative capitalization fixes and context-required findings."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec
from .titles import FULL_NAME_DISPLAY_PATTERN


_DATA_PATH = Path(__file__).with_name("data") / "capitalization.json"
_JURISDICTION_TOKEN = r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+"
_NON_JURISDICTION_PREFIXES = (
    "A|An|Any|City|County|Each|Every|Federal|Local|Many|Most|Municipal|No|"
    "Private|Public|Regional|Several|Some|State|The"
)
_JURISDICTION = (
    rf"(?!(?:{_NON_JURISDICTION_PREFIXES})\b)"
    rf"{_JURISDICTION_TOKEN}(?:\s+{_JURISDICTION_TOKEN}){{0,3}}"
)


CapitalizationFinding = Finding


def load_capitalization_rules() -> dict[str, object]:
    """Load the public capitalization registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        return json.load(source)


_RULES = load_capitalization_rules()


def _exact_patterns() -> tuple[tuple[re.Pattern[str], dict[str, str]], ...]:
    compiled: list[tuple[re.Pattern[str], dict[str, str]]] = []
    records = sorted(
        _RULES["automatic_exact"],
        key=lambda record: len(record["from"]),
        reverse=True,
    )
    for record in records:
        compiled.append(
            (
                re.compile(
                    rf"(?<![\w-]){re.escape(record['from'])}(?![\w-])",
                    re.IGNORECASE,
                ),
                record,
            )
        )
    return tuple(compiled)


_EXACT_PATTERNS = _exact_patterns()
_BEFORE_NAME_PATTERNS = tuple(
    (
        re.compile(
            rf"(?<![\w.])(?i:{re.escape(record['from'])})"
            rf"(?=\s+{FULL_NAME_DISPLAY_PATTERN}(?:\b|(?<=\*\*)))"
        ),
        record,
    )
    for record in sorted(
        _RULES["before_name_titles"],
        key=lambda record: len(record["from"]),
        reverse=True,
    )
)
_BODY_PATTERNS = tuple(
    (
        re.compile(
            rf"\b({_JURISDICTION})\s+(?i:{re.escape(record['from'])})\b"
        ),
        record,
    )
    for record in sorted(
        _RULES["governmental_bodies"],
        key=lambda record: len(record["from"]),
        reverse=True,
    )
)
_FLAG_PATTERNS = tuple(
    (
        re.compile(
            rf"(?<![\w-]){re.escape(record['from'])}(?![\w-])",
            re.IGNORECASE,
        ),
        record,
    )
    for record in sorted(
        _RULES["context_flags"],
        key=lambda record: len(record["from"]),
        reverse=True,
    )
)


def apply_capitalization_rules_to_session(session: EditingSession) -> None:
    for pattern, record in _EXACT_PATTERNS:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.capitalization.{record['id']}",
                authority=record["authority"],
            ),
            pattern,
            record["to"],
        )
    for pattern, record in _BEFORE_NAME_PATTERNS:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.capitalization.{record['id']}",
                authority=record["authority"],
            ),
            pattern,
            record["to"],
        )
    for pattern, record in _BODY_PATTERNS:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.capitalization.{record['id']}",
                authority=record["authority"],
            ),
            pattern,
            lambda match, _text, body=record["to"]: (
                f"{match.group(1)} {body}"
            ),
        )


def normalize_capitalization(text: str) -> str:
    """Apply only capitalization changes with sufficient textual context."""
    session = EditingSession(text)
    apply_capitalization_rules_to_session(session)
    return session.text


def capitalization_flags_for_session(session: EditingSession) -> tuple[Finding, ...]:
    """Report possible house forms against the session's original source."""
    text = session.text
    protected = find_protected_spans(text)
    findings: list[Finding] = []
    cursor = 0

    for span in [*protected, None]:
        end = span.start if span is not None else len(text)
        chunk = text[cursor:end]
        occupied: list[tuple[int, int]] = []
        for pattern, _record in (
            *_EXACT_PATTERNS,
            *_BEFORE_NAME_PATTERNS,
            *_BODY_PATTERNS,
        ):
            occupied.extend((match.start(), match.end()) for match in pattern.finditer(chunk))
        for pattern, record in _FLAG_PATTERNS:
            for match in pattern.finditer(chunk):
                found = match.group(0)
                if found == record["to"]:
                    continue
                candidate = (match.start(), match.end())
                if any(
                    candidate[0] < existing[1] and existing[0] < candidate[1]
                    for existing in occupied
                ):
                    continue
                findings.append(
                    Finding(
                        rule_id=f"flapol.capitalization.{record['id']}",
                        action="FLAG",
                        found=found,
                        suggestion=record["to"],
                        source_start=session.source_span(
                            cursor + match.start(), cursor + match.end()
                        )[0],
                        source_end=session.source_span(
                            cursor + match.start(), cursor + match.end()
                        )[1],
                        severity="warning",
                        authority=record.get("authority", "Florida Politics main"),
                    )
                )
                occupied.append(candidate)
        if span is None:
            break
        cursor = span.end

    return tuple(sorted(findings, key=lambda item: (item.start, item.end, item.rule_id)))


def find_capitalization_flags(text: str) -> tuple[CapitalizationFinding, ...]:
    """Report possible house forms that still require semantic confirmation."""
    return capitalization_flags_for_session(EditingSession(text))
