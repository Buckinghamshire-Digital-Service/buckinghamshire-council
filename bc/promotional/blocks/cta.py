from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class MediaWithTextCTA(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    text = blocks.TextBlock(max_length=512, required=False)
    image = ImageChooserBlock()
    embed = EmbedBlock(
        required=False,
        label="Embed URL",
        help_text="URL to a YouTube video or another embed",
    )
    link_page = blocks.PageChooserBlock()
    link_text = blocks.CharBlock(max_length=128)

    class Meta:
        label = "Media with text call to action"
