import textwrap
from unittest import mock

from django.http.response import HttpResponse
from django.test import TestCase

from bc.cases.backends.respond.client import RespondClientException
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
        self.assertContains(resp, "not available")

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
