"""Conservative title abbreviations before recognized name-shaped text."""

from __future__ import annotations

import json
from pathlib import Path
import re

from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec


_DATA_PATH = Path(__file__).with_name("data") / "title_abbreviations.json"
_AGRICULTURE_COMMISSIONER_ORDER_RULE = RuleSpec(
    "flapol.titles.agriculture-commissioner-order",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=False,
)
_AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE = RuleSpec(
    "flapol.titles.agriculture-commissioner-capitalization",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=True,
)
_FLORIDA_GOVERNOR_HOME_STATE_RULE = RuleSpec(
    "flapol.titles.florida-governor-home-state",
    "Florida Politics owner ruling 2026-10-02",
    speech_preserving=False,
)
_COMMISSIONER_OF_AGRICULTURE_RE = re.compile(
    r"(?<![\w])(?i:Commissioner\s+of\s+Agriculture)"
    r"(?!(?i:\s+and\s+Consumer\s+Services\b))(?![\w])"
)
_AGRICULTURE_COMMISSIONER_RE = re.compile(
    r"(?<![\w])(?i:Agriculture\s+Commissioner)(?![\w])"
)
NAME_TOKEN_PATTERN = r"(?:[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|[A-Z]\.)"
FULL_NAME_PATTERN = (
    rf"{NAME_TOKEN_PATTERN}"
    rf"(?:\s+(?:[A-Z]\.?\s+)?{NAME_TOKEN_PATTERN})+"
)
FULL_NAME_DISPLAY_PATTERN = (
    rf"(?:{FULL_NAME_PATTERN}|\*\*{FULL_NAME_PATTERN}\*\*)"
)
_FLORIDA_GOVERNOR_BEFORE_NAME_RE = re.compile(
    rf"(?<![\w])(?i:Florida)\s+"
    rf"(?=(?i:Governor|Gov\.)\s+{FULL_NAME_DISPLAY_PATTERN}"
    rf"(?:\b|(?<=\*\*)))"
)
_FLORIDA_GOVERNOR_WITHOUT_NAME_RE = re.compile(
    r"(?<![\w])(?i:Florida\s+)(?P<title>(?i:Governor|Gov\.))(?![\w])"
)
_GOVERNORS_MANSION_SUFFIX_RE = re.compile(
    r"^['’]s\s+Mansion\b",
    re.IGNORECASE,
)


def load_title_abbreviations() -> tuple[dict[str, str], ...]:
    """Load the public before-name title registry."""
    with _DATA_PATH.open(encoding="utf-8") as source:
        records = json.load(source)
    return tuple(records)


def _compile_rules() -> tuple[tuple[re.Pattern[str], dict[str, str]], ...]:
    rules: list[tuple[re.Pattern[str], dict[str, str]]] = []
    for record in sorted(load_title_abbreviations(),
                         key=lambda item: len(item["from"]), reverse=True):
        title = record["from"]
        rules.append(
            (
                re.compile(
                    rf"(?<![\w.\-])(?i:{re.escape(title)})"
                    rf"(?=\s+{FULL_NAME_DISPLAY_PATTERN}(?:\b|(?<=\*\*)))",
                ),
                record,
            )
        )
    return tuple(rules)


_ABBREVIATION_RULES = _compile_rules()

_CIVILIAN_GENERAL_PREFIX_RE = re.compile(
    r"\b(?:Attorney|Solicitor|Inspector|Surgeon|Postmaster|Secretary|"
    r"Director|Consul|Adjutant)[ -]+$", re.IGNORECASE
)
_NONPERSON_NAME_RE = re.compile(
    r"^(?:Assembly|Counsel|Dynamics|Electric|Election|General|Hospital|"
    r"League|Magistrate|Manager|Secretary|Conference|Motors|Services|Store|Street|Avenue|Boulevard|Road|Court|"
    r"Drive|Trial|Order)\b", re.IGNORECASE
)
_ENTITY_HEADS = frozenset({
    "academy", "institute", "institution", "university", "college", "school",
    "award", "medal", "prize", "program", "programme", "scholarship", "act",
    "fund", "trust", "foundation", "endowment", "association", "society", "coalition", "declaration",
    "council", "commission", "committee", "subcommittee", "authority", "agency",
    "department", "division", "bureau", "museum", "memorial", "library",
    "building", "bridge", "highway", "trail", "hall", "park", "center", "centre", "hospital",
    "street", "avenue", "boulevard", "road", "airport", "stadium", "arena", "campus", "courthouse",
    "company", "corporation", "corp", "inc", "llc", "group", "partners",
    "holdings", "management", "services", "solutions", "rum", "whiskey",
    "vodka", "spirits", "bonds", "rights",
})
_AMBIGUOUS_ENTITY_HEADS = frozenset({"hall", "park", "center", "centre"})
_ENTITY_CLAUSE_BOUNDARIES = frozenset({
    "said", "says", "spoke", "told", "testified", "met", "served", "serves",
    "received", "receives", "announced", "announces", "will", "would", "has",
    "had", "is", "was", "who", "whose", "and", "or", "with", "at", "from",
    "for", "to", "in", "on", "of", "about", "a", "an", "the",
})
_ENTITY_WORD_RE = re.compile(r"[^\W\d_][\w’'\-]*", re.UNICODE)
_UNIFORMED_CONTEXT_RE = re.compile(
    r"\b(?:Army|Navy|Air Force|Marine Corps|Marines?|Coast Guard|Space Force|"
    r"Police(?: Department)?|Fire(?: Department)?|FHP|Florida Highway Patrol|"
    r"Sheriff['’]s Office)(?:[ \t\r\n]+(?:Reserve|veteran|attorney|retired))*[ \t\r\n]+$",
    re.IGNORECASE,
)
_CIVILIAN_SPECIALIST_RE = re.compile(
    r"\b(?:finance|financial|healthcare|marketing|communications|media|technical|"
    r"medical|education|information technology)[ \t]+$", re.IGNORECASE
)
_NONLEGISLATIVE_REPRESENTATIVE_RE = re.compile(
    r"\b(?:applicant|company|corporate|firm|union|client|customer|sales|legal|"
    r"campaign|media|press|marketing|business|association|agency)\s+"
    r"(?:(?:U\.S\.|Florida|state)\s+)?(?:representatives?|reps\.)\s*$",
    re.IGNORECASE,
)


def nonlegislative_representative_at(text: str, name_start: int) -> bool:
    prefix = text[max(0, name_start - 100):name_start].rstrip().removesuffix("**").rstrip()
    return bool(_NONLEGISLATIVE_REPRESENTATIVE_RE.search(prefix))


def named_entity_phrase_at(text: str, start: int, *, name_words: int = 0) -> bool:
    """Recognize a bounded noun phrase, including mixed-case official names.

    Stop before a new clause: a person who spoke about a program is not the
    program. This protects all title families, not an ever-growing name list.
    """
    tail = text[start:]
    previous_end = 0
    previous_word = ""
    for index, word in enumerate(_ENTITY_WORD_RE.finditer(tail)):
        if index >= 20:
            return True  # An overlong unresolved noun phrase fails closed.
        gap = tail[previous_end:word.start()].replace("**", "")
        token = word.group().casefold()
        head = token
        if head not in _ENTITY_HEADS and head.endswith("ies"):
            head = head[:-3] + "y"
        elif head not in _ENTITY_HEADS and head.endswith("s"):
            head = head[:-1]
        if re.search(r"\n[ \t\r]*\n", gap):
            break
        if gap.strip():
            initial_period = gap.strip() == "." and len(previous_word) == 1
            suffix_punctuation = (set(gap.strip()) <= {",", "."}
                                  and (token in {"jr", "sr"}
                                       or previous_word in {"jr", "sr"}))
            nickname_quotes = index >= 1 and set(gap.strip()) <= {'"', '“', '”'}
            if not initial_period and not suffix_punctuation and not nickname_quotes:
                break
        if index + name_words >= 2 and token in _ENTITY_CLAUSE_BOUNDARIES:
            break
        if head in _ENTITY_HEADS:
            if head not in _AMBIGUOUS_ENTITY_HEADS or index + name_words >= 2:
                return True
        previous_end = word.end()
        previous_word = token
    return False


def _named_entity_follows(match: re.Match[str], text: str) -> bool:
    return named_entity_phrase_at(text, match.end())


def _nonmilitary_use(match: re.Match[str], text: str,
                     record: dict[str, str]) -> bool:
    prefix = text[max(0, match.start() - 60):match.start()]
    if record["from"] == "General" and _CIVILIAN_GENERAL_PREFIX_RE.search(prefix):
        return True
    if record["from"] == "Specialist" and _CIVILIAN_SPECIALIST_RE.search(prefix):
        return True
    name = text[match.end():].lstrip().removeprefix("**")
    return bool(_NONPERSON_NAME_RE.match(name))


def _uniformed_context(match: re.Match[str], text: str) -> bool:
    # Capitalized name-shaped words do not prove a rank. Qualify this exact
    # occurrence; mentioning the Army elsewhere cannot authorize every match.
    context = _UNIFORMED_CONTEXT_RE.search(text[max(0, match.start() - 90):match.start()])
    return bool(context and not re.search(r"\n[ \t\r]*\n", context.group()))


def _title_replacement(match: re.Match[str], text: str,
                       record: dict[str, str]) -> str | None:
    if (_named_entity_follows(match, text)
            or nonlegislative_representative_at(text, match.end())):
        return None
    if record["class"] == "military":
        if _nonmilitary_use(match, text, record) or not _uniformed_context(match, text):
            return None
    return record["to"]


def military_title_flags_for_session(session: EditingSession) -> tuple[Finding, ...]:
    """Keep unqualified rank-like title candidates for review, not rewriting."""
    text = session.text
    protected = find_protected_spans(text)
    occupied: list[tuple[int, int]] = []
    findings: list[Finding] = []
    for pattern, record in _ABBREVIATION_RULES:
        if record["class"] != "military":
            continue
        for match in pattern.finditer(text):
            start, end = match.span()
            if any(start < right and left < end for left, right in occupied):
                continue
            occupied.append((start, end))
            if (match.group() == record["to"]
                    or any(start < span.end and span.start < end for span in protected)
                    or _named_entity_follows(match, text)
                    or _nonmilitary_use(match, text, record)
                    or _uniformed_context(match, text)):
                continue
            source_start, source_end = session.source_span(start, end)
            findings.append(Finding(
                "flapol.titles.military-context-required", "FLAG", match.group(),
                f"Confirm a uniformed-service title before using {record['to']}",
                source_start, source_end, "warning",
                "Florida Politics owner safety clarification 2026-11-12",
            ))
    return tuple(findings)


def apply_office_title_form_rules_to_session(session: EditingSession) -> None:
    """Apply house order and capitalization for office titles."""
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_ORDER_RULE,
        _COMMISSIONER_OF_AGRICULTURE_RE,
        "Agriculture Commissioner",
    )
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE,
        _AGRICULTURE_COMMISSIONER_RE,
        "Agriculture Commissioner",
    )
    session.replace_pattern(
        _AGRICULTURE_COMMISSIONER_CAPITALIZATION_RULE,
        _COMMISSIONER_OF_AGRICULTURE_RE,
        "Commissioner of Agriculture",
    )


def apply_home_state_title_rules_to_session(session: EditingSession) -> None:
    """Remove a redundant Florida label where the full title proves context."""
    session.replace_pattern(
        _FLORIDA_GOVERNOR_HOME_STATE_RULE,
        _FLORIDA_GOVERNOR_BEFORE_NAME_RE,
        "",
    )


def home_state_title_flags_for_session(
    session: EditingSession,
) -> tuple[Finding, ...]:
    """Flag unresolved Florida title labels that lack a full-name context."""
    text = session.text
    protected = find_protected_spans(text)
    findings: list[Finding] = []

    for match in _FLORIDA_GOVERNOR_WITHOUT_NAME_RE.finditer(text):
        if any(
            match.start() < span.end and span.start < match.end()
            for span in protected
        ):
            continue
        if _GOVERNORS_MANSION_SUFFIX_RE.match(text[match.end():]):
            continue
        source_start, source_end = session.source_span(
            match.start(), match.end()
        )
        title = match.group("title")
        suggestion = "Gov." if title.casefold() == "gov." else "Governor"
        findings.append(
            Finding(
                rule_id="flapol.titles.florida-governor-without-name",
                action="FLAG",
                found=match.group(0),
                suggestion=suggestion,
                source_start=source_start,
                source_end=source_end,
                severity="warning",
                authority="Florida Politics owner ruling 2026-10-02",
            )
        )

    return tuple(findings)


def apply_title_rules_to_session(session: EditingSession) -> None:
    apply_office_title_form_rules_to_session(session)
    apply_home_state_title_rules_to_session(session)
    for pattern, record in _ABBREVIATION_RULES:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.titles.{record['id']}",
                authority=record["authority"],
                speech_preserving=record["speech_preserving"],
            ),
            pattern,
            lambda match, text, item=record: _title_replacement(match, text, item),
        )


def abbreviate_titles_before_names(text: str) -> str:
    """Abbreviate approved titles only when they directly precede a full name."""
    session = EditingSession(text)
    for pattern, record in _ABBREVIATION_RULES:
        session.replace_pattern(
            RuleSpec(
                rule_id=f"flapol.titles.{record['id']}",
                authority=record["authority"],
                speech_preserving=record["speech_preserving"],
            ),
            pattern,
            lambda match, text, item=record: _title_replacement(match, text, item),
        )
    return session.text


def normalize_office_title_forms(text: str) -> str:
    """Apply deterministic Florida Politics office-title forms."""
    session = EditingSession(text)
    apply_office_title_form_rules_to_session(session)
    return session.text
