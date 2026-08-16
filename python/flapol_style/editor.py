"""Public product-neutral Florida Politics editing pipeline."""

from __future__ import annotations

from datetime import date

from .capitalization import (
    apply_capitalization_rules_to_session,
    capitalization_flags_for_session,
)
from .dates import apply_date_rules_to_session
from .mechanics import apply_mechanical_rules_to_session
from .reporting import EditingSession, EditResult
from .titles import apply_title_rules_to_session
from .words import apply_word_rules_to_session


def apply_main_style_with_report(
    text: str, publication_date: date | None = None
) -> EditResult:
    """Apply automatic main rules and return explainable edits and findings."""
    session = EditingSession(text)
    apply_word_rules_to_session(session)
    apply_title_rules_to_session(session)
    apply_capitalization_rules_to_session(session)
    apply_mechanical_rules_to_session(session)
    apply_date_rules_to_session(session, publication_date)
    findings = capitalization_flags_for_session(session)
    return session.result(findings)


def apply_main_style(text: str, publication_date: date | None = None) -> str:
    """Apply implemented automatic main-guide rules in a stable order.

    This entry point includes only rules classified as safe automatic fixes.
    Flags and editor-only guidance are deliberately absent.
    """
    return apply_main_style_with_report(text, publication_date).text
