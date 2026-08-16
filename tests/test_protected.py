import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.protected import find_protected_spans, transform_unprotected


class ProtectedRegionTests(unittest.TestCase):
    def test_curly_and_straight_quotations_are_unchanged(self):
        text = 'January 8. “January 9th.” Then "January 10th."'
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(
            result, 'Jan. 8. “January 9th.” Then "January 10th."'
        )

    def test_unbalanced_quotation_fails_closed(self):
        text = 'January 8. He said, "January 9th and continued'
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(
            result, 'Jan. 8. He said, "January 9th and continued'
        )

    def test_markdown_link_destination_is_protected_but_label_is_eligible(self):
        text = "[January 8](https://example.com/January-8)"
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(result, "[Jan. 8](https://example.com/January-8)")

    def test_inline_and_fenced_code_are_protected(self):
        text = "January 8 and `January 9`\n\n```text\nJanuary 10\n```"
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(
            result, "Jan. 8 and `January 9`\n\n```text\nJanuary 10\n```"
        )

    def test_unclosed_fence_protects_remainder(self):
        text = "January 8\n```text\nJanuary 9"
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(result, "Jan. 8\n```text\nJanuary 9")

    def test_urls_and_email_addresses_are_protected(self):
        text = "January 8 https://example.com/January-9 January10@example.com"
        result = transform_unprotected(
            text, lambda value: value.replace("January", "Jan.")
        )
        self.assertEqual(
            result,
            "Jan. 8 https://example.com/January-9 January10@example.com",
        )

    def test_spans_are_sorted_and_nonoverlapping(self):
        spans = find_protected_spans('[label](https://example.com/a) and "quote"')
        self.assertEqual(spans, sorted(spans))
        for previous, current in zip(spans, spans[1:]):
            self.assertLess(previous.end, current.start)


if __name__ == "__main__":
    unittest.main()
