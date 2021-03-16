from wagtail.core import blocks
from wagtail.images import blocks as image_blocks
from wagtail.embeds import blocks as embed_blocks


class ImageOrEmbedBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock(required=False)
    embed = embed_blocks.EmbedBlock(required=False)


class SectionContentBlock(blocks.StructBlock):
    image_or_embed = ImageOrEmbedBlock()
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
