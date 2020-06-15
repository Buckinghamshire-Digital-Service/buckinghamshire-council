import datetime

from django import forms
from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.utils.timezone import now

from bc.cases.backends.respond.constants import (
    CONTACT_METHOD_EMAIL,
    CONTACT_METHOD_PHONE,
    CONTACT_METHOD_POST,
    CONTACT_TYPE_PRIMARY,
    CONTACT_TYPE_SECONDARY,
    DESCRIPTION_SCHEMA_NAME,
    PREFERRED_CONTACT_METHOD_CHOICES,
)
from bc.cases.backends.respond.forms import BaseCaseForm as _BaseCaseForm
from bc.utils.validators import get_current_year
from bc.utils.widgets import CustomCheckboxSelectMultiple, TelephoneNumberInput


class BaseCaseForm(_BaseCaseForm):

    title = forms.CharField(label="Title", required=False)
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    contact_method = forms.ChoiceField(
        label="How would you prefer to be contacted?",
        choices=PREFERRED_CONTACT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={"data-conditional-input": ""}),
    )
    email = forms.EmailField(label="Email address", required=False)
    email.widget.attrs.update({"autocomplete": "", "autocapitalize": "off"})
    contact_number = forms.CharField(label="Telephone number", require=False)
        required=False,
        widget=TelephoneNumberInput(),
        # This duplicates the API validation, saving a round trip
        validators=[
            MinLengthValidator(
                11, "Enter a telephone number that is 11 or 12 digits long"
            ),
            MaxLengthValidator(
                12, "Enter a telephone number that is 11 or 12 digits long"
            ),
        ],
    )
    address_01 = forms.CharField(label="Building and street address", required=False)
    town = forms.CharField(label="Town or city", required=False)
    county = forms.CharField(label="County", required=False)
    postcode = forms.CharField(required=False)

    @property
    def address_field_group(self):
        return [self[name] for name in ("address_01", "town", "county", "postcode")]

    field_schema_name_mapping = {
        "title": "Contact.OtherTitle",
        "first_name": "Contact.FirstName",
        "last_name": "Contact.Surname",
        "contact_method": "Contact.PreferredContactMethod",
        "email": "Contact.Email",
        "contact_number": "Contact.Mobile",
        "address_01": "Contact.Address01",
        "town": "Contact.Town",
        "county": "Contact.County",
        "postcode": "Contact.ZipCode",
    }

    def clean(self):
        cleaned_data = super().clean()

        # Add conditional required field error messages
        contact_method = cleaned_data.get("contact_method")
        if contact_method == CONTACT_METHOD_EMAIL and not cleaned_data.get("email"):
            self.add_error("email", "Enter your email address")
        if contact_method == CONTACT_METHOD_POST:
            for field_name in ["address_01", "town", "county", "postcode"]:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "Enter your address details")
        if contact_method == CONTACT_METHOD_PHONE and not self.data.get(
            "contact_number"
        ):
            self.add_error("contact_number", "Enter your telephone number")
        return cleaned_data


class ComplaintForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/generic_form.html"
    webservice = settings.RESPOND_COMPLAINTS_WEBSERVICE
    feedback_type = "Corporate"

    your_involvement = forms.ChoiceField(
        label="Who are you complaining for?",
        choices=[
            # NB the keys must match the Aptean Respond categories definitions
            (CONTACT_TYPE_PRIMARY, "Myself"),
            (CONTACT_TYPE_SECONDARY, "Someone else"),
        ],
        widget=forms.RadioSelect(),
    )
    description = forms.CharField(
        label="Your complaint",
        widget=forms.Textarea,
        help_text="Tell us which service this is about, what happened and when",
    )
    action_taken_01 = forms.CharField(
        label="What would you like to happen as a result of your complaint?",
        widget=forms.Textarea,
    )
    additional_comments = forms.CharField(
        label=(
            "If you have contacted us about this issue before and you have a "
            "reference number, enter it here"
        ),
        required=False,
    )

    @property
    def field_group_1(self):
        return [
            self[name]
            for name in (
                "your_involvement",
                "description",
                "action_taken_01",
                "additional_comments",
                "title",
                "first_name",
                "last_name",
            )
        ]

    field_schema_name_mapping = {
        "your_involvement": "Contact.ContactType",
        "description": DESCRIPTION_SCHEMA_NAME,
        "action_taken_01": "Case.ActionTaken01",
        "additional_comments": "Case.AdditionalComments",
    }
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)


class FOIForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/foi_form.html"
    webservice = settings.RESPOND_FOI_WEBSERVICE
    feedback_type = "FOI/EIR"

    your_involvement = forms.ChoiceField(
        label="Who are you requesting information for?",
        choices=[
            # NB the keys must match the Aptean Respond categories definitions
            (CONTACT_TYPE_PRIMARY, "Myself"),
            (CONTACT_TYPE_SECONDARY, "For a company or organisation",),
        ],
        widget=forms.RadioSelect(attrs={"data-conditional-input": ""}),
    )
    organisation = forms.CharField(
        label="Name of company or organisation", required=False
    )

    description = forms.CharField(
        label="What information do you need?",
        widget=forms.Textarea,
        help_text="Tell us in as much detail as you can to help us find it."
        "For example, a description of the information, names, dates and any reference numbers.",
    )

    field_schema_name_mapping = {
        "your_involvement": "Contact.ContactType",
        "organisation": "Contact.Organisation",
        "description": DESCRIPTION_SCHEMA_NAME,
    }
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)

    def clean(self):
        cleaned_data = super().clean()
        your_involvement = cleaned_data.get("your_involvement")
        organisation = cleaned_data.get("organisation")

        # organisation is required if contact is secondary
        if your_involvement == CONTACT_TYPE_SECONDARY and not organisation:
            # Only do something if both fields are valid so far.
            self.add_error("organisation", "Enter the name of the organisation")
        return cleaned_data


class SARForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/sar_form.html"
    webservice = settings.RESPOND_SAR_WEBSERVICE
    feedback_type = "SAR"
    YES = "Yes"
    NO = "No"

    your_involvement = forms.ChoiceField(
        label="Who are you requesting information for?",
        choices=[
            # NB the keys must match the Aptean Respond categories definitions
            (CONTACT_TYPE_PRIMARY, "Myself"),
            (CONTACT_TYPE_SECONDARY, "Someone else"),
        ],
        widget=forms.RadioSelect(),
    )
    description = forms.CharField(
        label="What information do you need?",
        widget=forms.Textarea,
        help_text="Tell us in as much detail as you can to help us find it. For "
        "example, a description of the information, names and any reference numbers, "
        "like a customer account number.",
    )
    time_period = forms.CharField(
        label="Which time period does your request cover?",
        help_text="For example, from March 2018 to November 2019",
    )

    buckinghamshire_council_employee = forms.ChoiceField(
        label="Do you work (or have you worked in the past) for Buckinghamshire Council or "
        "previous Buckinghamshire district councils?",
        choices=[(YES, "Yes"), (NO, "No")],
        widget=forms.RadioSelect(attrs={"data-conditional-input": ""}),
    )
    employee_id = forms.CharField(
        label="Your employee identification number", required=False
    )
    employment_dates = forms.CharField(
        label="Your approximate dates of employment", required=False
    )

    dob_day = forms.IntegerField(
        label="Day",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]*"}),
        min_value=1,
        max_value=31,
    )
    dob_month = forms.IntegerField(
        label="Month",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]*"}),
        min_value=1,
        max_value=12,
    )
    dob_year = forms.IntegerField(
        label="Year",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]{4}"}),
        validators=[
            MinValueValidator(1000, "Enter a 4-digit year"),
            MaxValueValidator(get_current_year, "Enter a date in the past"),
        ],
    )

    @property
    def append_to_description_fields(self):
        return [
            self[name]
            for name in [
                "time_period",
                "buckinghamshire_council_employee",
                "employee_id",
                "employment_dates",
            ]
        ]

    field_schema_name_mapping = {
        "your_involvement": "Contact.ContactType",
        "dob": "Contact.DateOfBirth",
        "description": DESCRIPTION_SCHEMA_NAME,
    }
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)

    def clean(self):
        cleaned_data = super().clean()
        buckinghamshire_council_employee = cleaned_data.get(
            "buckinghamshire_council_employee"
        )

        if buckinghamshire_council_employee == self.YES:
            # employment details are required
            if not cleaned_data.get("employee_id"):
                self.add_error("employee_id", "Enter your employee number")
            if not cleaned_data.get("employment_dates"):
                self.add_error("employment_dates", "Enter your employment dates")

        day = cleaned_data.get("dob_day")
        month = cleaned_data.get("dob_month")
        year = cleaned_data.get("dob_year")
        if day and month and year:
            try:
                dob = datetime.date(year, month, day)
            except ValueError:
                self.add_error(None, "Enter a valid date")
            else:
                if dob > now().date():
                    self.add_error(None, "Enter a date in the past")
                else:
                    cleaned_data["dob"] = dob

        return cleaned_data


class CommentForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/generic_form.html"
    webservice = settings.RESPOND_COMMENTS_WEBSERVICE
    feedback_type = "Corporate"

    service_name = forms.CharField(label="Which service is this about?",)
    description = forms.CharField(
        label="Your comment or suggestion", widget=forms.Textarea,
    )
    response_needed = forms.ChoiceField(
        label="Do you need a response from us?",
        choices=[("Yes", "Yes"), ("No", "No")],
        widget=forms.RadioSelect(),
    )

    @property
    def append_to_description_fields(self):
        return [self[name] for name in ["service_name", "response_needed"]]

    @property
    def field_group_1(self):
        return [
            self[name] for name in ("service_name", "description", "response_needed",)
        ]

    field_schema_name_mapping = {"description": DESCRIPTION_SCHEMA_NAME}
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)


class ComplimentForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/generic_form.html"
    webservice = settings.RESPOND_COMPLIMENTS_WEBSERVICE
    feedback_type = "Compliment"

    service_name = forms.CharField(label="Which service is this about?",)
    description = forms.CharField(label="Your compliment", widget=forms.Textarea,)

    @property
    def append_to_description_fields(self):
        return [self[name] for name in ["service_name"]]

    @property
    def field_group_1(self):
        return [self[name] for name in ("service_name", "description",)]

    field_schema_name_mapping = {"description": DESCRIPTION_SCHEMA_NAME}
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)


class DisclosureForm(BaseCaseForm):
    template_name = "patterns/organisms/form-templates/disclosures_form.html"
    webservice = settings.RESPOND_DISCLOSURES_WEBSERVICE
    feedback_type = "Disclosures"
    ACT_OF_PARLIAMENT = "Disclosure is required by an act of Parliament"

    organisation = forms.CharField(
        label="Name of your organisation",
        help_text="For example, Thames Valley Police.",
    )
    description = forms.CharField(
        label="What information do you need?",
        widget=forms.Textarea,
        help_text="Tell us in as much detail as you can to help us find it. "
        "For example, a description of the information, names, dates and any reference numbers.",
    )
    investigation = forms.CharField(
        label="What is the investigation?", widget=forms.Textarea,
    )
    reason = forms.MultipleChoiceField(
        label="Why do you need the information?",
        choices=[
            # Use a list comprehension to avoid repetition
            (x, x)
            for x in [
                "Without it the prevention or detection of crime will be prejudiced",
                "Without it the apprehension or prosecution of offenders will be prejudiced",
                "Without it the assessment or collection of any tax or duty will be prejudiced",
                "The data is necessary for the purpose of, or in connection with, "
                "legal proceedings or is otherwise necessary for the purpose of "
                "establishing, exercising or defending legal rights",
                "The data is necessary for the maintenance of effective immigration "
                "control and/or for the investigation or detection of activities that "
                "would undermine the maintenance of effective immigration control",
                ACT_OF_PARLIAMENT,
            ]
        ],
        help_text="Select all that apply",
        widget=CustomCheckboxSelectMultiple(),
    )
    act_of_parliament = forms.CharField(
        label="The name of the act, the year and the number of the section",
        required=False,
    )

    @property
    def field_group_1(self):
        return [
            self[name] for name in ("description", "title", "first_name", "last_name",)
        ]

    @property
    def append_to_description_fields(self):
        return [self[name] for name in ["investigation", "reason"]]

    field_schema_name_mapping = {
        "organisation": "Contact.Organisation",
        "description": DESCRIPTION_SCHEMA_NAME,
        "act_of_parliament": "Case.ActofParliament",
    }
    field_schema_name_mapping.update(BaseCaseForm.field_schema_name_mapping)

    def clean(self):
        cleaned_data = super().clean()
        act_of_parliament = cleaned_data.get("act_of_parliament")
        reason = cleaned_data.get("reason")

        # act of parliament is required if reason includes act of parliament
        if reason and self.ACT_OF_PARLIAMENT in reason and not act_of_parliament:
            self.add_error(
                "act_of_parliament",
                f"This field is required if you have selected '{self.ACT_OF_PARLIAMENT}'",
            )

        return cleaned_data
