from datetime import date
import pathlib
import re
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style import apply_main_style, apply_main_style_with_report
from flapol_style.capitalization import load_capitalization_rules
from flapol_style.titles import load_title_abbreviations
from flapol_style.words import load_word_preferences


class ReportingTests(unittest.TestCase):
    def test_registry_rule_ids_are_unique_and_stable_names(self):
        ids = [
            *(f"flapol.words.{record['id']}" for record in load_word_preferences()),
            *(
                f"flapol.titles.{record['id']}"
                for record in load_title_abbreviations()
            ),
        ]
        capitalization = load_capitalization_rules()
        for family in (
            "automatic_exact",
            "before_name_titles",
            "governmental_bodies",
            "context_flags",
        ):
            ids.extend(
                f"flapol.capitalization.{record['id']}"
                for record in capitalization[family]
            )
        self.assertEqual(len(ids), len(set(ids)))
        for rule_id in ids:
            self.assertRegex(
                rule_id,
                re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z0-9-]+)+$"),
            )

    def test_simple_and_reported_apis_share_the_same_pipeline(self):
        source = (
            "Governor Ron DeSantis discussed health care at a press conference "
            "January 8th, 2026."
        )
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, apply_main_style(source))
        self.assertEqual(
            result.text,
            "Gov. Ron DeSantis discussed healthcare at a news conference "
            "Jan. 8, 2026.",
        )

    def test_every_change_has_a_stable_rule_and_original_source_coordinates(self):
        source = "Governor Ron DeSantis discussed health care January 8th."
        result = apply_main_style_with_report(source)
        self.assertTrue(result.changes)
        self.assertEqual(
            [change.sequence for change in result.changes],
            list(range(1, len(result.changes) + 1)),
        )
        for change in result.changes:
            self.assertTrue(change.rule_id)
            self.assertTrue(change.authority)
            self.assertEqual(change.action, "AUTO_FIX")
            self.assertLessEqual(change.source_start, change.source_end)
            self.assertLessEqual(change.source_end, len(source))

        healthcare = next(
            change
            for change in result.changes
            if change.rule_id == "flapol.words.healthcare-one-word"
        )
        self.assertEqual(
            source[healthcare.source_start:healthcare.source_end],
            "health care",
        )
        month = next(
            change
            for change in result.changes
            if change.rule_id == "ap.dates.month-with-numbered-day"
        )
        self.assertEqual(source[month.source_start:month.source_end], "January")

    def test_relative_date_report_uses_explicit_context_rule_id(self):
        source = "The meeting is Monday, January 5, 2026."
        result = apply_main_style_with_report(
            source, publication_date=date(2026, 1, 1)
        )
        self.assertEqual(result.text, "The meeting is Monday.")
        self.assertIn(
            "ap.dates.weekday-window",
            [change.rule_id for change in result.changes],
        )

    def test_context_findings_use_original_offsets(self):
        source = "Governor Ron DeSantis spoke in the spring."
        result = apply_main_style_with_report(source)
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertEqual(finding.rule_id, "flapol.capitalization.season-spring")
        self.assertEqual(
            source[finding.source_start:finding.source_end],
            "spring",
        )
        self.assertEqual(finding.action, "FLAG")

    def test_speech_preserving_quote_changes_are_reported_but_flags_stay_out(self):
        source = '“Governor Ron DeSantis discussed health care in the spring.”'
        result = apply_main_style_with_report(source)
        self.assertEqual(
            result.text,
            '“Gov. Ron DeSantis discussed healthcare in the spring.”',
        )
        self.assertTrue(result.changes)
        self.assertTrue(all(change.speech_preserving for change in result.changes))
        self.assertEqual(result.findings, ())

    def test_second_report_is_idempotent(self):
        source = "Governor Ron DeSantis discussed health care January 8th."
        first = apply_main_style_with_report(source)
        second = apply_main_style_with_report(first.text)
        self.assertEqual(second.text, first.text)
        self.assertEqual(second.changes, ())


if __name__ == "__main__":
    unittest.main()
