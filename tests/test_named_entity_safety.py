"""A person's name inside an institution does not make its rank a title use."""

from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from flapol_style import (
    apply_main_style_with_report, abbreviate_titles_before_names,
    resolve_legislator_context, LegislatorIdentity,
)


class NamedEntitySafetyTests(unittest.TestCase):
    def check(self, source, expected=None, **kwargs):
        expected = source if expected is None else expected
        result = apply_main_style_with_report(source, **kwargs)
        self.assertEqual(result.text, expected)
        for change in result.changes:
            self.assertEqual(source[change.source_start:change.source_end], change.before)
        for finding in result.findings:
            self.assertEqual(source[finding.start:finding.end], finding.found)
        repeated = apply_main_style_with_report(result.text, **kwargs)
        self.assertEqual(repeated.text, result.text)
        self.assertEqual(repeated.changes, ())
        return result

    def test_fox_program_name_and_typographic_variants(self):
        for qualifier in ["", "U.S. Department of Veterans Affairs’ ", "Army "]:
            for suffix in ["Suicide Prevention Grant Program", "suicide prevention grant program",
                           "Suicide Prevention Grant\nProgram", "suicide-prevention grant program"]:
                source = qualifier + "Staff Sergeant Parker Gordon Fox " + suffix + "."
                with self.subTest(source=source):
                    self.assertEqual(self.check(source).findings, ())
                    self.assertEqual(abbreviate_titles_before_names(source), source)
        self.check("Army Staff Sergeant Alex Example " + "Veterans " * 25 + "Grant Program.")

    def test_published_civilian_occupations_and_institutions(self):
        for source in [
            "A healthcare finance specialist Tosha Chambers spoke.",
            "A healthcare financial specialist Tosha Chambers spoke.",
            "Admiral Farragut Academy opened.",
            "The General Obligation Bonds Oversight Committee met.",
            "The state requested a Major Disaster Declaration.",
        ]:
            with self.subTest(source=source):
                self.assertEqual(self.check(source).findings, ())

    def test_generalized_entity_categories_not_a_name_allowlist(self):
        for title in ["General", "Major", "Captain", "Staff Sergeant", "Lieutenant Colonel"]:
            for head in ["Institute", "Academy", "Award", "Awards", "Medal", "Program",
                         "Foundation", "Fund", "Commission", "Museum", "Association"]:
                source = f"Army {title} **Alex Q. Example** memorial {head} opened."
                with self.subTest(title=title, head=head):
                    self.assertEqual(self.check(source).findings, ())

    def test_titles_inside_other_named_programs_are_preserved(self):
        for source in [
            "The Governor John Smith Institute opened.",
            "The U.S. Ambassador Jane Smith scholarship program opened.",
            "The Chief Executive Officer Leadership Institute opened.",
            "The retired General Jane Smith, Jr., Memorial Award was presented.",
            "The General Revenue Fund and Private Activity Bonds were discussed.",
            'Army Colonel John Paul “Jim” Smith memorial program opened.',
            'The U.S. Representative John Paul "Jim" Smith Institute opened.',
        ]:
            with self.subTest(source=source):
                self.check(source)

    def test_positive_local_service_context_still_abbreviates(self):
        for source, expected in [
            ("Army Staff Sergeant Parker Gordon Fox spoke.", "Army Staff Sgt. Parker Gordon Fox spoke."),
            ("Navy Admiral Jane Smith spoke.", "Navy Adm. Jane Smith spoke."),
            ("FHP Colonel Gary Howze spoke.", "FHP Col. Gary Howze spoke."),
            ("police Sergeant Jane Smith spoke.", "police Sgt. Jane Smith spoke."),
            ("retired Army General Jane Hall spoke.", "retired Army Gen. Jane Hall spoke."),
            ("Army\nColonel Jane Smith spoke.", "Army\nCol. Jane Smith spoke."),
            ("Army Colonel Jane Smith spoke about the Fox grant program.",
             "Army Col. Jane Smith spoke about the Fox grant program."),
            ("Army Colonel Jane Smith of the State University spoke.",
             "Army Col. Jane Smith of the State University spoke."),
        ]:
            with self.subTest(source=source):
                self.check(source, expected)

    def test_context_is_not_inherited_from_another_sentence_or_entity(self):
        for source in [
            "The Army funded the school. Admiral Farragut Academy opened.",
            "The Army hired a finance specialist Tosha Chambers.",
            "Army\n\nColonel Jane Smith spoke.",
            "Army Major Jane Smith spoke. The specialist Alex Example attended.",
        ]:
            with self.subTest(source=source):
                expected = source.replace("Army Major Jane Smith", "Army Maj. Jane Smith")
                self.check(source, expected)

    def test_unqualified_ranks_are_findings_instead_of_guesses(self):
        for title in ["General", "Major", "Private", "Specialist", "Commander", "Lieutenant Colonel"]:
            source = f"{title} Alex Example spoke."
            result = self.check(source)
            self.assertEqual([f.rule_id for f in result.findings],
                             ["flapol.titles.military-context-required"])
            self.assertEqual([f.found for f in result.findings], [title])
        self.assertEqual([f.found for f in self.check("A retired specialist Alex Example spoke.").findings],
                         ["specialist"])
        self.assertEqual([f.found for f in self.check(
            "General Alex Example Research Collaborative opened.").findings], ["General"])

    def test_quotations_and_literals_stay_protected(self):
        phrase = "Army Staff Sergeant Parker Gordon Fox spoke."
        for source in [f'"{phrase}"', f'“{phrase}”', f'"{phrase}', f'“{phrase}',
                       f'`{phrase}`', f'```text\n{phrase}\n```', f'```text\n{phrase}',
                       '[literal](https://example.test/Army%20Colonel%20Jane%20Smith)']:
            with self.subTest(source=source):
                self.assertEqual(self.check(source).findings, ())

    def test_lawmaker_identity_does_not_authorize_renaming_an_institution(self):
        options = {"officeholder_as_of": date(2026, 11, 12)}
        for source in [
            "The Senator Rick Scott Institute opened.",
            "The U.S. Representative Kathy Castor Scholarship Fund opened.",
            "The Senators Rick Scott and Ashley Moody Scholarship Fund opened.",
            '“The Senator Rick Scott Institute opened.”',
        ]:
            with self.subTest(source=source):
                self.assertEqual(self.check(source, **options).findings, ())
                context = resolve_legislator_context(source, as_of=options["officeholder_as_of"])
                self.assertEqual(context.mode, "unresolved")
                self.assertEqual(context.identities, ())

    def test_institution_names_do_not_change_other_lawmakers_jurisdiction(self):
        options = {"officeholder_as_of": date(2026, 11, 12),
                   "legislator_overlays": (LegislatorIdentity("Alex Example", "state", "house"),)}
        for institution in ["Senator Rick Scott Institute",
                            "Senators Rick Scott and Ashley Moody scholarship fund"]:
            source = f"The {institution} opened. Representative Alex Example spoke."
            self.check(source, source.replace("Representative Alex Example", "Rep. Alex Example"), **options)

    def test_existing_representative_occupation_guard_remains(self):
        self.check("An applicant representative Alex Example spoke.",
                   officeholder_as_of=date(2026, 11, 12))
        options = {"officeholder_as_of": date(2026, 11, 12),
                   "legislator_overlays": (LegislatorIdentity("Alex Example", "state", "house"),)}
        for role in ["company", "union", "legal", "campaign", "applicant"]:
            source = f"The {role} representative Alex Example spoke."
            self.assertEqual(self.check(source, **options).findings, ())
            source = f"The {role} U.S. Representative **Alex Example** spoke."
            self.assertEqual(self.check(source, **options).findings, ())
        source = ("The company representatives Rick Scott and Ashley Moody spoke. "
                  "Representative Alex Example spoke.")
        self.assertEqual(self.check(source, source.replace("Representative Alex Example", "Rep. Alex Example"),
                                    **options).findings, ())
        for alias in ['Alexander "Alex" Example', 'Alexander “Alex” Example']:
            options = {"officeholder_as_of": date(2026, 11, 12),
                       "legislator_overlays": (LegislatorIdentity("Alex Example", "state", "house", (alias,)),)}
            self.check(f"The Representative {alias} Civic Leadership Award opened.", **options)

    def test_source_coordinates_after_an_earlier_shortening(self):
        source = "Governor Ron DeSantis met Colonel Alex Example."
        result = self.check(source, "Gov. Ron DeSantis met Colonel Alex Example.")
        self.assertEqual([f.found for f in result.findings], ["Colonel"])


if __name__ == "__main__":
    unittest.main()
