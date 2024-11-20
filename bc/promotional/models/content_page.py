from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from bc.utils import blocks
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
    hero_link = StreamField(
        blocks.LinkBlock,
        blank=True,
        max_num=1,
    )

    body = StreamField(PromotionalStoryBlock())

    search_fields = BasePage.search_fields + [index.SearchField("body")]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            (
                FieldPanel("hero_title"),
                FieldPanel("hero_text"),
                FieldPanel("hero_image"),
                FieldPanel("hero_link"),
            ),
            heading="Hero",
        ),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        link_block = self.hero_link[0] if self.hero_link else None
        if not link_block:
            context.update({"hero_link": None})
        elif link_block.block_type == "internal_link":
            page = link_block.value.get("page")
            # Ensure page exists and is live.
            if page and page.live:
                context.update({"hero_link": link_block.value})
        elif link_block.block_type == "external_link":
            context.update({"hero_link": link_block.value})

        return context
