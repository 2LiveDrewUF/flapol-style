import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import (
    apply_headline_style_with_report,
    apply_main_style_with_report,
    find_number_sign_flags,
    normalize_number_sign_forms,
)


class NumberSignTests(unittest.TestCase):
    def test_context_proven_number_sign_forms_are_normalized(self):
        source = (
            "Florida is ranked #3 and rose to #2. The #1-ranked team was the "
            "#4 seed. Executive Order #123 assigned Room #5. "
            "Florida Amendment #4 and ballot Amendment #2 passed."
        )
        self.assertEqual(
            normalize_number_sign_forms(source),
            "Florida is ranked No. 3 and rose to No. 2. The No. 1-ranked team "
            "was the No. 4 seed. Executive Order No. 123 assigned Room No. 5. "
            "Florida Amendment 4 and ballot Amendment 2 passed.",
        )

    def test_numeric_hashtag_word_boundary_is_not_mistaken_for_a_number(self):
        source = "The slogan was #8isEnough, not #8_is_Enough or #88isEnough."
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.findings, ())

    def test_punctuation_hyphen_space_and_end_are_valid_number_boundaries(self):
        source = "ranked #3, placed #4. It was #1-ranked and finished #2"
        self.assertEqual(
            normalize_number_sign_forms(source),
            "ranked No. 3, placed No. 4. It was No. 1-ranked and finished No. 2",
        )

    def test_quoted_hash_forms_and_hashtags_are_untouched_and_unflagged(self):
        source = (
            'She posted, “We’re #1! #8isEnough.” '
            'He called it "the #3 program".'
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.findings, ())

    def test_unbalanced_quote_fails_closed(self):
        source = 'She said, “We are ranked #1 and signed Executive Order #12'
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.findings, ())

    def test_literal_and_link_destinations_are_hard_protected(self):
        source = (
            "Ranked #3, `ranked #4`, and "
            "[ranked #5](https://example.com/#6)."
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            "Ranked No. 3, `ranked #4`, and "
            "[ranked No. 5](https://example.com/#6).",
        )
        self.assertEqual(result.findings, ())

    def test_unresolved_numeric_hash_forms_are_findings_only(self):
        source = "Issue #3 raised Question #2 about Amendment #4 and #2026."
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, source)
        self.assertEqual(
            [(item.rule_id, item.found, item.suggestion) for item in result.findings],
            [
                ("flapol.numbers.number-sign-review", "#3", "No. 3"),
                ("flapol.numbers.number-sign-review", "#2", "No. 2"),
                (
                    "flapol.numbers.amendment-number-sign-review",
                    "Amendment #4",
                    "Amendment 4",
                ),
                ("flapol.numbers.number-sign-review", "#2026", "No. 2026"),
            ],
        )
        for finding in result.findings:
            self.assertEqual(
                source[finding.source_start:finding.source_end],
                finding.found,
            )

    def test_report_uses_stable_rules_offsets_and_quote_classification(self):
        source = "Ranked #3 in Room #5 under Executive Order #12."
        result = apply_main_style_with_report(source)
        self.assertEqual(
            [change.rule_id for change in result.changes],
            [
                "flapol.numbers.ranking-number-sign",
                "flapol.numbers.executive-order-number-sign",
                "flapol.numbers.room-number-sign",
            ],
        )
        self.assertTrue(all(not change.speech_preserving for change in result.changes))
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )

    def test_headline_profile_applies_proven_forms_and_reports_the_rest(self):
        result = apply_headline_style_with_report(
            "Team Ranked #3 After Question #2"
        )
        self.assertEqual(result.text, "Team ranked No. 3 after question #2")
        self.assertEqual(
            [(item.found, item.suggestion) for item in result.findings],
            [("#2", "No. 2")],
        )

    def test_number_sign_pass_is_idempotent(self):
        source = "Ranked #3 under Executive Order #12 in Room #5."
        once = normalize_number_sign_forms(source)
        self.assertEqual(normalize_number_sign_forms(once), once)
        self.assertEqual(find_number_sign_flags(once), ())


if __name__ == "__main__":
    unittest.main()
