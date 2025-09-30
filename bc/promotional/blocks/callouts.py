from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from bc.utils.blocks import LinkBlock


class CalloutWithImage(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    text = blocks.RichTextBlock(max_length=1024, required=False)
    image = ImageChooserBlock()
    link = LinkBlock(max_num=1, required=False)

    class Meta:
        icon = "redirect"
        template = "patterns/molecules/promotional-callout-with-image/promotional-callout-with-image.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        stream_block = value.get("link")
        link_block = stream_block[0] if stream_block else None

        if link_block:
            match link_block.block_type:
                case "internal_link" if (
                    link_block.value and link_block.value.get("page").live
                ):
                    context.update({"link": link_block.value})
                case "external_link":
                    context.update({"link": link_block.value})

        return context
