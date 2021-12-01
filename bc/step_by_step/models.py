from django.db import models

from wagtail.admin.edit_handlers import RichTextFieldPanel, StreamFieldPanel
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

    introduction = RichTextField()

    steps = StreamField([("step", StepBlock())])

    content_panels = BasePage.content_panels + [
        RichTextFieldPanel("introduction"),
        StreamFieldPanel("steps"),
    ]


class StepByStepReference(models.Model):
    step_by_step_page = models.ForeignKey(
        StepByStepPage, on_delete=models.CASCADE, related_name="referenced_pages"
    )
    referenced_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        related_name="referenced_step_by_step_pages",
    )
