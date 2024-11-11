# Generated by Django 2.2.13 on 2020-10-27 04:49

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("navigation", "0002_remove_pri_sec_footer_navs"),
    ]

    operations = [
        migrations.AddField(
            model_name="navigationsettings",
            name="footer_columns",
            field=wagtail.fields.StreamField(
                [
                    (
                        "column",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading",
                                    wagtail.blocks.CharBlock(
                                        help_text="Leave blank if no header required.",
                                        required=False,
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
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                default="",
            ),
            preserve_default=False,
        ),
    ]
