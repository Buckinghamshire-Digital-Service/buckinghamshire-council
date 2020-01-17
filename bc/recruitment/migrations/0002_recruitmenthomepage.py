# Generated by Django 2.2.9 on 2020-01-16 07:40

import django.db.models.deletion
from django.db import migrations, models

import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_customimage_file_hash"),
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("recruitment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecruitmentHomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("social_text", models.CharField(blank=True, max_length=255)),
                (
                    "listing_title",
                    models.CharField(
                        blank=True,
                        help_text="Override the page title used when this page appears in listings",
                        max_length=255,
                    ),
                ),
                (
                    "listing_summary",
                    models.CharField(
                        blank=True,
                        help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.",
                        max_length=255,
                    ),
                ),
                (
                    "hero_title",
                    models.CharField(
                        help_text="eg. Finding a job in Buckinghamshire", max_length=255
                    ),
                ),
                (
                    "search_box_placeholder",
                    models.CharField(
                        default="Search jobs, e.g. “Teacher in Aylesbury”",
                        help_text="eg. Search jobs, e.g. “Teacher in Aylesbury”",
                        max_length=255,
                    ),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "content_block",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        ("title", wagtail.core.blocks.CharBlock()),
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
                                    ],
                                    icon="list-ul",
                                ),
                            )
                        ],
                        blank=True,
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
                (
                    "listing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the image you wish to be displayed when this page appears in listings",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page", models.Model),
        ),
    ]
