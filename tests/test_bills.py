"""Numbered bill labels: review suggestions without entering quoted speech."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from flapol_style import apply_main_style_with_report, apply_headline_style_with_report
from flapol_style.usage import _NUMBERED_BILL_RULE


class NumberedBillTests(unittest.TestCase):
    def bill_findings(self, text):
        result = apply_main_style_with_report(text)
        return result, tuple(f for f in result.findings
                             if f.rule_id == _NUMBERED_BILL_RULE.rule_id)

    def test_both_chambers_bill_cases_and_one_to_four_digits(self):
        for chamber, abbreviation in [("House", "HB"), ("Senate", "SB")]:
            for label in ["Bill", "bill"]:
                for number in ["1", "24", "123", "1234"]:
                    source = f"{chamber} {label} {number} advances."
                    with self.subTest(source=source):
                        result, findings = self.bill_findings(source)
                        self.assertEqual(result.text, source)
                        self.assertEqual(result.changes, ())
                        self.assertEqual(len(findings), 1)
                        finding = findings[0]
                        self.assertEqual(finding.action, "FLAG")
                        self.assertEqual(finding.severity, "error")
                        self.assertEqual(finding.suggestion, f"{abbreviation} {number}")
                        self.assertEqual(source[finding.start:finding.end], finding.found)
                        self.assertIn("2026-11-19", finding.authority)

    def test_generic_existing_and_unsupported_number_forms_are_preserved(self):
        for source in [
            "A House bill is heading to its final committee stop.",
            "The Senate bill advances.", "House Bill of Rights", "HB 123 and SB 24",
            "House Bill 12345", "Senate bill 123456", "House Bill 123A",
            "House Bill 123rd", "House Bill 1,234", "House Bill 12.3",
            "House Bill 12/3", "House Bill 12-3", "House Bills 123 and 124",
            "House Bill -123", "House Bill １２３", "House Bill\n123",
        ]:
            with self.subTest(source=source):
                result, findings = self.bill_findings(source)
                self.assertEqual(result.text, source)
                self.assertEqual(findings, ())

    def test_quotation_literal_and_malformed_protection(self):
        self.assertFalse(_NUMBERED_BILL_RULE.speech_preserving)
        for phrase in ["House Bill 123", "Senate bill 24"]:
            for source in [
                f'"{phrase}"', f'“{phrase}”', f'"{phrase}', f'“{phrase}',
                f'{phrase}”', f'`{phrase}`', f'```text\n{phrase}\n```',
                f'```text\n{phrase}', f'[literal]({phrase})',
                f'https://example.test/{phrase.replace(" ", "%20")}',
                'HouseBill123@example.test',
            ]:
                with self.subTest(source=source):
                    result, findings = self.bill_findings(source)
                    self.assertEqual(result.text, source)
                    self.assertEqual(result.changes, ())
                    self.assertEqual(findings, ())

    def test_visible_link_labels_are_reviewable_but_destinations_are_not(self):
        source = "[House bill 123](https://example.test/Senate%20Bill%2024)"
        result, findings = self.bill_findings(source)
        self.assertEqual(result.text, source)
        self.assertEqual([f.suggestion for f in findings], ["HB 123"])

    def test_source_offsets_after_prior_edits_and_repeat_stability(self):
        source = 'Governor Ron DeSantis discussed House bill 123, then “Senate bill 24.”'
        first, findings = self.bill_findings(source)
        self.assertEqual(first.text,
                         'Gov. Ron DeSantis discussed House bill 123, then “Senate bill 24.”')
        self.assertEqual(len(findings), 1)
        self.assertEqual(source[findings[0].start:findings[0].end], "House bill 123")
        second, repeated = self.bill_findings(first.text)
        self.assertEqual(second.text, first.text)
        self.assertEqual(second.changes, ())
        self.assertEqual([(f.found, f.suggestion) for f in repeated],
                         [("House bill 123", "HB 123")])
        self.assertEqual(first.text[repeated[0].start:repeated[0].end], "House bill 123")

    def test_rule_is_body_only_and_punctuation_ends_the_number(self):
        source = "House Bill 123; Senate bill 24. House bill 7/Senate bill 8"
        _, findings = self.bill_findings(source)
        self.assertEqual([f.suggestion for f in findings], ["HB 123", "SB 24", "HB 7", "SB 8"])
        headline = apply_headline_style_with_report("House Bill 123 advances")
        self.assertFalse(any(f.rule_id == _NUMBERED_BILL_RULE.rule_id
                             for f in headline.findings))


if __name__ == "__main__":
    unittest.main()
