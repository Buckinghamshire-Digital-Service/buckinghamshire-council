import json

from django.test import TestCase

from bc.recruitment.text_utils import extract_salary_range

from .fixtures import TalentLinkJobFactory


class SalaryRangeExtractionTest(TestCase):
    def test_salary_ranges(self):
        for raw, expected in [
            ("£20,001 - £30,000", ("20001", "30000")),
            ("£30,001 - £40,000", ("30001", "40000")),
            ("£40,001 - £50,000", ("40001", "50000")),
            ("£50,001 - £60,000", ("50001", "60000")),
            ("£60,000+", ("60000", None)),
            ("Leadership", None),
            ("MPS", None),
            ("MPS/UPS", None),
            ("See advert for details", None),
            ("Up to £20,000", (None, "20000")),
        ]:
            with self.subTest(raw):
                self.assertEqual(extract_salary_range(raw), expected)


class SchemaOrgTest(TestCase):
    def test_salary_range_is_preferred(self):
        job = TalentLinkJobFactory(
            salary_range="£12345 - £23,456", searchable_salary="£56,789 - £67,890"
        )

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "12345")
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "23456")

    def test_searchable_salary_is_used_as_a_fallback(self):
        job = TalentLinkJobFactory(
            salary_range="See ad for details", searchable_salary="£56,789 - £67,890"
        )

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "56789")
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "67890")

    def test_full_salary_range(self):
        job = TalentLinkJobFactory(salary_range="£20,001 - £30,000")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "20001")
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "30000")

    def test_lower_bounded_salary(self):
        job = TalentLinkJobFactory(salary_range="Up to £20,000")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertFalse("minValue" in markup["baseSalary"]["value"])
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "20000")

    def test_upper_bounded_salary(self):
        job = TalentLinkJobFactory(salary_range="£60,000+")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "60000")
        self.assertFalse("maxValue" in markup["baseSalary"]["value"])

    def test_nonnumeric_salary(self):
        job = TalentLinkJobFactory(
            salary_range="Something unparsable", searchable_salary="Something else"
        )

        markup = json.loads(job.schema_org_markup)
        self.assertFalse("baseSalary" in markup)
