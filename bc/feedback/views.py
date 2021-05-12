from http import HTTPStatus

from django import http, urls
from django.views import generic

from wagtail.admin.views import reports as report_views

from bc.feedback.forms import FeedbackCommentForm, UsefulnessFeedbackForm
from bc.feedback.models import FeedbackComment, UsefulnessFeedback


class UsefulnessFeedbackCreateView(generic.CreateView):
    """
    Create UsefulnessFeedback from form submission.

    The forms are pre-populated with either positive or negative feedback. The user
    only submits one of the two forms displayed.

    The current implementation still contains a success redirect. This allows these
    feedback forms to be directly submitted without the need to be handled through JS.
    This follows the idea of progressive enhancement.

    """

    model = UsefulnessFeedback
    form_class = UsefulnessFeedbackForm
    http_method_names = ["post"]

    def form_invalid(self, form):
        return http.HttpResponseBadRequest()

    def get_success_url(self):
        return urls.reverse("feedback:thank_you")


class FeedbackThankYouView(generic.TemplateView):
    template_name = "patterns/pages/feedback/thank-you.html"


class UsefulnessFeedbackReportView(report_views.ReportView):
    title = "Usefulness feedback"
    header_icon = "help"
    template_name = "patterns/pages/reports/usefulness_feedback_report.html"
    list_export = ["created", "page.title", "useful"]
    export_headings = {
        "page.title": "Page"
    }

    def get_queryset(self):
        return UsefulnessFeedback.objects.all().order_by("-created")


class FeedbackCommentCreateView(generic.CreateView):
    model = FeedbackComment
    form_class = FeedbackCommentForm
    http_method_names = ["post"]

    def form_valid(self, form):
        form.save()
        return http.JsonResponse(data={}, status=HTTPStatus.OK)
