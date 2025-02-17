# Generated by Django 1.10.7 on 2017-04-14 09:44

import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("images", "0001_initial"),
        ("wagtailcore", "0032_add_bulk_delete_page_permission"),
        ("wagtaildocs", "0007_merge"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventIndexPage",
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
                ("social_text", models.CharField(blank=True, max_length=255)),
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
                    "listing_summary",
                    models.CharField(
                        blank=True,
                        help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.",
                        max_length=255,
                    ),
                ),
                (
                    "listing_title",
                    models.CharField(
                        blank=True,
                        help_text="Override the page title used when this page appears in listings",
                        max_length=255,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="EventPage",
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
                ("start_date", models.DateField()),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
                (
                    "street_address_1",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Street Address 1"
                    ),
                ),
                (
                    "street_address_2",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Street Address 2"
                    ),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=255, verbose_name="City"),
                ),
                (
                    "region",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="State or county"
                    ),
                ),
                (
                    "postcode",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Zip or postal code"
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Country"
                    ),
                ),
                ("introduction", models.TextField(blank=True)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        (
                            (
                                "heading",
                                wagtail.blocks.CharBlock(
                                    classname="full title",
                                    icon="title",
                                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                                ),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock()),
                            (
                                "image",
                                wagtail.blocks.StructBlock(
                                    (
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    )
                                ),
                            ),
                            (
                                "quote",
                                wagtail.blocks.StructBlock(
                                    (
                                        (
                                            "quote",
                                            wagtail.blocks.CharBlock(classname="title"),
                                        ),
                                        (
                                            "attribution",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    )
                                ),
                            ),
                            ("embed", wagtail.embeds.blocks.EmbedBlock()),
                            (
                                "call_to_action",
                                wagtail.snippets.blocks.SnippetChooserBlock(
                                    "utils.CallToActionSnippet",
                                    template="patterns/molecules/streamfield/blocks/call_to_action_block.html",
                                ),
                            ),
                            (
                                "document",
                                wagtail.blocks.StructBlock(
                                    (
                                        (
                                            "document",
                                            wagtail.documents.blocks.DocumentChooserBlock(),
                                        ),
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    )
                                ),
                            ),
                        )
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
            options={"abstract": False},
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="EventPageEventType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
        ),
        migrations.CreateModel(
            name="EventPageRelatedPage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "source_page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_pages",
                        to="events.EventPage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False},
        ),
        migrations.CreateModel(
            name="EventType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="eventpageeventtype",
            name="event_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="events.EventType"
            ),
        ),
        migrations.AddField(
            model_name="eventpageeventtype",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="event_types",
                to="events.EventPage",
            ),
        ),
    ]
