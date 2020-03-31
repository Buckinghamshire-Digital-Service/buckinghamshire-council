import textwrap
from collections import defaultdict
from unittest import skip

from django import forms
from django.conf import settings
from django.test import TestCase

from bs4 import BeautifulSoup
from lxml import etree

from bc.cases.backends.respond.constants import (
    APPEND_TO_DESCRIPTION,
    DESCRIPTION_SCHEMA_NAME,
    XML_ENTITY_MAPPING,
)
from bc.cases.backends.respond.forms import BaseCaseForm


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

    # FIXME this needs to work
    @skip
    def test_building_xml(self):
        def element(entity_name):
            outer_container_name, container_name = XML_ENTITY_MAPPING[entity_name]
            outer_container = etree.Element(outer_container_name)
            etree.SubElement(outer_container, container_name, Tag="")
            return outer_container

        entities = defaultdict(element)  # noqa

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
        soup = BeautifulSoup(etree.tostring(form.get_xml(cleaned_data)), "lxml")
        self.assertEqual(
            soup.find(schemaname=DESCRIPTION_SCHEMA_NAME).text,
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
        soup = BeautifulSoup(etree.tostring(form.get_xml(cleaned_data)), "lxml")
        self.assertEqual(
            soup.find(schemaname=DESCRIPTION_SCHEMA_NAME).text,
            textwrap.dedent(
                """\
                Some description

                First extra field:
                Synthetic past

                Second extra field:
                Spider bite"""
            ),
        )
