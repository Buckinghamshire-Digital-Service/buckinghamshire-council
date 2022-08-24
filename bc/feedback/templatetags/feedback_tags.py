from django import template
from django.conf import settings

from wagtail.models import Page

from bc.feedback.forms import FeedbackCommentForm, UsefulnessFeedbackForm

register = template.Library()


@register.inclusion_tag(
    "patterns/molecules/feedback-widget/feedback-widget.html", takes_context=True
)
def feedback_widget(context):
    page = context.get("page")
    extra_context = {}

    if (
        settings.ENABLE_FEEDBACK_WIDGET
        and page
        and isinstance(page, Page)  # needed for pattern library compatibility only
    ):
        extra_context["yes_form"] = UsefulnessFeedbackForm(
            prefix="yes", initial={"useful": True, "page": page}
        )
        extra_context["no_form"] = UsefulnessFeedbackForm(
            prefix="no", initial={"useful": False, "page": page}
        )
        extra_context["comment_form"] = FeedbackCommentForm(
            prefix="comment_form", initial={"page": page}
        )
        extra_context["site_name"] = page.get_site().site_name

    return extra_context
