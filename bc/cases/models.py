from django.db import models
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.cache import never_cache

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
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
from bc.cases.blocks import CaseFormStoryBlock
from bc.cases.utils import get_case_reference
from bc.utils.constants import RICH_TEXT_FEATURES
from bc.utils.models import BasePage, RelatedPage

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


class ApteanRespondCaseFormPageRelatedPage(RelatedPage):
    source_page = ParentalKey("ApteanRespondCaseFormPage", related_name="related_pages")


@method_decorator(never_cache, name="serve")
class ApteanRespondCaseFormPage(RoutablePageMixin, BasePage):
    """A form page using forms integrated with the Aptean Respond case management API.

    This uses routes to show an information page and a form page. After a successful
    form submission, the view redirects to the index route, but uses session data to
    show a 'thank you' message.
    """

    template = "patterns/pages/cases/form_page_initial.html"
    form_page_template = "patterns/pages/cases/form_page.html"
    landing_page_template = "patterns/pages/cases/form_page_landing.html"

    form = models.CharField(max_length=255, choices=APTEAN_FORM_CHOICES)

    body = StreamField(
        CaseFormStoryBlock(block_counts={"form_link_button": {"min_num": 1}})
    )

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

    search_fields = BasePage.search_fields + [
        index.SearchField("body"),
        index.SearchField("introduction"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                StreamFieldPanel("body"),
                InlinePanel("related_pages", label="Related pages"),
            ],
            "Intro page",
        ),
        MultiFieldPanel(
            [
                FieldPanel("form"),
                FieldPanel("introduction"),
                FieldPanel("pre_submission_text"),
                FieldPanel("action_text"),
            ],
            "Form page",
        ),
        MultiFieldPanel(
            [FieldPanel("completion_title"), FieldPanel("completion_content")],
            "Confirmation page",
        ),
    ]

    @cached_property
    def live_related_pages(self):
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]

    def get_form_class(self):
        return APTEAN_FORM_MAPPING[self.form]

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        return form_class(*args, **kwargs)

    def get_case_reference_session_key(self):
        return f"case_reference-{self.pk}"

    def get_landing_page_session_key(self):
        return f"landing_page-{self.pk}"

    @route(r"^$")
    def index_route(self, request, *args, **kwargs):
        context = self.get_context(request)
        if request.session.pop(self.get_landing_page_session_key(), False):
            context["case_reference"] = request.session.pop(
                self.get_case_reference_session_key(), None
            )
            return render(request, self.landing_page_template, context)
        return super().index_route(request, *args, **kwargs)

    @route(r"^form/$")
    def form_route(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                form = self.get_form(request.POST, request.FILES)

                if form.is_valid():
                    form, case_reference = self.process_form_submission(form)
                    if form.is_valid():  # still
                        # store the case_reference in the session for the thank you page
                        request.session[
                            self.get_case_reference_session_key()
                        ] = case_reference
                        request.session[self.get_landing_page_session_key()] = True
                        return redirect(self.url, permanent=False)
            else:
                form = self.get_form()
        except RespondClientException:
            form = None

        context = self.get_context(request)
        context["form"] = form
        context["form_template"] = form.template_name
        return render(request, self.form_page_template, context)

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
            case_reference = get_case_reference(soup)
            return form, case_reference
