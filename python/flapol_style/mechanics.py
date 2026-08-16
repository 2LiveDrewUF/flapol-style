"""Protected mechanical rules already established by Vale fixtures."""

from __future__ import annotations

import re

from .reporting import EditingSession, RuleSpec


_COVID_RE = re.compile(r"\bCOVID-19\b", re.IGNORECASE)
_US_RE = re.compile(r"\bUS\b")
_CHAIR_RE = re.compile(r"\bChair(?:man|woman)\b", re.IGNORECASE)
_PERCENT_RE = re.compile(
    r"(?<![\w.])(\d+(?:,\d{3})*(?:\.\d+)?)\s+(?:percent|per cent)\b",
    re.IGNORECASE,
)
_SMALL_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
_TENS_NUMBER_WORDS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
_SMALL_WORD_RE = "|".join(_SMALL_NUMBER_WORDS)
_UNIT_WORD_RE = "|".join(tuple(_SMALL_NUMBER_WORDS)[1:10])
_TENS_WORD_RE = "|".join(_TENS_NUMBER_WORDS)
_UNDER_HUNDRED_RE = (
    rf"(?:{_SMALL_WORD_RE}|(?:{_TENS_WORD_RE})(?:[- ](?:{_UNIT_WORD_RE}))?)"
)
_SPOKEN_NUMBER_RE = (
    rf"(?:{_UNDER_HUNDRED_RE}|(?:{_UNIT_WORD_RE}) hundred"
    rf"(?: (?:and )?{_UNDER_HUNDRED_RE})?)"
)
_SPOKEN_PERCENT_RE = re.compile(
    rf"(?<![\w-])({_SPOKEN_NUMBER_RE})\s+(?:percent|per cent)\b",
    re.IGNORECASE,
)
_TIME_RE = re.compile(
    r"(?<![\w:])((?:0?[1-9]|1[0-2])(?::[0-5]\d)?)\s*"
    r"([ap])\.?m\.?(?=\s|[.,;:!?)\"”’]|$)",
    re.IGNORECASE,
)
_SPOKEN_HOUR_RE = re.compile(
    r"(?<![\w-])(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s*([ap])\.?m\.?(?=\s|[.,;:!?)\"”’]|$)",
    re.IGNORECASE,
)

_COVID_RULE = RuleSpec(
    "flapol.terms.covid-without-19",
    "Florida Politics main",
)
_US_RULE = RuleSpec(
    "flapol.terms.us-periods",
    "AP baseline and Florida Politics main",
    speech_preserving=True,
)
_CHAIR_RULE = RuleSpec(
    "flapol.titles.gender-neutral-chair",
    "Florida Politics main",
)
_PERCENT_RULE = RuleSpec(
    "ap.numbers.percent-symbol",
    "AP Stylebook 56th edition, percent entry",
    speech_preserving=True,
)
_SPOKEN_PERCENT_RULE = RuleSpec(
    "ap.numbers.spoken-percent-symbol",
    "AP percent form and Florida Politics quote-boundary clarification 2026-08-16",
    speech_preserving=True,
)
_TIME_RULE = RuleSpec(
    "ap.times.meridiem-format",
    "AP Stylebook 56th edition, times entry",
    speech_preserving=True,
)
_SPOKEN_HOUR_RULE = RuleSpec(
    "ap.times.spoken-hour-meridiem",
    "AP time form and Florida Politics quote-boundary clarification 2026-08-16",
    speech_preserving=True,
)


def _spoken_number_value(source: str) -> int | None:
    words = source.lower().replace("-", " ").split()
    words = [word for word in words if word != "and"]
    if "hundred" in words:
        if len(words) < 2 or words[0] not in _SMALL_NUMBER_WORDS:
            return None
        value = _SMALL_NUMBER_WORDS[words[0]] * 100
        words = words[2:]
    else:
        value = 0
    if not words:
        return value
    if len(words) == 1:
        return value + _SMALL_NUMBER_WORDS.get(
            words[0], _TENS_NUMBER_WORDS.get(words[0], -1000)
        )
    if (
        len(words) == 2
        and words[0] in _TENS_NUMBER_WORDS
        and words[1] in _SMALL_NUMBER_WORDS
        and 0 < _SMALL_NUMBER_WORDS[words[1]] < 10
    ):
        return value + _TENS_NUMBER_WORDS[words[0]] + _SMALL_NUMBER_WORDS[words[1]]
    return None


def apply_mechanical_rules_to_session(session: EditingSession) -> None:
    session.replace_pattern(_COVID_RULE, _COVID_RE, "COVID")
    session.replace_pattern(_US_RULE, _US_RE, "U.S.")
    session.replace_pattern(_CHAIR_RULE, _CHAIR_RE, "Chair")
    session.replace_pattern(_PERCENT_RULE, _PERCENT_RE, r"\1%")
    session.replace_pattern(
        _SPOKEN_PERCENT_RULE,
        _SPOKEN_PERCENT_RE,
        lambda match, _text: (
            f"{value}%"
            if (value := _spoken_number_value(match.group(1))) is not None
            else None
        ),
    )
    session.replace_pattern(
        _TIME_RULE,
        _TIME_RE,
        lambda match, _text: (
            f"{match.group(1)} {match.group(2).lower()}.m"
            f"{'' if match.end() < len(_text) and _text[match.end()] == '.' else '.'}"
        ),
    )
    session.replace_pattern(
        _SPOKEN_HOUR_RULE,
        _SPOKEN_HOUR_RE,
        lambda match, _text: (
            f"{_SMALL_NUMBER_WORDS[match.group(1).lower()]} "
            f"{match.group(2).lower()}.m"
            f"{'' if match.end() < len(_text) and _text[match.end()] == '.' else '.'}"
        ),
    )


def normalize_mechanical_forms(text: str) -> str:
    """Normalize protected house and AP mechanical forms."""
    session = EditingSession(text)
    apply_mechanical_rules_to_session(session)
    return session.text
