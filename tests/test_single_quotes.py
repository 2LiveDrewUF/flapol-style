"""Single-quoted speech is protected; ordinary apostrophes stay narration."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from flapol_style import (
    apply_main_style_with_report,
    apply_headline_style_with_report,
    apply_presentation_style_with_report,
    find_protected_spans,
)

BILL_RULE = "flapol.usage.numbered-bill-abbreviation"


class SingleQuotationTests(unittest.TestCase):
    def assert_closed(self, source):
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, source)
        self.assertEqual(result.changes, ())
        self.assertEqual(result.findings, ())
        again = apply_main_style_with_report(result.text)
        self.assertEqual(again, result)

    def test_consumer_reproduction_straight_and_curly_single_quotes(self):
        for source in [
            "She said, 'House Bill 123 and Senate bill 24.'",
            "She said, ‘House Bill 123 and Senate bill 24.’",
        ]:
            with self.subTest(source=source):
                self.assert_closed(source)

    def test_ordinary_word_edit_cannot_enter_single_quoted_speech(self):
        for source in ["She said, 'press conference.'", "She said, ‘press conference.’"]:
            self.assert_closed(source)

    def test_single_quotes_remain_closed_to_speech_preserving_rules(self):
        for source in ["'US and health care at 4 PM.'", "‘US and health care at 4 PM.’"]:
            self.assert_closed(source)
            spans = find_protected_spans(source, allow_balanced_quotations=True)
            self.assertTrue(any(s.start == 0 and s.end == len(source) for s in spans))

    def test_contractions_names_and_possessives_do_not_hide_narration(self):
        for prefix in ["Don't change", "D’Angelo's", "O'Neill’s", "The writers'",
                       "The writers’", "James'", "James’", "'90s", "’26",
                       "'Cause", "Rock 'n' roll"]:
            source = f"{prefix} House bill 123 advances."
            with self.subTest(source=source):
                result = apply_main_style_with_report(source)
                self.assertEqual(result.text, source)
                self.assertEqual([f.suggestion for f in result.findings
                                  if f.rule_id == BILL_RULE], ["HB 123"])

    def test_contractions_and_apostrophes_inside_speech_do_not_close_it(self):
        for source in [
            "She said, 'I don't support House Bill 123.'",
            "She said, ‘I don’t support Senate bill 24.’",
            "She said, 'The writers' House Bill 123 passed.'",
            "She said, ‘James’ Senate bill 24 passed.’",
            "She said, 'rock 'n' roll and House Bill 123.'",
        ]:
            with self.subTest(source=source):
                self.assert_closed(source)

    def test_unclosed_or_mismatched_single_quotes_fail_closed(self):
        for source in [
            "She said, 'House Bill 123 and press conference",
            "She said, ‘Senate bill 24 and press conference",
            "She said, 'The writers' House Bill 123",
            "She said, ‘House Bill 123' and press conference",
            "She said, 'Senate bill 24’ and press conference",
            "She said, ’House Bill 123 and press conference",
        ]:
            with self.subTest(source=source):
                self.assert_closed(source)

    def test_unmatched_closing_single_quote_protects_uncertain_prefix(self):
        for closer in ["'", "’"]:
            source = f"House Bill 123{closer} Senate bill 24 advances."
            result = apply_main_style_with_report(source)
            self.assertEqual(result.text, source)
            self.assertEqual([f.suggestion for f in result.findings], ["SB 24"])

    def test_nested_single_and_double_quotations_remain_protected(self):
        for source in [
            '''She said, 'He called "House Bill 123" a press conference.' ''',
            '''She said, "He called 'House Bill 123' a press conference."''',
            "She said, ‘He called 'House Bill 123' a press conference.’",
        ]:
            with self.subTest(source=source):
                self.assert_closed(source)

    def test_delimiters_in_code_and_link_destinations_do_not_hide_narration(self):
        for prefix in ["`'literal`", "```text\n'literal\n```", "[literal](url/'value)",
                       "writer@example.test"]:
            source = f"{prefix}\nHouse bill 123 advances."
            result = apply_main_style_with_report(source)
            self.assertEqual([f.suggestion for f in result.findings], ["HB 123"])

    def test_closed_speech_does_not_hide_later_narration_and_keeps_offsets(self):
        source = "Governor Ron DeSantis said, 'House Bill 123.' Senate bill 24 advances."
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text,
                         "Gov. Ron DeSantis said, 'House Bill 123.' Senate bill 24 advances.")
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertEqual(finding.suggestion, "SB 24")
        self.assertEqual(source[finding.start:finding.end], "Senate bill 24")
        self.assertEqual([c.rule_id for c in result.changes], ["flapol.titles.title-governor"])

    def test_single_quote_protection_applies_to_all_profiles(self):
        source = "'House Bill 123 and press conference.'"
        for function in [apply_main_style_with_report, apply_headline_style_with_report,
                         apply_presentation_style_with_report]:
            with self.subTest(function=function.__name__):
                result = function(source)
                self.assertEqual(result.text, source)
                self.assertEqual(result.changes, ())
                self.assertEqual(result.findings, ())

    def test_nested_protected_spans_stay_sorted_and_nonoverlapping(self):
        source = "'House Bill 123 and `code`.' Then [label](url/'value)."
        spans = find_protected_spans(source)
        self.assertEqual(spans, sorted(spans))
        for left, right in zip(spans, spans[1:]):
            self.assertLess(left.end, right.start)


if __name__ == "__main__":
    unittest.main()
