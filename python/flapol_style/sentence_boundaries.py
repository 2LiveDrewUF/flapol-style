"""Conservative sentence-boundary checks for body copy."""

import re


# Blank lines and standalone passage separators start fresh prose.
_PARAGRAPH_BOUNDARY_RE = re.compile(r"\n[ \t]*(?:\u2063[ \t]*)?\r?\n\s*\Z")
_AMBIGUOUS_PERIOD_RE = re.compile(
    r"\.{2,}$|\b(?:[a-z]\.)+$|"
    r"\b(?:mr|mrs|ms|mx|dr|prof|rev|hon|gov|lt|sen|sens|rep|reps|"
    r"st|mt|ft|capt|sgt|col|gen|jr|sr|no|vs|inc|ltd|co|etc)\.$",
    re.IGNORECASE,
)


def starts_body_sentence(text: str, start: int) -> bool | None:
    """Return None when punctuation could mark a continuation or a new sentence."""
    preceding = text[:start]
    if preceding.endswith(("**", "__")):
        preceding = preceding[:-2]
    if not preceding.strip() or _PARAGRAPH_BOUNDARY_RE.search(preceding):
        return True

    preceding = preceding.rstrip()
    closes_quote = preceding.endswith(('"', "”", "'", "’"))
    punctuation = preceding[:-1] if closes_quote else preceding
    if (
        _AMBIGUOUS_PERIOD_RE.search(punctuation)
        or punctuation.endswith("…")
        or (closes_quote and punctuation.endswith(("?", "!")))
    ):
        return None
    return punctuation.endswith((".", "!", "?"))
