# Generated by Django 2.2.10 on 2020-03-05 09:33

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inlineindex", "0005_add_table_block"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inlineindex",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.CharBlock(
                            classname="full title",
                            icon="title",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
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
                                (
                                    "postscript",
                                    wagtail.blocks.RichTextBlock(
                                        default='<p>Or <a href="https://www.gov.uk/find-local-council">find your area based on your postcode</a>.</p>',
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                        required=False,
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
                ]
            ),
        ),
        migrations.AlterField(
            model_name="inlineindexchild",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.CharBlock(
                            classname="full title",
                            icon="title",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
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
                                (
                                    "postscript",
                                    wagtail.blocks.RichTextBlock(
                                        default='<p>Or <a href="https://www.gov.uk/find-local-council">find your area based on your postcode</a>.</p>',
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                        ],
                                        required=False,
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
                ]
            ),
        ),
    ]
