import pathlib
import textwrap

from django.conf import settings
from django.test import TestCase, override_settings

import requests
import responses

from bc.cases.backends.respond.client import (
    RespondClient,
    RespondClientException,
    get_client,
)
from bc.cases.backends.respond.constants import CREATE_CASE_SERVICES, CREATE_CASE_TYPE


@override_settings(
    RESPOND_API_USERNAME="foo",
    RESPOND_API_PASSWORD="bar",
    RESPOND_API_BASE_URL="http://www.example.invalid/",
)
class TestNonMockedClient(TestCase):
    def test_client_exception_raised_when_misconfigured(self):
        with self.assertRaises(RespondClientException):
            RespondClient()


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
        with open(pathlib.Path(__file__).parent / "fixtures/getservices.xml", "r") as f:
            services_xml = f.read()
        with open(pathlib.Path(__file__).parent / "fixtures/getfields.xml", "r") as f:
            fields_xml = f.read()
        with open(
            pathlib.Path(__file__).parent / "fixtures/getcategories.xml", "r"
        ) as f:
            categories_xml = f.read()
        self.get_services_response_params = (
            (
                responses.GET,
                settings.RESPOND_API_BASE_URL + "metadata.svc/getservices",
                services_xml,
            ),
            {"status": 200, "content_type": "text/xml"},
        )
        self.get_fields_complaints_response_params = (
            (
                responses.GET,
                settings.RESPOND_API_BASE_URL
                + "metadata.svc/Fields/TestGetFieldsComplaints",
                fields_xml,
            ),
            {"status": 200, "content_type": "text/xml"},
        )
        self.get_category_complaints_response_params = (
            (
                responses.GET,
                settings.RESPOND_API_BASE_URL
                + "metadata.svc/Categories/TestGetCategoryComplaints",
                categories_xml,
            ),
            {"status": 200, "content_type": "text/xml"},
        )
        self.all_response_params = [
            self.get_services_response_params,
            self.get_fields_complaints_response_params,
            self.get_category_complaints_response_params,
        ]

    def get_client(
        self, responses_context_manager, response_params, force_refresh=True
    ):
        for args, kwargs in response_params:
            responses_context_manager.add(*args, **kwargs)
        return get_client(force_refresh)

    def test_creating_client(self):
        try:
            with responses.RequestsMock() as rsps:
                self.get_client(rsps, self.all_response_params)
        except Exception:
            self.fail("Creating test client failed unexpectedly")

    def test_creating_client_again_uses_existing_client(self):
        with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
            self.get_client(rsps, self.all_response_params)
            self.assertEqual(len(rsps.calls), 3)
            self.get_client(rsps, self.all_response_params, force_refresh=False)
            self.assertEqual(len(rsps.calls), 3)  # NB unchanged

    def test_creating_client_registers_create_case_services(self):
        with responses.RequestsMock() as rsps:
            client = self.get_client(rsps, self.all_response_params)
        with override_settings(
            RESPOND_COMPLAINTS_WEBSERVICE="TestCreateComplaints",
            RESPOND_FOI_WEBSERVICE="TestCreateFOI",
            RESPOND_SAR_WEBSERVICE="TestCreateSAR",
            RESPOND_COMMENTS_WEBSERVICE="TestCreateComments",
            RESPOND_COMPLIMENTS_WEBSERVICE="TestCreateCompliments",
            RESPOND_DISCLOSURES_WEBSERVICE="TestCreateDisclosures",
        ):
            for key in CREATE_CASE_SERVICES.keys():
                self.assertIn(key, client.services[CREATE_CASE_TYPE])

    def test_exceptions_on_submission(self):
        response_params = [
            self.get_services_response_params,
            self.get_fields_complaints_response_params,
            self.get_category_complaints_response_params,
            (
                (
                    responses.POST,
                    settings.RESPOND_API_BASE_URL + "case.svc/TestCreateComplaints",
                ),
                {"body": requests.RequestException()},
            ),
        ]
        with responses.RequestsMock() as rsps:
            client = self.get_client(rsps, response_params)
            with self.assertRaises(RespondClientException):
                client.create_case("TestCreateComplaints", self.post_xml)
