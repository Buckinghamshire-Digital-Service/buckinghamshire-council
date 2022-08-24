from django.db import models

from wagtail.admin.panels import FieldPanel, RichTextFieldPanel, StreamFieldPanel
from wagtail.blocks import StructBlock, TextBlock
from wagtail.blocks.field_block import RichTextBlock
from wagtail.fields import RichTextField, StreamField

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


class StepByStepReference(models.Model):
    step_by_step_page = models.ForeignKey(
        StepByStepPage, on_delete=models.CASCADE, related_name="referenced_pages"
    )
    referenced_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        related_name="referenced_step_by_step_pages",
    )

    @property
    def page(self):
        return self.step_by_step_page
