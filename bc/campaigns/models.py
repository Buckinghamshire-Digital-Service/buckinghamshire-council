from django.db import models

from wagtail.admin import edit_handlers
from wagtail.core import fields
from wagtail.core import models as wt_models
from wagtail.images import edit_handlers as image_handlers

from bc.campaigns.blocks import SectionBlock
from bc.utils.models import BasePage


class CampaignIndexPage(wt_models.Page):
    parent_page_types = ["home.homepage"]
    subpage_types = ["campaigns.campaignpage"]
    max_count = 1


class CampaignPage(BasePage):
    parent_page_types = ["campaigns.campaignindexpage"]

    template = "patterns/pages/campaigns/campaign_page.html"

    intro = fields.RichTextField(features=("link"))
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    sections = fields.StreamField(
        block_types=[("section", SectionBlock())], null=True, blank=False,
    )

    content_panels = BasePage.content_panels + [
        edit_handlers.FieldPanel("intro"),
        image_handlers.ImageChooserPanel("hero_image"),
        edit_handlers.StreamFieldPanel("sections"),
    ]
