# Generated by Django 2.2.13 on 2020-11-02 21:45

from django.db import migrations

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0038_merge_20201007_1224"),
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
                            classname="full title",
                            group="Heading",
                            icon="title",
                            label="Main heading",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
                        ),
                    ),
                    (
                        "subheading",
                        wagtail.blocks.CharBlock(
                            classname="full title",
                            group="Heading",
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
                                    "introduction",
                                    wagtail.blocks.RichTextBlock(
                                        default="<p>Select your local area for information:</p>",
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
                                    wagtail.blocks.URLBlock(
                                        label="Aylesbury Vale URL", required=False
                                    ),
                                ),
                                (
                                    "chiltern_url",
                                    wagtail.blocks.URLBlock(
                                        label="Chiltern URL", required=False
                                    ),
                                ),
                                (
                                    "south_bucks_url",
                                    wagtail.blocks.URLBlock(
                                        label="South Bucks URL", required=False
                                    ),
                                ),
                                (
                                    "wycombe_url",
                                    wagtail.blocks.URLBlock(
                                        label="Wycombe URL", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                    (
                        "button",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.CharBlock(classname="title"),
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
                                                        classname="full title",
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
                                                                    classname="full title",
                                                                    group="Heading",
                                                                    icon="title",
                                                                    label="Main heading",
                                                                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                                                                ),
                                                            ),
                                                            (
                                                                "subheading",
                                                                wagtail.blocks.CharBlock(
                                                                    classname="full title",
                                                                    group="Heading",
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
                                                                            "introduction",
                                                                            wagtail.blocks.RichTextBlock(
                                                                                default="<p>Select your local area for information:</p>",
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
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Aylesbury Vale URL",
                                                                                required=False,
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "chiltern_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Chiltern URL",
                                                                                required=False,
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "south_bucks_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="South Bucks URL",
                                                                                required=False,
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "wycombe_url",
                                                                            wagtail.blocks.URLBlock(
                                                                                label="Wycombe URL",
                                                                                required=False,
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
                                                                wagtail.blocks.StructBlock(
                                                                    [
                                                                        (
                                                                            "text",
                                                                            wagtail.blocks.CharBlock(
                                                                                classname="title"
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
                                        classname="full title",
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
