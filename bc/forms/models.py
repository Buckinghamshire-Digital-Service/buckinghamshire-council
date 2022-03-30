import logging

from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.template.response import TemplateResponse
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.search import index

from wagtailcaptcha.models import WagtailCaptchaEmailForm

from bc.area_finder.utils import validate_postcode
from bc.forms.forms import LookupPageForm
from bc.utils.constants import RICH_TEXT_FEATURES
from bc.utils.models import BasePage, RelatedPage
from bc.utils.widgets import CustomCheckboxSelectMultiple, CustomCheckboxSelectSingle

logger = logging.getLogger(__name__)


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields")

    additional_text = RichTextField(
        blank=True, help_text="Rich text to display before the form field"
    )

    panels = AbstractFormField.panels + [FieldPanel("additional_text")]


class CustomFormBuilder(FormBuilder):
    # create a function that returns an instanced Django form field
    # function name must match create_<field_type_key>_field
    def create_checkbox_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        return forms.BooleanField(widget=CustomCheckboxSelectSingle, **options)

    def create_checkboxes_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        options["choices"] = [(x.strip(), x.strip()) for x in field.choices.split(",")]
        options["initial"] = [x.strip() for x in field.default_value.split(",")]
        return forms.MultipleChoiceField(widget=CustomCheckboxSelectMultiple, **options)


class FormPage(WagtailCaptchaEmailForm, BasePage):
    """A page with editorially controlled forms for anonymous users.

    We use custom CSRF middleware to exempt form pages from CSRF token checks.
    Maintain this in bc.utils.middleware.
    """

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


class PostcodeLookupResponse(models.Model):
    page = ParentalKey("forms.LookupPage", related_name="responses")
    answer = models.TextField(
        help_text="You can include the postcode in the answer by writing {postcode}.",
    )
    link_page = models.ForeignKey("wagtailcore.Page", on_delete=models.PROTECT)
    link_button_text = models.CharField(
        max_length=32, blank=True, help_text="Leave blank to use the link page title."
    )
    postcodes = ArrayField(
        models.CharField(max_length=10, validators=[validate_postcode]),
        help_text="Enter a comma-separated list of postcodes. Individual values will be validated and reformatted.",
    )

    panels = [
        FieldPanel("answer"),
        PageChooserPanel("link_page"),
        FieldPanel("link_button_text"),
        FieldPanel("postcodes"),
    ]

    query_parameter = "postcode"

    def __str__(self):
        return self.answer

    @staticmethod
    def get_form(*args, **kwargs):
        """Returns the form that will be used in the front-end"""
        label = kwargs.pop("label")
        help_text = kwargs.pop("help_text")

        class PostcodeForm(forms.Form):
            postcode = forms.CharField(
                label=label,
                help_text=help_text,
                validators=[validate_postcode],
            )

            def clean_postcode(self):
                postcode = validate_postcode(self.cleaned_data["postcode"])
                return postcode

        return PostcodeForm(*args, **kwargs)

    @staticmethod
    def process_form_submission(page, form):
        postcode = form.cleaned_data["postcode"]
        response = page.responses.get(postcodes__contains=[postcode])
        # We cache the postcode for formatting the response later
        response.queried_postcode = postcode
        return response

    def clean_fields(self, exclude=None):
        exclude = exclude or []
        errors = {}
        if "answer" not in exclude:
            try:
                self.answer.format(postcode="test")
            except KeyError:
                errors["answer"] = "Invalid template formatting"
        if errors:
            raise ValidationError(errors)

    def format_answer(self):
        return self.answer.format(postcode=self.queried_postcode)


class LookupPageRelatedPage(RelatedPage):
    source_page = ParentalKey("LookupPage", related_name="related_pages")


class LookupPage(BasePage):
    """A page to take an input and return one of several predefined answers.

    Don't be decieved: this does not subclass FormPage, even though it reuses several of
    the concepts.
    """

    template = "patterns/pages/forms/lookup_page.html"
    landing_page_template = "patterns/pages/forms/lookup_page_landing.html"
    base_form_class = LookupPageForm

    form_heading = RichTextField("Heading", features=RICH_TEXT_FEATURES)
    input_label = models.CharField(max_length=255)
    input_help_text = models.CharField(max_length=255)
    action_text = models.CharField(
        max_length=32, blank=True, help_text='Form action text. Defaults to "Submit".'
    )
    no_match_message = models.CharField(
        max_length=255, help_text="Message shown when an invalid input is given"
    )
    start_again_text = models.CharField(
        max_length=255, help_text="A link to reset the form and perform another lookup"
    )

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("form_heading"),
                FieldPanel("input_label"),
                FieldPanel("input_help_text"),
                FieldPanel("action_text"),
                FieldPanel("no_match_message"),
                FieldPanel("start_again_text"),
            ],
            "Form",
        ),
        InlinePanel("responses", label="Responses", min_num=1),
        InlinePanel("related_pages", label="Related pages"),
    ]

    search_fields = BasePage.search_fields + [index.SearchField("form_heading")]

    @cached_property
    def lookup_response_class(self):
        return self.responses.first()._meta.model

    def get_form(self, *args, **kwargs):
        """Get the form that is defined by the LookupResponse class, so that we can do
        type-specific validation.
        """
        form_kwargs = {"label": self.input_label, "help_text": self.input_help_text}
        form_kwargs.update(kwargs)
        return self.lookup_response_class.get_form(*args, **form_kwargs)

    def process_form_submission(self, form):
        """Defer to the LookupResponse class to process responses, so that different
        response types can be used in future.
        """
        return self.lookup_response_class.process_form_submission(self, form)

    def serve(self, request, *args, **kwargs):
        query_parameter = self.lookup_response_class.query_parameter

        if query_parameter in request.GET:  # The form was submitted
            form = self.get_form(request.GET)

            if form.is_valid():
                try:
                    lookup_response = self.process_form_submission(form)
                    return self.render_landing_page(
                        request, lookup_response, *args, **kwargs
                    )
                except self.lookup_response_class.DoesNotExist:
                    form.add_error(query_parameter, self.no_match_message)
                except self.lookup_response_class.MultipleObjectsReturned:
                    logger.error(
                        "LookupForm submission raised MultipleObjectsReturned; query: %s",
                        request.GET[query_parameter],
                    )
                    form.add_error(
                        query_parameter,
                        "Sorry, an error occured. This has been reported.",
                    )
        else:
            form = self.get_form()

        context = self.get_context(request)
        context["form"] = form
        return TemplateResponse(request, self.get_template(request), context)

    def render_landing_page(self, request, lookup_response, *args, **kwargs):
        """
        Renders the landing page.
        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        context = self.get_context(request)
        context["lookup_response"] = lookup_response
        return TemplateResponse(request, self.landing_page_template, context)
