from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, RichTextFieldPanel, StreamFieldPanel
from wagtail.core.blocks import StructBlock, TextBlock
from wagtail.core.blocks.field_block import RichTextBlock
from wagtail.core.fields import RichTextField, StreamField

from bc.utils.models import BasePage


class StepBlock(StructBlock):
    heading = TextBlock()
    information = RichTextBlock()

    class Meta:
        template = "patterns/molecules/step_by_step/step-block.html"


class StepByStepPage(BasePage):
    template = "patterns/pages/step_by_step/step_by_step_page.html"

    intro_text = models.TextField(blank=True)
    introduction = RichTextField()

    steps = StreamField([("step", StepBlock())])

    content_panels = BasePage.content_panels + [
        FieldPanel("intro_text"),
        RichTextFieldPanel("introduction"),
        StreamFieldPanel("steps"),
    ]
