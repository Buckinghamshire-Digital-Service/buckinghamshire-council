from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from wagtailorderable.modeladmin.mixins import OrderableMixin

from bc.events.models import EventType
from bc.news.models import NewsType
from bc.recruitment.models import JobCategory, JobSubcategory
from bc.search.models import Term

from .views import MissingMetadataReportView, UnpublishedChangesReportView

# from bc.people.models import PersonType


class JobSubcategoryModelAdmin(ModelAdmin):
    model = JobSubcategory
    menu_icon = "tag"
    list_display = ("title", "get_categories_list")


class JobCategoryModelAdmin(OrderableMixin, ModelAdmin):
    model = JobCategory
    menu_icon = "tag"
    list_display = (
        "title",
        "slug",
        "get_subcategories_list",
        "is_schools_and_early_years",
    )
    search_fields = ("title", "slug")


class EventTypeModelAdmin(ModelAdmin):
    model = EventType
    menu_icon = "tag"


class NewsTypeModelAdmin(ModelAdmin):
    model = NewsType
    menu_icon = "tag"


class TermModelAdmin(ModelAdmin):
    model = Term
    menu_icon = "search"
    list_display = ("canonical_term", "synonyms")


# class PersonTypeModelAdmin(ModelAdmin):
#     model = PersonType
#     menu_icon = "tag"


class TaxonomiesModelAdminGroup(ModelAdminGroup):
    menu_label = "Taxonomies"
    # items = (NewsTypeModelAdmin, EventTypeModelAdmin, PersonTypeModelAdmin)
    items = (
        TermModelAdmin,
        NewsTypeModelAdmin,
        EventTypeModelAdmin,
        JobCategoryModelAdmin,
        JobSubcategoryModelAdmin,
    )
    menu_icon = "tag"


modeladmin_register(TaxonomiesModelAdminGroup)


@hooks.register("register_reports_menu_item")
def register_unpublished_changes_report_menu_item():
    return AdminOnlyMenuItem(
        "Pages with unpublished changes",
        reverse("unpublished_changes_report"),
        classnames="icon icon-" + UnpublishedChangesReportView.header_icon,
        order=700,
    )


@hooks.register("register_admin_urls")
def register_unpublished_changes_report_url():
    return [
        path(
            "reports/unpublished-changes/",
            UnpublishedChangesReportView.as_view(),
            name="unpublished_changes_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_missing_metadata_report_menu_item():
    return AdminOnlyMenuItem(
        "Pages with missing metadata",
        reverse("missing_metadata_report"),
        classnames="icon icon-" + MissingMetadataReportView.header_icon,
        order=700,
    )


@hooks.register("register_admin_urls")
def register_missing_metadata_report_url():
    return [
        path(
            "reports/missing-metadata/",
            MissingMetadataReportView.as_view(),
            name="missing_metadata_report",
        ),
    ]


@hooks.register("insert_editor_css")
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("bc_admin_ui/editor.css")
    )
