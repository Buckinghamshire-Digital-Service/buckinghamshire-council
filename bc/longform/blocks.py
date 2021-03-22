from wagtail.core import blocks

from bc.utils.blocks import (
    BarChartBlock,
    BaseStoryBlock,
    DetailBlock,
    LineChartBlock,
    PieChartBlock,
)
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
    numbered_heading = NumberedHeadingBlock(
        help_text=(
            "Adds a number to the heading if is_numbered is not enabled on the long-form"
            " content page (e.g. 1. My heading). The link to this heading will be"
            ' "section-x" where x is the heading number.'
        ),
    )
    numbered_subheading = NumberedSubheadingBlock(
        help_text=(
            "Adds a number to the subheading (e.g. 1.1. My subheading). The link to this"
            ' subheading will be "section-x.y" where x is the heading or chapter number,'
            " and y is the subheading number."
        ),
    )
    numbered_paragraph = NumberedParagraphBlock(
        help_text=(
            "Adds a number before the paragraph (e.g. 1.1.1.). The link to this"
            ' paragraph will be "section-x.y.z" where x  is the heading or chapter'
            " number, y is the subheading number, and z is the paragraph number."
        ),
    )
    detail = DetailBlock()
    bar_chart = BarChartBlock()
    line_chart = LineChartBlock()
    pie_chart = PieChartBlock()
