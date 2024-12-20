# Generated by Django 4.2.14 on 2024-11-19 16:53

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("promotional", "0024_alter_promotionalsiteconfiguration_primary_navigation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="promotionalcontentpage",
            name="hero_link_page",
        ),
        migrations.RemoveField(
            model_name="promotionalcontentpage",
            name="hero_link_text",
        ),
        migrations.AddField(
            model_name="promotionalcontentpage",
            name="hero_link",
            field=wagtail.fields.StreamField(
                [
                    (
                        "external_link",
                        wagtail.blocks.StructBlock(
                            [
                                ("url", wagtail.blocks.URLBlock()),
                                ("title", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    (
                        "internal_link",
                        wagtail.blocks.StructBlock(
                            [
                                ("page", wagtail.blocks.PageChooserBlock()),
                                ("title", wagtail.blocks.CharBlock(required=False)),
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
