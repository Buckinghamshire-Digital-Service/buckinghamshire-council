import logging
from collections import OrderedDict, defaultdict

import django.forms
from django.core.cache import cache

from lxml import etree

from .constants import (
    CASE_FEEDBACK_TYPE,
    CASE_HOW_RECEIVED,
    CONTACT_CONTACT_IS,
    FIELD_MAPPINGS,
    RESPOND_CATEGORIES_CACHE_PREFIX,
    RESPOND_FIELDS_CACHE_PREFIX,
    XML_ENTITY_MAPPING,
)

logger = logging.getLogger(__name__)

FIELD_TYPES = [
    # "Status", This one appears only in one web service, not of the create case type
    # "SystemAllocation", Maybe a foreign key field, used for data like 'created by'
    # "Journal", This appears only against a field with schema Case.ActionTaken
    ("Category", "RadioSelect"),
    ("DateTime", "DateInput"),
    ("LongText", "Textarea"),
    ("ShortText", "TextInput"),
]


class BaseCaseForm(django.forms.Form):
    def get_xml(self, cleaned_data):
        case = etree.Element(
            "case", Tag="", xmlns="http://www.aptean.com/respond/caserequest/1"
        )

        entities = defaultdict(list)

        # Add required field values
        # TODO: Case.FeedbackType and Contact.ContactIs may need to vary by form
        cleaned_data["Case.FeedbackType"] = CASE_FEEDBACK_TYPE
        cleaned_data["Case.HowReceived"] = CASE_HOW_RECEIVED
        cleaned_data["Contact.ContactIs"] = CONTACT_CONTACT_IS

        # The Contact.Title filed must be set to Other if the user
        # enters a title
        if cleaned_data["Contact.OtherTitle"] != "":
            cleaned_data["Contact.Title"] = "Other"

        # Convert the fields to XML elements in entities dict
        # reverse_field_types_dict = {k: v for v, k in FIELD_TYPES}
        for key, value in cleaned_data.items():
            entity_name = key.partition(".")[0]

            element = etree.Element(
                "field",
                **{
                    "schemaName": key,
                    # "field-type": reverse_field_types_dict[
                    #     self.fields[key].widget.__class__.__name__
                    # ],
                },
            )
            value_element = etree.SubElement(element, "value")
            value_element.text = value
            entities[entity_name].append(element)

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


class CaseFormBuilder:
    """Create a form from an XML Create Case element."""

    def __init__(self, web_service_definition):
        self.web_service_definition = web_service_definition

    @property
    def formfields(self):
        formfields = OrderedDict()

        # form_class = CreateCaseForm()

        """ example field element from the xml
        <field data-type="LongText" schema-name="Case.Description">
            <name locale="en-GB">
                Description
            </name>
        </field>
        """

        service_name = self.web_service_definition.find("name").text.strip()
        field_mapping = FIELD_MAPPINGS[service_name]

        # The webservice definition contains field name and schema name. We need to
        # match these to the client-supplied constants.FIELD_MAPPING which maps field
        # names to desired labels.
        field_defs = {
            xml_field.find("name").text: xml_field
            for xml_field in self.web_service_definition.find_all("field")
        }

        field_types_dict = dict(FIELD_TYPES)
        for label, name in field_mapping.items():
            xml_field = field_defs[name]
            schema_name = xml_field.attrs["schema-name"]
            data_type = xml_field.attrs["data-type"]
            try:
                field_type = field_types_dict[data_type]
            except KeyError:
                raise ValueError("Unexpected field data type encountered")
            create_field = getattr(self, f"create_{field_type}_field")
            options = self.get_field_options(xml_field)
            if not options:
                logger.error(f"options could not be found for field '{schema_name}")
                # TODO: We will end up here if a field definition is missing
                # from the field definition endpoint response. We should
                # probably raise an exception here
            options["label"] = label
            formfields[schema_name] = create_field(schema_name, options)
        return formfields

    def create_TextInput_field(self, schema_name, options):
        options["max_length"] = 255
        return django.forms.CharField(**options)

    def create_Textarea_field(self, schema_name, options):
        return django.forms.CharField(widget=django.forms.Textarea, **options)

    def create_datetime_field(self, options):
        return django.forms.DateTimeField(**options)

    # def create_email_field(self, schema_name, options):
    #     return django.forms.EmailField(**options)

    def create_RadioSelect_field(self, schema_name, options):
        """A radio input"""
        cache_key = RESPOND_CATEGORIES_CACHE_PREFIX + schema_name
        cached_choices = cache.get(cache_key)
        """ Example categories API response element
        <field data-type="Category" leaf-only="true" multiple-select="false" schema-name="Contact.ContactType">
            <name locale="en-GB">
                Contact Type
            </name>
            <options>
                <option available="true" id="552affc7-1596-4762-a771-3a47e5b3bab2">
                    <name locale="en-GB">
                        Primary
                    </name>
                </option>
                <option available="true" id="3286a683-7ce8-4b9e-bb78-af34ae0d9fe1">
                    <name locale="en-GB">
                        Secondary
                    </name>
                </option>
            </options>
        </field>
        """
        options["choices"] = cached_choices
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)

    def get_field_options(self, xml_field):
        """ This may end up just returning 'required' or not. """
        schema_name = xml_field.attrs["schema-name"]
        cache_key = RESPOND_FIELDS_CACHE_PREFIX + schema_name
        return cache.get(cache_key)

    def get_form_class(self):
        return type("CaseForm", (BaseCaseForm,), self.formfields)
