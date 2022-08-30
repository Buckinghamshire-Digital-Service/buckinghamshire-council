# Generated by Django 3.2.13 on 2022-08-02 12:31

from django.db import migrations

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks

import bc.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0052_talentlinkjob_dbs_check_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruitmentindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.CharBlock(
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
                        wagtail.blocks.CharBlock(
                            form_classname="full title",
                            group="Heading",
                            help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            icon="title",
                            template="patterns/molecules/streamfield/blocks/subheading_block.html",
                        ),
                    ),
                    (
                        "paragraph",
                        wagtail.blocks.RichTextBlock(
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
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "alt_text",
                                    wagtail.blocks.CharBlock(
                                        help_text="Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ]
                        ),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    (
                        "local_area_links",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.RichTextBlock(
                                        default="<p><b>Find local information</b></p>",
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
                                    "introduction",
                                    wagtail.blocks.RichTextBlock(
                                        default="<p>While we finish building this new website, we’re keeping some local information on our old council websites</p>",
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
                                    "postcode_lookup_text",
                                    wagtail.blocks.RichTextBlock(
                                        default="<p>Enter your postcode to help us redirect you to the right place.</p>",
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                        help_text="The text that appears on top of the postcode lookup input",
                                    ),
                                ),
                                (
                                    "area_lookup_text",
                                    wagtail.blocks.RichTextBlock(
                                        default="<p>Select your local area to help us direct you to the right place:</p>",
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                        help_text="The text that appears on top of the list of local area links",
                                    ),
                                ),
                                (
                                    "aylesbury_vale_url",
                                    wagtail.blocks.URLBlock(label="Aylesbury Vale URL"),
                                ),
                                (
                                    "chiltern_url",
                                    wagtail.blocks.URLBlock(label="Chiltern URL"),
                                ),
                                (
                                    "south_bucks_url",
                                    wagtail.blocks.URLBlock(label="South Bucks URL"),
                                ),
                                (
                                    "wycombe_url",
                                    wagtail.blocks.URLBlock(label="Wycombe URL"),
                                ),
                            ]
                        ),
                    ),
                    (
                        "plain_text_table",
                        wagtail.contrib.table_block.blocks.TableBlock(group="Table"),
                    ),
                    (
                        "table",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "table",
                                    wagtail.contrib.typed_table_block.blocks.TypedTableBlock(
                                        [
                                            (
                                                "left_aligned_column",
                                                wagtail.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "numeric",
                                                            wagtail.blocks.DecimalBlock(),
                                                        ),
                                                        (
                                                            "rich_text",
                                                            wagtail.blocks.RichTextBlock(),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "right_aligned_column",
                                                wagtail.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "numeric",
                                                            wagtail.blocks.DecimalBlock(),
                                                        ),
                                                        (
                                                            "rich_text",
                                                            wagtail.blocks.RichTextBlock(),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.blocks.TextBlock(required=False),
                                ),
                            ],
                            group="Table",
                        ),
                    ),
                    (
                        "button",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.CharBlock(form_classname="title"),
                                ),
                                (
                                    "link_url",
                                    wagtail.blocks.URLBlock(required=False),
                                ),
                                (
                                    "link_page",
                                    wagtail.blocks.PageChooserBlock(required=False),
                                ),
                            ]
                        ),
                    ),
                    ("highlight", bc.utils.blocks.HighlightBlock()),
                    ("inset_text", bc.utils.blocks.InsetTextBlock()),
                    (
                        "accordion",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "items",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        form_classname="full title",
                                                        icon="title",
                                                        label="Accordion title",
                                                    ),
                                                ),
                                                (
                                                    "content",
                                                    wagtail.blocks.StreamBlock(
                                                        [
                                                            (
                                                                "heading",
                                                                wagtail.blocks.CharBlock(
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
                                                                wagtail.blocks.CharBlock(
                                                                    form_classname="full title",
                                                                    group="Heading",
                                                                    help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                                                                    icon="title",
                                                                    template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                                                ),
                                                            ),
                                                            (
                                                                "paragraph",
                                                                wagtail.blocks.RichTextBlock(
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
                                                                wagtail.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "image",
                                                                            wagtail.images.blocks.ImageChooserBlock(),
                                                                        ),
                                                                        (
                                                                            "alt_text",
                                                                            wagtail.blocks.CharBlock(
                                                                                help_text="Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                                                                                required=False,
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "caption",
                                                                            wagtail.blocks.CharBlock(
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
                                                                wagtail.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "heading",
                                                                            wagtail.blocks.RichTextBlock(
                                                                                default="<p><b>Find local information</b></p>",
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
                                                                            "introduction",
                                                                            wagtail.blocks.RichTextBlock(
                                                                                default="<p>While we finish building this new website, we’re keeping some local information on our old council websites</p>",
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
                                                                            "postcode_lookup_text",
                                                                            wagtail.blocks.RichTextBlock(
                                                                                default="<p>Enter your postcode to help us redirect you to the right place.</p>",
                                                                                features=[
                                                                                    "bold",
                                                                                    "italic",
                                                                                    "ol",
                                                                                    "ul",
                                                                                    "link",
                                                                                    "document-link",
                                                                                ],
                                                                                help_text="The text that appears on top of the postcode lookup input",
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "area_lookup_text",
                                                                            wagtail.blocks.RichTextBlock(
                                                                                default="<p>Select your local area to help us direct you to the right place:</p>",
                                                                                features=[
                                                                                    "bold",
                                                                                    "italic",
                                                                                    "ol",
                                                                                    "ul",
                                                                                    "link",
                                                                                    "document-link",
                                                                                ],
                                                                                help_text="The text that appears on top of the list of local area links",
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "aylesbury_vale_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Aylesbury Vale URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "chiltern_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Chiltern URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "south_bucks_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="South Bucks URL"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "wycombe_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Wycombe URL"
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                            (
                                                                "plain_text_table",
                                                                wagtail.contrib.table_block.blocks.TableBlock(
                                                                    group="Table"
                                                                ),
                                                            ),
                                                            (
                                                                "table",
                                                                wagtail.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "table",
                                                                            wagtail.contrib.typed_table_block.blocks.TypedTableBlock(
                                                                                [
                                                                                    (
                                                                                        "left_aligned_column",
                                                                                        wagtail.blocks.StreamBlock(
                                                                                            [
                                                                                                (
                                                                                                    "numeric",
                                                                                                    wagtail.blocks.DecimalBlock(),
                                                                                                ),
                                                                                                (
                                                                                                    "rich_text",
                                                                                                    wagtail.blocks.RichTextBlock(),
                                                                                                ),
                                                                                            ]
                                                                                        ),
                                                                                    ),
                                                                                    (
                                                                                        "right_aligned_column",
                                                                                        wagtail.blocks.StreamBlock(
                                                                                            [
                                                                                                (
                                                                                                    "numeric",
                                                                                                    wagtail.blocks.DecimalBlock(),
                                                                                                ),
                                                                                                (
                                                                                                    "rich_text",
                                                                                                    wagtail.blocks.RichTextBlock(),
                                                                                                ),
                                                                                            ]
                                                                                        ),
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "caption",
                                                                            wagtail.blocks.TextBlock(
                                                                                required=False
                                                                            ),
                                                                        ),
                                                                    ],
                                                                    group="Table",
                                                                ),
                                                            ),
                                                            (
                                                                "button",
                                                                wagtail.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "text",
                                                                            wagtail.blocks.CharBlock(
                                                                                form_classname="title"
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "link_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                required=False
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "link_page",
                                                                            wagtail.blocks.PageChooserBlock(
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
                                                            (
                                                                "inset_text",
                                                                bc.utils.blocks.InsetTextBlock(),
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
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        form_classname="full title",
                                        icon="title",
                                        label="Detail title",
                                    ),
                                ),
                                (
                                    "content",
                                    wagtail.blocks.RichTextBlock(
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
