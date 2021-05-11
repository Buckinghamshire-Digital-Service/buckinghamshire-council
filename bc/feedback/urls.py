from django.urls import path

from bc.feedback.views import FeedbackThankYouView, UsefulnessFeedbackCreateView

app_name = "feedback"

urlpatterns = [
    path(
        "create/",
        UsefulnessFeedbackCreateView.as_view(),
        name="create_usefulness_feedback",
    ),
    path("thank-you/", FeedbackThankYouView.as_view(), name="thank_you")
]
