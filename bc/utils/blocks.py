import copy

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from wagtail import blocks
from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.table_block.blocks import TableBlock as BaseTableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from .constants import PLAIN_TEXT_TABLE_HELP_TEXT, RICH_TEXT_FEATURES
from .utils import convert_markdown_links_to_html, is_number
from .widgets import BarChartInput, LineChartInput, PieChartInput


class TableBlock(BaseTableBlock):
    def render(self, value, context=None):
        if not value:
            return super().render(value, context)
        data = value["data"]
        for row_index, row in enumerate(data):
            for cell_index, cell in enumerate(row):
                if cell:
                    data[row_index][cell_index] = convert_markdown_links_to_html(cell)
        value["data"] = data
        return super().render(value, context)

    def get_table_options(self, table_options=None):
        options = super().get_table_options(table_options)
        options["renderer"] = "html"
        return options


class AlignedBlock(blocks.StreamBlock):
    numeric = blocks.DecimalBlock()
    rich_text = blocks.RichTextBlock()


class CaptionedTableBlock(blocks.StructBlock):
    table = TypedTableBlock(
        [
            ("left_aligned_column", AlignedBlock()),
            ("right_aligned_column", AlignedBlock()),
        ],
    )
    caption = blocks.TextBlock(required=False)

    class Meta:
        icon = "table"
        template = "patterns/molecules/streamfield/blocks/captioned_table_block.html"

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context)

        rows = []
        num_rows = 0

        for row in value["table"].rows:
            rows.append([])
            for col_ind, col in enumerate(row):
                for internal_ind, internal_col in enumerate(col.value):
                    while internal_ind + num_rows >= len(rows):
                        rows.append([])
                    rows[internal_ind + num_rows].append(
                        {
                            "block_name": col.block.name,
                            "value": internal_col,
                            "ind": col_ind,
                        }
                    )
            num_rows = len(rows)

        if rows:
            # equalise all rows to maintain alignment
            max_row_length = max([len(row) for row in rows])
            for row in rows:
                for i in range(max_row_length):
                    try:
                        col = row[i]
                        if col["ind"] != i:
                            row.insert(
                                i, {"block_name": "rich_text", "value": "", "ind": i}
                            )
                    except IndexError:
                        row.append({"block_name": "rich_text", "value": "", "ind": i})

        ctx["value"]["rows"] = rows
        return ctx


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
        default_features = ["h2", "h3", "big-text"] + RICH_TEXT_FEATURES
        features = kwargs.get("features", default_features)
        super().__init__(*args, features=features, **kwargs)


class InsetTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "patterns/molecules/streamfield/blocks/inset_block.html"

    def __init__(self, *args, **kwargs):
        # Setting features in class Meta doesn't work, so add it on init
        default_features = ["link", "document-link"]
        features = kwargs.get("features", default_features)
        super().__init__(*args, features=features, **kwargs)


class LocalAreaLinksBlock(blocks.StructBlock):
    heading = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        default="<p><b>Find local information</b></p>",
    )
    introduction = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        default=(
            "<p>While we finish building this new website, we’re keeping some local"
            " information on our old council websites</p>"
        ),
    )
    postcode_lookup_text = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        default="<p>Enter your postcode to help us redirect you to the right place.</p>",
        help_text="The text that appears on top of the postcode lookup input",
    )
    area_lookup_text = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        default="<p>Select your local area to help us direct you to the right place:</p>",
        help_text="The text that appears on top of the list of local area links",
    )
    aylesbury_vale_url = blocks.URLBlock(label="Aylesbury Vale URL")
    chiltern_url = blocks.URLBlock(label="Chiltern URL")
    south_bucks_url = blocks.URLBlock(label="South Bucks URL")
    wycombe_url = blocks.URLBlock(label="Wycombe URL")

    class Meta:
        icon = ""
        template = "patterns/molecules/streamfield/blocks/local_area_links_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["link_urls"] = {
            "Aylesbury Vale": value["aylesbury_vale_url"],
            "Chiltern": value["chiltern_url"],
            "South Bucks": value["south_bucks_url"],
            "Wycombe": value["wycombe_url"],
        }
        if parent_context is not None and parent_context.get("request"):
            from .models import ImportantPages

            request = parent_context["request"]
            context["contact_us_page"] = ImportantPages.for_request(
                request
            ).contact_us_page
        return context


class LinkBlockValue(blocks.StructValue):
    def get_text(self):
        if title := self.get("title"):
            return title
        if page := self.get("page"):
            return page.specific.listing_title or page.title
        return ""

    def get_url(self):
        if page := self.get("page"):
            return page.url
        if url := self.get("url"):
            return url
        return ""


class ExternalLinkBlock(blocks.StructBlock):
    url = blocks.URLBlock()
    title = blocks.CharBlock()

    class Meta:
        icon = "link"
        label = "External link"
        value_class = LinkBlockValue


class InternalLinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(required=False)

    class Meta:
        icon = "link"
        label = "Internal link"
        value_class = LinkBlockValue


class LinkBlock(blocks.StreamBlock):
    external_link = ExternalLinkBlock()
    internal_link = InternalLinkBlock()


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


class BaseChartBlock(BaseTableBlock):
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

    def convert_column_data_to_numbers(self, columns):
        """
        Converts string data inside a column into its number/float equivalent
        if applicable
        """
        result = []
        for column in columns:
            series = {
                "name": column["name"],
                "data": [
                    float(cell) if is_number(cell) else cell for cell in column["data"]
                ],
            }
            result.append(series)

        return result

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

        cleaned_table = copy.deepcopy(table)

        # Remove empty rows
        for row in table:
            if all([cell is None or not cell.strip() for cell in row]):
                cleaned_table.remove(row)

        # Remove empty columns
        transposed_table = [*zip(*cleaned_table)]
        removed_count = 0
        for index, col in enumerate(transposed_table):
            if all([cell is None or not cell.strip() for cell in col]):
                for row in cleaned_table:
                    del row[index - removed_count]
                removed_count += 1

        return cleaned_table

    def clean(self, value):
        """
        In Wagtail 6.0, the TableBlock header controls were switched to
        a field (`table_header_choice`) that requires user input.

        References:
        - https://docs.wagtail.org/en/stable/releases/6.0.html#accessibility-improvements
        - https://github.com/wagtail/wagtail/blob/ab9d1edb/wagtail/contrib/table_block/blocks.py#L162
        - https://github.com/wagtail/wagtail/blob/ab9d1edb/wagtail/contrib/table_block/blocks.py#L131-L134

        This ensures that `table_header_choice` is not empty,
        otherwise, a ValidationError is raised.

        Since the chart blocks *always* have row and column labels,
        we set the value of `table_header_choice` to "both"
        """
        value["table_header_choice"] = "both"
        return super().clean(value)

    class Meta:
        abstract = True
        template = "patterns/molecules/streamfield/blocks/chart_block.html"


class WasteWizardSnippetBlock(blocks.StaticBlock):
    class Meta:
        admin_text = "This will be replaced by the Waste Wizard widget"
        icon = "placeholder"
        template = (
            "patterns/molecules/streamfield/blocks/waste_wizard_snippet_block.html"
        )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["has_rc_consent"] = parent_context["page"].has_rc_consent(
            parent_context["request"]
        )
        return context


class BarChartBlock(BaseChartBlock):
    @cached_property
    def field(self):
        return forms.CharField(
            widget=BarChartInput(table_options=self.table_options),
            **self.field_options,
        )

    def render(self, value, context=None):
        if context is None:
            new_context = {}
        else:
            new_context = dict(context)

        # If no value at all, exit early
        if not value:
            return super().render(value, new_context)

        cleaned_data = self.clean_table_values(value["data"])
        columns = self.get_table_columns(cleaned_data)

        # If no data found, exit early
        if not columns:
            return super().render(value, new_context)

        data_columns = self.convert_column_data_to_numbers(columns[1:])
        new_value = {
            "chart": {"type": "column"},
            "series": data_columns,
        }
        if value["direction"] == "horizontal":
            new_value["chart"]["type"] = "bar"

        first_column = columns[0]
        new_value["xAxis"] = {
            "categories": first_column["data"],
            "title": {"text": first_column["name"]},
        }
        new_value["yAxis"] = {}

        new_context.update(
            {
                "id": "bar-{0}".format(value["id"]),
                "table_first": value["table_first"],
                "table_headers": cleaned_data[0],
                "table_data": cleaned_data[1:],
                "title": value["table_title"],
                "caption": value["chart_caption"],
                "default_title": "Bar chart",
            }
        )

        return super().render(new_value, new_context)


class LineChartBlock(BaseChartBlock):
    @cached_property
    def field(self):
        return forms.CharField(
            widget=LineChartInput(table_options=self.table_options),
            **self.field_options,
        )

    def render(self, value, context=None):
        if context is None:
            new_context = {}
        else:
            new_context = dict(context)

        # If no value at all, exit early
        if not value:
            return super().render(value, new_context)

        cleaned_data = self.clean_table_values(value["data"])
        columns = self.get_table_columns(cleaned_data)

        # If no data found, exit early
        if not columns:
            return super().render(value, new_context)

        data_columns = self.convert_column_data_to_numbers(columns[1:])
        new_value = {
            "chart": {"type": "line"},
            "series": data_columns,
        }

        first_column = columns[0]
        new_value["xAxis"] = {
            "categories": first_column["data"],
            "title": {"text": first_column["name"]},
        }
        new_value["yAxis"] = {}

        new_context.update(
            {
                "id": "line-{0}".format(value["id"]),
                "table_first": value["table_first"],
                "table_headers": cleaned_data[0],
                "table_data": cleaned_data[1:],
                "title": value["table_title"],
                "caption": value["chart_caption"],
                "default_title": "Line graph",
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

    def render(self, value, context=None):
        if context is None:
            new_context = {}
        else:
            new_context = dict(context)

        # If no value at all, exit early
        if not value:
            return super().render(value, new_context)

        cleaned_data = self.clean_table_values(value["data"])

        # Get total value
        total_value = 0
        for row in cleaned_data:
            try:
                # The preview will update when key presses are made, so we need to
                # handle the case where the second column has no value.
                # When the second column is completed, the preview will update again
                # and the total value will be correct.
                if is_number(row[1]):
                    total_value += float(row[1])
            except IndexError:
                pass  # Fails silently

        # Use percentage values for the chart
        series_data = []
        for row in cleaned_data:
            try:
                # The preview will update when key presses are made, so we need to
                # handle the case where the second column has no value.
                # When the second column is completed, the preview will update again
                # and the total value will be correct.
                if is_number(row[1]):
                    series_value = round(float(row[1]) / total_value * 100, 1)
                else:
                    series_value = row[1]
                series = {"name": row[0], "y": series_value}
                series_data.append(series)
                row.append(f"{series_value}%")
            except IndexError:
                pass  # Fails silently

        new_value = {"chart": {"type": "pie"}, "series": [{"data": series_data}]}

        new_context.update(
            {
                "id": "pie-{0}".format(value["id"]),
                "table_first": value["table_first"],
                "table_headers": ["", "Values", "Percentage (%)"],
                "table_data": cleaned_data,
                "title": value["table_title"],
                "caption": value["chart_caption"],
                "default_title": "Pie chart",
            }
        )

        return super().render(new_value, new_context)


class EHCCoSearchBlock(blocks.StaticBlock):
    class Meta:
        admin_text = "This will be replaced by the EHC CoSearch widget"
        icon = "placeholder"
        template = "patterns/molecules/streamfield/blocks/ehc_cosearch_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["get_matching_schools_url"] = reverse(
            "family_information:get_matching_schools"
        )
        context["get_corresponding_ehc_co_url"] = reverse(
            "family_information:get_corresponding_ehc_co"
        )
        return context


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
    paragraph = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
    )
    image = ImageBlock()
    embed = EmbedBlock()
    local_area_links = LocalAreaLinksBlock()
    plain_text_table = TableBlock(
        group="Table", help_text=mark_safe(PLAIN_TEXT_TABLE_HELP_TEXT)
    )
    table = CaptionedTableBlock(group="Table")
    button = ButtonBlock()
    highlight = HighlightBlock()
    inset_text = InsetTextBlock()
    ehc_co_search = EHCCoSearchBlock(label="EHCCo Search")

    class Meta:
        abstract = True
        template = "patterns/molecules/streamfield/stream_block.html"


class NestedStoryBlock(BaseStoryBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(**kwargs)
        # Bump down template for heading fields so headings don't clash with those outside the accordion
        self.child_blocks["heading"] = copy.deepcopy(self.child_blocks["heading"])
        self.child_blocks["subheading"] = copy.deepcopy(self.child_blocks["subheading"])
        self.child_blocks["heading"].meta.template = (
            "patterns/molecules/streamfield/blocks/subheading_block.html"
        )
        self.child_blocks["subheading"].meta.template = (
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
        icon = "list-ul"
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


class ImageOrEmbedBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False)

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        if not value["image"] and not value["embed"]:
            errors["image"] = ErrorList(["You must specify an image or an embed URL."])
            errors["embed"] = ErrorList(["You must specify an image or an embed URL."])

        if value["image"] and value["embed"]:
            errors["image"] = ErrorList(
                ["You must specify an image or an embed URL — not both."]
            )
            errors["embed"] = ErrorList(
                ["You must specify an image or an embed URL — not both."]
            )

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return result

    class Meta:
        icon = "media"
