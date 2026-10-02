from datetime import date, datetime
import json
import pathlib
import sys
import unittest
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import (
    OfficeholderBookStaleError,
    list_officeholder_groups,
    load_officeholder_group,
)


DATA_PATH = ROOT / "python" / "flapol_style" / "data" / "officeholders.json"


class OfficeholderBookTests(unittest.TestCase):
    def test_narrow_public_groups_are_explicit(self):
        self.assertEqual(
            list_officeholder_groups(),
            (
                "florida-state-executive",
                "florida-congressional-delegation",
                "florida-state-legislature",
            ),
        )

    def test_state_executive_contains_only_settled_base_scope(self):
        group = load_officeholder_group(
            "florida-state-executive", as_of=date(2026, 10, 2)
        )
        self.assertEqual(
            {entry["office"] for entry in group["entries"]},
            {
                "governor",
                "lieutenant-governor",
                "attorney-general",
                "chief-financial-officer",
                "agriculture-commissioner",
            },
        )
        self.assertEqual(len(group["entries"]), 5)

    def test_current_snapshot_accounts_for_every_legislative_seat(self):
        delegation = load_officeholder_group(
            "florida-congressional-delegation", as_of=date(2026, 10, 2)
        )
        legislature = load_officeholder_group(
            "florida-state-legislature", as_of=date(2026, 11, 3)
        )
        self.assertEqual(len(delegation["entries"]), 29)
        self.assertEqual(len(delegation["vacancies"]), 1)
        self.assertEqual(len(legislature["entries"]), 155)
        self.assertEqual(len(legislature["vacancies"]), 5)
        self.assertEqual(
            len(legislature["entries"]) + len(legislature["vacancies"]),
            160,
        )

    def test_state_legislature_loads_through_election_day(self):
        group = load_officeholder_group(
            "florida-state-legislature", as_of=date(2026, 11, 3)
        )
        self.assertEqual(group["valid_through"], "2026-11-03")
        self.assertEqual(group["stale_from"], "2026-11-04")

    def test_state_legislature_requires_adjudication_from_november_4(self):
        with self.assertRaises(OfficeholderBookStaleError) as raised:
            load_officeholder_group(
                "florida-state-legislature", as_of=date(2026, 11, 4)
            )
        self.assertEqual(raised.exception.group_id, "florida-state-legislature")
        self.assertIn("adjudicate and refresh", str(raised.exception))

    def test_as_of_date_is_explicit_and_not_a_timestamp(self):
        with self.assertRaises(TypeError):
            load_officeholder_group(
                "florida-state-legislature",
                as_of=datetime(2026, 10, 2, 12, 0),
            )

    def test_ids_and_names_are_unambiguous_within_each_group(self):
        for group_id in list_officeholder_groups():
            group = load_officeholder_group(group_id, as_of=date(2026, 10, 2))
            ids = [entry["id"] for entry in [*group["entries"], *group["vacancies"]]]
            self.assertEqual(len(ids), len(set(ids)), group_id)

            identities: dict[str, str] = {}
            for entry in group["entries"]:
                for name in [entry["name"], *entry["aliases"]]:
                    normalized = name.casefold()
                    self.assertNotIn(normalized, identities, name)
                    identities[normalized] = entry["id"]

    def test_every_source_is_an_https_official_government_site(self):
        book = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        allowed_hosts = {
            "dos.fl.gov",
            "myfloridacfo.com",
            "steube.house.gov",
            "www.fdacs.gov",
            "www.flgov.com",
            "www.flhouse.gov",
            "www.flsenate.gov",
            "www.house.gov",
            "www.leg.state.fl.us",
            "www.myfloridalegal.com",
            "www.senate.gov",
        }
        for source in book["sources"]:
            parsed = urlparse(source["url"])
            self.assertEqual(parsed.scheme, "https")
            self.assertIn(parsed.hostname, allowed_hosts)
            self.assertEqual(source["checked_on"], "2026-10-02")


if __name__ == "__main__":
    unittest.main()
