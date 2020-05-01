import datetime
import logging
from base64 import b64encode
from collections import OrderedDict, defaultdict

import django.forms
from django.core.cache import cache
from django.core.validators import FileExtensionValidator

from lxml import etree

from .constants import (
    ACTIVITY_TITLE_SCHEMA_NAME,
    APPEND_TO_DESCRIPTION,
    ATTACHMENT_ACTIVITY_TITLE,
    ATTACHMENT_SCHEMA_NAME,
    CATEGORY_DATA_TYPE,
    CREATE_CASE_SERVICES,
    DESCRIPTION_SCHEMA_NAME,
    FIELD_MAPPINGS,
    FIELD_TYPES,
    FILE_DATA_TYPE,
    RESPOND_CATEGORIES_CACHE_PREFIX,
    RESPOND_FIELDS_CACHE_PREFIX,
    SHORT_TEXT_DATA_TYPE,
    VALID_FILE_EXTENSIONS,
    XML_ENTITY_MAPPING,
)

logger = logging.getLogger(__name__)


class BaseCaseForm(django.forms.Form):
    def create_element(self, key, value):
        element = etree.Element("field", schemaName=key)
        value_element = etree.SubElement(element, "value")
        value_element.text = value
        return element

    def create_attachments_element(self, files, location_type="Database"):
        element = etree.Element("Attachments")
        for file in files:
            attachment_element = etree.SubElement(
                element,
                "attachment",
                locationType=location_type,
                summary=file.name,
                location=file.name,
                tag="",
            )
            attachment_element.text = b64encode(file.read())
        return element

    def cast(self, value):
        if isinstance(value, datetime.date):
            value = str(value)
        return value

    def get_xml(self, cleaned_data):
        case = etree.Element(
            "case", Tag="", xmlns="http://www.aptean.com/respond/caserequest/1"
        )

        # Add required field values
        service_name = cleaned_data.pop("service_name")
        cleaned_data.update(CREATE_CASE_SERVICES[service_name]["stanagedicfixelds"])

        description = cleaned_data.pop(DESCRIPTION_SCHEMA_NAME)
        entities = defaultdict(list)

        # Convert the fields to XML elements in entities dict
        for key, value in cleaned_data.items():
            entity_name = key.partition(".")[0]
            if key == ATTACHMENT_SCHEMA_NAME:
                # The documentation tells only of the Activity.Note element, but we use
                # the undocumented Activity.Title field for fun, because it lands in a
                # more sensible place; we hardcode the title.
                entities[entity_name].append(
                    self.create_element(
                        ACTIVITY_TITLE_SCHEMA_NAME, ATTACHMENT_ACTIVITY_TITLE
                    )
                )

                files = self.files.getlist(ATTACHMENT_SCHEMA_NAME)
                entities[entity_name].append(self.create_attachments_element(files))
                continue

            value = self.cast(value)
            if entity_name == APPEND_TO_DESCRIPTION:
                # Special case: append this type of field to the description, rather
                # than creating an XML element.
                label = self.fields[key].label
                description = description + f"\n\n{label}:\n{value}"
                continue

            entities[entity_name].append(self.create_element(key, value))

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

        self.service_name = self.web_service_definition.find("name").text.strip()
        formfields["service_name"] = self.create_TextInput_field(
            schema_name="",
            options={
                "initial": self.service_name,
                "widget": django.forms.widgets.HiddenInput(),
            },
        )

        field_mapping = FIELD_MAPPINGS[self.service_name]

        # It's much faster to build a dict of field elements and use dictionary lookups
        # than to use self.web_service_definition.find(**{schema-name: schema_name}) on
        # a per-field basis.
        field_defs = {
            xml_field.attrs["schema-name"]: xml_field
            for xml_field in self.web_service_definition.find_all("field")
        }

        for label, schema_name in field_mapping.items():
            if schema_name.startswith(APPEND_TO_DESCRIPTION):
                # special case
                options = self.get_field_options(schema_name, permit_cache_miss=True)
                if "choices" in options:
                    data_type = CATEGORY_DATA_TYPE
                else:
                    data_type = SHORT_TEXT_DATA_TYPE
            elif schema_name == ATTACHMENT_SCHEMA_NAME:
                # special case: file attachments are appended to the Activity.Title
                # LongText field
                data_type = FILE_DATA_TYPE
                options = self.get_field_options(schema_name)
            else:
                xml_field = field_defs[schema_name]
                data_type = xml_field.attrs["data-type"]
                options = self.get_field_options(schema_name)

            options["label"] = label

            try:
                data_type = CREATE_CASE_SERVICES[self.service_name][
                    "field_type_overrides"
                ][schema_name]
            except KeyError:
                pass

            try:
                field_type = FIELD_TYPES[data_type]
            except KeyError:
                raise ValueError("Unexpected field data type encountered")
            create_field = getattr(self, f"create_{field_type}_field")
            formfields[schema_name] = create_field(schema_name, options)
        return formfields

    def create_TextInput_field(self, schema_name, options):
        options["max_length"] = 255
        return django.forms.CharField(**options)

    def create_Textarea_field(self, schema_name, options):
        return django.forms.CharField(widget=django.forms.Textarea, **options)

    def create_DateInput_field(self, schema_name, options):
        return django.forms.DateField(**options)

    def create_RadioSelect_field(self, schema_name, options):
        """A radio input"""
        if "choices" not in options:
            cache_key = RESPOND_CATEGORIES_CACHE_PREFIX + schema_name
            cached_choices = cache.get(cache_key)
            options["choices"] = cached_choices
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)

    def create_FileField_field(self, schema_name, options):
        return django.forms.FileField(
            validators=[
                FileExtensionValidator(allowed_extensions=VALID_FILE_EXTENSIONS)
            ],
            widget=django.forms.ClearableFileInput(attrs={"multiple": True}),
            **options,
        )

    def get_field_options(self, schema_name, permit_cache_miss=False):
        """ This may end up just returning 'required' or not. """
        cache_key = RESPOND_FIELDS_CACHE_PREFIX + schema_name
        options = cache.get(cache_key, {})
        if not options and not permit_cache_miss:
            raise Exception(f"Cache miss for field options: key={cache_key}")

        try:
            options.update(
                CREATE_CASE_SERVICES[self.service_name]["custom_field_options"][
                    schema_name
                ]
            )
        except KeyError:
            pass
        return options

    def get_form_class(self):
        return type("CaseForm", (BaseCaseForm,), self.formfields)
