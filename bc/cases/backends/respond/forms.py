import datetime
import logging
from collections import defaultdict

import django.forms

from lxml import etree

from .constants import (
    DEFAULT_STANAGEDICFIXELDS,
    DESCRIPTION_SCHEMA_NAME,
    XML_ENTITY_MAPPING,
)

logger = logging.getLogger(__name__)


class BaseCaseForm(django.forms.Form):
    append_to_description_fields = []

    def create_element(self, key, value):
        element = etree.Element("field", schemaName=key)
        value_element = etree.SubElement(element, "value")
        value_element.text = value
        return element

    def cast(self, value):
        if isinstance(value, datetime.date):
            value = str(value)
        return value

    def get_xml(self, cleaned_data):
        case = etree.Element(
            "case", Tag="", xmlns="http://www.aptean.com/respond/caserequest/1"
        )

        entities = defaultdict(list)

        # Add required field values
        entities["Case"].append(
            self.create_element("Case.FeedbackType", self.feedback_type)
        )
        for schema_name, value in DEFAULT_STANAGEDICFIXELDS.items():
            entity_name = schema_name.partition(".")[0]
            entities[entity_name].append(self.create_element(schema_name, value))

        description = cleaned_data.pop("description")
        for field in self.append_to_description_fields:
            value = self.cleaned_data[field.name]
            value = self.cast(value)
            # Special case: append this type of field to the description, rather than
            # creating an XML element.
            description = description + f"\n\n{field.label}:\n{value}"
            continue

        # Convert the fields to XML elements in entities dict
        for key, schema_name in self.field_schema_name_mapping.items():
            if schema_name == DESCRIPTION_SCHEMA_NAME:
                # We've handled the description separately
                continue
            value = self.cleaned_data[key]
            value = self.cast(value)
            entity_name = schema_name.partition(".")[0]
            entities[entity_name].append(self.create_element(schema_name, value))

        # Finally, add the updated description
        description_schema_entity_name = DESCRIPTION_SCHEMA_NAME.partition(".")[0]
        entities[description_schema_entity_name].append(
            self.create_element(DESCRIPTION_SCHEMA_NAME, description)
        )

        # Now assemble the XML document in the right order
        # Put Case fields at the root level, and first.
        for element in entities["Case"]:
            case.append(element)

        for (
            entity_name,
            (outer_container_name, container_name),
        ) in XML_ENTITY_MAPPING.items():
            # Do nothing if we have no elements
            if entity_name not in entities:
                continue

            outer_container = etree.SubElement(case, outer_container_name)
            parent = etree.SubElement(outer_container, container_name, Tag="")

            for element in entities[entity_name]:
                parent.append(element)

        return case

    def get_xml_string(self):
        return etree.tostring(self.get_xml(self.cleaned_data))

    @property
    def field_schema_name_mapping(self):
        raise NotImplementedError
