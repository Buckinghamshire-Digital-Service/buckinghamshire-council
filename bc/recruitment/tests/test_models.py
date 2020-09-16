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
    def test_full_salary_range(self):
        job = TalentLinkJobFactory(searchable_salary="£20,001 - £30,000")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "20001")
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "30000")

    def test_lower_bounded_salary(self):
        job = TalentLinkJobFactory(searchable_salary="Up to £20,000")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertFalse("minValue" in markup["baseSalary"]["value"])
        self.assertEqual(markup["baseSalary"]["value"]["maxValue"], "20000")

    def test_upper_bounded_salary(self):
        job = TalentLinkJobFactory(searchable_salary="£60,000+")

        markup = json.loads(job.schema_org_markup)
        self.assertTrue("baseSalary" in markup)
        self.assertEqual(markup["baseSalary"]["value"]["minValue"], "60000")
        self.assertFalse("maxValue" in markup["baseSalary"]["value"])

    def test_nonnumeric_salary(self):
        job = TalentLinkJobFactory(searchable_salary="Something else")

        markup = json.loads(job.schema_org_markup)
        self.assertFalse("baseSalary" in markup)
