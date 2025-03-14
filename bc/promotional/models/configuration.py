from django import http
from django.db import models
from django.utils.cache import add_never_cache_headers
from django.utils.html import format_html

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page, Site


class PrimaryNavigationSubItem(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        required=False,
        max_length=64,
        help_text="If left blank, the page title will be used",
    )


class PrimaryNavigationSection(blocks.StructBlock):
    """
    Top-level navigation section that has no link but it's a collection
    of child pages.
    """

    title = blocks.CharBlock(
        required=False,
        max_length=64,
    )
    items = blocks.ListBlock(PrimaryNavigationSubItem)


class PrimaryNavigationItem(blocks.StructBlock):
    """
    Top-level navigation item without child pages.
    """

    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        max_length=64,
        help_text="If left blank, the page title will be used",
        required=False,
    )


class PromotionalSiteConfiguration(Page):
    parent_page_types = ("promotional.PromotionalHomePage",)
    subpage_types = ()
    preview_modes = ()

    max_count_per_parent = 1

    primary_navigation = StreamField(
        [
            ("primary_navigation_item", PrimaryNavigationItem()),
            ("primary_navigation_section", PrimaryNavigationSection()),
        ]
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
        """
        We want to redirect the editors clicking live in Wagtail admin to the homepage,
        instead of showing them 404.
        """
        site = Site.find_for_request(request)
        if site is None or site.root_page is None:
            raise http.Http404()

        response = http.HttpResponseRedirect(
            site.root_page.specific.get_url(request=request)
        )

        # Make sure redirect is not cached or indexed.
        del response["cache-control"]
        add_never_cache_headers(response)
        response["X-Robots-Tag"] = "noindex"

        return response

    def get_sitemap_urls(self, request=None):
        # We don't want this page in the sitemap.
        return []
