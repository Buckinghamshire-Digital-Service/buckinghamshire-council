import textwrap
from unittest import mock

from django.http.response import HttpResponse
from django.test import TestCase

from bc.cases.backends.respond.client import RespondClientException
from bc.cases.forms import ComplaintForm
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
            <case Id="01fc3664f6194732a37f61222cca21bd" Name="DIS 10028 - Last Name,  First Name" Tag="">
              <field name="Feedback Type &amp; Reference Number" schemaName="Case.FeedbackTypeReferenceNumber" type="ShortText">
                <value>DIS 10028</value>
              </field>
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
        expected_case_reference = "DIS 10028"
        self.assertEqual(resp.context["case_reference"], expected_case_reference)

    @mock.patch("bc.cases.models.get_client")
    @mock.patch("bc.cases.models.ApteanRespondCaseFormPage.get_form")
    def test_extracting_case_name_with_no_feedback_type_element(
        self, mock_get_form, mock_get_client
    ):
        homepage = HomePage.objects.first()
        self.case_form_page = ApteanRespondCaseFormPageFactory.build()
        homepage.add_child(instance=self.case_form_page)
        # This is not a realistic response, but we're only parsing the case element.
        response_xml = textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8"?> <caseResponse version="2" xmlns:="http://www.aptean.com/respond/caseresponse/2">
            <case Id="01fc3664f6194732a37f61222cca21bd" Name="DIS 10028 - Last Name,  First Name" Tag="">
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
        expected_case_reference = "DIS 10028"
        self.assertEqual(resp.context["case_reference"], expected_case_reference)

    @mock.patch("bc.cases.models.get_client")
    def test_initial_page_has_cache_prevention_headers(self, mock_get_client):
        resp = self.client.get(self.case_form_page.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp._headers["cache-control"],
            ("Cache-Control", "max-age=0, no-cache, no-store, must-revalidate"),
        )

    @mock.patch("bc.cases.models.get_client")
    @mock.patch("bc.cases.models.ApteanRespondCaseFormPage.get_form")
    def test_error_page_has_cache_prevention_headers(
        self, mock_get_form, mock_get_client
    ):
        mock_get_form.return_value = ComplaintForm()
        resp = self.client.post(self.case_form_page.url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["form"].is_valid())
        self.assertEqual(
            resp._headers["cache-control"],
            ("Cache-Control", "max-age=0, no-cache, no-store, must-revalidate"),
        )

    @mock.patch("bc.cases.models.get_client")
    @mock.patch("bc.cases.models.ApteanRespondCaseFormPage.get_form")
    def test_success_page_has_cache_prevention_headers(
        self, mock_get_form, mock_get_client
    ):
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
        resp = self.client.post(self.case_form_page.url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("form", resp.context)
        self.assertEqual(
            resp._headers["cache-control"],
            ("Cache-Control", "max-age=0, no-cache, no-store, must-revalidate"),
        )


class CaseNameFormattingTest(TestCase):
    def test_old_compliant_values(self):
        """The format used to be ABC - 12345 Surname, Firstname"""
        for reference, expected in [
            ("ABC - 12345", "ABC 12345"),  # trivial example
            ("DIS - 10028 Response Xml Test,", "DIS 10028"),
            ("DIS - 10028 Response Xml Test,", "DIS 10028"),
            ("COR - 09849 Mänikkölahti", "COR 09849"),
            ("ABC - 1 Dentistry, Squalid", "ABC 1"),
            ("ABC - 123456 Pliant, Coconuted", "ABC 123456"),
            ("ABC - 1234567890", "ABC 1234567890"),
            ("ABC 12345 - 789", "ABC 12345"),
            ("ABC 12345 - 789, 012", "ABC 12345"),
        ]:
            with self.subTest(reference):
                self.assertEqual(format_case_reference(reference), expected)

    def test_new_compliant_values(self):
        """The format changed to ABC 12345 - Surname, Firstname"""
        for reference, expected in [
            ("ABC 12345", "ABC 12345"),  # trivial example
            ("DIS 10028 - Response Xml Test,", "DIS 10028"),
            ("COR 09849 - Mänikkölahti", "COR 09849"),
            ("ABC 1 - Dentistry, Squalid", "ABC 1"),
            ("ABC 123456 - Pliant, Coconuted", "ABC 123456"),
            ("ABC 1234567890 - A, Z", "ABC 1234567890"),
            ("ABC 12345 - 789", "ABC 12345"),
            ("ABC 12345 - 789, 012", "ABC 12345"),
        ]:
            with self.subTest(reference):
                self.assertEqual(format_case_reference(reference), expected)

    def test_extraterrestrial_values_are_not_reformatted(self):
        for reference in [
            "D2S - 10028 Response Xml Test,",
            "D2S 10028 - Response Xml Test,",
            "This is a random sentence",
            "123 - ABCDE Jellyfish",
            "123 ABCDE - Jellyfish",
            "COM - 1A Marmot",
            "COM 1A - Marmot",
            "COM - A1 Grouse",
            "COM A1 - Grouse",
            "ABCD - 12345 Muskrat",
            "ABCD 12345 - Muskrat",
            "AB - 12345 Wallaby",
            "AB 12345 - Wallaby",
        ]:
            with self.subTest(reference):
                self.assertEqual(format_case_reference(reference), reference)
