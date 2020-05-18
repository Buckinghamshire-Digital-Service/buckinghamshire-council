import textwrap

from django import forms
from django.conf import settings
from django.test import TestCase

from bs4 import BeautifulSoup
from lxml import etree

from bc.cases.backends.respond.constants import (
    DESCRIPTION_SCHEMA_NAME,
    PREFERRED_CONTACT_METHOD_CHOICES,
)
from bc.cases.backends.respond.forms import BaseCaseForm
from bc.cases.forms import ComplaintForm


class TestFormXML(TestCase):
    def test_appending_a_custom_field_to_the_description(self):
        class TestCaseForm(BaseCaseForm):
            service_name = settings.RESPOND_SAR_WEBSERVICE
            feedback_type = "SAR"

            description = forms.CharField(label="Something")
            extra_field = forms.CharField(label="Extra field to be appended")

            @property
            def append_to_description_fields(self):
                return [self[name] for name in ["extra_field"]]

            field_schema_name_mapping = {"description": DESCRIPTION_SCHEMA_NAME}

        form_data = {
            "description": "Some description",
            "extra_field": "Two weeks last Sunday",
        }
        form = TestCaseForm(form_data)
        self.assertTrue(form.is_valid())
        soup = BeautifulSoup(etree.tostring(form.get_xml(form.cleaned_data)), "xml")
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
        class TestCaseForm(BaseCaseForm):
            service_name = settings.RESPOND_COMPLAINTS_WEBSERVICE
            feedback_type = "Corporate"

            description = forms.CharField(label="Description")
            extra_field_one = forms.CharField(label="First extra field")
            extra_field_two = forms.CharField(label="Second extra field")

            @property
            def append_to_description_fields(self):
                return [self[name] for name in ["extra_field_one", "extra_field_two"]]

            field_schema_name_mapping = {"description": DESCRIPTION_SCHEMA_NAME}

        form_data = {
            "description": "Some description",
            "extra_field_one": "Synthetic past",
            "extra_field_two": "Spider bite",
        }
        form = TestCaseForm(form_data)
        self.assertTrue(form.is_valid())
        soup = BeautifulSoup(etree.tostring(form.get_xml(form.cleaned_data)), "xml")
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
  <field schemaName="Case.FeedbackType">
    <value>Corporate</value>
  </field>
  <field schemaName="Case.HowReceived">
    <value>Web Form</value>
  </field>
  <field schemaName="Case.ActionTaken01">
    <value>I want this to happen</value>
  </field>
  <field schemaName="Case.AdditionalComments">
    <value>These are additional comments</value>
  </field>
  <field schemaName="Case.Description">
    <value>I don\'t like fish.</value>
  </field>
  <Contacts>
    <contact Tag="">
      <field schemaName="Contact.ContactIs">
        <value>Other</value>
      </field>
      <field schemaName="Contact.ContactType">
        <value>Primary</value>
      </field>
      <field schemaName="Contact.OtherTitle">
        <value>Kreivi</value>
      </field>
      <field schemaName="Contact.FirstName">
        <value>Vlad</value>
      </field>
      <field schemaName="Contact.Surname">
        <value>Dracula</value>
      </field>
      <field schemaName="Contact.PreferredContactMethod">
        <value>E-mail</value>
      </field>
      <field schemaName="Contact.Email">
        <value>user@example.com</value>
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
        form_data = {
            "your_involvement": "Primary",
            "organisation": "",
            "description": "I don't like fish.",
            "action_taken_01": "I want this to happen",
            "additional_comments": "These are additional comments",
            "title": "Kreivi",
            "first_name": "Vlad",
            "last_name": "Dracula",
            "contact_method": PREFERRED_CONTACT_METHOD_CHOICES[0][0],
            "email": "user@example.com",
            "contact_number": "",
            "address_01": "",
            "town": "",
            "county": "",
            "postcode": "",
        }
        form = ComplaintForm(form_data)
        self.assertTrue(form.is_valid())
        generated = etree.tostring(
            form.get_xml(form.cleaned_data), pretty_print=True
        ).decode()
        self.maxDiff = None
        self.assertEqual(generated, self.known_xml)
