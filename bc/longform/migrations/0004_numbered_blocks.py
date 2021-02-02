# Generated by Django 2.2.13 on 2020-11-25 07:24

import bc.longform.blocks
import bc.utils.blocks
from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("longform", "0003_add_hero_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="longformpage",
            name="is_numbered",
            field=models.BooleanField(
                default=False,
                help_text='Adds numbers to each chapter, e.g. "1. Introduction"',
            ),
        ),
        migrations.AlterField(
            model_name="longformchapterpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            classname="full title",
                            group="Heading",
                            icon="title",
                            label="Main heading",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
                        ),
                    ),
                    (
                        "subheading",
                        wagtail.core.blocks.CharBlock(
                            classname="full title",
                            group="Heading",
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
                                    wagtail.core.blocks.CharBlock(classname="title"),
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
                        "numbered_heading",
                        bc.longform.blocks.NumberedHeadingBlock(
                            help_text='Adds a number to the heading if is_numbered is not enabled on the long-form content page (e.g. 1. My heading). The link to this heading will be "section-x" where x is the heading number.'
                        ),
                    ),
                    (
                        "numbered_subheading",
                        bc.longform.blocks.NumberedSubheadingBlock(
                            help_text='Adds a number to the subheading (e.g. 1.1. My subheading). The link to this subheading will be "section-x.y" where x is the heading or chapter number, and y is the subheading number.'
                        ),
                    ),
                    (
                        "numbered_paragraph",
                        bc.longform.blocks.NumberedParagraphBlock(
                            help_text='Adds a number before the paragraph (e.g. 1.1.1.). The link to this paragraph will be "section-x.y.z" where x  is the heading or chapter number, y is the subheading number, and z is the paragraph number.'
                        ),
                    ),
                    (
                        "detail",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(
                                        classname="full title",
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
        migrations.AlterField(
            model_name="longformpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            classname="full title",
                            group="Heading",
                            icon="title",
                            label="Main heading",
                            template="patterns/molecules/streamfield/blocks/heading_block.html",
                        ),
                    ),
                    (
                        "subheading",
                        wagtail.core.blocks.CharBlock(
                            classname="full title",
                            group="Heading",
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
                                    wagtail.core.blocks.CharBlock(classname="title"),
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
                        "numbered_heading",
                        bc.longform.blocks.NumberedHeadingBlock(
                            help_text='Adds a number to the heading if is_numbered is not enabled on the long-form content page (e.g. 1. My heading). The link to this heading will be "section-x" where x is the heading number.'
                        ),
                    ),
                    (
                        "numbered_subheading",
                        bc.longform.blocks.NumberedSubheadingBlock(
                            help_text='Adds a number to the subheading (e.g. 1.1. My subheading). The link to this subheading will be "section-x.y" where x is the heading or chapter number, and y is the subheading number.'
                        ),
                    ),
                    (
                        "numbered_paragraph",
                        bc.longform.blocks.NumberedParagraphBlock(
                            help_text='Adds a number before the paragraph (e.g. 1.1.1.). The link to this paragraph will be "section-x.y.z" where x  is the heading or chapter number, y is the subheading number, and z is the paragraph number.'
                        ),
                    ),
                    (
                        "detail",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(
                                        classname="full title",
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
        migrations.AlterField(
            model_name="longformpage",
            name="chapter_heading",
            field=models.CharField(
                blank=True,
                default="Introduction",
                help_text='Optional, e.g. "Introduction", chapter heading that will appear before the body. Is the same level as a main heading',
                max_length=255,
            ),
        ),
    ]
