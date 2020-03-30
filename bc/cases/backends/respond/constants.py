from collections import OrderedDict

CREATE_CASE_TYPE = "CaseCreate"
FIELD_INFO_TYPE = "FieldInfo"
CATEGORY_INFO_TYPE = "CategoryInfo"

APPEND_TO_DESCRIPTION = "append to description"
DESCRIPTION_SCHEMA_NAME = "Case.Description"

RESPOND_FIELDS_CACHE_PREFIX = "respond_field__"
RESPOND_CATEGORIES_CACHE_PREFIX = "respond_categories__"

# Known create case web services
COMPLAINTS_WEBSERVICE = "TestCreateComplaints"
FOI_WEBSERVICE = "TestCreateFOI"
SAR_WEBSERVICE = "TestCreateSAR"
COMMENTS_WEBSERVICE = "TestCreateComments"
COMPLIMENTS_WEBSERVICE = "TestCreateCompliments"
DISCLOSURE_WEBSERVICE = "TestCreateDisclosures"

# This defines the services to register, and provides options for them. Only set
# stanagedicfixelds (system-managed static fixed fields) where they differ from those in
# the defaults set below here. This options dictionary is processed when the module is
# loaded.
CREATE_CASE_SERVICES = {
    COMPLAINTS_WEBSERVICE: {
        "custom_field_options": {
            DESCRIPTION_SCHEMA_NAME: {
                "help_text": "Which service is this about? What happened and when?"
            },
            "Contact.OtherTitle": {"help_text": "optional"},
        },
        "field_type_overrides": {"Case.ActionTaken01": "TextInput"},
    },
    FOI_WEBSERVICE: {
        "custom_field_options": {
            DESCRIPTION_SCHEMA_NAME: {
                "help_text": {
                    "Where appropriate, include names, dates, references and descriptions to "
                    "enable us to identify and locate the required information"
                }
            }
        }
    },
    SAR_WEBSERVICE: {
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
        }
    },
    COMMENTS_WEBSERVICE: {},
    COMPLIMENTS_WEBSERVICE: {"stanagedicfixelds": {"Case.FeedbackType": "Compliment"}},
    DISCLOSURE_WEBSERVICE: {
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
            }
        }
    },
}

DEFAULT_STANAGEDICFIXELDS = {
    "Case.FeedbackType": "Corporate",
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
    COMPLAINTS_WEBSERVICE: OrderedDict(
        [
            ("Your Involvement", "Contact.ContactType"),
            # TODO This field is missing from the API response
            # ("Which service is this about?", "Service Area"),
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
    FOI_WEBSERVICE: OrderedDict(
        [
            ("Organisation/Company name", "Contact.Organisation"),
            ("What information do you need?", DESCRIPTION_SCHEMA_NAME),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            ("How would you prefer to be contacted?", "Contact.PreferredContactMethod"),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.HomePhone"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    SAR_WEBSERVICE: OrderedDict(
        [
            ("Your Involvement", "Contact.ContactType"),
            ("What personal information is required?", DESCRIPTION_SCHEMA_NAME),
            (
                "Which time period does your request cover?",
                APPEND_TO_DESCRIPTION + ".time_period",
            ),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Surname", "Contact.Surname"),
            ("Previous names, if applicable", "Case.Anyothercomments"),
            ("Date of Birth", "Contact.DateofBirth"),
            (
                "How would you prefer to be contacted? ",
                "Contact.PreferredContactMethod",
            ),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    COMMENTS_WEBSERVICE: OrderedDict(
        [
            ("Your comment or suggestion", DESCRIPTION_SCHEMA_NAME),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            (
                "How would you prefer to be contacted? ",
                "Contact.PreferredContactMethod",
            ),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    COMPLIMENTS_WEBSERVICE: OrderedDict(
        [
            ("Your comment or suggestion", DESCRIPTION_SCHEMA_NAME),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            (
                "How would you prefer to be contacted? ",
                "Contact.PreferredContactMethod",
            ),
            ("Email address", "Contact.Email"),
            ("Contact number", "Contact.Mobile"),
            ("Building and street address", "Contact.Address01"),
            ("Town or city", "Contact.Town"),
            ("County", "Contact.County"),
            ("Postcode", "Contact.ZipCode"),
        ]
    ),
    DISCLOSURE_WEBSERVICE: OrderedDict(
        [
            ("Details of information required", DESCRIPTION_SCHEMA_NAME),
            # NOTE 'nature of the investigation -> 'additionalcomments' in doc but not in API
            ("Information required because", APPEND_TO_DESCRIPTION + ".reason"),
            # TODO ("Do you wish to attach any documents to this request?",
            ("Are you an individual or a company?", "Contact.Organisation"),
            ("Title", "Contact.OtherTitle"),
            ("First name", "Contact.FirstName"),
            ("Last name", "Contact.Surname"),
            (
                "How would you prefer to be contacted? ",
                "Contact.PreferredContactMethod",
            ),
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
