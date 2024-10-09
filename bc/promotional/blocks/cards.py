from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkCard(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    description = blocks.TextBlock(max_length=255)
    image = ImageChooserBlock()
    link_page = blocks.PageChooserBlock()
    link_text = blocks.CharBlock(max_length=128)


class LinkCards(blocks.StructBlock):
    items = blocks.ListBlock(LinkCard, max_num=3)
