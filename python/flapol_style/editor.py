"""Public product-neutral Florida Politics editing pipeline."""

from __future__ import annotations

from datetime import date
from typing import Iterable

from .capitalization import (
    apply_capitalization_rules_to_session,
    capitalization_flags_for_session,
)
from .dates import apply_date_rules_to_session
from .legislators import LegislatorIdentity, apply_legislator_rules_to_session
from .mechanics import apply_mechanical_rules_to_session
from .numbers import (
    apply_number_sign_rules_to_session,
    number_sign_flags_for_session,
)
from .reporting import EditingSession, EditResult
from .titles import (
    apply_title_rules_to_session,
    home_state_title_flags_for_session,
)
from .words import apply_word_rules_to_session


def apply_main_style_with_report(
    text: str,
    publication_date: date | None = None,
    *,
    officeholder_as_of: date | None = None,
    legislator_overlays: Iterable[LegislatorIdentity] = (),
) -> EditResult:
    """Apply automatic main rules and return explainable edits and findings."""
    session = EditingSession(text)
    overlays = tuple(legislator_overlays)
    legislator_findings = ()
    if officeholder_as_of is not None:
        legislator_findings = apply_legislator_rules_to_session(
            session,
            as_of=officeholder_as_of,
            overlays=overlays,
        )
    elif overlays:
        raise ValueError(
            "officeholder_as_of is required when legislator_overlays are supplied"
        )
    apply_word_rules_to_session(session)
    apply_title_rules_to_session(session)
    apply_capitalization_rules_to_session(session)
    apply_mechanical_rules_to_session(session)
    apply_number_sign_rules_to_session(session)
    apply_date_rules_to_session(session, publication_date)
    findings = tuple(
        sorted(
            (
                *legislator_findings,
                *capitalization_flags_for_session(session),
                *home_state_title_flags_for_session(session),
                *number_sign_flags_for_session(session),
            ),
            key=lambda item: (item.start, item.end, item.rule_id),
        )
    )
    return session.result(findings)


def apply_main_style(
    text: str,
    publication_date: date | None = None,
    *,
    officeholder_as_of: date | None = None,
    legislator_overlays: Iterable[LegislatorIdentity] = (),
) -> str:
    """Apply implemented automatic main-guide rules in a stable order.

    This entry point includes only rules classified as safe automatic fixes.
    Flags and editor-only guidance are deliberately absent.
    """
    return apply_main_style_with_report(
        text,
        publication_date,
        officeholder_as_of=officeholder_as_of,
        legislator_overlays=legislator_overlays,
    ).text
