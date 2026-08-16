"""AP/FlaPol date normalization salvaged from Streamlet.

The legacy implementation supplied the month mappings, weekday validation
and publication-date-relative behavior. This version separates display
normalization from contextual rewriting, protects verbatim/literal regions,
and never defaults contextual rules to the machine's current date.
"""

from __future__ import annotations

from datetime import date
import re

from .protected import transform_unprotected


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


def _normalize_full_date_commas(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month_day, year, existing_trailing_comma = match.groups()
        following = text[match.end():]
        trailing = existing_trailing_comma
        if not trailing and re.match(r"\s+[A-Za-z0-9]", following):
            trailing = ","
        return f"{month_day}, {year}{trailing}"

    return _FULL_DATE_RE.sub(replace, text)


def normalize_date_display(text: str) -> str:
    """Apply fixed date-form rules to an already unprotected text slice."""
    if not text:
        return text
    text = _SLOPPY_ABBREVIATION_RE.sub(
        lambda match: _ABBREVIATION_CANON.get(
            match.group(1), match.group(1) + "."
        ),
        text,
    )
    text = _ORDINAL_DATE_RE.sub(r"\1", text)
    text = _ABBREVIATE_WITH_DAY_RE.sub(
        lambda match: AP_ABBREVIATIONS[match.group(1)], text
    )
    text = _EXPAND_WITH_YEAR_RE.sub(
        lambda match: (
            f"{ABBREVIATION_TO_FULL[match.group(1)]} {match.group(2)}"
        ),
        text,
    )
    text = _MONTH_YEAR_COMMA_RE.sub(r"\1 \2", text)
    return _normalize_full_date_commas(text)


def normalize_relative_dates(text: str, publication_date: date) -> str:
    """Apply context-dependent weekday and current-year rules.

    A contradictory written weekday is left unchanged because the processor
    cannot know whether the weekday or numeric date is the reporting error.
    """
    if not text:
        return text

    def replace(match: re.Match[str]) -> str:
        weekday, month_token, day_text, year_text, trailing_comma = match.groups()
        trailing_comma = trailing_comma or ""
        if not weekday and not year_text:
            return match.group(0)

        month_number = MONTH_TO_NUMBER[month_token]
        day_number = int(day_text)
        if year_text:
            try:
                resolved = date(int(year_text), month_number, day_number)
            except ValueError:
                return match.group(0)
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
                return match.group(0)
            resolved = min(
                candidates,
                key=lambda candidate: abs((candidate - publication_date).days),
            )

        is_current_year = resolved.year == publication_date.year
        if weekday:
            if weekday != resolved.strftime("%A"):
                return match.group(0)
            if year_text and not is_current_year:
                return f"{month_token} {day_text}, {year_text}{trailing_comma}"
            if abs((resolved - publication_date).days) < 7:
                return weekday
            if year_text and is_current_year:
                return f"{month_token} {day_text}"
            return f"{month_token} {day_text}{trailing_comma}"

        if is_current_year:
            return f"{month_token} {day_text}"
        return match.group(0)

    return _RELATIVE_DATE_RE.sub(replace, text)


def apply_date_rules(text: str, publication_date: date | None = None) -> str:
    """Normalize eligible date text while preserving protected regions.

    ``publication_date`` is required for current-year and weekday-window
    changes. Omitting it still permits fixed display normalization.
    """
    text = transform_unprotected(text, normalize_date_display)
    if publication_date is not None:
        text = transform_unprotected(
            text,
            lambda chunk: normalize_relative_dates(chunk, publication_date),
        )
    return text
