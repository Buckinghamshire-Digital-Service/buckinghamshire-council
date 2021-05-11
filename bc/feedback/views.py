from django.views import generic

from bc.feedback.forms import UsefulnessFeedbackForm
from bc.feedback.models import UsefulnessFeedback


class UsefulnessFeedbackCreateView(generic.CreateView):
    model = UsefulnessFeedback
    form_class = UsefulnessFeedbackForm
    http_method_names = ["post"]
