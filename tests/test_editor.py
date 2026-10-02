from datetime import date
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.editor import apply_main_style, apply_main_style_with_report


class MainEditorTests(unittest.TestCase):
    def test_main_pipeline_combines_implemented_rules(self):
        self.assertEqual(
            apply_main_style(
                "Governor Ron DeSantis held a press conference January 8th, 2026."
            ),
            "Gov. Ron DeSantis held a news conference Jan. 8, 2026.",
        )

    def test_main_pipeline_includes_safe_capitalization(self):
        self.assertEqual(
            apply_main_style(
                "president Joe Biden discussed the general election with the "
                "Leon County school board."
            ),
            "President Joe Biden discussed the General Election with the "
            "Leon County School Board.",
        )

    def test_main_pipeline_uses_explicit_publication_date(self):
        self.assertEqual(
            apply_main_style(
                "The news conference is Monday, January 5, 2026.",
                publication_date=date(2026, 1, 1),
            ),
            "The news conference is Monday.",
        )

    def test_main_pipeline_applies_only_speech_preserving_quote_rules(self):
        source = (
            'Governor Ron DeSantis discussed health care. '
            '“Governor Ron DeSantis discussed health care January 8th.”'
        )
        once = apply_main_style(source)
        self.assertEqual(
            once,
            'Gov. Ron DeSantis discussed healthcare. '
            '“Gov. Ron DeSantis discussed healthcare Jan. 8.”',
        )
        self.assertEqual(apply_main_style(once), once)

    def test_main_pipeline_reports_agriculture_commissioner_changes(self):
        source = "Commissioner of Agriculture Wilton Simpson spoke."
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            "Agriculture Commissioner Wilton Simpson spoke.",
        )
        self.assertEqual(
            [change.rule_id for change in result.changes],
            ["flapol.titles.agriculture-commissioner-order"],
        )
        self.assertTrue(
            all(not change.speech_preserving for change in result.changes)
        )
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )
        self.assertEqual(apply_main_style(result.text), result.text)

    def test_main_pipeline_reports_quote_capitalization_without_reordering(self):
        source = 'She said, “the commissioner of agriculture called.”'
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            'She said, “the Commissioner of Agriculture called.”',
        )
        self.assertEqual(len(result.changes), 1)
        change = result.changes[0]
        self.assertEqual(
            change.rule_id,
            "flapol.titles.agriculture-commissioner-capitalization",
        )
        self.assertTrue(change.speech_preserving)
        self.assertEqual(
            source[change.source_start:change.source_end],
            change.before,
        )

    def test_main_pipeline_drops_florida_before_governor_and_full_name(self):
        source = (
            "Florida Governor Ron DeSantis met California Governor Gavin Newsom "
            "and former Florida Gov. Jeb Bush."
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            "Gov. Ron DeSantis met California Gov. Gavin Newsom and former "
            "Gov. Jeb Bush.",
        )
        self.assertEqual(
            [change.rule_id for change in result.changes],
            [
                "flapol.titles.florida-governor-home-state",
                "flapol.titles.florida-governor-home-state",
                "flapol.titles.title-governor",
                "flapol.titles.title-governor",
            ],
        )
        for change in result.changes:
            self.assertEqual(
                source[change.source_start:change.source_end],
                change.before,
            )
        self.assertEqual(apply_main_style(result.text), result.text)

    def test_florida_governor_rule_requires_a_full_name(self):
        source = "The Florida governor met the California governor."
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            "The Florida Governor met the California Governor.",
        )
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertEqual(
            finding.rule_id,
            "flapol.titles.florida-governor-without-name",
        )
        self.assertEqual(finding.found, "Florida Governor")
        self.assertEqual(finding.suggestion, "Governor")
        self.assertEqual(
            source[finding.source_start:finding.source_end],
            "Florida governor",
        )

    def test_florida_governor_flag_excludes_quotes_and_formal_mansion_name(self):
        source = (
            '“The Florida governor called,” she said outside the '
            "Florida Governor's Mansion."
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            '“The Florida Governor called,” she said outside the '
            "Florida Governor's Mansion.",
        )
        self.assertEqual(result.findings, ())

    def test_florida_label_is_preserved_in_quote_while_title_is_abbreviated(self):
        source = (
            'She said, “Florida Governor Ron DeSantis called.” '
            'He replied, "Florida Governor Ron DeSantis answered."'
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            'She said, “Florida Gov. Ron DeSantis called.” '
            'He replied, "Florida Gov. Ron DeSantis answered."',
        )
        self.assertEqual(len(result.changes), 2)
        self.assertTrue(
            all(
                change.rule_id == "flapol.titles.title-governor"
                and change.speech_preserving
                for change in result.changes
            )
        )

    def test_florida_governor_rule_protects_literals_and_uncertain_quotes(self):
        source = (
            '`Florida Governor Ron DeSantis` is literal. '
            'She said, "Florida Governor Ron DeSantis called'
        )
        self.assertEqual(apply_main_style(source), source)

    def test_florida_governor_rule_handles_bold_full_name(self):
        self.assertEqual(
            apply_main_style("Florida Governor **Ron DeSantis** spoke."),
            "Gov. **Ron DeSantis** spoke.",
        )


if __name__ == "__main__":
    unittest.main()
