"""Identity-backed Florida Politics legislator title conventions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Iterable

from .officeholders import load_officeholder_group
from .protected import find_protected_spans
from .reporting import EditingSession, Finding, RuleSpec
from .titles import FULL_NAME_DISPLAY_PATTERN


_AUTHORITY = "Florida Politics owner ruling 2026-10-02"
_SINGULAR_RULE = RuleSpec(
    "flapol.legislators.jurisdiction-before-name",
    _AUTHORITY,
    speech_preserving=False,
)
_PLURAL_RULE = RuleSpec(
    "flapol.legislators.jurisdiction-plural",
    _AUTHORITY,
    speech_preserving=False,
)
_IDENTITY_ABBREVIATION_RULE = RuleSpec(
    "flapol.legislators.identity-backed-title-abbreviation",
    "Florida Politics owner ruling 2026-10-07",
    speech_preserving=True,
)
_IDENTITY_PLURAL_ABBREVIATION_RULE = RuleSpec(
    "flapol.legislators.identity-backed-plural-title-abbreviation",
    "Florida Politics owner ruling 2026-10-07",
    speech_preserving=True,
)
_ATTRIBUTION_RULE = RuleSpec(
    "flapol.legislators.jurisdiction-attribution",
    _AUTHORITY,
    speech_preserving=False,
)

_SINGULAR_TITLE = r"(?:Representative|Rep\.|Senator|Sen\.)"
_PLURAL_TITLE = r"(?:Representatives|Reps\.|Senators|Sens\.)"
_JURISDICTION = r"(?:(?:Florida|U\.S\.|state)\s+)?"
_GENERIC_SINGULAR_TITLE = r"(?i:Representative|Rep\.|Senator|Sen\.)"
_GENERIC_PLURAL_TITLE = r"(?i:Representatives|Reps\.|Senators|Sens\.)"
_GENERIC_JURISDICTION = r"(?:(?i:Florida|U\.S\.|state)\s+)?"
_GENERIC_SINGULAR_RE = re.compile(
    rf"(?<![\w.])(?P<prefix>"
    rf"{_GENERIC_JURISDICTION}{_GENERIC_SINGULAR_TITLE})"
    rf"(?=\s+(?P<name>{FULL_NAME_DISPLAY_PATTERN})(?:\b|(?<=\*\*)))"
)
_GENERIC_NAME_LIST = (
    rf"{FULL_NAME_DISPLAY_PATTERN}"
    rf"(?:\s*,\s*{FULL_NAME_DISPLAY_PATTERN})*"
    rf"(?:\s*,?\s+and\s+{FULL_NAME_DISPLAY_PATTERN})"
)
_GENERIC_PLURAL_RE = re.compile(
    rf"(?<![\w.])(?P<prefix>"
    rf"{_GENERIC_JURISDICTION}{_GENERIC_PLURAL_TITLE})"
    rf"(?=\s+(?P<names>{_GENERIC_NAME_LIST}))"
)
_ATTRIBUTION_RE = re.compile(
    rf"(?<![\w])(?P<article>the\s+)"
    rf"(?P<prefix>{_JURISDICTION}{_SINGULAR_TITLE})"
    rf"(?=\s+said\b)",
    re.IGNORECASE,
)
_SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
_HISTORICAL_MODIFIER_RE = re.compile(
    r"(?i)(?:\bformer\s+|\bthen(?:-|\s+))$"
)
_HISTORICAL_MENTION_RE = re.compile(
    rf"(?i)(?:\bformer\s+|\bthen(?:-|\s+))"
    rf"{_JURISDICTION}{_SINGULAR_TITLE}\s+$"
)


@dataclass(frozen=True)
class LegislatorIdentity:
    """One caller-supplied legislator identity or alias overlay."""

    name: str
    level: str
    chamber: str
    aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("legislator name must not be empty")
        if self.level not in {"state", "federal"}:
            raise ValueError("legislator level must be 'state' or 'federal'")
        if self.chamber not in {"house", "senate"}:
            raise ValueError("legislator chamber must be 'house' or 'senate'")
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(
            self,
            "aliases",
            tuple(alias.strip() for alias in self.aliases if alias.strip()),
        )


@dataclass(frozen=True)
class LegislatorContext:
    """Resolved identities and state/federal mode for one document."""

    mode: str
    identities: tuple[LegislatorIdentity, ...]


def _normalized_name(value: str) -> str:
    return " ".join(value.replace("**", "").split()).casefold()


def _token_kind(token: str) -> str:
    bare = token.strip(".,").casefold()
    if bare in _SUFFIXES:
        return "suffix"
    if len(bare) == 1:
        return "initial"
    return "word"


def _conservative_name_variants(identity: LegislatorIdentity) -> tuple[str, ...]:
    variants = {identity.name, *identity.aliases}
    for value in tuple(variants):
        tokens = value.split()
        if len(tokens) < 3:
            continue

        without_suffix = list(tokens)
        if _token_kind(without_suffix[-1]) == "suffix":
            without_suffix.pop()
            variants.add(" ".join(without_suffix))

        interior = tokens[1:-1]
        if interior and all(
            _token_kind(token) in {"initial", "suffix"}
            for token in interior
        ):
            variants.add(f"{tokens[0]} {tokens[-1]}")

    return tuple(sorted(variants, key=lambda value: (-len(value), value)))


def _regex_name(value: str) -> str:
    return r"\s+".join(re.escape(token) for token in value.split())


class _IdentityResolver:
    def __init__(self, identities: Iterable[LegislatorIdentity]):
        by_variant: dict[str, dict[tuple[str, str, str], LegislatorIdentity]] = {}
        for identity in identities:
            identity_key = (identity.name, identity.level, identity.chamber)
            for variant in _conservative_name_variants(identity):
                by_variant.setdefault(_normalized_name(variant), {})[
                    identity_key
                ] = identity

        self._by_variant = {
            variant: tuple(records.values())
            for variant, records in by_variant.items()
        }
        variants = sorted(
            (variant for variant in self._by_variant if variant),
            key=lambda value: (-len(value), value),
        )
        if not variants:
            raise ValueError("legislator identity context must not be empty")
        alternatives = "|".join(_regex_name(variant) for variant in variants)
        self.name_pattern = rf"(?:{alternatives})"
        self.name_re = re.compile(
            rf"(?<![\w])(?P<name>{self.name_pattern})(?![\w])",
            re.IGNORECASE,
        )

    def lookup(self, value: str) -> tuple[LegislatorIdentity, ...]:
        return self._by_variant.get(_normalized_name(value), ())

    def mentions(self, text: str) -> tuple[LegislatorIdentity, ...]:
        hard_protected = find_protected_spans(
            text, allow_balanced_quotations=True
        )
        found: dict[tuple[str, str, str], LegislatorIdentity] = {}
        for match in self.name_re.finditer(text):
            if _overlaps(match.start(), match.end(), hard_protected):
                continue
            if _HISTORICAL_MENTION_RE.search(
                text[max(0, match.start() - 64):match.start()]
            ):
                continue
            records = self.lookup(match.group("name"))
            if len(records) != 1:
                continue
            identity = records[0]
            found[(identity.name, identity.level, identity.chamber)] = identity
        return tuple(found.values())


def _overlaps(start: int, end: int, spans: Iterable[object]) -> bool:
    return any(start < span.end and span.start < end for span in spans)


def _has_historical_modifier(text: str, start: int) -> bool:
    return bool(_HISTORICAL_MODIFIER_RE.search(text[max(0, start - 24):start]))


def _load_identities(
    as_of: date,
    overlays: Iterable[LegislatorIdentity],
) -> tuple[LegislatorIdentity, ...]:
    if type(as_of) is not date:
        raise TypeError("as_of must be an explicit datetime.date")

    identities: list[LegislatorIdentity] = []
    for group_id in (
        "florida-congressional-delegation",
        "florida-state-legislature",
    ):
        group = load_officeholder_group(group_id, as_of=as_of)
        for entry in group["entries"]:
            identities.append(
                LegislatorIdentity(
                    name=entry["name"],
                    aliases=tuple(entry.get("aliases", ())),
                    level=entry["level"],
                    chamber=entry["chamber"],
                )
            )

    for overlay in overlays:
        if not isinstance(overlay, LegislatorIdentity):
            raise TypeError("legislator overlays must be LegislatorIdentity values")
        identities.append(overlay)
    return tuple(identities)


def resolve_legislator_context(
    text: str,
    *,
    as_of: date,
    overlays: Iterable[LegislatorIdentity] = (),
) -> LegislatorContext:
    """Resolve current lawmakers and the document's legislative level mode."""
    resolver = _IdentityResolver(_load_identities(as_of, overlays))
    identities = resolver.mentions(text)
    levels = {identity.level for identity in identities}
    if levels == {"state"}:
        mode = "state-only"
    elif levels == {"federal"}:
        mode = "federal-only"
    elif levels == {"state", "federal"}:
        mode = "mixed"
    else:
        mode = "unresolved"
    return LegislatorContext(mode=mode, identities=identities)


def _chamber_from_title(title: str) -> str:
    normalized = title.casefold()
    return "house" if "rep" in normalized else "senate"


def _level_from_title(title: str) -> str | None:
    normalized = title.casefold()
    if "u.s." in normalized:
        return "federal"
    if "state" in normalized or "florida" in normalized:
        return "state"
    return None


def _looks_explicitly_legislative(title: str) -> bool:
    """Limit unresolved findings to forms that present themselves as titles."""
    normalized = title.casefold()
    if any(label in normalized for label in ("florida ", "u.s. ", "state ")):
        return True
    final_word = title.rsplit(maxsplit=1)[-1]
    return "." in final_word or final_word[:1].isupper()


def _singular_title(chamber: str) -> str:
    return "Rep." if chamber == "house" else "Sen."


def _plural_title(chamber: str) -> str:
    return "Reps." if chamber == "house" else "Sens."


def _long_title(chamber: str) -> str:
    return "Representative" if chamber == "house" else "Senator"


def _singular_target(identity: LegislatorIdentity, mode: str) -> str:
    title = _singular_title(identity.chamber)
    if identity.level == "federal":
        return f"U.S. {title}"
    if mode == "mixed":
        return f"state {title}"
    return title


def _plural_target(level: str, chamber: str, mode: str) -> str:
    title = _plural_title(chamber)
    if level == "federal":
        return f"U.S. {title}"
    if mode == "mixed":
        return f"state {title}"
    return title


def _display_name(match: re.Match[str]) -> str:
    return match.group("name").replace("**", "")


def _finding(
    session: EditingSession,
    *,
    rule_id: str,
    start: int,
    end: int,
    suggestion: str,
) -> Finding:
    source_start, source_end = session.source_span(start, end)
    return Finding(
        rule_id=rule_id,
        action="FLAG",
        found=session.text[start:end],
        suggestion=suggestion,
        source_start=source_start,
        source_end=source_end,
        severity="warning",
        authority=_AUTHORITY,
    )


def _split_name_list(value: str) -> tuple[str, ...]:
    return tuple(
        part.strip().replace("**", "")
        for part in re.split(r"\s*,\s*|\s+and\s+", value, flags=re.IGNORECASE)
        if part.strip()
    )


def _collect_before_name_findings(
    session: EditingSession,
    resolver: _IdentityResolver,
) -> list[Finding]:
    protected = find_protected_spans(session.text)
    findings: list[Finding] = []

    for match in _GENERIC_SINGULAR_RE.finditer(session.text):
        end = match.end("name")
        if _overlaps(match.start(), end, protected):
            continue
        if _has_historical_modifier(session.text, match.start()):
            suggestion = (
                "Confirm the historical office and jurisdiction; the current "
                "officeholder book does not establish a former title."
            )
        else:
            records = resolver.lookup(_display_name(match))
            if len(records) != 1:
                if not _looks_explicitly_legislative(match.group("prefix")):
                    continue
                suggestion = (
                    "Confirm the lawmaker's level and chamber before choosing "
                    "Rep./Sen., U.S. Rep./Sen. or state Rep./Sen."
                )
            elif records[0].chamber != _chamber_from_title(match.group("prefix")):
                suggestion = (
                    f"Confirm the title; the current roster identifies "
                    f"{records[0].name} as a {_long_title(records[0].chamber)}."
                )
            else:
                continue
        findings.append(
            _finding(
                session,
                rule_id=_SINGULAR_RULE.rule_id,
                start=match.start(),
                end=end,
                suggestion=suggestion,
            )
        )

    for match in _GENERIC_PLURAL_RE.finditer(session.text):
        end = match.end("names")
        if _overlaps(match.start(), end, protected):
            continue
        if _has_historical_modifier(session.text, match.start()):
            suggestion = (
                "Confirm the historical offices and jurisdictions before "
                "normalizing this shared plural title."
            )
        else:
            records: list[LegislatorIdentity] = []
            unresolved = False
            for name in _split_name_list(match.group("names")):
                matches = resolver.lookup(name)
                if len(matches) != 1:
                    unresolved = True
                    break
                records.append(matches[0])
            expected_chamber = _chamber_from_title(match.group("prefix"))
            same_scope = (
                records
                and len({record.level for record in records}) == 1
                and {record.chamber for record in records} == {expected_chamber}
            )
            if not unresolved and same_scope:
                continue
            if unresolved and not _looks_explicitly_legislative(
                match.group("prefix")
            ):
                continue
            suggestion = (
                "Use a shared plural title only when every named lawmaker "
                "resolves to the same legislative level and chamber."
            )
        findings.append(
            _finding(
                session,
                rule_id=_PLURAL_RULE.rule_id,
                start=match.start(),
                end=end,
                suggestion=suggestion,
            )
        )

    return findings


def _collect_attribution_findings(
    session: EditingSession,
    mode: str,
) -> list[Finding]:
    if mode in {"state-only", "federal-only"}:
        return []
    protected = find_protected_spans(session.text)
    findings: list[Finding] = []
    for match in _ATTRIBUTION_RE.finditer(session.text):
        if _overlaps(match.start(), match.end(), protected):
            continue
        if mode == "mixed" and _level_from_title(match.group("prefix")):
            continue
        findings.append(
            _finding(
                session,
                rule_id=_ATTRIBUTION_RULE.rule_id,
                start=match.start(),
                end=match.end(),
                suggestion=(
                    "Identify the speaker as state or U.S. before normalizing "
                    "the attribution title."
                ),
            )
        )
    return findings


def apply_legislator_rules_to_session(
    session: EditingSession,
    *,
    as_of: date,
    overlays: Iterable[LegislatorIdentity] = (),
) -> tuple[Finding, ...]:
    """Apply identity-proven title forms and return unresolved findings."""
    resolver = _IdentityResolver(_load_identities(as_of, overlays))
    identities = resolver.mentions(session.text)
    levels = {identity.level for identity in identities}
    if levels == {"state"}:
        mode = "state-only"
    elif levels == {"federal"}:
        mode = "federal-only"
    elif levels == {"state", "federal"}:
        mode = "mixed"
    else:
        mode = "unresolved"

    findings = [
        *_collect_before_name_findings(session, resolver),
        *_collect_attribution_findings(session, mode),
    ]

    name_display = (
        rf"(?:\*\*(?:{resolver.name_pattern})\*\*|"
        rf"(?:{resolver.name_pattern}))"
    )
    singular_pattern = re.compile(
        rf"(?<![\w.])(?P<prefix>{_JURISDICTION}{_SINGULAR_TITLE})"
        rf"(?=\s+(?P<name>{name_display})(?![\w]))",
        re.IGNORECASE,
    )

    def singular_replacement(match: re.Match[str], _text: str) -> str | None:
        if _has_historical_modifier(_text, match.start()):
            return None
        records = resolver.lookup(_display_name(match))
        if len(records) != 1:
            return None
        identity = records[0]
        if identity.chamber != _chamber_from_title(match.group("prefix")):
            return None
        return _singular_target(identity, mode)

    session.replace_pattern(
        _SINGULAR_RULE,
        singular_pattern,
        singular_replacement,
    )

    name_list = (
        rf"{name_display}(?:\s*,\s*{name_display})*"
        rf"(?:\s*,?\s+and\s+{name_display})"
    )
    plural_pattern = re.compile(
        rf"(?<![\w.])(?P<prefix>{_JURISDICTION}{_PLURAL_TITLE})"
        rf"(?=\s+(?P<names>{name_list}))",
        re.IGNORECASE,
    )

    def plural_replacement(match: re.Match[str], _text: str) -> str | None:
        if _has_historical_modifier(_text, match.start()):
            return None
        records: list[LegislatorIdentity] = []
        for name_match in resolver.name_re.finditer(match.group("names")):
            matches = resolver.lookup(name_match.group("name"))
            if len(matches) != 1:
                return None
            records.append(matches[0])
        expected_chamber = _chamber_from_title(match.group("prefix"))
        if (
            len(records) < 2
            or len({record.level for record in records}) != 1
            or {record.chamber for record in records} != {expected_chamber}
        ):
            return None
        return _plural_target(records[0].level, expected_chamber, mode)

    session.replace_pattern(
        _PLURAL_RULE,
        plural_pattern,
        plural_replacement,
    )

    identity_singular_pattern = re.compile(
        rf"(?<![\w.])(?P<jurisdiction>{_JURISDICTION})"
        rf"(?P<title>Representative|Senator)"
        rf"(?=\s+(?P<name>{name_display})(?![\w]))",
        re.IGNORECASE,
    )

    def identity_singular_abbreviation(
        match: re.Match[str], _text: str
    ) -> str | None:
        if _has_historical_modifier(_text, match.start()):
            return None
        records = resolver.lookup(_display_name(match))
        if len(records) != 1:
            return None
        identity = records[0]
        if identity.chamber != _chamber_from_title(match.group("title")):
            return None
        return f"{match.group('jurisdiction')}{_singular_title(identity.chamber)}"

    session.replace_pattern(
        _IDENTITY_ABBREVIATION_RULE,
        identity_singular_pattern,
        identity_singular_abbreviation,
    )

    identity_plural_pattern = re.compile(
        rf"(?<![\w.])(?P<jurisdiction>{_JURISDICTION})"
        rf"(?P<title>Representatives|Senators)"
        rf"(?=\s+(?P<names>{name_list}))",
        re.IGNORECASE,
    )

    def identity_plural_abbreviation(
        match: re.Match[str], _text: str
    ) -> str | None:
        if _has_historical_modifier(_text, match.start()):
            return None
        records: list[LegislatorIdentity] = []
        for name_match in resolver.name_re.finditer(match.group("names")):
            matches = resolver.lookup(name_match.group("name"))
            if len(matches) != 1:
                return None
            records.append(matches[0])
        expected_chamber = _chamber_from_title(match.group("title"))
        if (
            len(records) < 2
            or {record.chamber for record in records} != {expected_chamber}
        ):
            return None
        return (
            f"{match.group('jurisdiction')}"
            f"{_plural_title(expected_chamber)}"
        )

    session.replace_pattern(
        _IDENTITY_PLURAL_ABBREVIATION_RULE,
        identity_plural_pattern,
        identity_plural_abbreviation,
    )

    def attribution_replacement(
        match: re.Match[str], _text: str
    ) -> str | None:
        level: str | None
        if mode == "state-only":
            level = "state"
        elif mode == "federal-only":
            level = "federal"
        elif mode == "mixed":
            level = _level_from_title(match.group("prefix"))
        else:
            return None
        if level is None:
            return None
        chamber = _chamber_from_title(match.group("prefix"))
        title = _long_title(chamber)
        if level == "federal":
            title = f"U.S. {title}"
        elif mode == "mixed":
            title = f"state {title}"
        return f"the {title}"

    session.replace_pattern(
        _ATTRIBUTION_RULE,
        _ATTRIBUTION_RE,
        attribution_replacement,
    )

    return tuple(findings)
