from wagtail import blocks

from bc.utils.blocks import StoryBlock


class FormButtonBlock(blocks.StructBlock):
    """A block to act as a hard-coded link to the form subpage route"""

    text = blocks.CharBlock(form_classname="title", help_text="The button label")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["text"] = value["text"]

        # Hard-code the URL of the button
        page = parent_context["page"]
        context["value"]["url"] = page.reverse_subpage("form_route")

        return context

    class Meta:
        icon = "success"
        template = "patterns/molecules/streamfield/blocks/button_block.html"


class CaseFormStoryBlock(StoryBlock):
    form_link_button = FormButtonBlock()
