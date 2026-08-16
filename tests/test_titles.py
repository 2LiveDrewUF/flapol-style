import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.titles import abbreviate_titles_before_names, load_title_abbreviations


class TitleAbbreviationTests(unittest.TestCase):
    def test_every_registry_rule_declares_quote_policy(self):
        self.assertTrue(load_title_abbreviations())
        for record in load_title_abbreviations():
            self.assertIs(type(record.get("speech_preserving")), bool)

    def test_public_titles_before_full_names_are_abbreviated(self):
        self.assertEqual(
            abbreviate_titles_before_names(
                "Governor Ron DeSantis met Lieutenant Governor Jeanette Nuñez, "
                "U.S. Senator Rick Scott and Representative Anna Eskamani."
            ),
            "Gov. Ron DeSantis met Lt. Gov. Jeanette Nuñez, "
            "U.S. Sen. Rick Scott and Rep. Anna Eskamani.",
        )

    def test_c_suite_titles_may_use_initialisms_on_first_reference(self):
        self.assertEqual(
            abbreviate_titles_before_names(
                "Chief Executive Officer Jane Smith met Chief Financial Officer John Doe."
            ),
            "CEO Jane Smith met CFO John Doe.",
        )

    def test_title_alone_or_after_name_is_not_abbreviated(self):
        source = "The Governor spoke. Ron DeSantis, the Governor, responded."
        self.assertEqual(abbreviate_titles_before_names(source), source)

    def test_lowercase_words_are_not_mistaken_for_a_name(self):
        source = "The Governor general election memo was withdrawn."
        self.assertEqual(abbreviate_titles_before_names(source), source)

    def test_state_attorney_is_not_abbreviated(self):
        source = "State Attorney Jack Campbell spoke."
        self.assertEqual(abbreviate_titles_before_names(source), source)

    def test_title_abbreviation_is_speech_preserving_inside_quotation(self):
        source = 'Governor Ron DeSantis spoke. “Governor Ron DeSantis called.”'
        self.assertEqual(
            abbreviate_titles_before_names(source),
            'Gov. Ron DeSantis spoke. “Gov. Ron DeSantis called.”',
        )

    def test_unbalanced_quote_blocks_title_abbreviation(self):
        source = 'He said, "Governor Ron DeSantis called'
        self.assertEqual(abbreviate_titles_before_names(source), source)

    def test_corporate_initialism_does_not_pass_read_aloud_test_in_quote(self):
        source = '“Chief Executive Officer Jane Smith called,” he said.'
        self.assertEqual(abbreviate_titles_before_names(source), source)

    def test_title_before_bold_full_name_is_abbreviated(self):
        self.assertEqual(
            abbreviate_titles_before_names("Governor **Ron DeSantis** spoke."),
            "Gov. **Ron DeSantis** spoke.",
        )

    def test_title_pass_is_idempotent(self):
        source = "U.S. Representative Kathy Castor spoke."
        once = abbreviate_titles_before_names(source)
        self.assertEqual(abbreviate_titles_before_names(once), once)


if __name__ == "__main__":
    unittest.main()
