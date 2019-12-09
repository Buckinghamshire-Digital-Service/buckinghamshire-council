from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from .constants import RICH_TEXT_FEATURES


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "patterns/molecules/streamfield/blocks/image_block.html"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    title = blocks.CharBlock(required=False)

    class Meta:
        icon = "doc-full-inverse"
        template = "patterns/molecules/streamfield/blocks/document_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "patterns/molecules/streamfield/blocks/quote_block.html"


class LocalAreaLinksBlock(blocks.StructBlock):
    introduction = blocks.RichTextBlock(features=RICH_TEXT_FEATURES)
    aylesbury_vale_url = blocks.URLBlock(required=False, label="Aylesbury Vale URL")
    chiltern_url = blocks.URLBlock(required=False, label="Chiltern URL")
    south_bucks_url = blocks.URLBlock(required=False, label="South Bucks URL")
    wycombe_url = blocks.URLBlock(required=False, label="Wycombe URL")
    postscript = blocks.RichTextBlock(required=False, features=RICH_TEXT_FEATURES)

    class Meta:
        icon = ""
        template = "patterns/molecules/local_area_links.html"


# Main streamfield block to be inherited by Pages
class StoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        classname="full title",
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
    )
    paragraph = blocks.RichTextBlock(features=RICH_TEXT_FEATURES,)
    local_area_links = LocalAreaLinksBlock()

    class Meta:
        template = "patterns/molecules/streamfield/stream_block.html"
