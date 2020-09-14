from collections import OrderedDict

CREATE_CASE_TYPE = "CaseCreate"
FIELD_INFO_TYPE = "FieldInfo"
CATEGORY_INFO_TYPE = "CategoryInfo"

APPEND_TO_DESCRIPTION = "append to description"
DESCRIPTION_SCHEMA_NAME = "Case.Description"
ACTIVITY_TITLE_SCHEMA_NAME = "Activity.Title"
ATTACHMENT_SCHEMA_NAME = "Activity.Note"

ATTACHMENT_FAILURE_ERROR = "AttachmentFailure"
ATTACHMENT_ACTIVITY_TITLE = "Web form attachments"

APTEAN_FORM_COMPLAINT = "complaint"
APTEAN_FORM_FOI = "foi"
APTEAN_FORM_SAR = "sar"
APTEAN_FORM_COMMENT = "comments"
APTEAN_FORM_COMPLIMENT = "compliments"
APTEAN_FORM_DISCLOSURE = "disclosures"

APTEAN_FORM_CHOICES = [
    (APTEAN_FORM_COMPLAINT, "Complaint"),
    (APTEAN_FORM_FOI, "FOI"),
    (APTEAN_FORM_SAR, "SAR"),
    (APTEAN_FORM_COMMENT, "Comments"),
    (APTEAN_FORM_COMPLIMENT, "Compliments"),
    (APTEAN_FORM_DISCLOSURE, "Disclosures"),
]

CONTACT_METHOD_EMAIL = "E-mail"
CONTACT_METHOD_POST = "Letter"
CONTACT_METHOD_PHONE = "Contact Number"

PREFERRED_CONTACT_METHOD_CHOICES = [
    # NB the keys must match the Aptean Respond categories definitions
    (CONTACT_METHOD_EMAIL, "Email"),
    (CONTACT_METHOD_POST, "Post"),
    (CONTACT_METHOD_PHONE, "Phone"),
]
COMPLAINTS_CONTACT_METHOD_CHOICES = [
    # Don't include phone
    (CONTACT_METHOD_EMAIL, "Email"),
    (CONTACT_METHOD_POST, "Post"),
]

CONTACT_TYPE_PRIMARY = "Primary"
CONTACT_TYPE_SECONDARY = "Secondary"

VALID_FILE_EXTENSIONS = [
    "bmp",
    "csv",
    "doc",
    "docx",
    "dot",
    "dotx",
    "eml",
    "gif",
    "jpeg",
    "jpg",
    "m4a",
    "mp3",
    "msg",
    "pdf",
    "png",
    "pptx",
    "rtf",
    "txt",
    "wav",
    "xls",
    "xlsm",
    "xlsx",
    "zip",
]

# Stanagedicfixelds (system-managed static fixed fields) are fields to be hardcoded with
# every form submission to the Aptean Respond create case web service endpoints.
DEFAULT_STANAGEDICFIXELDS = {
    "Case.HowReceived": "Web Form",
    "Contact.ContactIs": "Other",
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
