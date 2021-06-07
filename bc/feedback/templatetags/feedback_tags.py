from django import template

from bc.feedback.forms import FeedbackCommentForm, UsefulnessFeedbackForm

register = template.Library()


@register.inclusion_tag(
    "patterns/molecules/feedback-widget/feedback-widget.html", takes_context=True
)
def feedback_widget(context):
    page = context.get("page")
    extra_context = {}

    if page:
        extra_context["yes_form"] = UsefulnessFeedbackForm(
            initial={"useful": True, "page": page}
        )
        extra_context["no_form"] = UsefulnessFeedbackForm(
            initial={"useful": False, "page": page}
        )
        extra_context["comment_form"] = FeedbackCommentForm(initial={"page": page})
        extra_context["site_name"] = page.get_site().site_name

    return extra_context
