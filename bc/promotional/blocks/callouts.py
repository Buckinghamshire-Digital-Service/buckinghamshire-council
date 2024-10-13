from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class CalloutWithImage(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    text = blocks.RichTextBlock(max_length=1024, required=False)
    image = ImageChooserBlock()
    link_page = blocks.PageChooserBlock(required=False)
    link_text = blocks.CharBlock(max_length=128, required=False)

    class Meta:
        icon = "redirect"
        template = "patterns/molecules/promotional-callout-with-image/promotional-callout-with-image.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if value.get("link_page") is not None:
            context["link_url"] = value["link_page"].get_url(
                request=context.get("request")
            )
        return context
