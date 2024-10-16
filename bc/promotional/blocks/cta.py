from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BaseMediaWithTextCTA(blocks.StructBlock):
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
        template = "patterns/molecules/promotional-media-with-text-cta/promotional-media-with-text-cta.html"
        icon = "pick"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        request = context.get("request")
        context["title"] = value["title"]
        context["text"] = value["text"]
        context["image"] = value["image"]

        embed = value["embed"]
        if embed is not None:
            context["embed_url"] = embed.url

        link_page = value["link_page"]
        if link_page is not None and link_page.live:
            context["link_url"] = link_page.get_url(request=request)
            context["link_text"] = value["link_text"]

        return context


class PrimaryMediaWithTextCTA(BaseMediaWithTextCTA):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["flavour"] = "primary"
        return context


class SecondaryMediaWithTextCTA(BaseMediaWithTextCTA):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["flavour"] = "secondary"
        return context
