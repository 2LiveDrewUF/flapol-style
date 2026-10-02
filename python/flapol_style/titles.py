"""Conservative title abbreviations before recognized name-shaped text."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec


_DATA_PATH = Path(__file__).with_name("data") / "title_abbreviations.json"
_AGRICULTURE_COMMISSIONER_ORDER_RULE = RuleSpec(
    "flapol.titles.agriculture-commissioner-order",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=False,
)
_AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE = RuleSpec(
    "flapol.titles.agriculture-commissioner-capitalization",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=True,
)
_FLORIDA_GOVERNOR_HOME_STATE_RULE = RuleSpec(
    "flapol.titles.florida-governor-home-state",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=False,
)
_COMMISSIONER_OF_AGRICULTURE_RE = re.compile(
    r"(?<![\w])(?i:Commissioner\s+of\s+Agriculture)(?![\w])"
)
_AGRICULTURE_COMMISSIONER_RE = re.compile(
    r"(?<![\w])(?i:Agriculture\s+Commissioner)(?![\w])"
)
NAME_TOKEN_PATTERN = r"(?:[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|[A-Z]\.)"
FULL_NAME_PATTERN = (
    rf"{NAME_TOKEN_PATTERN}"
    rf"(?:\s+(?:[A-Z]\.?\s+)?{NAME_TOKEN_PATTERN})+"
)
FULL_NAME_DISPLAY_PATTERN = (
    rf"(?:{FULL_NAME_PATTERN}|\*\*{FULL_NAME_PATTERN}\*\*)"
)
_FLORIDA_GOVERNOR_BEFORE_NAME_RE = re.compile(
    rf"(?<![\w])(?i:Florida)\s+"
    rf"(?=(?i:Governor|Gov\.)\s+{FULL_NAME_DISPLAY_PATTERN}"
    rf"(?:\b|(?<=\*\*)))"
)
_FLORIDA_GOVERNOR_WITHOUT_NAME_RE = re.compile(
    r"(?<![\w])(?i:Florida\s+)(?P<title>(?i:Governor|Gov\.))(?![\w])"
)
_GOVERNORS_MANSION_SUFFIX_RE = re.compile(
    r"^['’]s\s+Mansion\b",
    re.IGNORECASE,
)


def load_title_abbreviations() -> tuple[dict[str, str], ...]:
    """Load the public before-name title registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        records = json.load(source)
    return tuple(records)


def _compile_rules() -> tuple[tuple[re.Pattern[str], dict[str, str]], ...]:
    rules: list[tuple[re.Pattern[str], dict[str, str]]] = []
    for record in load_title_abbreviations():
        title = record["from"]
        rules.append(
            (
                re.compile(
                    rf"(?<![\w.])(?i:{re.escape(title)})"
                    rf"(?=\s+{FULL_NAME_DISPLAY_PATTERN}(?:\b|(?<=\*\*)))",
                ),
                record,
            )
        )
    return tuple(rules)


_ABBREVIATION_RULES = _compile_rules()


def apply_office_title_form_rules_to_session(session: EditingSession) -> None:
    """Apply house order and capitalization for office titles."""
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_ORDER_RULE,
        _COMMISSIONER_OF_AGRICULTURE_RE,
        "Agriculture Commissioner",
    )
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE,
        _AGRICULTURE_COMMISSIONER_RE,
        "Agriculture Commissioner",
    )
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE,
        _COMMISSIONER_OF_AGRICULTURE_RE,
        "Commissioner of Agriculture",
    )


def apply_home_state_title_rules_to_session(session: EditingSession) -> None:
    """Remove a redundant Florida label where the full title proves context."""
    session.replace_pattern(
        _FLORIDA_GOVERNOR_HOME_STATE_RULE,
        _FLORIDA_GOVERNOR_BEFORE_NAME_RE,
        "",
    )


def home_state_title_flags_for_session(
    session: EditingSession,
) -> tuple[Finding, ...]:
    """Flag unresolved Florida title labels that lack a full-name context."""
    text = session.text
    protected = find_protected_spans(text)
    findings: list[Finding] = []

    for match in _FLORIDA_GOVERNOR_WITHOUT_NAME_RE.finditer(text):
        if any(
            match.start() < span.end and span.start < match.end()
            for span in protected
        ):
            continue
        if _GOVERNORS_MANSION_SUFFIX_RE.match(text[match.end():]):
            continue
        source_start, source_end = session.source_span(
            match.start(), match.end()
        )
        title = match.group("title")
        suggestion = "Gov." if title.casefold() == "gov." else "Governor"
        findings.append(
            Finding(
                rule_id="flapol.titles.florida-governor-without-name",
                action="FLAG",
                found=match.group(0),
                suggestion=suggestion,
                source_start=source_start,
                source_end=source_end,
                severity="warning",
                authority="Florida Politics owner ruling 2026-10-02",
            )
        )

    return tuple(findings)


def apply_title_rules_to_session(session: EditingSession) -> None:
    apply_office_title_form_rules_to_session(session)
    apply_home_state_title_rules_to_session(session)
    for pattern, record in _ABBREVIATION_RULES:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.titles.{record['id']}",
                authority=record["authority"],
                speech_preserving=record["speech_preserving"],
            ),
            pattern,
            record["to"],
        )


def abbreviate_titles_before_names(text: str) -> str:
    """Abbreviate approved titles only when they directly precede a full name."""
    session = EditingSession(text)
    for pattern, record in _ABBREVIATION_RULES:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.titles.{record['id']}",
                authority=record["authority"],
                speech_preserving=record["speech_preserving"],
            ),
            pattern,
            record["to"],
        )
    return session.text


def normalize_office_title_forms(text: str) -> str:
    """Apply deterministic Florida Politics office-title forms."""
    session = EditingSession(text)
    apply_office_title_form_rules_to_session(session)
    return session.text
