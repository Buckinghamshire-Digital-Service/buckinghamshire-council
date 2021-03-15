from django.db import models

from wagtail.admin import edit_handlers
from wagtail.core import fields
from wagtail.images import edit_handlers as image_handlers

from bc.utils.models import BasePage


class CampaignPage(BasePage):
    template = "patterns/pages/campaigns/campaign_page.html"

    intro = fields.RichTextField(features=("link"))
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )

    content_panels = BasePage.content_panels + [
        edit_handlers.FieldPanel("intro"),
        image_handlers.ImageChooserPanel("hero_image"),
    ]
