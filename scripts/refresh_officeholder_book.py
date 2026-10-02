#!/usr/bin/env python3
"""Refresh the narrow public Florida officeholder book from official sources.

This script deliberately writes a review candidate. Running it does not adjudicate
the result or authorize a release. Review vacancies, source-name changes and the
dated staleness boundary before committing generated data.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
import html
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "python" / "flapol_style" / "data" / "officeholders.json"
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
    "florida-house": "https://www.flhouse.gov/Representatives",
    "florida-senate": "https://www.flsenate.gov/Senators",
    "florida-2026-election-dates": "https://dos.fl.gov/elections/for-voters/election-dates/",
    "florida-legislative-terms": "https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0100-0199/0100/Sections/0100.041.html",
    "greg-steube": "https://steube.house.gov/",
}


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
    blocks = re.findall(
        r'<a\b[^>]*href="([^"]*details\.aspx\?MemberId=[^"]+)"[^>]*>(.*?)</a>',
        page,
        flags=re.I | re.S,
    )
    for href, block in blocks:
        name_match = re.search(r"<h5[^>]*>(.*?)</h5>", block, flags=re.I | re.S)
        party_match = re.search(
            r"<p[^>]*>\s*(Republican|Democrat|No Party Affiliation)\s*&mdash;.*?District:\s*(\d+)",
            block,
            flags=re.I | re.S,
        )
        dates = re.search(r"(\d{2}/\d{2}/\d{2})\s*-\s*(\d{2}/\d{2}/\d{2})", clean_markup(block))
        if not all((name_match, party_match, dates)) or dates.group(2) != "11/03/26":
            continue
        source_name = clean_markup(name_match.group(1))
        name, aliases = aliases_from_inverted(source_name)
        district = int(party_match.group(2))
        entries.append(
            person_entry(
                entry_id=f"fl-house-{district}",
                name=name,
                level="state",
                office="representative",
                chamber="house",
                district=district,
                party=party_match.group(1),
                source_id="florida-house",
                source_name=source_name,
                aliases=aliases,
                profile_url=urljoin(SOURCES["florida-house"], html.unescape(href)),
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
            "source_id": "florida-house",
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
                    "source_id": "florida-senate",
                }
            )
            continue
        if not link_match:
            raise ValueError(f"member link missing for Florida Senate district {district}")
        name, aliases = aliases_from_inverted(source_name)
        entries.append(
            person_entry(
                entry_id=f"fl-senate-{district}",
                name=name,
                level="state",
                office="senator",
                chamber="senate",
                district=district,
                party=clean_markup(party_cell),
                source_id="florida-senate",
                source_name=source_name,
                aliases=aliases,
                profile_url=urljoin(SOURCES["florida-senate"], html.unescape(link_match.group(1))),
            )
        )
    return sorted(entries, key=lambda item: item["district"]), vacancies


def build_book(checked_on: str) -> dict[str, object]:
    pages = {source_id: fetch(url) for source_id, url in SOURCES.items()}
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
    florida_house, florida_house_vacancies = parse_florida_house(pages["florida-house"])
    florida_senate, florida_senate_vacancies = parse_florida_senate(pages["florida-senate"])

    if len(state_executive) != 5:
        raise ValueError(f"expected 5 statewide officers, found {len(state_executive)}")
    if len(us_house) + len(us_house_vacancies) != 28:
        raise ValueError("U.S. House roster does not account for all 28 Florida districts")
    if len(us_senate) != 2:
        raise ValueError("U.S. Senate roster does not contain two Florida senators")
    if len(florida_house) + len(florida_house_vacancies) != 120:
        raise ValueError(
            "Florida House roster does not account for all 120 districts: "
            f"{len(florida_house)} active, {len(florida_house_vacancies)} pending"
        )
    if len(florida_senate) + len(florida_senate_vacancies) != 40:
        raise ValueError(
            "Florida Senate roster does not account for all 40 districts: "
            f"{len(florida_senate)} active, {len(florida_senate_vacancies)} vacant"
        )

    source_ids = [
        "florida-governor",
        "florida-lieutenant-governor",
        "florida-attorney-general",
        "florida-chief-financial-officer",
        "florida-agriculture-commissioner",
        "us-house-florida",
        "us-senate-florida",
        "florida-house",
        "florida-senate",
        "florida-2026-election-dates",
        "florida-legislative-terms",
        "greg-steube",
    ]
    return {
        "schema_version": 1,
        "book_id": "florida-public-officeholders",
        "verified_as_of": checked_on,
        "sources": [source_record(source_id, checked_on) for source_id in source_ids],
        "groups": [
            {
                "id": "florida-state-executive",
                "verified_as_of": checked_on,
                "entries": state_executive,
                "vacancies": [],
            },
            {
                "id": "florida-congressional-delegation",
                "verified_as_of": checked_on,
                "entries": [*us_senate, *us_house],
                "vacancies": us_house_vacancies,
            },
            {
                "id": "florida-state-legislature",
                "verified_as_of": checked_on,
                "valid_through": "2026-11-03",
                "stale_from": "2026-11-04",
                "entries": [*florida_senate, *florida_house],
                "vacancies": [*florida_senate_vacancies, *florida_house_vacancies],
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checked-on", required=True, type=checked_date)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    book = build_book(args.checked_on)
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
