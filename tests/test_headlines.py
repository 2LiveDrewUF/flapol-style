import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import apply_headline_style, apply_headline_style_with_report


class HeadlineRuleTests(unittest.TestCase):
    def test_imported_title_case_is_converted_to_sentence_case(self):
        self.assertEqual(
            apply_headline_style(
                "Democrats Clash Over Who Replaces Platner Even Before He Exits",
                preserve_phrases=("Platner",),
            ),
            "Democrats clash over who replaces Platner even before he exits",
        )

    def test_major_source_names_are_preserved(self):
        self.assertEqual(
            apply_headline_style(
                "What The New York Times And Wall Street Journal Said About Florida"
            ),
            "What The New York Times and Wall Street Journal said about Florida",
        )

    def test_consumer_can_supply_current_names(self):
        self.assertEqual(
            apply_headline_style(
                "What Ron DeSantis Said About Casey DeSantis",
                preserve_phrases=("Ron DeSantis", "Casey DeSantis"),
            ),
            "What Ron DeSantis said about Casey DeSantis",
        )

    def test_house_style_titles_are_preserved(self):
        self.assertEqual(
            apply_headline_style(
                "Florida Governor And CFO Announce New Program"
            ),
            "Florida Governor and CFO announce new program",
        )

    def test_internal_capitals_acronyms_and_money_are_preserved(self):
        self.assertEqual(
            apply_headline_style("DeSantis Says SpaceX Deal Is Worth $547M"),
            "DeSantis says SpaceX deal is worth $547M",
        )

    def test_first_word_after_colon_is_preserved(self):
        self.assertEqual(
            apply_headline_style("Election Night: What Happens Next"),
            "Election night: What happens next",
        )

    def test_existing_sentence_case_is_unchanged(self):
        source = "Florida lawmakers prepare for a long budget debate"
        self.assertEqual(apply_headline_style(source), source)

    def test_sentence_case_change_is_reported_per_word(self):
        source = "Florida Lawmakers Debate New Bill"
        result = apply_headline_style_with_report(source)
        self.assertEqual(result.text, "Florida lawmakers debate new bill")
        self.assertEqual(
            [change.rule_id for change in result.changes],
            ["flapol.headlines.sentence-case"] * 4,
        )
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )

    def test_quoted_text_is_not_decapped(self):
        source = 'Candidate Calls Plan “The New American Century” A Mistake'
        self.assertEqual(
            apply_headline_style(source),
            'Candidate calls plan “The New American Century” a mistake',
        )

    def test_unclosed_quote_fails_closed(self):
        source = 'Candidate Calls Plan “The New American Century A Mistake'
        self.assertEqual(
            apply_headline_style(source),
            'Candidate calls plan “The New American Century A Mistake',
        )

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
