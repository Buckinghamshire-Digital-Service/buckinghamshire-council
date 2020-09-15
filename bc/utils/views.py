from django.db.models import Q
from django.views import defaults

from wagtail.admin.views.reports import PageReportView
from wagtail.core.models import Page

from .models import SEARCH_DESCRIPTION_LABEL, SEO_TITLE_LABEL


def page_not_found(request, exception, template_name="patterns/pages/errors/404.html"):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name="patterns/pages/errors/500.html"):
    return defaults.server_error(request, template_name)


class UnpublishedChangesReportView(PageReportView):

    header_icon = "doc-empty-inverse"
    template_name = "patterns/pages/reports/unpublished_changes_report.html"
    title = "Pages with unpublished changes"

    list_export = PageReportView.list_export + ["last_published_at"]
    export_headings = dict(
        last_published_at="Last Published", **PageReportView.export_headings
    )

    def get_queryset(self):
        return Page.objects.filter(has_unpublished_changes=True)


class MissingMetadataReportView(PageReportView):

    header_icon = "search"
    template_name = "patterns/pages/reports/missing_metadata_report.html"
    title = "Pages missing SEO metadata"

    list_export = PageReportView.list_export + ["seo_title", "search_description"]
    export_headings = dict(
        seo_title=SEO_TITLE_LABEL,
        search_description=SEARCH_DESCRIPTION_LABEL,
        **PageReportView.export_headings
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "seo_title_label": SEO_TITLE_LABEL,
                "search_description_label": SEARCH_DESCRIPTION_LABEL,
            }
        )
        return context

    def get_queryset(self):
        return Page.objects.exclude(depth=1).filter(
            Q(seo_title="") | Q(search_description="")
        )
