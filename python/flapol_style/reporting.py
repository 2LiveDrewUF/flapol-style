"""Structured, source-coordinate-aware edit reporting."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import re
from typing import Callable

from .protected import find_protected_spans


@dataclass(frozen=True)
class RuleSpec:
    rule_id: str
    authority: str
    action: str = "AUTO_FIX"
    severity: str = "error"


@dataclass(frozen=True)
class Replacement:
    text: str
    rule: RuleSpec | None = None


@dataclass(frozen=True)
class Edit:
    sequence: int
    rule_id: str
    action: str
    before: str
    after: str
    source_start: int
    source_end: int
    working_start: int
    working_end: int
    severity: str
    authority: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    action: str
    found: str
    suggestion: str
    source_start: int
    source_end: int
    severity: str
    authority: str

    @property
    def start(self) -> int:
        """Backward-compatible alias for the original-source start offset."""
        return self.source_start

    @property
    def end(self) -> int:
        """Backward-compatible alias for the original-source end offset."""
        return self.source_end


@dataclass(frozen=True)
class EditResult:
    text: str
    changes: tuple[Edit, ...]
    findings: tuple[Finding, ...] = ()


ReplacementValue = str | Replacement | None
ReplacementFunction = Callable[[re.Match[str], str], ReplacementValue]


class EditingSession:
    """Track transformations while retaining offsets into the original input."""

    def __init__(self, text: str):
        self.source_text = text
        self.text = text
        self._source_boundaries = list(range(len(text) + 1))
        self._changes: list[Edit] = []
        self._sequence = 0

    @property
    def changes(self) -> tuple[Edit, ...]:
        return tuple(self._changes)

    def source_span(self, working_start: int, working_end: int) -> tuple[int, int]:
        return (
            self._source_boundaries[working_start],
            self._source_boundaries[working_end],
        )

    @staticmethod
    def _map_replacement_boundaries(
        before: str,
        after: str,
        source_boundaries: list[int],
    ) -> list[int]:
        """Preserve original offsets for unchanged parts of a replacement."""
        if not after:
            return [source_boundaries[-1]]

        mapped: list[int | None] = [None] * (len(after) + 1)
        matcher = SequenceMatcher(None, before, after, autojunk=False)
        for operation, old_start, old_end, new_start, new_end in matcher.get_opcodes():
            if operation == "equal":
                for offset in range(new_end - new_start + 1):
                    mapped[new_start + offset] = source_boundaries[old_start + offset]
                continue

            source_start = source_boundaries[old_start]
            source_end = source_boundaries[old_end]
            new_length = new_end - new_start
            if new_length == 0:
                mapped[new_start] = source_end
                continue
            for offset in range(new_length + 1):
                mapped[new_start + offset] = round(
                    source_start
                    + ((source_end - source_start) * offset / new_length)
                )

        previous = source_boundaries[0]
        for index, value in enumerate(mapped):
            if value is None:
                mapped[index] = previous
            else:
                previous = value
        return [int(value) for value in mapped]

    def replace_pattern(
        self,
        rule: RuleSpec,
        pattern: re.Pattern[str],
        replacement: str | ReplacementFunction,
    ) -> None:
        """Replace unprotected matches and append exact structured edits."""
        protected = find_protected_spans(self.text)
        candidates: list[tuple[re.Match[str], str, RuleSpec, int, int]] = []

        for match in pattern.finditer(self.text):
            if any(
                match.start() < span.end and span.start < match.end()
                for span in protected
            ):
                continue

            if callable(replacement):
                value = replacement(match, self.text)
            else:
                value = match.expand(replacement)
            if value is None:
                continue
            if isinstance(value, Replacement):
                after = value.text
                applied_rule = value.rule or rule
            else:
                after = value
                applied_rule = rule
            before = match.group(0)
            if before == after:
                continue
            source_start, source_end = self.source_span(match.start(), match.end())
            candidates.append(
                (match, after, applied_rule, source_start, source_end)
            )

        for match, after, applied_rule, source_start, source_end in candidates:
            self._sequence += 1
            self._changes.append(
                Edit(
                    sequence=self._sequence,
                    rule_id=applied_rule.rule_id,
                    action=applied_rule.action,
                    before=match.group(0),
                    after=after,
                    source_start=source_start,
                    source_end=source_end,
                    working_start=match.start(),
                    working_end=match.end(),
                    severity=applied_rule.severity,
                    authority=applied_rule.authority,
                )
            )

        for match, after, _applied_rule, source_start, source_end in reversed(candidates):
            old_boundaries = self._source_boundaries[
                match.start():match.end() + 1
            ]
            replacement_boundaries = self._map_replacement_boundaries(
                match.group(0), after, old_boundaries
            )
            self.text = self.text[:match.start()] + after + self.text[match.end():]
            self._source_boundaries = (
                self._source_boundaries[:match.start()]
                + replacement_boundaries
                + self._source_boundaries[match.end() + 1:]
            )

    def result(self, findings: tuple[Finding, ...] = ()) -> EditResult:
        return EditResult(
            text=self.text,
            changes=tuple(self._changes),
            findings=findings,
        )
