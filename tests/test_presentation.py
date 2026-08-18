import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import (
    apply_presentation_style,
    apply_presentation_style_with_report,
    load_bolding_rules,
)


class PresentationStyleTests(unittest.TestCase):
    def test_public_bolding_registry_loads(self):
        rules = load_bolding_rules()
        self.assertIn("Gov.", rules["title_prefixes"])
        self.assertIn("Lt. Gov.", rules["title_prefixes"])
        self.assertIn("State Rep.", rules["title_prefixes"])
        self.assertIn("State Sen.", rules["title_prefixes"])
        self.assertIn("commissioners", rules["nonperson_office_terms"])

    def test_inline_hyperlink_text_is_bolded_without_changing_destination(self):
        self.assertEqual(
            apply_presentation_style(
                "Read [Florida Politics](https://floridapolitics.com/story?q=1)."
            ),
            "Read [**Florida Politics**](https://floridapolitics.com/story?q=1).",
        )

    def test_reference_hyperlink_text_is_bolded(self):
        self.assertEqual(
            apply_presentation_style("Read [Florida Politics][flapol]."),
            "Read [**Florida Politics**][flapol].",
        )

    def test_image_alt_text_is_not_treated_as_a_hyperlink(self):
        source = "![Florida Politics](logo.png)"
        self.assertEqual(apply_presentation_style(source), source)

    def test_outer_bold_hyperlink_is_already_permitted(self):
        source = "**[Florida Politics](https://floridapolitics.com)**"
        result = apply_presentation_style_with_report(
            source, person_context_complete=True
        )
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())

    def test_hyperlink_bold_takes_precedence_over_title_narrowing(self):
        source = "[**Gov. Ron DeSantis**](https://example.com)"
        self.assertEqual(apply_presentation_style(source), source)

    def test_link_destination_is_unchanged_and_never_reclassified_as_a_person(self):
        source = "[Cord Byrd](https://example.com/Cord-Byrd)"
        self.assertEqual(
            apply_presentation_style(
                source, ("Cord Byrd",), person_context_complete=True
            ),
            "[**Cord Byrd**](https://example.com/Cord-Byrd)",
        )

    def test_known_title_is_moved_outside_bold_without_a_roster(self):
        forms = {
            "**Governor Ron DeSantis**": "Governor **Ron DeSantis**",
            "**Gov. Ron DeSantis**": "Gov. **Ron DeSantis**",
            "**Lieutenant Governor Jay Collins**": "Lieutenant Governor **Jay Collins**",
            "**Lt. Gov. Jay Collins**": "Lt. Gov. **Jay Collins**",
            "**Secretary of State Cord Byrd**": "Secretary of State **Cord Byrd**",
            "**U.S. Sen. Marco Rubio**": "U.S. Sen. **Marco Rubio**",
            "**U.S. Rep. Byron Donalds**": "U.S. Rep. **Byron Donalds**",
            "**Sen. Shevrin Jones**": "Sen. **Shevrin Jones**",
            "**Rep. Anna Eskamani**": "Rep. **Anna Eskamani**",
            "**State Sen. Lori Berman**": "State Sen. **Lori Berman**",
            "**State Sen Lori Berman**": "State Sen **Lori Berman**",
            "**State Rep. Michele Rayner**": "State Rep. **Michele Rayner**",
            "**State Rep Michele Rayner**": "State Rep **Michele Rayner**",
            "**CEO Jane Smith**": "CEO **Jane Smith**",
            "**CFO John Smith**": "CFO **John Smith**",
        }
        for source, expected in forms.items():
            with self.subTest(source=source):
                result = apply_presentation_style_with_report(source)
                self.assertEqual(result.text, expected)
                self.assertEqual(result.findings, ())

    def test_officeholder_group_bolding_is_removed_without_a_roster(self):
        phrases = (
            "Flagler County commissioners",
            "Governors",
            "state reps.",
            "State Sens.",
            "representatives",
            "Senators",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertEqual(
                    apply_presentation_style(f"**{phrase}** approved it."),
                    f"{phrase} approved it.",
                )

    def test_flagler_county_commissioners_example_loses_only_bold_markup(self):
        source = (
            "**Flagler County commissioners** have approved a 190-foot "
            "telecommunications tower near homes in the Hunters Ridge "
            "development, overriding a unanimous recommendation of denial "
            "from the county's planning and development board."
        )
        self.assertEqual(
            apply_presentation_style(source),
            source.replace("**", ""),
        )

    def test_officeholder_group_remains_bold_when_it_is_link_text(self):
        source = "[**Flagler County commissioners**](https://example.com)"
        self.assertEqual(apply_presentation_style(source), source)

    def test_supplied_person_is_bolded_only_on_first_reference(self):
        source = "Cord Byrd spoke. Cord Byrd later voted."
        self.assertEqual(
            apply_presentation_style(source, ("Cord Byrd",)),
            "**Cord Byrd** spoke. Cord Byrd later voted.",
        )

    def test_supplied_person_narrows_arbitrary_descriptive_bold(self):
        source = "**the longtime elections official Cord Byrd** spoke."
        self.assertEqual(
            apply_presentation_style(source, ("Cord Byrd",)),
            "the longtime elections official **Cord Byrd** spoke.",
        )

    def test_complete_person_context_removes_every_other_nonlink_bold(self):
        source = (
            "**Flagler County commissioners** heard **Cord Byrd** discuss "
            "**the proposal** with [county officials](https://example.com)."
        )
        self.assertEqual(
            apply_presentation_style(
                source, ("Cord Byrd",), person_context_complete=True
            ),
            "Flagler County commissioners heard **Cord Byrd** discuss "
            "the proposal with [**county officials**](https://example.com).",
        )

    def test_incomplete_context_flags_unknown_bold_instead_of_removing_it(self):
        source = "**Cord Byrd** discussed **the proposal**."
        result = apply_presentation_style_with_report(source, ("Cord Byrd",))
        self.assertEqual(result.text, source)
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(
            result.findings[0].rule_id,
            "flapol.presentation.unverified-nonlink-bold",
        )
        self.assertEqual(result.findings[0].found, "**the proposal**")

    def test_empty_person_context_must_be_explicitly_complete_for_cleanup(self):
        source = "This has **general emphasis**."
        incomplete = apply_presentation_style_with_report(source)
        complete = apply_presentation_style_with_report(
            source, person_context_complete=True
        )
        self.assertEqual(incomplete.text, source)
        self.assertEqual(len(incomplete.findings), 1)
        self.assertEqual(complete.text, "This has general emphasis.")
        self.assertEqual(complete.findings, ())

    def test_complete_context_does_not_preserve_an_unsupplied_title_guess(self):
        self.assertEqual(
            apply_presentation_style(
                "**Secretary of State Cord Byrd** spoke.",
                person_context_complete=True,
            ),
            "Secretary of State Cord Byrd spoke.",
        )

    def test_invalid_person_context_fails_closed(self):
        with self.assertRaises(ValueError):
            apply_presentation_style("Text", ("**Cord Byrd**",))

    def test_balanced_quote_allows_speech_neutral_presentation_rendering(self):
        source = '“**Gov. Ron DeSantis** linked [the order](https://example.com).”'
        result = apply_presentation_style_with_report(source)
        self.assertEqual(
            result.text,
            '“Gov. **Ron DeSantis** linked [**the order**](https://example.com).”',
        )
        self.assertTrue(result.changes)
        self.assertTrue(all(change.speech_preserving for change in result.changes))

        straight = '"[the order](https://example.com)," she said.'
        self.assertEqual(
            apply_presentation_style(straight),
            '"[**the order**](https://example.com)," she said.',
        )

    def test_inline_and_fenced_code_are_hard_protected(self):
        source = (
            "`[code link](https://example.com)`\n"
            "```md\n**State Reps.**\n[link](https://example.com)\n```\n"
            "[outside](https://example.com)"
        )
        self.assertEqual(
            apply_presentation_style(source),
            source.replace(
                "[outside](https://example.com)",
                "[**outside**](https://example.com)",
            ),
        )

    def test_unbalanced_quote_and_code_fail_closed(self):
        source = (
            '“**Gov. Ron DeSantis** linked [the order](https://example.com).\n'
            '`[code link](https://example.com)`\n'
            '```\n**State Reps.**\n'
        )
        self.assertEqual(apply_presentation_style(source), source)

    def test_changes_retain_original_source_coordinates(self):
        source = "**Secretary of State Cord Byrd** linked [the page](https://x.test)."
        result = apply_presentation_style_with_report(source)
        self.assertEqual(len(result.changes), 2)
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )

    def test_presentation_pass_is_idempotent(self):
        source = (
            "**Secretary of State Cord Byrd** met **commissioners** at "
            "[Florida Politics](https://floridapolitics.com)."
        )
        first = apply_presentation_style_with_report(source)
        second = apply_presentation_style_with_report(first.text)
        self.assertEqual(second.text, first.text)
        self.assertEqual(second.changes, ())
        self.assertEqual(second.findings, ())


if __name__ == "__main__":
    unittest.main()
