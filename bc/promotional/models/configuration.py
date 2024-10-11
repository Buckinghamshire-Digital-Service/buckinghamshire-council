from django import http
from django.db import models
from django.utils.html import format_html

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class PrimaryNavigationItem(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title",
        required=False,
        max_length=64,
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
    )
    primary_cta_link_text = models.CharField(
        max_length=128, blank=True, verbose_name="primary CTA link text"
    )
    primary_cta_link_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="primary CTA link page",
    )
    events_feed = models.ForeignKey(
        "events.EventIndexPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Select the events feed page to fetch events from on this site",
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
        MultiFieldPanel(
            (
                FieldPanel("primary_cta_link_text"),
                FieldPanel("primary_cta_link_page"),
            ),
            heading="Primary Call to Action",
        ),
        FieldPanel("events_feed"),
    ]

    def serve(self, request, *args, **kwargs):
        raise http.Http404("Headless page")
