from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from bc.utils.constants import RICH_TEXT_FEATURES


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title", required=False
    )

    class Meta:
        template = ("patterns/molecules/navigation/blocks/menu_item.html",)


class ColumnWithHeader(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False, help_text="Leave blank if no header required."
    )
    content = blocks.RichTextBlock(features=RICH_TEXT_FEATURES)

    class Meta:
        template = ("patterns/molecules/navigation/blocks/footer_column.html",)


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    header_title = models.CharField(max_length=250, null=True, blank=True)
    footer_columns = StreamField(
        StreamBlock(
            [("column", ColumnWithHeader())],
            required=False,
            help_text="Columns of free text above the base footer.",
            max_num=3,
        ),
        blank=True,
    )
    footer_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of elements at the base of the page.",
    )

    panels = [
        FieldPanel("header_title"),
        StreamFieldPanel("footer_columns"),
        StreamFieldPanel("footer_links"),
    ]
