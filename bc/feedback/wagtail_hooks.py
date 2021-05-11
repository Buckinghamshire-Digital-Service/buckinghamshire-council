from django import urls

from wagtail.admin import menu
from wagtail.core import hooks

from bc.feedback.views import UsefulnessFeedbackReportView


@hooks.register("register_reports_menu_item")
def register_usefulness_feedback_report_menu_item():
    return menu.MenuItem(
        UsefulnessFeedbackReportView.title,
        urls.reverse("usefuleness_feedback_report"),
        classnames='icon icon-' + UsefulnessFeedbackReportView.header_icon,
        order=300,
    )


@hooks.register('register_admin_urls')
def register_usefulness_feedback_report_url():
    return [
        urls.path(
            'reports/usefulness-feedback/',
            UsefulnessFeedbackReportView.as_view(),
            name="usefuleness_feedback_report"
        ),
    ]
