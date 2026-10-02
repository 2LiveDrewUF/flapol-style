"""Dated, public Florida officeholder identity data.

The base book is intentionally narrow. It supplies identity context; it does
not authorize an editorial transformation by itself. Consumers may add their
own names and aliases without moving private or local registries here.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import json
from pathlib import Path


_DATA_PATH = Path(__file__).with_name("data") / "officeholders.json"


class OfficeholderBookStaleError(RuntimeError):
    """Raised when a dated roster requires adjudication before further use."""

    def __init__(self, group_id: str, stale_from: date, as_of: date):
        self.group_id = group_id
        self.stale_from = stale_from
        self.as_of = as_of
        super().__init__(
            f"{group_id} is stale from {stale_from.isoformat()} for "
            f"as-of date {as_of.isoformat()}; adjudicate and refresh the roster"
        )


def _load_book() -> dict[str, object]:
    with _DATA_PATH.open(encoding="utf-8") as source:
        book = json.load(source)
    if book.get("schema_version") != 1:
        raise ValueError("unsupported officeholder-book schema")
    return book


def load_officeholder_group(group_id: str, *, as_of: date) -> dict[str, object]:
    """Load one usable roster group for an explicit date.

    A group whose ``stale_from`` date has arrived raises instead of returning
    identities. That failure is the adjudication gate: stale data is still
    inspectable in the packaged JSON, but cannot silently remain operational.
    """
    if type(as_of) is not date:
        raise TypeError("as_of must be an explicit datetime.date")

    book = _load_book()
    for group in book["groups"]:
        if group["id"] != group_id:
            continue
        stale_value = group.get("stale_from")
        if stale_value is not None:
            stale_from = date.fromisoformat(stale_value)
            if as_of >= stale_from:
                raise OfficeholderBookStaleError(group_id, stale_from, as_of)
        return deepcopy(group)
    raise KeyError(f"unknown officeholder group: {group_id}")


def list_officeholder_groups() -> tuple[str, ...]:
    """Return stable group IDs without asserting that any group is current."""
    return tuple(group["id"] for group in _load_book()["groups"])

