from django import http, urls
from django.views import generic

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
