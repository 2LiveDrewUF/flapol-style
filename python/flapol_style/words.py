"""Closed, provenance-bearing Florida Politics word-form replacements."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .reporting import EditingSession, RuleSpec


_DATA_PATH = Path(__file__).with_name("data") / "word_preferences.json"


def load_word_preferences() -> tuple[dict[str, str], ...]:
    """Load the public word-form registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        records = json.load(source)
    return tuple(records)


def _project_case(source: str, replacement: str) -> str:
    # A title-cased phrase may be part of a verified formal name, such as the
    # Health Care District of Palm Beach County. Without entity metadata, fail
    # conservatively rather than silently renaming it.
    if source in {"Health Care", "Health-Care"} and replacement == "healthcare":
        return source
    if source.isupper():
        return replacement.upper()
    if source[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _compile_rules() -> tuple[tuple[re.Pattern[str], dict[str, str]], ...]:
    rules: list[tuple[re.Pattern[str], dict[str, str]]] = []
    for record in load_word_preferences():
        source = record["from"]
        pattern = re.compile(
            rf"(?<![\w-]){re.escape(source)}(?![\w-])",
            re.IGNORECASE,
        )
        rules.append((pattern, record))
    return tuple(rules)


_RULES = _compile_rules()


def apply_word_rules_to_session(session: EditingSession) -> None:
    for pattern, record in _RULES:
        spec = RuleSpec(
            rule_id=f"flapol.words.{record['id']}",
            authority=record["authority"],
            action=record["action"],
            speech_preserving=record["speech_preserving"],
        )
        session.replace_pattern(
            spec,
            pattern,
            lambda match, _text, replacement=record["to"]: _project_case(
                match.group(0), replacement
            ),
        )


def normalize_word_forms(text: str) -> str:
    """Apply approved word forms under their individual quote policies."""
    session = EditingSession(text)
    apply_word_rules_to_session(session)
    return session.text
