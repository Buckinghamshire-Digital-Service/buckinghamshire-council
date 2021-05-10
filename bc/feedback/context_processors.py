from bc.feedback.forms import UsefulnessFeedbackForm


def feedback_forms(request):
    return {"usefulness_feedback_form": UsefulnessFeedbackForm()}
