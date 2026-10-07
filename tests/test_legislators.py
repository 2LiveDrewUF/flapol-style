from datetime import date
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import (
    LegislatorIdentity,
    OfficeholderBookStaleError,
    apply_main_style,
    apply_main_style_with_report,
    resolve_legislator_context,
)


AS_OF = date(2026, 10, 2)


class LegislatorStyleTests(unittest.TestCase):
    def apply(self, text, overlays=()):
        return apply_main_style_with_report(
            text,
            officeholder_as_of=AS_OF,
            legislator_overlays=overlays,
        )

    def test_state_only_titles_use_unqualified_abbreviations(self):
        source = (
            "Representative Anna Eskamani and Senator Carlos Guillermo Smith "
            "spoke."
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "Rep. Anna Eskamani and Sen. Carlos Guillermo Smith spoke.",
        )
        self.assertEqual(
            [change.rule_id for change in result.changes],
            [
                "flapol.legislators.jurisdiction-before-name",
                "flapol.legislators.jurisdiction-before-name",
            ],
        )
        self.assertEqual(result.findings, ())

    def test_federal_only_titles_receive_us_qualification(self):
        result = self.apply(
            "Representative Darren Soto and Senator Rick Scott spoke."
        )
        self.assertEqual(
            result.text,
            "U.S. Rep. Darren Soto and U.S. Sen. Rick Scott spoke.",
        )

    def test_mixed_document_distinguishes_state_and_federal_lawmakers(self):
        source = (
            "Florida Representative Darren Soto met Florida Representative "
            "Anna Eskamani."
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "U.S. Rep. Darren Soto met state Rep. Anna Eskamani.",
        )
        self.assertTrue(
            all(
                change.rule_id
                == "flapol.legislators.jurisdiction-before-name"
                for change in result.changes
            )
        )

    def test_middle_initial_may_be_omitted_when_identity_stays_unambiguous(self):
        context = resolve_legislator_context(
            "Representative Anna Eskamani spoke.",
            as_of=AS_OF,
        )
        self.assertEqual(context.mode, "state-only")
        self.assertEqual(context.identities[0].name, "Anna V. Eskamani")

    def test_state_and_federal_plural_lists_use_document_mode(self):
        state = self.apply(
            "Representatives Anna Eskamani, Fentrice Driskell and "
            "Michele K. Rayner spoke."
        )
        federal = self.apply(
            "Representatives Darren Soto and Maxwell Frost spoke."
        )
        self.assertEqual(
            state.text,
            "Reps. Anna Eskamani, Fentrice Driskell and Michele K. Rayner "
            "spoke.",
        )
        self.assertEqual(
            federal.text,
            "U.S. Reps. Darren Soto and Maxwell Frost spoke.",
        )

    def test_state_and_federal_senate_plural_lists_use_document_mode(self):
        state = self.apply(
            "Senators Carlos Guillermo Smith and Lori Berman spoke."
        )
        federal = self.apply("Senators Rick Scott and Ashley Moody spoke.")
        self.assertEqual(
            state.text,
            "Sens. Carlos Guillermo Smith and Lori Berman spoke.",
        )
        self.assertEqual(
            federal.text,
            "U.S. Sens. Rick Scott and Ashley Moody spoke.",
        )

    def test_mixed_document_qualifies_a_state_only_plural_list(self):
        result = self.apply(
            "Representatives Anna Eskamani and Fentrice Driskell met "
            "U.S. Rep. Darren Soto."
        )
        self.assertEqual(
            result.text,
            "state Reps. Anna Eskamani and Fentrice Driskell met "
            "U.S. Rep. Darren Soto.",
        )

    def test_shared_plural_title_is_flagged_for_mixed_levels(self):
        source = "Representatives Darren Soto and Anna Eskamani spoke."
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "Reps. Darren Soto and Anna Eskamani spoke.",
        )
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertEqual(
            finding.rule_id,
            "flapol.legislators.jurisdiction-plural",
        )
        self.assertEqual(
            source[finding.source_start:finding.source_end],
            finding.found,
        )

    def test_attributions_follow_single_level_document_mode(self):
        federal = self.apply(
            '"Text," the Representative said after Darren Soto spoke.'
        )
        state = self.apply(
            '"Text," the U.S. Representative said after Anna Eskamani spoke.'
        )
        self.assertEqual(
            federal.text,
            '"Text," the U.S. Representative said after Darren Soto spoke.',
        )
        self.assertEqual(
            state.text,
            '"Text," the Representative said after Anna Eskamani spoke.',
        )
        federal_senate = self.apply(
            '"Text," the Senator said after Rick Scott spoke.'
        )
        state_senate = self.apply(
            '"Text," the U.S. Senator said after Carlos Guillermo Smith spoke.'
        )
        self.assertEqual(
            federal_senate.text,
            '"Text," the U.S. Senator said after Rick Scott spoke.',
        )
        self.assertEqual(
            state_senate.text,
            '"Text," the Senator said after Carlos Guillermo Smith spoke.',
        )

    def test_mixed_document_attribution_is_flagged_without_guessing_speaker(self):
        source = (
            '"Text," the Representative said after Darren Soto met '
            "Anna Eskamani."
        )
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(
            result.findings[0].rule_id,
            "flapol.legislators.jurisdiction-attribution",
        )

    def test_mixed_document_preserves_explicit_us_attribution(self):
        source = (
            '"Text," the U.S. Representative said after Darren Soto met '
            "Anna Eskamani."
        )
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.findings, ())

    def test_mixed_document_normalizes_explicit_florida_attribution(self):
        source = (
            '"Text," the Florida Representative said after Darren Soto met '
            "Anna Eskamani."
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            '"Text," the state Representative said after Darren Soto met '
            "Anna Eskamani.",
        )
        self.assertEqual(result.findings, ())

    def test_quote_preserves_spoken_jurisdiction_but_abbreviates_title(self):
        source = (
            "She said, “Florida Representative Anna Eskamani called.” "
            'He replied, "Florida Senator Carlos Guillermo Smith answered."'
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "She said, “Florida Rep. Anna Eskamani called.” "
            'He replied, "Florida Sen. Carlos Guillermo Smith answered."',
        )
        self.assertTrue(result.changes)
        self.assertTrue(
            all(change.speech_preserving for change in result.changes)
        )
        second = self.apply(result.text)
        self.assertEqual(second.text, result.text)
        self.assertEqual(second.changes, ())

    def test_quote_does_not_abbreviate_an_unknown_identity(self):
        source = 'She said, "Representative Jane Doe called."'
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())
        self.assertEqual(result.findings, ())

    def test_quote_abbreviates_plural_title_without_changing_jurisdiction(self):
        result = self.apply(
            'She said, "Florida Representatives Anna Eskamani and '
            'Fentrice Driskell called."'
        )
        self.assertEqual(
            result.text,
            'She said, "Florida Reps. Anna Eskamani and Fentrice Driskell '
            'called."',
        )
        self.assertEqual(len(result.changes), 1)
        self.assertEqual(
            result.changes[0].rule_id,
            "flapol.legislators.identity-backed-plural-title-abbreviation",
        )
        self.assertTrue(result.changes[0].speech_preserving)

    def test_name_in_quote_counts_toward_mode_without_mutating_jurisdiction(self):
        result = self.apply(
            '“Representative Darren Soto called.” Representative Anna '
            "Eskamani answered."
        )
        self.assertEqual(
            result.text,
            '“Rep. Darren Soto called.” state Rep. Anna Eskamani answered.',
        )

    def test_unknown_and_wrong_chamber_identities_are_findings(self):
        unknown = self.apply("Florida Representative Jane Doe spoke.")
        wrong = self.apply("Senator Anna Eskamani spoke.")
        self.assertEqual(unknown.text, "Florida Representative Jane Doe spoke.")
        self.assertEqual(len(unknown.findings), 1)
        self.assertIn("Confirm the lawmaker's level", unknown.findings[0].suggestion)
        self.assertEqual(wrong.text, "Senator Anna Eskamani spoke.")
        self.assertEqual(len(wrong.findings), 1)
        self.assertIn("identifies Anna V. Eskamani", wrong.findings[0].suggestion)

    def test_former_office_is_flagged_without_current_role_inference(self):
        source = (
            "Former Florida Representative Darren Soto met Representative "
            "Anna Eskamani."
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "Former Florida Representative Darren Soto met Rep. Anna Eskamani.",
        )
        self.assertEqual(len(result.findings), 1)
        self.assertIn("historical office", result.findings[0].suggestion)

    def test_other_state_lawmaker_requires_an_overlay(self):
        result = self.apply("Georgia Representative Jane Doe spoke.")
        self.assertEqual(result.text, "Georgia Representative Jane Doe spoke.")
        self.assertEqual(len(result.findings), 1)
        self.assertIn("Confirm the lawmaker's level", result.findings[0].suggestion)

    def test_literals_and_unbalanced_quotes_fail_closed(self):
        source = (
            "`Florida Representative Anna Eskamani` is literal. "
            'She said, "Florida Representative Darren Soto called'
        )
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())
        self.assertEqual(result.findings, ())

    def test_link_destination_is_hard_protected(self):
        source = "[record](Florida Representative Anna Eskamani)"
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())
        self.assertEqual(result.findings, ())

    def test_url_and_email_remain_character_exact(self):
        source = (
            "Representative Anna Eskamani cited "
            "https://example.com/Representative%20Darren%20Soto and "
            "representative.anna.eskamani@example.com."
        )
        result = self.apply(source)
        self.assertEqual(
            result.text,
            "Rep. Anna Eskamani cited "
            "https://example.com/Representative%20Darren%20Soto and "
            "representative.anna.eskamani@example.com.",
        )

    def test_bold_name_is_normalized_without_changing_bold_span(self):
        result = self.apply("Florida Representative **Anna Eskamani** spoke.")
        self.assertEqual(result.text, "Rep. **Anna Eskamani** spoke.")

    def test_caller_overlay_adds_identity_and_aliases(self):
        overlay = LegislatorIdentity(
            name="Jane Q. Doe",
            aliases=("Jane Doe",),
            level="state",
            chamber="house",
        )
        result = self.apply(
            "Florida Representative Jane Doe spoke.",
            overlays=(overlay,),
        )
        self.assertEqual(result.text, "Rep. Jane Doe spoke.")
        self.assertEqual(result.findings, ())

    def test_ambiguous_overlay_alias_is_flagged(self):
        overlays = (
            LegislatorIdentity(
                name="Jane Q. Doe",
                aliases=("Jane Doe",),
                level="state",
                chamber="house",
            ),
            LegislatorIdentity(
                name="Jane R. Doe",
                aliases=("Jane Doe",),
                level="federal",
                chamber="house",
            ),
        )
        result = self.apply(
            "Florida Representative Jane Doe spoke.",
            overlays=overlays,
        )
        self.assertEqual(result.text, "Florida Representative Jane Doe spoke.")
        self.assertEqual(len(result.findings), 1)
        self.assertIn("Confirm the lawmaker's level", result.findings[0].suggestion)

    def test_overlay_requires_explicit_officeholder_date(self):
        overlay = LegislatorIdentity(
            name="Jane Doe",
            level="state",
            chamber="house",
        )
        with self.assertRaises(ValueError):
            apply_main_style(
                "Representative Jane Doe spoke.",
                legislator_overlays=(overlay,),
            )

    def test_identity_rules_require_roster_adjudication_when_stale(self):
        with self.assertRaises(OfficeholderBookStaleError):
            apply_main_style(
                "Representative Anna Eskamani spoke.",
                officeholder_as_of=date(2026, 11, 4),
            )

    def test_legacy_call_without_identity_date_does_not_infer_a_mode(self):
        self.assertEqual(
            apply_main_style("Representative Darren Soto spoke."),
            "Representative Darren Soto spoke.",
        )

    def test_nonlegislative_representatives_are_not_changed_or_flagged(self):
        sources = (
            "Santa Rosa County School District representative Joey Harrell spoke.",
            "The applicant representative Joey Harrell spoke.",
            "LEAD representatives Brad Weber and Mike Kelly spoke.",
            "Former District 6 representatives Karl Nurse and Frank Peterman spoke.",
            "Florida House of Representatives Legislative Fellows Program",
        )
        for source in sources:
            with self.subTest(source=source):
                result = self.apply(source)
                self.assertEqual(result.text, source)
                self.assertEqual(result.changes, ())
                self.assertEqual(result.findings, ())

    def test_abbreviated_unknown_lawmaker_title_is_preserved_and_flagged(self):
        source = "Sen. René García discussed the Miami-Dade budget."
        result = self.apply(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(
            result.findings[0].rule_id,
            "flapol.legislators.jurisdiction-before-name",
        )

    def test_edits_retain_source_coordinates_and_text_is_idempotent(self):
        source = "Representative Darren Soto met Representative Anna Eskamani."
        first = self.apply(source)
        self.assertEqual(
            first.text,
            "U.S. Rep. Darren Soto met state Rep. Anna Eskamani.",
        )
        for change in first.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )
        second = self.apply(first.text)
        self.assertEqual(second.text, first.text)
        self.assertEqual(second.changes, ())
        self.assertEqual(second.findings, ())


if __name__ == "__main__":
    unittest.main()
