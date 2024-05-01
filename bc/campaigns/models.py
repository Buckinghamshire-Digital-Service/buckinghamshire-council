from django.db import models
from django.shortcuts import redirect
from wagtail import fields
from wagtail import models as wt_models
from wagtail.admin.panels import FieldPanel

from bc.campaigns.blocks import CampaignPageStoryBlock
from bc.utils.models import BasePage


class CampaignIndexPage(wt_models.Page):
    parent_page_types = ["home.homepage"]
    subpage_types = ["campaigns.campaignpage"]
    max_count = 1

    def serve(self, request, *args, **kwargs):
        site = wt_models.Site.find_for_request(request)
        return redirect(site.root_page.url)


class CampaignPage(BasePage):
    parent_page_types = ["campaigns.campaignindexpage"]
    subpage_types = ["forms.formpage", "standardpages.informationpage"]

    template = "patterns/pages/campaigns/campaign_page.html"

    intro = fields.RichTextField(features=("link", "bold", "italic"))
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    body = fields.StreamField(
        CampaignPageStoryBlock(block_counts={"heading": {"min_num": 3, "max_num": 3}})
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hero_image"),
        FieldPanel("body"),
    ]
