from django.db.models import Q
from django.views import defaults

from wagtail.admin.auth import permission_denied
from wagtail.admin.views.pages.listing import ExplorablePageFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page

from .models import SEARCH_DESCRIPTION_LABEL, SEO_TITLE_LABEL


def page_not_found(request, exception, template_name="patterns/pages/errors/404.html"):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name="patterns/pages/errors/500.html"):
    return defaults.server_error(request, template_name)


class UnpublishedChangesReportView(PageReportView):

    header_icon = "doc-empty-inverse"
    results_template_name = (
        "patterns/pages/reports/unpublished_changes_report_results.html"
    )
    page_title = "Pages with unpublished changes"
    index_url_name = "unpublished_changes_report"
    index_results_url_name = "unpublished_changes_report_results"
    filterset_class = ExplorablePageFilterSet

    list_export = PageReportView.list_export + ["last_published_at"]
    export_headings = dict(
        last_published_at="Last Published", **PageReportView.export_headings
    )

    def get_queryset(self):
        return Page.objects.filter(has_unpublished_changes=True)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)


class MissingMetadataReportView(PageReportView):

    header_icon = "search"
    results_template_name = (
        "patterns/pages/reports/missing_metadata_report_results.html"
    )
    page_title = "Pages missing SEO metadata"
    index_url_name = "missing_metadata_report"
    index_results_url_name = "missing_metadata_report_results"
    filterset_class = ExplorablePageFilterSet

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)
