# Generated by Django 3.2.9 on 2022-05-04 12:23

from django.db import migrations

import wagtail.contrib.table_block.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks

import bc.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0025_merge_20220504_1314"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspage",
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
                                    "heading",
                                    wagtail.core.blocks.RichTextBlock(
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
                                    wagtail.core.blocks.RichTextBlock(
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
                                    wagtail.core.blocks.RichTextBlock(
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
                                    wagtail.core.blocks.RichTextBlock(
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
                    (
                        "table",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "table",
                                    wagtail.contrib.typed_table_block.blocks.TypedTableBlock(
                                        [
                                            (
                                                "left_aligned_column",
                                                wagtail.core.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "numeric",
                                                            wagtail.core.blocks.DecimalBlock(),
                                                        ),
                                                        (
                                                            "rich_text",
                                                            wagtail.core.blocks.RichTextBlock(),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "right_aligned_column",
                                                wagtail.core.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "numeric",
                                                            wagtail.core.blocks.DecimalBlock(),
                                                        ),
                                                        (
                                                            "rich_text",
                                                            wagtail.core.blocks.RichTextBlock(),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.TextBlock(required=False),
                                ),
                            ]
                        ),
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
                    ("inset_text", bc.utils.blocks.InsetTextBlock()),
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
                                                                            "heading",
                                                                            wagtail.core.blocks.RichTextBlock(
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
                                                                            wagtail.core.blocks.RichTextBlock(
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
                                                                            wagtail.core.blocks.RichTextBlock(
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
                                                                            wagtail.core.blocks.RichTextBlock(
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
                ]
            ),
        ),
    ]
