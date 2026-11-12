"""Narrow narrative usage rules and review-only findings."""

from __future__ import annotations

import re

from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec


_AUTHORITY = "Florida Politics owner ruling 2026-11-11"
_NO_PARTY_RE = re.compile(
    r"(?<![\w-])(?P<prefix>no[- ]party[- ]affiliation)[ \t]+"
    r"(?P<noun>voters?|members?)(?![\w-])", re.IGNORECASE
)
_THIRD_AND_NO_PARTY_RE = re.compile(
    r"(?<![\w-])(?P<third>[Tt]hird)-party[ \t]+and[ \t]+"
    r"no[- ]party(?:[- ]affiliation)?[ \t]+voters\b"
)
_NPA_RE = re.compile(r"\bNPAs?\b(?=[ \t]+(?i:voters?|members?|candidates?)\b)")
_NO_PARTY_ANTECEDENT_RE = re.compile(r"\bno-party\s+(?:voters?|members?)\b", re.I)
_CORPORATE_SUFFIX_RE = re.compile(
    r"\b(?:[A-Z][A-Za-z0-9’'&-]+|[a-z]+[A-Z][A-Za-z0-9’'&-]*)"
    r",?[ \t]+(?P<suffix>Inc\.|LLC|L\.L\.C\.)"
    r"(?![\w.])"
)
_INTERVENER_RE = re.compile(r"\binterveners?\b", re.IGNORECASE)
_LEGAL_CUE_RE = re.compile(r"\b(?:court|lawsuit|litigation|motion|petition|status)\b", re.I)
_CITY_OF_RE = re.compile(r"\bCity of(?=[ \t]+[A-Z][A-Za-z’'-]+\b)")
_VOTE_TALLY_RE = re.compile(
    r"\bvoted[ \t]+(?P<first>\d{1,2})[-–](?P<second>\d{1,2})[ \t]+against\b", re.I
)
_STREET_TOKEN = r"(?:[A-Z][A-Za-zÀ-ÖØ-öø-ÿ’'.-]*|\d{1,3}(?:st|nd|rd|th)|de|la|del|of|the)"
_ADDRESS_RE = re.compile(
    rf"(?<![\w$#.,-])\d{{1,6}}[A-Za-z]?[ \t]+"
    rf"{_STREET_TOKEN}(?:[ \t]+{_STREET_TOKEN}){{0,6}}[ \t]+"
    r"(?P<kind>Avenue|Boulevard|Street)(?![\w-])\.?"
)
_ADDRESS_FORMS = {"Avenue": "Ave.", "Boulevard": "Blvd.", "Street": "St."}
_ADDRESS_COUNT_PREFIX_RE = re.compile(
    r"\b(?:than|about|approximately|nearly|over|under|some|at least|at most)\s*$", re.I
)
_ADDRESS_NONLOCATION_SUFFIX_RE = re.compile(
    r"^[ \t]+(?:businesses|stores|shops|residents|properties|homes|voters|"
    r"Survey|Program|Association|Initiative|Plan|Project|Fund|Company|LLC|Inc\.)\b"
)


def _address_replacement(match: re.Match[str], text: str) -> str | None:
    if (_ADDRESS_COUNT_PREFIX_RE.search(text[max(0, match.start() - 25):match.start()])
            or _ADDRESS_NONLOCATION_SUFFIX_RE.match(text[match.end():])):
        return None
    return (match.group(0)[:match.start("kind") - match.start()]
            + _ADDRESS_FORMS[match.group("kind")])


def apply_usage_rules_to_session(session: EditingSession) -> None:
    def no_party(match: re.Match[str], _text: str) -> str | None:
        # A title-cased noun can be part of a formal document name.
        if match.group("noun")[0].isupper():
            return None
        prefix = "No-party" if match.group("prefix")[0].isupper() else "no-party"
        return f"{prefix} {match.group('noun')}"

    session.replace_pattern(
        RuleSpec("flapol.usage.third-and-no-party-voters", _AUTHORITY),
        _THIRD_AND_NO_PARTY_RE,
        lambda match, _text: f"{match.group('third')}- and no-party voters",
    )
    session.replace_pattern(
        RuleSpec("flapol.usage.no-party-voter-member", _AUTHORITY),
        _NO_PARTY_RE, no_party,
    )
    session.replace_pattern(
        RuleSpec("ap.addresses.numbered-street-type",
                 "AP addresses; Florida Politics owner confirmation 2026-11-11"),
        _ADDRESS_RE,
        _address_replacement,
    )


def usage_flags_for_session(session: EditingSession) -> tuple[Finding, ...]:
    text = session.text
    protected = find_protected_spans(text)

    def visible(start: int, end: int) -> bool:
        return not any(start < span.end and span.start < end for span in protected)

    findings: list[Finding] = []

    def flag(rule_id: str, start: int, end: int, suggestion: str) -> None:
        source_start, source_end = session.source_span(start, end)
        findings.append(Finding(
            rule_id, "FLAG", text[start:end], suggestion,
            source_start, source_end, "warning", _AUTHORITY,
        ))

    antecedents = [m for m in _NO_PARTY_ANTECEDENT_RE.finditer(text)
                   if visible(m.start(), m.end())]
    for match in _NPA_RE.finditer(text):
        if visible(match.start(), match.end()):
            if not any(prior.end() <= match.start() for prior in antecedents):
                flag("flapol.usage.npa-first-reference", match.start(), match.end(),
                     "Use no-party on first reference, unless a writer override applies")
            break
    for match in _CORPORATE_SUFFIX_RE.finditer(text):
        start, end = match.span("suffix")
        if (match.group(0).split()[0] not in {"A", "An", "The", "Any", "Each"}
                and visible(match.start(), match.end())):
            flag("flapol.usage.corporate-designator", start, end,
                 "Omit unless needed to distinguish the legal entity")
    for match in _INTERVENER_RE.finditer(text):
        if not visible(match.start(), match.end()):
            continue
        sentence_start = max(text.rfind(".", 0, match.start()),
                             text.rfind("\n", 0, match.start())) + 1
        sentence_end = text.find(".", match.end())
        sentence = text[sentence_start:sentence_end if sentence_end >= 0 else len(text)]
        if _LEGAL_CUE_RE.search(sentence):
            suggestion = "intervenors" if match.group().lower().endswith("s") else "intervenor"
            if match.group()[0].isupper():
                suggestion = suggestion.capitalize()
            flag("flapol.usage.intervenor-legal-form", match.start(), match.end(),
                 suggestion)
    for match in _CITY_OF_RE.finditer(text):
        prefix = text[:match.start()].rstrip()
        if visible(match.start(), match.end()) and prefix and prefix[-1] not in ".!?\n":
            flag("flapol.usage.city-of-capitalization", match.start(), match.end(),
                 "city of in narration; retain a verified formal name")
    for match in _VOTE_TALLY_RE.finditer(text):
        if (visible(match.start(), match.end())
                and int(match.group("first")) < int(match.group("second"))):
            flag("flapol.usage.vote-tally-order", match.start(), match.end(),
                 "Confirm the outcome and report the winning side first")
    return tuple(findings)
