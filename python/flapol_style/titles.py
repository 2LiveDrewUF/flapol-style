"""Conservative title abbreviations before recognized name-shaped text."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .protected import transform_unprotected


_DATA_PATH = Path(__file__).with_name("data") / "title_abbreviations.json"
_NAME_TOKEN = r"(?:[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|[A-Z]\.)"
_FULL_NAME = rf"{_NAME_TOKEN}(?:\s+(?:[A-Z]\.?\s+)?{_NAME_TOKEN})+"


def load_title_abbreviations() -> tuple[dict[str, str], ...]:
    """Load the public before-name title registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        records = json.load(source)
    return tuple(records)


def _compile_rules() -> tuple[tuple[re.Pattern[str], str], ...]:
    rules: list[tuple[re.Pattern[str], str]] = []
    for record in load_title_abbreviations():
        title = record["from"]
        rules.append(
            (
                re.compile(
                    rf"(?<![\w.])(?i:{re.escape(title)})(?=\s+{_FULL_NAME}\b)",
                ),
                record["to"],
            )
        )
    return tuple(rules)


_RULES = _compile_rules()


def abbreviate_titles_before_names(text: str) -> str:
    """Abbreviate approved titles only when they directly precede a full name."""

    def transform(chunk: str) -> str:
        for pattern, replacement in _RULES:
            chunk = pattern.sub(replacement, chunk)
        return chunk

    return transform_unprotected(text, transform)
