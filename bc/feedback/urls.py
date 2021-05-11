from django.urls import path

from bc.feedback.views import UsefulnessFeedbackCreateView

app_name = "feedback"

urlpatterns = [
    path(
        "create/",
        UsefulnessFeedbackCreateView.as_view(),
        name="create_usefulness_feedback",
    )
]
