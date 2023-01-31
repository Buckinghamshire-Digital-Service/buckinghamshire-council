from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class AwardBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        form_classname="full title", icon="title", label="Award title"
    )
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = "success"
