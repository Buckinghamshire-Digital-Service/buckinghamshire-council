import logging

from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.contrib.forms.models import FormSubmission as WagtailFormSubmission
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.search import index

from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
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


class CustomFormBuilder(WagtailCaptchaFormBuilder):
    # create a function that returns an instanced Django form field
    # function name must match create_<field_type_key>_field
    def create_checkbox_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        return forms.BooleanField(widget=CustomCheckboxSelectSingle, **options)

    def create_checkboxes_field(self, field, options):
        # Based on code in wagtail.contrib.forms, but changing widget
        options["choices"] = self.get_formatted_field_choices(field)
        options["initial"] = self.get_formatted_field_initial(field)
        return forms.MultipleChoiceField(widget=CustomCheckboxSelectMultiple, **options)


class FormPage(WagtailCaptchaEmailForm, BasePage):
    """A page with editorially controlled forms for anonymous users.

    We use custom CSRF middleware to exempt form pages from CSRF token checks.
    Maintain this in bc.utils.middleware.
    """

    class AUTO_DELETE(models.IntegerChoices):
        NO_DELETE = 0, "Don't delete submissions"
        WEEK = 7, "One week"
        MONTH = 30, "One month"
        QUARTER = 90, "Three months"

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

    auto_delete = models.PositiveIntegerField(
        choices=AUTO_DELETE.choices,
        default=AUTO_DELETE.NO_DELETE,
        help_text="Delete submissions automatically after this amount of time",
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
        FieldPanel("auto_delete"),
    ]

    form_builder = CustomFormBuilder


class FormSubmissionQuerySet(models.QuerySet):
    def with_delete_after(self):
        """
        Adds a `delete_after` annotation on the queryset which corresponds to
        the date after which the form submission should be deleted. If the
        submission should not be auto-deleted, the value will be NULL.
        """
        # Using page__formpage allows joining the FormSubmission with the
        # corresponding FormPage (whereas `page` would join with the base Page
        # model which doesn't have an `auto_delete` field).
        cutoff_date = models.ExpressionWrapper(
            # With postgres, adding a Date to an integer is equivalent to adding
            # that number of days to the date.
            models.F("submit_time__date") + models.F("page__formpage__auto_delete"),
            output_field=models.DateField(),
        )
        expr = models.Case(
            models.When(page__formpage__auto_delete__gt=0, then=cutoff_date)
        )
        return self.annotate(delete_after=expr)

    def stale(self):
        """
        Return all submissions that should be deleted as of today.
        """
        queryset = self.with_delete_after()
        return queryset.exclude(delete_after__isnull=True).filter(
            delete_after__lt=timezone.localdate()
        )


class FormSubmission(WagtailFormSubmission):
    objects = FormSubmissionQuerySet.as_manager()

    class Meta:
        proxy = True


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
        FieldPanel("link_page"),
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
    subpage_types = [
        "standardpages.informationpage",
        "inlineindex.inlineindex",
        "location.locationindexpage",
        "longform.longformpage",
        "step_by_step.stepbysteppage",
    ]

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


@register_setting
class FormSubmissionAccessControl(BaseGenericSetting):
    groups_with_access = models.ManyToManyField(
        "auth.Group",
        help_text="The group(s) that can see form submissions",
    )

    panels = [FieldPanel("groups_with_access", widget=forms.CheckboxSelectMultiple())]

    class Meta:
        verbose_name = "Form submission access control"
