import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from flapol_style.capitalization import (
    find_capitalization_flags,
    load_capitalization_rules,
    normalize_capitalization,
)


class CapitalizationTests(unittest.TestCase):
    def test_every_legacy_capitalization_entry_is_classified(self):
        legacy_entries = {
            "President",
            "Vice President",
            "First Lady",
            "Second Lady",
            "Governor",
            "Attorney General",
            "Representative",
            "Senator",
            "Mayor",
            "CEO",
            "Managing Partner",
            "Director",
            "Chair",
            "County Commission",
            "City Commission",
            "City Council",
            "School Board",
            "School District",
            "Legislative Session",
            "Florida Legislature",
            "Legislature",
            "General Election",
            "Primary Election",
            "Special Election",
            "Midterm Elections",
            "Midterms",
        }
        rules = load_capitalization_rules()
        classified = {
            record["to"] for record in rules["automatic_exact"]
        }
        classified.update(record["to"] for record in rules["before_name_titles"])
        classified.update(record["to"] for record in rules["governmental_bodies"])
        classified.update(record["to"] for record in rules["context_flags"])
        self.assertTrue(legacy_entries <= classified)
        self.assertEqual(rules["unresolved_legacy"], [])

    def test_named_election_stages_are_automatic(self):
        self.assertEqual(
            normalize_capitalization(
                "The primary election precedes the general election and Election Day."
            ),
            "The Primary Election precedes the General Election and Election Day.",
        )

    def test_midterms_is_capitalized(self):
        self.assertEqual(
            normalize_capitalization("The midterms will determine control."),
            "The Midterms will determine control.",
        )

    def test_c_suite_initialisms_are_automatic(self):
        self.assertEqual(
            normalize_capitalization("The ceo met the cfo, coo and cmo."),
            "The CEO met the CFO, COO and CMO.",
        )

    def test_florida_legislature_is_automatic(self):
        self.assertEqual(
            normalize_capitalization("The florida legislature adjourned."),
            "The Florida Legislature adjourned.",
        )

    def test_nonabbreviated_title_before_full_name_is_automatic(self):
        self.assertEqual(
            normalize_capitalization(
                "president Joe Biden met attorney general Ashley Moody and "
                "managing partner Jane Smith."
            ),
            "President Joe Biden met Attorney General Ashley Moody and "
            "Managing Partner Jane Smith.",
        )

    def test_second_lady_is_capitalized_as_a_title(self):
        self.assertEqual(
            normalize_capitalization("second lady Jane Smith spoke."),
            "Second Lady Jane Smith spoke.",
        )
        findings = find_capitalization_flags("The second lady spoke.")
        self.assertEqual(
            [(finding.found, finding.suggestion) for finding in findings],
            [("second lady", "Second Lady")],
        )

    def test_title_before_bold_full_name_is_automatic(self):
        self.assertEqual(
            normalize_capitalization("president **Joe Biden** spoke."),
            "President **Joe Biden** spoke.",
        )

    def test_named_governmental_body_is_automatic(self):
        self.assertEqual(
            normalize_capitalization(
                "The Leon County school board met the Tampa city council."
            ),
            "The Leon County School Board met the Tampa City Council.",
        )

    def test_generic_governmental_body_is_not_rewritten(self):
        source = "Every school board should publish its agenda."
        self.assertEqual(normalize_capitalization(source), source)
        findings = find_capitalization_flags(source)
        self.assertEqual(
            [(finding.found, finding.suggestion) for finding in findings],
            [("school board", "School Board")],
        )

    def test_ambiguous_season_and_organization_forms_are_flags(self):
        source = "They will visit florida in the spring and read politico."
        self.assertEqual(normalize_capitalization(source), source)
        self.assertEqual(
            [(finding.rule_id, finding.suggestion) for finding in find_capitalization_flags(source)],
            [
                ("flapol.capitalization.visit-florida", "VISIT FLORIDA"),
                ("flapol.capitalization.season-spring", "Spring"),
                ("flapol.capitalization.politico", "POLITICO"),
            ],
        )

    def test_automatic_context_is_not_also_flagged(self):
        source = "vice president Kamala Harris addressed the general election."
        self.assertEqual(find_capitalization_flags(source), ())

    def test_quotation_is_neither_changed_nor_flagged(self):
        source = 'The general election matters. “It may fall in the spring.”'
        self.assertEqual(
            normalize_capitalization(source),
            'The General Election matters. “It may fall in the spring.”',
        )
        self.assertEqual(find_capitalization_flags(source), ())

    def test_context_proven_capitalization_is_speech_preserving_in_quote(self):
        self.assertEqual(
            normalize_capitalization('“The general election is next.”'),
            '“The General Election is next.”',
        )

    def test_capitalization_pass_is_idempotent(self):
        source = "attorney general Ashley Moody discussed the general election."
        once = normalize_capitalization(source)
        self.assertEqual(normalize_capitalization(once), once)


if __name__ == "__main__":
    unittest.main()
