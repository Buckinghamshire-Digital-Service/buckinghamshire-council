from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField

from bc.utils.models import BasePage

from ..blocks.cards import LinkCards


class PromotionalHomePage(BasePage):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "promotional.PromotionalSiteConfiguration",
        "promotional.PromotionalContentPage",
    ]
    template = "patterns/pages/promotional/home_page.html"

    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField(max_length=1024, blank=True)
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    hero_link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    hero_link_text = models.CharField(max_length=255)

    teasers = StreamField(
        [
            ("link_cards", LinkCards()),
        ],
        max_num=1,
        blank=True,
    )

    search_fields = BasePage.search_fields.copy()
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
        FieldPanel("teasers"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.hero_link_page is not None:
            context["hero_link_url"] = self.hero_link_page.get_url(request=request)
        return context
