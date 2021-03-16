from wagtail.core import blocks

from bc.utils.blocks import ImageOrEmbedBlock


class SectionContentBlock(blocks.StructBlock):
    image_or_embed = ImageOrEmbedBlock(
        form_classname="struct-block c-sf-block c-sf-block__content-inner"
    )
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
