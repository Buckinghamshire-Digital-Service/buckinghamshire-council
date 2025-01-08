from http import HTTPStatus

from django import http, urls
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from wagtail.admin.views import reports as report_views

from bc.feedback.filters import FeedbackCommentFilterSet, UsefulnessFeedbackFilterSet
from bc.feedback.forms import FeedbackCommentForm, UsefulnessFeedbackForm
from bc.feedback.models import FeedbackComment, UsefulnessFeedback


@method_decorator(csrf_exempt, name="dispatch")
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

    def post(self, request, *args, **kwargs):
        """Set the form prefix based on the submitted data

        To avoid duplicate HTML element IDs on the page, we prefix the forms. Both the
        'yes' and 'no' form are POSTed to this view, but the data includes the form
        prefix. Without matching the prefix to the submitted data, no form will be
        valid.
        """
        self.prefix = request.POST.get("form_prefix")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Denormalise the URL, lest the page be deleted or moved.
        self.object.original_url = self.object.page.url[:2048]
        self.object.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return http.HttpResponseBadRequest()

    def get_success_url(self):
        return urls.reverse("feedback:thank_you")


class FeedbackThankYouView(generic.TemplateView):
    template_name = "patterns/pages/feedback/thank-you.html"


class UsefulnessFeedbackReportView(report_views.ReportView):
    page_title = "Usefulness feedback"
    index_url_name = "usefuleness_feedback_report"
    index_results_url_name = "usefuleness_feedback_report_results"
    header_icon = "help"
    results_template_name = (
        "patterns/pages/reports/usefulness_feedback_report_results.html"
    )
    list_export = ["created", "get_title", "get_current_url", "original_url", "useful"]
    export_headings = {
        "get_title": "Page",
        "get_current_url": "URL",
        "original_url": "Original URL",
    }
    filterset_class = UsefulnessFeedbackFilterSet

    def get_queryset(self):
        queryset = UsefulnessFeedback.objects.all().order_by("-created")

        # Apply the filterset
        filterset = self.filterset_class(data=self.request.GET, queryset=queryset)
        queryset = filterset.qs

        return queryset


@method_decorator(csrf_exempt, name="dispatch")
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
    prefix = "comment_form"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Denormalise the URL, lest the page be deleted or moved.
        self.object.original_url = self.object.page.url[:2048]
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
    page_title = "Feedback comments"
    index_url_name = "feedback_comment_report"
    index_results_url_name = "feedback_comment_report_results"
    header_icon = "edit"
    results_template_name = (
        "patterns/pages/reports/feedback_comment_report_results.html"
    )
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

    filterset_class = FeedbackCommentFilterSet

    def get_queryset(self):
        queryset = FeedbackComment.objects.all().order_by("-created")

        # Apply the filterset
        filterset = self.filterset_class(data=self.request.GET, queryset=queryset)
        queryset = filterset.qs

        return queryset
