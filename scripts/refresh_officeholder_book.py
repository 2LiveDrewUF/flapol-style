#!/usr/bin/env python3
"""Refresh the narrow public Florida officeholder book from official sources.

This script deliberately writes a review candidate. Running it does not adjudicate
the result or authorize a release. Review vacancies, source-name changes and the
dated staleness boundary before committing generated data.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
import html
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "python" / "flapol_style" / "data" / "officeholders.json"
NAME_PREFERENCES = DEFAULT_OUTPUT.with_name("officeholder_name_preferences.json")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/140.0.0.0 Safari/537.36 "
    "flapol-style-officeholder-refresh/1.0"
)

SOURCES = {
    "florida-governor": "https://www.flgov.com/eog/",
    "florida-lieutenant-governor": "https://www.flgov.com/eog/leadership/people/jay-collins",
    "florida-attorney-general": "https://www.myfloridalegal.com/ag-bio",
    "florida-chief-financial-officer": "https://myfloridacfo.com/about/meet-the-cfo",
    "florida-agriculture-commissioner": "https://www.fdacs.gov/About-Us/Meet-Commissioner-Simpson",
    "us-house-florida": "https://www.house.gov/representatives",
    "us-senate-florida": "https://www.senate.gov/states/FL/intro.htm",
    "florida-house-2026-2028": "https://www.flhouse.gov/Representatives",
    "florida-senate-2026-2028": "https://www.flsenate.gov/Senators/2026-2028",
    "florida-2026-election-dates": "https://dos.fl.gov/elections/for-voters/election-dates/",
    "florida-legislative-terms": "https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0100-0199/0100/Sections/0100.041.html",
    "greg-steube": "https://steube.house.gov/",
}

STATE_LEGISLATURE_ID = "florida-state-legislature"
STATE_VALID_FROM = "2026-11-04"
STATE_VALID_THROUGH = "2028-11-07"
STATE_HOUSE_SOURCE = "florida-house-2026-2028"
STATE_SENATE_SOURCE = "florida-senate-2026-2028"
STATE_PARTY_PATTERN = r"Republican|Democrat|No Party Affiliation"


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urlopen(request, timeout=45) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding, errors="replace")
    except Exception as error:
        raise RuntimeError(f"official source fetch failed: {url}: {error}") from error


def clean_markup(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def checked_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise argparse.ArgumentTypeError("checked date must be YYYY-MM-DD") from error


def source_record(source_id: str, checked_on: str) -> dict[str, str]:
    return {
        "id": source_id,
        "url": SOURCES[source_id],
        "checked_on": checked_on,
    }


def aliases_from_inverted(source_name: str) -> tuple[str, list[str]]:
    """Return a natural-order official name and conservative source-derived aliases."""
    surname, given = (part.strip() for part in source_name.split(",", 1))
    given = re.sub(r"^(?:Dr\.|Hon\.)\s+", "", given).strip()
    suffix_match = re.search(r"\s+(Jr\.|Sr\.|II|III|IV)$", surname)
    suffix = suffix_match.group(1) if suffix_match else ""
    base_surname = surname[: suffix_match.start()].strip() if suffix_match else surname
    nickname_match = re.search(r'"([^"]+)"', given)
    nickname = nickname_match.group(1).strip() if nickname_match else ""
    formal_given = re.sub(r'\s*"[^"]+"\s*', " ", given).strip()
    official_name = " ".join(part for part in (formal_given, base_surname, suffix) if part)

    aliases: list[str] = []
    first = formal_given.split()[0] if formal_given else ""
    short_form = " ".join(part for part in (first, base_surname, suffix) if part)
    if short_form and short_form != official_name:
        aliases.append(short_form)
    if suffix:
        without_suffix = f"{first} {base_surname}".strip()
        if without_suffix and without_suffix not in {official_name, *aliases}:
            aliases.append(without_suffix)
    if nickname:
        nickname_form = " ".join(part for part in (nickname, base_surname, suffix) if part)
        if nickname_form not in {official_name, *aliases}:
            aliases.insert(0, nickname_form)
        if suffix:
            nickname_without_suffix = f"{nickname} {base_surname}"
            if nickname_without_suffix not in {official_name, *aliases}:
                aliases.append(nickname_without_suffix)
    return official_name, aliases


def state_legislator_names(source_name: str) -> tuple[str, list[str]]:
    """Keep source-backed variants while omitting initials in the primary name."""
    surname, given = (part.strip() for part in source_name.split(",", 1))
    given = re.sub(r"^(?:Dr\.|Hon\.)\s+", "", given)
    suffix = ""
    for field in (surname, given):
        match = re.search(r"(?:,\s*|\s+)(Jr\.|Sr\.|II|III|IV)$", field)
        if match:
            suffix = match[1]
            if field == surname:
                surname = surname[:match.start()]
            else:
                given = given[:match.start()]
            break

    nickname_match = re.search(r'"([^"]+)"|“([^”]+)”', given)
    nickname = ""
    if nickname_match:
        nickname = (nickname_match[1] or nickname_match[2]).strip()
        given = f"{given[:nickname_match.start()]} {given[nickname_match.end():]}"
    if re.search(r'["“”]', given):
        raise ValueError(f"unrecognized nickname structure: {source_name}")
    first, *middle = given.split()
    initial = re.compile(r"[A-Z]\.?")
    preferred = " ".join([first, *(part for part in middle if not initial.fullmatch(part))])
    official = " ".join([first, *middle])
    undotted = " ".join(
        [first, *(part.rstrip(".") if initial.fullmatch(part) else part for part in middle)]
    )
    given_forms = list(dict.fromkeys((preferred, official, undotted, first)))
    if nickname:
        formal_forms = tuple(given_forms)
        given_forms.append(nickname)
        for formal in formal_forms:
            given_forms.extend((f'{formal} "{nickname}"', f"{formal} “{nickname}”"))

    name = " ".join(part for part in (preferred, surname, suffix) if part)
    aliases = dict.fromkeys(
        " ".join(part for part in (form, surname, ending) if part)
        for form in given_forms
        for ending in (suffix, "")
    )
    aliases.pop(name)
    return name, list(aliases)


def person_entry(
    *,
    entry_id: str,
    name: str,
    level: str,
    office: str,
    source_id: str,
    source_name: str | None = None,
    aliases: list[str] | None = None,
    chamber: str | None = None,
    district: int | None = None,
    party: str | None = None,
    profile_url: str | None = None,
) -> dict[str, object]:
    entry: dict[str, object] = {
        "id": entry_id,
        "name": name,
        "aliases": aliases or [],
        "jurisdiction": "Florida",
        "level": level,
        "office": office,
        "status": "active",
        "source_id": source_id,
    }
    if source_name and source_name != name:
        entry["source_name"] = source_name
    if chamber:
        entry["chamber"] = chamber
    if district is not None:
        entry["district"] = district
    if party:
        entry["party"] = party
    if profile_url:
        entry["profile_url"] = profile_url
    return entry


def state_legislator_entry(
    *, chamber: str, district: int, party: str, source_name: str, profile_url: str
) -> dict[str, object]:
    name, aliases = state_legislator_names(source_name)
    # A seat alone is not identity: an owner-approved familiar name applies
    # only while the chamber's exact source name still matches that person.
    preferences = json.loads(NAME_PREFERENCES.read_text(encoding="utf-8"))
    if preferences.get("schema_version") != 1:
        raise ValueError("unsupported officeholder-name preference schema")
    entry_id = f"fl-{chamber}-{district}"
    for preference in preferences["preferences"]:
        if preference["id"] == entry_id and preference["source_name"] == source_name:
            aliases = list(dict.fromkeys([name, *aliases, *preference["aliases"]]))
            name = preference["name"]
            aliases = [alias for alias in aliases if alias != name]
            break
    return person_entry(
        entry_id=entry_id,
        name=name,
        level="state",
        office="representative" if chamber == "house" else "senator",
        chamber=chamber,
        district=district,
        party=party,
        source_id=STATE_HOUSE_SOURCE if chamber == "house" else STATE_SENATE_SOURCE,
        source_name=source_name,
        aliases=aliases,
        profile_url=profile_url,
    )


def title_text(page: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", page, flags=re.I | re.S)
    if not match:
        raise ValueError("page has no title")
    return clean_markup(match.group(1))


def parse_state_executive(pages: dict[str, str]) -> list[dict[str, object]]:
    governor_match = re.match(r"Governor (.+?) \|", title_text(pages["florida-governor"]))
    lieutenant_title = title_text(pages["florida-lieutenant-governor"])
    attorney_match = re.match(
        r"Attorney General (.+?) \|", title_text(pages["florida-attorney-general"])
    )
    cfo_match = re.search(
        r"Meet Your Chief(?:&nbsp;|\s)*Financial(?:&nbsp;|\s)*Officer.*?<strong>([^<]+)</strong>",
        pages["florida-chief-financial-officer"],
        flags=re.I | re.S,
    )
    agriculture_match = re.search(
        r"Commissioner\s*(?:<!--.*?-->)?\s*([A-Z][A-Za-z'’.-]+\s+[A-Z][A-Za-z'’.-]+)",
        pages["florida-agriculture-commissioner"],
        flags=re.S,
    )
    if not all((governor_match, attorney_match, cfo_match, agriculture_match)):
        raise ValueError("one or more statewide officer names could not be verified")

    lieutenant_name = lieutenant_title.split(" |", 1)[0].strip()
    records = (
        ("fl-governor", governor_match.group(1).strip(), "governor", "florida-governor"),
        (
            "fl-lieutenant-governor",
            lieutenant_name,
            "lieutenant-governor",
            "florida-lieutenant-governor",
        ),
        (
            "fl-attorney-general",
            attorney_match.group(1).strip(),
            "attorney-general",
            "florida-attorney-general",
        ),
        (
            "fl-chief-financial-officer",
            clean_markup(cfo_match.group(1)),
            "chief-financial-officer",
            "florida-chief-financial-officer",
        ),
        (
            "fl-agriculture-commissioner",
            clean_markup(agriculture_match.group(1)),
            "agriculture-commissioner",
            "florida-agriculture-commissioner",
        ),
    )
    return [
        person_entry(
            entry_id=entry_id,
            name=name,
            level="state",
            office=office,
            source_id=source_id,
            profile_url=SOURCES[source_id],
        )
        for entry_id, name, office, source_id in records
    ]


def parse_us_house(page: str, steube_page: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    table_match = re.search(
        r"<table\b[^>]*>.*?<caption[^>]*>\s*Florida\s*</caption>(.*?)</table>",
        page,
        flags=re.I | re.S,
    )
    if not table_match:
        raise ValueError("Florida table not found on U.S. House roster")

    entries: list[dict[str, object]] = []
    vacancies: list[dict[str, object]] = []
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", table_match.group(1), flags=re.I | re.S):
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", row, flags=re.I | re.S)
        if len(cells) < 3:
            continue
        district_text, name_cell, party_cell = cells[:3]
        district_match = re.search(r"\d+", clean_markup(district_text))
        if not district_match:
            continue
        district = int(district_match.group(0))
        name_text = clean_markup(name_cell)
        if "Vacancy" in name_text:
            vacancies.append(
                {
                    "id": f"us-house-fl-{district}",
                    "jurisdiction": "Florida",
                    "level": "federal",
                    "chamber": "house",
                    "district": district,
                    "status": "vacant",
                    "source_id": "us-house-florida",
                }
            )
            continue
        link_match = re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', name_cell, flags=re.I | re.S)
        if not link_match:
            raise ValueError(f"member link missing for U.S. House district {district}")
        source_name = clean_markup(link_match.group(2))
        name, aliases = aliases_from_inverted(source_name)
        profile_url = urljoin(SOURCES["us-house-florida"], html.unescape(link_match.group(1)))
        if district == 17:
            if "Greg Steube" not in clean_markup(steube_page):
                raise ValueError("Greg Steube could not be verified on his official House site")
            name = "Greg Steube"
            aliases = [alias for alias in aliases if alias != "W. Steube"]
        entries.append(
            person_entry(
                entry_id=f"us-house-fl-{district}",
                name=name,
                level="federal",
                office="representative",
                chamber="house",
                district=district,
                party=clean_markup(party_cell),
                source_id="us-house-florida",
                source_name=source_name,
                aliases=aliases,
                profile_url=profile_url,
            )
        )
    return sorted(entries, key=lambda item: item["district"]), vacancies


def parse_us_senate(page: str) -> list[dict[str, object]]:
    matches = re.findall(
        r'<strong>\s*<a\b[^>]*href="([^"]+)"[^>]*>([^<]+)</a>\s*\(([RDI])\)\s*</strong>',
        page,
        flags=re.I,
    )
    if len(matches) != 2:
        raise ValueError(f"expected two Florida U.S. senators, found {len(matches)}")
    return [
        person_entry(
            entry_id=f"us-senate-fl-{index}",
            name=clean_markup(name),
            level="federal",
            office="senator",
            chamber="senate",
            party=party.upper(),
            source_id="us-senate-florida",
            profile_url=urljoin(SOURCES["us-senate-florida"], href),
        )
        for index, (href, name, party) in enumerate(matches, start=1)
    ]


def parse_florida_house(page: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    entries: list[dict[str, object]] = []
    term_end = date.fromisoformat(STATE_VALID_THROUGH).strftime("%m/%d/%y")
    blocks = re.findall(
        r'<a\b[^>]*href="([^"]*details\.aspx\?MemberId=[^"]+)"[^>]*>(.*?)</a>',
        page,
        flags=re.I | re.S,
    )
    for href, block in blocks:
        name_match = re.search(r"<h5[^>]*>(.*?)</h5>", block, flags=re.I | re.S)
        plain_block = clean_markup(block)
        party_match = re.search(
            rf"({STATE_PARTY_PATTERN})\s*—\s*District:\s*(\d+)", plain_block
        )
        dates = re.search(r"\d{2}/\d{2}/\d{2}\s*-\s*(\d{2}/\d{2}/\d{2})", plain_block)
        if not all((name_match, party_match, dates)) or dates[1] != term_end:
            continue
        source_name = clean_markup(name_match.group(1))
        district = int(party_match.group(2))
        entries.append(
            state_legislator_entry(
                chamber="house",
                district=district,
                party=party_match.group(1),
                source_name=source_name,
                profile_url=urljoin(SOURCES[STATE_HOUSE_SOURCE], html.unescape(href)),
            )
        )

    plain_page = clean_markup(page)
    pending = sorted(
        {
            int(value)
            for value in re.findall(
                r"Pending Election\s+—\s+District:\s*(\d+)", plain_page
            )
        }
    )
    vacancies = [
        {
            "id": f"fl-house-{district}",
            "jurisdiction": "Florida",
            "level": "state",
            "chamber": "house",
            "district": district,
            "status": "pending-election",
            "source_id": STATE_HOUSE_SOURCE,
        }
        for district in pending
    ]
    return sorted(entries, key=lambda item: item["district"]), vacancies


def parse_florida_senate(page: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    entries: list[dict[str, object]] = []
    vacancies: list[dict[str, object]] = []
    for row in re.findall(
        r'<tr\b[^>]*class="All[^"]*"[^>]*>(.*?)</tr>', page, flags=re.I | re.S
    ):
        cells = re.findall(r"<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>", row, flags=re.I | re.S)
        if len(cells) < 3:
            continue
        name_cell, district_cell, party_cell = cells[:3]
        district_match = re.search(r"\d+", clean_markup(district_cell))
        if not district_match:
            continue
        district = int(district_match.group(0))
        link_match = re.search(
            r'<a\b[^>]*class="[^"]*senatorLink[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            name_cell,
            flags=re.I | re.S,
        )
        source_name = clean_markup(link_match.group(2) if link_match else name_cell)
        if source_name == "Vacant":
            vacancies.append(
                {
                    "id": f"fl-senate-{district}",
                    "jurisdiction": "Florida",
                    "level": "state",
                    "chamber": "senate",
                    "district": district,
                    "status": "vacant",
                    "source_id": STATE_SENATE_SOURCE,
                }
            )
            continue
        if not link_match:
            raise ValueError(f"member link missing for Florida Senate district {district}")
        entries.append(
            state_legislator_entry(
                chamber="senate",
                district=district,
                party=clean_markup(party_cell),
                source_name=source_name,
                profile_url=urljoin(SOURCES[STATE_SENATE_SOURCE], html.unescape(link_match.group(1))),
            )
        )
    return sorted(entries, key=lambda item: item["district"]), vacancies


def state_legislature_group(
    checked_on: str,
    house: tuple[list[dict[str, object]], list[dict[str, object]]],
    senate: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> dict[str, object]:
    if not STATE_VALID_FROM <= checked_on <= STATE_VALID_THROUGH:
        raise ValueError("checked date is outside the supported 2026-2028 state term")
    for chamber, seat_count, (entries, vacancies) in (
        ("House", 120, house),
        ("Senate", 40, senate),
    ):
        districts = sorted(row["district"] for row in [*entries, *vacancies])
        if districts != list(range(1, seat_count + 1)):
            raise ValueError(
                f"Florida {chamber} roster must account for each of its {seat_count} districts once"
            )
    return {
        "id": STATE_LEGISLATURE_ID,
        "verified_as_of": checked_on,
        "valid_from": STATE_VALID_FROM,
        "valid_through": STATE_VALID_THROUGH,
        "stale_from": (date.fromisoformat(STATE_VALID_THROUGH) + timedelta(days=1)).isoformat(),
        "entries": [*senate[0], *house[0]],
        "vacancies": [*senate[1], *house[1]],
    }


def update_state_legislature(book: dict[str, object], group: dict[str, object]) -> None:
    current = next(row for row in book["groups"] if row["id"] == STATE_LEGISLATURE_ID)
    if current.get("valid_from") != group["valid_from"]:
        book.setdefault("previous_groups", []).insert(0, current)
    book["groups"][book["groups"].index(current)] = group
    source_ids = (STATE_HOUSE_SOURCE, STATE_SENATE_SOURCE)
    checked_on = group["verified_as_of"]
    book["sources"] = [
        *(source for source in book["sources"] if source["id"] not in source_ids),
        *(source_record(source_id, checked_on) for source_id in source_ids),
    ]
    book["verified_as_of"] = max(source["checked_on"] for source in book["sources"])


def build_book(checked_on: str, *, legislature_only: bool = False) -> dict[str, object]:
    book = json.loads(DEFAULT_OUTPUT.read_text(encoding="utf-8"))
    executive = next(group for group in book["groups"] if group["id"] == "florida-state-executive")
    congress = next(
        group for group in book["groups"] if group["id"] == "florida-congressional-delegation"
    )
    if not legislature_only:
        for group in (executive, congress):
            if group.get("incoming") and checked_on >= group["stale_from"]:
                raise ValueError(f"adjudicate the {group['id']} transition before a full refresh")

    legislature = state_legislature_group(
        checked_on,
        parse_florida_house(fetch(SOURCES[STATE_HOUSE_SOURCE])),
        parse_florida_senate(fetch(SOURCES[STATE_SENATE_SOURCE])),
    )
    update_state_legislature(book, legislature)
    if legislature_only:
        return book

    legislature_sources = {STATE_HOUSE_SOURCE, STATE_SENATE_SOURCE}
    pages = {
        source_id: fetch(url)
        for source_id, url in SOURCES.items()
        if source_id not in legislature_sources
    }
    election_dates = clean_markup(pages["florida-2026-election-dates"])
    legislative_terms = clean_markup(pages["florida-legislative-terms"])
    if not re.search(r"Election Day:\s*November 3, 2026", election_dates, flags=re.I):
        raise ValueError("official election calendar does not confirm Nov. 3, 2026")
    if not re.search(
        r"term of office of each member of the Legislature shall begin upon election",
        legislative_terms,
        flags=re.I,
    ):
        raise ValueError("official statute does not confirm legislative terms begin upon election")
    state_executive = parse_state_executive(pages)
    us_house, us_house_vacancies = parse_us_house(
        pages["us-house-florida"], pages["greg-steube"]
    )
    us_senate = parse_us_senate(pages["us-senate-florida"])
    if len(state_executive) != 5:
        raise ValueError(f"expected 5 statewide officers, found {len(state_executive)}")
    if len(us_house) + len(us_house_vacancies) != 28:
        raise ValueError("U.S. House roster does not account for all 28 Florida districts")
    if len(us_senate) != 2:
        raise ValueError("U.S. Senate roster does not contain two Florida senators")
    book["sources"] = [
        source_record(source["id"], checked_on) if source["id"] in pages else source
        for source in book["sources"]
    ]
    executive.update(verified_as_of=checked_on, entries=state_executive, vacancies=[])
    congress.update(
        verified_as_of=checked_on,
        entries=[*us_senate, *us_house],
        vacancies=us_house_vacancies,
    )
    return book


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checked-on", required=True, type=checked_date)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--legislature-only", action="store_true")
    args = parser.parse_args()

    book = build_book(args.checked_on, legislature_only=args.legislature_only)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "groups": {
                    group["id"]: {
                        "entries": len(group["entries"]),
                        "vacancies": len(group["vacancies"]),
                    }
                    for group in book["groups"]
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
