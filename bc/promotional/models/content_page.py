from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from bc.utils.models import BasePage

from ..blocks.definition import PromotionalStoryBlock


class PromotionalContentPage(BasePage):
    parent_page_types = [
        "promotional.PromotionalHomePage",
        "promotional.PromotionalContentPage",
    ]
    subpage_types = ["promotional.PromotionalContentPage"]

    template = "patterns/pages/promotional/content_page.html"

    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField(max_length=1024, blank=True)
    hero_image = models.ForeignKey(
        "images.CustomImage",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    hero_link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    hero_link_text = models.CharField(max_length=255)

    body = StreamField(PromotionalStoryBlock())

    search_fields = BasePage.search_fields + [index.SearchField("body")]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            (
                FieldPanel("hero_title"),
                FieldPanel("hero_text"),
                FieldPanel("hero_image"),
                FieldPanel("hero_link_page"),
                FieldPanel("hero_link_text"),
            ),
            heading="Hero",
        ),
        FieldPanel("body"),
    ]
