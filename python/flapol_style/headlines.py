"""Explicit headline-only Florida Politics rules."""

from __future__ import annotations

import re

from .reporting import EditingSession, EditResult, RuleSpec


_US_HEADLINE_RE = re.compile(r"\bUS\b")
_US_HEADLINE_RULE = RuleSpec(
    "flapol.headlines.us-periods",
    "Florida Politics main headline override",
)


def apply_headline_rules_to_session(session: EditingSession) -> None:
    session.replace_pattern(_US_HEADLINE_RULE, _US_HEADLINE_RE, "U.S.")


def apply_headline_style_with_report(text: str) -> EditResult:
    """Apply only explicitly implemented headline-profile rules."""
    session = EditingSession(text)
    apply_headline_rules_to_session(session)
    return session.result()


def apply_headline_style(text: str) -> str:
    """Apply only explicitly implemented headline-profile rules."""
    return apply_headline_style_with_report(text).text
