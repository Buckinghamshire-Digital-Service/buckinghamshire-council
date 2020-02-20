# Generated by Django 2.2.10 on 2020-02-20 09:55

from django.db import migrations

import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0010_add_hero_link_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruitmentindexpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            classname="full title",
                            icon="title",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
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
                        "local_area_links",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "introduction",
                                    wagtail.core.blocks.RichTextBlock(
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
                                    wagtail.core.blocks.URLBlock(
                                        label="Aylesbury Vale URL", required=False
                                    ),
                                ),
                                (
                                    "chiltern_url",
                                    wagtail.core.blocks.URLBlock(
                                        label="Chiltern URL", required=False
                                    ),
                                ),
                                (
                                    "south_bucks_url",
                                    wagtail.core.blocks.URLBlock(
                                        label="South Bucks URL", required=False
                                    ),
                                ),
                                (
                                    "wycombe_url",
                                    wagtail.core.blocks.URLBlock(
                                        label="Wycombe URL", required=False
                                    ),
                                ),
                                (
                                    "postscript",
                                    wagtail.core.blocks.RichTextBlock(
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
                ],
                blank=True,
            ),
        ),
    ]
