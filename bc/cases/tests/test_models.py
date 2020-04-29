from unittest import mock

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
