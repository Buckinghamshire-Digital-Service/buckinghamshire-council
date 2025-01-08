from django import urls

from wagtail import hooks
from wagtail.admin import menu

from bc.feedback.views import FeedbackCommentReportView, UsefulnessFeedbackReportView


@hooks.register("register_reports_menu_item")
def register_usefulness_feedback_report_menu_item():
    return menu.MenuItem(
        UsefulnessFeedbackReportView.page_title,
        urls.reverse("usefuleness_feedback_report"),
        icon_name=UsefulnessFeedbackReportView.header_icon,
        order=300,
    )


@hooks.register("register_admin_urls")
def register_usefulness_feedback_report_url():
    return [
        urls.path(
            "reports/usefulness-feedback/",
            UsefulnessFeedbackReportView.as_view(),
            name="usefuleness_feedback_report",
        ),
        # Results-only view to add support for AJAX-based filtering
        urls.path(
            "reports/usefulness-feedback/results/",
            UsefulnessFeedbackReportView.as_view(results_only=True),
            name="usefuleness_feedback_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_feedback_comment_report_menu_item():
    return menu.MenuItem(
        FeedbackCommentReportView.page_title,
        urls.reverse("feedback_comment_report"),
        icon_name=FeedbackCommentReportView.header_icon,
        order=400,
    )


@hooks.register("register_admin_urls")
def register_feedback_comment_report_url():
    return [
        urls.path(
            "reports/feedback-comments/",
            FeedbackCommentReportView.as_view(),
            name="feedback_comment_report",
        ),
        # Results-only view to add support for AJAX-based filtering
        urls.path(
            "reports/feedback-comments/results/",
            FeedbackCommentReportView.as_view(results_only=True),
            name="feedback_comment_report_results",
        ),
    ]
