import textwrap

import requests
import responses
from django.conf import settings
from django.test import TestCase, override_settings

from bc.cases.backends.respond.client import RespondClientException, get_client


@override_settings(
    RESPOND_API_USERNAME="foo",
    RESPOND_API_PASSWORD="bar",
    RESPOND_API_BASE_URL="https://www.example.invalid/",
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)
class TestClient(TestCase):
    def setUp(self):
        self.post_xml = textwrap.dedent(
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

    def test_creating_client(self):
        try:
            get_client()
        except Exception:
            self.fail("Creating test client failed unexpectedly")

    @responses.activate
    def test_exceptions_on_submission(self):
        responses.add(
            responses.POST,
            settings.RESPOND_API_BASE_URL + "case.svc/TestCreateComplaints",
            body=requests.RequestException(),
        )
        client = get_client()
        with self.assertRaises(RespondClientException):
            client.create_case("TestCreateComplaints", self.post_xml)

    @responses.activate
    def test_normal_submission(self):
        responses.add(
            responses.POST,
            settings.RESPOND_API_BASE_URL + "case.svc/TestCreateComplaints",
            body="success",
        )
        client = get_client()
        try:
            client.create_case("TestCreateComplaints", self.post_xml)
        except RespondClientException:
            self.fail("client.create_case failed unexpectedly")
