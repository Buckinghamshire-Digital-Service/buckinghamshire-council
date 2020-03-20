from django import forms
from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import FORM_FIELD_CHOICES, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.search import index

from wagtailcaptcha.models import WagtailCaptchaEmailForm

from bc.utils.constants import RICH_TEXT_FEATURES
from bc.utils.models import BasePage
from bc.utils.widgets import (
    CustomCheckboxSelectMultiple,
    CustomCheckboxSelectSingle,
    CustomHeadingField,
    CustomSubheadingField,
)


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields")
    CHOICES = FORM_FIELD_CHOICES + (
        ("heading", "Heading"),
        ("subheading", "Subheading"),
    )

    # Override the field_type field with extended choices
    field_type = models.CharField(
        verbose_name="field type", max_length=16, choices=CHOICES
    )


class CustomFormBuilder(FormBuilder):
    # create a function that returns an instanced Django form field
    # function name must match create_<field_type_key>_field
    def create_heading_field(self, field, options):
        options["initial"] = options["label"]
        options["required"] = False

        return forms.Field(widget=CustomHeadingField, **options)

    def create_subheading_field(self, field, options):
        options["initial"] = options["label"]
        options["required"] = False

        return forms.Field(widget=CustomSubheadingField, **options)

    def create_checkbox_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        return forms.BooleanField(widget=CustomCheckboxSelectSingle, **options)

    def create_checkboxes_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        options["choices"] = [(x.strip(), x.strip()) for x in field.choices.split(",")]
        options["initial"] = [x.strip() for x in field.default_value.split(",")]
        return forms.MultipleChoiceField(widget=CustomCheckboxSelectMultiple, **options)


# Never cache form pages since they include CSRF tokens.
@method_decorator(never_cache, name="serve")
class FormPage(WagtailCaptchaEmailForm, BasePage):
    template = "patterns/pages/forms/form_page.html"
    landing_page_template = "patterns/pages/forms/form_page_landing.html"

    subpage_types = []

    introduction = models.TextField(blank=True)
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text displayed to the user on successful submission of the form",
        features=RICH_TEXT_FEATURES,
    )
    action_text = models.CharField(
        max_length=32, blank=True, help_text='Form action text. Defaults to "Submit"'
    )

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("action_text"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    form_builder = CustomFormBuilder
