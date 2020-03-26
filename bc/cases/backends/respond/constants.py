from collections import OrderedDict

CREATE_CASE_TYPE = "CaseCreate"
FIELD_INFO_TYPE = "FieldInfo"
CATEGORY_INFO_TYPE = "CategoryInfo"

COMPLAINTS_WEBSERVICE = "TestCreateComplaints"
FOI_WEBSERVICE = "TestCreateFOI"

CREATE_CASE_SERVICES = [COMPLAINTS_WEBSERVICE, FOI_WEBSERVICE]

RESPOND_FIELDS_CACHE_PREFIX = "respond_field__"
RESPOND_CATEGORIES_CACHE_PREFIX = "respond_categories__"

FIELD_MAPPINGS = {
    COMPLAINTS_WEBSERVICE: OrderedDict(
        [
            ("Your Involvement", "Contact.ContactType"),
            # TODO This field is missing from the API response
            # ("Which service is this about?", "Service Area"),
            ("Your complaint", "Case.Description"),
            (
                "What would you like to happen as a result of your complaint?",
                "Case.ActionTaken01",
            ),
            (
                "Please provide any relevant reference numbers and detail",
                "Case.AdditionalComments",
            ),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Surname", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    FOI_WEBSERVICE: OrderedDict(
        [
            ("Organisation/Company name", "Contact.Organisation"),
            ("What information do you need", "Case.Description"),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.HomePhone"),
            ("Street ", "Contact.Address01"),
            ("Town", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
}


"""Help text format:
>>> {
    service_name: {
        SchemaName: text_string
    }
}
"""
HELP_TEXT = {
    COMPLAINTS_WEBSERVICE: {
        "Case.Description": "Which service is this about? What happened and when?",
        "Contact.OtherTitle": "optional",
    },
    FOI_WEBSERVICE: {
        "Case.Description": (
            "Where appropriate, include names, dates, references and descriptions to "
            "enable us to identify and locate the required information"
        )
    },
}


"""Custom options format:
>>> {
    SchemaName: {
        provided_label: desired_label
    }
}
"""
CUSTOM_OPTIONS = {
    "Contact.ContactType": {
        "Primary": "I am the complainant",
        "Secondary": "I represent someone else",
    }
}


XML_ENTITY_MAPPING = OrderedDict(
    [
        # Format
        # (schema-name prefix, (outer container element, container element))
        ("Aspect", ("Aspects", "aspect")),
        ("Qualities", ("Qualities", "qualities")),
        ("Contact", ("Contacts", "contact")),
        ("Task", ("Tasks", "task")),
        ("Cost", ("Costs", "cost")),
        ("Activity", ("Activities", "activity")),
    ]
)

# Hardcode some fields
CASE_FEEDBACK_TYPE_VALUE = "Corporate"
CASE_HOW_RECEIVED_VALUE = "Web Form"
CONTACT_CONTACT_IS_VALUE = "Other"
