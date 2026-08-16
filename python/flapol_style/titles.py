"""Conservative title abbreviations before recognized name-shaped text."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .reporting import EditingSession, RuleSpec


_DATA_PATH = Path(__file__).with_name("data") / "title_abbreviations.json"
NAME_TOKEN_PATTERN = r"(?:[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|[A-Z]\.)"
FULL_NAME_PATTERN = (
    rf"{NAME_TOKEN_PATTERN}"
    rf"(?:\s+(?:[A-Z]\.?\s+)?{NAME_TOKEN_PATTERN})+"
)
FULL_NAME_DISPLAY_PATTERN = (
    rf"(?:{FULL_NAME_PATTERN}|\*\*{FULL_NAME_PATTERN}\*\*)"
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


_RULES = _compile_rules()


def apply_title_rules_to_session(session: EditingSession) -> None:
    for pattern, record in _RULES:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.titles.{record['id']}",
                authority=record["authority"],
            ),
            pattern,
            record["to"],
        )


def abbreviate_titles_before_names(text: str) -> str:
    """Abbreviate approved titles only when they directly precede a full name."""
    session = EditingSession(text)
    apply_title_rules_to_session(session)
    return session.text
