from datetime import date
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.dates import apply_date_rules


class DateRuleTests(unittest.TestCase):
    def test_month_with_day_uses_ap_abbreviation(self):
        self.assertEqual(
            apply_date_rules("January 8, September 12 and March 4"),
            "Jan. 8, Sept. 12 and March 4",
        )

    def test_month_with_year_is_spelled_and_has_no_comma(self):
        self.assertEqual(
            apply_date_rules("Jan. 2026 and September, 2027"),
            "January 2026 and September 2027",
        )

    def test_calendar_ordinal_suffix_is_removed(self):
        self.assertEqual(
            apply_date_rules("April 13th and the 13th District"),
            "April 13 and the 13th District",
        )

    def test_full_date_year_commas_are_added(self):
        self.assertEqual(
            apply_date_rules(
                "The January 8 2027 meeting followed January 7, 2027."
            ),
            "The Jan. 8, 2027, meeting followed Jan. 7, 2027.",
        )

    def test_current_publication_year_is_removed_only_with_context(self):
        source = "The Jan. 8, 2026, meeting was canceled."
        self.assertEqual(apply_date_rules(source), source)
        self.assertEqual(
            apply_date_rules(source, publication_date=date(2026, 1, 1)),
            "The Jan. 8 meeting was canceled.",
        )

    def test_weekday_within_seven_days_replaces_numeric_date(self):
        self.assertEqual(
            apply_date_rules(
                "The board meets Monday, Jan. 5, 2026, in Tallahassee.",
                publication_date=date(2026, 1, 1),
            ),
            "The board meets Monday in Tallahassee.",
        )

    def test_weekday_outside_window_is_removed(self):
        self.assertEqual(
            apply_date_rules(
                "The board meets Tuesday, Jan. 20, 2026, in Tallahassee.",
                publication_date=date(2026, 1, 1),
            ),
            "The board meets Jan. 20 in Tallahassee.",
        )

    def test_contradictory_weekday_is_not_rewritten(self):
        source = "The board meets Tuesday, Jan. 5, 2026."
        self.assertEqual(
            apply_date_rules(source, publication_date=date(2026, 1, 1)),
            source,
        )

    def test_invalid_calendar_date_is_not_rewritten(self):
        self.assertEqual(
            apply_date_rules(
                "Feb. 30, 2026", publication_date=date(2026, 1, 1)
            ),
            "Feb. 30, 2026",
        )

    def test_different_year_keeps_year_and_drops_valid_weekday(self):
        self.assertEqual(
            apply_date_rules(
                "The filing was Wednesday, Jan. 8, 2025.",
                publication_date=date(2026, 1, 1),
            ),
            "The filing was Jan. 8, 2025.",
        )

    def test_quotation_link_destination_and_code_are_unchanged(self):
        source = (
            'January 8th. “January 9th, 2026.” '
            '[January 10th](https://example.com/January-10th) `January 11th`'
        )
        self.assertEqual(
            apply_date_rules(source),
            'Jan. 8. “January 9th, 2026.” '
            '[Jan. 10](https://example.com/January-10th) `January 11th`',
        )

    def test_date_pass_is_idempotent(self):
        source = (
            "The board meets Tuesday, January 20th 2026 in Tallahassee. "
            'It called the prior date “January 8th, 2026.”'
        )
        once = apply_date_rules(source, publication_date=date(2026, 1, 1))
        twice = apply_date_rules(once, publication_date=date(2026, 1, 1))
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
