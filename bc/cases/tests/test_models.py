import textwrap
from unittest import mock

from django.http.response import HttpResponse
from django.test import TestCase

from bc.cases.backends.respond.client import RespondClientException
from bc.cases.utils import format_case_reference
from bc.home.models import HomePage

from .fixtures import ApteanRespondCaseFormPageFactory


class CaseFormPageTest(TestCase):
    def setUp(self):
        homepage = HomePage.objects.first()
        self.case_form_page = ApteanRespondCaseFormPageFactory.build()
        homepage.add_child(instance=self.case_form_page)

    @mock.patch("bc.cases.models.get_client")
    def test_page_loads_when_client_not_configured(self, mock_get_client):
        mock_get_client.side_effect = RespondClientException
        resp = self.client.get(self.case_form_page.url)
        self.assertEqual(resp.status_code, 200)

    @mock.patch("bc.cases.models.get_client")
    @mock.patch("bc.cases.models.ApteanRespondCaseFormPage.get_form")
    def test_extracting_case_name_from_case_response(
        self, mock_get_form, mock_get_client
    ):
        homepage = HomePage.objects.first()
        self.case_form_page = ApteanRespondCaseFormPageFactory.build()
        homepage.add_child(instance=self.case_form_page)
        # This is not a realistic response, but case.attrs is all that we parse.
        response_xml = textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8"?> <caseResponse version="2" xmlns:="http://www.aptean.com/respond/caseresponse/2">
            <case Id="01fc3664f6194732a37f61222cca21bd" Name="DIS - 10028 Response Xml Test," Tag="">
            </case>
            </caseResponse>
        """  # noqa
        )
        mock_get_client.return_value = mock.Mock(
            **{"create_case.return_value": HttpResponse(response_xml)}
        )
        with self.assertTemplateUsed("patterns/pages/cases/form_page_landing.html"):
            resp = self.client.post(self.case_form_page.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "10028")
        self.assertNotContains(resp, "Response Xml Test")
        expected_case_reference = "DIS - 10028"
        self.assertEqual(resp.context["case_reference"], expected_case_reference)


class CaseNameFormattingTest(TestCase):
    def test_compliant_values(self):
        for reference, expected in [
            ("ABC - 12345", "ABC - 12345"),  # trivial example
            ("DIS - 10028 Response Xml Test,", "DIS - 10028"),
            ("COR - 09849 Mänikkölahti", "COR - 09849"),
            ("ABC - 123456", "ABC - 123456"),
            ("ABC - 1234567890", "ABC - 1234567890"),
            ("ABC - 1", "ABC - 1"),
        ]:
            with self.subTest(reference):
                self.assertEqual(format_case_reference(reference), expected)

    def test_extraterrestrial_values_are_not_reformatted(self):
        for reference in [
            "D2S - 10028 Response Xml Test,",
            "This is a random sentence",
            "123 - ABCDE Jones",
            "COM - 1A Jones",
            "COM - A1 Jones",
            "ABCD - 12345",
            "AB - 12345",
        ]:
            with self.subTest(reference):
                self.assertEqual(format_case_reference(reference), reference)
