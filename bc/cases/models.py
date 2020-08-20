from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from bs4 import BeautifulSoup

from bc.cases.backends.respond.client import RespondClientException, get_client
from bc.cases.backends.respond.constants import (
    APTEAN_FORM_CHOICES,
    APTEAN_FORM_COMMENT,
    APTEAN_FORM_COMPLAINT,
    APTEAN_FORM_COMPLIMENT,
    APTEAN_FORM_DISCLOSURE,
    APTEAN_FORM_FOI,
    APTEAN_FORM_SAR,
    ATTACHMENT_FAILURE_ERROR,
    ATTACHMENT_SCHEMA_NAME,
)
from bc.cases.utils import format_case_reference
from bc.utils.constants import RICH_TEXT_FEATURES

from ..utils.models import BasePage
from .forms import (
    CommentForm,
    ComplaintForm,
    ComplimentForm,
    DisclosureForm,
    FOIForm,
    SARForm,
)

APTEAN_FORM_MAPPING = {
    APTEAN_FORM_COMPLAINT: ComplaintForm,
    APTEAN_FORM_FOI: FOIForm,
    APTEAN_FORM_SAR: SARForm,
    APTEAN_FORM_COMMENT: CommentForm,
    APTEAN_FORM_COMPLIMENT: ComplimentForm,
    APTEAN_FORM_DISCLOSURE: DisclosureForm,
}


@method_decorator(never_cache, name="serve")
class ApteanRespondCaseFormPage(BasePage):

    template = "patterns/pages/cases/form_page.html"
    landing_page_template = "patterns/pages/cases/form_page_landing.html"

    form = models.CharField(max_length=255, choices=APTEAN_FORM_CHOICES)

    introduction = RichTextField(
        blank=True,
        help_text="Text displayed before the form",
        features=RICH_TEXT_FEATURES,
    )
    pre_submission_text = RichTextField(
        blank=True,
        help_text="Text displayed after the form, above the submit button",
        features=RICH_TEXT_FEATURES,
        verbose_name="pre-submission text",
    )

    completion_title = models.CharField(
        max_length=255,
        help_text="Heading for the page shown after successful form submission.",
    )
    completion_content = RichTextField(
        blank=True,
        help_text="Text displayed to the user on successful submission of the form",
        features=RICH_TEXT_FEATURES,
    )
    action_text = models.CharField(
        max_length=32,
        blank=True,
        help_text='Form action button text. Defaults to "Submit"',
    )

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    content_panels = BasePage.content_panels + [
        FieldPanel("form"),
        FieldPanel("introduction"),
        FieldPanel("pre_submission_text"),
        FieldPanel("action_text"),
        MultiFieldPanel(
            [FieldPanel("completion_title"), FieldPanel("completion_content")],
            "Confirmation page",
        ),
    ]

    def get_form_class(self):
        return APTEAN_FORM_MAPPING[self.form]

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        return form_class(*args, **kwargs)

    def serve(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                form = self.get_form(request.POST, request.FILES)

                if form.is_valid():
                    form, case_reference = self.process_form_submission(form)
                    if form.is_valid():  # still
                        return self.render_landing_page(
                            request, case_reference, *args, **kwargs
                        )
            else:
                form = self.get_form()
        except RespondClientException:
            form = None

        context = self.get_context(request)
        context["form"] = form
        context["form_template"] = form.template_name
        return render(request, self.get_template(request), context)

    def process_form_submission(self, form):
        case_xml = form.get_xml_string()
        client = get_client()
        response = client.create_case(form.webservice, case_xml)
        soup = BeautifulSoup(response.content, "xml")
        if response.status_code != 200:
            reverse_schema_mapping = {
                v: k for k, v in form.field_schema_name_mapping.items()
            }
            for error in soup.find_all("failure"):
                if (
                    "schemaName" in error.attrs
                    and error.attrs["schemaName"] in reverse_schema_mapping
                ):
                    form.add_error(
                        reverse_schema_mapping[error.attrs["schemaName"]], error.text
                    )
                elif (
                    "type" in error.attrs
                    and error.attrs["type"] == ATTACHMENT_FAILURE_ERROR
                ):
                    form.add_error(ATTACHMENT_SCHEMA_NAME, error.text)
                else:
                    form.add_error(None, error.text)
            return form, None
        else:
            case_reference = format_case_reference(soup.find("case").attrs["Name"])
            return form, case_reference

    def get_landing_page_template(self, request, *args, **kwargs):
        return self.landing_page_template

    def render_landing_page(self, request, case_reference=None, *args, **kwargs):
        """
        Renders the landing page.
        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        context = self.get_context(request)
        context["case_reference"] = case_reference
        return render(request, self.get_landing_page_template(request), context)
