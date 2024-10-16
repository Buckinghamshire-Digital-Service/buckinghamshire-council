from wagtail import blocks

from bc.utils.constants import RICH_TEXT_FEATURES


class Step(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    information = blocks.StreamBlock(
        (("paragraph", blocks.RichTextBlock(features=RICH_TEXT_FEATURES)),)
    )


class Steps(blocks.StructBlock):
    steps = blocks.ListBlock(Step, min_num=1)

    class Meta:
        icon = "list-ol"
        template = "patterns/organisms/promotional-steps/promotional-steps.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["steps"] = value["steps"]
        return context
