from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from bc.utils.blocks import Accordion


class ExplainerCTALink(blocks.StructBlock):
    text = blocks.CharBlock(max_length=128)
    page = blocks.PageChooserBlock()

    class Meta:
        label = "Link"


class ExplainerCTA(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    text = blocks.TextBlock(max_length=512, required=False)
    image = ImageChooserBlock()
    links = blocks.ListBlock(ExplainerCTALink, min_num=1, max_num=2)

    class Meta:
        label = "Call to action"


class Explainer(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    text = blocks.RichTextBlock(required=False)
    details = Accordion()
    details_link_page = blocks.PageChooserBlock(required=False)
    details_link_text = blocks.CharBlock(max_length=128, required=False)
    cta = blocks.StreamBlock(
        [("cta", ExplainerCTA())], max_num=1, required=False, label="Call to action"
    )
