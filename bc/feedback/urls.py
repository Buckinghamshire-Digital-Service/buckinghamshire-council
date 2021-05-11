from django.urls import path

from bc.feedback.views import (
    FeedbackCommentCreateView,
    FeedbackThankYouView,
    UsefulnessFeedbackCreateView,
)

app_name = "feedback"

urlpatterns = [
    path(
        "submit-usefulness-feedback/",
        UsefulnessFeedbackCreateView.as_view(),
        name="create_usefulness_feedback",
    ),
    path(
        "submit-comment/",
        FeedbackCommentCreateView.as_view(),
        name="feedback_comment_create",
    ),
    path("thank-you/", FeedbackThankYouView.as_view(), name="thank_you"),
]
