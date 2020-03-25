from collections import defaultdict
from unittest import skip

from django.test import TestCase

from lxml import etree

from bc.cases.backends.respond.constants import XML_ENTITY_MAPPING
from bc.cases.backends.respond.forms import BaseCaseForm


class SchemaTest(TestCase):

    known_xml = """<case Tag="" xmlns="http://www.aptean.com/respond/caserequest/1">
  <field schemaName="Case.Description">
    <value>I don\'t like fish.</value>
  </field>
  <field schemaName="Case.ActionTaken01">
    <value></value>
  </field>
  <field schemaName="Case.AdditionalComments">
    <value></value>
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
        }
        generated = etree.tostring(
            form.get_xml(cleaned_data), pretty_print=True
        ).decode()
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
