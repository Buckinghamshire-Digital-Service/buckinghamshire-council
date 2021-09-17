# Generated by Django 2.2.24 on 2021-07-23 00:05

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0009_fullwidthbanner_add_heading"),
    ]

    operations = [
        migrations.RemoveField(model_name="campaignpage", name="sections",),
        migrations.AddField(
            model_name="campaignpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            form_classname="full title",
                            group="Text",
                            help_text='3 required. The link to this heading uses the heading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            icon="title",
                            label="Section heading",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
                        ),
                    ),
                    (
                        "media_with_subheading_and_paragraph",
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
                                        help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                                        max_length=250,
                                        template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["link", "bold", "italic", "ul", "ol"],
                                        icon="pilcrow",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "directory_banner",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("title", wagtail.core.blocks.TextBlock()),
                                ("description", wagtail.core.blocks.TextBlock()),
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
                                        ],
                                        form_classname="struct-block c-sf-block c-sf-block__content-inner",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "full_width_banner",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.core.blocks.CharBlock(max_length=250),
                                ),
                                ("text", wagtail.core.blocks.TextBlock()),
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
                                        ],
                                        form_classname="struct-block c-sf-block c-sf-block__content-inner",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "subheading_and_paragraph",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "subheading",
                                    wagtail.core.blocks.CharBlock(
                                        help_text='The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                                        max_length=250,
                                        template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                    ),
                                ),
                                (
                                    "paragraph",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["link", "bold", "italic", "ul", "ol"],
                                        icon="pilcrow",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph",
                        wagtail.core.blocks.RichTextBlock(
                            features=["link", "bold", "italic", "ul", "ol"],
                            group="Text",
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "media_or_image",
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
                                    wagtail.embeds.blocks.EmbedBlock(required=False),
                                ),
                            ],
                            group="Media",
                            template="patterns/molecules/campaigns/blocks/image-or-media-block.html",
                        ),
                    ),
                ],
                default="",
            ),
            preserve_default=False,
        ),
    ]