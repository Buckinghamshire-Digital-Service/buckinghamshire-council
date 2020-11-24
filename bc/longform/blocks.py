from wagtail.core import blocks

from bc.utils.blocks import BaseStoryBlock, DetailBlock
from bc.utils.constants import RICH_TEXT_FEATURES


class NumberedHeadingBlock(blocks.CharBlock):
    class Meta:
        classname = "full title"
        group = "Heading"
        icon = "title"
        label = "Numbered main heading"
        template = "patterns/molecules/streamfield/blocks/numbered_heading_block.html"


class NumberedSubheadingBlock(blocks.CharBlock):
    class Meta:
        classname = "full title"
        group = "Heading"
        icon = "title"
        template = (
            "patterns/molecules/streamfield/blocks/numbered_subheading_block.html"
        )


class NumberedParagraphBlock(blocks.RichTextBlock):
    class Meta:
        features = RICH_TEXT_FEATURES
        template = "patterns/molecules/streamfield/blocks/numbered_paragraph_block.html"


# Main streamfield block to be inherited by Longform Pages
# Consider if any new blocks are also needed on utils/blocks.py
class LongformStoryBlock(BaseStoryBlock):
    numbered_heading = NumberedHeadingBlock()
    numbered_subheading = NumberedSubheadingBlock()
    numbered_paragraph = NumberedParagraphBlock()
    detail = DetailBlock()
