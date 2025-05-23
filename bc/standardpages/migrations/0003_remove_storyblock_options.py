# Generated by Django 2.2.7 on 2019-12-09 15:41

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("standardpages", "0002_remove_infomationpage_intro"),
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
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                ]
            ),
        ),
    ]
