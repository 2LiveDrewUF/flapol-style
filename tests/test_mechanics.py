import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import apply_main_style_with_report
from flapol_style.mechanics import normalize_mechanical_forms


class MechanicalRuleTests(unittest.TestCase):
    def test_body_us_and_gender_neutral_chair_are_normalized(self):
        self.assertEqual(
            normalize_mechanical_forms(
                "The US Chairman and chairwoman announced the US policy."
            ),
            "The U.S. Chair and Chair announced the U.S. policy.",
        )

    def test_us_pronoun_and_longer_initialisms_are_untouched(self):
        source = "Us and USF researchers discussed USDA policy."
        self.assertEqual(normalize_mechanical_forms(source), source)

    def test_covid_percent_and_time_forms_are_normalized(self):
        self.assertEqual(
            normalize_mechanical_forms(
                "A COVID-19 rule drew 8 percent support at 9 PM and 6:30p.m"
            ),
            "A COVID rule drew 8% support at 9 p.m. and 6:30 p.m.",
        )

    def test_per_cent_is_supported_but_percentage_points_are_untouched(self):
        self.assertEqual(
            normalize_mechanical_forms(
                "Support was 8 per cent, up 4 percentage points."
            ),
            "Support was 8%, up 4 percentage points.",
        )

    def test_invalid_meridiem_hours_are_not_legitimized(self):
        source = "The log says 13 PM and 9:75 AM."
        self.assertEqual(normalize_mechanical_forms(source), source)

    def test_protected_regions_are_unchanged(self):
        source = (
            'The US Chairman said COVID-19 rose 8 percent at 9PM. '
            '“The US Chairman said COVID-19 rose 8 percent at 9PM.” '
            '`The US Chairman said 8 percent`'
        )
        self.assertEqual(
            normalize_mechanical_forms(source),
            'The U.S. Chair said COVID rose 8% at 9 p.m. '
            '“The US Chairman said COVID-19 rose 8 percent at 9PM.” '
            '`The US Chairman said 8 percent`',
        )

    def test_mechanical_changes_are_reported_with_stable_ids(self):
        source = "The US Chairman said COVID-19 drew 8 percent at 9PM."
        result = apply_main_style_with_report(source)
        self.assertEqual(
            [change.rule_id for change in result.changes],
            [
                "flapol.terms.covid-without-19",
                "flapol.terms.us-periods",
                "flapol.titles.gender-neutral-chair",
                "ap.numbers.percent-symbol",
                "ap.times.meridiem-format",
            ],
        )
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end], change.before
            )

    def test_mechanical_pass_is_idempotent(self):
        source = "COVID-19 drew 8 percent at 9PM."
        once = normalize_mechanical_forms(source)
        self.assertEqual(normalize_mechanical_forms(once), once)


if __name__ == "__main__":
    unittest.main()
