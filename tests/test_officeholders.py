from datetime import date, datetime
import json
import pathlib
import runpy
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
REFRESH = runpy.run_path(str(ROOT / "scripts" / "refresh_officeholder_book.py"))


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
            "florida-state-legislature", as_of=date(2026, 11, 13)
        )
        self.assertEqual(len(delegation["entries"]), 29)
        self.assertEqual(len(delegation["vacancies"]), 1)
        self.assertEqual(len(legislature["entries"]), 159)
        self.assertEqual(
            {(row["chamber"], row["district"], row["status"]) for row in legislature["vacancies"]},
            {("senate", 39, "vacant")},
        )
        for chamber, seat_count in (("house", 120), ("senate", 40)):
            districts = sorted(
                entry["district"]
                for entry in [*legislature["entries"], *legislature["vacancies"]]
                if entry["chamber"] == chamber
            )
            self.assertEqual(districts, list(range(1, seat_count + 1)))

    def test_state_legislature_changes_on_november_4(self):
        before = load_officeholder_group(
            "florida-state-legislature", as_of=date(2026, 11, 3)
        )
        after = load_officeholder_group(
            "florida-state-legislature", as_of=date(2026, 11, 4)
        )
        self.assertEqual(before["valid_through"], "2026-11-03")
        self.assertEqual(before["stale_from"], "2026-11-04")
        self.assertEqual(after["valid_from"], "2026-11-04")
        before_names = {entry["id"]: entry["name"] for entry in before["entries"]}
        after_names = {entry["id"]: entry["name"] for entry in after["entries"]}
        self.assertEqual(before_names["fl-house-33"], "Monique Miller")
        self.assertEqual(after_names["fl-house-33"], "Dan McDow")
        self.assertEqual(before_names["fl-house-67"], "Fentrice Driskell")
        self.assertEqual(after_names["fl-senate-16"], "Fentrice Driskell")

    def test_state_legislature_requires_adjudication_after_current_term(self):
        group = load_officeholder_group(
            "florida-state-legislature", as_of=date(2028, 11, 7)
        )
        self.assertEqual(group["valid_through"], "2028-11-07")
        with self.assertRaises(OfficeholderBookStaleError) as raised:
            load_officeholder_group(
                "florida-state-legislature", as_of=date(2028, 11, 8)
            )
        self.assertEqual(raised.exception.group_id, "florida-state-legislature")
        self.assertIn("adjudicate and refresh", str(raised.exception))

    def test_district_33_familiar_and_formal_names_survive_a_refresh(self):
        group = load_officeholder_group(
            "florida-state-legislature", as_of=date(2026, 11, 13)
        )
        entry = next(row for row in group["entries"] if row["id"] == "fl-house-33")
        self.assertEqual(entry["name"], "Dan McDow")
        self.assertEqual(entry["source_name"], "McDow, Daniel R.")
        self.assertTrue({"Daniel McDow", "Daniel R. McDow", "Daniel R McDow",
                         'Daniel "Dan" McDow', 'Daniel R. “Dan” McDow'} <= set(entry["aliases"]))
        regenerated = REFRESH["state_legislator_entry"](
            chamber="house", district=33, party="Democrat",
            source_name="McDow, Daniel R.", profile_url=entry["profile_url"],
        )
        self.assertEqual(regenerated, entry)

    def test_familiar_name_preference_never_transfers_to_another_identity(self):
        make_entry = REFRESH["state_legislator_entry"]
        for chamber, district, source_name, expected in (
            ("house", 33, "Miller, Monique", "Monique Miller"),
            ("house", 34, "McDow, Daniel R.", "Daniel McDow"),
            ("senate", 33, "McDow, Daniel R.", "Daniel McDow"),
        ):
            with self.subTest(chamber=chamber, district=district, source_name=source_name):
                entry = make_entry(chamber=chamber, district=district, party="Democrat",
                                   source_name=source_name, profile_url="https://www.flhouse.gov/Representatives")
                self.assertEqual(entry["name"], expected)
                self.assertNotIn("Dan McDow", entry["aliases"])

    def test_as_of_date_is_explicit_and_not_a_timestamp(self):
        with self.assertRaises(TypeError):
            load_officeholder_group(
                "florida-state-legislature",
                as_of=datetime(2026, 10, 2, 12, 0),
            )

    def test_incoming_house_covers_every_district_separately_from_sitting_members(self):
        group_id = "florida-congressional-delegation"
        self.assertNotIn("incoming", load_officeholder_group(group_id, as_of=date(2026, 11, 4)))
        group = load_officeholder_group(group_id, as_of=date(2026, 11, 5))
        sitting = {entry["name"]: entry for entry in group["entries"]}
        self.assertEqual(sitting["Debbie Wasserman Schultz"]["district"], 25)
        self.assertEqual(sitting["Byron Donalds"]["district"], 19)
        self.assertEqual(group["vacancies"][0]["district"], 20)
        incoming = group["incoming"]
        self.assertEqual(incoming["expected_start"], "2027-01-03")
        slate = {entry["district"]: entry for entry in incoming["entries"]}
        self.assertEqual(len(incoming["entries"]), 28)
        self.assertEqual(set(slate), set(range(1, 29)))
        self.assertEqual(slate[20]["name"], "Debbie Wasserman Schultz")
        self.assertEqual(slate[10]["election_status"], "unopposed")
        self.assertEqual(slate[24]["name"], "Oliver Gilbert III")
        self.assertIn("Oliver G. Gilbert III", slate[24]["aliases"])
        self.assertEqual(
            {seat: row["name"] for seat, row in slate.items() if row["election_status"] == "provisional"},
            {7: "Ryan Elijah", 9: "Darren Soto", 26: "Mario Diaz-Balart", 27: "Maria Elvira Salazar"},
        )
        with self.assertRaises(OfficeholderBookStaleError):
            load_officeholder_group(group_id, as_of=date(2027, 1, 3))

    def test_executive_transition_lists_successors_before_the_january_gate(self):
        group_id = "florida-state-executive"
        group = load_officeholder_group(group_id, as_of=date(2027, 1, 4))
        sitting = {entry["office"]: entry["name"] for entry in group["entries"]}
        self.assertEqual(sitting["governor"], "Ron DeSantis")
        self.assertEqual(sitting["lieutenant-governor"], "Jay Collins")
        self.assertEqual(group["incoming"]["expected_start"], "2027-01-05")
        self.assertEqual(
            [(row["display_title"], row["name"], row["status"]) for row in group["incoming"]["entries"]],
            [("Gov.-elect", "Byron Donalds", "elect"), ("Lt. Gov.-elect", "Bryan Avila", "elect")],
        )
        with self.assertRaises(OfficeholderBookStaleError):
            load_officeholder_group(group_id, as_of=date(2027, 1, 5))

    def test_ids_and_names_are_unambiguous_within_each_group(self):
        book = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        for group in [*book["groups"], *book["previous_groups"]]:
            ids = [entry["id"] for entry in [*group["entries"], *group["vacancies"]]]
            self.assertEqual(len(ids), len(set(ids)), group["id"])

            identities: dict[str, str] = {}
            for entry in group["entries"]:
                for name in [entry["name"], *entry["aliases"]]:
                    normalized = name.casefold()
                    self.assertNotIn(normalized, identities, name)
                    identities[normalized] = entry["id"]

    def test_every_source_is_an_https_official_government_site(self):
        book = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        allowed_hosts = {
            "dos.elections.myflorida.com",
            "dos.fl.gov",
            "floridaelectionwatch.gov",
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
        source_dates = {}
        for source in book["sources"]:
            parsed = urlparse(source["url"])
            self.assertEqual(parsed.scheme, "https")
            self.assertIn(parsed.hostname, allowed_hosts)
            self.assertNotIn(source["id"], source_dates)
            source_dates[source["id"]] = date.fromisoformat(source["checked_on"])
        for group in [*book["groups"], *book["previous_groups"]]:
            for row in [*group["entries"], *group["vacancies"]]:
                self.assertIn(row["source_id"], source_dates)
            if incoming := group.get("incoming"):
                for row in incoming["entries"]:
                    self.assertEqual(
                        source_dates[row["source_id"]], date.fromisoformat(incoming["checked_on"])
                    )

    def test_state_name_import_preserves_source_variants_and_first_name_initials(self):
        names = REFRESH["state_legislator_names"]
        name, aliases = names('Leek, Thomas J. “Tom”')
        self.assertEqual(name, "Thomas Leek")
        self.assertTrue({
            "Tom Leek", "Thomas J. Leek", "Thomas J Leek",
            'Thomas J. "Tom" Leek', "Thomas “Tom” Leek",
        }.issubset(aliases))
        self.assertEqual(names("Massullo, Ralph E., Jr.")[0], "Ralph Massullo Jr.")
        self.assertEqual(names("Grow, J.J."), ("J.J. Grow", []))
        self.assertEqual(names("Porras, Juan Carlos")[0], "Juan Carlos Porras")
        with self.assertRaisesRegex(ValueError, "unrecognized nickname structure"):
            names('Leek, Thomas J. "Tom')

    def test_state_refresh_rejects_duplicate_districts_even_with_correct_totals(self):
        book = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        group = book["groups"][-1]
        houses = [row for row in group["entries"] if row["chamber"] == "house"]
        senators = [row for row in group["entries"] if row["chamber"] == "senate"]
        vacancies = {row["chamber"]: row for row in group["vacancies"]}
        houses[0] = houses[1]
        with self.assertRaisesRegex(ValueError, "each of its 120 districts once"):
            REFRESH["state_legislature_group"](
                "2026-11-05",
                (houses, []),
                (senators, [vacancies["senate"]]),
            )


if __name__ == "__main__":
    unittest.main()
