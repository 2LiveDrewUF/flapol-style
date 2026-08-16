import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.words import normalize_word_forms


class WordFormTests(unittest.TestCase):
    def test_approved_forms_are_normalized(self):
        self.assertEqual(
            normalize_word_forms(
                "A longtime frontrunner discussed health care at a press conference."
            ),
            "A longtime front-runner discussed healthcare at a news conference.",
        )

    def test_plural_and_house_hyphenation(self):
        self.assertEqual(
            normalize_word_forms(
                "The frontrunners held press conferences before the reelection vote."
            ),
            "The front-runners held news conferences before the re-election vote.",
        )

    def test_case_is_projected(self):
        self.assertEqual(
            normalize_word_forms("Press conference and HEALTH CARE"),
            "News conference and HEALTHCARE",
        )

    def test_protected_regions_are_unchanged(self):
        source = (
            'Health care changed. “Health care at a press conference.” '
            '[health care](https://example.com/health-care) `press conference`'
        )
        self.assertEqual(
            normalize_word_forms(source),
            'Healthcare changed. “Health care at a press conference.” '
            '[healthcare](https://example.com/health-care) `press conference`',
        )

    def test_rejected_or_unrelated_legacy_forms_are_not_changed(self):
        source = "Officials tried to preempt a child care dispute."
        self.assertEqual(normalize_word_forms(source), source)

    def test_title_cased_health_care_may_be_a_formal_name(self):
        source = "The Health Care District of Palm Beach County met Tuesday."
        self.assertEqual(normalize_word_forms(source), source)

    def test_word_pass_is_idempotent(self):
        source = "The frontrunner discussed health-care at a press conference."
        once = normalize_word_forms(source)
        self.assertEqual(normalize_word_forms(once), once)


if __name__ == "__main__":
    unittest.main()
