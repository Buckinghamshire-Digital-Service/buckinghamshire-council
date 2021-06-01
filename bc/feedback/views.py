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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Denormalise the URL, lest the page be deleted or moved.
        self.object.original_url = self.object.page.url
        self.object.save()
        return http.HttpResponseRedirect(self.get_success_url())

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
    list_export = ["created", "get_title", "get_current_url", "original_url", "useful"]
    export_headings = {
        "get_title": "Page",
        "get_current_url": "URL",
        "original_url": "Original URL",
    }

    def get_queryset(self):
        return UsefulnessFeedback.objects.all().order_by("-created")


class FeedbackCommentCreateView(generic.CreateView):
    """
    Create FeedbackComment from posted forms.

    The forms is not visible by default and only revealed through a previous action
    (i.e. submitting a negative UsefulnessFeedbackForm). A redirect to a thank you page
    is not necessary, as the thank you message is meant to be displayed through JS.

    Progressive enhancement is not possible as simply as in the usefulness feedback
    case. That is because the form is only supposed to be revealed through JS.

    Because of the above, JsonResponse objects are used to respond to form submissions.

    """

    model = FeedbackComment
    form_class = FeedbackCommentForm
    http_method_names = ["post"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Denormalise the URL, lest the page be deleted or moved.
        self.object.original_url = self.object.page.url
        self.object.save()
        return http.JsonResponse(data={}, status=HTTPStatus.OK)

    def form_invalid(self, form):
        data = {
            "form": {
                "data": dict(form.data),
                "errors": dict(form.errors),
                "non_field_errors": form.non_field_errors(),
            }
        }
        return http.JsonResponse(data=data, status=HTTPStatus.BAD_REQUEST)


class FeedbackCommentReportView(report_views.ReportView):
    title = "Feedback comments"
    header_icon = "edit"
    template_name = "patterns/pages/reports/feedback_comment_report.html"
    list_export = [
        "created",
        "get_title",
        "get_current_url",
        "original_url",
        "action",
        "issue",
    ]
    export_headings = {
        "get_title": "Page",
        "get_current_url": "URL",
        "original_url": "Original URL",
    }

    def get_queryset(self):
        return FeedbackComment.objects.all().order_by("-created")
