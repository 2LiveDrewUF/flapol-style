"""Deterministic Florida Politics editing primitives.

The Vale package reports isolated textual violations. This Python package
handles transformations that require document context or protected-region
awareness. Public callers should use the narrow functions exported here
rather than depending on private regular expressions.
"""

from .capitalization import (
    CapitalizationFinding,
    find_capitalization_flags,
    load_capitalization_rules,
    normalize_capitalization,
)
from .dates import apply_date_rules, normalize_date_display, normalize_relative_dates
from .editor import apply_main_style, apply_main_style_with_report
from .headlines import apply_headline_style, apply_headline_style_with_report
from .mechanics import normalize_mechanical_forms
from .protected import ProtectedSpan, find_protected_spans, transform_unprotected
from .reporting import Edit, EditingSession, EditResult, Finding, RuleSpec
from .titles import abbreviate_titles_before_names, load_title_abbreviations
from .words import load_word_preferences, normalize_word_forms

__version__ = "0.1.0a3"

__all__ = [
    "ProtectedSpan",
    "CapitalizationFinding",
    "Edit",
    "EditingSession",
    "EditResult",
    "Finding",
    "abbreviate_titles_before_names",
    "apply_main_style",
    "apply_main_style_with_report",
    "apply_headline_style",
    "apply_headline_style_with_report",
    "apply_date_rules",
    "find_protected_spans",
    "find_capitalization_flags",
    "load_capitalization_rules",
    "load_title_abbreviations",
    "load_word_preferences",
    "normalize_date_display",
    "normalize_capitalization",
    "normalize_relative_dates",
    "normalize_mechanical_forms",
    "normalize_word_forms",
    "RuleSpec",
    "transform_unprotected",
    "__version__",
]
