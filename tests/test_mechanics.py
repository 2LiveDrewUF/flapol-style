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

    def test_spelled_out_percent_at_a_body_sentence_start_has_no_review_item(self):
        cases = (
            "Thirty-six percent favored it.",
            "The poll was released. Ninety-one percent supported it.",
            "The poll closed! Fifty-three percent favored it.",
            "How many responded? Ninety-nine percent did.",
            "Survey results\n\nFifty-three percent also supported it.",
            "Survey results\n\u2063\nFifty-three percent also supported it.",
            "Survey results\r\n \u2063 \r\nOne hundred and six per cent was reported.",
            "The choice was called “Option A.” Thirty-six percent favored it.",
            "The poll closed at 6 p.m. Thirty-six percent favored it.",
            "They hesitated… Thirty-six percent had already voted.",
        )
        for source in cases:
            with self.subTest(source=source):
                result = apply_main_style_with_report(source)
                self.assertEqual(result.text, source)
                self.assertEqual(result.changes, ())
                self.assertEqual(result.findings, ())

    def test_percent_edits_keep_original_offsets_across_passages(self):
        source = (
            "📊 The US survey closed.\n\u2063\n"
            "Thirty-six percent favored it. In the survey, fifty-three percent "
            "also supported the amendment. Support reached 8 percent."
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            "📊 The U.S. survey closed.\n\u2063\n"
            "Thirty-six percent favored it. In the survey, 53% "
            "also supported the amendment. Support reached 8%.",
        )
        by_rule = {change.rule_id: change for change in result.changes}
        for rule, before, after in (
            ("ap.numbers.spoken-percent-symbol", "fifty-three percent", "53%"),
            ("ap.numbers.percent-symbol", "8 percent", "8%"),
        ):
            change = by_rule[rule]
            self.assertEqual((change.before, change.after), (before, after))
            self.assertEqual(change.source_start, source.index(before))
            self.assertEqual(source[change.source_start:change.source_end], before)
        repeated = apply_main_style_with_report(result.text)
        self.assertEqual(repeated.text, result.text)
        self.assertEqual(repeated.changes, ())
        self.assertEqual(result.findings, ())

    def test_spoken_percent_with_continuation_and_literal_text(self):
        for prefix in ("At 6 p.m. ", "The poll found\n", "In the survey, "):
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    normalize_mechanical_forms(f"{prefix}thirty-six percent favored it."),
                    f"{prefix}36% favored it.",
                )
        for source in (
            "'Thirty-six percent voted.'",
            "‘Thirty-six percent voted.’",
            '“Thirty-six percent voted.',
            "`Thirty-six percent`",
            "[survey](Thirty-six percent)",
            "https://example.com/thirty-six-percent",
        ):
            with self.subTest(source=source):
                result = apply_main_style_with_report(source)
                self.assertEqual(result.text, source)
                self.assertEqual(result.changes, ())
                self.assertEqual(result.findings, ())

    def test_invalid_meridiem_hours_are_not_legitimized(self):
        source = "The log says 13 PM and 9:75 AM."
        self.assertEqual(normalize_mechanical_forms(source), source)

    def test_quote_policy_is_rule_specific_and_literals_stay_protected(self):
        source = (
            'The US Chairman said COVID-19 rose 8 percent at 9PM. '
            '“The US Chairman said COVID-19 rose 8 percent at 9PM.” '
            '`The US Chairman said 8 percent`'
        )
        self.assertEqual(
            normalize_mechanical_forms(source),
            'The U.S. Chair said COVID rose 8% at 9 p.m. '
            '“The U.S. Chairman said COVID-19 rose 8% at 9 p.m.” '
            '`The US Chairman said 8 percent`',
        )

    def test_spoken_percent_and_time_forms_inside_straight_and_curly_quotes(self):
        source = (
            '“Eight percent arrived at four PM.” '
            '"One hundred twenty-three percent arrived at twelve AM."'
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            '“8% arrived at 4 p.m.” "123% arrived at 12 a.m."',
        )
        self.assertTrue(result.changes)
        self.assertTrue(all(change.speech_preserving for change in result.changes))
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )

    def test_sentence_start_guard_preserves_double_quote_rendering(self):
        for opening, closing in (('"', '"'), ("“", "”")):
            with self.subTest(opening=opening):
                lead = f"She said, {opening}The survey closed. "
                tail = f" supported it.{closing}"
                result = apply_main_style_with_report(
                    lead + "Thirty-six percent" + tail
                )
                self.assertEqual(result.text, lead + "36%" + tail)
                change, = result.changes
                self.assertTrue(change.speech_preserving)
                self.assertEqual(change.source_start, len(lead))
                self.assertEqual(change.before, "Thirty-six percent")

    def test_literal_regions_inside_quote_remain_hard_protected(self):
        source = '“US `US` https://example.com/US eight percent”'
        self.assertEqual(
            normalize_mechanical_forms(source),
            '“U.S. `US` https://example.com/US 8%”',
        )

    def test_unbalanced_quote_blocks_speech_preserving_mechanical_rules(self):
        source = 'He said, “US support was eight percent at four PM'
        self.assertEqual(normalize_mechanical_forms(source), source)

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
