from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class AwardBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        form_classname="full title", icon="title", label="Award title"
    )
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = "success"


class JobPlatformBlock(blocks.StructBlock):
    """e.g. Indeed, Glassdoor"""

    title = blocks.CharBlock(form_classname="full title", icon="title", label="Name")
    image = ImageChooserBlock(label="Logo")
    url = blocks.URLBlock()

    class Meta:
        icon = "plus-inverse"


class MediaBlock(blocks.StructBlock):
    """Image or Embed or both"""

    embed = EmbedBlock(required=False)
    image = ImageChooserBlock(required=False)
    url = blocks.URLBlock(
        required=False,
        help_text="Optional URL for the image, if the embed is not specified",
    )

    def clean(self, value):
        """
        Valid combinations:

        1. embed
        2. embed + image
        3. image + url
        """
        struct_value = super().clean(value)

        errors = {}
        embed = value.get("embed")
        image = value.get("image")
        url = value.get("url")

        if not embed:
            if not image:
                error = ErrorList(
                    [
                        ValidationError(
                            "Please specify either an image or an embed, or both."
                        )
                    ]
                )
                errors["embed"] = errors["image"] = error

            if not url:
                error = ErrorList(
                    [
                        ValidationError(
                            "Please specify a url and an image if you are not using the embed field."
                        )
                    ]
                )
                errors["url"] = error
        else:
            if url:
                error = ErrorList(
                    [ValidationError("A url is not required if you specify an embed.")]
                )
                errors["url"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value

    class Meta:
        icon = "media"
