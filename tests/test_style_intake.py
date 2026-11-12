"""Owner-approved intake rules: meaningful positives and adversarial boundaries."""

from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from flapol_style import apply_main_style_with_report, apply_main_style


class IntakeTests(unittest.TestCase):
    def assert_rendering(self, source, expected):
        result = apply_main_style_with_report(source)
        self.assertEqual(result.text, expected)
        for change in result.changes:
            self.assertEqual(source[change.source_start:change.source_end], change.before)
            self.assertEqual(change.action, "AUTO_FIX")
        repeated = apply_main_style_with_report(result.text)
        self.assertEqual(repeated.text, result.text)
        self.assertEqual(repeated.changes, ())
        return result

    def test_president_and_compound_titles(self):
        cases = [
            ("The president and two presidents spoke.", "The President and two Presidents spoke."),
            ("Jane Smith is market president and CEO.", "Jane Smith is market President and CEO."),
            ("The vice president met the president-elect.", "The Vice President met the President-elect."),
            ("A vice president-elect met the president-designate.", "A Vice President-elect met the President-designate."),
            ("The presidential race is unprecedented.", "The presidential race is unprecedented."),
            ("The president's staff called.", "The President's staff called."),
            ("The president’s staff called.", "The President’s staff called."),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assert_rendering(source, expected)

    def test_local_titles_plural_possessive_and_elect(self):
        cases = [
            ("The city manager and city attorney spoke.", "The City Manager and City Attorney spoke."),
            ("Two city managers met three city attorneys.", "Two City Managers met three City Attorneys."),
            ("A council member met board members.", "A Council Member met Board Members."),
            ("The city attorney’s advice guided council members.", "The City Attorney’s advice guided Council Members."),
            ("The board member-elect met the council member-elect.", "The Board Member-elect met the Council Member-elect."),
            ("City management and board membership matter.", "City management and board membership matter."),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assert_rendering(source, expected)

    def test_police_agencies_and_ambiguous_councils(self):
        r = self.assert_rendering(
            "The Naples police department announced an arrest. The police department said more.",
            "The Naples Police Department announced an arrest. The Police Department said more.",
        )
        self.assertEqual(r.findings, ())
        for source in [
            "Every police department should report. The council met.",
            "The police department said nothing.",
            "The Naples Police Department met the Tampa Police Department. The police department said nothing.",
            "The police department said nothing before the Naples Police Department arrived.",
            "The Naples Police Department met every police department in Florida.",
            '“The Naples police department spoke.” The police department said nothing.',
        ]:
            with self.subTest(source=source):
                self.assert_rendering(source, source)
                self.assertTrue(apply_main_style_with_report(source).findings)

    def test_contextual_local_offices_and_fiscal_years(self):
        self.assert_rendering("commissioner Jane Smith met deputy John Jones.",
                              "Commissioner Jane Smith met Deputy John Jones.")
        source = "The commissioners and deputies met in the fiscal year."
        r = self.assert_rendering(source, source)
        self.assertEqual([f.found for f in r.findings], ["commissioners", "deputies", "fiscal year"])
        source = '“commissioner Jane Smith met deputy John Jones.”'
        self.assert_rendering(source, source)

    def test_numbered_street_addresses_only(self):
        cases = [
            ("At 609 Brickell Avenue, they met.", "At 609 Brickell Ave., they met."),
            ("At 123 Main Street and 456 Oak Boulevard.", "At 123 Main St. and 456 Oak Blvd."),
            ("At 123A North Main Street, Suite 4.", "At 123A North Main St., Suite 4."),
            ("At 100 21st Street; at 7 Fifth Avenue.", "At 100 21st St.; at 7 Fifth Ave."),
            ("On Main Avenue and Oak Boulevard.", "On Main Avenue and Oak Boulevard."),
            ("At 9 University Road and 12 Oak Drive.", "At 9 University Road and 12 Oak Drive."),
            ("At 123 Avenue of the Americas.", "At 123 Avenue of the Americas."),
            ("A $123 Main Street grant.", "A $123 Main Street grant."),
            ("The 123-125 Main Street range.", "The 123-125 Main Street range."),
            ("At 123 Main\nStreet.", "At 123 Main\nStreet."),
            ("Over 100 Main Street businesses closed.", "Over 100 Main Street businesses closed."),
            ("The 2026 Main Street Survey opened.", "The 2026 Main Street Survey opened."),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assert_rendering(source, expected)

    def test_military_compound_ranks_and_names(self):
        cases = [
            ("Lieutenant Colonel Jane Smith", "Lt. Col. Jane Smith"),
            ("Army attorney Lieutenant Colonel Jane Smith", "Army attorney Lt. Col. Jane Smith"),
            ("Major General Jane Smith", "Maj. Gen. Jane Smith"),
            ("Lieutenant General Jane Smith", "Lt. Gen. Jane Smith"),
            ("Chief Master Sergeant Jane Smith", "Chief Master Sgt. Jane Smith"),
            ("Command Sergeant Major Jane Smith", "Command Sgt. Maj. Jane Smith"),
            ("Sergeant First Class Jane Smith", "Sgt. 1st Class Jane Smith"),
            ("Master Gunnery Sergeant Jane Smith", "Master Gunnery Sgt. Jane Smith"),
            ("Lance Corporal Jane Smith", "Lance Cpl. Jane Smith"),
            ("Lieutenant Commander Jane Smith", "Lt. Cmdr. Jane Smith"),
            ("Vice Admiral Jane Smith", "Vice Adm. Jane Smith"),
            ("Petty Officer Second Class Jane Smith", "Petty Officer 2nd Class Jane Smith"),
            ("Lieutenant Junior Grade Jane Smith", "Lt. j.g. Jane Smith"),
            ("retired Army Lieutenant Colonel **Jane Smith**", "retired Army Lt. Col. **Jane Smith**"),
            ("Colonel José Nuñez", "Col. José Nuñez"),
            ("Captain Jane O’Neill", "Capt. Jane O’Neill"),
            ("General Jane Hall", "Gen. Jane Hall"),
            ("Sergeant Anne-Marie Smith", "Sgt. Anne-Marie Smith"),
            ("Airman First Class Jane Smith", "Airman 1st Class Jane Smith"),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assert_rendering(source, expected)

    def test_rank_words_are_not_always_military_titles(self):
        cases = [
            "General Motors Chief Jane Smith spoke.", "General Electric Company filed.",
            "Major League Baseball returned.", "Attorney General Jane Smith spoke.",
            "Secretary-General Jane Smith spoke.", "Inspector General Jane Smith spoke.",
            "Surgeon General Jane Smith spoke.", "The general and the major spoke.",
            "Jane Smith, a Lieutenant Colonel, spoke.", "Colonel Smith spoke.",
            "The Lieutenant Colonel spoke.", "Lieutenant Colonel jane smith spoke.",
            "Airman Basic Jane Smith spoke.", "Chief Petty Officer Jane Smith spoke.",
            "General Magistrate Jane Smith spoke.",
            "The Major John Leroy Haynes Florida Veterans’ History Program opened.",
            "The General John Smith Memorial Bridge opened.",
            "Private Equity Partners filed.", "General Atlantic Capital filed.",
            "Captain Morgan Rum sold.",
        ]
        for source in cases:
            with self.subTest(source=source):
                self.assert_rendering(source, source)

    def test_ambassador_mapping_requires_supplied_us_qualifier(self):
        self.assert_rendering("U.S. Ambassador Jane Smith spoke.", "U.S. Amb. Jane Smith spoke.")
        for source in ["French Ambassador Jane Smith spoke.", "Ambassador Jane Smith spoke.",
                       "U.S. Ambassador Smith spoke.", "The U.S. Ambassador spoke."]:
            with self.subTest(source=source):
                self.assert_rendering(source, source)

    def test_no_party_narration_and_reference_order(self):
        r = self.assert_rendering(
            "Third-party and no-party-affiliation voters voted. NPA voters agreed.",
            "Third- and no-party voters voted. NPA voters agreed.",
        )
        self.assertEqual(r.findings, ())
        self.assert_rendering("A no-party-affiliation member spoke.", "A no-party member spoke.")
        for phrase in ["no-party-affiliation", "no party affiliation", "no-party affiliation", "no party-affiliation"]:
            self.assert_rendering(f"Third-party and {phrase} voters voted.",
                                  "Third- and no-party voters voted.")
        for source in ["NPA voters spoke.", "One NPA member spoke.",
                       "NPA voters spoke before no-party voters."]:
            r = self.assert_rendering(source, source)
            self.assertEqual([f.rule_id for f in r.findings], ["flapol.usage.npa-first-reference"])
        self.assert_rendering("No-Party-Affiliation Voter Form", "No-Party-Affiliation Voter Form")
        self.assertEqual(self.assert_rendering("NPA means a nonperforming asset.",
                                              "NPA means a nonperforming asset.").findings, ())

    def test_corporate_identity_is_never_deleted(self):
        source = "Acme Holdings LLC met Acme Holdings Inc. and Acme Holdings L.L.C."
        r = self.assert_rendering(source, source)
        self.assertEqual([f.found for f in r.findings], ["LLC", "Inc.", "L.L.C."])
        for source in ["I read Inc. magazine.", "An LLC is a legal structure."]:
            self.assertEqual(self.assert_rendering(source, source).findings, ())
        source = "eBay Inc. filed."
        self.assertEqual([f.found for f in self.assert_rendering(source, source).findings], ["Inc."])

    def test_hard_protection_and_unbalanced_structure(self):
        source = "president@example.test https://example.test/president `city manager`"
        r = self.assert_rendering(source, source)
        self.assertEqual(r.findings, ())
        source = 'A city manager said, "the president met NPA voters and Acme LLC'
        self.assert_rendering(source, source.replace("city manager", "City Manager"))

    def test_new_rules_do_not_leak_into_headline_profile(self):
        from flapol_style import apply_headline_style
        source = "A city manager meets NPA voters at 123 Main Avenue"
        result = apply_headline_style(source)
        self.assertNotIn("City Manager", result)
        self.assertNotIn("Main Ave.", result)

    def test_legal_intervenor_is_a_finding(self):
        source = "The court granted intervener status."
        r = self.assert_rendering(source, source)
        self.assertEqual([(f.found, f.suggestion) for f in r.findings], [("intervener", "intervenor")])
        source = "A helpful intervener calmed the argument."
        self.assertEqual(self.assert_rendering(source, source).findings, ())

    def test_city_of_and_vote_outcomes_are_review_only(self):
        source = "They asked the City of Naples. The board voted 1-4 against it."
        r = self.assert_rendering(source, source)
        self.assertEqual([f.rule_id for f in r.findings], [
            "flapol.usage.city-of-capitalization", "flapol.usage.vote-tally-order"])
        for source in ["City of Naples officials spoke.", "The board voted 4-1 against it.",
                       "The vote failed 1-4.", '“The board voted 1-4 against it.”']:
            self.assertEqual(self.assert_rendering(source, source).findings, ())

    def test_new_word_forms_and_title_case_protection(self):
        self.assert_rendering("They re-scoped the pre-construction plan and are re-scoping it.",
                              "They rescoped the preconstruction plan and are rescoping it.")
        self.assert_rendering("The Pre-Construction Company filed.", "The Pre-Construction Company filed.")

    def test_new_rules_do_not_enter_quotations_or_literals(self):
        for phrase in ["the president", "a city manager", "a board member", "council",
                       "Lieutenant Colonel Jane Smith", "U.S. Ambassador Jane Smith",
                       "609 Brickell Avenue", "no-party-affiliation voters", "NPA voters",
                       "Acme LLC", "re-scoped", "pre-construction", "Naples police department"]:
            for source in [f'"{phrase}"', f'“{phrase}”', f'"{phrase}', f'“{phrase}',
                           f'`{phrase}`', f'```text\n{phrase}\n```', f'```text\n{phrase}',
                           f'[literal](https://example.test/{phrase.replace(" ", "%20")})']:
                with self.subTest(source=source):
                    r = self.assert_rendering(source, source)
                    self.assertEqual(r.findings, ())

    def test_source_offsets_after_earlier_shortening(self):
        source = "Lieutenant Colonel Jane Smith met a no-party-affiliation member at 609 Brickell Avenue. Acme LLC paid."
        r = self.assert_rendering(source,
            "Lt. Col. Jane Smith met a no-party member at 609 Brickell Ave. Acme LLC paid.")
        self.assertEqual([f.found for f in r.findings], ["LLC"])
        for finding in r.findings:
            self.assertEqual(source[finding.start:finding.end], finding.found)


if __name__ == "__main__":
    unittest.main()
