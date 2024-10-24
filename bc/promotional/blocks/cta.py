from django.core.exceptions import ValidationError

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
    link_page = blocks.PageChooserBlock(required=False)
    link_url = blocks.URLBlock(
        label="Link URL",
        required=False,
        help_text="Please specify the URL or an internal page, not both at the same time",
    )
    link_text = blocks.CharBlock(
        max_length=128,
        required=False,
        help_text="Link text must be populated if a link is specified",
    )

    class Meta:
        label = "Media with text call to action"
        template = "patterns/molecules/promotional-media-with-text-cta/promotional-media-with-text-cta.html"
        icon = "pick"

    def clean(self, value) -> None:
        result = super().clean(value)
        errors = {}
        if value["link_page"] is not None and value["link_url"]:
            errors["link_page"] = ValidationError(
                "Page cannot be specified at the same time as the URL"
            )
            errors["link_url"] = ValidationError(
                "URL cannot be specified at the same time as the page"
            )
        if not value["link_text"] and (
            value["link_page"] is not None or value["link_url"]
        ):
            errors["link_text"] = ValidationError(
                "Link text cannot be empty if a link is specified"
            )
        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)
        return result

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        request = context.get("request")
        context["title"] = value["title"]
        context["text"] = value["text"]
        context["image"] = value["image"]
        context["link_text"] = value["link_text"]

        embed = value["embed"]
        if embed is not None:
            context["embed_url"] = embed.url

        link_page = value["link_page"]
        if value["link_url"]:
            context["link_url"] = value["link_url"]
        elif link_page is not None and link_page.live:
            context["link_url"] = link_page.get_url(request=request)

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


class AlignedMediaWithTextItem(BaseMediaWithTextCTA):
    class Meta:
        label = "Item"


class AlignedMediaWithText(blocks.StructBlock):
    items = blocks.ListBlock(AlignedMediaWithTextItem, min_num=1)

    class Meta:
        template = "patterns/organisms/promotional-aligned-media-with-text/promotional-aligned-media-with-text.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        items = []
        for i, item in enumerate(value["items"]):
            items.append(
                {
                    "block": item,
                    "alignment": "left" if i % 2 == 0 else "right",
                }
            )

        context["items"] = items
        return context
