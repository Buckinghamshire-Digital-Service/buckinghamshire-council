import pathlib
import textwrap

from django.conf import settings
from django.test import TestCase, override_settings

import requests
import responses

from bc.cases.backends.respond.client import RespondClientException, get_client


@override_settings(
    RESPOND_API_USERNAME="foo",
    RESPOND_API_PASSWORD="bar",
    RESPOND_API_BASE_URL="https://www.example.invalid/",
)
class TestClient(TestCase):
    def setUp(self):
        self.xml = textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8"?>
            <case Tag="" xmlns:="http://www.aptean.com/respond/caserequest/1">
             <field schemaName="Case.FeedbackType">
              <value>
               SAR
              </value>
             </field>
             <field schemaName="Case.HowReceived">
              <value>
               Web Form
              </value>
             </field>
             <field schemaName="Case.Description">
              <value>
               Some description
              </value>
             </field>
             <Contacts>
              <contact Tag="">
               <field schemaName="Contact.ContactIs">
                <value>
                 Other
                </value>
               </field>
              </contact>
             </Contacts>
            </case>
        """
        )
        self.client = self._get_client()

    @responses.activate
    def _get_client(self):
        with open(pathlib.Path(__file__).parent / "fixtures/getservices.xml") as f:
            services_xml = f.read()
        responses.add(
            responses.GET,
            settings.RESPOND_API_BASE_URL + "metadata.svc/getservices",
            services_xml,
            status=200,
            content_type="text/xml",
        )
        with open(pathlib.Path(__file__).parent / "fixtures/getfields.xml") as f:
            fields_xml = f.read()
        responses.add(
            responses.GET,
            settings.RESPOND_API_BASE_URL
            + "metadata.svc/Fields/TestGetFieldsComplaints",
            fields_xml,
            status=200,
            content_type="text/xml",
        )
        with open(pathlib.Path(__file__).parent / "fixtures/getcategories.xml") as f:
            categories_xml = f.read()
        responses.add(
            responses.GET,
            settings.RESPOND_API_BASE_URL
            + "metadata.svc/Categories/TestGetCategoryComplaints",
            categories_xml,
            status=200,
            content_type="text/xml",
        )
        return get_client()

    @responses.activate
    def test_exceptions_on_submission(self):
        responses.add(
            responses.POST,
            settings.RESPOND_API_BASE_URL + "case.svc/TestCreateComplaints",
            body=requests.RequestException(),
        )
        with self.assertRaises(RespondClientException):
            self.client.create_case("TestCreateComplaints", self.xml)
