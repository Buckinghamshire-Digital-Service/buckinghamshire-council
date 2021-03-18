import copy

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.functional import cached_property

from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from .constants import RICH_TEXT_FEATURES
from .widgets import BarChartInput, PieChartInput


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
    quote = blocks.CharBlock(form_classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "patterns/molecules/streamfield/blocks/quote_block.html"


class HighlightBlock(blocks.RichTextBlock):
    class Meta:
        icon = "pick"
        template = "patterns/molecules/streamfield/blocks/highlight_block.html"

    def __init__(self, *args, **kwargs):
        # Setting features in class Meta doesn't work, so add it on init
        default_features = ["h3", "big-text"] + RICH_TEXT_FEATURES
        features = kwargs.get("features", default_features)
        super().__init__(self, *args, features=features, **kwargs)


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
    text = blocks.CharBlock(form_classname="title")
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


class BaseChartBlock(TableBlock):
    @property
    def media(self):
        return forms.Media(
            css={
                "all": [
                    versioned_static("utils/css/vendor/handsontable-6.2.2.full.min.css")
                ]
            },
            js=[versioned_static("utils/js/vendor/handsontable-6.2.2.full.min.js")],
        )

    def get_table_columns(self, table):
        """
        Return table as column headers and column values
        e.g. { name: row 1, data: [row 2, row 3, ...] }
        """
        result = []
        transposed_table = [*zip(*table)]
        for col in transposed_table:
            series = {
                "name": col[0],
                "data": [cell for cell in col[1:]],
            }
            result.append(series)

        return result

    def clean_table_values(self, table):
        """
        Remove empty rows and columns
        """
        import copy

        cleaned_table = copy.deepcopy(table)

        # Remove empty rows
        for row in table:
            if all([cell is None for cell in row]):
                cleaned_table.remove(row)

        # Remove empty columns
        transposed_table = [*zip(*cleaned_table)]
        for index, col in enumerate(transposed_table):
            if all([cell is None for cell in col]):
                for row in cleaned_table:
                    del row[index]

        return cleaned_table

    class Meta:
        abstract = True
        template = "patterns/molecules/streamfield/blocks/chart_block.html"


class BarChartBlock(BaseChartBlock):
    @cached_property
    def field(self):
        return forms.CharField(
            widget=BarChartInput(table_options=self.table_options),
            **self.field_options,
        )

    def render(self, value, context={}):
        if context is None:
            new_context = {}
        else:
            new_context = dict(context)

        cleaned_data = self.clean_table_values(value["data"])
        columns = self.get_table_columns(cleaned_data)

        if value["direction"] == "horizontal":
            new_value = {
                "chart": {"type": "bar"},
                "plotOptions": {"series": {"stacking": "normal"}},
                "series": columns[1:],
            }
        else:
            new_value = {
                "chart": {"type": "column"},
                "plotOptions": {"column": {"stacking": "normal"}},
                "series": columns[1:],
            }

        first_column = columns[0]
        new_value["xAxis"] = {"categories": first_column["data"]}
        new_value["yAxis"] = {"title": {"text": first_column["name"]}}

        new_context.update(
            {
                "id": "bar-" + value["id"],
                "table_first": value["table_first"],
                "table_headers": cleaned_data[0],
                "table_data": cleaned_data[1:],
                "title": value["table_title"],
                "caption": value["chart_caption"],
            }
        )

        return super().render(new_value, new_context)


class PieChartBlock(BaseChartBlock):
    @cached_property
    def field(self):
        return forms.CharField(
            widget=PieChartInput(table_options=self.table_options),
            **self.field_options,
        )

    def render(self, value, context={}):
        if context is None:
            new_context = {}
        else:
            new_context = dict(context)

        cleaned_data = self.clean_table_values(value["data"])
        data = []
        for row in cleaned_data:
            try:
                data_as_number = float(row[1])
            except:
                data_as_number = row[1]
            series = {
                "name": row[0],
                "y": data_as_number,
            }
            data.append(series)

        new_value = {"chart": {"type": "pie"}, "series": [{"data": data,}]}

        new_context.update(
            {
                "id": "pie" + value["id"],
                "table_first": value["table_first"],
                "table_data": cleaned_data,
                "title": value["table_title"],
                "caption": value["chart_caption"],
            }
        )

        return super().render(new_value, new_context)


class BaseStoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        form_classname="full title",
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
        form_classname="full title",
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
                        form_classname="full title",
                        icon="title",
                        label="Accordion title",
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
    title = blocks.CharBlock(
        form_classname="full title", icon="title", label="Detail title"
    )
    content = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Detail content")

    class Meta:
        icon = "arrow-right"
        template = "patterns/molecules/streamfield/blocks/detail_block.html"


# Main streamfield block to be inherited by Pages
# Consider if any new blocks are also needed on longform/blocks.py
class StoryBlock(BaseStoryBlock):
    accordion = Accordion()
    detail = DetailBlock()
