"""Closed, provenance-bearing Florida Politics word-form replacements."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .protected import transform_unprotected


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


def _compile_rules() -> tuple[tuple[re.Pattern[str], str], ...]:
    rules: list[tuple[re.Pattern[str], str]] = []
    for record in load_word_preferences():
        source = record["from"]
        pattern = re.compile(
            rf"(?<![\w-]){re.escape(source)}(?![\w-])",
            re.IGNORECASE,
        )
        rules.append((pattern, record["to"]))
    return tuple(rules)


_RULES = _compile_rules()


def normalize_word_forms(text: str) -> str:
    """Apply approved word forms outside quotations and literal regions."""

    def transform(chunk: str) -> str:
        for pattern, replacement in _RULES:
            chunk = pattern.sub(
                lambda match: _project_case(match.group(0), replacement),
                chunk,
            )
        return chunk

    return transform_unprotected(text, transform)
