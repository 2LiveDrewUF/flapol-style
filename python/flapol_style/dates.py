"""AP/FlaPol date normalization salvaged from Streamlet.

The legacy implementation supplied the month mappings, weekday validation
and publication-date-relative behavior. This version separates display
normalization from contextual rewriting, protects verbatim/literal regions,
and never defaults contextual rules to the machine's current date.
"""

from __future__ import annotations

from datetime import date
import re

from .reporting import EditingSession, Replacement, RuleSpec


MONTHS_FULL = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
AP_ABBREVIATIONS = {
    "January": "Jan.",
    "February": "Feb.",
    "August": "Aug.",
    "September": "Sept.",
    "October": "Oct.",
    "November": "Nov.",
    "December": "Dec.",
}
ABBREVIATION_TO_FULL = {
    abbreviation: full for full, abbreviation in AP_ABBREVIATIONS.items()
}

MONTH_TO_NUMBER: dict[str, int] = {
    month: index for index, month in enumerate(MONTHS_FULL, 1)
}
for full, abbreviation in AP_ABBREVIATIONS.items():
    MONTH_TO_NUMBER[abbreviation] = MONTH_TO_NUMBER[full]

MONTH_TOKEN = (
    r"(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December|Jan\.|Feb\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)"
)
DAY_OF_WEEK = r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"

_SLOPPY_ABBREVIATION_RE = re.compile(
    r"\b(Jan|Feb|Sept|Sep|Aug|Oct|Nov|Dec)\b\.?(?=\s+\d{1,4}\b)"
)
_ABBREVIATION_CANON = {"Sep": "Sept."}
_ORDINAL_DATE_RE = re.compile(rf"\b({MONTH_TOKEN}\s+\d{{1,2}})(?:st|nd|rd|th)\b")
_ABBREVIATE_WITH_DAY_RE = re.compile(
    r"\b(January|February|August|September|October|November|December)"
    r"(?=\s+\d{1,2}\b)"
)
_EXPAND_WITH_YEAR_RE = re.compile(
    r"\b(Jan\.|Feb\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.),?\s+(\d{4})\b"
)
_MONTH_YEAR_COMMA_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|"
    r"October|November|December),\s+(\d{4})\b"
)
_FULL_DATE_RE = re.compile(
    rf"\b({MONTH_TOKEN}\s+\d{{1,2}}),?\s+(\d{{4}})\b(,?)"
)
_RELATIVE_DATE_RE = re.compile(
    rf"(?:({DAY_OF_WEEK}),?\s+)?"
    rf"({MONTH_TOKEN})\s+(\d{{1,2}})\b"
    rf"(?:,?\s*(\d{{4}})\b)?"
    r"(\s*,)?"
)


_MONTH_DAY_RULE = RuleSpec(
    "ap.dates.month-with-numbered-day",
    "AP Stylebook 56th edition, months entry",
    speech_preserving=True,
)
_ORDINAL_RULE = RuleSpec(
    "ap.dates.calendar-ordinal",
    "AP Stylebook 56th edition, dates entry",
    speech_preserving=True,
)
_MONTH_YEAR_RULE = RuleSpec(
    "ap.dates.month-without-numbered-day",
    "AP Stylebook 56th edition, months entry",
    speech_preserving=True,
)
_MONTH_YEAR_PUNCTUATION_RULE = RuleSpec(
    "ap.dates.month-year-punctuation",
    "AP Stylebook 56th edition, months entry",
    speech_preserving=True,
)
_FULL_DATE_PUNCTUATION_RULE = RuleSpec(
    "ap.dates.full-date-year-punctuation",
    "AP Stylebook 56th edition, dates entry",
    speech_preserving=True,
)
_CURRENT_YEAR_RULE = RuleSpec(
    "ap.dates.current-year-reference",
    "AP Stylebook 56th edition, time element entry",
)
_WEEKDAY_WINDOW_RULE = RuleSpec(
    "ap.dates.weekday-window",
    "AP Stylebook 56th edition, time element entry",
)


def apply_date_display_rules_to_session(session: EditingSession) -> None:
    session.replace_pattern(
        _MONTH_DAY_RULE,
        _SLOPPY_ABBREVIATION_RE,
        lambda match, _text: _ABBREVIATION_CANON.get(
            match.group(1), match.group(1) + "."
        ),
    )
    session.replace_pattern(_ORDINAL_RULE, _ORDINAL_DATE_RE, r"\1")
    session.replace_pattern(
        _MONTH_DAY_RULE,
        _ABBREVIATE_WITH_DAY_RE,
        lambda match, _text: AP_ABBREVIATIONS[match.group(1)],
    )
    session.replace_pattern(
        _MONTH_YEAR_RULE,
        _EXPAND_WITH_YEAR_RE,
        lambda match, _text: (
            f"{ABBREVIATION_TO_FULL[match.group(1)]} {match.group(2)}"
        ),
    )
    session.replace_pattern(
        _MONTH_YEAR_PUNCTUATION_RULE,
        _MONTH_YEAR_COMMA_RE,
        r"\1 \2",
    )

    def full_date_replacement(match: re.Match[str], text: str) -> str:
        month_day, year, existing_trailing_comma = match.groups()
        following = text[match.end():]
        trailing = existing_trailing_comma
        if not trailing and re.match(r"\s+[A-Za-z0-9]", following):
            trailing = ","
        return f"{month_day}, {year}{trailing}"

    session.replace_pattern(
        _FULL_DATE_PUNCTUATION_RULE,
        _FULL_DATE_RE,
        full_date_replacement,
    )


def normalize_date_display(text: str) -> str:
    """Apply fixed date-form rules outside protected regions."""
    session = EditingSession(text)
    apply_date_display_rules_to_session(session)
    return session.text


def apply_relative_date_rules_to_session(
    session: EditingSession, publication_date: date
) -> None:
    """Apply context-dependent weekday and current-year rules.

    A contradictory written weekday is left unchanged because the processor
    cannot know whether the weekday or numeric date is the reporting error.
    """
    def replace(match: re.Match[str], _text: str) -> Replacement | None:
        weekday, month_token, day_text, year_text, trailing_comma = match.groups()
        trailing_comma = trailing_comma or ""
        if not weekday and not year_text:
            return None

        month_number = MONTH_TO_NUMBER[month_token]
        day_number = int(day_text)
        if year_text:
            try:
                resolved = date(int(year_text), month_number, day_number)
            except ValueError:
                return None
        else:
            candidates: list[date] = []
            for year in (
                publication_date.year - 1,
                publication_date.year,
                publication_date.year + 1,
            ):
                try:
                    candidates.append(date(year, month_number, day_number))
                except ValueError:
                    continue
            if not candidates:
                return None
            resolved = min(
                candidates,
                key=lambda candidate: abs((candidate - publication_date).days),
            )

        is_current_year = resolved.year == publication_date.year
        if weekday:
            if weekday != resolved.strftime("%A"):
                return None
            if year_text and not is_current_year:
                return Replacement(
                    f"{month_token} {day_text}, {year_text}{trailing_comma}",
                    _WEEKDAY_WINDOW_RULE,
                )
            if abs((resolved - publication_date).days) < 7:
                return Replacement(weekday, _WEEKDAY_WINDOW_RULE)
            if year_text and is_current_year:
                return Replacement(
                    f"{month_token} {day_text}", _WEEKDAY_WINDOW_RULE
                )
            return Replacement(
                f"{month_token} {day_text}{trailing_comma}",
                _WEEKDAY_WINDOW_RULE,
            )

        if is_current_year:
            return Replacement(f"{month_token} {day_text}", _CURRENT_YEAR_RULE)
        return None

    session.replace_pattern(_CURRENT_YEAR_RULE, _RELATIVE_DATE_RE, replace)


def normalize_relative_dates(text: str, publication_date: date) -> str:
    """Apply context-dependent weekday and current-year rules."""
    session = EditingSession(text)
    apply_relative_date_rules_to_session(session, publication_date)
    return session.text


def apply_date_rules_to_session(
    session: EditingSession, publication_date: date | None = None
) -> None:
    apply_date_display_rules_to_session(session)
    if publication_date is not None:
        apply_relative_date_rules_to_session(session, publication_date)


def apply_date_rules(text: str, publication_date: date | None = None) -> str:
    """Normalize eligible date text while preserving protected regions.

    ``publication_date`` is required for current-year and weekday-window
    changes. Omitting it still permits fixed display normalization.
    """
    session = EditingSession(text)
    apply_date_rules_to_session(session, publication_date)
    return session.text
