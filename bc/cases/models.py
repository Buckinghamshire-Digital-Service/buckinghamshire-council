from django import forms
from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from bs4 import BeautifulSoup

from bc.cases.backends.respond.client import get_client
from bc.cases.backends.respond.constants import CREATE_CASE_SERVICES, CREATE_CASE_TYPE
from bc.utils.constants import RICH_TEXT_FEATURES

from ..utils.models import BasePage


class ApteanRespondCaseFormPage(BasePage):

    template = "patterns/pages/cases/form_page.html"
    landing_page_template = "patterns/pages/cases/form_page_landing.html"

    web_service_definition = models.CharField(
        max_length=255,
        help_text="The name of the CreateCase web service to use.",
        choices=[(s, s) for s in CREATE_CASE_SERVICES],
    )

    introduction = models.TextField(blank=True)
    pre_submission_text = RichTextField(
        blank=True,
        help_text="Text displayed after the form, above the submit button",
        features=RICH_TEXT_FEATURES,
        verbose_name="pre-submission text",
    )

    completion_title = models.CharField(
        max_length=255,
        help_text="Heading for the page show after successful form submission.",
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
        FieldPanel(
            "web_service_definition", widget=forms.Select(choices=CREATE_CASE_SERVICES)
        ),
        FieldPanel("introduction"),
        FieldPanel("pre_submission_text"),
        FieldPanel("action_text"),
        MultiFieldPanel(
            [FieldPanel("completion_title"), FieldPanel("completion_content")],
            "Confirmation page",
        ),
    ]

    def get_form_class(self):
        return get_client().services[CREATE_CASE_TYPE][self.web_service_definition]

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        return form_class(*args, **kwargs)

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.get_form(
                request.POST, request.FILES  # , page=self, user=request.user
            )

            if form.is_valid():
                form, case_details = self.process_form_submission(form)
                if form.is_valid():  # still
                    return self.render_landing_page(
                        request, case_details, *args, **kwargs
                    )
        else:
            form = self.get_form()

        context = self.get_context(request)
        context["form"] = form
        return render(request, self.get_template(request), context)

    def process_form_submission(self, form):
        case_xml = form.get_xml_string()
        client = get_client()
        response = client.create_case(self.web_service_definition, case_xml)
        soup = BeautifulSoup(response.content, "xml")
        if response.status_code != 200:
            for error in soup.find_all('failure'):
                form.add_error(error.attrs['schemaName'], error.text)
            return form, None
        else:
            case = soup.find('case')
            return form, case.attrs

    def get_landing_page_template(self, request, *args, **kwargs):
        return self.landing_page_template

    def render_landing_page(self, request, case_details=None, *args, **kwargs):
        """
        Renders the landing page.
        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        context = self.get_context(request)
        context["case_details"] = case_details
        return render(request, self.get_landing_page_template(request), context)
