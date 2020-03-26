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
            ("Your Involvement", "Client is"),
            # TODO This field is missing from the API response
            # ("Which service is this about?", "Service Area"),
            ("Your complaint", "Description"),
            (
                "What would you like to happen as a result of your complaint?",
                "Desired outcome(s)",
            ),
            (
                "Please provide any relevant reference numbers and detail",
                "Additional Comments",
            ),
            ("Title", "Other Title"),
            ("First name", "First Name"),
            ("Surname", "Surname"),
            ("How would you prefer to be contacted?", "Preferred Contact Method"),
            ("Email address", "E-mail Address"),
            ("Contact number", "Contact Number"),
            ("Street", "Address Line 1"),
            ("Town", "Town"),
            ("County", "County"),
            ("Postcode", "Postcode"),
        ]
    ),
    FOI_WEBSERVICE: OrderedDict(
        [
            ("Organisation/Company name", "Organisation"),
            ("What information do you need", "Description"),
            ("Title", "Other Title"),
            ("First name", "First Name"),
            ("Last name", "Surname"),
            ("How would you prefer to be contacted?", "Preferred Contact Method"),
            ("Email address", "E-mail Address"),
            ("Contact number", "Home Phone"),
            ("Street ", "Address Line 1"),
            ("Town", "Town"),
            ("County", "County"),
            ("Postcode", "Postcode"),
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
    COMPLAINTS_WEBSERVICE: {},
    FOI_WEBSERVICE: {
        "Description": (
            "Where appropriate, include names, dates, references and descriptions to "
            "enable us to identify and locate the required information"
        )
    },
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

CASE_FEEDBACK_TYPE = "Corporate"
CASE_HOW_RECEIVED = "Web Form"
CONTACT_CONTACT_IS = "Other"
