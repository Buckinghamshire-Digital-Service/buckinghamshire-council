from django import http, urls
from django.views import generic

from wagtail.admin.views import reports as report_views

from bc.feedback.forms import UsefulnessFeedbackForm
from bc.feedback.models import UsefulnessFeedback


class UsefulnessFeedbackCreateView(generic.CreateView):
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

    def get_queryset(self):
        return UsefulnessFeedback.objects.all().order_by("-created")
