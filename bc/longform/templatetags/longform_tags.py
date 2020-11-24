from django import template
from django.utils.safestring import mark_safe

from ..blocks import (
    NumberedHeadingBlock,
    NumberedParagraphBlock,
    NumberedSubheadingBlock,
)

register = template.Library()


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

            if chapter_number:
                block_number = f"{chapter_number}.{subheading_number}"
            elif heading_number:
                block_number = f"{heading_number}.{subheading_number}"
            else:
                block_number = subheading_number

            rendered_child = child.block.render(
                child.value, context={"block_number": block_number}
            )
        elif isinstance(child.block, NumberedParagraphBlock):
            # Increase number
            paragraph_number += 1

            if subheading_number:
                block_number = f"{subheading_number}.{paragraph_number}"
            else:
                block_number = paragraph_number

            if chapter_number:
                block_number = f"{chapter_number}.{block_number}"
            elif heading_number:
                block_number = f"{heading_number}.{block_number}"

            rendered_child = child.block.render(
                child.value, context={"block_number": block_number}
            )
        else:
            rendered_child = child.block.render(child.value)

        html += rendered_child

    return mark_safe(html)
