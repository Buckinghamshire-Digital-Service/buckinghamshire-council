from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from bc.utils.constants import RICH_TEXT_FEATURES

from ..utils.models import BasePage


class RecruitmentHomePage(BasePage):
    template = "patterns/pages/home/home_page--jobs.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    hero_title = models.CharField(
        max_length=255, help_text="eg. Finding a job in Buckinghamshire"
    )
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    body = StreamField(
        blocks.StreamBlock(
            [
                (
                    "content_block",
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock()),
                            (
                                "paragraph",
                                blocks.RichTextBlock(features=RICH_TEXT_FEATURES),
                            ),
                        ],
                        icon="list-ul",
                    ),
                )
            ],
            max_num=2,
            required=False,
        ),
        blank=True,
    )
    search_fields = BasePage.search_fields + [index.SearchField("hero_title")]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("hero_title"), ImageChooserPanel("hero_image")], "Hero",
        ),
        StreamFieldPanel("body"),
    ]
