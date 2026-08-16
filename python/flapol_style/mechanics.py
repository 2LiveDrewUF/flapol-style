"""Protected mechanical rules already established by Vale fixtures."""

from __future__ import annotations

import re

from .reporting import EditingSession, RuleSpec


_COVID_RE = re.compile(r"\bCOVID-19\b", re.IGNORECASE)
_PERCENT_RE = re.compile(
    r"(?<![\w.])(\d+(?:,\d{3})*(?:\.\d+)?)\s+(?:percent|per cent)\b",
    re.IGNORECASE,
)
_TIME_RE = re.compile(
    r"(?<![\w:])((?:0?[1-9]|1[0-2])(?::[0-5]\d)?)\s*"
    r"([ap])\.?m\.?(?=\s|[.,;:!?)\"]|$)",
    re.IGNORECASE,
)

_COVID_RULE = RuleSpec(
    "flapol.terms.covid-without-19",
    "Florida Politics main",
)
_PERCENT_RULE = RuleSpec(
    "ap.numbers.percent-symbol",
    "AP Stylebook 56th edition, percent entry",
)
_TIME_RULE = RuleSpec(
    "ap.times.meridiem-format",
    "AP Stylebook 56th edition, times entry",
)


def apply_mechanical_rules_to_session(session: EditingSession) -> None:
    session.replace_pattern(_COVID_RULE, _COVID_RE, "COVID")
    session.replace_pattern(_PERCENT_RULE, _PERCENT_RE, r"\1%")
    session.replace_pattern(
        _TIME_RULE,
        _TIME_RE,
        lambda match, _text: (
            f"{match.group(1)} {match.group(2).lower()}.m."
        ),
    )


def normalize_mechanical_forms(text: str) -> str:
    """Normalize protected COVID, percent and meridiem forms."""
    session = EditingSession(text)
    apply_mechanical_rules_to_session(session)
    return session.text
