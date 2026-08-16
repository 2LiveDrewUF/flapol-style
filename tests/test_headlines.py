import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import apply_headline_style, apply_headline_style_with_report


class HeadlineRuleTests(unittest.TestCase):
    def test_us_is_normalized_only_by_headline_api(self):
        self.assertEqual(
            apply_headline_style("US Senate advances bill"),
            "U.S. Senate advances bill",
        )

    def test_pronoun_and_longer_initialisms_are_untouched(self):
        source = "Us and USF researchers"
        self.assertEqual(apply_headline_style(source), source)

    def test_headline_api_does_not_silently_apply_main_rules(self):
        source = "US health care debate"
        self.assertEqual(
            apply_headline_style(source),
            "U.S. health care debate",
        )

    def test_quoted_us_is_protected(self):
        source = 'Candidate calls policy “US first”'
        self.assertEqual(apply_headline_style(source), source)

    def test_headline_change_is_reported(self):
        source = "US Senate advances bill"
        result = apply_headline_style_with_report(source)
        self.assertEqual(len(result.changes), 1)
        change = result.changes[0]
        self.assertEqual(change.rule_id, "flapol.headlines.us-periods")
        self.assertEqual(
            source[change.source_start:change.source_end], "US"
        )

    def test_headline_pass_is_idempotent(self):
        once = apply_headline_style("US Senate advances bill")
        self.assertEqual(apply_headline_style(once), once)


if __name__ == "__main__":
    unittest.main()
