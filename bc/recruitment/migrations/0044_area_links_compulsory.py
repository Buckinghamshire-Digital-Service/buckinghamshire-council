# Generated by Django 2.2.24 on 2021-09-28 16:20

from django.db import migrations

import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks

import bc.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0043_talentlinkjob_dbs_check"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruitmentindexpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title",
                            group="Heading",
                            help_text='The link to this heading uses the heading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            icon="title",
                            label="Main heading",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
                        ),
                    ),
                    (
                        "subheading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title",
                            group="Heading",
                            help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            icon="title",
                            template="patterns/molecules/streamfield/blocks/subheading_block.html",
                        ),
                    ),
                    (
                        "paragraph",
                        wagtail.core.blocks.RichTextBlock(
                            features=[
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ]
                        ),
                    ),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "alt_text",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(required=False),
                                ),
                            ]
                        ),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    (
                        "local_area_links",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "introduction",
                                    wagtail.core.blocks.RichTextBlock(
                                        default="<p>Enter your postcode to find information for your area:</p>",
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                    ),
                                ),
                                (
                                    "aylesbury_vale_url",
                                    wagtail.core.blocks.URLBlock(
                                        label="Aylesbury Vale URL"
                                    ),
                                ),
                                (
                                    "chiltern_url",
                                    wagtail.core.blocks.URLBlock(label="Chiltern URL"),
                                ),
                                (
                                    "south_bucks_url",
                                    wagtail.core.blocks.URLBlock(
                                        label="South Bucks URL"
                                    ),
                                ),
                                (
                                    "wycombe_url",
                                    wagtail.core.blocks.URLBlock(label="Wycombe URL"),
                                ),
                            ]
                        ),
                    ),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                    (
                        "button",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.core.blocks.CharBlock(
                                        form_classname="title"
                                    ),
                                ),
                                (
                                    "link_url",
                                    wagtail.core.blocks.URLBlock(required=False),
                                ),
                                (
                                    "link_page",
                                    wagtail.core.blocks.PageChooserBlock(
                                        required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("highlight", bc.utils.blocks.HighlightBlock()),
                    (
                        "accordion",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "items",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    wagtail.core.blocks.CharBlock(
                                                        form_classname="full title",
                                                        icon="title",
                                                        label="Accordion title",
                                                    ),
                                                ),
                                                (
                                                    "content",
                                                    wagtail.core.blocks.StreamBlock(
                                                        [
                                                            (
                                                                "heading",
                                                                wagtail.core.blocks.CharBlock(
                                                                    form_classname="full title",
                                                                    group="Heading",
                                                                    help_text='The link to this heading uses the heading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                                                                    icon="title",
                                                                    label="Main heading",
                                                                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                                                                ),
                                                            ),
                                                            (
                                                                "subheading",
                                                                wagtail.core.blocks.CharBlock(
                                                                    form_classname="full title",
                                                                    group="Heading",
                                                                    help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                                                                    icon="title",
                                                                    template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                                                ),
                                                            ),
                                                            (
                                                                "paragraph",
                                                                wagtail.core.blocks.RichTextBlock(
                                                                    features=[
                                                                        "bold",
                                                                        "italic",
                                                                        "ol",
                                                                        "ul",
                                                                        "link",
                                                                        "document-link",
                                                                    ]
                                                                ),
                                                            ),
                                                            (
                                                                "image",
                                                                wagtail.core.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "image",
                                                                            wagtail.images.blocks.ImageChooserBlock(),
                                                                        ),
                                                                        (
                                                                            "alt_text",
                                                                            wagtail.core.blocks.CharBlock(
                                                                                help_text="Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                                                                                required=False,
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "caption",
                                                                            wagtail.core.blocks.CharBlock(
                                                                                required=False
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                            (
                                                                "embed",
                                                                wagtail.embeds.blocks.EmbedBlock(),
                                                            ),
                                                            (
                                                                "local_area_links",
                                                                wagtail.core.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "introduction",
                                                                            wagtail.core.blocks.RichTextBlock(
                                                                                default="<p>Enter your postcode to find information for your area:</p>",
                                                                                features=[
                                                                                    "bold",
                                                                                    "italic",
                                                                                    "ol",
                                                                                    "ul",
                                                                                    "link",
                                                                                    "document-link",
                                                                                ],
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "aylesbury_vale_url",
                                                                            wagtail.core.blocks.URLBlock(
                                                                                label="Aylesbury Vale URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "chiltern_url",
                                                                            wagtail.core.blocks.URLBlock(
                                                                                label="Chiltern URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "south_bucks_url",
                                                                            wagtail.core.blocks.URLBlock(
                                                                                label="South Bucks URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "wycombe_url",
                                                                            wagtail.core.blocks.URLBlock(
                                                                                label="Wycombe URL"
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                            (
                                                                "table",
                                                                wagtail.contrib.table_block.blocks.TableBlock(),
                                                            ),
                                                            (
                                                                "button",
                                                                wagtail.core.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "text",
                                                                            wagtail.core.blocks.CharBlock(
                                                                                form_classname="title"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "link_url",
                                                                            wagtail.core.blocks.URLBlock(
                                                                                required=False
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "link_page",
                                                                            wagtail.core.blocks.PageChooserBlock(
                                                                                required=False
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                            (
                                                                "highlight",
                                                                bc.utils.blocks.HighlightBlock(),
                                                            ),
                                                        ],
                                                        label="Accordion content",
                                                    ),
                                                ),
                                            ]
                                        ),
                                        label="Accordion items",
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "detail",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(
                                        form_classname="full title",
                                        icon="title",
                                        label="Detail title",
                                    ),
                                ),
                                (
                                    "content",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                        label="Detail content",
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
