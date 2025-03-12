from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class AwardBlock(blocks.StructBlock):
    title = blocks.CharBlock(form_classname="title", icon="title", label="Award title")
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = "success"


class JobPlatformBlock(blocks.StructBlock):
    """e.g. Indeed, Glassdoor"""

    title = blocks.CharBlock(form_classname="title", icon="title", label="Name")
    image = ImageChooserBlock(label="Logo")
    url = blocks.URLBlock()

    class Meta:
        icon = "plus-inverse"


class ImageWithLinkBlock(blocks.StructBlock):
    """Image with link"""

    image = ImageChooserBlock()
    url = blocks.URLBlock(
        help_text="Link for the image",
    )

    class Meta:
        icon = "image"


class MediaBlock(blocks.StreamBlock):
    """Image with link or Embed"""

    embed = EmbedBlock(
        help_text="Embed URL, e.g. https://www.youtube.com/watch?v=Js8dIRxwSRY"
    )
    image_with_link = ImageWithLinkBlock()

    class Meta:
        icon = "media"
