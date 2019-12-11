from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from bc.utils.models import BasePage


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

    search_fields = BasePage.search_fields + [index.SearchField("strapline")]

    content_panels = BasePage.content_panels + [
        FieldPanel("strapline"),
        ImageChooserPanel("hero_image"),
        SnippetChooserPanel("call_to_action"),
    ]
