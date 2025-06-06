from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail.admin.rich_text.editors.draftail import features as draftail_features

from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
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
        "icon",
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
        icon_name=UnpublishedChangesReportView.header_icon,
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
        # Results-only view to add support for AJAX-based filtering
        path(
            "reports/unpublished-changes/results/",
            UnpublishedChangesReportView.as_view(results_only=True),
            name="unpublished_changes_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_missing_metadata_report_menu_item():
    return AdminOnlyMenuItem(
        "Pages with missing metadata",
        reverse("missing_metadata_report"),
        icon_name=MissingMetadataReportView.header_icon,
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
        # Results-only view to add support for AJAX-based filtering
        path(
            "reports/missing-metadata/results/",
            MissingMetadataReportView.as_view(results_only=True),
            name="missing_metadata_report_results",
        ),
    ]


@hooks.register("register_rich_text_features")
def register_big_text_feature(features):
    """
    Registering the `big-text` Draftail feature, which adds a paragraph around the
    selected text with its classs set to `big-text`.
    """
    feature_name = "big-text"
    type_ = "big-text"

    control = {
        "type": type_,
        "label": "BT",
        "description": "Big Text",
        "element": "p",
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(control),
    )
    db_conversion = {
        "from_database_format": {"p[class=big-text]": BlockElementHandler(type_)},
        "to_database_format": {
            "block_map": {type_: {"element": "p", "props": {"class": "big-text"}}},
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)


@hooks.register("insert_editor_js")
def editor_js():
    return mark_safe(
        '<script type="text/javascript" src="%s"></script>'
        % static("utils/js/table-with-links.js")
    )


@hooks.register("insert_global_admin_css")
def editor_css():
    return mark_safe(
        '<link rel="stylesheet" type="text/css" href="%s">'
        % static("utils/css/typedtable.css")
    )
