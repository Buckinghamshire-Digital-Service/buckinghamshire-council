from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from bc.utils.constants import RICH_TEXT_FEATURES

from ..events.models import EventIndexPage
from ..news.models import NewsIndex
from ..standardpages.models import IndexPage
from ..utils.models import BasePage


class HomePage(BasePage):
    template = "patterns/pages/home/home_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    strapline = models.CharField(
        max_length=255, help_text="eg. Welcome to Buckinghamshire"
    )
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    alert_title = models.CharField(max_length=255, blank=True,)
    alert_message = RichTextField(blank=True, features=RICH_TEXT_FEATURES)

    search_fields = BasePage.search_fields + [index.SearchField("strapline")]

    content_panels = BasePage.content_panels + [
        FieldPanel("strapline"),
        ImageChooserPanel("hero_image"),
        SnippetChooserPanel("call_to_action"),
        MultiFieldPanel(
            [FieldPanel("alert_title"), FieldPanel("alert_message")],
            "Temporary alert message",
            help_text="This will only be displayed if both alert title and alert message are defined.",
        ),
    ]

    @cached_property
    def child_sections(self):
        """
        Returns queryset of this page's live, public children that are of IndexPage class
        Ordered by Wagtail explorer custom sort (ie. path)
        """
        return (
            IndexPage.objects.child_of(self)
            .filter(show_in_menus=True)
            .live()
            .public()
            .order_by("path")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        try:
            news_index = NewsIndex.objects.live().public().first()
            context["news_index"] = news_index
            context["latest_news"] = news_index.news_pages[:3]
        except AttributeError:
            # No news index, ignore
            pass

        try:
            event_index = EventIndexPage.objects.live().public().first()
            context["event_index"] = event_index
            context["latest_events"] = event_index.upcoming_events[:3]
        except AttributeError:
            # No event index, ignore
            pass

        sections = self.child_sections
        context["sections"] = sections

        return context
