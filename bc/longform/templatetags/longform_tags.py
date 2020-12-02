from django import template
from django.utils.safestring import mark_safe

from ..blocks import (
    NumberedHeadingBlock,
    NumberedParagraphBlock,
    NumberedSubheadingBlock,
)

register = template.Library()


def generate_block_number(
    chapter_number, heading_number, subheading_number, paragraph_number
):
    """
    Returns chapter_number.subheading_number.paragraph_number if chapter_number is
    available, or heading_number.subheading_number.paragraph_number if not.

    Doesn't include any part that isn't available. (e.g. can also return
    chapter_number.subheading_number only or heading_number.paragraph_number only)
    """
    block_number = ".".join(
        [
            f"{number}"
            for number in (
                chapter_number or heading_number,
                subheading_number,
                paragraph_number,
            )
            if number
        ]
    )

    return block_number


@register.filter
def process_block_numbers(streamblock, chapter_number=0):
    heading_number = 0
    subheading_number = 0
    paragraph_number = 0
    html = ""

    for child in streamblock:
        if isinstance(child.block, NumberedHeadingBlock) and not chapter_number:
            # Increase and reset numbers
            heading_number += 1
            subheading_number = 0
            paragraph_number = 0

            rendered_child = child.block.render(
                child.value, context={"block_number": heading_number}
            )
        elif isinstance(child.block, NumberedSubheadingBlock):
            # Increase and reset numbers
            if paragraph_number and not subheading_number:
                subheading_number = paragraph_number
            subheading_number += 1
            paragraph_number = 0

            block_number = generate_block_number(
                chapter_number, heading_number, subheading_number, paragraph_number,
            )

            rendered_child = child.block.render(
                child.value, context={"block_number": block_number}
            )
        elif isinstance(child.block, NumberedParagraphBlock):
            # Increase number
            paragraph_number += 1

            block_number = generate_block_number(
                chapter_number, heading_number, subheading_number, paragraph_number,
            )

            rendered_child = child.block.render(
                child.value, context={"block_number": block_number}
            )
        else:
            rendered_child = child.block.render(child.value)

        html += rendered_child

    return mark_safe(html)
