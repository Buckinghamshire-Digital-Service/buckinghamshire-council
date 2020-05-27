import textwrap
from unittest import mock

from django import forms
from django.conf import settings
from django.test import TestCase

from bs4 import BeautifulSoup
from lxml import etree

from bc.cases.backends.respond.constants import (
    APPEND_TO_DESCRIPTION,
    DESCRIPTION_SCHEMA_NAME,
    RESPOND_CATEGORIES_CACHE_PREFIX,
    RESPOND_FIELDS_CACHE_PREFIX,
)
from bc.cases.backends.respond.forms import BaseCaseForm, CaseFormBuilder
from bc.cases.backends.respond.tests.fixtures import generate_webservice_xml

cache_dict = None


def mock_cache_get(key, default=None):
    if key.startswith(RESPOND_CATEGORIES_CACHE_PREFIX):
        return ["foo", "bar"]
    if key.startswith(RESPOND_FIELDS_CACHE_PREFIX):
        return {"required": False}


@mock.patch("bc.cases.backends.respond.forms.cache.get", side_effect=mock_cache_get)
class TestFormBuilder(TestCase):
    def test_basic(self, mock_cache_get):
        Form = CaseFormBuilder(generate_webservice_xml()).get_form_class()
        self.assertTrue(issubclass(Form, BaseCaseForm))
        self.assertTrue(issubclass(Form, forms.Form))

    def test_help_text(self, mock_cache_get):
        with mock.patch.dict(
            "bc.cases.backends.respond.forms.CREATE_CASE_SERVICES",
            {
                settings.RESPOND_COMPLAINTS_WEBSERVICE: {
                    "custom_field_options": {
                        DESCRIPTION_SCHEMA_NAME: {"help_text": "foo"}
                    }
                }
            },
        ):
            form = CaseFormBuilder(generate_webservice_xml()).get_form_class()()
        self.assertEqual(form.fields[DESCRIPTION_SCHEMA_NAME].help_text, "foo")

    def test_hidden_service_name_field(self, mock_cache_get):
        form = CaseFormBuilder(generate_webservice_xml()).get_form_class()()
        self.assertIn("service_name", form.fields)
        service_name = form.fields["service_name"]
        self.assertIsInstance(service_name.widget, forms.widgets.HiddenInput)


class TestFormXML(TestCase):
    def test_appending_a_custom_field_to_the_description(self):
        extra_field_name = APPEND_TO_DESCRIPTION + ".time_period"

        class TestCaseForm(BaseCaseForm):
            def __init__(self, *args, **kwargs):
                super().__init__(self, *args, **kwargs)
                self.fields = {
                    DESCRIPTION_SCHEMA_NAME: forms.CharField(label="Description"),
                    extra_field_name: forms.CharField(
                        label="Extra field to be appended"
                    ),
                }

        form = TestCaseForm()

        cleaned_data = {
            DESCRIPTION_SCHEMA_NAME: "Some description",
            extra_field_name: "Two weeks last Sunday",
            "service_name": settings.RESPOND_SAR_WEBSERVICE,
        }
        soup = BeautifulSoup(etree.tostring(form.get_xml(cleaned_data)), "xml")
        self.assertEqual(
            soup.find(schemaName=DESCRIPTION_SCHEMA_NAME).text,
            textwrap.dedent(
                """\
                Some description

                Extra field to be appended:
                Two weeks last Sunday"""
            ),
        )

    def test_appending_two_custom_fields_to_the_description(self):
        extra_field_one = APPEND_TO_DESCRIPTION + ".context"
        extra_field_two = APPEND_TO_DESCRIPTION + ".song"

        class TestCaseForm(BaseCaseForm):
            def __init__(self, *args, **kwargs):
                super().__init__(self, *args, **kwargs)
                self.fields = {
                    DESCRIPTION_SCHEMA_NAME: forms.CharField(label="Description"),
                    extra_field_one: forms.CharField(label="First extra field"),
                    extra_field_two: forms.CharField(label="Second extra field"),
                }

        form = TestCaseForm()

        cleaned_data = {
            DESCRIPTION_SCHEMA_NAME: "Some description",
            extra_field_one: "Synthetic past",
            extra_field_two: "Spider bite",
            "service_name": settings.RESPOND_SAR_WEBSERVICE,
        }
        soup = BeautifulSoup(etree.tostring(form.get_xml(cleaned_data)), "xml")
        self.assertEqual(
            soup.find(schemaName=DESCRIPTION_SCHEMA_NAME).text,
            textwrap.dedent(
                """\
                Some description

                First extra field:
                Synthetic past

                Second extra field:
                Spider bite"""
            ),
        )


class SchemaTest(TestCase):

    known_xml = """<case Tag="" xmlns="http://www.aptean.com/respond/caserequest/1">
  <field schemaName="Case.ActionTaken01">
    <value></value>
  </field>
  <field schemaName="Case.AdditionalComments">
    <value></value>
  </field>
  <field schemaName="Case.FeedbackType">
    <value>Corporate</value>
  </field>
  <field schemaName="Case.HowReceived">
    <value>Web Form</value>
  </field>
  <field schemaName="Case.Description">
    <value>I don\'t like fish.</value>
  </field>
  <Contacts>
    <contact Tag="">
      <field schemaName="Contact.Clientis">
        <value>212f3677-b4f5-4461-b62f-fd7f4fe2bdcc</value>
      </field>
      <field schemaName="Contact.OtherTitle">
        <value>Kreivi</value>
      </field>
      <field schemaName="Contact.FirstName">
        <value></value>
      </field>
      <field schemaName="Contact.Surname">
        <value>M&#228;nnikk&#246;lahti</value>
      </field>
      <field schemaName="Contact.PreferredContactMethod">
        <value></value>
      </field>
      <field schemaName="Contact.Email">
        <value></value>
      </field>
      <field schemaName="Contact.Mobile">
        <value></value>
      </field>
      <field schemaName="Contact.Address01">
        <value></value>
      </field>
      <field schemaName="Contact.Town">
        <value></value>
      </field>
      <field schemaName="Contact.County">
        <value></value>
      </field>
      <field schemaName="Contact.ZipCode">
        <value></value>
      </field>
      <field schemaName="Contact.ContactIs">
        <value>Other</value>
      </field>
    </contact>
  </Contacts>
</case>
"""

    def setUp(self):
        with open("bc/cases/backends/respond/schemata/create_case.xsd", "r") as f:
            schema = etree.XMLSchema(etree.XML(f.read().encode("utf-8")))
        self.parser = etree.XMLParser(schema=schema)

    def test_aptean_provided_example_submission(self):
        with open(
            "bc/cases/backends/respond/schemata/example_create_case_submission.xml", "r"
        ) as f:
            etree.fromstring(f.read().encode("utf-8"), self.parser)

    def test_a_known_form_submission_validates(self):
        etree.fromstring(self.known_xml, self.parser)

    def test_form_converts_to_valid_xml(self):
        form = BaseCaseForm()
        cleaned_data = {
            "Contact.Clientis": "212f3677-b4f5-4461-b62f-fd7f4fe2bdcc",
            "Case.Description": "I don't like fish.",
            "Case.ActionTaken01": "",
            "Case.AdditionalComments": "",
            "Contact.OtherTitle": "Kreivi",
            "Contact.FirstName": "",
            "Contact.Surname": "Männikkölahti",
            "Contact.PreferredContactMethod": "",
            "Contact.Email": "",
            "Contact.Mobile": "",
            "Contact.Address01": "",
            "Contact.Town": "",
            "Contact.County": "",
            "Contact.ZipCode": "",
            "service_name": settings.RESPOND_COMPLAINTS_WEBSERVICE,
        }
        generated = etree.tostring(
            form.get_xml(cleaned_data), pretty_print=True
        ).decode()
        self.maxDiff = None
        self.assertEqual(generated, self.known_xml)
