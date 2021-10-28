from wagtail.admin.edit_handlers import RichTextFieldPanel, StreamFieldPanel
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
    paragraph = TextBlock(
        template="patterns/molecules/step_by_step/blocks/paragraph-block.html",
    )
    external_link = StructBlock(
        [("url", URLBlock()), ("title", CharBlock())],
        icon="link",
        template="patterns/molecules/step_by_step/blocks/external-link-block.html",
    )

    internal_link = StructBlock(
        [("page", PageChooserBlock()), ("title", CharBlock(required=False))],
        icon="link",
        template="patterns/molecules/step_by_step/blocks/internal-link-block.html",
    )

    class Meta:
        template = "patterns/molecules/step_by_step/blocks/step-block.html"


class StepBlock(StructBlock):
    heading = TextBlock()
    information = StepInformationBlock()

    class Meta:
        template = "patterns/molecules/step_by_step/blocks/step-block.html"


class StepByStepIndexPage(BasePage):
    template = "patterns/pages/step_by_step/step_by_step_index_page.html"

    introduction = RichTextField()

    steps = StreamField([("step", StepBlock())])

    content_panels = BasePage.content_panels + [
        RichTextFieldPanel("introduction"),
        StreamFieldPanel("steps"),
    ]
