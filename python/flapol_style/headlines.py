"""Explicit headline-only Florida Politics rules."""

from __future__ import annotations

from collections.abc import Iterable
import json
from importlib.resources import files
import re

from .reporting import EditingSession, EditResult, RuleSpec


_WORD_RE = re.compile(r"[A-Za-z]+(?:['’.-][A-Za-z]+)*")
_US_HEADLINE_RE = re.compile(r"\bUS\b")
_SENTENCE_CASE_RULE = RuleSpec(
    "flapol.headlines.sentence-case",
    "Florida Politics headline sentence-case rule",
)
_US_HEADLINE_RULE = RuleSpec(
    "flapol.headlines.us-periods",
    "Florida Politics main headline override",
)


def _load_builtin_preserve_phrases() -> tuple[str, ...]:
    path = files("flapol_style").joinpath("data/headline_preserve.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return tuple(data["phrases"])


_BUILTIN_PRESERVE_PHRASES = _load_builtin_preserve_phrases()


def _normalize_preserve_phrases(
    preserve_phrases: Iterable[str] | str,
) -> tuple[str, ...]:
    if isinstance(preserve_phrases, str):
        preserve_phrases = (preserve_phrases,)
    phrases = {
        phrase.strip()
        for phrase in (*_BUILTIN_PRESERVE_PHRASES, *preserve_phrases)
        if phrase and phrase.strip()
    }
    return tuple(sorted(phrases, key=len, reverse=True))


def _preserved_phrase_spans(
    text: str,
    phrases: tuple[str, ...],
) -> tuple[tuple[int, int], ...]:
    spans: list[tuple[int, int]] = []
    for phrase in phrases:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9]){re.escape(phrase)}(?![A-Za-z0-9])",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            original = match.group(0)
            if phrase.isupper():
                if original.isupper():
                    spans.append(match.span())
            elif original[0].isupper():
                spans.append(match.span())
    return tuple(spans)


def _looks_sentence_cased(text: str) -> bool:
    """Recognize copy that already contains ordinary lowercase words."""
    words = tuple(_WORD_RE.finditer(text))
    if not words:
        return True
    lowercase_initials = sum(match.group(0)[0].islower() for match in words)
    return lowercase_initials / len(words) > 0.4


def _starts_sentence(text: str, start: int) -> bool:
    prefix = text[:start]
    if not any(character.isalpha() for character in prefix):
        return True
    index = start - 1
    while index >= 0 and (
        text[index].isspace() or text[index] in "\"'“”‘’([{—–-"
    ):
        index -= 1
    return index >= 0 and text[index] in ".!?:"


def _has_internal_capital(word: str) -> bool:
    letters = [character for character in word if character.isalpha()]
    return any(character.isupper() for character in letters[1:])


def _apply_sentence_case(
    session: EditingSession,
    preserve_phrases: tuple[str, ...],
) -> None:
    if _looks_sentence_cased(session.text):
        return

    preserved_spans = _preserved_phrase_spans(session.text, preserve_phrases)

    def replace_word(match: re.Match[str], text: str) -> str | None:
        start, end = match.span()
        word = match.group(0)
        if start > 0 and text[start - 1].isdigit():
            return None
        if _starts_sentence(text, start):
            return None
        if any(
            start < span_end and span_start < end
            for span_start, span_end in preserved_spans
        ):
            return None
        letters = "".join(
            character for character in word if character.isalpha()
        )
        if len(letters) > 1 and letters.isupper():
            return None
        if _has_internal_capital(word):
            return None
        return word.lower()

    session.replace_pattern(_SENTENCE_CASE_RULE, _WORD_RE, replace_word)


def apply_headline_rules_to_session(
    session: EditingSession,
    preserve_phrases: Iterable[str] | str = (),
) -> None:
    phrases = _normalize_preserve_phrases(preserve_phrases)
    _apply_sentence_case(session, phrases)
    session.replace_pattern(_US_HEADLINE_RULE, _US_HEADLINE_RE, "U.S.")


def apply_headline_style_with_report(
    text: str,
    preserve_phrases: Iterable[str] | str = (),
) -> EditResult:
    """Apply the headline profile and return source-aware edit details.

    ``preserve_phrases`` lets a consumer supply current names or specialized
    proper nouns without making that changing registry part of this package.
    """
    session = EditingSession(text)
    apply_headline_rules_to_session(session, preserve_phrases)
    return session.result()


def apply_headline_style(
    text: str,
    preserve_phrases: Iterable[str] | str = (),
) -> str:
    """Convert imported title case to Florida Politics sentence case."""
    return apply_headline_style_with_report(text, preserve_phrases).text
