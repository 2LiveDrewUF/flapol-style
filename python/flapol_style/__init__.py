"""Deterministic Florida Politics editing primitives.

The Vale package reports isolated textual violations. This Python package
handles transformations that require document context or protected-region
awareness. Public callers should use the narrow functions exported here
rather than depending on private regular expressions.
"""

from .dates import apply_date_rules, normalize_date_display, normalize_relative_dates
from .editor import apply_main_style
from .protected import ProtectedSpan, find_protected_spans, transform_unprotected
from .titles import abbreviate_titles_before_names, load_title_abbreviations
from .words import load_word_preferences, normalize_word_forms

__all__ = [
    "ProtectedSpan",
    "abbreviate_titles_before_names",
    "apply_main_style",
    "apply_date_rules",
    "find_protected_spans",
    "load_title_abbreviations",
    "load_word_preferences",
    "normalize_date_display",
    "normalize_relative_dates",
    "normalize_word_forms",
    "transform_unprotected",
]
