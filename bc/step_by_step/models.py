from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, RichTextFieldPanel, StreamFieldPanel
from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.core.fields import RichTextField, StreamField

from bc.utils.models import BasePage


class StepInformationBlock(StreamBlock):
    paragraph = TextBlock()
    external_link = StructBlock(
        [("url", URLBlock()), ("title", CharBlock())], icon="link",
    )

    internal_link = StructBlock(
        [("page", PageChooserBlock()), ("title", CharBlock(required=False))],
        icon="link",
    )


class StepBlock(StructBlock):
    heading = TextBlock()
    information = StepInformationBlock()


class StepByStepIndexPage(BasePage):
    template = "patterns/pages/step_by_step/step_by_step_index_page.html"

    heading = models.TextField()
    introduction = RichTextField()

    steps = StreamField([("step", StepBlock())])

    content_panels = BasePage.content_panels + [
        FieldPanel("heading"),
        RichTextFieldPanel("introduction"),
        StreamFieldPanel("steps"),
    ]
