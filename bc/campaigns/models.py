from django.db import models

from wagtail.admin import edit_handlers
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.images import edit_handlers as image_handlers
from wagtail.images import blocks as image_blocks


from bc.utils.models import BasePage


class SectionContentBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock()
    subheading = blocks.CharBlock(
        max_length=250,
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
    )
    paragraph = blocks.RichTextBlock(features=["link"])


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="full title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
    )
    intro = blocks.RichTextBlock(features=["link"])

    content = blocks.ListBlock(SectionContentBlock())


class CampaignPage(BasePage):
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
