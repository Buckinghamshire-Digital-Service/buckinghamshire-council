from django.utils.safestring import mark_safe

from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock

from bc.utils.blocks import (
    Accordion,
    ButtonBlock,
    CaptionedTableBlock,
    DetailBlock,
    HighlightBlock,
    ImageBlock,
    InsetTextBlock,
    TableBlock,
)
from bc.utils.constants import PLAIN_TEXT_TABLE_HELP_TEXT, RICH_TEXT_FEATURES

from .callouts import CalloutWithImage
from .cards import LinkCards


class PromotionalStoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        form_classname="full title",
        help_text=(
            "The link to this heading uses the heading text in lowercase, with no"
            " symbols, and with the spaces replaced with hyphens."
            ' e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"'
        ),
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
        group="Heading",
        label="Main heading",
    )
    subheading = blocks.CharBlock(
        form_classname="full title",
        help_text=(
            "The link to this subheading uses the subheading text in lowercase, with no"
            " symbols, and with the spaces replaced with hyphens."
            ' e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"'
        ),
        icon="title",
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
        group="Heading",
    )
    paragraph = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
    )
    image = ImageBlock()
    embed = EmbedBlock()
    plain_text_table = TableBlock(
        group="Table", help_text=mark_safe(PLAIN_TEXT_TABLE_HELP_TEXT)
    )
    table = CaptionedTableBlock(group="Table")
    button = ButtonBlock()
    highlight = HighlightBlock()
    inset_text = InsetTextBlock()
    accordion = Accordion()
    detail = DetailBlock()
    link_cards = LinkCards()
    callout_with_image = CalloutWithImage()

    class Meta:
        template = "patterns/molecules/streamfield-promotional/stream_block.html"
