import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.titles import (
    abbreviate_titles_before_names,
    load_title_abbreviations,
    normalize_office_title_forms,
)


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
            "U.S. Sen. Rick Scott and Representative Anna Eskamani.",
        )

    def test_unqualified_legislative_title_requires_identity_context(self):
        source = (
            "Representative Anna Eskamani met Senators Rick Scott and "
            "Ashley Moody."
        )
        self.assertEqual(abbreviate_titles_before_names(source), source)

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


class OfficeTitleFormTests(unittest.TestCase):
    def test_commissioner_of_agriculture_uses_house_form(self):
        self.assertEqual(
            normalize_office_title_forms(
                "The Commissioner of Agriculture spoke with "
                "commissioner of agriculture Wilton Simpson."
            ),
            "The Agriculture Commissioner spoke with "
            "Agriculture Commissioner Wilton Simpson.",
        )

    def test_geographic_modifiers_are_retained(self):
        self.assertEqual(
            normalize_office_title_forms(
                "Florida Commissioner of Agriculture Wilton Simpson met the "
                "Florida agriculture commissioner."
            ),
            "Florida Agriculture Commissioner Wilton Simpson met the "
            "Florida Agriculture Commissioner.",
        )

    def test_other_state_geography_is_retained(self):
        self.assertEqual(
            normalize_office_title_forms(
                "Georgia Commissioner of Agriculture Tyler Harper spoke."
            ),
            "Georgia Agriculture Commissioner Tyler Harper spoke.",
        )

    def test_unrelated_federal_title_and_plural_are_untouched(self):
        source = (
            "The USDA Secretary met several agriculture commissioners and the "
            "commissioner of agricultural services."
        )
        self.assertEqual(normalize_office_title_forms(source), source)

    def test_full_agriculture_and_consumer_services_title_is_untouched(self):
        source = (
            "Commissioner of Agriculture and Consumer Services; "
            "commissioner of agriculture and consumer services"
        )
        self.assertEqual(normalize_office_title_forms(source), source)

    def test_quote_capitalization_preserves_the_spoken_order(self):
        source = (
            'Commissioner of Agriculture appeared outside the quote. '
            '“commissioner of agriculture is what I said,” she replied. '
            '"florida agriculture commissioner was my phrase," he added.'
        )
        self.assertEqual(
            normalize_office_title_forms(source),
            'Agriculture Commissioner appeared outside the quote. '
            '“Commissioner of Agriculture is what I said,” she replied. '
            '"florida Agriculture Commissioner was my phrase," he added.',
        )

    def test_unbalanced_quote_and_literal_fail_closed(self):
        source = (
            '`Commissioner of Agriculture` is a literal. '
            'He said, "Commissioner of Agriculture'
        )
        self.assertEqual(normalize_office_title_forms(source), source)

    def test_office_title_form_is_idempotent(self):
        source = "Commissioner of Agriculture Wilton Simpson spoke."
        once = normalize_office_title_forms(source)
        self.assertEqual(normalize_office_title_forms(once), once)


if __name__ == "__main__":
    unittest.main()
