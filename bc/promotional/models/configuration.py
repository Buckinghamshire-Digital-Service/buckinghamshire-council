from django import http
from django.utils.html import format_html

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class PrimaryNavigationItem(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title", required=False
    )
    populate_child_pages = blocks.BooleanBlock(
        required=False,
        help='Auto-populated pages with "Show in menus" selected in their "Promote" tab',
    )


class PromotionalSiteConfiguration(Page):
    parent_page_types = ("promotional.PromotionalHomePage",)
    subpage_types = ()
    preview_modes = ()

    max_count_per_parent = 1

    primary_navigation = StreamField(
        [("primary_navigation_item", PrimaryNavigationItem())],
        help_text="Primary navigation items",
    )

    content_panels = [
        HelpPanel(
            format_html(
                "<p>{}</p><p>{}</p>",
                "In order to apply those site configuration changes, please publish this page.",
                "Saving this page as draft will not have any effect.",
            )
        ),
        FieldPanel("title"),
        FieldPanel("primary_navigation"),
    ]

    def serve(self, request, *args, **kwargs):
        raise http.Http404("Headless page")