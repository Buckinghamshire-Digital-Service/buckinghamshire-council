# Generated by Django 2.2.19 on 2021-03-15 12:18

from django.db import migrations

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0002_campaignpage_sections"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignpage",
            name="sections",
            field=wagtail.fields.StreamField(
                [
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        form_classname="full title"
                                    ),
                                ),
                                (
                                    "intro",
                                    wagtail.blocks.RichTextBlock(features=["link"]),
                                ),
                                (
                                    "content",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(),
                                                ),
                                                (
                                                    "subheading",
                                                    wagtail.blocks.CharBlock(
                                                        max_length=250,
                                                        template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                                    ),
                                                ),
                                                (
                                                    "paragraph",
                                                    wagtail.blocks.RichTextBlock(
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
