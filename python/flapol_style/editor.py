"""Public product-neutral Florida Politics editing pipeline."""

from __future__ import annotations

from datetime import date

from .dates import apply_date_rules
from .titles import abbreviate_titles_before_names
from .words import normalize_word_forms


def apply_main_style(text: str, publication_date: date | None = None) -> str:
    """Apply implemented automatic main-guide rules in a stable order.

    This entry point includes only rules classified as safe automatic fixes.
    Flags and editor-only guidance are deliberately absent.
    """
    text = normalize_word_forms(text)
    text = abbreviate_titles_before_names(text)
    return apply_date_rules(text, publication_date=publication_date)
