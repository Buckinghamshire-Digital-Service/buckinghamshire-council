from wagtail.core import blocks
from wagtail.images import blocks as image_blocks


class SectionContentBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock()
    subheading = blocks.CharBlock(
        max_length=250,
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
    )
    paragraph = blocks.RichTextBlock(features=["link"])


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="full title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
    )
    intro = blocks.RichTextBlock(features=["link"])

    content = blocks.ListBlock(SectionContentBlock())
