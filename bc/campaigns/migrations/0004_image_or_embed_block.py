# Generated by Django 2.2.19 on 2021-03-16 04:50

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0003_add_section_content_blocks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignpage",
            name="sections",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.core.blocks.CharBlock(
                                        form_classname="full title",
                                        template="patterns/molecules/streamfield/blocks/heading_block.html",
                                    ),
                                ),
                                (
                                    "intro",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["link"]
                                    ),
                                ),
                                (
                                    "content",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "image_or_embed",
                                                    wagtail.core.blocks.StructBlock(
                                                        [
                                                            (
                                                                "image",
                                                                wagtail.images.blocks.ImageChooserBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "embed",
                                                                wagtail.embeds.blocks.EmbedBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                        ],
                                                        form_classname="struct-block c-sf-block c-sf-block__content-inner",
                                                    ),
                                                ),
                                                (
                                                    "subheading",
                                                    wagtail.core.blocks.CharBlock(
                                                        max_length=250,
                                                        template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                                    ),
                                                ),
                                                (
                                                    "paragraph",
                                                    wagtail.core.blocks.RichTextBlock(
                                                        features=["link"]
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                null=True,
            ),
        ),
    ]