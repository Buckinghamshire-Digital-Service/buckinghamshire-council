import copy

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from .constants import RICH_TEXT_FEATURES


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text = blocks.CharBlock(
        required=False,
        help_text="Describe the information, not the picture. Leave blank if the image "
        "is purely decorative. Do not repeat captions or content already on the page.",
    )
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "patterns/molecules/streamfield/blocks/image_block.html"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    title = blocks.CharBlock(required=False)

    class Meta:
        icon = "doc-full-inverse"
        template = "patterns/molecules/streamfield/blocks/document_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "patterns/molecules/streamfield/blocks/quote_block.html"


class HighlightBlock(blocks.RichTextBlock):
    class Meta:
        icon = "pick"
        features = RICH_TEXT_FEATURES
        template = "patterns/molecules/streamfield/blocks/highlight_block.html"


class LocalAreaLinksBlock(blocks.StructBlock):
    introduction = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        default="<p>Select your local area for information:</p>",
    )
    aylesbury_vale_url = blocks.URLBlock(required=False, label="Aylesbury Vale URL")
    chiltern_url = blocks.URLBlock(required=False, label="Chiltern URL")
    south_bucks_url = blocks.URLBlock(required=False, label="South Bucks URL")
    wycombe_url = blocks.URLBlock(required=False, label="Wycombe URL")

    class Meta:
        icon = ""
        template = "patterns/molecules/streamfield/blocks/local_area_links_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["has_area_links"] = any(
            [
                value["aylesbury_vale_url"],
                value["chiltern_url"],
                value["south_bucks_url"],
                value["wycombe_url"],
            ]
        )
        return context


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(classname="title")
    link_url = blocks.URLBlock(required=False)
    link_page = blocks.PageChooserBlock(required=False)

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        if not value["link_url"] and not value["link_page"]:
            errors["link_url"] = ErrorList(["You must specify a link url or page."])
            errors["link_page"] = ErrorList(["You must specify a link url or page."])

        if value["link_url"] and value["link_page"]:
            errors["link_url"] = ErrorList(
                ["You must specify a link url or page and not both."]
            )
            errors["link_page"] = ErrorList(
                ["You must specify a link url or page and not both."]
            )

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return result

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["text"] = value["text"]
        if value["link_url"]:
            context["value"]["url"] = value["link_url"]
        elif value["link_page"]:
            context["value"]["url"] = value["link_page"].get_url
        return context

    class Meta:
        icon = "success"
        template = "patterns/molecules/streamfield/blocks/button_block.html"


class BaseStoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        classname="full title",
        help_text=(
            "The link to this heading uses the heading text in lowercase, with no"
            " symbols, and with the spaces replaced with hyphens."
            ' e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"'
        ),
        icon="title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
        group="Heading",
        label="Main heading",
    )
    subheading = blocks.CharBlock(
        classname="full title",
        help_text=(
            "The link to this subheading uses the subheading text in lowercase, with no"
            " symbols, and with the spaces replaced with hyphens."
            ' e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"'
        ),
        icon="title",
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
        group="Heading",
    )
    paragraph = blocks.RichTextBlock(features=RICH_TEXT_FEATURES,)
    image = ImageBlock()
    embed = EmbedBlock()
    local_area_links = LocalAreaLinksBlock()
    table = TableBlock()
    button = ButtonBlock()
    highlight = HighlightBlock()

    class Meta:
        abstract = True
        template = "patterns/molecules/streamfield/stream_block.html"


class NestedStoryBlock(BaseStoryBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(**kwargs)
        # Bump down template for heading fields so headings don't clash with those outside the accordion
        self.child_blocks["heading"] = copy.deepcopy(self.child_blocks["heading"])
        self.child_blocks["subheading"] = copy.deepcopy(self.child_blocks["subheading"])
        self.child_blocks[
            "heading"
        ].meta.template = "patterns/molecules/streamfield/blocks/subheading_block.html"
        self.child_blocks[
            "subheading"
        ].meta.template = (
            "patterns/molecules/streamfield/blocks/subsubheading_block.html"
        )


class Accordion(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "title",
                    blocks.CharBlock(
                        classname="full title", icon="title", label="Accordion title"
                    ),
                ),
                ("content", NestedStoryBlock(label="Accordion content")),
            ]
        ),
        label="Accordion items",
    )

    class Meta:
        icon = ("list-ul",)
        template = ("patterns/molecules/streamfield/blocks/accordion.html",)


class DetailBlock(blocks.StructBlock):
    title = blocks.CharBlock(classname="full title", icon="title", label="Detail title")
    content = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Detail content")

    class Meta:
        icon = "arrow-right"
        template = "patterns/molecules/streamfield/blocks/detail_block.html"


# Main streamfield block to be inherited by Pages
class StoryBlock(BaseStoryBlock):
    accordion = Accordion()
    detail = DetailBlock()
