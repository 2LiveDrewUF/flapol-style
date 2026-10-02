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


if __name__ == "__main__":
    unittest.main()
