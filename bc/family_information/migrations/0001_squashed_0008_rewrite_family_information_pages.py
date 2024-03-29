# Generated by Django 2.2.13 on 2020-10-27 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("family_information", "0001_initial"),
        ("family_information", "0002_auto_20200512_2324"),
        ("family_information", "0003_auto_20200512_2333"),
        ("family_information", "0004_auto_20200512_2343"),
        ("family_information", "0005_auto_20200512_2346"),
        ("family_information", "0006_familyinformationhomepage_links_image"),
        ("family_information", "0007_set_null_on_link_page_deletion"),
        ("family_information", "0008_rewrite_family_information_pages"),
    ]

    initial = True

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("utils", "0004_add_important_pages_settings"),
        ("images", "0003_job_employer_logo"),
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
    ]

    operations = [
        migrations.CreateModel(
            name="FamilyInformationHomePage",
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
                (
                    "call_to_action",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="utils.CallToActionSnippet",
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
                ("banner_description", models.TextField(default="")),
                (
                    "banner_image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
                ("banner_link", models.URLField(default="")),
                ("banner_link_text", models.CharField(blank=True, max_length=100)),
                ("banner_title", models.TextField(default="")),
                ("description", models.TextField(blank=True)),
                ("search_placeholder", models.CharField(blank=True, max_length=100)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="CategoryTypeOnePage",
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
                ("banner_title", models.TextField()),
                ("banner_description", models.TextField()),
                ("banner_link", models.URLField()),
                ("banner_link_text", models.CharField(blank=True, max_length=100)),
                (
                    "banner_image",
                    models.ForeignKey(
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
        migrations.CreateModel(
            name="CategoryTypeTwoPage",
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
                ("banner_title", models.TextField()),
                ("banner_description", models.TextField()),
                ("banner_link", models.URLField()),
                ("banner_link_text", models.CharField(blank=True, max_length=100)),
                (
                    "banner_image",
                    models.ForeignKey(
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
