# Generated by Django 2.2.24 on 2021-10-26 13:54

import django.db.models.deletion
from django.db import migrations, models

import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0062_comment_models_and_pagesubscription"),
        ("images", "0003_job_employer_logo"),
    ]

    operations = [
        migrations.CreateModel(
            name="StepByStepIndexPage",
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
                        help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                        max_length=255,
                    ),
                ),
                (
                    "redirect_to",
                    models.URLField(
                        blank=True,
                        help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                        verbose_name="Redirect to external URL",
                    ),
                ),
                (
                    "show_live_chat_client",
                    models.BooleanField(
                        default=False,
                        help_text="Show live chat support client on this page",
                    ),
                ),
                ("introduction", wagtail.core.fields.RichTextField()),
                (
                    "steps",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "step",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        ("heading", wagtail.core.blocks.TextBlock()),
                                        (
                                            "information",
                                            wagtail.core.blocks.StreamBlock(
                                                [
                                                    (
                                                        "paragraph",
                                                        wagtail.core.blocks.TextBlock(
                                                            template="patterns/molecules/step_by_step/blocks/paragraph-block.html"
                                                        ),
                                                    ),
                                                    (
                                                        "external_link",
                                                        wagtail.core.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "url",
                                                                    wagtail.core.blocks.URLBlock(),
                                                                ),
                                                                (
                                                                    "title",
                                                                    wagtail.core.blocks.CharBlock(),
                                                                ),
                                                            ],
                                                            icon="link",
                                                            template="patterns/molecules/step_by_step/blocks/external-link-block.html",
                                                        ),
                                                    ),
                                                    (
                                                        "internal_link",
                                                        wagtail.core.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "page",
                                                                    wagtail.core.blocks.PageChooserBlock(),
                                                                ),
                                                                (
                                                                    "title",
                                                                    wagtail.core.blocks.CharBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                            ],
                                                            icon="link",
                                                            template="patterns/molecules/step_by_step/blocks/internal-link-block.html",
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ]
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
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
    ]