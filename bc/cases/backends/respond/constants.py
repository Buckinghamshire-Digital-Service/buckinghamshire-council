from collections import OrderedDict

from django.conf import settings

CREATE_CASE_TYPE = "CaseCreate"
FIELD_INFO_TYPE = "FieldInfo"
CATEGORY_INFO_TYPE = "CategoryInfo"

APPEND_TO_DESCRIPTION = "append to description"
DESCRIPTION_SCHEMA_NAME = "Case.Description"

RESPOND_FIELDS_CACHE_PREFIX = "respond_field__"
RESPOND_CATEGORIES_CACHE_PREFIX = "respond_categories__"

SHORT_TEXT_DATA_TYPE = "ShortText"
CATEGORY_DATA_TYPE = "Category"
FIELD_TYPES = {
    CATEGORY_DATA_TYPE: "RadioSelect",
    "DateTime": "DateInput",
    "LongText": "Textarea",
    SHORT_TEXT_DATA_TYPE: "TextInput",
}


# This defines the services to register, and provides options for them. The
# stanagedicfixelds (system-managed static fixed fields) options dictionary is processed
# when the module is loaded. Only set where they differ from those in the defaults set
# below here.
CREATE_CASE_SERVICES = {
    settings.RESPOND_COMPLAINTS_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "Corporate"},
        "custom_field_options": {
            DESCRIPTION_SCHEMA_NAME: {
                "help_text": "Which service is this about? What happened and when?"
            },
            "Contact.OtherTitle": {"help_text": "optional"},
            "Contact.PreferredContactMethod": {
                "required": True,
                "choices": [
                    ("E-mail", "E-mail"),
                    ("Letter", "Letter"),
                    ("Contact Number", "Contact Number"),
                ],
            },
        },
        "field_type_overrides": {
            "Case.ActionTaken01": SHORT_TEXT_DATA_TYPE,
            "Case.AdditionalComments": SHORT_TEXT_DATA_TYPE,
        },
    },
    settings.RESPOND_FOI_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "FOI/EIR"},
        "custom_field_options": {
            DESCRIPTION_SCHEMA_NAME: {
                "help_text": (
                    "Where appropriate, include names, dates, references and descriptions to "
                    "enable us to identify and locate the required information"
                )
            },
            "Contact.PreferredContactMethod": {
                "required": True,
                "choices": [
                    ("E-mail", "E-mail"),
                    ("Letter", "Letter"),
                    ("Contact Number", "Contact Number"),
                ],
            },
        },
    },
    settings.RESPOND_SAR_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "SAR"},
        "custom_field_options": {
            "Case.TypeofSAR": {
                "help_text": {
                    (
                        "Include any known reference numbers or other unique identifiers to help "
                        "us locate your personal data (for example, a customer account number)"
                    )
                }
            },
            "Contact.DateofBirth": {"help_text": "YYYY-MM-DD, for example, 1978-05-23"},
            APPEND_TO_DESCRIPTION
            + ".buckinghamshire_council_employee": {
                "choices": [("Yes", "Yes"), ("No", "No")]
            },
            APPEND_TO_DESCRIPTION
            + ".employee_id": {"required": False, "help_text": "optional"},
            APPEND_TO_DESCRIPTION
            + ".employment_dates": {"required": False, "help_text": "optional"},
            "Contact.PreferredContactMethod": {
                "required": True,
                "choices": [
                    ("E-mail", "E-mail"),
                    ("Letter", "Letter"),
                    ("Contact Number", "Contact Number"),
                ],
            },
        },
        "field_type_overrides": {"Case.Anyothercomments": SHORT_TEXT_DATA_TYPE},
    },
    settings.RESPOND_COMMENTS_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "Corporate"},
        "custom_field_options": {
            APPEND_TO_DESCRIPTION
            + ".response_needed": {"choices": [("Yes", "Yes"), ("No", "No")]},
            DESCRIPTION_SCHEMA_NAME: {"required": False, "help_text": "optional"},
            "Contact.PreferredContactMethod": {
                "required": True,
                "choices": [
                    ("E-mail", "E-mail"),
                    ("Letter", "Letter"),
                    ("Contact Number", "Contact Number"),
                ],
            },
        },
    },
    settings.RESPOND_COMPLIMENTS_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "Compliment"}
    },
    settings.RESPOND_DISCLOSURES_WEBSERVICE: {
        "stanagedicfixelds": {"Case.FeedbackType": "Disclosures"},
        "custom_field_options": {
            APPEND_TO_DESCRIPTION
            + ".reason": {
                "choices": [
                    # Use a list comprehension to avoid repetition
                    (x, x)
                    for x in [
                        "Without it the prevention or detection of crime will be prejudiced",
                        "Without it the apprehension or prosecution of offenders will be prejudiced",
                        "Without it the assessment or collection of any tax or duty will be prejudiced",
                        (
                            "The data is necessary for the purpose of, or in "
                            "connection with, legal proceedings or is otherwise "
                            "necessary for the purpose of establishing, exercising or "
                            "defending legal rights"
                        ),
                        (
                            "The data is necessary for the maintenance of effective "
                            "immigration control and/or for the investigation or "
                            "detection of activities that would undermine the "
                            "maintenance of effective"
                        ),
                        "Disclosure is required by an Act of Parliament",
                    ]
                ]
            },
            "Contact.PreferredContactMethod": {
                "required": True,
                "choices": [
                    ("E-mail", "E-mail"),
                    ("Letter", "Letter"),
                    ("Contact Number", "Contact Number"),
                ],
            },
        },
    },
    # TODO
    # DATA_BREACH_WEBSERVICE: {
    #     "stanagedicfixelds": {"Case.FeedbackType": "Data Breach"},
    # },
}

DEFAULT_STANAGEDICFIXELDS = {
    "Case.HowReceived": "Web Form",
    "Contact.ContactIs": "Other",
}

# Set defaults for services which have not set custom stanagedicfixelds
for service in CREATE_CASE_SERVICES.values():
    try:
        stanagedicfixelds = service["stanagedicfixelds"]
    except KeyError:
        service["stanagedicfixelds"] = DEFAULT_STANAGEDICFIXELDS
    else:
        for key in DEFAULT_STANAGEDICFIXELDS:
            if key not in stanagedicfixelds:
                stanagedicfixelds[key] = DEFAULT_STANAGEDICFIXELDS[key]


FIELD_MAPPINGS = {
    settings.RESPOND_COMPLAINTS_WEBSERVICE: OrderedDict(
        [
            ("Your Involvement", "Contact.ContactType"),
            ("Your complaint", DESCRIPTION_SCHEMA_NAME),
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
    settings.RESPOND_FOI_WEBSERVICE: OrderedDict(
        [
            ("Organisation/Company name", "Contact.Organisation"),
            ("What information do you need?", DESCRIPTION_SCHEMA_NAME),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    settings.RESPOND_SAR_WEBSERVICE: OrderedDict(
        [
            ("Your Involvement", "Contact.ContactType"),
            ("What personal information is required?", DESCRIPTION_SCHEMA_NAME),
            (
                "Which time period does your request cover?",
                APPEND_TO_DESCRIPTION + ".time_period",
            ),
            (
                "Do you work (or have worked in the past) for Buckinghamshire Council "
                "or previous Buckinghamshire District Councils?",
                APPEND_TO_DESCRIPTION + ".buckinghamshire_council_employee",
            ),
            (
                "Your employee identification number",
                APPEND_TO_DESCRIPTION + ".employee_id",
            ),
            (
                "Your approximate dates of employment",
                APPEND_TO_DESCRIPTION + ".employment_dates",
            ),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Surname", "Contact.Surname"),
            ("Previous names, if applicable", "Case.Anyothercomments"),
            ("Date of Birth", "Contact.DateofBirth"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    settings.RESPOND_COMMENTS_WEBSERVICE: OrderedDict(
        [
            ("Your comment or suggestion", DESCRIPTION_SCHEMA_NAME),
            (
                "Do you require a response from us?",
                APPEND_TO_DESCRIPTION + ".response_needed",
            ),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    settings.RESPOND_COMPLIMENTS_WEBSERVICE: OrderedDict(
        [
            ("Your comment or suggestion", DESCRIPTION_SCHEMA_NAME),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    settings.RESPOND_DISCLOSURES_WEBSERVICE: OrderedDict(
        [
            ("Details of information required", DESCRIPTION_SCHEMA_NAME),
            ("Information required because", APPEND_TO_DESCRIPTION + ".reason"),
            # TODO ("Do you wish to attach any documents to this request?",
            ("Name of your organisation", "Contact.Organisation"),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
}


"""Custom option labels for select input fields. Format:
>>> {
    SchemaName: {
        provided_label: desired_label
    }
}
"""
CUSTOM_OPTIONS = {
    "Contact.ContactType": {
        # Ideally this text would be different for Complaints and for SARs
        "Primary": "I am submitting this form for myself",
        "Secondary": "I represent someone else",
    }
}


# This is used to generate the submitted data in accordance with the provided schema
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
