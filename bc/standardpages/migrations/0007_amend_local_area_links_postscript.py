# Generated by Django 2.2.9 on 2020-01-17 10:58

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("standardpages", "0006_update_local_area_links_default_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="informationpage",
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
                ]
            ),
        ),
    ]
